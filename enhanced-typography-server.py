"""
Enhanced Typography MCP Server with comprehensive Bringhurst analysis.
Based on deep extraction from "The Elements of Typographic Style".
"""

from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any, Optional
import json
import re
import math

# Create the MCP server
mcp = FastMCP("Enhanced Typography Design System", dependencies=[])

# Load comprehensive typography data
with open("/Users/bengold/Documents/GitHub/MCP/Design_MCP/bringhurst_comprehensive.json", "r") as f:
    COMPREHENSIVE_DATA = json.load(f)

# Load basic principles
with open("/Users/bengold/Documents/GitHub/MCP/Design_MCP/typography_principles.json", "r") as f:
    BASIC_DATA = json.load(f)

# Typography scales (mathematical ratios)
TYPOGRAPHIC_SCALES = {
    "minor_second": 1.067,
    "major_second": 1.125, 
    "minor_third": 1.200,
    "major_third": 1.250,
    "perfect_fourth": 1.333,
    "tritone": 1.414,
    "perfect_fifth": 1.500,
    "golden_ratio": 1.618,
    "major_sixth": 1.667,
    "minor_seventh": 1.778,
    "major_seventh": 1.875,
    "octave": 2.000
}

# Page proportion systems from Bringhurst
PAGE_PROPORTIONS = {
    "1:1": {"name": "Square", "ratio": 1.0, "usage": "Rare, special purposes"},
    "6:5": {"name": "Minor Sixth", "ratio": 1.2, "usage": "Compact, wide pages"},
    "5:4": {"name": "Major Third", "ratio": 1.25, "usage": "Pleasant proportions"},
    "4:3": {"name": "Perfect Fourth", "ratio": 1.333, "usage": "Common, stable"},
    "√2:1": {"name": "ISO Standard", "ratio": 1.414, "usage": "A4, B5 paper sizes"},
    "3:2": {"name": "Perfect Fifth", "ratio": 1.5, "usage": "Harmonious, classic"},
    "φ:1": {"name": "Golden Section", "ratio": 1.618, "usage": "Natural, pleasing"},
    "5:3": {"name": "Major Sixth", "ratio": 1.667, "usage": "Elegant, tall"},
    "16:9": {"name": "Screen Standard", "ratio": 1.778, "usage": "Widescreen format"},
    "2:1": {"name": "Octave", "ratio": 2.0, "usage": "Dramatic, elongated"}
}

@mcp.tool()
def search_bringhurst_rules(
    query: str,
    category: Optional[str] = None,
    max_results: int = 10
) -> Dict[str, Any]:
    """Search through comprehensive Bringhurst rules and guidelines.
    
    Args:
        query: Search term (e.g., "spacing", "leading", "kerning")
        category: Filter by category (spacing_rules, font_guidelines, etc.)
        max_results: Maximum number of results to return
    
    Returns:
        Matching rules and guidelines from the complete text
    """
    results = {
        "query": query,
        "category_filter": category,
        "matches": [],
        "total_found": 0
    }
    
    query_lower = query.lower()
    
    # Search through detailed rules
    for rule_category, rules in COMPREHENSIVE_DATA["detailed_rules"].items():
        if category and category != rule_category:
            continue
            
        for rule in rules:
            if query_lower in rule.lower():
                results["matches"].append({
                    "category": rule_category,
                    "rule": rule.strip(),
                    "type": "detailed_rule"
                })
    
    # Search through document structure
    for section_num, section_title in COMPREHENSIVE_DATA["document_structure"]["sections"].items():
        if query_lower in section_title.lower():
            results["matches"].append({
                "section": section_num,
                "title": section_title,
                "type": "section_heading"
            })
    
    # Search through typeface recommendations
    typefaces = COMPREHENSIVE_DATA["typeface_recommendations"]
    for font_category, fonts in typefaces.items():
        if isinstance(fonts, list):
            for font in fonts:
                if query_lower in font.lower():
                    results["matches"].append({
                        "category": font_category,
                        "typeface": font,
                        "type": "typeface_recommendation"
                    })
    
    # Limit results
    results["matches"] = results["matches"][:max_results]
    results["total_found"] = len(results["matches"])
    
    return results

