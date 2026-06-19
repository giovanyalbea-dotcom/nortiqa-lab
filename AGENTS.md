# Nortiqa Lab - Shared AI Context

## Rule 0 - Canonical Memory First

Before doing any work in this repository, read the canonical Notion root:

**MEM-NL-ROOT-001 - Raiz de Memoria Canonica**  
https://app.notion.com/p/382e4fe3bfea818aacfad4f9793a697f

The canonical source of truth is Notion. Local files, chat history, IDE state,
and native AI memory are helpers only.

If Notion is unavailable, continue only with local, reversible work and clearly
mark the result as a draft.

## Project Context

- Nortiqa Lab is an AI agent factory based in Rio Gallegos, Patagonia.
- This local repository contains public/site assets, support scripts, and
  versionable drafts. Production apps and staging services live on the VPS.
- Motto: "Primero funcional. Despues excelente. Siempre: lo mejor o nada."

## Context Isolation

Never mix contexts between:

- Nortiqa Lab
- Valent Capital Group
- ERP Gio+Edson
- Surlancer or client-specific projects

No secret, client data, operational token, or internal decision from one entity
may be copied into another entity context.

## Protected Pieces

Do not create, edit, replace, or reorganize protected Notion roots, mother
documents, dictamens, PAOs, OTs, or official databases unless Gio explicitly
authorizes it and the applicable PAO/OT exists.

Allowed without extra authorization:

- Read canon and summarize it.
- Create local drafts in `.drafts/`.
- Update versionable technical files in this repository when requested.
- Propose checklists, handoffs, schemas, and implementation plans.

## Session Startup Checklist

1. Read `AGENTS.md` and `CLAUDE.md`.
2. Read MEM-NL-ROOT-001 in Notion when the connector is available.
3. Identify active plans, dictamens, OTs, and blocked actions.
4. Check `git status --short` before editing.
5. Keep unrelated user changes intact.
6. If touching VPS/staging, confirm the current operational gate first.

## Handoff Rule

Any substantial AI session should leave a short handoff containing:

- Date and actor.
- Canon sources read.
- What changed.
- What was verified.
- What remains blocked.
- Next safest step.

Use `.drafts/AI_SESSION_HANDOFF_TEMPLATE.md` as the local template.

