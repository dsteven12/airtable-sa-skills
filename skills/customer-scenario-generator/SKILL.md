---
name: customer-scenario-generator
description: "Generate a realistic, demo-ready customer scenario from a bare pattern description or learning objective. Produces a complete fictional company with named stakeholders, direct quotes, specific pain points, team composition, and business context — plus an optional Airtable schema skeleton (tables, primary fields, key links, field types) ready for design review. MANDATORY TRIGGERS: customer scenario, generate a scenario, fictional company, demo scenario, use case scenario, create a customer story, frame this as a customer, make up a company, workshop scenario, learning scenario. ALWAYS invoke when the user needs a realistic customer framing for a learning exercise, demo, workshop, or pattern exploration — even if they just say 'give me a scenario for testing AI extraction' or 'I need a fake company for this demo'."
---

# Customer Scenario Generator

Generate realistic, demo-ready customer scenarios from bare technical requirements. The output should feel like notes from a real discovery call — specific enough to ground every design decision in customer value, rich enough to walk someone through as a demo narrative.

## Why Scenarios Matter

Abstract pattern descriptions ("learn structured extraction") produce abstract solutions. Customer scenarios ("Marcus at Orion Consulting lost a deliverable because action items from a meeting never made it into the tracker") produce grounded solutions where every design choice has a "because the customer needs..." justification. This is especially valuable for:

- **Learning builds**: Approaching design as "post-discovery-call" exercises pattern recognition that transfers to real engagements
- **Demos**: Walking a prospect through a named company with real-sounding pain points is more compelling than showing a generic template
- **Workshops**: Participants engage more deeply when the scenario feels real
- **Pattern exploration**: When you're testing a new Airtable pattern, a scenario forces you to think about edge cases that pure technical exploration misses

## Input

The user provides any combination of:

- **Technical patterns** to exercise (e.g., "AI structured extraction with linked record creation")
- **Learning objectives** (e.g., "practice the Hybrid linking pattern")
- **Design principles** to apply (e.g., "exercise Risk 4 — implicit automation chains")
- **Target audience** (e.g., "mid-market ops team", "enterprise marketing department")
- **Constraints** (e.g., "needs to involve translations", "should be a consulting firm")

Minimal input is fine — even just "give me a scenario for testing conditional automations" is enough to work with.

## Scenario Anatomy

Every generated scenario follows this structure. These elements are the result of trial and error — each one exists because leaving it out produced scenarios that were too thin to design against.

### 1. Company Profile

- **Name**: Distinctive, memorable, appropriate to the industry. Not generic ("Acme Corp") — evocative of the business (*Sélene Beauty*, *Greenline Media*, *Orion Consulting Group*).
- **Industry**: Specific enough to imply workflows. "Marketing agency" beats "company." "DTC skincare brand selling online across four countries" beats "beauty company."
- **Size**: Team size matters for design decisions. A 5-person team has different needs than a 200-person team. State the number and the team composition.
- **Geography**: Where they operate, especially if it affects workflows (multi-region, multi-language, time zones).

### 2. Team Composition

Name the specific roles that interact with the system being designed. These become your personas for interface design and permission scoping.

- How many people in each role
- Which roles create data, which consume it, which approve/review
- Who's the decision-maker (this person's quote drives the "why")
- Who's the day-to-day user (this person's workflow drives the "how")

### 3. Named Stakeholders (2-3 people)

Each stakeholder needs:
- **Name**: First name only is fine. Pick names that feel real and are easy to reference in conversation.
- **Role**: Their title and what they actually do (not just "Manager" — "managing editor who oversees the content calendar and reports to the VP of Marketing").
- **Direct quote**: This is the most important element. The quote should:
  - Express a specific pain point in their own words
  - Reveal the business impact (missed deadlines, lost revenue, team frustration)
  - Sound like something a real person would say in a discovery call — conversational, not polished
  - Give the SA a design anchor ("we're building this because Priya said...")

### 4. Current State (The Pain)