@mcp.tool()
def get_typeface_recommendations(
    style: str = "serif",
    usage_context: str = "body_text"
) -> Dict[str, Any]:
    """Get specific typeface recommendations from Bringhurst's analysis.
    
    Args:
        style: Font style (serif, sans_serif, script, display, monospace)
        usage_context: Usage context (body_text, headings, captions, display)
    
    Returns:
        Recommended typefaces with historical and usage context
    """
    typefaces = COMPREHENSIVE_DATA["typeface_recommendations"]
    
    style_key = f"{style}_fonts"
    if style_key not in typefaces:
        return {
            "error": f"Style '{style}' not found",
            "available_styles": list(typefaces.keys())
        }
    
    recommendations = {
        "style": style,
        "usage_context": usage_context,
        "typefaces": typefaces[style_key],
        "count": len(typefaces[style_key]),
        "usage_guidelines": {},
        "historical_notes": []
    }
    
    # Add usage guidelines based on context
    if usage_context == "body_text":
        recommendations["usage_guidelines"] = {
            "font_size": "14-16px for screen, 10-12pt for print",
            "line_height": "1.2-1.5 times font size",
            "character_count": "45-75 characters per line",
            "considerations": ["Readability over long periods", "Good x-height", "Clear letterforms"]
        }
    elif usage_context == "headings":
        recommendations["usage_guidelines"] = {
            "font_size": "Use mathematical scale ratios",
            "line_height": "1.0-1.2 times font size",
            "letter_spacing": "Slight negative spacing for large sizes",
            "considerations": ["Strong hierarchy", "Visual impact", "Complement body text"]
        }
    elif usage_context == "display":
        recommendations["usage_guidelines"] = {
            "font_size": "24px and above",
            "line_height": "Tight leading acceptable",
            "letter_spacing": "Negative spacing often beneficial",
            "considerations": ["Visual drama", "Short reading bursts", "Character personality"]
        }
    
    # Add historical context for mentioned designers
    designers = COMPREHENSIVE_DATA["historical_context"]["type_designers"]
    if designers:
        recommendations["historical_notes"] = [
            f"Referenced type designers: {', '.join(designers[:5])}",
            "These typefaces have rich historical significance in typography"
        ]
    
    return recommendations

@mcp.tool()
def analyze_page_proportions(
    page_width: float,
    page_height: float,
    unit: str = "mm"
) -> Dict[str, Any]:
    """Analyze page proportions against classical systems.
    
    Args:
        page_width: Page width
        page_height: Page height  
        unit: Measurement unit (mm, inches, px)
    
    Returns:
        Analysis of page proportions with recommendations
    """
    if page_height == 0:
        return {"error": "Page height cannot be zero"}
    
    current_ratio = page_width / page_height
    
    analysis = {
        "dimensions": {
            "width": page_width,
            "height": page_height,
            "unit": unit,
            "ratio": round(current_ratio, 3)
        },
        "proportion_analysis": {},
        "recommendations": [],
        "classical_systems": []
    }
    
    # Find closest classical proportion
    closest_proportion = None
    smallest_difference = float('inf')
    
    for proportion_name, details in PAGE_PROPORTIONS.items():
        difference = abs(current_ratio - details["ratio"])
        if difference < smallest_difference:
            smallest_difference = difference
            closest_proportion = (proportion_name, details)
        
        # Add to classical systems list
        analysis["classical_systems"].append({
            "name": details["name"],
            "ratio": details["ratio"],
            "notation": proportion_name,
            "usage": details["usage"],
            "difference": round(difference, 3)
        })
    
    # Sort by difference
    analysis["classical_systems"].sort(key=lambda x: x["difference"])
    
    if closest_proportion:
        prop_name, prop_details = closest_proportion
        analysis["proportion_analysis"] = {
            "closest_match": prop_details["name"],
            "classical_ratio": prop_details["ratio"],
            "difference": round(smallest_difference, 3),
            "percentage_off": round((smallest_difference / prop_details["ratio"]) * 100, 1)
        }
        
        if smallest_difference < 0.05:
            analysis["recommendations"].append(f"Excellent! Very close to {prop_details['name']} proportion")
        elif smallest_difference < 0.1:
            analysis["recommendations"].append(f"Good approximation of {prop_details['name']} proportion")
        else:
            analysis["recommendations"].append(f"Consider adjusting toward {prop_details['name']} proportion for better harmony")
    
    # Add Bringhurst's guidance
    if current_ratio < 1.2:
        analysis["recommendations"].append("Very wide format - consider vertical emphasis")
    elif current_ratio > 1.8:
        analysis["recommendations"].append("Very tall format - ensure adequate horizontal breathing room")
    else:
        analysis["recommendations"].append("Ratio within harmonious range for text layouts")
    
    return analysis

