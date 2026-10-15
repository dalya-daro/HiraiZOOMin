# HiraiZOOMin Agent Guide

Start with the detailed project guidance in `docs/`:

- `ai_context.md` — project context, learning level, and fixed decisions
- `tasks.md` — implementation order and completion checks
- `coding_rules.md` — coding, safety, and scope rules
- `requirements.md`, `screens.md`, `routes.md`, and `database.md` — MVP design source of truth
- `learned.md` — concepts the project owner has and has not learned

## Core rules

- Use Python, Flask, PeeWee, and SQLite as agreed. Follow the existing requirements, screen design, routes, and database design.
- Implement in small, beginner-friendly steps. Prefer learned concepts; explain unfamiliar concepts, syntax, packages, or techniques before using them.
- Stay within the agreed MVP. Ask before adding features, dependencies, advanced architecture, or changing documented decisions.
- Use one `Place` model and only these stored category values: `sightseeing`, `food`, and `shopping`.
- Handle nullable optional data, invalid categories, and missing place IDs safely.
- Keep static assets under `static/`; do not implement user uploads.
- Do not invent or claim verification of real-world place information, addresses, opening hours, or Google Maps links. The project owner supplies and verifies the six sample places.
- Do not write secrets or private information into source code.
