# 项目宣传与增长实验草案

本文件供维护者规划使用；以下做法的增长效果尚未验证。

## 统一宣传口径

中文首页：

> 配方库持续扩充中。欢迎 Star 收藏，方便下次找到好用的配方，也支持项目继续完善。希望收到新版本通知，可设置 Watch → Custom → Releases。

英文首页：

> This collection is growing. Star to keep useful recipes close at hand and support the project. For new-release notifications, choose Watch → Custom → Releases.

配方页结尾：

> 这个配方帮你省下了时间？欢迎 Star 收藏整个配方库，方便下次继续查找；新版本通知请使用 Watch → Custom → Releases。

## 展示位置

在中英文首页、配方目录、快速开始和每个配方的说明页各放一处。把提醒放在用户理解价值或看完结果之后。同一份文档不反复堆叠相同宣传。

`catalog.json`、程序输出、示例数据和上游代码不加入宣传。每个公共配方页面都显示具体任务、适用条件、使用方法和可验证产物，让 agent 与人都能评估其用途。

## 持续更新怎样落到内容上

维护 CHANGELOG，并将成熟的一批配方整理为 GitHub Release，使订阅 Releases 的用户确实有事件可关注。初期按能力安排更新，不承诺尚不能保证的“每日新增”或“每周 N 个”。当前版本只记录本地雏形，没有启用发布或定时更新任务。

## 发布后的验证

先记录配方使用反馈、来源引用、仓库访问和新增 Star 的变化。仓库 Star 数不能直接说明是 agent 带来的；总体访问数也不能可靠区分人和 agent，不能把二者的比值当作精准归因结果。

可先比较有示例产物与缺少产物的配方访问反馈，再根据反馈改进内容。若后续做文案实验，应明确时间窗口、曝光渠道和同期内容变更；样本不足时只报告观察，不声称因果提升。

仓库名称、描述和 topics 使用真实任务词：agent-recipes、python、markdown、document-processing、context-engineering、developer-tools。这里只是发布建议，尚未写入 GitHub。