@mcp.tool()
def calculate_text_block_proportions(
    page_width: float,
    page_height: float,
    target_proportion: str = "golden_ratio",
    margin_style: str = "classical"
) -> Dict[str, Any]:
    """Calculate optimal text block size and margins using classical proportions.
    
    Args:
        page_width: Page width
        page_height: Page height
        target_proportion: Desired text block proportion
        margin_style: Margin calculation method (classical, modern, minimal)
    
    Returns:
        Calculated text block dimensions and margin specifications
    """
    # Get target ratio
    if target_proportion in PAGE_PROPORTIONS:
        target_ratio = PAGE_PROPORTIONS[target_proportion]["ratio"]
    elif target_proportion == "match_page":
        target_ratio = page_width / page_height
    else:
        target_ratio = 1.618  # Default to golden ratio
    
    layout = {
        "page_dimensions": {"width": page_width, "height": page_height},
        "target_proportion": target_proportion,
        "target_ratio": target_ratio,
        "text_block": {},
        "margins": {},
        "calculations": []
    }
    
    # Calculate text block using different methods
    if margin_style == "classical":
        # Classical method: 1/9 margins
        inner_margin = page_width / 9
        top_margin = page_height / 9
        
        text_width = page_width - (2 * inner_margin)
        text_height = page_height - (2 * top_margin)
        
        layout["margins"] = {
            "top": round(top_margin, 1),
            "bottom": round(top_margin, 1),
            "inner": round(inner_margin, 1),
            "outer": round(inner_margin, 1),
            "method": "Classical 1/9 system"
        }
        
    elif margin_style == "golden":
        # Golden section margins
        ratio = 1.618
        text_width = page_width / ratio
        text_height = page_height / ratio
        
        side_margin = (page_width - text_width) / 2
        vertical_margin = (page_height - text_height) / 2
        
        layout["margins"] = {
            "top": round(vertical_margin, 1),
            "bottom": round(vertical_margin, 1), 
            "inner": round(side_margin, 1),
            "outer": round(side_margin, 1),
            "method": "Golden section margins"
        }
        
    else:  # modern
        # Modern approach: 1/12 to 1/8 margins
        margin_ratio = 10  # 1/10 margins
        side_margin = page_width / margin_ratio
        vertical_margin = page_height / margin_ratio
        
        text_width = page_width - (2 * side_margin)
        text_height = page_height - (2 * vertical_margin)
        
        layout["margins"] = {
            "top": round(vertical_margin, 1),
            "bottom": round(vertical_margin, 1),
            "inner": round(side_margin, 1), 
            "outer": round(side_margin, 1),
            "method": "Modern proportional margins"
        }
    
    layout["text_block"] = {
        "width": round(text_width, 1),
        "height": round(text_height, 1),
        "ratio": round(text_width / text_height, 3),
        "area_percentage": round((text_width * text_height) / (page_width * page_height) * 100, 1)
    }
    
    # Add recommendations
    layout["recommendations"] = []
    
    actual_ratio = text_width / text_height
    if abs(actual_ratio - target_ratio) < 0.1:
        layout["recommendations"].append("Text block proportions are harmonious")
    else:
        layout["recommendations"].append(f"Consider adjusting to achieve {target_proportion} ratio")
    
    area_percentage = (text_width * text_height) / (page_width * page_height) * 100
    if 45 <= area_percentage <= 65:
        layout["recommendations"].append("Good balance of text and white space")
    elif area_percentage < 45:
        layout["recommendations"].append("Consider reducing margins for more efficient space use") 
    else:
        layout["recommendations"].append("Consider increasing margins for better readability")
    
    return layout

