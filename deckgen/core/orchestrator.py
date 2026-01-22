"""Main orchestrator for deck generation pipeline."""

import logging
from pathlib import Path
from typing import List, Optional

from .analyzer import ContentAnalyzer
from .designer import ThemeDesigner
from .image_generator import ImageGenerator
from .renderer import HTMLRenderer

logger = logging.getLogger(__name__)


class DeckOrchestrator:
    """Orchestrates the complete deck generation pipeline."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize orchestrator with all components.
        
        Args:
            api_key: Optional Gemini API key for image generation.
                     If not provided, reads from GEMINI_API_KEY env var.
        """
        self.analyzer = ContentAnalyzer()
        self.designer = ThemeDesigner()
        self.image_generator = ImageGenerator(api_key=api_key)
        self.renderer = HTMLRenderer()
    
    def create_deck(
        self,
        description: str,
        files: Optional[List[str]] = None,
        theme: Optional[str] = None,
        output_path: Optional[str] = None,
        generate_images: bool = True,
    ) -> str:
        """
        Create a complete presentation deck.

        Args:
            description: User's description of the presentation
            files: Optional list of file paths for context
            theme: Optional theme to force (otherwise auto-selected)
            output_path: Optional output file path
            generate_images: Whether to generate AI images (default: True)

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
        
        # Step 3: Generate images (if enabled)
        if generate_images and self.image_generator.enabled:
            logger.debug("Step 3: Generating images")
            slides = self.image_generator.generate_images_for_slides(
                slides=slides,
                theme_name=theme_name,
                deck_context=description,
            )
        elif generate_images:
            logger.info("Image generation skipped - no API key configured")
        
        # Step 4: Render HTML
        logger.debug("Step 4: Rendering HTML")
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
