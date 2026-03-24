# React Patterns for Airtable Interface Extensions

Extended reference for patterns beyond what's in the main SKILL.md. Read this when you need deeper guidance on a specific pattern.

## Table of Contents

1. [Error Boundaries](#error-boundaries)
2. [Custom Hooks for SDK](#custom-hooks-for-sdk)
3. [Optimistic Updates](#optimistic-updates)
4. [Debounced Inputs](#debounced-inputs)
5. [Batch Operations with Progress](#batch-operations-with-progress)
6. [Linked Record Patterns](#linked-record-patterns)
7. [Inline Field Editing](#inline-field-editing)

---

## Error Boundaries

Every extension needs a top-level error boundary. Without one, a single bad record or unexpected null crashes the entire extension with a white screen.

Interface Extensions have no Airtable UI components — use plain HTML/React for the error state:

```jsx
import { Component } from "react";

class ErrorBoundary extends Component {
  state = { hasError: false, error: null };

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: 24, textAlign: 'center' }}>
          <h3 style={{ fontSize: 16, fontWeight: 600 }}>Something went wrong</h3>
          <p style={{ color: '#666', marginTop: 8 }}>
            {this.state.error?.message || "An unexpected error occurred"}
          </p>
          <button
            style={{ marginTop: 16, padding: '8px 16px', cursor: 'pointer' }}
            onClick={() => this.setState({ hasError: false, error: null })}
          >
            Try Again
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

// Usage in entry point:
import { initializeBlock } from '@airtable/blocks/interface/ui';

function App() {
  return (
    <ErrorBoundary>
      <Extension />
    </ErrorBoundary>
  );
}

initializeBlock({ interface: () => <App /> });
```

Place additional error boundaries around high-risk sub-trees (data visualization components, record processing views) so a crash in one section doesn't take down the whole extension.

---

## Custom Hooks for SDK

Wrap common SDK patterns in custom hooks to reduce boilerplate and centralize loading/error handling.

### useRecordsWithLoading

```typescript
import { useRecords } from "@airtable/blocks/interface/ui";

function useRecordsWithLoading(table) {
  const records = useRecords(table);
  const isLoading = records === null;
  const isEmpty = !isLoading && records.length === 0;
  return { records: records || [], isLoading, isEmpty };
}
```

### useViewState

```typescript
import { useReducer, useCallback } from "react";

const initialState = { current: "list", history: [], params: {} };

function viewReducer(state, action) {
  switch (action.type) {
    case "NAVIGATE":
      return {
        current: action.view,
        history: [...state.history, state.current],
        params: action.params || {},
      };
    case "BACK": {
      const prev = state.history[state.history.length - 1];
      return {
        current: prev || "list",
        history: state.history.slice(0, -1),
        params: {},
      };
    }
    case "RESET":
      return initialState;
    default:
      return state;
  }
}

function useViewState(initialView = "list") {
  const [state, dispatch] = useReducer(viewReducer, {
    ...initialState,
    current: initialView,
  });

  const navigate = useCallback(
    (view, params) => dispatch({ type: "NAVIGATE", view, params }),
    []
  );
  const goBack = useCallback(() => dispatch({ type: "BACK" }), []);
  const reset = useCallback(() => dispatch({ type: "RESET" }), []);

  return { view: state.current, params: state.params, navigate, goBack, reset };
}
```

---

## Optimistic Updates

Update the UI immediately on write, roll back on failure. The SDK applies writes optimistically locally — your extension sees changes immediately — but wrapping in local state gives you control over the rollback.

```jsx
import { useState } from "react";

function StatusToggle({ table, record, statusField }) {
  const [optimisticStatus, setOptimisticStatus] = useState(null);
  const currentStatus = optimisticStatus ?? record.getCellValueAsString(statusField);

  const toggleStatus = async () => {
    const newStatus = currentStatus === "Done" ? "To Do" : "Done";
    setOptimisticStatus(newStatus);

    try {
      await table.updateRecordAsync(record, {
        [statusField.id]: { name: newStatus },
      });
      setOptimisticStatus(null); // Clear — real data takes over
    } catch (error) {
      setOptimisticStatus(null); // Roll back on failure
      console.error("Failed to update status:", error);
    }
  };

  return <button onClick={toggleStatus}>{currentStatus}</button>;
}
```

---

## Debounced Inputs

Search and filter inputs should be debounced to avoid re-filtering on every keystroke:

```jsx
import { useState, useMemo, useEffect } from "react";
import { getFieldString } from "airtable-extension-toolkit/fields";

function useDebounce(value, delay = 300) {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);
  return debounced;
}

function SearchableList({ records, nameFieldId }) {
  const [query, setQuery] = useState("");
  const debouncedQuery = useDebounce(query, 250);

  const filtered = useMemo(() => {
    if (!debouncedQuery) return records;
    const lower = debouncedQuery.toLowerCase();
    return records.filter((r) =>
      getFieldString(r, nameFieldId).toLowerCase().includes(lower)
    );
  }, [records, debouncedQuery, nameFieldId]);

  return (
    <>
      <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search..." />
      {filtered.map((record) => (
        <div key={record.id}>{getFieldString(record, nameFieldId)}</div>
      ))}
    </>
  );
}
```

---

## Batch Operations with Progress

Show progress during batch operations:

```jsx
async function batchUpdate(table, updates, onProgress) {
  const BATCH_SIZE = 50;
  for (let i = 0; i < updates.length; i += BATCH_SIZE) {
    const batch = updates.slice(i, i + BATCH_SIZE);
    await table.updateRecordsAsync(batch);
    onProgress?.(Math.min(i + BATCH_SIZE, updates.length), updates.length);
  }
}

function BatchProgress({ current, total }) {
  const percent = Math.round((current / total) * 100);
  return (
    <div style={{ width: '100%', background: '#e5e7eb', borderRadius: 4, height: 8 }}>
      <div
        style={{
          width: `${percent}%`,
          background: '#2d7ff9',
          borderRadius: 4,
          height: 8,
          transition: 'width 300ms',
        }}
      />
    </div>
  );
}
```

---

## Linked Record Patterns

### Linked record pills

Linked record fields should render as clickable pills, not plain text. This matches Airtable's native UX.

The toolkit provides `<LinkedRecordPills>` and `<LinkedPillsWithAdd>` components (see `references/toolkit-utilities.md`). If not using those, here's the core pattern:

```tsx
import { expandRecord } from '@airtable/blocks/interface/ui';
import { getField } from 'airtable-extension-toolkit/fields';

function LinkedPills({ record, fieldId, linkedRecords }) {
    const links = getField(record, fieldId);
    if (!links || !Array.isArray(links) || links.length === 0) return null;

    // Pre-build map for O(1) lookups
    const recordMap = new Map(linkedRecords?.map(r => [r.id, r]) || []);

    return (
        <span style={{ display: 'inline-flex', flexWrap: 'wrap', gap: 4 }}>
            {links.map(link => {
                const full = recordMap.get(link.id);
                return full ? (
                    <button
                        key={link.id}
                        onClick={(e) => { e.stopPropagation(); expandRecord(full); }}
                        style={{
                            padding: '2px 8px', borderRadius: 12, fontSize: 12,
                            background: '#d1e2ff', color: '#0d52ac', cursor: 'pointer',
                            border: 'none',
                        }}
                    >
                        {link.name}
                    </button>
                ) : (
                    <span key={link.id} style={{
                        padding: '2px 8px', borderRadius: 12, fontSize: 12,
                        background: '#e5e9f0', color: '#666',
                    }}>
                        {link.name}
                    </span>
                );
            })}
        </span>
    );
}
```

**Rules:**
1. Always use pills for linked records — plain text loses relationship context.
2. Use raw `getCellValue()` (not `getCellValueAsString()`) — you need the `[{id, name}]` array.
3. Always `e.stopPropagation()` on click — pills are often nested inside other clickable elements.

### Autocomplete with fetchForeignRecordsAsync

```tsx
const [filterString, setFilterString] = useState('');
const [available, setAvailable] = useState([]);

useEffect(() => {
    const timeout = setTimeout(() => {
        record.fetchForeignRecordsAsync(linkedField, filterString)
            .then(response => setAvailable(response.records));
    }, 300);
    return () => clearTimeout(timeout);
}, [record, linkedField, filterString]);
```

### Create and link in one write

Pass `{name: 'New Record'}` (no `id`) to create a new record in the linked table AND link it:

```tsx
await table.updateRecordAsync(record, {
    'Linked Field': [
        ...record.getCellValue('Linked Field'),
        {name: 'New linked record'},  // creates + links
    ],
});
```

---

## Inline Field Editing

When exposing editable fields, read field options from the schema — never hardcode dropdown values.

```tsx
import { getFieldMeta, isWritableTextField } from 'airtable-extension-toolkit/fields';

function InlineFieldEdit({ label, value, fieldMeta, onSave, disabled }) {
    if (fieldMeta.choices.length > 0) {
        return (
            <div>
                <label>{label}</label>
                <select value={value} onChange={e => onSave(e.target.value)} disabled={disabled}>
                    <option value="">--</option>
                    {fieldMeta.choices.map(c => <option key={c} value={c}>{c}</option>)}
                </select>
            </div>
        );
    }
    return <input value={value} onChange={e => onSave(e.target.value)} disabled={disabled} />;
}
```

### Write values by field type

```tsx
// Single select → {name: 'Option'} or null to clear
onSave={val => updateField(record, FIELDS.STATUS, val ? {name: val} : null)}

// Text field → plain string or null
onSave={val => updateField(record, FIELDS.NOTES, val || null)}

// Number → number or null
onSave={val => updateField(record, FIELDS.SCORE, val ? Number(val) : null)}
```

**Rules:**
1. Never hardcode select options — use `field.options.choices` from the schema.
2. Always permission-check before writing.
3. Memoize field metadata: `useMemo(() => getFieldMeta(table, fieldId), [table])`.
4. Handle missing fields gracefully — degrade to read-only or hidden.
