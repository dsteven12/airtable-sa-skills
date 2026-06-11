---
name: workflow-comparison-svg
description: "Generate a side-by-side swimlane SVG comparing an original/current workflow against an updated/expected target workflow. Use when the user provides an existing workflow diagram (screenshot from Miro, Lucidchart, etc.) plus expected end-to-end workflow text and wants a visual gap analysis. MANDATORY TRIGGERS: compare original and updated workflow, swimlane comparison, original vs expected workflow, gap diagram, what's new in this workflow, workflow delta, current vs target workflow, side-by-side workflow diagram. Outputs an SVG with persona-preserving swimlanes, NEW/UPD badges, a System Outputs section, and a customer-facing What's new footnote. Renders inline via show_widget AND saves the SVG to the Work Brain folder. Do NOT use for full workflow documentation (use workflow-doc) or schema design (use airtable-design-advisor)."
---

# Workflow Comparison SVG

You generate a side-by-side swimlane SVG showing an original/current workflow alongside an updated/target workflow, with a structured System Outputs section and a customer-facing "What's new" footnote.

## When to invoke

The user has both:

- An **original workflow diagram** (typically a screenshot from Miro, Lucidchart, Whimsical, etc. showing existing swimlanes, boxes, and arrows)
- **Expected end-to-end workflow text** describing the target state in numbered steps

They want a visual comparison showing the gaps.

## Process

Follow these steps in order:

### 1. Analyze the original diagram

From the screenshot, extract:

- Lane labels (these are the personas — preserve them exactly)
- Boxes in each lane (label, color/category, approximate position)
- Arrows (source → destination, any conditional labels like "Not a Work Order")
- Side annotations or sticky notes (phasing notes, open questions, approval tags)

### 2. Parse the expected workflow text

For each numbered step:

- What activity is performed?
- WHO performs it? (this determines the lane)
- Is it a system action (automated) or human action?
- Is it an OUTPUT (report, dashboard, notification) or a workflow step?

### 3. Identify gaps

For each activity in the expected text:

- Present in original, unchanged → no badge
- Present but expanded → UPD badge
- Entirely new → NEW badge

### 4. Apply the Persona Preservation Rule (critical)

**Lanes in the updated diagram MUST mirror the original.** Only add a new lane when the text introduces a genuinely new actor (e.g., new role like "Supervisors", "Office of General Counsel", "External Auditor").

Concepts are NOT actors. Distribute the following kinds of activity groupings INTO existing actor lanes:

- "Linked Records", "Hierarchy Setup", "Fund Movements", "Completion & Notification", "Reporting & Oversight", "Review & Validation", "Field Updates" — these are activity groupings, not personas.
- Same-actor follow-up activities (e.g., a Review step done by the same staff who did Data Entry) → add as additional rows in the existing lane.

Before adding a lane, ask: "Is there a distinct actor who performs ONLY the activities in this lane?" If no, redistribute the activities.

### 5. Identify System Outputs (critical)

These are NOT actors and do NOT get a swimlane. They are automatically generated artifacts:

- Reports (Exhibit, GAA, Cost Center, Leadership, Daily Log, Asset Work History, Resolution Reporting)
- Dashboards (Active Events, KPIs, Workload Visibility)
- Notifications (automated emails, requestor notifications)
- Public calendars / public-facing views
- Trend / analytics outputs
- System records (Cost Code Items, Balance updates, Transfer History)

These go in a visually-distinct **System Outputs section below the swimlanes** with lavender background (`#F5F3FF`) and dashed indigo border (`#A78BFA`). Box styling uses the `output-artifact` class.

### 6. Generate the SVG

Use the standard structure (see SVG Structure section).

### 7. Mandatory pre-flight arrow audit (MUST be performed before rendering)

**This is the single most common quality issue. You MUST produce an explicit arrow audit table in your reasoning before calling `show_widget` or writing the SVG file. Skipping this step ships broken diagrams.**

