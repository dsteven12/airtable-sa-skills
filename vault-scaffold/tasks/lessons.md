---
purpose: self-improvement
last_updated:
tags:
  - cowork
  - lessons
---

# Lessons Learned

> Patterns captured after corrections. Review at session start. Each lesson is a rule to prevent repeating the same mistake.

## Airtable Automation Specs

- **Find Records conditions must match the UI.** Airtable's Find Records uses: Field (dropdown) → Operator (dropdown) → Value (token/text). Available operators: `contains`, `does not contain`, `is`, `is not`, `is empty`, `is not empty`. Never write SQL-style WHERE clauses or use operators like `=`, `equals`, `matches`. Always describe conditions as three explicit parts matching the UI controls.
- **Find Records always returns an array.** Even with Max records = 1, the result is a list. All downstream token references MUST use `First record:` accessor syntax (e.g., `{{Step 1: First record: AI Summary}}`). Never reference Find Records output as if it were a single record.
- **Cannot filter by Record ID in Find Records.** Record ID is not available as a filterable field in the conditions UI. Use a unique field like the primary field with the `is` operator, or add a formula field that surfaces the Record ID as text if exact-match is critical.
- **Trigger tokens are scoped to the trigger table.** A "When record created" trigger on Table A only exposes Table A's fields in the token picker. Linked record fields on Table A may or may not expand to show the linked table's fields — verify in the token picker before designing cross-table automations.
- **Structured data output schema supports nesting (object → array → object).** The Generate Structured Data UI allows creating an object-type key, then adding an array inside it, then objects inside that array. This enables variable-length AI extraction (e.g., arrays of action items) that feeds directly into a Repeating Group → Create Record pipeline, entirely no-code.
- **Linked record fields show "No valid nested options" in trigger token picker.** When a trigger is on Table A and Table A has a linked record field to Table B, you CANNOT expand that link to access Table B's fields in the token picker. Design around this by keeping all data access within the trigger table's automation.
- **Consolidate automations when data is already in scope.** Airtable has a 50-automation-per-base limit. When Automation A produces data that Automation B would need to look up, fold B's logic into A instead of creating a separate automation.
- **Script actions bypass token picker limitations.** When the automation token picker can't expand a field (linked records, multi-collaborator), a Script action can read the field values directly via the scripting API.
- **Script action timeout is 120 seconds.** Not 30s as some references state. Validated through direct testing.
- **Generate Structured Data → Repeating Group → Create Record.** The standard no-code pattern for one-to-many AI extraction. The structured data array feeds directly into a Repeating Group's "Repeat for each" input.
- **Counter Script inside Repeating Groups has a race condition.** Two iterations creating records at the same millisecond cause a read-then-write race on the counter field. Fix: replace Script-incremented counter with a platform-computed Count field (with filter conditions) or Rollup.
- **Count fields support conditional counting via "is any of" operator.** Toggle "Only include linked records that meet certain conditions" and use the "is any of" operator on single select fields.
- **Gate automations need dual trigger conditions to prevent premature firing.** A gate automation watching a formula also needs the prerequisite status as a second condition. Without both, the gate fires when the status first enters the prerequisite state — before any child records exist.

## AI Prompt Engineering (Airtable Automations)

- **Typed fields need prompt-level output guarantees.** Date fields reject non-ISO strings. Number fields interpret values literally. Single select fields need exact enum match. The prompt must constrain AI output to the field's accepted value space.
- **Temporal anchoring for historical data.** Any AI step processing data from a past date must be explicitly told to resolve relative references from that date, not the current date.
- **Integrity check fields for AI pipelines.** Have the AI report its own count (e.g., AI Action Item Count), then compare against actual records created. Surfaces silent failures.

## AI Field Agents

- **Field Agents are configured in the Airtable UI only — not via MCP API.** Build the core schema via MCP, then configure agents manually in the UI.
- **Field Agent source fields must be on the agent's own table.** If you need cross-table context in an agent's instructions, add lookup fields first.
- **Deep Match creates an editable linked record field.** A single field can serve as both the AI suggestion and the human override.

## Skill Delivery

- **Use `present_files`, not file paths.** Cowork renders `.skill` files with a "Copy to your skills" button. Pointing users to file paths doesn't work.
- **`.skills/` is read-only.** Copy to `/tmp/`, `chmod -R u+w`, edit, repackage with `package_skill.py`, deliver via `present_files`.
