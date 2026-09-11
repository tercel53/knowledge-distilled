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

Each article is distilled into eight parts:

1. One-sentence takeaway
2. What problem is the article solving?
3. Core ideas
4. Mental model / architecture
5. My understanding
6. What this changes for me
7. Connections to existing knowledge
8. Original source

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
