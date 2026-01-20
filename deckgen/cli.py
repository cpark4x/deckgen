"""Command-line interface for deckgen."""

import sys
import webbrowser
from pathlib import Path
from typing import List, Optional

import click

from .core.orchestrator import DeckOrchestrator
from .core.designer import ThemeDesigner


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Generate beautiful HTML presentations from context."""
    pass


@cli.command()
@click.argument("description")
@click.option(
    "--file",
    "-f",
    "files",
    multiple=True,
    help="Input file(s) for additional context",
)
@click.option(
    "--theme",
    "-t",
    help="Force specific theme (keynote-minimalist, technical-blueprint)",
)
@click.option("--output", "-o", help="Output filename")
@click.option("--no-open", is_flag=True, help="Don't open browser automatically")
def create(
    description: str,
    files: tuple,
    theme: Optional[str],
    output: Optional[str],
    no_open: bool,
):
    """Create a presentation from context.
    
    Examples:
    
        deckgen create "about shadow environments"
        
        deckgen create "API redesign" --file spec.md --theme technical
        
        deckgen create "Q4 results" --output results.html
    """
    click.echo(f"Creating deck: {description}")
    
    # Convert theme name if needed (allow hyphens)
    if theme:
        theme = theme.replace("-", "_")
    
    # Create orchestrator and generate deck
    orchestrator = DeckOrchestrator()
    
    try:
        output_path = orchestrator.create_deck(
            description=description,
            files=list(files) if files else None,
            theme=theme,
            output_path=output,
        )
        
        click.echo(f"✓ Deck created: {output_path}")
        
        # Open in browser unless --no-open
        if not no_open:
            click.echo("Opening in browser...")
            webbrowser.open(f"file://{output_path}")
        
    except Exception as e:
        click.echo(f"✗ Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
def list_themes():
    """List available themes."""
    designer = ThemeDesigner()
    themes = designer.list_themes()
    
    click.echo("\nAvailable Themes:\n")
    
    for theme in themes:
        name = theme["display_name"]
        desc = theme["description"]
        best_for = theme["best_for"]
        
        click.echo(f"  {name}")
        click.echo(f"    {desc}")
        if best_for:
            click.echo(f"    Best for: {best_for}")
        click.echo()


@cli.command()
@click.argument("theme_name")
def theme_info(theme_name: str):
    """Show details about a theme."""
    designer = ThemeDesigner()
    theme_name_normalized = theme_name.replace("-", "_")
    
    theme = designer.get_theme_info(theme_name_normalized)
    
    if not theme:
        click.echo(f"✗ Theme '{theme_name}' not found", err=True)
        click.echo("\nRun 'deckgen list-themes' to see available themes.")
        sys.exit(1)
    
    click.echo(f"\nTheme: {theme_name}")
    click.echo(f"Description: {theme.get('description', 'No description')}")
    click.echo(f"\nColors:")
    
    colors = theme.get("colors", {})
    for key, value in colors.items():
        click.echo(f"  {key}: {value}")
    
    click.echo(f"\nTypography:")
    typography = theme.get("typography", {})
    for key, value in typography.items():
        click.echo(f"  {key}: {value}")
    
    click.echo()


if __name__ == "__main__":
    cli()
