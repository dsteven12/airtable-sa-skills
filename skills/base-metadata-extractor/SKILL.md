---
name: base-metadata-extractor
description: "Shared extraction toolkit for pulling complete Airtable base metadata — schema via the Airtable MCP connector, plus optional automation and interface extraction via browser console scripts. Dependency read by doc-generating and analysis skills (technical-design-doc, health-check, training-guide, etc.) before they need base context. Schema extraction uses MCP tools (list_tables_for_base, get_table_schema, list_records_for_table). Automation and interface extraction require browser console scripts."
---

# Base Metadata Extractor

Shared extraction toolkit for pulling complete Airtable base metadata. This file is **read by other skills at extraction time** — it is not typically invoked directly.

**Consuming skills:** `technical-design-doc`, `health-check`, `training-guide`, and any future skill that needs base schema, automation, or interface data should read this file before beginning their data-gathering step.

---

## Overview

Base metadata comes from two sources depending on what's available through the Airtable MCP connector:

| Data | Source | Method |
|------|--------|--------|
| **Schema** (tables, fields, types, options, configs) | Airtable MCP Connector | `list_tables_for_base` + `get_table_schema` |
| **Record samples** (counts, field usage) | Airtable MCP Connector | `list_records_for_table` |
| **Automations** (triggers, actions, decisions) | Browser console script | User runs script and pastes JSON |
| **Interface pages** (layouts, elements, filters) | Browser console script (2-part) | User runs scripts and pastes JSON |

The general workflow for any consuming skill is:

1. **Schema** — Always extract via MCP first (no user action required)
2. **Automations** — Present the browser console script if the consuming skill needs automation data
3. **Interfaces** — Present the 2-part browser console script if the consuming skill needs interface data
4. User pastes any browser console output back into the conversation
5. Consuming skill processes all gathered data for its specific purpose

---

## Schema Extraction (MCP Connector)

Schema extraction is fully automated through the Airtable MCP tools. No user scripts required.

### Step 1: Find the Base

Use one of:
```
search_bases(searchQuery: "customer base name")
list_bases()
```

This returns the `baseId` (e.g., `appXXXXXXXXXXXXXX`).

### Step 2: Get All Tables and Fields

```
list_tables_for_base(baseId: "appXXXXXXXXXXXXXX")
```

This returns every table with:
- Table ID, name, description
- All fields per table: field ID, name, type
- Field configuration summary

### Step 3: Get Detailed Field Configs (When Needed)

For fields where you need full configuration details (select options, linked table targets, formula expressions, rollup configs), use:

```
get_table_schema(
  baseId: "appXXXXXXXXXXXXXX",
  tables: [{ tableId: "tblXXXXXXXXXXXXXX", fieldIds: ["fldXXXXXXXXXXXXXX", ...] }]
)
```

This returns the complete field config including:
- **Single/Multi Select**: choice IDs, names, colors
- **Linked Records**: linked table ID, inverse link field ID, single-record preference
- **Formulas**: expression string, result type
- **Rollups**: source field, link field, aggregation function, result type
- **Lookups**: source field, link field, result type
- **Currency/Number**: precision, symbol
- **Date/DateTime**: format, timezone
- **Rating**: max value

### Step 4: Sample Records (When Needed)

To understand field usage patterns, record counts, or see real data:

```
list_records_for_table(
  baseId: "appXXXXXXXXXXXXXX",
  tableId: "tblXXXXXXXXXXXXXX",
  fieldIds: ["fldXXXXXXXXXXXXXX", ...],
  pageSize: 10
)
```

