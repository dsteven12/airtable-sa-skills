---
name: deliverable-qa
description: "Quality gate for HTML deliverables before sharing with customers. Runs accessibility, print-readiness, semantic structure, and content quality checks against generated HTML documents. MANDATORY TRIGGERS: QA check, quality check, check this doc, review before sending, pre-delivery check, accessibility check, verify the doc, is this ready to send, final review. ALWAYS invoke this skill after generating any HTML deliverable (workflow-doc, technical-design-doc, training-guide) and before presenting the file to the user. Also invoke when the user asks to verify or audit an existing HTML document for quality issues."
---

# Deliverable QA

Post-generation quality gate for HTML deliverables. This skill catches accessibility violations, print layout problems, content quality issues, and brand consistency gaps before a document reaches the customer.

## When This Runs

This skill sits at the end of the doc-generation pipeline. The typical flow:

1. A doc-generating skill (workflow-doc, technical-design-doc, training-guide) produces an HTML file
2. **This skill runs against that file before it's presented to the user**
3. Issues get fixed inline, then the file is delivered

It can also be invoked standalone against any HTML file the user wants verified.

## Verification Process

Run checks in two phases: programmatic (script-based, objective) and judgmental (Claude review, subjective). Both phases must pass before delivery.

### Phase 1: Programmatic Checks

Run the bundled verification script against the HTML file:

```bash
python <skill-path>/scripts/html_qa.py <path-to-html-file>
```

The script checks:

**Accessibility (WCAG AA baseline)**
- Color contrast ratios: text against its background must meet 4.5:1 for normal text, 3:1 for large text (18px+ or 14px+ bold). The script extracts inline styles and CSS variable assignments to compute ratios for branded elements.
- Heading hierarchy: headings must not skip levels (no h1 → h3 without h2). Every document needs exactly one h1.
- Image alt text: every `<img>` must have a non-empty `alt` attribute. Decorative images should use `alt=""` with `role="presentation"`.
- Form labels: any `<input>`, `<select>`, or `<textarea>` must have an associated `<label>` or `aria-label`.
- Landmark elements: the document should use semantic landmarks (`<main>`, `<nav>`, `<header>`, `<footer>`, `<section>`) rather than bare `<div>` wrappers for major regions.
- Link text: no "click here" or "read more" — links need descriptive text that makes sense out of context.

**Print Readiness**
- `@page` rule exists with landscape orientation and reasonable margins
- `-webkit-print-color-adjust: exact` is present (or `print-color-adjust: exact`)
- `@media print` block exists
- No `page-break-before: always` or `page-break-after: always` on section-level elements (these cause blank pages)
- Grid containers have print fallbacks (block display) — checks for `.module-grid`, `.persona-grid`, `.erd-grid`, or any custom grid that isn't ERD
- `break-inside: avoid` present on card-level elements

**Structural Integrity**
- Document has a `<!DOCTYPE html>` declaration
- Character encoding is declared (`<meta charset>`)
- Viewport meta tag is present
- No empty sections (headings with no content following them)
- No broken internal anchor links

The script outputs a JSON report:
```json
{
  "passed": false,
  "total_checks": 14,
  "passed_checks": 11,
  "failed_checks": 3,
  "issues": [
    {
      "category": "accessibility",
      "severity": "error",
      "rule": "color-contrast",
      "message": "Text '#666' on background '#f5f5f5' has contrast ratio 3.9:1 (needs 4.5:1)",
      "line": 142,
      "fix_hint": "Darken text to at least #595959"
    }
  ]
}
```

Severity levels:
- **error** — must fix before delivery (contrast failures, missing alt text, broken print layout)
- **warning** — should fix, but won't block delivery (missing viewport meta, heading skip in a non-critical section)

### Phase 2: Judgment Checks

After fixing any programmatic issues, review the document yourself for things a script can't catch:

**Content Quality**
- No source-revealing language: scan for "transcript", "call recording", "meeting notes", "auto-generated", "based on the discussion", "as mentioned in the call". These phrases break the illusion that the SA authored the document directly.
- No placeholder or template text: "[Company Name]", "Lorem ipsum", "TBD", "TODO", empty table cells that should have content.
- Section completeness: every section header has substantive content beneath it. A section with just a header and one sentence is likely incomplete.
- Consistent terminology: if the document calls something "Projects" in one section and "Initiatives" in another, flag it.

**Brand Consistency**
- Primary and accent colors are applied consistently (headers, badges, buttons all use the same brand palette — not a mix of brand colors and default blues)
- If the document uses the Airtable fallback palette, confirm the customer doesn't have known brand colors that should have been used instead
- Font choices are consistent throughout (no mixing of font families within body text)

**Information Architecture**
- The document tells a coherent story from top to bottom — a reader shouldn't need to jump back and forth to understand the system
- Related information is grouped together (e.g., a table's fields and its automations should be near each other, not separated by 5 other sections)
- The level of detail is appropriate for the audience (executive summary is actually concise, technical sections have actual field names and formula syntax)

## Fixing Issues

When issues are found:

1. **Programmatic errors**: fix them directly in the HTML. The script's `fix_hint` field provides specific guidance (exact hex values for contrast fixes, missing attributes to add, etc.)
2. **Judgment issues**: fix inline. For content quality problems, rewrite the offending text. For brand issues, update the CSS variables.
3. **Re-run the script** after fixes to confirm all programmatic checks pass.

Do not present the QA report to the user. Just fix the issues and deliver a clean document. The user cares about the output quality, not the verification process.

## Integration with Doc Skills

When wired into the end of a doc-generating skill, the flow is:

1. Doc skill generates the HTML file
2. Read this skill
3. Run `html_qa.py` against the generated file
4. Fix any issues found
5. Run Phase 2 judgment checks
6. Fix any issues found
7. Re-run `html_qa.py` to confirm
8. Present the clean file to the user

The goal: every HTML deliverable that reaches the customer has passed both phases. No exceptions.
