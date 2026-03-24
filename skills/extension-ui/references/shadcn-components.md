# Component Libraries for Airtable Interface Extensions

Interface Extensions provide only `<CellRenderer>` as a built-in UI component. For buttons, inputs, dialogs, selects, and all other standard UI elements, you need a third-party library. This reference covers the recommended options.

## Option 1: MUI (Material UI)

Airtable's own sliding-bar-chart example uses MUI v7 + Emotion. This is the heaviest option but the most complete — full component set with built-in accessibility.

```bash
npm install @mui/material @emotion/react @emotion/styled
```

```jsx
import { Button, TextField, Select, MenuItem, Dialog } from '@mui/material';
```

Best for: feature-rich extensions where bundle size is less of a concern.

## Option 2: Radix UI (Headless Primitives)

Accessible primitives without styling opinions. Pair with Tailwind CSS for styling. Lighter than MUI.

```bash
npm install @radix-ui/react-dialog @radix-ui/react-dropdown-menu @radix-ui/react-select
```

```jsx
import * as Dialog from '@radix-ui/react-dialog';
import * as Select from '@radix-ui/react-select';
```

Best for: extensions where you want full control over styling and care about bundle size.

## Option 3: Plain HTML/React

For simple extensions, native HTML elements with CSS are perfectly fine. The extension doesn't need to match Airtable's exact UI — it just needs to be functional and accessible.

```jsx
<button onClick={handleClick}>Submit</button>
<input type="text" value={query} onChange={e => setQuery(e.target.value)} />
<select value={selected} onChange={e => setSelected(e.target.value)}>
  <option value="">Choose...</option>
</select>
```

Best for: simple extensions, prototypes, and when keeping dependencies minimal.

## Common UI Patterns

These patterns apply regardless of which component library you choose.

### Empty State

Every extension view needs an empty state. Don't show a blank panel.

```jsx
function EmptyState({ title, description, action }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '48px 0', textAlign: 'center' }}>
      <p style={{ fontSize: 14, fontWeight: 500 }}>{title}</p>
      <p style={{ fontSize: 12, color: '#666', marginTop: 4, maxWidth: 280 }}>{description}</p>
      {action && <div style={{ marginTop: 16 }}>{action}</div>}
    </div>
  );
}

<EmptyState
  title="No records found"
  description="Try adjusting your filters or select a different view."
  action={<button onClick={clearFilters}>Clear Filters</button>}
/>
```

### Loading Skeleton

Prefer skeletons over spinners for content areas:

```jsx
function RecordCardSkeleton() {
  return (
    <div style={{ padding: 12, border: '1px solid #e5e7eb', borderRadius: 8, marginBottom: 8 }}>
      <div style={{ height: 16, background: '#f3f4f6', borderRadius: 4, width: '75%', marginBottom: 8 }} />
      <div style={{ height: 12, background: '#f3f4f6', borderRadius: 4, width: '50%' }} />
    </div>
  );
}

function RecordListSkeleton({ count = 5 }) {
  return (
    <div>
      {Array.from({ length: count }).map((_, i) => (
        <RecordCardSkeleton key={i} />
      ))}
    </div>
  );
}
```

### Configuration Panel

Use custom properties for builder configuration (see main SKILL.md). If the extension also needs user-facing settings:

```jsx
function ConfigPanel({ onApply }) {
  const [groupBy, setGroupBy] = useState('');

  return (
    <div style={{ padding: 16, borderBottom: '1px solid #e5e7eb' }}>
      <label style={{ fontSize: 12, fontWeight: 500, color: '#666' }}>Group By</label>
      <select value={groupBy} onChange={e => setGroupBy(e.target.value)} style={{ width: '100%', marginTop: 4 }}>
        <option value="">None</option>
        <option value="status">Status</option>
        <option value="assignee">Assignee</option>
      </select>
      <button
        style={{ width: '100%', marginTop: 12, padding: '8px 0' }}
        disabled={!groupBy}
        onClick={() => onApply(groupBy)}
      >
        Apply
      </button>
    </div>
  );
}
```

## Tailwind with CVA

If using Tailwind CSS (see main SKILL.md for setup), `class-variance-authority` is the recommended way to handle component variants:

```typescript
import { cva } from "class-variance-authority";

const badge = cva(
  "inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium",
  {
    variants: {
      variant: {
        default: "bg-slate-100 text-slate-700",
        success: "bg-green-100 text-green-700",
        warning: "bg-yellow-100 text-yellow-700",
        danger: "bg-red-100 text-red-700",
      },
    },
    defaultVariants: { variant: "default" },
  }
);

// Usage: <span className={badge({ variant: "success" })}>Active</span>
```

## Theming for Airtable

To make components blend with Airtable's UI, use these baseline CSS variables:

```css
:root {
  --at-bg: #ffffff;
  --at-fg: #1d1f25;
  --at-muted: #f6f8fc;
  --at-muted-fg: #414551;
  --at-border: #daded6;
  --at-primary: #166ee1;      /* Airtable blue */
  --at-destructive: #dc043b;  /* Airtable red */
  --at-radius: 6px;
}

@media (prefers-color-scheme: dark) {
  :root {
    --at-bg: #1a1a2e;
    --at-fg: #e0e0e0;
    --at-muted: #31353e;
    --at-muted-fg: #c4c7cd;
    --at-border: #41454d;
  }
}
```

Adjust to match the specific Airtable theme version as needed.
