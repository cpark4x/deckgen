"""Theme and layout selection logic."""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

logger = logging.getLogger(__name__)


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
        
        logger.debug("Loaded %d themes: %s", len(themes), list(themes.keys()))
        return themes
    
    def select_theme(
        self, 
        content_brief: Dict[str, Any], 
        force_theme: str = None
    ) -> str:
        """
        Select appropriate theme based on content analysis and theme triggers.
        
        Args:
            content_brief: Content analysis results
            force_theme: Optional theme name to force selection
            
        Returns:
            Theme name
        """
        if force_theme:
            if force_theme in self.themes:
                return force_theme
            normalized = force_theme.replace("-", "_")
            if normalized in self.themes:
                return normalized
            logger.warning("Theme '%s' not found, will auto-select", force_theme)
        
        # Score each theme based on its triggers
        scores: Dict[str, float] = {}
        content_type = content_brief.get("content_type", "general")
        audience = content_brief.get("audience", "mixed")
        has_code = content_brief.get("has_code", False)
        technical_depth = content_brief.get("technical_depth", 0.0)
        
        for theme_name, theme_config in self.themes.items():
            score = 0.0
            triggers = theme_config.get("triggers", {})
            
            # Check content_type trigger
            trigger_content_types = triggers.get("content_type", [])
            if content_type in trigger_content_types:
                score += 2.0
            
            # Check audience trigger
            trigger_audiences = triggers.get("audience", [])
            if audience in trigger_audiences:
                score += 1.0
            
            # Check has_code trigger
            if triggers.get("has_code") and has_code:
                score += 1.5
            
            # Check technical_depth trigger (e.g., "0.6-1.0")
            depth_range = triggers.get("technical_depth", "")
            if isinstance(depth_range, str) and "-" in depth_range:
                try:
                    low, high = map(float, depth_range.split("-"))
                    if low <= technical_depth <= high:
                        score += 1.5
                except ValueError:
                    pass
            
            scores[theme_name] = score
            logger.debug("Theme '%s' score: %.1f", theme_name, score)
        
        # Select highest scoring theme, default to keynote_minimalist
        if scores:
            best_theme = max(scores, key=scores.get)  # type: ignore[arg-type]
            if scores[best_theme] > 0:
                logger.info("Selected theme '%s' (score: %.1f)", best_theme, scores[best_theme])
                return best_theme
        
        # Fallback to default
        default = "keynote_minimalist"
        logger.info("Using default theme '%s'", default)
        return default
    
    def design_slides(
        self, 
        content_brief: Dict[str, Any], 
        theme_name: str
    ) -> List[Dict[str, Any]]:
        """
        Design slide sequence with appropriate layouts using actual content.
        
        Args:
            content_brief: Content analysis results with extracted content
            theme_name: Selected theme name
            
        Returns:
            List of slide specifications with layout and content
        """
        theme = self.themes[theme_name]
        slides = []
        
        # Get slides from content brief (now contains real content)
        suggested_slides = content_brief.get("slides", [])
        
        for slide_spec in suggested_slides:
            slide_type = slide_spec.get("type", "title")
            designed_slide = self._design_slide(slide_spec, slide_type, theme, theme_name)
            if designed_slide:
                slides.append(designed_slide)
        
        return slides
    
    def _design_slide(
        self, 
        slide_spec: Dict[str, Any], 
        slide_type: str, 
        theme: Dict[str, Any],
        theme_name: str
    ) -> Optional[Dict[str, Any]]:
        """Design a single slide based on its type and content."""
        
        accent_color = theme.get("colors", {}).get("accent", "#0A84FF")
        
        if slide_type == "title":
            return {
                "layout": "title_center",
                "theme": theme_name,
                "content": {
                    "title": slide_spec.get("title", "Presentation"),
                    "subtitle": slide_spec.get("subtitle", ""),
                    "accent_color": accent_color
                }
            }
        
        elif slide_type == "statement":
            return {
                "layout": "statement",
                "theme": theme_name,
                "content": {
                    "title": slide_spec.get("title", ""),
                    "statement": slide_spec.get("content", "")
                }
            }
        
        elif slide_type == "points":
            points = slide_spec.get("points", [])
            return {
                "layout": "bullet_points",
                "theme": theme_name,
                "content": {
                    "title": slide_spec.get("title", "Key Points"),
                    "points": points
                }
            }
        
        elif slide_type == "numbered":
            items = slide_spec.get("items", [])
            return {
                "layout": "numbered_list",
                "theme": theme_name,
                "content": {
                    "title": slide_spec.get("title", "Steps"),
                    "items": items
                }
            }
        
        elif slide_type == "cards":
            cards = slide_spec.get("cards", [])
            return {
                "layout": "grid_thirds",
                "theme": theme_name,
                "content": {
                    "title": slide_spec.get("title", ""),
                    "cards": cards
                }
            }
        
        elif slide_type == "table":
            table = slide_spec.get("table", [])
            return {
                "layout": "table_slide",
                "theme": theme_name,
                "content": {
                    "title": slide_spec.get("title", ""),
                    "table": table
                }
            }
        
        elif slide_type == "code":
            return {
                "layout": "code_example",
                "theme": theme_name,
                "content": {
                    "title": slide_spec.get("title", "Implementation"),
                    "code": slide_spec.get("code", "# Code example"),
                    "language": slide_spec.get("language", "python")
                }
            }
        
        elif slide_type == "architecture":
            return {
                "layout": "architecture",
                "theme": theme_name,
                "content": {
                    "title": slide_spec.get("title", "Architecture"),
                    "description": slide_spec.get("content", ""),
                    "points": slide_spec.get("points", [])
                }
            }
        
        elif slide_type == "metrics":
            stats = slide_spec.get("stats", [])
            # Only render metrics slide if we have actual stats
            if not stats:
                logger.debug("Skipping metrics slide - no stats provided")
                return None
            return {
                "layout": "stat_grid",
                "theme": theme_name,
                "content": {
                    "title": slide_spec.get("title", "Impact"),
                    "stats": stats
                }
            }
        
        elif slide_type == "cta":
            return {
                "layout": "cta_final",
                "theme": theme_name,
                "content": {
                    "title": slide_spec.get("title", "Get Started"),
                    "subtitle": slide_spec.get("subtitle", ""),
                    "cta_text": slide_spec.get("cta_text", ""),
                    "cta_url": slide_spec.get("cta_url", "#")
                }
            }
        
        return None
    
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
