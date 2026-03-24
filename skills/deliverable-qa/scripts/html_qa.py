#!/usr/bin/env python3
"""
Deliverable QA — programmatic quality checks for HTML deliverables.

Checks accessibility (WCAG AA), print readiness, and structural integrity.
Outputs a JSON report to stdout.

Usage:
    python html_qa.py <path-to-html-file>
    python html_qa.py <path-to-html-file> --fix  (apply auto-fixes and write back)
"""

import sys
import json
import re
import math
from pathlib import Path
from html.parser import HTMLParser


# ---------------------------------------------------------------------------
# Color contrast utilities
# ---------------------------------------------------------------------------

def hex_to_rgb(hex_color):
    """Convert hex color (#fff, #ffffff, #ffffffff) to (r, g, b) tuple."""
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    elif len(h) == 8:
        h = h[:6]  # strip alpha
    if len(h) != 6:
        return None
    try:
        return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return None


def relative_luminance(rgb):
    """WCAG 2.1 relative luminance."""
    vals = []
    for c in rgb:
        s = c / 255.0
        vals.append(s / 12.92 if s <= 0.04045 else ((s + 0.055) / 1.055) ** 2.4)
    return 0.2126 * vals[0] + 0.7152 * vals[1] + 0.0722 * vals[2]


