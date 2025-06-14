"""
Typography MCP Server based on "The Elements of Typographic Style" by Robert Bringhurst.
Provides tools for typography analysis, validation, and guidance.
"""

from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any, Optional
import json
import re
import math

# Create the MCP server
mcp = FastMCP("Typography Design Rules", dependencies=[])

# Load typography principles
with open("/Users/bengold/Documents/GitHub/MCP/Design_MCP/typography_principles.json", "r") as f:
    TYPOGRAPHY_DATA = json.load(f)

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

def calculate_line_length_characters(text: str) -> int:
    """Calculate the character count of a line of text."""
    return len(text.strip())

def calculate_optimal_line_height(font_size: float, text_type: str = "body") -> Dict[str, float]:
    """Calculate optimal line height based on font size and text type."""
    if text_type == "body":
        min_ratio, max_ratio = 1.2, 1.5
        ideal_ratio = 1.4
    elif text_type == "heading":
        min_ratio, max_ratio = 1.0, 1.2
        ideal_ratio = 1.1
    elif text_type == "caption":
        min_ratio, max_ratio = 1.3, 1.6
        ideal_ratio = 1.45
    else:
        min_ratio, max_ratio = 1.2, 1.5
        ideal_ratio = 1.4
    
    return {
        "minimum": font_size * min_ratio,
        "maximum": font_size * max_ratio,
        "ideal": font_size * ideal_ratio,
        "ratio_range": f"{min_ratio}-{max_ratio}"
    }

@mcp.tool()
def analyze_typography(
    text: str,
    font_size: float = 16,
    line_height: Optional[float] = None,
    line_length_chars: Optional[int] = None
) -> Dict[str, Any]:
    """Analyze typography for readability and adherence to Bringhurst principles.
    
    Args:
        text: Sample text to analyze
        font_size: Font size in pixels/points
        line_height: Line height in pixels/points (optional)
        line_length_chars: Characters per line (optional, calculated from text if not provided)
    
    Returns:
        Comprehensive typography analysis with recommendations
    """
    analysis = {
        "text_sample": text[:100] + "..." if len(text) > 100 else text,
        "font_size": font_size,
        "analysis": {}
    }
    
    # Line length analysis
    if line_length_chars is None:
        lines = text.split('\n')
        if lines:
            line_length_chars = max(len(line) for line in lines)
    
    analysis["line_length_chars"] = line_length_chars
    
    # Evaluate line length
    if line_length_chars < 45:
        line_length_grade = "TOO_SHORT"
        line_length_message = "Lines are too short, may cause choppy reading rhythm"
    elif line_length_chars <= 75:
        if 65 <= line_length_chars <= 66:
            line_length_grade = "EXCELLENT"
            line_length_message = "Ideal line length for optimal readability"
        else:
            line_length_grade = "GOOD" 
            line_length_message = "Good line length within optimal range"
    else:
        line_length_grade = "TOO_LONG"
        line_length_message = "Lines are too long, may cause reader fatigue"
    
    analysis["analysis"]["line_length"] = {
        "grade": line_length_grade,
        "message": line_length_message,
        "optimal_range": "45-75 characters",
        "ideal": "65-66 characters"
    }
    
    # Line height analysis
    if line_height:
        analysis["line_height"] = line_height
        ratio = line_height / font_size
        optimal = calculate_optimal_line_height(font_size, "body")
        
        if optimal["minimum"] <= line_height <= optimal["maximum"]:
            if abs(line_height - optimal["ideal"]) <= 2:
                line_height_grade = "EXCELLENT"
                line_height_message = "Ideal line height for readability"
            else:
                line_height_grade = "GOOD"
                line_height_message = "Good line height within optimal range"
        elif line_height < optimal["minimum"]:
            line_height_grade = "TOO_TIGHT"
            line_height_message = "Leading too tight, may impair readability"
        else:
            line_height_grade = "TOO_LOOSE"
            line_height_message = "Leading too loose, may break text cohesion"
        
        analysis["analysis"]["line_height"] = {
            "grade": line_height_grade,
            "message": line_height_message,
            "ratio": round(ratio, 2),
            "optimal_range": optimal["ratio_range"],
            "recommended": round(optimal["ideal"], 1)
        }
    
    # Text rhythm analysis
    words = text.split()
    avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
    
    analysis["analysis"]["text_rhythm"] = {
        "average_word_length": round(avg_word_length, 1),
        "word_count": len(words),
        "character_count": len(text),
        "rhythm_grade": "GOOD" if 4 <= avg_word_length <= 6 else "NEEDS_ATTENTION"
    }
    
    return analysis

