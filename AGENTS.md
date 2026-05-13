# Viche Agent Guide

## Project Context

Viche is a civic deliberation platform project. Treat this repository as the project root for source, documents, architecture notes, and future implementation work.

The current root is documentation-first. Before making technical or product decisions, read:

- `TechnicalTask.md`
- `Architecture.md`

Those files describe the intended platform as an API-first civic infrastructure project with identity, sortition, deliberation, auditability, correspondence, public transparency, and multilingual presentation.

## Language and Duplicate Documents

Some root documents exist in multiple languages. Keep the Ukrainian version as the authoritative project text when documents disagree, unless a specific file states otherwise.

Known language pairs:

- `Маніфест Віче.md` is the Ukrainian counterpart of `The Viche Manifesto.md`.
- `Протокол мандата Віче.md` is the Ukrainian counterpart of `Viche Mandate Protocol.md`.

When editing duplicated documents:

- Prefer editing the Ukrainian source first.
- Keep translated versions aligned in meaning, not necessarily word-for-word.
- Preserve legal, civic, and procedural nuance across translations.
- Do not silently delete duplicate-language files.
- If a translation is intentionally partial or outdated, mark that explicitly in the file.

## Product and Architecture Principles

Follow the direction already established in the project notes:

- Build as civic infrastructure, not as a campaign tool, party tool, or social media clone.
- Prefer a modular monolith for the first implementation, with clear internal boundaries and API-first contracts.
- Keep Ukrainian as the canonical domain language and support multilingual output through a versioned translation layer.
- Separate authoritative process data from comments, reactions, summaries, and public discourse.
- Design identity with progressive assurance: low-friction accounts for basic participation and stronger verification/signature for high-trust actions.
- Keep public verifiability separate from public exposure of personal data.
- Use append-only audit logs, reproducible procedures, transparency checkpoints, and signed artifacts where trust matters.
- Treat AI as an assistant for deduplication, search, moderation queues, summarization, and translation support; never as the source of official will, mandates, votes, or final resolutions.

## Domain Boundaries

Central domain concepts include:

- members and verified members
- eligibility and assurance methods
- proposals, issues, evidence, and duplicate/alternative graphs
- sortition, panels, mandates, and rotation
- deliberation rooms, agendas, witnesses, transcripts, and resolutions
- official correspondence, responses, deadlines, and follow-up
- audit events, public transparency logs, and reproducibility proofs

Avoid designs centered on personal targeting. The system should focus on institutions, offices, services, territories, problems, proposals, panels, resolutions, and accountable public follow-up.

## Safety and Legal Posture

Viche must remain a lawful civic instrument. Do not add workflows that promote:

- electoral campaigning or candidate support/opposition
- doxxing, harassment, intimidation, or personal persecution
- unlawful investigation, surveillance, hacking, or covert collection
- secret private deals by mandate holders
- claims that Viche replaces courts, elections, journalism, or state institutions

Technical features should reinforce this posture through permissions, audit trails, moderation paths, conflict-of-interest handling, and clear public records.

## Repository Hygiene

- Keep root documents readable and stable.
- Put future source code in clearly named directories instead of mixing implementation files into the documentation root.
- Add tests with implementation changes once code exists.
- Do not introduce generated artifacts, local secrets, dependency folders, build outputs, or editor state into git.
- Use concise commits with clear scopes.