For EACH arrow in the updated diagram, list in your reasoning:

| Arrow | Source (box.edge) | Destination (box.edge) | Path | Segments crossed/within 10px | Conflict? |
|-------|-------------------|------------------------|------|------------------------------|-----------|

For each path segment, check it against EVERY box in the diagram (not just the source/destination). Specifically:

1. **Vertical segments at x = X** — does X equal (or sit within 10px of) any box's left or right edge? Does X fall within any box's horizontal range while the segment's y-range overlaps the box's y-range?

2. **Horizontal segments at y = Y** — does Y equal (or sit within 10px of) any box's top or bottom edge? Does Y fall within any box's vertical range while the segment's x-range overlaps the box's x-range?

3. **Diagonal segments** — avoid these. If needed, decompose into vertical + horizontal legs that respect the gap-midpoint rule.

If ANY segment has a conflict, reroute the arrow before rendering.

**Common reroute corridors (use these when an arrow would cross an unrelated box):**

- **Left margin corridor:** x ≈ 225 (between lane label column at x=210 and first box column starting at x=240)
- **Right margin corridor:** x ≈ 1430-1450 (right of the rightmost box column, before lane edge at x=1620)
- **Vertical gap midpoint** between two adjacent box columns (e.g., box A right=500, box B left=540 → use x=520)
- **Horizontal gap midpoint** between two adjacent rows (e.g., row 1 bottom=230, row 2 top=260 → use y=245)
- **Below-row corridor:** a horizontal at y between a row's box bottom and the next lane boundary (use the midpoint)

**Common conflict patterns to look for:**

- Adding a new row to an existing lane → the original linear flow arrows almost always cut through the new boxes. Reroute via left or right margin.
- A return-loop arrow (e.g., DECISION → notify back to requestor) often crosses through middle-lane boxes. Reroute via the FAR margin.
- An arrow from a top-lane box to a bottom-lane box that passes through middle lanes is rarely clean unless you've explicitly verified the trunk x is in a gap.
- Diamond-source arrows that exit at "bottom (700, 230)" may need to use the bottom POINT exactly, then split. Two arrows from the same bottom point overlap on the trunk — that's fine visually.

**Anti-patterns (must not ship with):**

- Vertical lines at x = box.left or box.right (outlines the box edge)
- Horizontal lines at y = box.top or box.bottom (outlines the box edge)
- L-shaped paths whose corner aligns with a box corner
- Segments that hug a box edge for more than ~10px
- Arrows that start or end in white space instead of on a box edge
- Arrows that cut through unrelated boxes (most common when adding new rows)

### Endpoint check — every arrow's final segment

In addition to the segment audit, you MUST verify each arrow's TERMINATION:

1. **The endpoint must land within ~2–5px of the destination box edge.** Not in white space, not deep inside the box.

2. **The final segment's direction must be perpendicular to the edge it lands on, pointing INTO the box.** A horizontal segment must land on the LEFT or RIGHT edge of the box. A vertical segment must land on the TOP or BOTTOM edge.

3. **The arrow path must NOT pass through the destination box interior before terminating.** The endpoint should be the FIRST point at which the path touches the box. If the path enters the box from one side, traverses through it, then ends on the other side, the arrow visually points the wrong direction and the path is broken.

**Worked example of the bug this catches:**