@mcp.tool()
def generate_typographic_scale(
    base_size: float = 16,
    scale_name: str = "major_third",
    levels: int = 6
) -> Dict[str, Any]:
    """Generate a harmonious typographic scale using mathematical ratios.
    
    Args:
        base_size: Base font size in pixels/points
        scale_name: Scale type (minor_third, major_third, perfect_fourth, golden_ratio, etc.)
        levels: Number of scale levels to generate
    
    Returns:
        Typography scale with sizes and usage recommendations
    """
    if scale_name not in TYPOGRAPHIC_SCALES:
        return {
            "error": f"Unknown scale '{scale_name}'",
            "available_scales": list(TYPOGRAPHIC_SCALES.keys())
        }
    
    ratio = TYPOGRAPHIC_SCALES[scale_name]
    scale = {
        "base_size": base_size,
        "scale_name": scale_name,
        "ratio": ratio,
        "sizes": {}
    }
    
    # Generate scale sizes
    for i in range(-2, levels - 1):
        size = base_size * (ratio ** i)
        level_name = f"level_{i + 3}" if i >= -2 else f"level_small_{abs(i)}"
        
        # Add usage recommendations
        if i == -2:
            usage = "Small captions, fine print"
        elif i == -1:
            usage = "Captions, metadata"
        elif i == 0:
            usage = "Body text (base)"
        elif i == 1:
            usage = "Subheadings, lead paragraphs"
        elif i == 2:
            usage = "Section headings"
        elif i == 3:
            usage = "Page titles, major headings"
        else:
            usage = "Display text, hero headings"
        
        scale["sizes"][level_name] = {
            "size": round(size, 1),
            "usage": usage,
            "line_height_recommendation": calculate_optimal_line_height(
                size, "heading" if i > 0 else "body"
            )["ideal"]
        }
    
    return scale

