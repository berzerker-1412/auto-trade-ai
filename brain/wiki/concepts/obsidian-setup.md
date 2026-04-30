---
title: Obsidian Vault Setup
type: concept
tags: [obsidian, pkm, tools, setup, web-clipper]
sources: 0
created: 2026-04-14 15:30
updated: 2026-04-14 15:30
---

Configuration and workflow for this Obsidian vault (2nd Brain at `~/Desktop/Brain/2nd Brain`).

## Core Plugins (enabled)

| Plugin | Purpose |
| --- | --- |
| file-explorer | Sidebar file tree |
| global-search | Full-text search across vault |
| switcher | Quick file open (Cmd+O) |
| graph | Knowledge graph view |
| backlink | Incoming link panel |
| canvas | Visual whiteboard notes |
| outgoing-link | Outgoing link panel |
| tag-pane | Tag browser |
| properties | YAML frontmatter editor |
| page-preview | Hover preview on links |
| daily-notes | Daily note creation |
| templates | Insert template snippets |
| note-composer | Merge/split notes |
| command-palette | Cmd+P command launcher |
| bookmarks | Starred files/searches |
| outline | Heading tree panel |
| word-count | Footer word/char count |
| file-recovery | Auto snapshot backup |
| sync | Obsidian Sync |
| bases | Database-style views |

## Community Plugins (enabled)

| Plugin | Purpose |
| --- | --- |
| obsidian-kanban | Kanban boards in markdown |
| terminal | Embedded terminal in sidebar |

## Community Plugins (installed, not enabled)

| Plugin | Notes |
| --- | --- |
| dataview | Query notes as a database — available but off |
| obsidian-excalidraw-plugin | Whiteboard drawing — available but off |
| breadcrumbs | Hierarchy navigation — available but off |

---

## Web Clipping — Obsidian Web Clipper

**Tool:** [Obsidian Web Clipper](https://obsidian.md/clipper) — official browser extension by Obsidian.

**Install:** Chrome / Firefox / Safari / Edge → search "Obsidian Web Clipper" in extension store.

### How it works

1. Browse to any page
2. Click the extension icon (or use keyboard shortcut)
3. Clipper converts the page to Markdown, fills template variables
4. Saves directly into vault via Obsidian URI

### Recommended Configuration for this Vault

**Save location:** `raw/` — keeps source material separate from wiki and สมุด

**Template** (set in extension settings):

```text
---
title: {{title}}
url: {{url}}
clipped: {{date:YYYY-MM-DD}}
tags: [clipped]
---

{{content}}
```

**Template variables available:**

| Variable | Output |
| --- | --- |
| `{{title}}` | Page title |
| `{{url}}` | Source URL |
| `{{date}}` | Today's date (format with `:YYYY-MM-DD`) |
| `{{content}}` | Full page content as Markdown |
| `{{highlights}}` | Text you highlighted before clipping |
| `{{author}}` | Page author (if available) |
| `{{description}}` | Meta description |
| `{{domain}}` | Domain name |

### Workflow After Clipping

1. Clipped file lands in `raw/` as Markdown
2. Read through it — find the 3–5 most important takeaways
3. Run INGEST workflow (see [[CLAUDE.md conventions]]):
   - Create `wiki/sources/<slug>.md`
   - Update relevant `wiki/entities/` and `wiki/concepts/` pages
   - Sync to `สมุด/` in Thai
   - Update `wiki/index.md` and append to `wiki/log.md`

### Tips

- **Highlight before clipping** — selected text becomes `{{highlights}}`, useful for pulling just the key quotes
- **Edit in clipper popup** — can trim/edit content before saving, avoid clipping full-page nav noise
- **Interpreter mode** — Web Clipper can run an Obsidian AI interpreter to auto-generate summaries and tags (requires Obsidian API key config)

---

## Vault Structure

```text
2nd Brain/
├── CLAUDE.md          ← schema + workflow for Claude Code
├── raw/               ← source documents (web clips land here)
│   └── assets/        ← images referenced by raw docs
├── สมุด/              ← Thai notes (human-written, informal)
│   ├── index.md
│   ├── concepts/
│   ├── entities/
│   ├── sources/
│   └── projects/
└── wiki/              ← English knowledge base (Claude-maintained)
    ├── index.md
    ├── log.md
    ├── overview.md
    ├── concepts/
    ├── entities/
    ├── sources/
    └── projects/
```

## Related Pages

- [[claude-setup/index|Claude Code Setup]] — hooks, skills, CLAUDE.md conventions
- [[soul-md]] — AI character/personality pattern