@mcp.tool()
def generate_baseline_grid(
    line_height: float,
    page_height: float,
    top_margin: float,
    grid_type: str = "simple"
) -> Dict[str, Any]:
    """Generate a baseline grid system for consistent vertical rhythm.
    
    Args:
        line_height: Base line height in points/pixels
        page_height: Total page height
        top_margin: Top margin size
        grid_type: Grid type (simple, modular, compound)
    
    Returns:
        Baseline grid specifications and guidelines
    """
    grid = {
        "line_height": line_height,
        "page_height": page_height,
        "top_margin": top_margin,
        "grid_type": grid_type,
        "grid_lines": [],
        "specifications": {},
        "usage_guidelines": []
    }
    
    # Calculate grid lines
    available_height = page_height - (2 * top_margin)
    line_count = int(available_height / line_height)
    
    for i in range(line_count + 1):
        baseline_position = top_margin + (i * line_height)
        grid["grid_lines"].append({
            "line_number": i,
            "position": round(baseline_position, 1),
            "from_top": round(baseline_position, 1)
        })
    
    # Grid specifications
    grid["specifications"] = {
        "total_lines": line_count,
        "line_spacing": line_height,
        "grid_height": round(line_count * line_height, 1),
        "bottom_space": round(page_height - top_margin - (line_count * line_height), 1)
    }
    
    # Different grid types
    if grid_type == "modular":
        # Add module subdivisions
        module_height = line_height * 4  # 4-line modules
        module_count = int(available_height / module_height)
        
        grid["modules"] = []
        for i in range(module_count):
            module_top = top_margin + (i * module_height)
            grid["modules"].append({
                "module_number": i + 1,
                "top": round(module_top, 1),
                "bottom": round(module_top + module_height, 1),
                "height": module_height
            })
        
        grid["specifications"]["module_count"] = module_count
        grid["specifications"]["module_height"] = module_height
        
    elif grid_type == "compound":
        # Multiple grid systems
        secondary_grid = line_height / 2  # Half-line grid
        
        grid["secondary_grid"] = {
            "line_spacing": secondary_grid,
            "usage": "For captions, small text, fine adjustments"
        }
    
    # Usage guidelines
    grid["usage_guidelines"] = [
        "Align all text baselines to grid lines",
        "Use consistent line height multiples for headings",
        "Maintain rhythm even with different font sizes",
        "Consider half-line adjustments for fine-tuning"
    ]
    
    if grid_type == "modular":
        grid["usage_guidelines"].extend([
            "Use modules for organizing content blocks",
            "Images and graphics should align to module boundaries",
            "White space should follow modular increments"
        ])
    
    return grid

# Enhanced resources with comprehensive data
@mcp.resource("typography://comprehensive-rules")
def get_comprehensive_rules() -> str:
    """Get comprehensive typography rules extracted from Bringhurst."""
    output = "# Comprehensive Typography Rules\n"
    output += "*Extracted from 200 pages of Bringhurst's masterwork*\n\n"
    
    stats = COMPREHENSIVE_DATA["extraction_stats"]
    output += f"**Source Analysis:**\n"
    output += f"- {stats['total_characters']:,} characters analyzed\n"
    output += f"- {stats['chapters_analyzed']} chapters\n" 
    output += f"- {stats['sections_analyzed']} sections\n"
    output += f"- {stats['total_rules_extracted']} detailed rules extracted\n\n"
    
    for category, rules in COMPREHENSIVE_DATA["detailed_rules"].items():
        if rules:
            output += f"## {category.replace('_', ' ').title()}\n\n"
            for rule in rules[:10]:  # Show first 10 rules per category
                output += f"• {rule.strip()}\n"
            if len(rules) > 10:
                output += f"*...and {len(rules) - 10} more rules*\n"
            output += "\n"
    
    return output