@mcp.tool()
def validate_typography_rules(
    font_family: str,
    font_size: float,
    line_height: float,
    line_length_chars: int,
    letter_spacing: Optional[float] = None,
    context: str = "body_text"
) -> Dict[str, Any]:
    """Validate typography against Bringhurst's rules and best practices.
    
    Args:
        font_family: Font family name
        font_size: Font size in pixels/points
        line_height: Line height in pixels/points
        line_length_chars: Characters per line
        letter_spacing: Letter spacing in em units (optional)
        context: Text context (body_text, heading, caption, display)
    
    Returns:
        Validation results with pass/fail for each rule
    """
    validation = {
        "input": {
            "font_family": font_family,
            "font_size": font_size,
            "line_height": line_height,
            "line_length_chars": line_length_chars,
            "letter_spacing": letter_spacing,
            "context": context
        },
        "rules": {},
        "overall_grade": "PASS",
        "score": 0,
        "max_score": 0
    }
    
    # Rule 1: Line length (measure)
    validation["max_score"] += 1
    if 45 <= line_length_chars <= 75:
        validation["rules"]["line_length"] = {
            "status": "PASS",
            "message": "Line length within optimal range",
            "points": 1
        }
        validation["score"] += 1
    else:
        validation["rules"]["line_length"] = {
            "status": "FAIL", 
            "message": f"Line length {line_length_chars} chars outside optimal range (45-75)",
            "points": 0
        }
    
    # Rule 2: Line height ratio
    validation["max_score"] += 1
    ratio = line_height / font_size
    optimal_range = (1.2, 1.5) if context == "body_text" else (1.0, 1.2)
    
    if optimal_range[0] <= ratio <= optimal_range[1]:
        validation["rules"]["line_height_ratio"] = {
            "status": "PASS",
            "message": f"Line height ratio {ratio:.2f} is appropriate for {context}",
            "points": 1
        }
        validation["score"] += 1
    else:
        validation["rules"]["line_height_ratio"] = {
            "status": "FAIL",
            "message": f"Line height ratio {ratio:.2f} outside optimal range {optimal_range}",
            "points": 0
        }
    
    # Rule 3: Font size appropriateness
    validation["max_score"] += 1
    if context == "body_text":
        size_range = (14, 18)  # For screen reading
    elif context == "caption":
        size_range = (12, 14)
    elif context == "heading":
        size_range = (18, 48)
    else:  # display
        size_range = (24, 96)
    
    if size_range[0] <= font_size <= size_range[1]:
        validation["rules"]["font_size"] = {
            "status": "PASS",
            "message": f"Font size {font_size}px appropriate for {context}",
            "points": 1
        }
        validation["score"] += 1
    else:
        validation["rules"]["font_size"] = {
            "status": "FAIL", 
            "message": f"Font size {font_size}px outside recommended range {size_range} for {context}",
            "points": 0
        }
    
    # Rule 4: Letter spacing (if provided)
    if letter_spacing is not None:
        validation["max_score"] += 1
        if context in ["heading", "display"] and letter_spacing < 0:
            validation["rules"]["letter_spacing"] = {
                "status": "PASS",
                "message": "Negative letter spacing appropriate for large text",
                "points": 1
            }
            validation["score"] += 1
        elif context == "body_text" and -0.02 <= letter_spacing <= 0.02:
            validation["rules"]["letter_spacing"] = {
                "status": "PASS", 
                "message": "Letter spacing appropriate for body text",
                "points": 1
            }
            validation["score"] += 1
        else:
            validation["rules"]["letter_spacing"] = {
                "status": "FAIL",
                "message": "Letter spacing may not be optimal for this context",
                "points": 0
            }
    
    # Calculate overall grade
    score_percentage = (validation["score"] / validation["max_score"]) * 100
    if score_percentage >= 80:
        validation["overall_grade"] = "EXCELLENT"
    elif score_percentage >= 60:
        validation["overall_grade"] = "GOOD"
    elif score_percentage >= 40:
        validation["overall_grade"] = "NEEDS_IMPROVEMENT"
    else:
        validation["overall_grade"] = "POOR"
    
    validation["score_percentage"] = round(score_percentage, 1)
    
    return validation

