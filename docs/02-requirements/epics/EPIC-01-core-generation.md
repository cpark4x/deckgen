# EPIC-01: Core Generation Pipeline

**Status:** ✅ Complete
**Priority:** P0 - Critical
**Target:** V1
**Owner:** Chris Park

---

## Summary

Build the foundational deck generation pipeline that transforms natural language descriptions into polished HTML presentations with AI-generated images.

---

## Problem Statement

Users need a way to quickly create professional presentations without design skills or significant time investment. The core pipeline must handle content analysis, theme selection, image generation, and HTML rendering in a single seamless flow.

---

## Success Criteria

| Criteria | Target | Status |
|----------|--------|--------|
| Generate deck from description | < 30 seconds | ✅ ~15s |
| Minimum slides per deck | 5+ | ✅ 6 slides |
| AI image generation | Title slide | ✅ Working |
| Theme auto-selection | Based on content | ✅ Working |
| Self-contained output | Single HTML file | ✅ Working |

---

## User Stories

### US-01: Basic Generation ✅
**As a** user
**I want to** provide a topic description and get a presentation
**So that** I can create decks without manual design work

**Acceptance Criteria:**
- [x] CLI accepts description string
- [x] Generates structured slides from description
- [x] Outputs valid HTML file
- [x] Keyboard navigation works

### US-02: Theme Selection ✅
**As a** user
**I want** the system to choose an appropriate theme
**So that** my presentation looks professional without manual styling

**Acceptance Criteria:**
- [x] Multiple themes available
- [x] Auto-selection based on content type
- [x] Manual theme override option
- [x] Consistent styling across slides

### US-03: AI Image Generation ✅
**As a** user
**I want** AI-generated images in my presentation
**So that** slides are visually engaging without sourcing images manually

**Acceptance Criteria:**
- [x] Gemini API integration (nano-banana model)
- [x] Title slide gets background image
- [x] Images relevant to content
- [x] Dark overlay for text readability
- [x] Graceful fallback if API unavailable

### US-04: Slide Expansion ✅
**As a** user
**I want** presentations to have sufficient content
**So that** I get a complete deck, not just 2-3 slides

**Acceptance Criteria:**
- [x] Minimum 5 slides per deck
- [x] Expansion templates for thin content
- [x] Logical slide progression
- [x] Closing slide included

---

## Technical Implementation

### Components Built

| Component | File | Purpose |
|-----------|------|---------|
| Orchestrator | `core/orchestrator.py` | Pipeline coordination |
| Analyzer | `core/analyzer.py` | Content parsing & structure |
| Designer | `core/designer.py` | Theme selection & slide design |
| Renderer | `core/renderer.py` | HTML generation |
| ImageGenerator | `core/image_generator.py` | Gemini API integration |

### Architecture

```
User Input (description)
       ↓
   Analyzer
   - Parse content
   - Extract structure
   - Generate slide specs
       ↓
   Designer
   - Select theme
   - Map to layouts
       ↓
 ImageGenerator
   - Create prompts
   - Call Gemini API
   - Embed base64 images
       ↓
   Renderer
   - Apply theme CSS
   - Render HTML
   - Add navigation JS
       ↓
   Output (HTML file)
```

### Dependencies

- Python 3.10+
- PyYAML (theme configs)
- Gemini API key (for images)

---

## Change History

| Date | Change | Author |
|------|--------|--------|
| 2026-01-21 | Epic completed - all stories done | Chris Park |
| 2026-01-21 | Added AI image generation | Chris Park |
| 2026-01-21 | Initial epic creation | Chris Park |
