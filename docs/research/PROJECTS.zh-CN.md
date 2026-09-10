# GitHub 同类项目与复用决定

检索日期：2026-09-10。查看了仓库页面、GitHub API 元数据及选中源码。以下不是穷尽式竞品调查，也未用 Star 数估算增长潜力。

| 项目 | 可参考之处 | 本轮处理 |
| --- | --- | --- |
| [OpenClaw Cookbook](https://github.com/openclaw/cookbook) | 小型可运行配方、独立应用、配方清单 | 参考每个任务单独目录与清单的组织方式；不引入其 SDK 或复制文案 |
| [Microsoft AgenticCookBook](https://github.com/microsoft/AgenticCookBook) | 按能力与应用示例组织 agent 教程 | 用作比较；当前雏形选择能够直接产生文件结果的小配方 |
| [Microsoft MarkItDown](https://github.com/microsoft/markitdown) | 文档转换为便于阅读的 Markdown | 实际复制一个 MIT 转换模块并原样保存，用于 HTML 配方 |
| [simonw/files-to-prompt](https://github.com/simonw/files-to-prompt) | 将目录文件整理为供模型阅读的文本 | 安装并调用 0.6 版本的 Markdown 格式化函数；文件筛选和清单逻辑由本项目实现 |

## 固定源码状态

| 仓库 | 本轮查询的默认分支提交 | 许可 |
| --- | --- | --- |
| microsoft/markitdown | `6270920c28000d217774ea29fa7a9262d7d5c65b` | MIT |
| simonw/files-to-prompt | `1b234ff6dccb2ca3e56b5c256696558fb85306dc` | Apache-2.0 |
| openclaw/cookbook | `f2b1b24e76295b5ebce154eec344e53dbe8dcadd` | MIT |
| microsoft/AgenticCookBook | `32c6b754cff666962b6cd4679a2bdd9183fbe28e` | MIT |

MarkItDown 的复制文件来自上表固定提交。files-to-prompt 的运行依赖固定为 PyPI 0.6；上表提交用于仓库考察和许可证快照，不能视为该 wheel 与此提交逐字一致的证明。

## 新增价值在哪里

本项目新增统一的任务说明、输入输出约定、中文入口、可查看结果、固定依赖、来源记录、目录索引及自动验证。当前仍然是轻量整合，技术独特性有限；下一阶段需要依据真实任务增加更完整的多步配方和更好的示例。

完整复用范围见[第三方说明](../../THIRD_PARTY_NOTICES.md)，下载文件的原始地址与校验值见[来源锁定文件](../../third_party/sources.lock.json)。