@mcp.tool()
def suggest_typography_improvements(
    current_font_size: float,
    current_line_height: float,
    current_line_length: int,
    text_type: str = "body_text",
    target_readability: str = "optimal"
) -> Dict[str, Any]:
    """Suggest typography improvements based on Bringhurst principles.
    
    Args:
        current_font_size: Current font size
        current_line_height: Current line height
        current_line_length: Current line length in characters
        text_type: Type of text (body_text, heading, caption)
        target_readability: Target level (minimal, good, optimal, excellent)
    
    Returns:
        Specific improvement suggestions with before/after values
    """
    suggestions = {
        "current": {
            "font_size": current_font_size,
            "line_height": current_line_height,
            "line_length": current_line_length,
            "text_type": text_type
        },
        "improvements": [],
        "recommended": {}
    }
    
    # Line length improvements
    if current_line_length < 45:
        suggestions["improvements"].append({
            "area": "Line Length",
            "issue": "Lines too short for comfortable reading",
            "recommendation": "Increase column width or decrease font size",
            "target_range": "45-75 characters",
            "priority": "HIGH"
        })
    elif current_line_length > 75:
        suggestions["improvements"].append({
            "area": "Line Length", 
            "issue": "Lines too long, may cause reading fatigue",
            "recommendation": "Decrease column width or increase font size",
            "target_range": "45-75 characters",
            "priority": "HIGH"
        })
    
    # Calculate optimal values
    optimal_line_height = calculate_optimal_line_height(current_font_size, text_type)
    
    # Line height improvements
    current_ratio = current_line_height / current_font_size
    if current_ratio < 1.2:
        suggestions["improvements"].append({
            "area": "Line Height",
            "issue": "Leading too tight, text may feel cramped",
            "recommendation": f"Increase line height to at least {optimal_line_height['minimum']:.1f}",
            "current_ratio": current_ratio,
            "target_ratio": optimal_line_height["ratio_range"],
            "priority": "MEDIUM"
        })
    elif current_ratio > 1.6:
        suggestions["improvements"].append({
            "area": "Line Height",
            "issue": "Leading too loose, may break text cohesion", 
            "recommendation": f"Decrease line height to around {optimal_line_height['ideal']:.1f}",
            "current_ratio": current_ratio,
            "target_ratio": optimal_line_height["ratio_range"],
            "priority": "MEDIUM"
        })
    
    # Font size recommendations based on readability target
    if target_readability == "excellent" and text_type == "body_text":
        if current_font_size < 16:
            suggestions["improvements"].append({
                "area": "Font Size",
                "issue": "Font size may be too small for excellent readability",
                "recommendation": "Consider increasing to 16-18px for better accessibility",
                "target_range": "16-18px",
                "priority": "MEDIUM"
            })
    
    # Provide specific recommended values
    suggestions["recommended"] = {
        "font_size": current_font_size if text_type == "body_text" and 14 <= current_font_size <= 18 else 16,
        "line_height": optimal_line_height["ideal"],
        "line_length_range": "45-75 characters",
        "line_length_ideal": "65-66 characters"
    }
    
    # Overall assessment
    if not suggestions["improvements"]:
        suggestions["assessment"] = "Typography looks good! Minor fine-tuning may still be beneficial."
    elif len(suggestions["improvements"]) <= 2:
        suggestions["assessment"] = "Good foundation with some areas for improvement."
    else:
        suggestions["assessment"] = "Several typography improvements recommended for better readability."
    
    return suggestions

@mcp.tool()
def calculate_reading_metrics(
    text: str,
    font_size: float,
    line_height: float,
    words_per_minute: int = 200
) -> Dict[str, Any]:
    """Calculate reading metrics and estimated reading time.
    
    Args:
        text: Text content to analyze
        font_size: Font size in pixels/points
        line_height: Line height in pixels/points
        words_per_minute: Average reading speed (default 200 WPM)
    
    Returns:
        Reading metrics including time estimates and text statistics
    """
    words = text.split()
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    metrics = {
        "text_statistics": {
            "character_count": len(text),
            "word_count": len(words),
            "sentence_count": len(sentences),
            "average_word_length": round(sum(len(word) for word in words) / len(words), 1) if words else 0,
            "average_sentence_length": round(len(words) / len(sentences), 1) if sentences else 0
        },
        "typography_metrics": {
            "font_size": font_size,
            "line_height": line_height,
            "line_height_ratio": round(line_height / font_size, 2),
            "estimated_lines": 0,
            "estimated_height_px": 0
        },
        "reading_estimates": {
            "reading_time_minutes": round(len(words) / words_per_minute, 1),
            "reading_time_seconds": round((len(words) / words_per_minute) * 60),
            "words_per_minute": words_per_minute
        }
    }
    
    # Estimate layout metrics (rough approximation)
    avg_chars_per_line = 65  # Assuming optimal line length
    estimated_lines = len(text) / avg_chars_per_line
    metrics["typography_metrics"]["estimated_lines"] = round(estimated_lines)
    metrics["typography_metrics"]["estimated_height_px"] = round(estimated_lines * line_height)
    
    # Reading difficulty assessment (basic)
    avg_word_len = metrics["text_statistics"]["average_word_length"]
    avg_sentence_len = metrics["text_statistics"]["average_sentence_length"]
    
    if avg_word_len <= 4.5 and avg_sentence_len <= 15:
        difficulty = "Easy"
    elif avg_word_len <= 5.5 and avg_sentence_len <= 20:
        difficulty = "Moderate"
    else:
        difficulty = "Challenging"
    
    metrics["reading_estimates"]["difficulty_level"] = difficulty
    
    return metrics

