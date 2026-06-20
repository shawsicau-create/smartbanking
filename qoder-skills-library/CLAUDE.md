# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A curated library of **175 AI skills** for QoderWork, oriented around economics academic research. Each skill is a `SKILL.md` file that teaches an AI agent how to perform a specific task. The repo is pure content — no build system, no tests, no linting.

## Repository Layout

```
NN-category-name/       # 20 numbered directories (01-ideation through 20-messaging)
  skill-name/           # One subdir per skill, kebab-case
    SKILL.md            # Required — the skill definition (YAML frontmatter + markdown body)
    README.md           # Optional — user-facing docs
    config.yaml         # Optional — skill-specific configuration
    scripts/            # Optional — helper scripts (Python/Shell)
    examples/           # Optional — example data or sub-skills
_archived/              # Deprecated skills (frontmatter `disable: true`)
meta/
  _index.yaml           # Master index of all 175 skills — must stay in sync
SKILL_TEMPLATE.md       # Canonical template for new skills
.mcp.json               # MCP server configs (email, playwright, maps, Stata, etc.)
```

## SKILL.md Frontmatter Schema

Every `SKILL.md` must have YAML frontmatter with these **7 required fields**:

```yaml
---
name: skill-name                    # kebab-case, max 64 chars, must match directory name
description: One-line description   # max ~100 chars, used for AI auto-discovery
workflow_stage: analysis             # ideation | literature | theory | data | analysis | writing | communication | engineering
compatibility:                       # platforms where this skill works
  - claude-code
  - cursor
  - codex
  - gemini-cli
author: Qoder Skills Library
version: 1.0.0                      # semver
tags: [tag1, tag2]                  # lowercase keywords
---
```

Optional fields (used in some skills): `argument-hint`, `allowed-tools`, `description_zh`, `description_en`, `homepage`, `disable`.

## When Adding or Modifying a Skill

1. **New skill**: create `NN-category/skill-name/SKILL.md` using `SKILL_TEMPLATE.md` as the base. Follow the authoring guide in `19-devtools/create-skill/SKILL.md`.
2. **Naming**: directory name = `name` in frontmatter = kebab-case slug.
3. **Category assignment**: match `workflow_stage` to the numbered category's purpose (see README.md tables).
4. **Index sync**: after adding/removing/renaming a skill, update `meta/_index.yaml` to match — it's the canonical machine-readable catalog.
5. **Body structure**: most skills follow Purpose → When to Use → Instructions (Steps) → Example Prompts → Requirements → Best Practices → Common Pitfalls.
6. **User arguments**: reference `$ARGUMENTS` in the body where user input should be interpolated.

## Key Reference Files

- `SKILL_TEMPLATE.md` — blank template with all sections
- `19-devtools/create-skill/SKILL.md` — detailed authoring guide, patterns, and anti-patterns
- `meta/_index.yaml` — full catalog (2600+ lines); single source of truth for skill count and metadata
- `README.md` — human-readable catalog in Chinese with all 20 categories and skill tables

## Conventions

- All skills are bilingual-ready; primary content is in Chinese, with some skills having `description_zh`/`description_en` variants.
- The `11-perspective/nuwa-skill/` directory contains 15 distilled persona examples (Munger, Taleb, Feynman, etc.) under `examples/`.
- Skills in `_archived/` have `disable: true` — they are not indexed and should not be referenced by new skills.
- Skills can chain/reference each other by name (e.g., `/novelty-check`, `/research-review`).
