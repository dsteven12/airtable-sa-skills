---
name: frontend-design
description: "Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when building web components, pages, artifacts, dashboards, React components, HTML/CSS layouts, or when styling/beautifying any web UI. Generates creative, polished code that avoids generic AI aesthetics. MANDATORY TRIGGERS: frontend, UI design, web design, make it look good, beautify, redesign, design system, landing page, dashboard design, polish the UI, make it pretty, it looks clunky, visual refresh."
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints.

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:

- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc. There are so many flavors to choose from. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work — the key is intentionality, not intensity.

Then implement working code (HTML/CSS/JS, React, Vue, etc.) that is:

- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines

Focus on:

- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics; unexpected, characterful font choices. Pair a distinctive display font with a refined body font. Use Google Fonts CDN when building HTML/JSX artifacts.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes. Build a full palette: background, surface, text primary, text secondary, accent, accent-subtle, border, hover states.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. For React artifacts, use CSS transitions and keyframes. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density. Avoid the generic equal-padding-on-everything look.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, and grain overlays.
- **Visual Hierarchy**: Every screen should have ONE thing that screams "look here first." Then a clear path for the eye to follow. If everything is the same visual weight, nothing stands out and the UI feels flat and overwhelming.

## Anti-Patterns — What to NEVER Do

NEVER use generic AI-generated aesthetics:

- Overused font families (Inter, Roboto, Arial, system fonts as the only choice)
- Cliched color schemes (particularly purple gradients on white backgrounds, or the "SaaS blue" #2563EB on white)
- Predictable layouts: equal-width grid cards with identical padding, centered everything, symmetric columns
- Cookie-cutter component patterns that lack context-specific character
- Rainbow badge soup — too many small colorful pills competing for attention
- Wall-of-cards syndrome — grids of identically-styled cards with no visual hierarchy
- Data-dump dashboards — showing every metric at once with no storytelling or progressive disclosure

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should look the same as the last thing you built. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices across generations.

## Wireframe & Prototype Specific Guidance

When building wireframes, prototypes, or interface mockups (common in Airtable interface design work):

- **Progressive Disclosure**: Don't show everything at once. Use tabs, accordions, expandable sections, or multi-step flows to manage complexity. The user should see exactly what they need for their current task.
- **Information Architecture**: Group related items visually. Use whitespace as a separator, not just borders. Establish clear zones: navigation, primary content, supporting context, actions.
- **State Communication**: Show hover, active, selected, empty, loading, and error states. A wireframe that only shows the "happy path full state" is incomplete.
- **Density Control**: Match information density to the user's expertise level and task. Power users want density. New users want breathing room. Design for the primary user.

## Implementation Notes for Claude Artifacts (JSX)

When building React JSX artifacts for Claude's artifact renderer:

- All styles must be inline (style objects) or use Tailwind utility classes
- Import React hooks at the top: `import { useState } from "react"`
- Google Fonts can be loaded via `@import` in a style tag or `<link>` in an HTML wrapper
- Available libraries: lucide-react, recharts, d3, shadcn/ui, lodash, Three.js
- NEVER use localStorage or sessionStorage — use React state instead
- Use a default export for the main component

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.

Remember: Claude is capable of extraordinary creative work. Don't hold back — show what can truly be created when thinking outside the box and committing fully to a distinctive vision.
