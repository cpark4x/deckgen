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
        theme = self._load_theme(theme_name)
        css = self._generate_css(theme)
        nav_js = self._generate_navigation_js()
        slides_html = self._render_slides(slides, theme)
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title[:60]}</title>
    <style>
        {css}
    </style>
</head>
<body>
    {slides_html}
    <div class="nav" id="nav"></div>
    <div class="slide-counter" id="counter"></div>
    <script>
        {nav_js}
    </script>
</body>
</html>"""
        
        return html
    
    def _load_theme(self, theme_name: str) -> Dict[str, Any]:
        """Load theme configuration."""
        theme_file = Path(__file__).parent.parent / "themes" / f"{theme_name}.yaml"
        
        with open(theme_file, "r") as f:
            return yaml.safe_load(f)
    
    def _generate_navigation_js(self) -> str:
        """Generate navigation JavaScript with keyboard, touch, and click support."""
        return """
        let currentSlide = 0;
        const slides = document.querySelectorAll('.slide');
        const nav = document.getElementById('nav');
        const counter = document.getElementById('counter');
        
        // Create navigation dots with accessibility
        slides.forEach((_, i) => {
            const dot = document.createElement('div');
            dot.className = 'nav-dot' + (i === 0 ? ' active' : '');
            dot.setAttribute('role', 'button');
            dot.setAttribute('aria-label', `Go to slide ${i + 1}`);
            dot.setAttribute('tabindex', '0');
            dot.onclick = () => goToSlide(i);
            dot.onkeydown = (e) => { if (e.key === 'Enter' || e.key === ' ') goToSlide(i); };
            nav.appendChild(dot);
        });
        
        function updateCounter() {
            counter.textContent = `${currentSlide + 1} / ${slides.length}`;
        }
        
        function goToSlide(n) {
            slides[currentSlide].classList.remove('active');
            document.querySelectorAll('.nav-dot')[currentSlide].classList.remove('active');
            
            currentSlide = n;
            if (currentSlide >= slides.length) currentSlide = 0;
            if (currentSlide < 0) currentSlide = slides.length - 1;
            
            slides[currentSlide].classList.add('active');
            document.querySelectorAll('.nav-dot')[currentSlide].classList.add('active');
            updateCounter();
        }
        
        function nextSlide() { goToSlide(currentSlide + 1); }
        function prevSlide() { goToSlide(currentSlide - 1); }
        
        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            switch(e.key) {
                case 'ArrowRight':
                case ' ':
                case 'PageDown':
                    e.preventDefault();
                    nextSlide();
                    break;
                case 'ArrowLeft':
                case 'PageUp':
                    e.preventDefault();
                    prevSlide();
                    break;
                case 'Home':
                    e.preventDefault();
                    goToSlide(0);
                    break;
                case 'End':
                    e.preventDefault();
                    goToSlide(slides.length - 1);
                    break;
            }
        });
        
        // Touch swipe navigation
        let touchStartX = 0;
        let touchStartY = 0;
        let touchEndX = 0;
        let touchEndY = 0;
        const SWIPE_THRESHOLD = 50;
        
        document.addEventListener('touchstart', (e) => {
            touchStartX = e.changedTouches[0].screenX;
            touchStartY = e.changedTouches[0].screenY;
        }, { passive: true });
        
        document.addEventListener('touchend', (e) => {
            touchEndX = e.changedTouches[0].screenX;
            touchEndY = e.changedTouches[0].screenY;
            handleSwipe();
        }, { passive: true });
        
        function handleSwipe() {
            const diffX = touchStartX - touchEndX;
            const diffY = touchStartY - touchEndY;
            
            // Only handle horizontal swipes (ignore vertical scrolling)
            if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > SWIPE_THRESHOLD) {
                if (diffX > 0) {
                    nextSlide(); // Swipe left = next
                } else {
                    prevSlide(); // Swipe right = previous
                }
            }
        }
        
        // Click navigation (left half = back, right half = forward)
        // Exclude clicks on nav dots, buttons, and links
        document.addEventListener('click', (e) => {
            const tag = e.target.tagName.toLowerCase();
            const isInteractive = tag === 'a' || tag === 'button' || 
                                  e.target.classList.contains('nav-dot') ||
                                  e.target.closest('.nav') ||
                                  e.target.closest('a') ||
                                  e.target.closest('button');
            
            if (isInteractive) return;
            
            const clickX = e.clientX;
            const windowWidth = window.innerWidth;
            
            if (clickX < windowWidth / 3) {
                prevSlide(); // Left third = previous
            } else if (clickX > (windowWidth * 2 / 3)) {
                nextSlide(); // Right third = next
            }
            // Middle third does nothing (allows text selection, etc.)
        });
        
        updateCounter();
        """
    
    def _generate_css(self, theme: Dict[str, Any]) -> str:
        """Generate CSS from theme configuration with responsive design."""
        colors = theme.get("colors", {})
        typography = theme.get("typography", {})
        
        bg = colors.get('background', '#000')
        text_primary = colors.get('text_primary', '#fff')
        text_secondary = colors.get('text_secondary', 'rgba(255,255,255,0.7)')
        accent = colors.get('accent', '#0A84FF')
        accent_secondary = colors.get('accent_secondary', '#98D4A0')
        card_bg = colors.get('card_bg', 'rgba(255,255,255,0.05)')
        border = colors.get('border', 'rgba(255,255,255,0.1)')
        
        primary_font = typography.get('primary_font', '-apple-system, BlinkMacSystemFont, sans-serif')
        code_font = typography.get('code_font', "'SF Mono', 'Consolas', monospace")
        headline_weight = typography.get('headline_weight', 700)
        
        # Determine nav dot inactive color based on background brightness
        # For dark backgrounds use white-based, for light use black-based
        nav_dot_inactive = 'rgba(255,255,255,0.3)' if bg.startswith('#0') or bg.startswith('#1') or bg.startswith('#2') else 'rgba(0,0,0,0.3)'
        counter_color = 'rgba(255,255,255,0.4)' if bg.startswith('#0') or bg.startswith('#1') or bg.startswith('#2') else 'rgba(0,0,0,0.4)'
        
        return f"""
        :root {{
            /* Fluid typography scale */
            --font-headline: clamp(36px, 8vw, 72px);
            --font-headline-medium: clamp(28px, 6vw, 56px);
            --font-subhead: clamp(18px, 3.5vw, 28px);
            --font-body: clamp(16px, 2.5vw, 22px);
            --font-body-large: clamp(18px, 3vw, 28px);
            --font-small: clamp(12px, 1.5vw, 14px);
            --font-code: clamp(13px, 1.8vw, 16px);
            --font-stat: clamp(48px, 12vw, 72px);
            
            /* Fluid spacing scale */
            --space-slide-padding: clamp(24px, 5vw, 80px);
            --space-slide-padding-y: clamp(40px, 6vh, 60px);
            --space-gap-large: clamp(24px, 4vw, 80px);
            --space-gap-medium: clamp(16px, 3vw, 40px);
            --space-gap-small: clamp(12px, 2vw, 24px);
            --space-element-margin: clamp(16px, 3vw, 40px);
            
            /* Theme colors as CSS variables */
            --color-bg: {bg};
            --color-text: {text_primary};
            --color-text-secondary: {text_secondary};
            --color-accent: {accent};
            --color-accent-secondary: {accent_secondary};
            --color-card-bg: {card_bg};
            --color-border: {border};
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        html {{
            font-size: 16px;
            -webkit-text-size-adjust: 100%;
        }}
        
        body {{
            font-family: {primary_font};
            background: var(--color-bg);
            color: var(--color-text);
            overflow: hidden;
            min-height: 100vh;
            min-height: 100dvh;
        }}
        
        .slide {{
            display: none;
            width: 100vw;
            height: 100vh;
            height: 100dvh;
            padding: var(--space-slide-padding-y) var(--space-slide-padding);
            flex-direction: column;
            justify-content: center;
            overflow-y: auto;
        }}
        
        .slide.active {{ display: flex; }}
        
        .headline {{
            font-size: var(--font-headline);
            font-weight: {headline_weight};
            letter-spacing: -0.02em;
            line-height: 1.1;
            margin-bottom: var(--space-gap-small);
        }}
        
        .subhead {{
            font-size: var(--font-subhead);
            font-weight: 400;
            color: var(--color-text-secondary);
            line-height: 1.4;
        }}
        
        .section-label {{
            font-size: var(--font-small);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.15em;
            color: var(--color-accent);
            margin-bottom: var(--space-gap-small);
        }}
        
        .center {{ text-align: center; align-items: center; }}
        
        .split {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: var(--space-gap-large);
            align-items: center;
            height: 100%;
        }}
        
        .thirds {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(min(280px, 100%), 1fr));
            gap: var(--space-gap-medium);
            margin-top: var(--space-element-margin);
        }}
        
        .halves {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr));
            gap: var(--space-gap-medium);
            margin-top: var(--space-element-margin);
        }}
        
        .card {{
            background: var(--color-card-bg);
            border: 1px solid var(--color-border);
            border-radius: clamp(12px, 2vw, 16px);
            padding: var(--space-gap-medium);
        }}
        
        .card-title {{
            font-size: clamp(18px, 2.5vw, 22px);
            font-weight: 600;
            margin-bottom: var(--space-gap-small);
            color: var(--color-accent);
        }}
        
        .card-text {{
            font-size: var(--font-body);
            color: var(--color-text-secondary);
            line-height: 1.6;
        }}
        
        .bullet-list {{
            list-style: none;
            margin-top: var(--space-element-margin);
        }}
        
        .bullet-list li {{
            font-size: var(--font-body-large);
            line-height: 1.6;
            margin-bottom: var(--space-gap-small);
            padding-left: clamp(28px, 4vw, 40px);
            position: relative;
            color: var(--color-text-secondary);
        }}
        
        .bullet-list li::before {{
            content: "→";
            position: absolute;
            left: 0;
            color: var(--color-accent);
        }}
        
        .numbered-list {{
            list-style: none;
            margin-top: var(--space-element-margin);
            counter-reset: item;
        }}
        
        .numbered-list li {{
            font-size: var(--font-body-large);
            line-height: 1.5;
            margin-bottom: var(--space-gap-small);
            padding-left: clamp(44px, 6vw, 60px);
            position: relative;
            color: var(--color-text-secondary);
        }}
        
        .numbered-list li::before {{
            counter-increment: item;
            content: counter(item);
            position: absolute;
            left: 0;
            width: clamp(32px, 4vw, 40px);
            height: clamp(32px, 4vw, 40px);
            background: var(--color-accent);
            color: #fff;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            font-size: clamp(14px, 2vw, 18px);
        }}
        
        .code-block {{
            background: var(--color-card-bg);
            border: 1px solid var(--color-border);
            border-radius: clamp(8px, 1.5vw, 12px);
            padding: var(--space-gap-medium);
            font-family: {code_font};
            font-size: var(--font-code);
            line-height: 1.6;
            color: var(--color-accent-secondary);
            margin: var(--space-gap-small) 0;
            overflow-x: auto;
            white-space: pre-wrap;
            max-height: 60vh;
        }}
        
        .stat-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(min(150px, 100%), 1fr));
            gap: var(--space-gap-medium);
            margin-top: var(--space-element-margin);
            text-align: center;
        }}
        
        .stat-number {{
            font-size: var(--font-stat);
            font-weight: 700;
            color: var(--color-accent);
            margin-bottom: 8px;
        }}
        
        .stat-label {{
            font-size: var(--font-body);
            color: var(--color-text-secondary);
        }}
        
        .cta-button {{
            display: inline-block;
            padding: clamp(12px, 2vw, 16px) clamp(32px, 5vw, 48px);
            background: var(--color-accent);
            color: #fff;
            text-decoration: none;
            border-radius: 8px;
            font-size: var(--font-body);
            font-weight: 600;
            margin-top: var(--space-element-margin);
            transition: transform 0.2s ease;
            min-height: 44px;
            min-width: 44px;
        }}
        
        .cta-button:hover {{ transform: scale(1.05); }}
        
        .statement {{
            font-size: clamp(20px, 4vw, 32px);
            line-height: 1.5;
            color: var(--color-text-secondary);
            max-width: 900px;
        }}
        
        table.data-table {{
            width: 100%;
            margin-top: var(--space-gap-medium);
            border-collapse: collapse;
        }}
        
        table.data-table th,
        table.data-table td {{
            padding: clamp(10px, 2vw, 16px) clamp(12px, 2.5vw, 20px);
            text-align: left;
            border-bottom: 1px solid var(--color-border);
        }}
        
        table.data-table th {{
            color: var(--color-accent);
            font-weight: 600;
            font-size: var(--font-small);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        table.data-table td {{
            color: var(--color-text-secondary);
            font-size: var(--font-body);
        }}
        
        table.data-table tr:hover td {{
            background: var(--color-card-bg);
        }}
        
        .nav {{
            position: fixed;
            bottom: clamp(16px, 3vh, 30px);
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
            background: {nav_dot_inactive};
            cursor: pointer;
            transition: all 0.3s ease;
            min-width: 44px;
            min-height: 44px;
            display: flex;
            align-items: center;
            justify-content: center;
            background-clip: content-box;
            padding: 18px;
        }}
        
        .nav-dot.active {{
            background: var(--color-accent);
            width: 24px;
            border-radius: 4px;
            background-clip: content-box;
        }}
        
        .slide-counter {{
            position: fixed;
            bottom: clamp(16px, 3vh, 30px);
            right: clamp(20px, 4vw, 40px);
            font-size: var(--font-small);
            color: {counter_color};
        }}
        
        /* Tablet and below */
        @media (max-width: 768px) {{
            .split {{
                grid-template-columns: 1fr;
                gap: var(--space-gap-medium);
            }}
        }}
        
        /* Landscape mobile */
        @media (max-height: 500px) and (orientation: landscape) {{
            .slide {{
                justify-content: flex-start;
                padding-top: var(--space-gap-medium);
            }}
        }}
        
        /* Reduced motion preference */
        @media (prefers-reduced-motion: reduce) {{
            *, *::before, *::after {{
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }}
        }}
        """
    
    def _render_slides(self, slides: List[Dict[str, Any]], theme: Dict[str, Any]) -> str:
        """Render all slides."""
        html_slides = []
        
        for i, slide_spec in enumerate(slides):
            slide_html = self._render_slide(slide_spec, i == 0)
            html_slides.append(slide_html)
        
        return "\n".join(html_slides)
    
    def _render_slide(self, slide_spec: Dict[str, Any], is_first: bool = False) -> str:
        """Render a single slide based on its layout."""
        layout = slide_spec.get("layout", "title_center")
        content = slide_spec.get("content", {})
        active = " active" if is_first else ""
        bg_image = slide_spec.get("background_image")
        
        # Build inline style for background image if present
        bg_style = ""
        if bg_image:
            bg_style = (
                f'style="background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.7)), '
                f'url(data:image/png;base64,{bg_image}); '
                f'background-size: cover; background-position: center;"'
            )
        
        if layout == "title_center":
            return self._render_title_slide(content, active, bg_style)
        elif layout == "statement":
            return self._render_statement_slide(content, active, bg_style)
        elif layout == "bullet_points":
            return self._render_bullet_slide(content, active, bg_style)
        elif layout == "numbered_list":
            return self._render_numbered_slide(content, active, bg_style)
        elif layout == "grid_thirds":
            return self._render_cards_slide(content, active, bg_style)
        elif layout == "table_slide":
            return self._render_table_slide(content, active, bg_style)
        elif layout == "code_example":
            return self._render_code_slide(content, active, bg_style)
        elif layout == "architecture":
            return self._render_architecture_slide(content, active, bg_style)
        elif layout == "stat_grid":
            return self._render_stats_slide(content, active, bg_style)
        elif layout == "cta_final":
            return self._render_cta_slide(content, active, bg_style)
        else:
            return self._render_simple_slide(content, active, bg_style)
    
    def _render_title_slide(self, content: Dict[str, Any], active: str, bg_style: str = "") -> str:
        title = self._escape_html(content.get("title", "Presentation"))
        subtitle = self._escape_html(content.get("subtitle", ""))
        subtitle_html = f'<p class="subhead">{subtitle}</p>' if subtitle else ""
        
        return f"""
<div class="slide{active} center" {bg_style}>
    <h1 class="headline">{title}</h1>
    {subtitle_html}
</div>"""
    
    def _render_statement_slide(self, content: Dict[str, Any], active: str, bg_style: str = "") -> str:
        title = self._escape_html(content.get("title", ""))
        statement = self._escape_html(content.get("statement", ""))
        
        return f"""
<div class="slide{active}" {bg_style}>
    <h2 class="headline">{title}</h2>
    <p class="statement">{statement}</p>
</div>"""
    
    def _render_bullet_slide(self, content: Dict[str, Any], active: str, bg_style: str = "") -> str:
        title = self._escape_html(content.get("title", "Key Points"))
        points = content.get("points", [])
        
        points_html = "\n".join([
            f'        <li>{self._escape_html(p)}</li>' 
            for p in points
        ])
        
        return f"""
<div class="slide{active}" {bg_style}>
    <h2 class="headline">{title}</h2>
    <ul class="bullet-list">
{points_html}
    </ul>
</div>"""
    
    def _render_numbered_slide(self, content: Dict[str, Any], active: str, bg_style: str = "") -> str:
        title = self._escape_html(content.get("title", "Steps"))
        items = content.get("items", [])
        
        items_html = "\n".join([
            f'        <li>{self._escape_html(item)}</li>' 
            for item in items
        ])
        
        return f"""
<div class="slide{active}" {bg_style}>
    <h2 class="headline">{title}</h2>
    <ol class="numbered-list">
{items_html}
    </ol>
</div>"""
    
    def _render_cards_slide(self, content: Dict[str, Any], active: str, bg_style: str = "") -> str:
        title = self._escape_html(content.get("title", ""))
        cards = content.get("cards", [])
        
        grid_class = "thirds" if len(cards) >= 3 else "halves"
        
        cards_html = "\n".join([
            f'''        <div class="card">
            <div class="card-title">{self._escape_html(c.get("title", ""))}</div>
            <div class="card-text">{self._escape_html(c.get("description", ""))}</div>
        </div>'''
            for c in cards[:3]
        ])
        
        return f"""
<div class="slide{active}" {bg_style}>
    <h2 class="headline">{title}</h2>
    <div class="{grid_class}">
{cards_html}
    </div>
</div>"""
    
    def _render_table_slide(self, content: Dict[str, Any], active: str, bg_style: str = "") -> str:
        title = self._escape_html(content.get("title", ""))
        table_data = content.get("table", [])
        
        if not table_data:
            return self._render_simple_slide({"title": title}, active, bg_style)
        
        # Get headers from first row keys
        headers = list(table_data[0].keys())
        
        header_html = "".join([f"<th>{self._escape_html(h)}</th>" for h in headers])
        
        rows_html = ""
        for row in table_data[:6]:  # Max 6 rows
            cells = "".join([f"<td>{self._escape_html(str(row.get(h, '')))}</td>" for h in headers])
            rows_html += f"        <tr>{cells}</tr>\n"
        
        return f"""
<div class="slide{active}" {bg_style}>
    <h2 class="headline">{title}</h2>
    <table class="data-table">
        <thead><tr>{header_html}</tr></thead>
        <tbody>
{rows_html}        </tbody>
    </table>
</div>"""
    
    def _render_code_slide(self, content: Dict[str, Any], active: str, bg_style: str = "") -> str:
        title = self._escape_html(content.get("title", "Code"))
        code = self._escape_html(content.get("code", "# Example"))
        
        return f"""
<div class="slide{active}" {bg_style}>
    <h2 class="headline">{title}</h2>
    <pre class="code-block">{code}</pre>
</div>"""
    
    def _render_architecture_slide(self, content: Dict[str, Any], active: str, bg_style: str = "") -> str:
        title = self._escape_html(content.get("title", "Architecture"))
        description = self._escape_html(content.get("description", ""))
        points = content.get("points", [])
        
        points_html = ""
        if points:
            points_list = "\n".join([f'        <li>{self._escape_html(p)}</li>' for p in points[:4]])
            points_html = f"""
    <ul class="bullet-list">
{points_list}
    </ul>"""
        
        desc_html = f'<p class="statement">{description}</p>' if description else ""
        
        return f"""
<div class="slide{active}" {bg_style}>
    <h2 class="headline">{title}</h2>
    {desc_html}
    {points_html}
</div>"""
    
    def _render_stats_slide(self, content: Dict[str, Any], active: str, bg_style: str = "") -> str:
        title = self._escape_html(content.get("title", "Impact"))
        stats = content.get("stats", [])
        
        stats_html = "\n".join([
            f'''        <div>
            <div class="stat-number">{self._escape_html(s.get("number", ""))}</div>
            <div class="stat-label">{self._escape_html(s.get("label", ""))}</div>
        </div>'''
            for s in stats[:3]
        ])
        
        return f"""
<div class="slide{active}" {bg_style}>
    <h2 class="headline">{title}</h2>
    <div class="stat-grid">
{stats_html}
    </div>
</div>"""
    
    def _render_cta_slide(self, content: Dict[str, Any], active: str, bg_style: str = "") -> str:
        title = self._escape_html(content.get("title", "Thank You"))
        subtitle = self._escape_html(content.get("subtitle", ""))
        
        subtitle_html = f'<p class="subhead">{subtitle}</p>' if subtitle else ""
        
        return f"""
<div class="slide{active} center" {bg_style}>
    <h1 class="headline">{title}</h1>
    {subtitle_html}
</div>"""
    
    def _render_simple_slide(self, content: Dict[str, Any], active: str, bg_style: str = "") -> str:
        title = self._escape_html(content.get("title", "Slide"))
        
        return f"""
<div class="slide{active} center" {bg_style}>
    <h1 class="headline">{title}</h1>
</div>"""
    
    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters."""
        if not isinstance(text, str):
            text = str(text)
        return (text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;"))
