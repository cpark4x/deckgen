"""Theme and layout selection logic."""

from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


class ThemeDesigner:
    """Selects appropriate theme and layouts based on content analysis."""
    
    def __init__(self):
        """Initialize designer with available themes."""
        self.themes_dir = Path(__file__).parent.parent / "themes"
        self.themes = self._load_themes()
    
    def _load_themes(self) -> Dict[str, Dict[str, Any]]:
        """Load all theme configurations."""
        themes = {}
        
        for theme_file in self.themes_dir.glob("*.yaml"):
            with open(theme_file, "r") as f:
                theme_data = yaml.safe_load(f)
                theme_name = theme_file.stem
                themes[theme_name] = theme_data
        
        return themes
    
    def select_theme(
        self, 
        content_brief: Dict[str, Any], 
        force_theme: str = None
    ) -> str:
        """
        Select appropriate theme based on content analysis.
        
        Args:
            content_brief: Content analysis results
            force_theme: Optional theme name to force selection
            
        Returns:
            Theme name
        """
        # If theme is forced, use it
        if force_theme:
            if force_theme in self.themes:
                return force_theme
            # Normalize theme name (handle hyphens vs underscores)
            normalized = force_theme.replace("-", "_")
            if normalized in self.themes:
                return normalized
            # Fall back to default
            print(f"Warning: Theme '{force_theme}' not found, using default")
        
        # AI-driven selection based on content signals
        content_type = content_brief.get("content_type", "general")
        audience = content_brief.get("audience", "mixed")
        has_code = content_brief.get("has_code", False)
        technical_depth = content_brief.get("technical_depth", 0.0)
        
        # Decision logic
        if technical_depth > 0.6 or has_code:
            return "technical_blueprint"
        elif audience == "executive" or content_type == "vision":
            return "keynote_minimalist"
        elif content_type == "business":
            return "keynote_minimalist"  # Phase 1: only 2 themes
        else:
            return "keynote_minimalist"  # Default
    
    def design_slides(
        self, 
        content_brief: Dict[str, Any], 
        theme_name: str
    ) -> List[Dict[str, Any]]:
        """
        Design slide sequence with appropriate layouts.
        
        Args:
            content_brief: Content analysis results
            theme_name: Selected theme name
            
        Returns:
            List of slide specifications with layout and content
        """
        theme = self.themes[theme_name]
        slides = []
        
        # Get suggested slides from content brief
        suggested_slides = content_brief.get("slides", [])
        
        # Map slide types to layouts
        for slide_spec in suggested_slides:
            slide_type = slide_spec.get("type", "title")
            
            if slide_type == "title":
                slides.append({
                    "layout": "title_center",
                    "theme": theme_name,
                    "content": {
                        "title": content_brief.get("description", "Presentation"),
                        "subtitle": self._generate_subtitle(content_brief),
                        "accent_color": theme.get("colors", {}).get("accent", "#0A84FF")
                    }
                })
            
            elif slide_type == "problem":
                slides.append({
                    "layout": "grid_thirds",
                    "theme": theme_name,
                    "content": {
                        "title": "The Challenge",
                        "items": self._extract_problem_points(content_brief)
                    }
                })
            
            elif slide_type == "solution":
                slides.append({
                    "layout": "split_50_50",
                    "theme": theme_name,
                    "content": {
                        "title": "The Solution",
                        "left": "Overview",
                        "right": "Implementation"
                    }
                })
            
            elif slide_type == "code":
                slides.append({
                    "layout": "code_example",
                    "theme": theme_name,
                    "content": {
                        "title": "Implementation",
                        "code": "# Example code\nprint('Hello, World!')"
                    }
                })
            
            elif slide_type == "metrics":
                slides.append({
                    "layout": "stat_grid",
                    "theme": theme_name,
                    "content": {
                        "title": "Impact",
                        "stats": [
                            {"number": "3x", "label": "Faster"},
                            {"number": "50%", "label": "Cost Reduction"},
                            {"number": "99.9%", "label": "Uptime"}
                        ]
                    }
                })
            
            elif slide_type == "cta":
                slides.append({
                    "layout": "cta_final",
                    "theme": theme_name,
                    "content": {
                        "title": "Get Started",
                        "cta_text": "Learn More",
                        "cta_url": "#"
                    }
                })
        
        return slides
    
    def _generate_subtitle(self, content_brief: Dict[str, Any]) -> str:
        """Generate appropriate subtitle based on content."""
        content_type = content_brief.get("content_type", "general")
        
        subtitles = {
            "feature_launch": "A new capability",
            "technical": "Technical deep dive",
            "business": "Business impact",
            "tutorial": "Step-by-step guide",
            "vision": "Our vision for the future",
            "general": "An overview"
        }
        
        return subtitles.get(content_type, "An overview")
    
    def _extract_problem_points(self, content_brief: Dict[str, Any]) -> List[Dict[str, str]]:
        """Extract key problem points for grid layout."""
        # Simple placeholder for Phase 1
        return [
            {"title": "Challenge 1", "description": "First key challenge"},
            {"title": "Challenge 2", "description": "Second key challenge"},
            {"title": "Challenge 3", "description": "Third key challenge"}
        ]
    
    def get_theme_info(self, theme_name: str) -> Dict[str, Any]:
        """Get theme configuration."""
        normalized = theme_name.replace("-", "_")
        return self.themes.get(normalized, {})
    
    def list_themes(self) -> List[Dict[str, str]]:
        """List all available themes with descriptions."""
        theme_list = []
        
        for name, config in self.themes.items():
            theme_list.append({
                "name": name,
                "display_name": name.replace("_", "-"),
                "description": config.get("description", "No description"),
                "best_for": ", ".join(config.get("triggers", {}).get("content_type", []))
            })
        
        return theme_list
