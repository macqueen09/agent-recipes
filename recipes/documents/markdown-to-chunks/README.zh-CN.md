# Markdown → 可追溯的 JSONL 片段

[English](README.md) · [全部配方](../../../docs/CATALOG.md)

适用于：为后续检索、分批阅读或建立索引准备长文片段，并保留每段的来源和原文位置。

```sh
python scripts/run_recipe.py markdown-to-chunks --max-chars 240
python scripts/run_recipe.py markdown-to-chunks --input notes.md --source notes-v1 --max-chars 1200 --output outputs/chunks.jsonl
```

输入为不超过 10 MB 的 UTF-8 Markdown 文件，默认输出 `outputs/chunks.jsonl`。不需要第三方库，独立复制目录后也可直接运行 `python main.py`。

每条记录包含片段 ID、顺序、来源、起止字符位置和文本。位置从 0 开始，结束位置不包含在片段内。依次拼接文本能够还原解码后的原文，包括 CRLF 和空白；UTF-8 BOM 在解码时去除。可以用 `--source` 指定稳定来源名，默认使用输入文件名。

[查看输入](fixtures/notes.md) · [查看按 240 字符切分的结果](examples/chunks.jsonl)。

## 限制

按字符数量切分，不等于 token 数量。在窗口后半段优先找段落、换行或空格边界，必要时会切断长句或代码块。当前不保证每段语义完整，不生成重叠片段、向量或模型摘要。空输入得到空输出，字符上限不能小于 32。

本配方代码和示例为本项目原创，采用 MIT 许可。

> 配方库持续扩充中。欢迎 Star 收藏，方便下次查找；新版本通知请使用 Watch → Custom → Releases。

