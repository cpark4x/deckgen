"""Main orchestrator for deck generation pipeline."""

import logging
from pathlib import Path
from typing import List, Optional

from .analyzer import ContentAnalyzer
from .designer import ThemeDesigner
from .renderer import HTMLRenderer

logger = logging.getLogger(__name__)


class DeckOrchestrator:
    """Orchestrates the complete deck generation pipeline."""
    
    def __init__(self):
        """Initialize orchestrator with all components."""
        self.analyzer = ContentAnalyzer()
        self.designer = ThemeDesigner()
        self.renderer = HTMLRenderer()
    
    def create_deck(
        self,
        description: str,
        files: Optional[List[str]] = None,
        theme: Optional[str] = None,
        output_path: Optional[str] = None,
    ) -> str:
        """
        Create a complete presentation deck.

        Args:
            description: User's description of the presentation
            files: Optional list of file paths for context
            theme: Optional theme to force (otherwise auto-selected)
            output_path: Optional output file path

        Returns:
            Path to generated HTML file
        """
        logger.info("Starting deck generation for: %s", description[:50])
        
        # Step 1: Analyze content
        logger.debug("Step 1: Analyzing content")
        content_brief = self.analyzer.analyze(description, files or [])

        # Step 2: Select theme and design slides
        logger.debug("Step 2: Selecting theme and designing slides")
        theme_name = self.designer.select_theme(
            content_brief, force_theme=theme or ""
        )
        slides = self.designer.design_slides(content_brief, theme_name)
        logger.info("Selected theme: %s, Generated %d slides", theme_name, len(slides))
        
        # Step 3: Render HTML
        logger.debug("Step 3: Rendering HTML")
        # Use title from content brief (extracted by analyzer)
        title = content_brief.get("slides", [{}])[0].get("title", description[:60])
        html = self.renderer.render(slides, theme_name, title)
        
        # Step 4: Save to file
        if not output_path:
            output_path = self._generate_output_path(description)
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, "w") as f:
            f.write(html)
        
        logger.info("Deck saved to: %s", output_file)
        return str(output_file.absolute())
    
    def _generate_output_path(self, description: str) -> str:
        """Generate output filename from description."""
        # Create slug from description
        slug = description.lower()
        slug = slug.replace(" ", "-")
        
        # Remove special characters
        slug = "".join(c for c in slug if c.isalnum() or c == "-")
        
        # Limit length
        slug = slug[:50]
        
        # Ensure output directory exists
        output_dir = Path.cwd() / "output"
        output_dir.mkdir(exist_ok=True)
        
        return str(output_dir / f"{slug}.html")
