---
name: extension-ui
description: "Build production-quality Airtable Custom Extension UIs with React and accessibility built in. Use this skill when developing, designing, or reviewing the UI layer of an Airtable Custom Interface Extension — including component architecture, styling, performance, and accessibility. MANDATORY TRIGGERS: extension UI, extension component, extension design, extension styling, build extension interface, extension layout, extension dashboard, review extension code, extension performance, custom extension React. ALWAYS invoke when the user is actively building or reviewing the React/UI layer of a Custom Extension — even if they just say 'let's build the UI' or 'make this look better'. Do NOT invoke for Interface Designer work (that's native Airtable, not code). Do NOT invoke for scaffolding (that's scaffold-extension)."
---

# Extension UI

Build production-quality Airtable Custom Interface Extension UIs. This skill covers the Interface Extensions SDK (`@airtable/blocks/interface`), component architecture, styling, accessibility, and performance — everything after `scaffold-extension` sets up the project and before the extension ships.

## SDK Orientation — Interface Extensions ≠ Old Blocks SDK

Interface Extensions use `@airtable/blocks/interface` — a different SDK from the older `@airtable/blocks`. Claude's training data contains extensive examples from the old SDK. Those patterns will break Interface Extensions.

**Critical differences:**

| Old Blocks SDK (`@airtable/blocks/ui`) | Interface Extensions (`@airtable/blocks/interface/ui`) |
|---|---|
| `<Button>`, `<Input>`, `<Box>`, `<FormField>`, `<Select>`, `<Dialog>`, `<Tooltip>`, `<Icon>`, etc. | **None of these exist.** Only `<CellRenderer>`. Use plain HTML/React or a third-party library. |
| `import {useBase} from '@airtable/blocks/ui'` | `import {useBase} from '@airtable/blocks/interface/ui'` |
| `initializeBlock(() => <App />)` | `initializeBlock({interface: () => <App />})` |
| `useRecords(queryResult)` with views/sorts/fields | `useRecords(table)` — table-level only, no view access |
| `cursor`, `viewport`, `useViewport` | Not available |

**Import map — everything comes from two paths:**

```tsx
// Models & types
import {FieldType} from '@airtable/blocks/interface/models';

// Hooks, components, utils — everything UI
import {
    useBase, useRecords, useCustomProperties, useGlobalConfig,
    useSynced, useSession, useRunInfo, useColorScheme, useWatchable,
    CellRenderer, expandRecord, initializeBlock,
    colors, colorUtils,
    loadCSSFromString, loadCSSFromURLAsync, loadScriptFromURLAsync,
} from '@airtable/blocks/interface/ui';
```

There is NO Airtable-provided UI component library beyond `<CellRenderer>`. For buttons, inputs, selects, dialogs — use a third-party library or plain HTML/React. See the Styling section for options.

## Airtable Extension Constraints

Extensions run inside Airtable Interfaces as custom layout elements or dashboard widgets. Every UI decision flows from these constraints:

- **Vertical layouts dominate.** Horizontal space depends on how the builder sizes the element. Stack elements vertically by default. Side-by-side layouts only work for small, fixed-width elements.
- **No routing.** Extensions are single-page. Use view switching (state-driven conditional rendering) instead of React Router. Keep the view stack shallow — 2-3 levels max.
- **Loading states are mandatory.** Every `useRecords()` call is async. The UI will flash empty without a loading state. Always show a skeleton or spinner.
- **Fill the container.** Extensions should use the full width and height of their container by default. Use `position: fixed; inset: 0` or `width: 100%; height: 100vh` on the root element. The extension can scroll if content overflows.
- **No view-level access.** Data access is table-level via `useRecords(table)`. The records returned are scoped to what Interface Designer has configured as data sources.

## Safe Field Access

The SDK's `getCellValue()` and `getCellValueAsString()` throw if a field is missing, deleted, or not exposed as a data source. Unguarded calls crash the extension.

