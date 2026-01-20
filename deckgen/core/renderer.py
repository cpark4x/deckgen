"""HTML rendering from templates and design specifications."""

from pathlib import Path
from typing import Any, Dict, List

import yaml


class HTMLRenderer:
    """Renders HTML presentations from design specifications."""
    
    def __init__(self):
        """Initialize renderer with templates."""
        self.templates_dir = Path(__file__).parent.parent / "templates"
        self.layouts_dir = self.templates_dir / "layouts"
    
    def render(
        self, 
        slides: List[Dict[str, Any]], 
        theme_name: str,
        title: str = "Presentation"
    ) -> str:
        """
        Render complete HTML presentation.
        
        Args:
            slides: List of slide specifications
            theme_name: Theme to use
            title: Presentation title
            
        Returns:
            Complete HTML string
        """
        # Load theme configuration
        theme = self._load_theme(theme_name)
        
        # Load base template
        base_html = self._load_template("base.html")
        
        # Load navigation JS
        nav_js = self._load_template("navigation.js")
        
        # Generate CSS from theme
        css = self._generate_css(theme)
        
        # Render all slides
        slides_html = self._render_slides(slides, theme)
        
        # Combine everything
        html = base_html.replace("{{CSS}}", css)
        html = html.replace("{{SLIDES}}", slides_html)
        html = html.replace("{{NAVIGATION_JS}}", nav_js)
        html = html.replace("{{TITLE}}", title)
        
        return html
    
    def _load_theme(self, theme_name: str) -> Dict[str, Any]:
        """Load theme configuration."""
        theme_file = Path(__file__).parent.parent / "themes" / f"{theme_name}.yaml"
        
        with open(theme_file, "r") as f:
            return yaml.safe_load(f)
    
    def _load_template(self, filename: str) -> str:
        """Load template file."""
        template_path = self.templates_dir / filename
        
        with open(template_path, "r") as f:
            return f.read()
    
    def _generate_css(self, theme: Dict[str, Any]) -> str:
        """Generate CSS from theme configuration."""
        colors = theme.get("colors", {})
        typography = theme.get("typography", {})
        
        css = f"""
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: {typography.get('primary_font', '-apple-system, BlinkMacSystemFont, sans-serif')};
            background: {colors.get('background', '#000')};
            color: {colors.get('text_primary', '#fff')};
            overflow: hidden;
        }}
        
        .slide {{
            display: none;
            width: 100vw;
            height: 100vh;
            padding: 60px 80px;
            flex-direction: column;
            justify-content: center;
        }}
        
        .slide.active {{
            display: flex;
        }}
        
        .headline {{
            font-size: {typography.get('headline_size', '72px')};
            font-weight: {typography.get('headline_weight', 700)};
            letter-spacing: -2px;
            line-height: 1.1;
            margin-bottom: 24px;
        }}
        
        .subhead {{
            font-size: 32px;
            font-weight: 400;
            color: {colors.get('text_secondary', 'rgba(255,255,255,0.7)')};
            line-height: 1.4;
        }}
        
        .section-label {{
            font-size: 14px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: {colors.get('accent', '#0A84FF')};
            margin-bottom: 16px;
        }}
        
        .center {{
            text-align: center;
            align-items: center;
        }}
        
        .split {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 80px;
            align-items: center;
            height: 100%;
        }}
        
        .thirds {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 40px;
            margin-top: 40px;
        }}
        
        .card {{
            background: {colors.get('card_bg', 'rgba(255,255,255,0.05)')};
            border: 1px solid {colors.get('border', 'rgba(255,255,255,0.1)')};
            border-radius: 16px;
            padding: 32px;
        }}
        
        .card-title {{
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 12px;
            color: {colors.get('accent', '#0A84FF')};
        }}
        
        .card-text {{
            font-size: 16px;
            color: {colors.get('text_secondary', 'rgba(255,255,255,0.7)')};
            line-height: 1.5;
        }}
        
        .code-block {{
            background: {colors.get('card_bg', 'rgba(255,255,255,0.05)')};
            border: 1px solid {colors.get('border', 'rgba(255,255,255,0.1)')};
            border-radius: 12px;
            padding: 24px 32px;
            font-family: {typography.get('code_font', "'SF Mono', 'Consolas', monospace")};
            font-size: 18px;
            line-height: 1.6;
            color: #98D4A0;
            margin: 20px 0;
            overflow-x: auto;
        }}
        
        .code-comment {{
            color: rgba(255,255,255,0.4);
        }}
        
        .stat-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 40px;
            margin-top: 40px;
        }}
        
        .stat-number {{
            font-size: 64px;
            font-weight: 700;
            color: {colors.get('accent', '#0A84FF')};
            margin-bottom: 8px;
        }}
        
        .stat-label {{
            font-size: 18px;
            color: {colors.get('text_secondary', 'rgba(255,255,255,0.7)')};
        }}
        
        .cta-button {{
            display: inline-block;
            padding: 16px 48px;
            background: {colors.get('accent', '#0A84FF')};
            color: #fff;
            text-decoration: none;
            border-radius: 8px;
            font-size: 20px;
            font-weight: 600;
            margin-top: 40px;
            transition: transform 0.2s ease;
        }}
        
        .cta-button:hover {{
            transform: scale(1.05);
        }}
        
        .nav {{
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 8px;
            z-index: 100;
        }}
        
        .nav-dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: rgba(255,255,255,0.3);
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .nav-dot.active {{
            background: {colors.get('accent', '#0A84FF')};
            width: 24px;
            border-radius: 4px;
        }}
        
        .slide-counter {{
            position: fixed;
            bottom: 30px;
            right: 40px;
            font-size: 14px;
            color: rgba(255,255,255,0.4);
        }}
        """
        
        return css
    
    def _render_slides(self, slides: List[Dict[str, Any]], theme: Dict[str, Any]) -> str:
        """Render all slides."""
        html_slides = []
        
        for i, slide_spec in enumerate(slides):
            layout_name = slide_spec.get("layout", "title_center")
            content = slide_spec.get("content", {})
            
            # Load layout template
            slide_html = self._render_slide(layout_name, content, i == 0)
            html_slides.append(slide_html)
        
        return "\n".join(html_slides)
    
    def _render_slide(self, layout: str, content: Dict[str, Any], is_first: bool = False) -> str:
        """Render a single slide."""
        layout_file = self.layouts_dir / f"{layout}.html"
        
        if not layout_file.exists():
            # Fallback to simple slide
            return self._render_simple_slide(content, is_first)
        
        with open(layout_file, "r") as f:
            template = f.read()
        
        # Simple placeholder replacement
        for key, value in content.items():
            placeholder = f"{{{{{key.upper()}}}}}"
            template = template.replace(placeholder, str(value))
        
        # Add active class to first slide
        if is_first:
            template = template.replace('<div class="slide', '<div class="slide active')
        
        return template
    
    def _render_simple_slide(self, content: Dict[str, Any], is_first: bool = False) -> str:
        """Render a simple fallback slide."""
        active_class = " active" if is_first else ""
        title = content.get("title", "Slide")
        
        return f"""
        <div class="slide{active_class} center">
            <h1 class="headline">{title}</h1>
        </div>
        """
