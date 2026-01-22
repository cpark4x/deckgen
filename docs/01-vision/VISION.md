# deckgen: Vision

**AI-powered presentation generator that transforms simple descriptions into polished, professional slide decks in seconds.**

**Owner:** Chris Park
**Last Updated:** 2026-01-21

---

## Summary

deckgen solves the pain of creating presentations from scratch by using AI to analyze content, select appropriate themes, generate supporting images, and render beautiful HTML presentations. It's designed for busy professionals who need quality decks fast without wrestling with PowerPoint or design tools.

---

## 1. The Problems We're Solving

### Problem 1: Presentation Creation is Time-Consuming

**Current Reality:**
- Creating a decent 10-slide presentation takes 2-4 hours
- Most time is spent on formatting, not content
- Finding/creating visuals adds another hour or more

**The Impact:**
- Professionals waste hours on mechanical work
- Quality suffers under time pressure
- Many skip presentations entirely due to effort required

**Why This Matters:**
Presentations remain the primary medium for sharing ideas in business. The friction of creation limits how often good ideas get communicated.

### Problem 2: Design Tools Have a Steep Learning Curve

**Current Reality:**
- PowerPoint/Keynote require design skills most people lack
- Templates help but still need customization
- Consistency across slides is hard to maintain

**The Impact:**
- Ugly presentations undermine good content
- People stick to boring bullet points
- Visual communication potential is wasted

**Why This Matters:**
The gap between "can make slides" and "can make good slides" is huge. Most people are stuck on the wrong side.

### Problem 3: AI Tools Generate Generic Output

**Current Reality:**
- Existing AI slide tools produce cookie-cutter results
- No visual differentiation or polish
- Output looks obviously AI-generated

**The Impact:**
- Professionals avoid AI tools for important presentations
- Results require significant manual cleanup
- The promise of AI assistance goes unfulfilled

**Why This Matters:**
AI should elevate output quality, not just speed up mediocrity.

---

## 2. Strategic Positioning

### The Core Insight

**Beautiful presentations should be as easy as describing what you want.**

We believe the future of presentation creation is conversational: describe your topic, and AI handles structure, design, and visuals. The human focuses on the message; the machine handles the medium.

### What We're NOT Building

- ❌ A PowerPoint clone with AI features bolted on
- ❌ A template marketplace
- ❌ A collaborative editing tool
- ❌ A presentation hosting platform

### What We ARE Building

- ✅ A single-command presentation generator
- ✅ AI-native from the ground up
- ✅ Opinionated design that looks great by default
- ✅ Self-contained HTML output (no dependencies)

---

## 3. Who This Is For

### Primary: Busy Professionals

Engineers, product managers, executives, and consultants who need to communicate ideas visually but don't have time for design work. They value speed and quality over customization options.

**Characteristics:**
- Create 2-10 presentations per month
- Time-constrained, deadline-driven
- Care about looking professional
- Comfortable with CLI/developer tools

### Secondary: Developers & Technical Users

People who prefer text-based workflows over GUI tools. They appreciate the programmatic approach and self-contained output.

### Not For (Yet)

- Designers who want pixel-perfect control
- Marketing teams needing brand-compliant templates
- Users who need real-time collaboration

---

## 4. The Sequence

### V1: Foundation (Current)

**Focus:** Core generation pipeline that actually works

**Core capabilities:**
- Natural language description → slide deck
- Content analysis and structure extraction
- Theme selection and application
- AI image generation (Gemini nano-banana)
- Self-contained HTML output
- Keyboard navigation and responsive design

**Success Criteria:**
- Generate a 5+ slide deck in under 30 seconds
- Output looks professional without manual editing
- Works from simple text descriptions

### V2: Intelligence

**Focus:** Smarter content and better visuals

**Planned capabilities:**
- File/document ingestion (PDF, MD, DOCX)
- Multi-image generation (not just title slide)
- Speaker notes generation
- Multiple theme options
- Export to PDF

**Success Criteria:**
- Ingest a document and produce relevant deck
- Images on 50%+ of slides
- Quality matches professional templates

### V3: Integration

**Focus:** Fit into existing workflows

**Planned capabilities:**
- Amplifier tool integration
- Watch mode for iterative refinement
- Template customization
- Brand color/font injection
- PowerPoint/Keynote export

**Success Criteria:**
- Seamless use within Amplifier sessions
- Output usable in enterprise contexts

---

## 5. Success Metrics

| Metric | V1 Target | V2 Target |
|--------|-----------|-----------|
| Generation time | < 30s | < 45s (with more images) |
| Slides per deck | 5-10 | 8-15 |
| User satisfaction | "Good enough to use" | "Better than I'd make myself" |
| Image quality | Relevant backgrounds | Contextual illustrations |

---

## Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v1.0 | 2026-01-21 | Chris Park | Initial vision document |