# Resources for typography guidance
@mcp.resource("typography://bringhurst-principles")
def get_bringhurst_principles() -> str:
    """Get Robert Bringhurst's core typography principles."""
    output = "# The Elements of Typographic Style - Core Principles\n\n"
    output += "*Based on Robert Bringhurst's seminal work*\n\n"
    
    for category, details in TYPOGRAPHY_DATA["principles"].items():
        output += f"## {category.replace('_', ' ').title()}\n\n"
        output += f"**{details['description']}**\n\n"
        
        for rule in details['rules']:
            output += f"- {rule}\n"
        output += "\n"
    
    return output

@mcp.resource("typography://measurements-guide") 
def get_measurements_guide() -> str:
    """Get typography measurements and guidelines."""
    output = "# Typography Measurements & Guidelines\n\n"
    output += "*Professional standards for digital and print typography*\n\n"
    
    for category, details in TYPOGRAPHY_DATA["measurements"].items():
        output += f"## {category.replace('_', ' ').title()}\n\n"
        
        for key, value in details.items():
            output += f"**{key.replace('_', ' ').title()}**: {value}\n\n"
    
    return output

@mcp.resource("typography://scales-reference")
def get_typographic_scales() -> str:
    """Get reference for typographic scales and ratios."""
    output = "# Typographic Scales Reference\n\n"
    output += "*Mathematical ratios for harmonious typography*\n\n"
    
    for scale_name, ratio in TYPOGRAPHIC_SCALES.items():
        # Generate example sizes for 16px base
        base = 16
        sizes = [round(base * (ratio ** i), 1) for i in range(-1, 4)]
        
        output += f"## {scale_name.replace('_', ' ').title()}\n"
        output += f"**Ratio**: {ratio}\n"
        output += f"**Example sizes** (base 16px): {' → '.join(map(str, sizes))}\n\n"
    
    output += "\n## Usage Guidelines\n\n"
    output += "- **Minor Third (1.200)**: Subtle, elegant progression\n"
    output += "- **Major Third (1.250)**: Balanced, versatile scale\n"
    output += "- **Perfect Fourth (1.333)**: Strong hierarchy, good contrast\n"
    output += "- **Golden Ratio (1.618)**: Classic proportions, natural harmony\n"
    output += "- **Perfect Fifth (1.500)**: Bold, dramatic scale\n"
    
    return output

@mcp.prompt()
def typography_review_prompt(design_context: str = "website") -> str:
    """Generate a prompt for reviewing typography in design work."""
    return f"""Please review the typography in this {design_context} design based on Robert Bringhurst's principles from "The Elements of Typographic Style."

Analyze the following aspects:

## Rhythm and Proportion
- **Line length (measure)**: Is it within the optimal 45-75 character range?
- **Line height (leading)**: Does it create good vertical rhythm?
- **Letter spacing**: Is it appropriate for the font size and style?
- **Word spacing**: Does it create even text color and texture?

## Hierarchy and Scale
- **Font size relationships**: Do they follow a mathematical scale?
- **Visual hierarchy**: Is it clear and logical?
- **Typographic contrast**: Are different levels distinct but harmonious?

## Technical Excellence
- **Font choice**: Is it appropriate for the medium and audience?
- **Alignment**: Is it consistent and purposeful?
- **Character details**: Are proper quotes, dashes, and symbols used?

## Readability Factors
- **Comfort**: Can users read for extended periods without strain?
- **Accessibility**: Does it meet readability standards?
- **Context**: Is it appropriate for the intended use?

Provide specific recommendations for improvement, citing Bringhurst's principles where applicable."""

if __name__ == "__main__":
    mcp.run()