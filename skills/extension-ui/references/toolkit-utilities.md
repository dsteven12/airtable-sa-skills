# airtable-extension-toolkit Reference

The `airtable-extension-toolkit` npm package provides reusable utilities and React components for Interface Extensions. Install it as a project dependency:

```bash
npm install airtable-extension-toolkit
```

Source: https://github.com/victoriaplummer/airtable-extension-toolkit

## Table of Contents

1. [Field Helpers](#field-helpers)
2. [Color System](#color-system)
3. [Tailwind Preset](#tailwind-preset)
4. [React Components](#react-components)

---

## Field Helpers

`import { ... } from 'airtable-extension-toolkit/fields'`

### getField(record, fieldId) → any | null

Safely read a cell's raw value. Returns `null` if the field is missing, deleted, or throws. Use for linked records, attachments, selects — anything where you need the object shape.

### getFieldString(record, fieldId) → string

Safely read a cell's display string. Returns `''` if the field is missing or throws. Use for text, dates, numbers — anything you'll render as plain text.

### isWritableTextField(table, fieldId) → boolean

Check if a field supports plain string writes. Returns `true` only for: `singleLineText`, `multilineText`, `richText`, `email`, `url`, `phoneNumber`. Use to gate inline editing — prevents attempting writes to formula, AI text, lookup, and other computed fields.

### getFieldMeta(table, fieldId) → {choices: string[], type: string|null}

Read field metadata from the table schema. `choices` is populated for single/multi select fields — use to build dropdown UIs without hardcoding options.

### getSelectChoices(table, fieldId, options?) → Array<{name, styles}>

Read select field choices with their Airtable colors pre-resolved. Options:
- `mode: 'tailwind'` (default) — styles are Tailwind class bundles
- `mode: 'raw'` — styles are RGB strings for inline styles

### WRITABLE_TEXT_TYPES

`Set` of field type strings that support string writes: `singleLineText`, `multilineText`, `richText`, `email`, `url`, `phoneNumber`.

---

## Color System

`import { ... } from 'airtable-extension-toolkit/colors'`

Maps Airtable's select option color names (like `'blueBright'`, `'greenLight2'`) to usable style values. Covers all 10 color families (blue, cyan, teal, green, yellow, orange, red, pink, purple, gray) with base, dark1, light1, light2, light3 variants.

### airtableColorStyles(airtableColor) → object

Returns Tailwind class bundle: `{bg, text, header, dot, border, dropActive}`. Each value is a string of Tailwind classes including dark mode variants. Requires the toolkit's Tailwind preset.

```tsx
const styles = airtableColorStyles('blueBright');
// styles.bg → 'bg-blue-blueLight2 dark:bg-blue-blueDark1/30'
// styles.text → 'text-blue-blueDark1 dark:text-blue-blueLight1'
```

### airtableColorValues(airtableColor) → object

Returns raw RGB values: `{bg, text, header, dot, border, dropActive}`. Each value is an `rgb()` string. Use with inline styles for non-Tailwind projects.

```tsx
const raw = airtableColorValues('greenLight1');
// raw.bg → 'rgb(207, 245, 209)'
// raw.text → 'rgb(0, 100, 0)'
```

### createColorResolver(mode) → function

Factory to create a color resolver with a specific output mode.
- `'tailwind'` → returns `airtableColorStyles`
- `'raw'` → returns `airtableColorValues`
- `'both'` → returns `{bg: {class, value}, text: {class, value}, ...}`

---

## Tailwind Preset

`require('airtable-extension-toolkit/tailwind/airtable-preset')`

Complete Airtable design token system as a Tailwind CSS preset. Include in your `tailwind.config.js`:

```js
const airtablePreset = require('airtable-extension-toolkit/tailwind/airtable-preset');

module.exports = {
    presets: [airtablePreset],
    darkMode: 'media',  // CRITICAL: 'media' not 'class' — Airtable uses prefers-color-scheme
    content: ['./frontend/**/*.{js,ts,jsx,tsx}'],
};
```

Includes:
- **Colors**: All 10 Airtable color families with full variant sets (base, dusty, dark1, light1-3), plus gray scale (25-900)
- **Typography**: Airtable's font size scale (xs through 6xl with line heights)
- **Font families**: System font stacks for sans, display (Inter Display), and mono
- **Border radius**: Airtable's sm/md/lg values
- **Box shadows**: Airtable's 5-level shadow system (xs through xl)

**Note on darkMode**: The preset ships with `darkMode: 'class'` as a default. Override this to `'media'` in your config — Airtable controls dark mode via `prefers-color-scheme`, not a CSS class.

---

## React Components

`import { ... } from 'airtable-extension-toolkit/components'`

### EditableText

Click-to-edit text field. Renders as clickable text when not editing; switches to textarea/input on click. Escape cancels, blur/Enter commits.

Props: `value`, `onSave(newValue)`, `disabled`, `multiline`, `placeholder`, `rows`, `hideWhenEmpty`, `renderDisplay(value)`

### EditableSection

Labeled wrapper for EditableText with preset styles. Three variants:
- `FormSection` — default labels
- `BibleSection` — uppercase labels
- `AIOutputSection` — heading + markdown, 8 rows

Props: `label`, `value`, `onSave`, `disabled`, `multiline`, `labelStyle`, `placeholder`, `rows`, `renderDisplay`

### Badge

Colored status pill that matches select field colors.

Props: `text`, `colors` (from color resolver), `className`

```tsx
import { Badge } from 'airtable-extension-toolkit/components';
import { airtableColorStyles } from 'airtable-extension-toolkit/colors';

<Badge text="Active" colors={airtableColorStyles('greenBright')} />
```

### LinkedRecordPills

Renders linked record values as clickable pills that call `expandRecord()` on click.

Props: `value` (raw getCellValue output), `records` (loaded records from linked table), `onExpand` (expandRecord handler), `className`

Also exports `LinkedPillsWithAdd` — extends pills with a searchable `+` dropdown for adding new links without leaving the extension.

Props: `value`, `records`, `allRecords`, `onExpand`, `onAdd(recordId)`, `className`

### InlineFieldEdit

Smart field editor — auto-renders dropdown for select fields, text input for text fields.

Props: `label`, `value`, `fieldMeta` (from `getFieldMeta()`), `onSave`, `disabled`

### AttachmentPreview

Thumbnail image renderer for attachment field values.

Props: `attachments` (raw getCellValue), `className`, `index` (which attachment, default 0)

### Markdown

Zero-dependency markdown renderer. Supports headings, bold, italic, inline code, links, lists, blockquotes, code blocks, horizontal rules. Dark mode aware.

Props: `children` (markdown string), `className`

Also exports `looksLikeMarkdown(text)` — heuristic to auto-detect whether a string contains markdown formatting.
