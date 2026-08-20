"""
SVG Template Renderer: Loads modular CSS stylesheets and SVG component templates
to render polished telemetry cards.
"""

import math
from pathlib import Path
from string import Template
from typing import Dict, Any

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"

def load_styles() -> str:
    """Reads CSS stylesheet from templates/styles.css."""
    style_path = TEMPLATES_DIR / "styles.css"
    if style_path.exists():
        return style_path.read_text(encoding="utf-8")
    return ""

def render_stats_svg(stats: Dict[str, Any]) -> str:
    """Renders GitHub Stats SVG card using templates/stats_card.svg."""
    template_path = TEMPLATES_DIR / "stats_card.svg"
    template_content = template_path.read_text(encoding="utf-8")
    
    styles = load_styles()
    rank_level = stats.get('rank', 'B')
    percentile = stats.get('percentile', 50.0)
    
    radius = 38
    stroke_dasharray = 2 * math.pi * radius  # ~238.76
    stroke_dashoffset = (percentile / 100.0) * stroke_dasharray
    
    name = stats.get('name', 'Afonso Cruz Fernandes')
    title = f"{name}'s GitHub Stats"
    percentile_tag = f"TOP {percentile:.1f}%"
    
    mapping = {
        'title': title,
        'styles': styles,
        'stars': f"{stats.get('stars', 0):,}",
        'commits': f"{stats.get('commits', 0):,}",
        'prs': f"{stats.get('prs', 0):,}",
        'issues': f"{stats.get('issues', 0):,}",
        'repos': f"{stats.get('repos', 0):,}",
        'rank_level': rank_level,
        'percentile_tag': percentile_tag,
        'stroke_dasharray': f"{stroke_dasharray:.1f}",
        'stroke_dashoffset': f"{stroke_dashoffset:.1f}",
    }
    
    return Template(template_content).safe_substitute(mapping)

def render_languages_svg(stats: Dict[str, Any]) -> str:
    """Renders Most Used Languages SVG card using templates/languages_card.svg and templates/language_item.svg."""
    card_template_path = TEMPLATES_DIR / "languages_card.svg"
    item_template_path = TEMPLATES_DIR / "language_item.svg"
    
    card_template = card_template_path.read_text(encoding="utf-8")
    item_template = item_template_path.read_text(encoding="utf-8")
    
    styles = load_styles()
    langs = stats.get('langs', [])
    
    card_height = 80 + len(langs) * 40
    card_height_inner = card_height - 2
    
    rendered_items = []
    for idx, lang in enumerate(langs):
        y_pos = idx * 40
        pct = lang['pct']
        pct_str = f"{pct:.2f}%"
        bar_width = max(3, int((pct / 100.0) * 250))
        
        item_mapping = {
            'y_pos': str(y_pos),
            'name': lang['name'],
            'color': lang['color'],
            'pct_str': pct_str,
            'bar_width': str(bar_width)
        }
        rendered_items.append(Template(item_template).safe_substitute(item_mapping))
        
    language_items_str = "\n".join(rendered_items)
    
    card_mapping = {
        'card_height': str(card_height),
        'card_height_inner': str(card_height_inner),
        'styles': styles,
        'language_items': language_items_str
    }
    
    return Template(card_template).safe_substitute(card_mapping)