**Use the toolkit's safe wrappers** (`airtable-extension-toolkit/frontend/fields.js`):

```tsx
import {getField, getFieldString, isWritableTextField, getFieldMeta, getSelectChoices} from 'airtable-extension-toolkit/fields';

// Safe raw value — returns null on error (use for linked records, attachments, selects)
const links = getField(record, fieldId);

// Safe display string — returns '' on error (use for text, dates, numbers)
const name = getFieldString(record, fieldId);

// Gate inline editing — only allow for writable text types
if (isWritableTextField(table, fieldId)) { /* show edit UI */ }

// Read select field choices with colors pre-resolved
const choices = getSelectChoices(table, fieldId); // [{name, styles}]
const choicesRaw = getSelectChoices(table, fieldId, {mode: 'raw'}); // RGB values
```

**Always use `getFieldIfExists` / `getFieldByIdIfExists`** for direct SDK access — the throwing variants (`getField`, `getFieldByName`, `getFieldById`) crash if a field was deleted or isn't visible.

**Always use the FieldType enum for comparisons** — never compare against string literals:
```tsx
import {FieldType} from '@airtable/blocks/interface/models';

// ✅ CORRECT
if (field.type === FieldType.SINGLE_SELECT) { /* ... */ }

// ❌ WRONG — don't use string literals
if (field.type === 'singleSelect') { /* ... */ }
```

For the complete field type reference (read/write shapes for every FieldType), see `references/field-type-reference.md`.

## Writing Data

### Permission checks — always first

Interface Designer can disable editing per-field. Users may have read-only access. Always check before writing:

```tsx
if (table.hasPermissionToUpdateRecord(record, {'Status': {name: 'Done'}})) { /* ... */ }

// Detailed check with reason string for error messages
const check = table.checkPermissionsForUpdateRecord(record, fields);
if (!check.hasPermission) {
    alert(check.reasonDisplayString);
}
```

### The array field overwrite trap

Attachments, linked records, multi-select, and multi-collaborator fields **silently overwrite** when updated. You must spread the existing value to append:

```tsx
// ✅ CORRECT — append a linked record
await table.updateRecordAsync(record, {
    'Related Projects': [
        ...record.getCellValue('Related Projects'),  // keep existing
        {id: newRecordId},                            // add new
    ],
});

// ❌ WRONG — this replaces ALL linked records with just one
await table.updateRecordAsync(record, {
    'Related Projects': [{id: newRecordId}],
});
```

Same pattern applies to attachments, multi-select, and multi-collaborator. This is the single most common bug in extension write code.

### Batch operations

Max 50 records per batch call. Rate limit: 15 writes/sec globally across all tables. Always `await` between batches to avoid hitting the rate limit.

```tsx
const BATCH_SIZE = 50;
async function batchCreate(table, recordDefs) {
    const allIds = [];
    for (let i = 0; i < recordDefs.length; i += BATCH_SIZE) {
        const batch = recordDefs.slice(i, i + BATCH_SIZE);
        const ids = await table.createRecordsAsync(batch);
        allIds.push(...ids);
    }
    return allIds;
}
```

## Custom Properties for Builders

Custom properties appear in the Interface Designer sidebar. Builders configure them without code. This is how extensions become reusable across different bases and table structures.

**The `getCustomProperties` function must have a stable identity** — define it at the top level of the file or wrap in `useCallback`. Defining inline causes infinite re-renders.

