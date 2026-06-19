# Shared AI Memory - Nortiqa Lab

Status: versionable draft  
Date: 2026-06-17  
Scope: Nortiqa Lab only  
Canonical root: MEM-NL-ROOT-001 in Notion  

## Objective

Turn Nortiqa Lab shared memory into a simple operating system for AI agents:
any AI should be able to start a session, read the canon, understand limits,
do reversible work, and leave continuity.

## Current Canon

The canonical memory root already exists in Notion:

- MEM-NL-ROOT-001 - Raiz de Memoria Canonica.
- DICT-NL-MEM-001-CLAUDE - Dictamen de arquitectura de memoria comun.
- OT-NL-MEM-001 - Implementacion Fase 1 Memoria Comun IAs.

Confirmed rules:

- Native AI memory is not a source of truth.
- Notion is the canon.
- Writing to canon requires PAO/OT and explicit authorization from Gio.
- Nortiqa, Valent, ERP, Surlancer, and client contexts must not be mixed.

## Phase 2 Problem

The root exists, but the operating routine for multiple AIs is still thin.
The main risks are:

- An AI operates from stale memory.
- An AI does not read the canon before acting.
- Handoffs remain scattered in chats.
- Decisions lack clear state: draft, approved, blocked, obsolete.
- Notion pages are duplicated instead of linked.

## Deliverables

### 1. Repository AI Instructions

`AGENTS.md` gives Codex and other coding agents a local entrypoint with:

- MEM-NL-ROOT-001 link.
- Canon-first rule.
- Context isolation.
- Protected-piece rules.
- Startup checklist.
- Handoff rule.

### 2. Session Handoff Template

Use `handoff-template.md` to close substantial sessions without losing context.

### 3. Bootstrap Packet

Use `bootstrap-packet.md` when a Notion connector is unavailable. It does not
replace MEM-NL-ROOT-001.

### 4. Future Memory State Registry

Do not create this in Notion yet. Proposed future fields:

- Piece code.
- Type: root, plan, dictamen, OT, PAO, handoff, draft.
- State: canonical, draft, blocked, obsolete.
- Owner.
- Last validated read.
- Risk level.

## Proposed Operating Flow

1. AI starts a session.
2. AI reads `AGENTS.md` or equivalent instruction.
3. AI reads MEM-NL-ROOT-001.
4. AI fetches active plans, dictamens, and OTs.
5. AI classifies the task:
   - read/synthesis,
   - local draft,
   - versionable change,
   - protected canonical change,
   - VPS/staging/production action.
6. AI executes only allowed work.
7. AI leaves a handoff.
8. If the result must become canon, Gio authorizes PAO/OT before Notion is
   updated.

## State Policy

- Canonical: official current source in Notion.
- Local draft: file in repo or `.drafts/`, not official.
- Proposal: ready for Gio/Claude review, not canon yet.
- Blocked: requires human input, PAO/OT, secret, snapshot, or manual action.
- Obsolete: replaced by a later piece.

## Guardrails

- Do not store secrets in Notion or this repo.
- Do not copy data from another entity.
- Do not assume staging or VPS match local state.
- Do not mark untested work as validated.
- Do not create new memory roots when MEM-NL-ROOT-001 already exists.

## Next Step

Validate with Gio whether Phase 2 should proceed as:

1. Local/versionable package only for now.
2. PAO for a Notion "Memory State Registry".
3. Rollout of `AGENTS.md` across Nortiqa repositories.

