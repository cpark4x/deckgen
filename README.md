# deckgen

You spend 2 hours making 10 slides. Most of that time is formatting, not thinking. The content was clear in your head — the tool made it slow.

deckgen takes a description and produces a finished presentation in about 15 seconds. One command, one HTML file, zero dependencies. The file works offline forever — email it, Slack it, open it in 5 years. No accounts, no cloud, no PowerPoint.

```bash
deckgen create "shadow environments feature launch"
```

You get a polished deck with theme-matched layouts, proper typography, keyboard/touch/swipe navigation, and an AI-generated title image. Two themes ship today — Keynote Minimalist (product launches, vision decks) and Technical Blueprint (architecture, code reviews).

## Quick start

```bash
pip install git+https://github.com/cpark4x/deckgen
deckgen create "your topic here"
```

That's it. A browser tab opens with your deck.

Add context from files, force a theme, or change the output location:

```bash
deckgen create "API redesign" --file api-spec.md
deckgen create "deep dive" --theme technical-blueprint
deckgen create "Q4 results" --output ~/presentations/q4.html
```

## How it works

No LLM writes your slides. The pipeline is rule-based:

1. **Analyze** — detects content type, audience, tone, and technical depth from your description
2. **Design** — scores themes against your content signals, maps slides to layouts
3. **Generate image** — optional AI title background via Gemini (skips gracefully without API key)
4. **Render** — produces a single HTML file with all CSS and JS inline

~15 seconds. 9 slide layout types. Everything self-contained.

## Status

V1 complete — core generation pipeline works. V2 planned: file ingestion (PDF, Word), multi-slide images, speaker notes.

## Built by

[Chris Park](https://www.linkedin.com/in/chrispark) — Microsoft Office of the CTO, AI Incubation. Building the tools he actually uses.
