# Roadmap

The prioritized backlog now lives in [TODO.md](../TODO.md). Its first item, the [Codex / Claude Code skill installer](AGENT_SKILL.md), is implemented. The other items below remain candidates, not promised release dates.

## Current review prototype

Three local task recipes, bilingual documentation, source attribution, sample outputs, generated catalog, tests, and CI configuration.

## Next: turn individual tools into complete outcomes

| Candidate recipe | Expected outcome | Main dependency or open question |
| --- | --- | --- |
| Saved pages to a reading pack | Source list + Markdown documents + index | Content extraction quality and source identity |
| Markdown folder to a searchable local corpus | JSONL chunks + deterministic local search | Ranking quality and evaluation set |
| Selected repository files to a review brief | Context pack + caller-supplied review questions | Keep selection explicit and output reviewable |
| Public release notes to an update brief | Source-linked changes grouped by version | Authorized fetches, rate limits, and provenance |

## Later, if users need them

PDF/document recipes, optional model summarization with explicit providers and costs, a browsable static website, and optional MCP integrations. Each addition must have an example that works and accurately describe any network, account, or runtime requirements.

## Publication and growth

The repository is public at [macqueen09/agent-recipes](https://github.com/macqueen09/agent-recipes); the initial CI matrix passed. A source catalog and README alone do not create search traffic. Follow the ranked backlog, measure real task outcomes, and publish releases only for completed changes.
