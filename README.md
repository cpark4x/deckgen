# deckgen

Generate beautiful, self-contained HTML presentations from context. Never use PowerPoint or Keynote again.

## Features

✨ **AI-Driven Design** - Automatically selects theme and layouts based on content  
🎨 **Multiple Professional Themes** - Keynote Minimalist, Technical Blueprint, and more  
📦 **Self-Contained** - Single HTML file, zero dependencies, works offline forever  
⌨️ **Interactive Navigation** - Arrow keys, click, swipe, or dot navigation  
🚀 **Dead Simple** - Just describe what you want and get a presentation-ready deck  

## Installation

```bash
# Install with pip
pip install git+https://github.com/cpark4x/deckgen

# Or with uv (faster)
uv pip install git+https://github.com/cpark4x/deckgen
```

## Quick Start

```bash
# Create a deck from a simple description
deckgen create "about shadow environments feature"

# Add context from files
deckgen create "API redesign walkthrough" --file api-spec.md

# Force a specific theme
deckgen create "technical deep dive" --theme technical-blueprint

# Custom output location
deckgen create "Q4 results" --output ~/presentations/q4-results.html
```

## Usage

### Basic Command

```bash
deckgen create "DESCRIPTION" [OPTIONS]
```

### Options

| Option | Short | Description |
|--------|-------|-------------|
| `--file` | `-f` | Add file(s) for additional context (can use multiple times) |
| `--theme` | `-t` | Force specific theme |
| `--output` | `-o` | Custom output filename |
| `--no-open` | | Don't open browser automatically |

### Examples

**Simple presentation:**
```bash
deckgen create "introducing our new caching system"
```

**With context files:**
```bash
deckgen create "architecture review" \
  --file architecture.md \
  --file diagrams.md
```

**Force technical theme:**
```bash
deckgen create "API documentation" --theme technical-blueprint
```

**Multiple files:**
```bash
deckgen create "quarterly roadmap" \
  -f q1.md \
  -f q2.md \
  -f q3.md \
  -f q4.md
```

## Available Themes

### Keynote Minimalist

Professional, executive-focused design inspired by Apple Keynote.

- **Best for:** Product launches, vision statements, executive presentations
- **Style:** Pure black background, SF Pro typography, single accent color
- **Colors:** Black (#000), Blue accent (#0A84FF)

```bash
deckgen create "our vision for 2026" --theme keynote-minimalist
```

### Technical Blueprint

Developer-focused design with terminal aesthetics.

- **Best for:** Technical deep-dives, code reviews, architecture docs
- **Style:** Dark blue-gray background, monospace code, terminal colors
- **Colors:** Dark blue-gray (#1a1f2e), Cyan/Green accents

```bash
deckgen create "microservices architecture" --theme technical-blueprint
```

### List all themes

```bash
deckgen list-themes
```

### Theme details

```bash
deckgen theme-info keynote-minimalist
```

## How It Works

1. **Content Analysis** - Analyzes your description to understand content type, audience, and technical depth
2. **Theme Selection** - AI picks the appropriate design theme (or you can force one)
3. **Layout Design** - Selects optimal slide layouts based on content
4. **Rendering** - Generates beautiful, self-contained HTML

## Output

Every generated deck is:

- ✅ **Self-contained** - Single HTML file with inline CSS/JS
- ✅ **Interactive** - Full keyboard/mouse/touch navigation
- ✅ **Portable** - Works everywhere, no dependencies
- ✅ **Offline-ready** - Works without internet forever
- ✅ **Shareable** - Email it, Slack it, upload anywhere

### Navigation

- **Arrow keys** - Next/previous slide
- **Space/Page Down** - Next slide
- **Page Up** - Previous slide
- **Home** - First slide
- **End** - Last slide
- **Click anywhere** - Next slide
- **Swipe** - On touch devices
- **Dots** - Click navigation dots at bottom

## Real-World Examples

### Feature Launch

```bash
deckgen create "launching shadow environments - isolated testing for Amplifier"
```

**Result:** 6-slide deck with Keynote Minimalist theme, covering problem → solution → demo → impact

### Technical Deep-Dive

```bash
deckgen create "deep dive into our event-driven architecture" \
  --file architecture.md \
  --theme technical-blueprint
```

**Result:** Technical Blueprint theme with code examples, architecture diagrams, and implementation details

### Quick Update

```bash
deckgen create "weekly sprint review - shipped auth, caching, monitoring"
```

**Result:** Clean 3-slide deck with feature grid and stats

## Design Philosophy

### Ruthless Simplicity

- One idea per slide
- Minimal text - every word earns its place
- White space is intentional
- Visual hierarchy over decoration

### Content-Aware

- Technical content gets Technical Blueprint theme
- Business/executive content gets Keynote Minimalist
- AI analyzes content signals to make smart choices

### Self-Contained Forever

- No external dependencies
- No CDNs, no cloud services
- Works offline permanently
- Email-friendly, archive-friendly

## Development

### Install for development

```bash
git clone https://github.com/cpark4x/deckgen
cd deckgen
pip install -e ".[dev]"
```

### Run tests

```bash
pytest tests/
```

### Code quality

```bash
# Format
black deckgen/

# Lint
ruff check deckgen/
```

## What Makes This Different?

### vs PowerPoint/Keynote

| deckgen | PowerPoint/Keynote |
|---------|-------------------|
| `deckgen create "about X"` | Open → template → copy/paste → format → export |
| AI-designed | Manual design |
| Self-contained HTML | Requires software |
| Works everywhere | Platform-specific |
| 15 seconds | 30+ minutes |

### vs Google Slides

| deckgen | Google Slides |
|---------|--------------|
| Offline forever | Requires internet |
| No account needed | Requires Google account |
| Single file | Cloud-dependent |
| Zero dependencies | Browser + account + permissions |

### vs reveal.js / Spectacle

| deckgen | reveal.js |
|---------|-----------|
| Point at context, get deck | Write HTML/Markdown manually |
| AI-designed themes | DIY styling |
| One command | Configure build system |
| Non-technical friendly | Developer tool |

## Roadmap

**Phase 1 (Current):**
- ✅ Two professional themes
- ✅ AI-driven theme selection
- ✅ Six slide layouts
- ✅ CLI interface

**Phase 2 (Coming):**
- [ ] Business Deck theme (white background, charts/graphs)
- [ ] Modern Magazine theme (editorial, asymmetric)
- [ ] Academic Research theme (serif, scholarly)
- [ ] Startup Pitch theme (gradients, energetic)
- [ ] GitHub/URL context parsing
- [ ] Image support
- [ ] Chart generation

## Contributing

Contributions welcome! This project follows:

- Ruthless simplicity (KISS principle)
- Self-contained output (zero dependencies)
- Content-aware intelligence (AI-driven decisions)

## License

MIT

## Credits

Inspired by [ramparte/amplifier-stories](https://github.com/ramparte/amplifier-stories) - the original self-contained HTML presentation tool. `deckgen` evolves the concept with multiple professional design systems and intelligent theme selection.

---

**Questions?** [Open an issue](https://github.com/cpark4x/deckgen/issues)

**Built with ❤️ for people who hate building slides**
