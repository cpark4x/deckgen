"""Content analysis and narrative structuring."""

import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class ContentAnalyzer:
    """Analyzes content and creates structured content briefs."""
    
    def analyze(self, description: str, files: List[str] = None) -> Dict[str, Any]:
        """
        Analyze content and determine narrative structure.
        
        Args:
            description: User's description of the presentation
            files: Optional list of file paths for additional context
            
        Returns:
            Content brief dictionary with structure, type, audience, etc.
        """
        # Read and parse file content
        file_content = self._read_files(files or [])
        combined_text = f"{description}\n\n{file_content}"
        
        # Parse markdown structure
        sections = self._parse_markdown_sections(file_content)
        
        content_brief = {
            "description": description,
            "content_type": self._determine_content_type(combined_text),
            "audience": self._determine_audience(combined_text),
            "tone": self._determine_tone(combined_text),
            "has_code": self._detect_code_content(combined_text, files),
            "technical_depth": self._assess_technical_depth(combined_text),
            "sections": sections,
            "slides": self._generate_slides_from_content(description, sections, combined_text),
        }
        
        return content_brief
    
    def _read_files(self, files: List[str]) -> str:
        """Read content from all provided files."""
        content_parts = []
        
        for file_path in files:
            path = Path(file_path).expanduser()
            if path.exists():
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content_parts.append(f.read())
                    logger.debug("Read file: %s", file_path)
                except Exception as e:
                    logger.warning("Could not read %s: %s", file_path, e)
            else:
                logger.warning("File not found: %s", file_path)
        
        logger.info("Read %d files, total content length: %d chars", 
                   len(content_parts), sum(len(p) for p in content_parts))
        return "\n\n".join(content_parts)
    
    def _parse_markdown_sections(self, content: str) -> List[Dict[str, Any]]:
        """Parse markdown content into sections."""
        if not content.strip():
            return []
        
        sections = []
        current_section = None
        current_content = []
        
        lines = content.split("\n")
        
        for line in lines:
            # Check for headers (##, ###, or ####)
            h2_match = re.match(r'^##\s+(.+)$', line)
            h3_match = re.match(r'^###\s+(.+)$', line)
            h4_match = re.match(r'^####\s+(.+)$', line)
            
            # Treat both H2 and H3 as main sections
            if h2_match or h3_match:
                # Save previous section
                if current_section:
                    current_section["content"] = "\n".join(current_content).strip()
                    sections.append(current_section)
                
                title = (h2_match or h3_match).group(1).strip()
                level = 2 if h2_match else 3
                
                current_section = {
                    "level": level,
                    "title": title,
                    "content": "",
                    "subsections": []
                }
                current_content = []
            
            elif h4_match and current_section:
                # H4 becomes subsection
                current_section["subsections"].append({
                    "title": h4_match.group(1).strip(),
                    "content": ""
                })
                current_content.append(line)
            
            else:
                current_content.append(line)
        
        # Don't forget the last section
        if current_section:
            current_section["content"] = "\n".join(current_content).strip()
            sections.append(current_section)
        
        return sections
    
    def _extract_bullet_points(self, content: str, max_points: int = 5) -> List[str]:
        """Extract bullet points from content."""
        points = []
        
        # Match various bullet formats: -, *, •, numbered
        bullet_pattern = r'^[\s]*[-*•]\s+(.+)$|^[\s]*\d+\.\s+(.+)$'
        
        for line in content.split("\n"):
            match = re.match(bullet_pattern, line)
            if match:
                point = match.group(1) or match.group(2)
                if point:
                    # Clean up the point
                    point = re.sub(r'\*\*(.+?)\*\*', r'\1', point)  # Remove bold
                    point = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', point)  # Clean links
                    points.append(point.strip())
                    
                    if len(points) >= max_points:
                        break
        
        return points
    
    def _extract_table_data(self, content: str) -> Optional[List[Dict[str, str]]]:
        """Extract data from markdown tables."""
        lines = content.split("\n")
        table_data = []
        headers = []
        in_table = False
        
        for line in lines:
            if "|" in line and not line.strip().startswith("|--"):
                cells = [c.strip() for c in line.split("|") if c.strip()]
                
                if not in_table:
                    headers = cells
                    in_table = True
                elif cells and not all(c.replace("-", "").strip() == "" for c in cells):
                    if len(cells) >= len(headers):
                        row = {headers[i]: cells[i] for i in range(len(headers))}
                        table_data.append(row)
            elif in_table and "|" not in line and line.strip():
                break  # End of table
        
        return table_data if table_data else None
    
    def _extract_code_blocks(self, content: str) -> List[Dict[str, str]]:
        """Extract code blocks from markdown."""
        code_blocks = []
        pattern = r'```(\w*)\n(.*?)```'
        
        matches = re.findall(pattern, content, re.DOTALL)
        for lang, code in matches:
            code_blocks.append({
                "language": lang or "text",
                "code": code.strip()[:500]  # Limit code length
            })
        
        return code_blocks
    
    def _generate_slides_from_content(
        self, 
        description: str, 
        sections: List[Dict[str, Any]],
        full_text: str
    ) -> List[Dict[str, Any]]:
        """Generate slide specifications from parsed content."""
        slides = []
        
        # 1. Title slide
        title = self._extract_title(description, sections)
        subtitle = self._extract_subtitle(sections, full_text)
        slides.append({
            "type": "title",
            "title": title,
            "subtitle": subtitle
        })
        
        # 2. Generate slides from sections
        for section in sections:
            section_title = section["title"]
            section_content = section["content"]
            
            # Skip certain sections
            skip_titles = ["configuration", "files created", "environment"]
            if any(skip.lower() in section_title.lower() for skip in skip_titles):
                continue
            
            # Determine best slide type for this section
            bullet_points = self._extract_bullet_points(section_content)
            table_data = self._extract_table_data(section_content)
            code_blocks = self._extract_code_blocks(section_content)
            
            # Architecture/diagram sections
            if any(word in section_title.lower() for word in ["architecture", "diagram", "flow"]):
                slides.append({
                    "type": "architecture",
                    "title": section_title,
                    "content": self._get_first_paragraph(section_content),
                    "points": bullet_points[:4] if bullet_points else []
                })
            
            # Metrics/results sections
            elif any(word in section_title.lower() for word in ["result", "metric", "impact", "test"]):
                if table_data:
                    slides.append({
                        "type": "table",
                        "title": section_title,
                        "table": table_data[:5]
                    })
                elif bullet_points:
                    slides.append({
                        "type": "points",
                        "title": section_title,
                        "points": bullet_points[:5]
                    })
            
            # Code sections
            elif code_blocks or any(word in section_title.lower() for word in ["code", "implementation", "example"]):
                if code_blocks:
                    slides.append({
                        "type": "code",
                        "title": section_title,
                        "code": code_blocks[0]["code"],
                        "language": code_blocks[0]["language"]
                    })
            
            # Scenario/use case sections
            elif any(word in section_title.lower() for word in ["scenario", "use case", "hero"]):
                if bullet_points:
                    # Split into multiple slides if many points
                    for i in range(0, len(bullet_points), 3):
                        chunk = bullet_points[i:i+3]
                        slides.append({
                            "type": "cards",
                            "title": section_title if i == 0 else f"{section_title} (cont.)",
                            "cards": [{"title": p.split(":")[0] if ":" in p else p[:30], 
                                      "description": p.split(":")[-1].strip() if ":" in p else p} 
                                     for p in chunk]
                        })
            
            # What/Why sections - use points
            elif any(word in section_title.lower() for word in ["what", "why", "benefit", "feature", "built"]):
                if table_data:
                    slides.append({
                        "type": "table",
                        "title": section_title,
                        "table": table_data[:5]
                    })
                elif bullet_points:
                    slides.append({
                        "type": "points",
                        "title": section_title,
                        "points": bullet_points[:5]
                    })
                else:
                    # Use first paragraph as content
                    para = self._get_first_paragraph(section_content)
                    if para:
                        slides.append({
                            "type": "statement",
                            "title": section_title,
                            "content": para
                        })
            
            # Next steps / CTA sections
            elif any(word in section_title.lower() for word in ["next", "step", "action", "start"]):
                if bullet_points:
                    slides.append({
                        "type": "numbered",
                        "title": section_title,
                        "items": bullet_points[:5]
                    })
            
            # Default: use points or statement
            elif bullet_points:
                slides.append({
                    "type": "points",
                    "title": section_title,
                    "points": bullet_points[:5]
                })
            elif section_content.strip():
                para = self._get_first_paragraph(section_content)
                if para and len(para) > 20:
                    slides.append({
                        "type": "statement",
                        "title": section_title,
                        "content": para
                    })
        
        # 3. Ensure minimum slide count (at least 5 slides)
        min_slides = 5
        if len(slides) < min_slides - 1:  # -1 for closing slide we'll add
            slides = self._expand_slides(slides, description, min_slides - 1)
        
        # 4. Closing slide
        slides.append({
            "type": "cta",
            "title": "Thank You",
            "subtitle": "Questions?"
        })
        
        return slides
    
    def _expand_slides(
        self, 
        slides: List[Dict[str, Any]], 
        description: str, 
        min_count: int
    ) -> List[Dict[str, Any]]:
        """Expand slide count by generating topic-based content."""
        # Extract topic from description
        topic = self._extract_title(description, [])
        
        # Template slides to add based on common presentation structures
        expansion_templates = [
            {
                "type": "statement",
                "title": "The Challenge",
                "content": f"Understanding the key challenges and opportunities in {topic.lower()}."
            },
            {
                "type": "points",
                "title": "Key Insights",
                "points": [
                    "Industry trends and market dynamics",
                    "Critical success factors",
                    "Emerging opportunities",
                    "Strategic considerations"
                ]
            },
            {
                "type": "points",
                "title": "Our Approach",
                "points": [
                    "Research and analysis",
                    "Strategic planning",
                    "Implementation roadmap",
                    "Continuous improvement"
                ]
            },
            {
                "type": "cards",
                "title": "Key Benefits",
                "cards": [
                    {"title": "Efficiency", "description": "Streamlined processes and improved productivity"},
                    {"title": "Innovation", "description": "New capabilities and competitive advantages"},
                    {"title": "Growth", "description": "Expanded opportunities and scalability"}
                ]
            },
            {
                "type": "numbered",
                "title": "Next Steps",
                "items": [
                    "Review current state and objectives",
                    "Identify key priorities and resources",
                    "Develop implementation timeline",
                    "Execute and measure results"
                ]
            },
        ]
        
        # Insert expansion slides after title slide
        expanded = [slides[0]]  # Keep title slide
        
        template_idx = 0
        while len(expanded) < min_count and template_idx < len(expansion_templates):
            expanded.append(expansion_templates[template_idx])
            template_idx += 1
        
        # Add any remaining original slides (except title which is already added)
        for slide in slides[1:]:
            expanded.append(slide)
        
        return expanded
    
    def _extract_title(self, description: str, sections: List[Dict[str, Any]]) -> str:
        """Extract or generate a title."""
        # Check for H1 in first section
        if sections and sections[0].get("level") == 1:
            return sections[0]["title"]
        
        # Clean up description
        title = description.split(".")[0].strip()
        title = re.sub(r'^(create|make|build|generate)\s+(a\s+)?(deck|presentation|slides?)\s+(about|for|on)\s+', '', title, flags=re.I)
        
        return title[:80] if len(title) > 80 else title
    
    def _extract_subtitle(self, sections: List[Dict[str, Any]], full_text: str) -> str:
        """Extract or generate a subtitle."""
        # Look for session/date info
        date_match = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}', full_text)
        if date_match:
            return date_match.group(0)
        
        # Look for "Session Summary" or similar
        if "session summary" in full_text.lower():
            return "Session Summary"
        
        return ""
    
    def _get_first_paragraph(self, content: str) -> str:
        """Get the first meaningful paragraph from content."""
        paragraphs = content.split("\n\n")
        
        for para in paragraphs:
            # Skip headers, bullets, code blocks
            para = para.strip()
            if para and not para.startswith("#") and not para.startswith("-") and not para.startswith("```"):
                # Clean up markdown
                para = re.sub(r'\*\*(.+?)\*\*', r'\1', para)
                para = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', para)
                return para[:300]  # Limit length
        
        return ""
    
    def _determine_content_type(self, text: str) -> str:
        """Determine the type of content."""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["feature", "launch", "release", "announce"]):
            return "feature_launch"
        elif any(word in text_lower for word in ["architecture", "system", "design", "technical"]):
            return "technical"
        elif any(word in text_lower for word in ["metrics", "roi", "cost", "revenue", "business"]):
            return "business"
        elif any(word in text_lower for word in ["tutorial", "how to", "guide", "learn"]):
            return "tutorial"
        elif any(word in text_lower for word in ["vision", "strategy", "future", "roadmap"]):
            return "vision"
        else:
            return "general"
    
    def _determine_audience(self, text: str) -> str:
        """Determine target audience."""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["developer", "engineer", "technical", "code", "api"]):
            return "technical"
        elif any(word in text_lower for word in ["executive", "ceo", "leadership", "business"]):
            return "executive"
        else:
            return "mixed"
    
    def _determine_tone(self, text: str) -> str:
        """Determine presentation tone."""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["exciting", "innovative", "revolutionary"]):
            return "energetic"
        elif any(word in text_lower for word in ["professional", "enterprise", "formal"]):
            return "professional"
        else:
            return "neutral"
    
    def _detect_code_content(self, text: str, files: List[str] = None) -> bool:
        """Detect if content includes code."""
        # Check for code blocks
        if "```" in text:
            return True
        
        text_lower = text.lower()
        has_code_keywords = any(word in text_lower for word in [
            "code", "api", "function", "class", "implementation", "syntax"
        ])
        
        if files:
            code_extensions = [".py", ".js", ".ts", ".go", ".rs", ".java", ".cpp"]
            has_code_files = any(
                any(f.endswith(ext) for ext in code_extensions) 
                for f in files
            )
            return has_code_keywords or has_code_files
        
        return has_code_keywords
    
    def _assess_technical_depth(self, text: str) -> float:
        """Assess technical depth (0.0 to 1.0)."""
        technical_terms = [
            "architecture", "implementation", "algorithm", "infrastructure",
            "api", "database", "microservice", "container", "kubernetes",
            "protocol", "cache", "queue", "async", "performance"
        ]
        
        text_lower = text.lower()
        matches = sum(1 for term in technical_terms if term in text_lower)
        
        return min(matches / 5.0, 1.0)