```tsx
// ✅ CORRECT — top-level function
function getCustomProperties(base) {
    const table = base.tables[0];
    return [
        {key: 'title', label: 'Chart Title', type: 'string', defaultValue: 'My Chart'},
        {key: 'showLegend', label: 'Show Legend', type: 'boolean', defaultValue: true},
        {
            key: 'color', label: 'Color', type: 'enum',
            possibleValues: [{value: 'red', label: 'Red'}, {value: 'blue', label: 'Blue'}],
            defaultValue: 'red',
        },
        {key: 'dataTable', label: 'Data Table', type: 'table', defaultValue: table},
        {
            key: 'xAxis', label: 'X-axis Field', type: 'field', table,
            shouldFieldBeAllowed: (field) => field.config.type === FieldType.NUMBER,
        },
    ];
}

function MyExtension() {
    const {customPropertyValueByKey} = useCustomProperties(getCustomProperties);
    if (!customPropertyValueByKey.dataTable) {
        return <div>Open the properties panel to configure this extension.</div>;
    }
    // ... render extension
}
```

Use string custom properties for API keys — never hardcode them:
```tsx
{key: 'mapboxApiKey', label: 'Mapbox API Key', type: 'string', defaultValue: ''},
```

## GlobalConfig (Persistent Key-Value Storage)

For extension-internal state that persists across sessions. Syncs in real-time to all users.

```tsx
const globalConfig = useGlobalConfig();
const savedFilter = globalConfig.get('filter');
await globalConfig.setAsync('filter', 'active');
```

Limits: 150kB max size, 1000 keys max, 50 paths per `setPathsAsync`. Use `useSynced` as shorthand:

```tsx
const [value, setValue, canSetValue] = useSynced('filterKey');
```

## Other Essential Hooks & Utils

```tsx
// Session — current user info
const session = useSession();
session.currentUser // {id, email, name, profilePicUrl} | null

// Run info — edit mode detection
const runInfo = useRunInfo();
runInfo.isDevelopmentMode
runInfo.isPageElementInEditMode // useful for showing config UI

// Expand a record to its detail view — preferred over custom detail panes
expandRecord(record); // opens Airtable's native record detail modal

// Built-in color system (works without Tailwind)
import {colors, colorUtils} from '@airtable/blocks/interface/ui';
colorUtils.getHexForColor(colors.BLUE);    // '#2d7ff9'
colorUtils.shouldUseLightTextOnColor(colors.BLUE_DARK_1); // true
```

## Component Architecture

### When to Use CellRenderer vs Custom Components

**Use `<CellRenderer>`** when you want to display a cell value exactly as Airtable would — select pills, linked record chips, attachment thumbnails. It handles all field types automatically.

```tsx
<CellRenderer field={statusField} record={record} />
```

**Build custom components** when you need interaction (click-to-edit, drag-and-drop), custom layouts (dashboards, kanban), or richer styling than CellRenderer provides.

For third-party component libraries, see the Styling section.

### Compound Components Over Boolean Props

When a component grows beyond 3-4 props that control visibility or behavior, decompose it:

```jsx
// Instead of <RecordCard showActions={true} showTimestamp={true} ... />
<RecordCard record={record}>
  <RecordCard.Status />
  <RecordCard.Assignee />
  <RecordCard.Actions onEdit={handleEdit} />
</RecordCard>
```

Implementation uses React Context — the parent provides the record, sub-components consume it. Each is independently testable. New features compose without touching the parent API.

When compound components are overkill: if the component has fewer than 4 configuration concerns and won't grow, a flat props interface is fine.

### Explicit Variants Over Boolean Modes

When a component renders substantially different UI based on a mode, use explicit variant components instead of conditional rendering inside one component:

```jsx
<SummaryPanel />   // instead of <Panel mode="summary" />
<DetailPanel />
<EditPanel />
```

Shared logic lives in a custom hook (`usePanel`) or shared sub-component, not in a monolithic component with branching render paths.

## Styling

### Third-party libraries that work

The blocks CLI uses webpack. Any npm package compatible with webpack works.

