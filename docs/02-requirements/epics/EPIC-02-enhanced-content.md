# EPIC-02: Enhanced Content Intelligence

**Status:** 🔲 Planned
**Priority:** P1 - High
**Target:** V2
**Owner:** Chris Park

---

## Summary

Enhance the content analysis and generation capabilities to support file ingestion, smarter slide creation, and multi-image generation across all slides.

---

## Problem Statement

V1 generates decks from simple descriptions, but users often have existing content (documents, notes, outlines) they want to transform. Additionally, images only appear on title slides, limiting visual impact.

---

## Success Criteria

| Criteria | Target | Status |
|----------|--------|--------|
| File ingestion | MD, PDF, DOCX | 🔲 |
| Multi-image generation | 50%+ of slides | 🔲 |
| Speaker notes | Auto-generated | 🔲 |
| Generation time | < 45 seconds | 🔲 |

---

## User Stories

### US-05: Document Ingestion
**As a** user
**I want to** provide a document file and get a presentation
**So that** I can transform existing content into slides

**Acceptance Criteria:**
- [ ] Accept Markdown files
- [ ] Accept PDF files (text extraction)
- [ ] Accept DOCX files
- [ ] Preserve document structure in slides
- [ ] Handle large documents gracefully

### US-06: Multi-Slide Images
**As a** user
**I want** AI images on multiple slides
**So that** my entire presentation is visually engaging

**Acceptance Criteria:**
- [ ] Generate images for section/statement slides
- [ ] Skip images for data-heavy slides (tables, code)
- [ ] Parallel image generation for speed
- [ ] Style consistency across images

### US-07: Speaker Notes
**As a** user
**I want** auto-generated speaker notes
**So that** I have talking points for each slide

**Acceptance Criteria:**
- [ ] Notes generated per slide
- [ ] Based on slide content + context
- [ ] Accessible in HTML output
- [ ] Optional (can disable)

### US-08: Content Summarization
**As a** user
**I want** long content intelligently summarized
**So that** slides aren't overcrowded

**Acceptance Criteria:**
- [ ] Long bullet points condensed
- [ ] Key points extraction
- [ ] Maintain accuracy of information

---

## Technical Considerations

- PDF parsing library (PyMuPDF or pdfplumber)
- DOCX parsing (python-docx)
- Parallel async image generation
- Token budget management for summarization

---

## Change History

| Date | Change | Author |
|------|--------|--------|
| 2026-01-21 | Initial epic creation | Chris Park |
