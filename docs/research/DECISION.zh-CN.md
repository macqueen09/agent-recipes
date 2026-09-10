# 方向选择：先做 Agent Recipes

检索日期：2026-09-10。结论是产品选择，不是关于全体 agent 行为的统计结论。

## 官方资料能支持什么

| 来源 | 观察 | 不能据此推出什么 |
| --- | --- | --- |
| [Claude Code common workflows](https://code.claude.com/docs/en/common-workflows) | 调试示例围绕提供错误、定位代码、应用修复与复现信息展开 | 不能量化实际用户中多少任务使用了网页检索 |
| [Codex web search](https://learn.chatgpt.com/docs/web-search) | 工具具有网页检索能力，文档说明了默认搜索模式和配置方式 | 工具可用或默认启用，不等于每次遇到报错都先搜索 |

当前检索没有找到可据此判断“主流先搜索报错”或“主流不搜索报错”的跨产品代表性数据。因此不把上一轮对报错搜索的推测继续当作增长前提。

## 本轮决策

先选择 B：Agent Recipes。配方围绕明确任务提供可运行实现，并允许用户主动选用、复制和交给 agent 使用。A 的报错案例以后可作为 troubleshooting 类配方加入，不影响目录结构。

首个内容主题是“信息整理与上下文准备”。三个任务能够共享使用场景，又可以分别运行。HTML 转换与代码上下文利用已有开源实现，长文切分提供简单、可核对的原创实现。

这个选择降低了对某一种报错检索行为的依赖，但不证明 B 的流量或 Star 转化一定高于 A。自然检索、推荐率与收藏转化都需要发布后的实际使用来验证。

## Star 宣传口径

[GitHub 的 Star 说明](https://docs.github.com/en/get-started/exploring-projects-on-github/saving-repositories-with-stars)支持“收藏、方便回访、表达支持”的口径。[通知设置说明](https://docs.github.com/en/subscriptions-and-notifications/get-started/configuring-notifications)把更新订阅放在 Watch 设置中，并允许只选 Releases。

因此采用公开文案：配方库持续扩充，欢迎 Star 收藏；如需新版本通知，设置 Watch → Custom → Releases。不能将 Star 描述为自动订阅新资料通知，也不把多次展示文案对转化率的作用写成已经验证的事实。

