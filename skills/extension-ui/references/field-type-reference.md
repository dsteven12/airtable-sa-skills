# FieldType Cell Value Reference

Import: `import {FieldType} from '@airtable/blocks/interface/models';`

Complete read/write shapes for every field type in the Interface Extensions SDK.

## Table of Contents

1. [Text Fields](#text-fields)
2. [Number Fields](#number-fields)
3. [Date Fields](#date-fields)
4. [Select Fields](#select-fields)
5. [Checkbox](#checkbox)
6. [Linked Records](#linked-records)
7. [Attachments](#attachments)
8. [Collaborator Fields](#collaborator-fields)
9. [Computed Fields (Read-Only)](#computed-fields-read-only)
10. [Other Fields](#other-fields)
11. [Constraints & Limits](#constraints--limits)

---

## Text Fields

| Type | Read | Write |
|------|------|-------|
| `SINGLE_LINE_TEXT` | `string` | `string` |
| `MULTILINE_TEXT` | `string` (may contain mention tokens) | `string` |
| `RICH_TEXT` | `string` (markdown formatted) | `string` (markdown) |
| `EMAIL` | `string` | `string` |
| `URL` | `string` | `string` |
| `PHONE_NUMBER` | `string` | `string` |

These are the **only writable text types**. The toolkit's `WRITABLE_TEXT_TYPES` set and `isWritableTextField()` function check for these.

---

## Number Fields

| Type | Read | Write | Notes |
|------|------|-------|-------|
| `NUMBER` | `number` | `number` | `options.precision` (0-8) |
| `CURRENCY` | `number` | `number` | `options.symbol`, `options.precision` (0-7) |
| `PERCENT` | `number` | `number` | **0.5 = 50%, 1 = 100%** — this trips people up |
| `RATING` | `number` | `number` | `options.max` (1-10), `options.icon`, `options.color` |
| `DURATION` | `number` (seconds) | `number` | |
| `AUTO_NUMBER` | `number` | n/a (computed) | |

---

## Date Fields

| Type | Read | Write |
|------|------|-------|
| `DATE` | ISO 8601 `string` | `Date \| string` |
| `DATE_TIME` | ISO 8601 `string` | `Date \| string` |
| `CREATED_TIME` | ISO 8601 `string` | n/a (computed) |
| `LAST_MODIFIED_TIME` | ISO 8601 `string` | n/a (computed) |

For `DATE_TIME` with a non-UTC timezone: ambiguous strings like `"2020-09-05T07:00:00"` are interpreted in the field's timezone. Include zone offset for explicit control: `"2020-09-05T07:00:00-07:00"`.

---

## Select Fields

```tsx
// SINGLE_SELECT
// Read:  {id: string, name: string, color?: Color}
// Write: {id: string} | {name: string}
record.getCellValue('Status')
// → {id: 'selXXX', name: 'Done', color: 'greenBright'}

// MULTIPLE_SELECTS
// Read:  Array<{id, name, color?}>
// Write: Array<{id} | {name}>    ⚠️ OVERWRITES — spread to append
```

Use the toolkit's `getSelectChoices(table, fieldId)` to get choices with pre-resolved Airtable colors.

---

## Checkbox

```tsx
// CHECKBOX
// Read:  true | null    (NOT false — unchecked is null)
// Write: boolean | null
```

This is a common gotcha. `if (record.getCellValue('Done') === false)` will never match — unchecked is `null`.

---

## Linked Records

```tsx
// MULTIPLE_RECORD_LINKS
// Read:  Array<{id: RecordId, name: string}>
// Write: Array<{id: RecordId, name?: string} | {name: string}>
//        ⚠️ OVERWRITES — spread to append
//        {name: 'X'} without id creates a NEW record in linked table
```

The read value returns lightweight stubs, not full record objects. To render clickable pills that call `expandRecord()`, resolve each stub against loaded records from the linked table. Use a `Map` for O(1) lookups — see Performance section in main SKILL.md.

---

## Attachments

```tsx
// MULTIPLE_ATTACHMENTS
// Read: Array<{id, url, filename, size?, type?, thumbnails?}>
// Write: Array<{url: string, filename?: string} | existingAttachmentObject>
//        ⚠️ OVERWRITES — spread to append
//        New attachments: {url: '...', filename: '...'}
//        Existing: pass the full object from getCellValue (cannot modify properties)
```

Thumbnail URLs are available at `attachment.thumbnails.small.url`, `.large.url`, etc. The toolkit's `<AttachmentPreview>` component handles this.

---

## Collaborator Fields

```tsx
// SINGLE_COLLABORATOR
// Read:  {id, email, name?, profilePicUrl?}
// Write: {id: string}

// MULTIPLE_COLLABORATORS
// Read:  Array<{id, email, name?, profilePicUrl?}>
// Write: Array<{id: string}>    ⚠️ OVERWRITES — spread to append

// CREATED_BY / LAST_MODIFIED_BY — same read format, not writable
```

---

## Computed Fields (Read-Only)

These fields cannot be written to. Attempting to write throws an error.

```tsx
// FORMULA — read: any (check options.result.type for actual type)
// ROLLUP — read: any (check options.result.type)
// COUNT — read: number
// MULTIPLE_LOOKUP_VALUES — read: Array<{linkedRecordId, value}>
// AUTO_NUMBER — read: number
// CREATED_TIME, LAST_MODIFIED_TIME, CREATED_BY, LAST_MODIFIED_BY
```

---

## Other Fields

```tsx
// BARCODE — read: {text: string, type?: string}, write: n/a
// BUTTON — read: {label: string, url: string | null}, write: n/a
// AI_TEXT — read: {state, value, isStale, errorType?}, write: n/a
// EXTERNAL_SYNC_SOURCE — read: {id, name, color?}, write: n/a
```

**AI_TEXT is read-only.** Attempting to write throws `"invalid cell value"`. Always check `field.type` before exposing inline editing — use the toolkit's `isWritableTextField()` to gate edit UI.

---

## Constraints & Limits

| Constraint | Value |
|-----------|-------|
| Records per batch operation | **50 max** |
| Write rate limit | **15 writes/sec** (global across all tables) |
| Individual write payload | **1.9MB max** |
| GlobalConfig size | **150kB max** |
| GlobalConfig keys | **1000 max** |
| GlobalConfig paths per `setPathsAsync` | **50 max** |

Consecutive `updateRecordAsync` calls to the same table within a short period are automatically merged into one request. Only reliable for small updates.
