# LLMWiki · 知识库问答

> 把一堆 Markdown 变成能引用、能拒答的问答助手。

## 为什么做这个

这是学 Python 和 RAG 的载体，也是作品集里的"第二名"：DBACopilot 证明领域深度，LLMWiki 证明我能独立把一个 AI 应用从 0 写到上线。

和市面上大量"文档问答 demo"的区别在于两点，也是我重点要做的部分：

1. **评测**：30 条问题 + 标准答案 + 正确文档，量化命中率和忠实度，而不是"感觉还行"
2. **拒答**：检索不到就说不知道，不许编——企业场景里这比答对更重要

## 验收标准（v0.1，W3 末达到）

- [ ] 导入 100 篇 Markdown，支持增量更新（改一篇只重算那一篇）
- [ ] 30 条评测集：检索命中率 **≥ 80%**，答案忠实度人工评分 **≥ 4/5**
- [ ] 每个回答带 ≤3 条引用，引用能点回原文的具体段落
- [ ] 明确拒答：问题超出知识库范围时回答"知识库里没有相关内容"，并在评测集里有 5 条此类用例
- [ ] 单次问答 P95 延迟 < 8 秒，成本可查（每次调用的 token 与费用）
- [ ] 20 条 pytest 用例全绿

## 架构（v0.1 先用最小实现，不引入重框架）

```
Markdown 文件
   │  loader（解析标题层级、代码块、表格）
   ▼
切分（按标题优先，超长再按段落）
   │
   ▼
Embedding（OpenAI 兼容接口）──▶ pgvector
                                   │
用户提问 ──▶ 检索 top-k ──▶ 拼上下文 ──▶ LLM ──▶ 带引用回答
                                   │
                               无命中 ──▶ 拒答
```

**有意不用 LangChain**：W1 先用原生 SDK 写一遍，理解每一步在干什么；后面再决定要不要用框架。简历上"手写 RAG"比"调 LangChain"值钱。

## 技术栈

- Python 3.11+ · FastAPI · pydantic v2
- PostgreSQL + pgvector
- pytest · ruff
- 依赖管理：uv

## 里程碑

| 周 | 目标 | 完成标志 |
|---|---|---|
| W1 | 环境 + 骨架 + 流式聊天 CLI | `uv run pytest` 全绿；CLI 能多轮流式对话 |
| W2 | 文档导入 + 切分 + embedding | 100 篇 md 入库，能看到 chunk 数量与预览 |
| W3 | 检索 + 回答 + 引用 + 拒答 | 30 条评测跑出命中率 |
| W4 | 评测报告 + 混合检索对比 | 两种检索方案的命中率对比表 |

## 如何运行

```bash
# 1. 装 uv（一次性）
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 2. 同步依赖
uv sync

# 3. 配置
copy .env.example .env    # 填入 LLM API Key

# 4. 起服务
uv run uvicorn llmwiki.main:app --reload

# 5. 测试
uv run pytest -q
```

## 目录

```
src/llmwiki/
├── main.py        # FastAPI 入口
├── config.py      # 配置（环境变量）
├── loader.py      # Markdown 解析（W2）
├── chunker.py     # 切分策略（W2）
├── embedder.py    # Embedding 封装（W2）
├── retriever.py   # 检索 + rerank（W3）
└── answer.py      # 生成 + 引用 + 拒答（W3）
tests/
docs/eval/         # 评测集与报告
```

## 状态

🚧 W1：骨架 + 健康检查，业务代码从 W2 开始写。
