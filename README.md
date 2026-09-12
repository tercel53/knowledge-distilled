# Knowledge Distilled

A personal knowledge base for turning long-form technical articles into concise, visual, and reusable understanding.

## Local preview

This is a static website; no build step or package installation is required.

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Open http://127.0.0.1:8000/ to browse the knowledge base.

## Why this repository exists

This repository is not an article archive.

Its purpose is to transform external knowledge into personal understanding:

**Source → Read → Understand → Distill → Connect → Review**

Typical sources include:

- OpenAI
- Anthropic
- Google DeepMind
- Meta AI
- engineering blogs
- research papers
- high-quality individual blogs

## Knowledge page structure

Use a progressively deeper reading path, adapting it to the article:

1. One-sentence takeaway
2. Visual explanation of the core relationships, with brief supporting evidence
3. Practices or findings organized around the same ideas
4. Conditions, trade-offs, and limits

Keep original chapter summaries available on demand and link to the source. Avoid repeating the same content as a separate theme mapping or including repository-maintenance advice in the reader-facing note.

## Article distillation skill

The repository skill lives at [.agents/skills/article-distillation/SKILL.md](.agents/skills/article-distillation/SKILL.md).

Example invocation:

> 使用 $article-distillation 蒸馏这篇文章：<文章 URL>。生成可编辑图解优先的 HTML 笔记，并同步 Markdown 和元数据。

For planning only, add “先规划，暂不实现”. The skill follows the requested scope and does not automatically commit, push, or publish.

## Skill evaluation

The independent [article distillation evaluation tool](evals/article-distillation/README.md) compares frozen skill versions using fixed cases and isolated, anonymous reviews. It keeps test cases and scoring rules outside the production skill. See its guide for subAgent dispatch, process-worker integration, resumable runs, and reports.

Run the evaluation tool's own tests without calling a model:

```bash
python3 -m unittest discover -s evals/article-distillation/tests -v
```

## Repository structure

```text
knowledge-distilled/
├── README.md
├── index.html
├── assets/
│   └── css/
│       └── style.css
├── templates/
│   └── article.html
└── ai/
    └── agents/
        └── openai/
            └── harness-engineering/
                ├── README.md
                ├── index.html
                └── metadata.json
```

## Principles

### 1. Do not copy the original article

Store the source URL and your own interpretation. Avoid reproducing large portions of copyrighted text.

### 2. Focus on understanding, not summarization

A summary tells you what the author said.

A knowledge note should also answer:

- Why does this matter?
- What changed in my mental model?
- What does this connect to?
- What could I apply?

### 3. Optimize for fast review

A page should let you recover the core idea in 2–5 minutes.

### 4. Prefer stable concepts over transient details

Capture durable ideas, patterns, trade-offs, and mental models.

## Suggested commit format

```bash
git add .
git commit -m "knowledge: add OpenAI harness engineering"
git push
```

## Future evolution

- V1 — Static HTML + Markdown + GitHub Pages
- V2 — URL → LLM → structured draft
- V3 — Search, tagging, knowledge graph
- V4 — Personal knowledge agent
