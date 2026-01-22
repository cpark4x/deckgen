# deckgen Documentation

**AI-powered presentation generator that creates polished HTML decks from simple descriptions.**

---

## Quick Links

| Document | Purpose |
|----------|---------|
| [VISION](01-vision/VISION.md) | Problems, positioning, roadmap |
| [Epics](02-requirements/epics/) | Feature sets we're building |

---

## Epic Status

| # | Epic | Status | Description |
|---|------|--------|-------------|
| [01](02-requirements/epics/EPIC-01-core-generation.md) | Core Generation Pipeline | ✅ Complete | Text → slides with AI images |
| [02](02-requirements/epics/EPIC-02-enhanced-content.md) | Enhanced Content | 🔲 Planned | File ingestion, multi-image |

**Status Legend:** 🔲 Planned | 🔄 In Progress | ✅ Complete

---

## Current Capabilities (V1)

- ✅ Natural language → slide deck
- ✅ Automatic theme selection
- ✅ AI image generation (Gemini nano-banana)
- ✅ Minimum 5 slides per deck
- ✅ Self-contained HTML output
- ✅ Keyboard navigation

---

## Quick Start

```bash
# Generate a deck
cd /Users/chrispark/Projects/deckgen
python -m deckgen "Your presentation topic here"

# With theme override
python -m deckgen "Topic" --theme technical-blueprint

# Without images (faster)
python -m deckgen "Topic" --no-images
```

---

## Documentation Structure

```
docs/
├── README.md              # This file
├── 01-vision/
│   └── VISION.md          # Strategic direction
├── 02-requirements/
│   └── epics/             # Feature specifications
│       ├── EPIC-01-*.md   # Core generation (done)
│       └── EPIC-02-*.md   # Enhanced content (planned)
└── templates/             # Document templates
```

---

## Contributing

- **Vision changes**: Rare, require broad alignment
- **New epics**: Discuss in planning before creating
- **Updates**: Keep status table current as work progresses
