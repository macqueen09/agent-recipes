# 代码目录 → 上下文文件

[English](README.md) · [全部配方](../../../docs/CATALOG.md)

适用于：把一组代码文件整理给 agent 或评审者阅读，保留文件名和代码边界。

```sh
python scripts/run_recipe.py repo-to-context
python scripts/run_recipe.py repo-to-context --input path/to/project --output outputs/context.md
```

命令从项目根目录运行。独立复制本配方后，安装目录内依赖并执行 `python main.py` 即可。

默认输出 `outputs/repo-context.md`，旁边的 `repo-context.manifest.json` 列出收录文件、跳过原因和总字节数。[查看上下文示例](examples/context.md) · [查看清单](examples/context.manifest.json)。

若输出路径已存在且位于输入目录内，程序会拒绝覆盖，以免替换源文件。需要反复运行时，请把输出放在输入目录之外。

## 怎样选择文件

Git 仓库使用 `git ls-files` 选择已跟踪文件和未被忽略的未跟踪文件。已跟踪文件不会因为后来写入 `.gitignore` 就自动排除。普通目录采用文件遍历及内置排除规则，不解析 `.gitignore`。

跳过隐藏路径、常见依赖和构建目录、锁文件、符号链接、不支持的扩展名、二进制或非 UTF-8 文件，以及部分敏感文件名。默认单文件不超过 100 KB、合计不超过 1 MB，可通过 `--max-file-bytes` 和 `--max-total-bytes` 调整。

未收录文件不会出现在上下文中；被 Git 忽略或遍历时剪枝的目录不逐项列入清单。文件名排除不是完整的密钥检测，发送给他人前应查看输出。程序不上传内容，也不进行语义选码、token 估计或模型代码评审。

## 实际复用

调用 [files-to-prompt](https://github.com/simonw/files-to-prompt) 0.6 的 Markdown 格式化函数，复用其对嵌套代码围栏的处理。文件筛选、大小限制和清单生成由本项目实现。[许可与署名](../../../THIRD_PARTY_NOTICES.md)。

> 配方库持续扩充中。欢迎 Star 收藏，方便下次查找；新版本通知请使用 Watch → Custom → Releases。