> Path: `M 1220 240 L 1220 50 L 1300 50 L 1300 74` going from Box A (top-right at (1220, 240)) to Box B (at x=1190–1410, y=12–72).
>
> - Vertical at x=1220 enters Box B from below (since x=1220 is inside Box B's x-range 1190–1410).
> - At y=50 the segment is *inside* Box B (y=12–72 includes y=50).
> - Horizontal at y=50 runs THROUGH Box B's interior.
> - Final segment ends at (1300, 74) — BELOW Box B (box bottom is y=72), with the arrowhead pointing DOWN, OUT of the box.
>
> The arrow visually exits the box rather than entering it. To fix: reroute so the final segment approaches Box B from outside and lands perpendicularly on one edge. E.g., `M 1220 267 L 1450 267 L 1450 42 L 1412 42` — exits Box A on the right, goes UP via the x=1450 right-margin corridor (clear of all boxes), then LEFT to (1412, 42), landing 2px past Box B's right edge with arrowhead pointing left INTO the box.

**To verify each arrow in the audit table:**

For each arrow, write down:
- Endpoint coordinates: (x, y)
- Destination box: x=A–B, y=C–D
- Closest edge to endpoint: (top/bottom/left/right)
- Distance from endpoint to that edge: (px)
- Final segment direction at endpoint: (up/down/left/right)
- Does direction point INTO the box? (Y/N)
- Did the path traverse the box interior before terminating? (Y/N — must be N)

**Do not call show_widget or Write the SVG until the audit table shows zero conflicts AND every arrow passes the endpoint check.** The audit is not optional. If you find yourself thinking "this is probably fine," go back and trace the segments and endpoints explicitly.

### 8. Render and save

Do BOTH:

- Call `mcp__visualize__show_widget` to render the SVG inline for review.
- Write the SVG file to the Cowork workspace folder (use the workspace path from your system context — it follows the pattern `/sessions/<session-id>/mnt/Work Brain/`) with a descriptive filename like `<workflow-name>-original-vs-updated.svg` (kebab-case, no spaces).
- Use `mcp__cowork__present_files` to surface the saved file so the user can open it.

## SVG Structure

Standard layout (viewBox width 1700, height varies based on content):

```
y=0-130:    Original title (28px), subtitle (16px), legend (4-6 categories)
y=140-...:  Original diagram (translate group with lanes)
divider:    horizontal dashed line at lane boundary
y=...:      Updated title, subtitle, legend (with NEW/Changed marker, System Outputs marker)
y=...:      Updated diagram (translate group with persona-preserved lanes)
y=...:      System Outputs section (lavender bg #F5F3FF, dashed indigo border #A78BFA)
y=...:      What's new footnote (yellow bg #FEF3C7, amber border #F59E0B)
```

### Lane structure

Each lane has:

- A label column on the left (x=0-210, `label-col` bg `#F3F4F6`)
- Horizontal lane label text (font-size 17, weight 700)
- Lane sub-label (font-size 13.5, weight 400, color `#6B7280`) for actor disambiguation
- Alternating lane background (`lane-bg` `#FAFAFA` and `lane-bg-alt` `#FFFFFF`)
- Content area for boxes (x=210-1620)

### Box conventions

- Standard width: ~240-280px, height ~80-130px depending on content
- Corner radius: 5
- Box text: 15px, weight 500, anchor middle
- Box sub-text: 13px
- Badge (NEW/UPD): 28×18 orange (`#F59E0B`) box at top-right of new boxes, white 12px text weight 700

### Color palette (legend categories)

| Category | Fill | Stroke | Use |
|----------|------|--------|-----|
| External Actions / External User | `#C7B9F7` | `#8B7DD8` | Things outside the system (requestors, callers) |
| Decisions | `#BFC2C7` | `#8E939B` | Diamond decisions |
| Our Actions | `#FCD34D` | `#D4A91A` | Internal team actions |
| Automations | `#FAD2D2` or `#C7B9F7` | matching darker | System-automated steps |
| New / Changed | `#FEF3C7` with dashed `#F59E0B` border (stroke-dasharray 5 4, stroke-width 2) | — | Highlights newly added/changed boxes |
| System Outputs | `#E0E7FF` with dashed `#6366F1` border (stroke-dasharray 3 2) | — | Reports, dashboards, exports |

Match the original diagram's existing palette when reproducing it (some originals use purple for Automation, some pink — preserve what's there).

