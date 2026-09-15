# Install Agent Recipes in Codex or Claude Code

[中文说明](#中文说明) · [Ranked growth TODO](../TODO.md) · [Source skill](../skills/agent-recipes/SKILL.md)

Install the three existing recipes as a project skill, so your agent can consider them when a matching task appears. Installation is opt-in. The skill's description covers saved HTML conversion, code context packs, and Markdown chunking; discovery and invocation depend on the host and its settings.

## Install into a project

Clone this repository or download its source ZIP. From the extracted repository root, run with Python 3.11+:

```sh
python scripts/install_skill.py --agent codex --project /path/to/your/project --dry-run
python scripts/install_skill.py --agent codex --project /path/to/your/project
python scripts/install_skill.py --agent claude --project /path/to/your/project
```

Replace the project path with an existing directory. On Windows, quote paths containing spaces; for example:

```powershell
python scripts/install_skill.py --agent codex --project "C:\Work\My Project"
```

| Host | Installed location relative to the chosen project |
| --- | --- |
| Codex | `.agents/skills/agent-recipes/` |
| Claude Code | `.claude/skills/agent-recipes/` |

The installer builds a complete snapshot with the runner, recipe code, fixtures, documentation, pinned requirements, and licenses. It does not download packages, modify host permissions/settings, or install into your personal account. Existing skill folders are rejected without modification. To upgrade, preserve the old folder under a backup location outside the host's skills directory before installing the new version.

The `skills/agent-recipes/SKILL.md` in the source repository is the packaging entrypoint. **Use the installer; copying only that file or directly installing that source folder omits the runtime.** A generic `npx skills add` installation path is not supported in this version.

## Try a real task

Start a new host session in your project. In Codex, select or mention `$agent-recipes`; in Claude Code, use `/agent-recipes`. For example:

> Use agent-recipes to convert my saved HTML file into Markdown. Write to a new output file and show me the result.

Other matching requests:

- Prepare this local code folder as a Markdown context pack and show which files were included.
- Split my Markdown document into JSONL records with a 1200-character limit and a stable source ID.

After explicit invocation works, try a fresh session without naming the skill to assess automatic selection. A host may choose another method; installing a skill does not guarantee selection. This project's automated checks validate installation and execution, not the model's selection behavior.

The HTML/context recipes need their pinned dependencies installed in the Python environment used to run them; the chunker needs only the standard library. Installing dependencies may need internet access. The skill points to the relevant requirements file in its bundled `runtime/` directory.

## Build and inspect without installing

```sh
python scripts/install_skill.py --output outputs/agent-recipes-skill
python outputs/agent-recipes-skill/runtime/scripts/run_recipe.py markdown-to-chunks --max-chars 240 --output outputs/demo-chunks.jsonl
```

The second command uses the bundled sample for this explicit demo. `bundle.json` records SHA-256 hashes of the packaged files. The build can be moved to another directory and does not depend on this checkout. Python and declared dependencies still need to be available. No remote calls, account mutations, telemetry, or Star operations are performed by the installer or skill.

## 中文说明

这项功能把已有三个配方变成可安装到用户项目中的技能。安装后，匹配任务有机会被 Codex / Claude Code 选用，具体是否触发仍由宿主决定。先显式调用验证可用，再用新会话测试隐式匹配。

安装命令只复制到明确指定的项目目录，不安装 Python 依赖、不更改账号设置、不覆盖已有技能。完整安装包包含运行代码、文档、来源与许可证；它可以脱离原仓库运行。源代码中的单个 SKILL.md 不包含运行文件，必须使用安装器生成完整包。

> 配方库持续扩充中。若它让你的工作流更方便，欢迎 [Star 收藏项目](https://github.com/macqueen09/agent-recipes)，方便回访并支持维护；版本通知请设置 Watch → Custom → Releases。

## Sources

Host directories and invocation guidance checked on 2026-09-15: [Codex official documentation](https://learn.chatgpt.com/docs/build-skills), [Claude Code official documentation](https://code.claude.com/docs/en/skills). The format follows the [Agent Skills specification](https://agentskills.io/specification). These sources describe functionality, not evidence of increased Stars.