Useful for:
- Estimating record counts (check if there's a `nextCursor` for more pages)
- Seeing how fields are actually used (which selects are common, what formulas produce)
- Identifying empty tables vs. populated ones
- Understanding naming conventions and data patterns

### Schema Metrics for Consuming Skills

After MCP extraction, compile these metrics that consuming skills commonly need:

| Metric | How to Calculate |
|--------|-----------------|
| **Table count** | Count of tables returned |
| **Field count per table** | Count of fields in each table |
| **Link fields per table** | Fields where type = `multipleRecordLinks` |
| **Computed fields per table** | Fields where type in (`formula`, `multipleLookupValues`, `rollup`, `count`) |
| **Select fields** | Fields where type in (`singleSelect`, `multipleSelects`) — note choice options |
| **Attachment fields** | Fields where type = `multipleAttachments` |
| **Repeated slot patterns** | Fields matching numbered patterns (e.g., "Vendor Type 1"..."Vendor Type 8") — count distinct groups and slots per group |

---

## Automation Extraction (Browser Console Script)

The Airtable MCP connector does not expose automations. This browser console script captures all automations from the live base.

### What It Captures

- Automation name
- Deployment status (active vs disabled)
- Trigger type (human-readable)
- Actions list (in execution order)
- Decision/branching logic (conditionals, fan-outs, reducers)

### How to Present to the User

Tell the user:

> "Open your Airtable base in the browser (make sure the URL contains the base ID starting with `app`). Open DevTools (F12 or ⌘+Option+I) → Console tab → paste this script and press Enter. Copy the JSON output that appears after `=== AUTOMATIONS DATA ===` and paste it here."

### Script

```javascript
(async()=>{const baseId=window.location.pathname.match(/(app[A-Za-z0-9]+)/)?.[1];if(!baseId){console.error("Could not detect base ID from URL. Make sure you are on the correct Airtable base.");return;}const sid=(performance.getEntriesByType("resource").find(e=>e.name.includes("secretSocketId"))?.name.match(/secretSocketId=([^&]+)/)||[])[1];if(!sid){console.error("Could not find secretSocketId. Try refreshing the page and running again.");return;}console.log("Base ID:",baseId,"| secretSocketId:",sid);const t={"wttRECORDMATCHES0":"When record matches conditions","wttRECORDUPDATED0":"When record updated","wttCRON0000000000":"Scheduled","wttCONNECTIONINPT":"Button press","wttFORMSUBMITTED0":"Form submitted","wttRECORDCREATED0":"When record created","wttOUTLOKEVTCREAT":"Outlook event created","watUPDATERECORD00":"Update record","watCREATERECORD00":"Create record","watFINDRECORDS000":"Find records","watGMAILSENDMAIL0":"Send Gmail","watSENDTOSLACK000":"Send Slack message","watAIGENERATE0000":"AI Generate","watBETUHIcuho4hit":"Send email","watRUNSCRIPT00000":"Run script","watCUSTOMSCRIPT00":"Custom script","wdtNWAY0000000000":"Conditional (N-way)","wdtFANOUT00000000":"Fan-out (for each)","wdtREDUCER0000000":"Reducer"};try{const r=await fetch(`https://airtable.com/v0.3/application/${baseId}/listWorkflows?stringifiedObjectParams=%7B%7D&requestId=req${Date.now()}&secretSocketId=${sid}`,{credentials:"include",headers:{"x-airtable-application-id":baseId,"x-airtable-inter-service-client":"webClient","x-requested-with":"XMLHttpRequest","x-time-zone":Intl.DateTimeFormat().resolvedOptions().timeZone,"x-user-locale":"en"}});const d=await r.json();if(!d.data?.workflows){console.error("No workflows found. Response:",JSON.stringify(d));return;}const w=d.data.workflows.map(w=>({name:w.name,deployed:w.deploymentStatus==="deployed",trigger:t[w.trigger?.workflowTriggerTypeId]||w.trigger?.workflowTriggerTypeId||"Unknown",actions:Object.values(w.graph?.actionsById||{}).map(a=>t[a.workflowActionTypeId]||a.workflowActionTypeId),decisions:Object.values(w.graph?.decisionsById||{}).map(d=>t[d.workflowDecisionTypeId]||d.workflowDecisionTypeId)}));console.log("=== AUTOMATIONS DATA ===");console.log(JSON.stringify(w,null,2));}catch(e){console.error("Fetch failed:",e.message,"— Make sure you are on the correct base page and try refreshing.");}})()
```

### Automation Data Structure

```json
[
  {
    "name": "Send welcome email on signup",
    "deployed": true,
    "trigger": "When record created",
    "actions": ["Find records", "Send email", "Update record"],
    "decisions": ["Conditional (N-way)"]
  }
]
```

---

## Interface Page Extraction (Browser Console — 2-Part)

The Airtable MCP connector does not expose interface page layouts. Interface extraction is a two-step process because page IDs must be discovered from the browser's resource cache before their layouts can be fetched.

### What It Captures

- All interface page IDs
- Full page layouts: element types, data sources, filters, controls, custom extensions
- Drill-down page relationships
- Edit/create/delete permissions per element

### Part 1 — Page ID Discovery

Tell the user:

> "First, open the Interface Designer for your base and **click through every page tab** so the browser caches each page. Then open DevTools (F12) → Console → paste this script and press Enter. Copy the array of page IDs and paste it here."

**Part 1 Script:**

```javascript
(()=>{const pageIds=new Set();performance.getEntriesByType("resource").forEach(e=>{const m=e.name.match(/\/(pag[A-Za-z0-9]+)/g);if(m)m.forEach(p=>pageIds.add(p.slice(1)));});const urlMatch=window.location.href.match(/(pag[A-Za-z0-9]+)/g);if(urlMatch)urlMatch.forEach(p=>pageIds.add(p));document.querySelectorAll("a[href*='/pag']").forEach(a=>{const m=a.href.match(/(pag[A-Za-z0-9]+)/g);if(m)m.forEach(p=>pageIds.add(p));});console.log("=== INTERFACE PAGE IDS ===");console.log(JSON.stringify([...pageIds]));console.log("Found",pageIds.size,"pages. Now run Part 2 below to fetch details.");})()
```

### Part 2 — Fetch Page Layouts

After the user provides the page IDs array, **replace `PAGE_IDS_ARRAY`** in this script with the actual array before giving it to the user:

Tell the user:

> "Run this second script in the same browser console tab. Copy the JSON output after `=== INTERFACE DATA ===` and paste it here."

**Part 2 Script:**

```javascript
(async()=>{const pages=PAGE_IDS_ARRAY;const baseId=window.location.pathname.match(/(app[A-Za-z0-9]+)/)?.[1];const sid=(performance.getEntriesByType("resource").find(e=>e.name.includes("secretSocketId"))?.name.match(/secretSocketId=([^&]+)/)||[])[1];if(!baseId||!sid){console.error("Missing baseId or secretSocketId. Refresh and try again.");return;}const results={};for(const pid of pages){try{const r=await fetch(`https://airtable.com/v0.3/page/${pid}/readData?stringifiedObjectParams=%7B%22expectedPageLayoutSchemaVersion%22%3A26%7D&requestId=req${Date.now()}&secretSocketId=${sid}`,{credentials:"include",headers:{"x-airtable-application-id":baseId,"x-airtable-inter-service-client":"webClient","x-requested-with":"XMLHttpRequest","x-airtable-integration-id":pid,"x-time-zone":Intl.DateTimeFormat().resolvedOptions().timeZone,"x-user-locale":"en"}});const d=await r.json();results[pid]={status:r.status,data:d};}catch(e){results[pid]={status:"error",error:e.message};}}console.log("=== INTERFACE DATA ===");console.log(JSON.stringify(results,null,2));})()
```

---

## Reference: Type ID Mappings

### Known Trigger Type IDs

| ID | Label |
|----|-------|
| `wttRECORDMATCHES0` | When record matches conditions |
| `wttRECORDUPDATED0` | When record updated |
| `wttCRON0000000000` | Scheduled |
| `wttCONNECTIONINPT` | Button press |
| `wttFORMSUBMITTED0` | Form submitted |
| `wttRECORDCREATED0` | When record created |
| `wttOUTLOKEVTCREAT` | Outlook event created |

### Known Action Type IDs

| ID | Label |
|----|-------|
| `watUPDATERECORD00` | Update record |
| `watCREATERECORD00` | Create record |
| `watFINDRECORDS000` | Find records |
| `watGMAILSENDMAIL0` | Send Gmail |
| `watSENDTOSLACK000` | Send Slack message |
| `watAIGENERATE0000` | AI Generate |
| `watBETUHIcuho4hit` | Send email |
| `watRUNSCRIPT00000` | Run script |
| `watCUSTOMSCRIPT00` | Custom script |

### Known Decision Type IDs

| ID | Label |
|----|-------|
| `wdtNWAY0000000000` | Conditional (N-way branch) |
| `wdtFANOUT00000000` | Fan-out (for each record) |
| `wdtREDUCER0000000` | Reducer (aggregate) |

If a type ID is not in the tables above, display it as-is — Airtable may have added new types.

### Interface Element Type Reference

| Element Type | Description |
|-------------|-------------|
| `dashboard` | Dashboard view with charts, big numbers, pivot tables |
| `inbox` | Inbox-style record browser with thumbnails |
| `levels` | Hierarchical grid/list view |
| `chart` | Bar, line, or pie chart |
| `bigNumber` | KPI summary number |
| `pivotTable` | Cross-tab pivot table |
| `blockInstallationInQueryContainer` | Custom extension (Interface Extension) |
| `queryContainer` | Data source with filters, search, sort controls |
| `section` / `sectionGridRow` | Layout containers |
| `verticalStack` | Vertical layout container |

### Key Interface Properties to Document

- `source.tableId` — which table powers the element
- `staticFilters` — hardcoded filters (e.g., current user email)
- `editability` — what users can create/update/delete
- `endUserControls` — filter, sort, search, group toggles
- `blockInstallationData.blockName` — custom extension name
- `drillDownExpandedRow.pageId` — linked detail pages

---

## Authentication Details (Browser Console Scripts)

Both console scripts (automations + interfaces) use the same auth mechanism:

- **Cookies** — via `credentials: "include"` (uses the logged-in session)
- **Required headers:** `x-requested-with: XMLHttpRequest`, `x-airtable-application-id: {baseId}`, `x-airtable-inter-service-client: webClient`, `x-time-zone: {timezone}`, `x-user-locale: en`
- **Required query parameter:** `secretSocketId` — a session-specific token tied to the WebSocket connection, extracted from `performance.getEntriesByType('resource')`

### API Endpoints

| Endpoint | Purpose | ID Pattern |
|----------|---------|------------|
| `v0.3/application/{baseId}/listWorkflows` | List all automations | `app` prefix |
| `v0.3/page/{pageId}/readData` | Interface page layout | `pag` prefix |

---

## Troubleshooting (Browser Console Scripts)

| Issue | Solution |
|-------|----------|
| `Could not find secretSocketId` | WebSocket may not be initialized. Look in browser console for a **heartbeat log** containing `socrXXXXXXXXXXXXXX`. Hardcode it: replace `const sid = (performance...)` with `const sid = "YOUR_EXTRACTED_SOCKET_ID";` |
| `ERR_BLOCKED_BY_CLIENT` | **Ad blocker is blocking internal API calls.** Temporarily disable it for the Airtable tab, or use incognito with no extensions. |
| Both secretSocketId missing + fetch errors | Most common combo. Apply both fixes: (1) disable ad blocker, (2) hardcode secretSocketId from heartbeat log. Resolves ~90% of failures. |
| `401 Unauthorized` | Expired session or secretSocketId. Refresh the page and re-run. |
| `Failed to fetch` | Check for ad blocker first. Then verify URL contains correct base ID. |
| No page IDs found | Navigate through all interface pages first to populate resource cache, then re-run discovery script. |
| `404 MODEL_ID_NOT_FOUND` | Deleted page — skip safely. |

---

## Which Data to Extract When

Not every consuming skill needs all extraction methods. Use this guide:

| Skill | Schema (MCP) | Automations (Console) | Interfaces (Console) |
|-------|-------------|----------------------|---------------------|
| `technical-design-doc` | Required | Strongly recommended | Strongly recommended |
| `health-check` | Required | Optional (deeper analysis) | Optional |
| `training-guide` | Helpful | Not needed | Strongly recommended (for UI docs) |

When a consuming skill reads this file, it should determine which extraction methods are relevant and only use/present those — don't ask the user to run browser scripts if only MCP schema data is needed.