### Arrow marker

Standard arrow marker definition (use unique id per SVG, e.g. `arrowA`, `arrowB`):

```xml
<marker id="arrowX" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
  <path d="M0,0 L10,5 L0,10 z" fill="#4B5563"/>
</marker>
```

Standard solid arrow: `stroke="#4B5563" stroke-width="2" marker-end="url(#arrowX)"`
Dashed feeder/optional arrow: add `stroke-dasharray="4 3"`.

## Customer-Facing Voice

The SVG will be shown to customers. Do NOT include any meta-language about the generation process:

- ❌ "Persona preservation" / "actor lanes preserved"
- ❌ "Folded into BSS lane since same actor"
- ❌ "Routes around the X box because of arrow rule N"
- ❌ References to gap analysis or design choices

Use plain workflow language:

- Subtitle describes what the workflow does (e.g., "Adds explicit bill intake steps, facility linking, a review & validation phase, and reporting outputs.")
- "What's new" footnote describes changes in customer terms (new steps, new tracking, new reporting)
- Lane sub-labels are factual actor identifiers ("Energy Systems Analyst", "Tenant or staff", "Internal staff", "BBSS — Budget Team")

## Common patterns

### Multiple rows in one lane

When an actor has many activities (e.g., 8 boxes in the Operator lane for Call Center), stack them in 2-3 rows within the same lane. Use row gaps (~30-50px) for arrow trunks between rows.

### Optional/conditional activities

When an action is conditional (e.g., "Link Assets — when applicable"), use dashed arrows (`stroke-dasharray="4 3"`) and an italic label like "when applicable" or "optional" near the arrow.

### Side annotations (phasing notes, open questions)

Use a colored callout box on the right side of the diagram:

- Pink `#FCE7F3` / stroke `#EC4899` for phasing notes
- Green `#86EFAC` / stroke `#16A34A` for approval tags

Keep these separate from the workflow boxes.

### Lane that's empty in the original

Preserve it in the updated diagram with the same label, OR replace it if the text introduces a NEW actor who naturally fits that visual position. Note this clearly in the "What's new" footnote.

### Adding new rows to a lane (arrow consequences)

When you add Row 2 or Row 3 of new activities into an existing lane, the original linear flow arrows almost always need rerouting around the new boxes. Common solutions:

- **Left corridor** at x≈225 (between lane label col and first box column)
- **Right corridor** at x≈1430-1450 (right of the rightmost box column)
- **Gap midpoint** between two box columns

Verify after rerouting: trace every segment, confirm no box-edge overlap.

## What NOT to do (anti-patterns)

- Don't create conceptual lanes ("Reporting & Oversight", "Linked Records", "Hierarchy Setup", "Fund Movements", "Completion & Notification") — these are activity groupings, not personas.
- Don't put system outputs in a swimlane — they have their own dedicated section below.
- Don't ship without arrow pre-flight — arrows that outline boxes are a visible quality issue.
- Don't include meta-language ("persona preserved", "rerouted to avoid") in customer-facing text.
- Don't extend `workflow-doc` instead of using this skill — they serve different purposes.
- Don't assume Reporting always means a dedicated lane — it's almost always System Outputs.

## Output checklist

Before finishing:

- [ ] Original diagram matches the source screenshot (lanes, boxes, arrows)
- [ ] Updated diagram preserves original lane structure
- [ ] Any new lanes correspond to NEW actors (not concepts)
- [ ] System Outputs section exists and is visually distinct
- [ ] All NEW/UPD badges are present and accurate
- [ ] Arrow pre-flight passed: every segment in genuinely clear space, no edge-hugging
- [ ] "What's new" footnote is customer-facing (no meta-language)
- [ ] SVG rendered inline via `show_widget` for review
- [ ] SVG file saved to `Work Brain/` folder with descriptive filename
- [ ] `present_files` surfaces the saved SVG so the user can open it