def contrast_ratio(rgb1, rgb2):
    """WCAG contrast ratio between two RGB tuples."""
    l1 = relative_luminance(rgb1)
    l2 = relative_luminance(rgb2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def darken_to_meet_ratio(bg_rgb, target_ratio=4.5):
    """Find the lightest gray text color that meets target_ratio against bg_rgb."""
    for v in range(128, -1, -1):
        candidate = (v, v, v)
        if contrast_ratio(candidate, bg_rgb) >= target_ratio:
            return "#{:02x}{:02x}{:02x}".format(v, v, v)
    return "#000000"


# ---------------------------------------------------------------------------
# Named CSS colors (common subset used in deliverables)
# ---------------------------------------------------------------------------

NAMED_COLORS = {
    "white": (255, 255, 255), "black": (0, 0, 0),
    "red": (255, 0, 0), "green": (0, 128, 0), "blue": (0, 0, 255),
    "gray": (128, 128, 128), "grey": (128, 128, 128),
    "silver": (192, 192, 192), "navy": (0, 0, 128),
    "teal": (0, 128, 128), "orange": (255, 165, 0),
    "yellow": (255, 255, 0), "purple": (128, 0, 128),
    "transparent": None,
}


def parse_color(color_str):
    """Parse a CSS color string to (r, g, b) or None."""
    if not color_str:
        return None
    color_str = color_str.strip().lower()
    if color_str in NAMED_COLORS:
        return NAMED_COLORS[color_str]
    if color_str.startswith("#"):
        return hex_to_rgb(color_str)
    m = re.match(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)", color_str)
    if m:
        return (int(m.group(1)), int(m.group(2)), int(m.group(3)))
    return None


# ---------------------------------------------------------------------------
# HTML Parser for structural analysis
# ---------------------------------------------------------------------------

class DocAnalyzer(HTMLParser):
    def __init__(self):
        super().__init__()
        self.issues = []
        self.line_num = 0

        # Heading tracking
        self.headings = []  # (level, line, text)
        self.in_heading = False
        self.current_heading_level = 0
        self.current_heading_text = ""

        # Image tracking
        self.images = []  # (line, alt, has_role_presentation)

        # Form tracking — handles both explicit (for/id) and implicit (label wraps input) association
        self.inputs = []  # (line, id, has_aria_label)
        self.label_fors = set()
        self.in_label = False  # tracks whether we're inside a <label> element
        self.label_contains_input = False  # tracks if current label wraps an input
        self.recent_label_line = 0  # line of most recently closed label (for sibling detection)
        self.recent_label_had_for = False  # whether that label had a for attribute

        # Link tracking
        self.links = []  # (line, text, href)
        self.in_link = False
        self.current_link_text = ""
        self.current_link_href = ""
        self.current_link_line = 0

        # Landmark tracking
        self.has_main = False
        self.has_header = False

        # Structural
        self.has_doctype = False
        self.has_charset = False
        self.has_viewport = False
        self.anchor_ids = set()
        self.anchor_hrefs = []  # internal links

        # Style content
        self.in_style = False
        self.style_content = ""

        # Section tracking for empty section detection
        self.sections = []  # (heading_line, heading_text, has_content)
        self.content_after_heading = False
        self.last_heading_line = 0

    def handle_decl(self, decl):
        if "doctype" in decl.lower():
            self.has_doctype = True

    def handle_starttag(self, tag, attrs):
        self.line_num = self.getpos()[0]
        attr_dict = dict(attrs)

        # Track IDs for anchor resolution
        if "id" in attr_dict:
            self.anchor_ids.add(attr_dict["id"])

        # Headings
        if re.match(r"^h[1-6]$", tag):
            self.in_heading = True
            self.current_heading_level = int(tag[1])
            self.current_heading_text = ""

            # Check if previous section had content
            if self.sections and not self.content_after_heading:
                self.sections[-1] = (*self.sections[-1][:2], False)

            self.content_after_heading = False
            self.last_heading_line = self.line_num

        # Images
        elif tag == "img":
            alt = attr_dict.get("alt")
            role = attr_dict.get("role", "")
            if alt is None:
                self.issues.append({
                    "category": "accessibility",
                    "severity": "error",
                    "rule": "image-alt",
                    "message": f"Image missing alt attribute",
                    "line": self.line_num,
                    "fix_hint": "Add alt=\"descriptive text\" or alt=\"\" role=\"presentation\" for decorative images"
                })
            self.images.append((self.line_num, alt, role == "presentation"))

        # Form elements
        elif tag in ("input", "select", "textarea"):
            input_type = attr_dict.get("type", "text")
            if input_type in ("hidden", "submit", "button", "reset"):
                pass  # skip these
            else:
                has_label = bool(attr_dict.get("aria-label") or attr_dict.get("aria-labelledby") or attr_dict.get("title"))
                # Implicit association: input is wrapped inside a <label>
                if self.in_label:
                    has_label = True
                    self.label_contains_input = True
                # Sibling association: a <label> element appeared just before this input
                # (within 5 lines — covers the common pattern of label + input in a wrapper div)
                elif self.recent_label_line > 0 and (self.line_num - self.recent_label_line) <= 5:
                    has_label = True
                input_id = attr_dict.get("id", "")
                self.inputs.append((self.line_num, input_id, has_label))

        elif tag == "label":
            for_val = attr_dict.get("for", "")
            if for_val:
                self.label_fors.add(for_val)
            self.in_label = True
            self.label_contains_input = False

        # Links
        elif tag == "a":
            self.in_link = True
            self.current_link_text = ""
            self.current_link_href = attr_dict.get("href", "")
            self.current_link_line = self.line_num
            if self.current_link_href.startswith("#"):
                self.anchor_hrefs.append((self.line_num, self.current_link_href[1:]))

        # Landmarks
        elif tag == "main":
            self.has_main = True
        elif tag == "header":
            self.has_header = True

        # Meta tags
        elif tag == "meta":
            if "charset" in attr_dict:
                self.has_charset = True
            content = attr_dict.get("content", "")
            http_equiv = attr_dict.get("http-equiv", "")
            if http_equiv.lower() == "content-type" and "charset" in content.lower():
                self.has_charset = True
            name = attr_dict.get("name", "")
            if name.lower() == "viewport":
                self.has_viewport = True

        # Style
        elif tag == "style":
            self.in_style = True

        # Track content after headings
        elif not self.in_heading and self.last_heading_line > 0:
            if tag not in ("br", "hr"):
                self.content_after_heading = True

    def handle_endtag(self, tag):
        if re.match(r"^h[1-6]$", tag) and self.in_heading:
            self.in_heading = False
            self.headings.append((self.current_heading_level, self.last_heading_line, self.current_heading_text.strip()))
            self.sections.append((self.last_heading_line, self.current_heading_text.strip(), None))

        elif tag == "label":
            self.in_label = False
            self.recent_label_line = self.getpos()[0]

        elif tag == "a" and self.in_link:
            self.in_link = False
            text = self.current_link_text.strip().lower()
            if text in ("click here", "here", "read more", "more", "link"):
                self.issues.append({
                    "category": "accessibility",
                    "severity": "warning",
                    "rule": "link-text",
                    "message": f"Non-descriptive link text: \"{self.current_link_text.strip()}\"",
                    "line": self.current_link_line,
                    "fix_hint": "Use descriptive text that makes sense out of context"
                })
            self.links.append((self.current_link_line, self.current_link_text.strip(), self.current_link_href))

        elif tag == "style":
            self.in_style = False

    def handle_data(self, data):
        if self.in_heading:
            self.current_heading_text += data
        if self.in_link:
            self.current_link_text += data
        if self.in_style:
            self.style_content += data

        # Track non-whitespace content after headings
        if not self.in_heading and data.strip() and self.last_heading_line > 0:
            self.content_after_heading = True

    def finalize(self):
        """Run post-parse checks and return all issues."""

        # Heading hierarchy
        if self.headings:
            h1_count = sum(1 for h in self.headings if h[0] == 1)
            if h1_count == 0:
                self.issues.append({
                    "category": "accessibility",
                    "severity": "warning",
                    "rule": "heading-hierarchy",
                    "message": "Document has no h1 element",
                    "line": 1,
                    "fix_hint": "Add a single h1 as the document title"
                })
            elif h1_count > 1:
                self.issues.append({
                    "category": "accessibility",
                    "severity": "warning",
                    "rule": "heading-hierarchy",
                    "message": f"Document has {h1_count} h1 elements (expected 1)",
                    "line": self.headings[1][1] if len(self.headings) > 1 else 1,
                    "fix_hint": "Use a single h1 for the document title; use h2+ for sections"
                })

            prev_level = 0
            for level, line, text in self.headings:
                if prev_level > 0 and level > prev_level + 1:
                    self.issues.append({
                        "category": "accessibility",
                        "severity": "warning",
                        "rule": "heading-hierarchy",
                        "message": f"Heading level skips from h{prev_level} to h{level}: \"{text}\"",
                        "line": line,
                        "fix_hint": f"Use h{prev_level + 1} instead of h{level}"
                    })
                prev_level = level

        # Form labels
        for line, input_id, has_aria_label in self.inputs:
            if not has_aria_label and input_id not in self.label_fors:
                self.issues.append({
                    "category": "accessibility",
                    "severity": "error",
                    "rule": "form-label",
                    "message": "Form input without associated label",
                    "line": line,
                    "fix_hint": "Add aria-label=\"...\" or a <label for=\"...\"> element"
                })

        # Broken anchor links
        for line, anchor_id in self.anchor_hrefs:
            if anchor_id and anchor_id not in self.anchor_ids:
                self.issues.append({
                    "category": "structure",
                    "severity": "error",
                    "rule": "broken-anchor",
                    "message": f"Internal link #{anchor_id} has no matching id in the document",
                    "line": line,
                    "fix_hint": f"Add id=\"{anchor_id}\" to the target element or fix the href"
                })

        # Structural checks
        if not self.has_doctype:
            self.issues.append({
                "category": "structure",
                "severity": "warning",
                "rule": "doctype",
                "message": "Missing <!DOCTYPE html> declaration",
                "line": 1,
                "fix_hint": "Add <!DOCTYPE html> as the first line"
            })
        if not self.has_charset:
            self.issues.append({
                "category": "structure",
                "severity": "warning",
                "rule": "charset",
                "message": "Missing character encoding declaration",
                "line": 1,
                "fix_hint": "Add <meta charset=\"UTF-8\"> in the <head>"
            })
        if not self.has_viewport:
            self.issues.append({
                "category": "structure",
                "severity": "warning",
                "rule": "viewport",
                "message": "Missing viewport meta tag",
                "line": 1,
                "fix_hint": "Add <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
            })

        # Landmark check
        if not self.has_main:
            self.issues.append({
                "category": "accessibility",
                "severity": "warning",
                "rule": "landmarks",
                "message": "Document has no <main> landmark element",
                "line": 1,
                "fix_hint": "Wrap primary content in a <main> element"
            })

        # Empty sections
        if self.sections:
            # Finalize last section
            if not self.content_after_heading:
                self.sections[-1] = (*self.sections[-1][:2], False)
            else:
                self.sections[-1] = (*self.sections[-1][:2], True)

            for line, text, has_content in self.sections:
                if has_content is False:
                    self.issues.append({
                        "category": "structure",
                        "severity": "warning",
                        "rule": "empty-section",
                        "message": f"Section appears empty: \"{text}\"",
                        "line": line,
                        "fix_hint": "Add content below this heading or remove the section"
                    })

        return self.issues


# ---------------------------------------------------------------------------
# CSS / Print checks (regex-based on style content)
# ---------------------------------------------------------------------------

def check_print_readiness(style_content, full_html):
    """Check print CSS rules."""
    issues = []

    # @page rule with landscape
    if not re.search(r"@page\s*\{[^}]*size\s*:\s*landscape", style_content, re.DOTALL):
        issues.append({
            "category": "print",
            "severity": "error",
            "rule": "page-landscape",
            "message": "Missing @page rule with landscape orientation",
            "line": 0,
            "fix_hint": "Add @page { size: landscape; margin: 0.4in 0.5in; }"
        })

    # Print color adjust
    has_webkit = "print-color-adjust" in style_content or "-webkit-print-color-adjust" in style_content
    if not has_webkit:
        issues.append({
            "category": "print",
            "severity": "error",
            "rule": "color-adjust",
            "message": "Missing print-color-adjust or -webkit-print-color-adjust",
            "line": 0,
            "fix_hint": "Add -webkit-print-color-adjust: exact; print-color-adjust: exact;"
        })

    # @media print block
    if "@media print" not in style_content:
        issues.append({
            "category": "print",
            "severity": "error",
            "rule": "media-print",
            "message": "No @media print block found",
            "line": 0,
            "fix_hint": "Add a @media print { ... } block with print-specific styles"
        })

    # Dangerous page breaks on sections
    dangerous_breaks = re.findall(
        r"(\.section[^{]*|section[^{]*)\{[^}]*(page-break-(?:before|after)\s*:\s*always)[^}]*\}",
        style_content, re.DOTALL
    )
    for selector, rule in dangerous_breaks:
        issues.append({
            "category": "print",
            "severity": "error",
            "rule": "forced-page-break",
            "message": f"Forced page break on section element may cause blank pages: {rule.strip()}",
            "line": 0,
            "fix_hint": "Remove page-break-before/after: always from section elements; let content flow naturally"
        })

    # Grid print fallback check
    grid_classes = re.findall(r"\.([\w-]*grid[\w-]*)\s*\{[^}]*display\s*:\s*grid", style_content, re.DOTALL)
    if grid_classes:
        media_print_match = re.search(r"@media\s+print\s*\{(.*?)\}\s*\}", style_content, re.DOTALL)
        media_print_content = media_print_match.group(1) if media_print_match else ""
        for grid_class in grid_classes:
            if grid_class == "erd-grid":
                continue  # ERD grid is fine as-is per doc-css-framework
            if grid_class not in media_print_content:
                issues.append({
                    "category": "print",
                    "severity": "warning",
                    "rule": "grid-print-fallback",
                    "message": f"Grid container .{grid_class} has no print fallback to block layout",
                    "line": 0,
                    "fix_hint": f"Add .{grid_class} {{ display: block !important; }} inside @media print"
                })

    # break-inside on cards
    card_classes = re.findall(r"\.([\w-]*card[\w-]*)\s*\{", style_content)
    if card_classes:
        has_break_inside = "break-inside" in style_content
        if not has_break_inside:
            issues.append({
                "category": "print",
                "severity": "warning",
                "rule": "card-break-inside",
                "message": "Card elements found but no break-inside: avoid rule detected",
                "line": 0,
                "fix_hint": "Add break-inside: avoid; page-break-inside: avoid; to card elements"
            })

    return issues


# ---------------------------------------------------------------------------
# Color contrast checks (extract from CSS variables and inline styles)
# ---------------------------------------------------------------------------

def extract_css_colors(style_content):
    """Extract CSS custom property color definitions."""
    colors = {}
    # Match --variable: #hex or --variable: rgb(...)
    for match in re.finditer(r"--([\w-]+)\s*:\s*(#[0-9a-fA-F]{3,8}|rgb\([^)]+\))", style_content):
        name = match.group(1)
        rgb = parse_color(match.group(2))
        if rgb:
            colors[name] = rgb
    return colors


def check_contrast(style_content):
    """Check color contrast for common text/background combinations."""
    issues = []
    colors = extract_css_colors(style_content)

    # Common pairings to check in doc deliverables
    pairings = [
        # (text_var_or_color, bg_var_or_color, context)
        ("text", "bg", "body text on background"),
        ("text-secondary", "bg", "secondary text on background"),
        ("text-light", "bg", "light text on background"),
    ]

    # Also check explicit color declarations in rules
    # Look for patterns like: color: #xxx; ... background: #yyy
    rule_blocks = re.findall(r"\{([^}]+)\}", style_content)
    for block in rule_blocks:
        fg_match = re.search(r"(?:^|;)\s*color\s*:\s*(#[0-9a-fA-F]{3,8}|rgb\([^)]+\))", block)
        bg_match = re.search(r"background(?:-color)?\s*:\s*(#[0-9a-fA-F]{3,8}|rgb\([^)]+\))", block)
        if fg_match and bg_match:
            fg_rgb = parse_color(fg_match.group(1))
            bg_rgb = parse_color(bg_match.group(1))
            if fg_rgb and bg_rgb:
                ratio = contrast_ratio(fg_rgb, bg_rgb)
                if ratio < 4.5:
                    fix_color = darken_to_meet_ratio(bg_rgb)
                    issues.append({
                        "category": "accessibility",
                        "severity": "error",
                        "rule": "color-contrast",
                        "message": f"Text '{fg_match.group(1)}' on background '{bg_match.group(1)}' has contrast ratio {ratio:.1f}:1 (needs 4.5:1)",
                        "line": 0,
                        "fix_hint": f"Darken text to at least {fix_color}"
                    })

    # Check CSS variable pairings
    for text_var, bg_var, context in pairings:
        fg_rgb = colors.get(text_var)
        bg_rgb = colors.get(bg_var)
        if fg_rgb and bg_rgb:
            ratio = contrast_ratio(fg_rgb, bg_rgb)
            if ratio < 4.5:
                fix_color = darken_to_meet_ratio(bg_rgb)
                issues.append({
                    "category": "accessibility",
                    "severity": "error",
                    "rule": "color-contrast",
                    "message": f"CSS variable --{text_var} on --{bg_var} ({context}) has contrast ratio {ratio:.1f}:1 (needs 4.5:1)",
                    "line": 0,
                    "fix_hint": f"Darken --{text_var} to at least {fix_color}"
                })

    return issues


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_checks(html_path):
    """Run all checks against an HTML file and return the report."""
    html_content = Path(html_path).read_text(encoding="utf-8")

    # Parse HTML structure
    analyzer = DocAnalyzer()

    # Check for doctype before feeding to parser (parser doesn't handle it well)
    if html_content.strip().lower().startswith("<!doctype"):
        analyzer.has_doctype = True

    analyzer.feed(html_content)
    issues = analyzer.finalize()

    # Extract all style content (parser collected inline <style> tags)
    style_content = analyzer.style_content

    # Also grab any style attributes for completeness
    # (the structural parser handles inline checks)

    # Print readiness
    issues.extend(check_print_readiness(style_content, html_content))

    # Color contrast
    issues.extend(check_contrast(style_content))

    # Deduplicate by (rule, line, message)
    seen = set()
    deduped = []
    for issue in issues:
        key = (issue["rule"], issue["line"], issue["message"])
        if key not in seen:
            seen.add(key)
            deduped.append(issue)

    # Build report
    errors = [i for i in deduped if i["severity"] == "error"]
    warnings = [i for i in deduped if i["severity"] == "warning"]

    report = {
        "passed": len(errors) == 0,
        "total_checks": 14,  # total rule categories checked
        "errors": len(errors),
        "warnings": len(warnings),
        "issues": deduped,
    }

    return report


def main():
    if len(sys.argv) < 2:
        print("Usage: python html_qa.py <path-to-html-file>", file=sys.stderr)
        sys.exit(1)

    html_path = sys.argv[1]
    if not Path(html_path).exists():
        print(json.dumps({"error": f"File not found: {html_path}"}))
        sys.exit(1)

    report = run_checks(html_path)
    print(json.dumps(report, indent=2))

    # Exit code: 1 if errors found, 0 if clean (warnings don't fail)
    sys.exit(1 if not report["passed"] else 0)


if __name__ == "__main__":
    main()
