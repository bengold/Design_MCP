#!/usr/bin/env python3
"""
Standalone demo of typography analysis tools based on Bringhurst's principles.
"""

import json
import re
import math

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

def calculate_optimal_line_height(font_size, text_type="body"):
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

def analyze_typography(text, font_size=16, line_height=None, line_length_chars=None):
    """Analyze typography for readability and adherence to Bringhurst principles."""
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
    
    return analysis

def generate_typographic_scale(base_size=16, scale_name="major_third", levels=6):
    """Generate a harmonious typographic scale using mathematical ratios."""
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

def print_header(title):
    print(f"\n{'='*60}")
    print(f"📝 {title}")
    print('='*60)

def main():
    print("📚 Typography Analysis Demo")
    print("Based on 'The Elements of Typographic Style' by Robert Bringhurst")
    
    # Test 1: Analyze sample typography
    print_header("1. Typography Analysis")
    sample_text = """Typography is the craft of endowing human language with a durable visual form, and thus with an independent existence. Its heartwood is calligraphy – the dance, on a tiny stage, of the living, speaking hand – and its roots reach into living soil, though its branches may be hung each year with new machines."""
    
    analysis = analyze_typography(
        text=sample_text,
        font_size=16,
        line_height=24,
        line_length_chars=68
    )
    
    print(f"📊 Font size: {analysis['font_size']}px")
    print(f"📏 Line length: {analysis['line_length_chars']} characters")
    print(f"📐 Line height: {analysis['line_height']}px (ratio: {analysis['analysis']['line_height']['ratio']})")
    print(f"✅ Line length: {analysis['analysis']['line_length']['grade']} - {analysis['analysis']['line_length']['message']}")
    print(f"✅ Line height: {analysis['analysis']['line_height']['grade']} - {analysis['analysis']['line_height']['message']}")
    
    # Test 2: Generate typographic scale
    print_header("2. Typographic Scale Generation")
    scale = generate_typographic_scale(
        base_size=16,
        scale_name="major_third",
        levels=6
    )
    
    print(f"📐 Scale: {scale['scale_name']} (ratio: {scale['ratio']})")
    print(f"🎯 Base size: {scale['base_size']}px")
    print("\nGenerated sizes:")
    for level, details in scale['sizes'].items():
        print(f"  {level}: {details['size']}px - {details['usage']}")
    
    # Test 3: Compare different scales
    print_header("3. Typographic Scale Comparison")
    
    scales_to_compare = ["minor_third", "major_third", "perfect_fourth", "golden_ratio"]
    
    for scale_name in scales_to_compare:
        scale = generate_typographic_scale(16, scale_name, 4)
        sizes = [str(details['size']) for details in scale['sizes'].values()]
        print(f"📐 {scale_name.replace('_', ' ').title()} ({scale['ratio']}): {' → '.join(sizes)}")
    
    # Test 4: Analyze different line lengths
    print_header("4. Line Length Analysis")
    
    test_cases = [
        {"chars": 35, "description": "Too short"},
        {"chars": 55, "description": "Good range"},
        {"chars": 65, "description": "Ideal"},
        {"chars": 85, "description": "Too long"}
    ]
    
    for case in test_cases:
        analysis = analyze_typography("Sample text", line_length_chars=case["chars"])
        grade = analysis["analysis"]["line_length"]["grade"]
        print(f"📏 {case['chars']} chars ({case['description']}): {grade}")
    
    # Test 5: Show Bringhurst principles
    print_header("5. Bringhurst's Core Principles")
    
    for category, details in TYPOGRAPHY_DATA["principles"].items():
        print(f"\n🎯 {category.replace('_', ' ').title()}")
        print(f"   {details['description']}")
        for rule in details['rules'][:2]:  # Show first 2 rules
            print(f"   • {rule}")
    
    print_header("Analysis Complete! 🎉")
    print("Key typography insights:")
    print("• Optimal line length: 45-75 characters (ideal: 65-66)")
    print("• Line height ratio: 1.2-1.5 for body text")
    print("• Use mathematical scales for harmonious sizing")
    print("• Honor the reader through thoughtful typography")
    print(f"\nBased on {len(TYPOGRAPHY_DATA['principles'])} core principles from Bringhurst")

if __name__ == "__main__":
    main()