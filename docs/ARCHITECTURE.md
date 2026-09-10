# Repository architecture

Keep the unit of growth small: one folder is one task, with an explicit input, output, and executable entrypoint.

```text
agent-recipes/
├── README.md / README.zh-CN.md        Public entry points
├── REVIEW.zh-CN.md                   Prototype review brief
├── catalog.json                     Generated agent-readable index
├── recipes/
│   ├── documents/
│   │   ├── html-to-markdown/
│   │   └── markdown-to-chunks/
│   └── development/
│       └── repo-to-context/
├── templates/recipe/                 Extension starting point
├── scripts/                         Catalog, runner, source fetch, verification
├── tests/                           Behavior and CLI checks
├── docs/
│   ├── CATALOG.md                   Generated browsing index
│   ├── QUICKSTART.md
│   ├── ROADMAP.md
│   ├── GROWTH.zh-CN.md
│   ├── VERIFICATION.md
│   └── research/                    Source-backed selection notes
├── third_party/                     License snapshots and source hashes
└── .github/workflows/verify.yml      Proposed publication-time CI
```

## Recipe contract

Each `recipes/<category>/<id>/` owns:

- `recipe.json`: identity, task, tags, input/output, entrypoint, requirements, origin.
- `main.py`: direct command-line entrypoint; usable when the folder is copied out.
- `requirements.txt`: pinned third-party dependencies or a standard-library-only comment.
- `README.md` and `README.zh-CN.md`: when to use it, commands, outputs, limits, credits.
- `fixtures/`: small original or properly licensed example inputs.
- `examples/`: inspectable outputs produced by the documented command.
- `vendor/`: only when a small upstream source module must be bundled, with its license.

Manifests are the source of truth. `scripts/build_catalog.py` validates required fields and paths, then generates `catalog.json` and `docs/CATALOG.md`. New recipes do not require editing the runner. Templates stay outside `recipes/` so unfinished work never appears in the runnable catalog.

`requires_network` describes execution, not first-time package installation. `requires_credentials` describes the recipe itself; neither implies that a caller should grant additional permissions. `origin` distinguishes copied source, installed dependencies, and original work.

## Keep expansion incremental

Start with ordinary Python scripts and files. Add a new category only when its first working recipe exists. Add shared utilities only after several recipes actually need them; preserve standalone copyability. A future web catalog, skill, or MCP adapter can consume the same index, but those interfaces are not implemented in this prototype.

Recipe code produces the requested task outputs. Marketing remains in documentation and is never appended to user-generated files or machine-readable data.