@mcp.resource("typography://typeface-library")
def get_typeface_library() -> str:
    """Get comprehensive typeface recommendations from Bringhurst."""
    typefaces = COMPREHENSIVE_DATA["typeface_recommendations"]
    
    output = "# Bringhurst's Typeface Library\n\n"
    output += "*Fonts mentioned and recommended in The Elements of Typographic Style*\n\n"
    
    output += f"## Serif Fonts ({len(typefaces['serif_fonts'])} mentioned)\n"
    for font in typefaces['serif_fonts']:
        output += f"- {font}\n"
    
    output += f"\n## Sans Serif Fonts ({len(typefaces['sans_serif_fonts'])} mentioned)\n"
    for font in typefaces['sans_serif_fonts']:
        output += f"- {font}\n"
    
    designers = COMPREHENSIVE_DATA["historical_context"]["type_designers"]
    if designers:
        output += f"\n## Referenced Type Designers\n"
        for designer in designers:
            output += f"- {designer}\n"
    
    return output

@mcp.resource("typography://page-proportions")
def get_page_proportions() -> str:
    """Get classical page proportion systems."""
    output = "# Classical Page Proportions\n\n"
    output += "*Mathematical ratios for harmonious page design*\n\n"
    
    for prop_notation, details in PAGE_PROPORTIONS.items():
        output += f"## {details['name']} ({prop_notation})\n"
        output += f"**Ratio:** {details['ratio']}\n"
        output += f"**Usage:** {details['usage']}\n\n"
    
    output += "## Bringhurst's Guidance\n\n"
    output += "- Page proportions should create harmonious relationships\n"
    output += "- Text block proportions can echo or contrast page proportions\n" 
    output += "- Classical ratios have stood the test of centuries\n"
    output += "- Golden section (φ) appears frequently in nature and art\n"
    
    return output

@mcp.prompt()
def comprehensive_typography_audit(design_type: str = "book") -> str:
    """Generate comprehensive typography audit prompt using all Bringhurst principles."""
    return f"""Conduct a comprehensive typography audit for this {design_type} using Robert Bringhurst's complete methodology from "The Elements of Typographic Style."

## Comprehensive Analysis Framework

### 1. Rhythm & Proportion
**Horizontal Motion:**
- Line length (measure): 45-75 characters optimal, 65-66 ideal
- Letter spacing and kerning appropriateness
- Word spacing consistency and texture

**Vertical Motion:**
- Leading ratios: 1.2-1.5 for body text, 1.0-1.2 for headings
- Baseline grid alignment and consistency
- Vertical space intervals and rhythm

### 2. Harmony & Counterpoint
**Size Relationships:**
- Mathematical scale progression (minor third, golden ratio, etc.)
- Consistent type size hierarchy
- Appropriate size for reading distance and context

**Font Mixing:**
- Maximum 2-3 type families
- Harmonious weight and style combinations
- Clear functional distinctions

### 3. Structural Forms & Devices
**Typography Mechanics:**
- Proper dash usage (em, en, hyphen)
- Correct quotation marks and apostrophes
- Appropriate ligature usage
- Small caps for abbreviations

### 4. Analphabetic Symbols
**Numbers & Symbols:**
- Text figures vs. titling figures usage
- Mathematical notation correctness
- Proper fraction formatting
- Symbol consistency and spacing

### 5. Page Architecture
**Layout Systems:**
- Page proportion analysis (golden section, classical ratios)
- Text block proportions and positioning
- Margin relationships and white space
- Grid system consistency

### 6. Typeface Evaluation
**Historical Appropriateness:**
- Typeface choice for content and context
- Cultural and period considerations
- Technical quality assessment

### 7. Technical Excellence
**Craft Standards:**
- Hyphenation and line breaking quality
- Paragraph formatting consistency
- Hierarchical clarity and navigation
- Overall typographic color and texture

## Analysis Deliverables
For each section, provide:
1. Current state assessment
2. Specific issues identified
3. Prioritized recommendations
4. Implementation guidance

Use Bringhurst's principle: "Typography exists to honor content."
Base all recommendations on the extracted rules and guidelines from the complete text analysis."""

if __name__ == "__main__":
    mcp.run()