| Need | Recommended | Notes |
|------|-------------|-------|
| **Component library** | `@mui/material` (MUI) | Airtable's own sliding-bar-chart example uses MUI v7. Full component set. |
| **Headless UI** | `@radix-ui/react-*` | Accessible primitives without styling opinions. Lighter than MUI. |
| **CSS framework** | **Tailwind CSS** | Officially supported — used in Airtable's map extension. |
| **Charts** | `recharts` (React), `d3` | Airtable's word-cloud example uses D3. |
| **Icons** | `@phosphor-icons/react` | Append `Icon` suffix: `import {ArrowRightIcon}`. |
| **Drag & drop** | `@dnd-kit/core` | Accessible drag-and-drop. |
| **Markdown** | `marked` | Or use the toolkit's zero-dependency `<Markdown>` component. |

React 19 note: if a library doesn't list React 19 as peer dependency, use `npm install --legacy-peer-deps`.

### Tailwind CSS setup

Tailwind is officially supported. Airtable's own map extension uses this exact setup.

```bash
npm install -D tailwindcss postcss postcss-loader css-loader style-loader autoprefixer @airtable/blocks-webpack-bundler
```

**tailwind.config.js:**
```js
const airtablePreset = require('airtable-extension-toolkit/tailwind/airtable-preset');

module.exports = {
    presets: [airtablePreset],
    // CRITICAL: must be 'media', not 'class'. Airtable controls dark mode via
    // prefers-color-scheme, not a CSS class.
    darkMode: 'media',
    content: ['./frontend/**/*.{js,ts,jsx,tsx}'],
};
```

The toolkit's Tailwind preset (`airtable-extension-toolkit/tailwind/airtable-preset.js`) includes all Airtable design tokens — 10 color families with all variants, typography scale, border radius, and box shadows.

**frontend/style.css:**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

Then `import './style.css'` in your component.

### CSS approach for imports

```tsx
import './style.css';  // webpack handles it

// External CSS
await loadCSSFromURLAsync('https://cdn.example.com/library.css');

// Dynamic CSS
loadCSSFromString('.my-card { border: 1px solid #ddd; }');
```

### Color system from the toolkit

The toolkit provides a complete Airtable color resolution system (`airtable-extension-toolkit/frontend/colors.js`):

```tsx
import {airtableColorStyles, airtableColorValues, createColorResolver} from 'airtable-extension-toolkit/colors';

// Tailwind class bundles (bg, text, header, dot, border, dropActive)
const styles = airtableColorStyles('blueBright');
// → {bg: 'bg-blue-blueLight2 dark:bg-blue-blueDark1/30', text: 'text-blue-blueDark1 ...', ...}

// Raw RGB values for inline styles
const raw = airtableColorValues('greenLight1');
// → {bg: 'rgb(207, 245, 209)', text: 'rgb(0, 100, 0)', ...}

// Factory for flexible output modes
const resolve = createColorResolver('both'); // 'tailwind' | 'raw' | 'both'
```

### Dark Mode

`prefers-color-scheme` automatically matches the user's **Airtable** appearance setting (not their OS setting):

```css
@media (prefers-color-scheme: dark) {
    .my-extension { background: #1a1a2e; color: #e0e0e0; }
}
```

JavaScript fallback:
```tsx
const colorScheme = useColorScheme(); // 'light' | 'dark'
```

For Tailwind, use `darkMode: 'media'` — not `'class'`. This is because Airtable controls the color scheme via the media query, not a CSS class.

### CVA for variant styling

Use `class-variance-authority` for components with multiple visual variants:

```typescript
import { cva } from "class-variance-authority";

const statusBadge = cva(
  "inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium",
  {
    variants: {
      status: {
        todo: "bg-slate-100 text-slate-700",
        "in-progress": "bg-blue-100 text-blue-700",
        done: "bg-green-100 text-green-700",
        blocked: "bg-red-100 text-red-700",
      },
    },
    defaultVariants: { status: "todo" },
  }
);
```

## Debug Panel

Interface Extensions only expose tables and fields the builder has explicitly added as data sources. This is the #1 cause of "field not found" / blank data issues. A debug panel controlled by a custom property is essential during development.

