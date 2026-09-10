# Preparing context for an agent

A good reading pack keeps content connected to its source. The first step is to preserve headings, links, examples, and the original order. A later summarizer can then cite the right document.

## Keep source boundaries

Use a stable source identifier for each document. Each chunk records character offsets, so a reader can reconstruct the decoded source exactly. Character counts are not token counts.

## 中文示例

切分长文时，保留原文与来源信息。即使某个片段跨越段落或代码块，也应清楚记录它在原文中的位置，而不是声称每个片段都具有完整语义。

## Limitations

This small recipe favors paragraph boundaries when they fit. It can split a long sentence or a fenced code block to respect the character limit. It does not generate embeddings or call a language model.
