# Agent Recipes

**把常见任务变成可直接运行、可查看结果的小配方。**

[English](README.md) · [配方目录](docs/CATALOG.md) · [机器可读索引](catalog.json) · [参与贡献](CONTRIBUTING.md)

把网页保存成 Markdown；把代码目录整理成上下文；把长文切分成带来源与位置的片段。

每个配方都包含代码、示例输入、结果文件、固定依赖和来源说明。你可以直接运行，也可以让 coding agent 在完成任务时使用。

> 配方库持续扩充中。**欢迎 Star 收藏，方便下次找到好用的配方，也支持项目继续完善。** 希望收到新版本通知，可设置 **Watch → Custom → Releases**。Star 本身不订阅更新通知。

## 先运行一个例子

需要 Python 3.11+。安装依赖时需要网络；当前三个配方运行时均不调用外部服务，不需要 API Key。代码目录配方建议安装 Git。

在项目根目录、所选 Python 环境中运行：

```sh
python -m pip install -r requirements.txt
python scripts/run_recipe.py html-to-markdown
python scripts/run_recipe.py repo-to-context
python scripts/run_recipe.py markdown-to-chunks --max-chars 240
```

结果写入 `outputs/`。Windows 与 macOS/Linux 的虚拟环境步骤见[快速开始](docs/QUICKSTART.md)。

| 你要完成的任务 | 配方说明 | 可以直接查看的结果 |
| --- | --- | --- |
| 把已保存网页转成易读的 Markdown | [HTML 转换](recipes/documents/html-to-markdown/README.zh-CN.md) | [示例 Markdown](recipes/documents/html-to-markdown/examples/article.md) |
| 把代码文件整理成供 agent 阅读的上下文 | [代码上下文](recipes/development/repo-to-context/README.zh-CN.md) | [示例上下文](recipes/development/repo-to-context/examples/context.md) |
| 把长文切成保留来源与位置的片段 | [长文切分](recipes/documents/markdown-to-chunks/README.zh-CN.md) | [示例 JSONL](recipes/documents/markdown-to-chunks/examples/chunks.jsonl) |

## 怎样让 agent 使用

把仓库提供给 agent，直接描述目标，例如：

> 用这个仓库的 html-to-markdown 配方转换我保存的网页，保留原文件，并给我查看输出结果和限制。

也可以先在本地按任务搜索：

```sh
python scripts/run_recipe.py --search markdown
```

[catalog.json](catalog.json) 提供配方输入、输出、标签、运行入口和所需条件。当前配方是供 agent 调用的确定性任务工具，尚未包含自主 agent 框架、托管检索服务或模型总结功能。

## 后续怎样扩充

每个配方放在 `recipes/<分类>/<配方名>/`，拥有独立代码、文档、依赖和样例。新增目录后生成索引，再通过验证即可加入。

[目录设计](docs/ARCHITECTURE.md) · [扩展计划](docs/ROADMAP.md) · [更新记录](CHANGELOG.md) · [验证记录](docs/VERIFICATION.md)

## 来源和许可

HTML 转换实际复用了 [Microsoft MarkItDown](https://github.com/microsoft/markitdown) 的 MIT 模块；上下文输出调用 [files-to-prompt](https://github.com/simonw/files-to-prompt) 的 Apache-2.0 实现。配方组织参考了 [OpenClaw Cookbook](https://github.com/openclaw/cookbook)。

本项目新增部分采用 [MIT](LICENSE)，第三方内容保留原许可与署名。具体见[复用说明](THIRD_PARTY_NOTICES.md)。

当前为 0.1.0 初始版本，配方范围与维护节奏仍在完善。