```tsx
{key: 'showDebug', label: 'Show Debug Panel', type: 'boolean', defaultValue: false},
```

The debug panel should show for each table: resolution status, record count, available fields (with id/name/type), missing field validation against your expected field map, write permissions, and a sample record probe. The Interface SDK silently fails for unconfigured fields — the debug panel makes this visible.

## Performance

Ordered by impact. Skip the rest until you have a measured problem.

### 1. Eliminate Request Waterfalls

Each `useRecords()` call is a separate fetch. If one depends on another's result, they execute sequentially. Fetch broadly, filter locally — the SDK's record cache makes this efficient for tables under ~5,000 records.

```jsx
// Parallel (good) — both fire immediately
const projects = useRecords(projectsTable);
const allTasks = useRecords(tasksTable);
const tasks = activeProject
  ? allTasks.filter(t => t.getCellValue("Project")?.[0]?.id === activeProject.id)
  : [];
```

### 2. Memoize Expensive Computations

`useRecords()` returns a new array reference on every data change. Without `useMemo`, grouping/sorting/aggregating runs on every render.

`getCellValue()` and `getCellValueAsString()` are SDK method calls with overhead — not simple property lookups. Calling them 5+ times per record inside a `.map()` adds up with hundreds of records.

```jsx
const grouped = useMemo(() => {
  return records.reduce((groups, record) => {
    const status = record.getCellValueAsString("Status");
    (groups[status] ||= []).push(record);
    return groups;
  }, {});
}, [records]);
```

### 3. Pre-build ID Maps for Linked Records

Linked record fields return `[{id, name}]` stubs. Resolving with `records.find(r => r.id === link.id)` is O(n) per link. With many links across many rows, this kills performance.

```tsx
const recordMap = useMemo(() => {
    const map = new Map();
    if (records) records.forEach(r => map.set(r.id, r));
    return map;
}, [records]);

// O(1) lookup instead of O(n)
const fullRecord = recordMap.get(link.id);
```

### 4. Virtualize Long Lists

If displaying 50+ records in a scrollable list, use `react-window`:

```jsx
import { FixedSizeList } from "react-window";

<FixedSizeList height={400} itemCount={records.length} itemSize={72} width="100%">
  {({ index, style }) => (
    <div style={style}><RecordCard record={records[index]} /></div>
  )}
</FixedSizeList>
```

### 5. Bundle Size Awareness

Extensions load in an iframe. Import selectively, avoid lodash full import, and import individual icons from icon libraries.

## Accessibility

Extensions inherit Airtable's accessibility expectations. An extension that breaks keyboard/screen reader flow is a broken extension.

### Keyboard Navigation
- All interactive elements must be focusable. If using `<div>` with `onClick`, add `tabIndex={0}`, `role="button"`, and `onKeyDown` for Enter/Space.
- Focus order must be logical — test by tabbing through without a mouse.
- Visible focus indicators — never set `outline: none` without an alternative.
- Escape closes modals/dialogs.

### Screen Reader Support
- Label all inputs with `<label>` or `aria-label`.
- Announce state changes with `aria-live="polite"`.
- Alt text on icon buttons: `<button aria-label="Delete record"><Trash2 /></button>`.
- Use semantic `<table>`, `<thead>`, `<th>` — not divs styled as tables.

### Minimum Contrast
WCAG AA: 4.5:1 for normal text, 3:1 for large text (18px+ or 14px+ bold).

## View State Management

Standard pattern for 2-3 views:

```jsx
const [view, setView] = useState("list");
const [selectedRecord, setSelectedRecord] = useState(null);

switch (view) {
  case "list": return <ListView onSelect={(r) => { setSelectedRecord(r); setView("detail"); }} />;
  case "detail": return <DetailView record={selectedRecord} onBack={() => setView("list")} />;
  case "edit": return <EditView record={selectedRecord} onSave={() => setView("detail")} />;
}
```

