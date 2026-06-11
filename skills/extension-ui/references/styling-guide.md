# Extension UI Styling Guide

Complete styling reference for Airtable Custom Interface Extensions — library recommendations, Tailwind setup, color system, dark mode, and variant styling.

## Third-party libraries that work

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

## Tailwind CSS setup

Tailwind is officially supported. Airtable's own map extension uses this exact setup.

```bash
npm install -D tailwindcss postcss postcss-loader css-loader style-loader autoprefixer @airtable/blocks-webpack-bundler
```

**tailwind.config.js:**
```js
const airtablePreset = require('airtable-extension-toolkit/tailwind/airtable-preset');

module.exports = {
    presets: [airtablePreset],
    // Must be 'media', not 'class'. Airtable controls dark mode via
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

## CSS approach for imports

```tsx
import './style.css';  // webpack handles it

// External CSS
await loadCSSFromURLAsync('https://cdn.example.com/library.css');

// Dynamic CSS
loadCSSFromString('.my-card { border: 1px solid #ddd; }');
```

## Color system from the toolkit

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

## Dark Mode

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

## CVA for variant styling

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