How they work today, in enough detail to understand what's broken:
- What tools they currently use (and how they're failing)
- Where information gets lost or delayed
- The specific workflow breakdown that causes pain
- A concrete anecdote if possible ("last quarter, a partner promised a client...")

### 5. Desired State (The Ask)

What they want the solution to do, stated in their language (not Airtable jargon):
- The capability they're asking for
- The outcome they expect
- Any specific requirements they've mentioned

### 6. Business Context

Details that shape design decisions:
- Volume: How many records/items/transactions per week/month
- Cadence: Daily workflow? Weekly batch? Event-driven?
- Integrations: What other systems are in play
- Growth trajectory: Is this stable or scaling

## Schema Skeleton

After the narrative, produce a starter schema that translates the scenario into an Airtable data model. This is a starting point for design review — not a final schema.

### Format

For each table:

```
TABLE: [Table Name]
Purpose: [One sentence — what this table tracks]
Primary field: [Name] ([type])
Key fields:
  - [Field Name] ([Type]) — [why it's needed]
  - [Field Name] ([Type]) — [why it's needed]
Records represent: [what one row means]
Expected volume: [estimate based on business context]
```

Then a linking summary:

```
RELATIONSHIPS:
- [Table A] → [Table B]: [relationship type] ([Pattern N — name])
  Reason: [why this linking strategy]
- [Table A] → [Table B]: [relationship type] ([Pattern N — name])
  Reason: [why this linking strategy]
```

### Schema Principles

- **3-5 tables max** per scenario. Enough to exercise linking patterns without overcomplicating.
- **Name tables as hub nouns** — People, Meetings, Content, Projects — not actions or processes.
- **Include linking strategy rationale** — every link should reference which Pattern (1-5) and why. If the choice is debatable, say so — that's a design conversation the user should have with the design-advisor skill.
- **Flag deliberate design decision points** — places where the scenario creates a genuine tradeoff (e.g., "Author could be Collaborator-only or Hybrid — depends on whether rollups are needed").
- **Include AI-relevant fields** if the scenario involves AI patterns — note which fields would be AI-generated and what type (AI field vs. automation AI action).
- **Estimate volumes** from the business context — this matters for scaling decisions.

## Generation Principles

### Authenticity Over Cleverness
The scenario should feel like it came from a real discovery call, not a creative writing exercise. Real customers describe problems in messy, specific terms. They mention the tool they're frustrated with by name. They reference specific incidents. Keep that texture.

### Cultural and Industry Specificity
When the scenario involves specific cultures, industries, or domains, get the details right. If it's a consulting firm, consultants really do lose action items in meeting notes. If it's a DTC brand doing localization, the cultural adaptation challenges are real (Tagalog honorifics, Italian marketing tone, LatAm vs. Castilian Spanish). Surface-level details feel fake; specific details feel real.

### Design Tension is a Feature
Good scenarios create genuine design tradeoffs — not one obvious answer, but 2-3 reasonable approaches with different pros and cons. This is what makes the scenario useful for learning: the user has to think through the tradeoffs, not just follow a recipe.

### Scale the Complexity to the Patterns
If the user wants to exercise one pattern, the scenario should be focused. If they want to exercise five patterns, the scenario needs enough business complexity to justify all five without feeling contrived. Don't add complexity for complexity's sake — every element should earn its place.

### Demo Narrative Arc
The scenario should tell a story that works when walking someone through it:
1. Here's the company and their problem (empathy)
2. Here's what they asked for (requirements)
3. Here's how we designed it (architecture)
4. Here's what it looks like in Airtable (demo)
5. Here's why we made these specific choices (expertise)

The scenario generator provides steps 1-2. The design and build work provides 3-5.

## Integration with Other Skills

- **airtable-design-advisor**: The schema skeleton is designed to be handed directly to the design-advisor for review. It includes linking strategy references and deliberate decision points that the advisor can evaluate.
- **engagement-orchestrator**: For learning builds, the generated scenario becomes the customer context in the engagement's SCOPE phase.
- **workflow-doc**: If the scenario is developed into a formal engagement, the narrative can seed the workflow-doc's project summary and user stories.
- **learning-loop**: The Brief mode references the scenario's target patterns to set learning objectives.
