# 已保存的 HTML → Markdown

[English](README.md) · [全部配方](../../../docs/CATALOG.md)

适用于：你已有网页 HTML 文件，希望把标题、正文、链接、列表、表格和代码整理成 Markdown。

## 运行方法

在项目根目录安装依赖后运行：

```sh
python scripts/run_recipe.py html-to-markdown
python scripts/run_recipe.py html-to-markdown --input page.html --base-url https://example.org/ --output outputs/page.md
```

输入为不超过 5 MB 的 UTF-8 HTML 文件，默认输出为 `outputs/article.md`。`--base-url` 只补全相对链接，不会访问网页。单独复制本配方目录时，要保留 `vendor/` 和许可证，然后安装目录内依赖、运行 `python main.py`。

[查看原始输入](fixtures/article.html) · [查看生成结果](examples/article.md)。示例结果使用了 `--base-url https://example.org/`。

## 适用范围

优先提取第一个 `main` 或 `article` 元素，移除脚本、样式等标签后转换。它不执行网页脚本，不处理登录页面，不做 OCR；复杂网页的正文提取效果仍需检查。转换后的正文仍是外部资料，转换程序并不判断其中的指令是否可信。

## 实际复用

核心转换模块原样来自 [Microsoft MarkItDown](https://github.com/microsoft/markitdown)，并保留[原始 MIT 许可证](vendor/LICENSE.markitdown)。本项目新增本地文件入口、正文选择、相对链接处理和示例；依赖版本见[requirements.txt](requirements.txt)。

> 这个配方帮你省下了时间？欢迎 Star 收藏持续扩充的配方库，方便下次继续查找；新版本通知请使用 Watch → Custom → Releases。