For 4+ views or shared state, extract into `useReducer`. See `references/react-patterns.md` for the full `useViewState` hook.

## Common Mistakes

1. **Importing from wrong package.** Use `@airtable/blocks/interface/ui` and `@airtable/blocks/interface/models`. NOT `@airtable/blocks/ui`.
2. **Trying to import UI components from Airtable.** No `<Button>`, `<Input>`, `<Box>`, `<FormField>` exist. Only `<CellRenderer>`.
3. **Forgetting permission checks before writes.**
4. **Overwriting array fields instead of appending.** Always spread existing value for linked records, attachments, multi-select, multi-collaborator.
5. **Defining getCustomProperties inline.** Must be stable — define at top level or `useCallback`.
6. **Checkbox reads as `null`, not `false`.** Unchecked → `null`.
7. **Not awaiting between batches.** Exceeds 15 writes/sec rate limit.
8. **Using `ReactDOM.render`.** Entry point is `initializeBlock({interface: () => <App />})`.
9. **Ignoring dark mode.** Use `@media (prefers-color-scheme: dark)` in CSS.
10. **Expecting view-level access.** No views in Interface Extensions. Data is table-level.
11. **Comparing field.type against string literals.** Always use `FieldType` enum.
12. **Hardcoding field/table names.** Use custom properties.
13. **Not filling the container.** Use `position: fixed; inset: 0` or `width: 100%; height: 100vh`.
14. **Using throwing field/table getters.** Prefer `getFieldIfExists()` and `getTableByIdIfExists()`.
15. **Writing to AI text fields.** `AI_TEXT` is read-only. Check `field.type` before exposing edit UI — only `singleLineText`, `multilineText`, `richText`, `email`, `url`, `phoneNumber` are writable.

## File Structure

```
frontend/
├── components/
│   └── extension/   # your composed components
│       ├── record-card.tsx
│       ├── status-panel.tsx
│       └── action-bar.tsx
├── hooks/
│   ├── use-records-with-loading.ts
│   └── use-view-state.ts
├── lib/
│   └── utils.ts     # cn() utility if using Tailwind
├── style.css        # Tailwind entry
└── index.tsx        # entry point with initializeBlock
```

## Deployment

```bash
block run      # Develop locally (hot reload)
block release  # Build and upload to Airtable
block submit   # Submit to Airtable Marketplace (optional)
```

During development, click `</>  Develop` in the Interface Designer properties panel to load the local version.

## Pre-Delivery Checklist

**Functional**
- [ ] All `useRecords()` calls have loading states
- [ ] Extension handles empty states (no records, no table selected, no permission)
- [ ] Error boundaries wrap the top-level component
- [ ] Custom properties unconfigured state shows helpful message
- [ ] Debug panel available via boolean custom property

**Visual**
- [ ] UI fills container and works at various sizes
- [ ] Text doesn't overflow or get clipped
- [ ] Colors work in both light and dark themes
- [ ] Loading → loaded transitions don't cause layout shift

**Accessibility**
- [ ] Tab through the entire extension — focus order is logical
- [ ] Every interactive element is keyboard-operable
- [ ] Screen reader announces form labels and status changes
- [ ] No color-only indicators (always pair color with text/icon)

**Performance**
- [ ] No request waterfalls — parallel fetches where possible
- [ ] Expensive record processing is memoized
- [ ] Linked record lookups use Map, not find()
- [ ] Lists of 50+ records are virtualized

**Code Quality**
- [ ] TypeScript: `tsc --noEmit` passes
- [ ] Linter passes
- [ ] No SDK deprecation warnings in console

## Reference Files

- `references/field-type-reference.md` — Complete read/write shapes for every FieldType
- `references/react-patterns.md` — Error boundaries, custom hooks, optimistic updates, debouncing, batch operations
- `references/toolkit-utilities.md` — Guide to airtable-extension-toolkit components and utilities
