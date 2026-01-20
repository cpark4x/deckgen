"""Content analysis and narrative structuring."""

from typing import Any, Dict, List, Optional


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
        # Simple keyword-based analysis for Phase 1
        content_brief = {
            "description": description,
            "content_type": self._determine_content_type(description),
            "audience": self._determine_audience(description),
            "tone": self._determine_tone(description),
            "has_code": self._detect_code_content(description, files),
            "technical_depth": self._assess_technical_depth(description),
            "slides": self._suggest_slides(description),
        }
        
        return content_brief
    
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
        text_lower = text.lower()
        has_code_keywords = any(word in text_lower for word in [
            "code", "api", "function", "class", "implementation", "syntax"
        ])
        
        # Check if any files are code files
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
        
        # Normalize to 0-1 range
        return min(matches / 5.0, 1.0)
    
    def _suggest_slides(self, text: str) -> List[Dict[str, str]]:
        """Suggest slide structure based on content."""
        slides = []
        
        # Always start with title
        slides.append({
            "type": "title",
            "content": text[:100]  # First 100 chars as title hint
        })
        
        # Add context-appropriate slides
        text_lower = text.lower()
        
        if "problem" in text_lower or "challenge" in text_lower:
            slides.append({"type": "problem", "content": ""})
        
        if "solution" in text_lower or "how" in text_lower:
            slides.append({"type": "solution", "content": ""})
        
        if self._detect_code_content(text):
            slides.append({"type": "code", "content": ""})
        
        if any(word in text_lower for word in ["metric", "result", "impact", "performance"]):
            slides.append({"type": "metrics", "content": ""})
        
        # Always end with CTA
        slides.append({"type": "cta", "content": ""})
        
        return slides
