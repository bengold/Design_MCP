#!/usr/bin/env python3
"""
Demo script for the Typography MCP Server based on Bringhurst's principles.
"""

import sys
import os

# Import the tools directly by loading the server module
exec(open("/Users/bengold/Documents/GitHub/MCP/Design_MCP/typography-mcp-server.py").read())

def print_header(title):
    print(f"\n{'='*60}")
    print(f"📝 {title}")
    print('='*60)

def print_section(title):
    print(f"\n📋 {title}")
    print('-' * 40)

def main():
    print("📚 Typography MCP Server Demo")
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
    
    # Test 3: Validate typography rules
    print_header("3. Typography Rules Validation")
    validation = validate_typography_rules(
        font_family="Georgia",
        font_size=16,
        line_height=24,
        line_length_chars=68,
        letter_spacing=0.01,
        context="body_text"
    )
    
    print(f"🎯 Overall Grade: {validation['overall_grade']}")
    print(f"📊 Score: {validation['score']}/{validation['max_score']} ({validation['score_percentage']}%)")
    print("\nRule validation:")
    for rule, details in validation['rules'].items():
        status_emoji = "✅" if details['status'] == "PASS" else "❌"
        print(f"  {status_emoji} {rule}: {details['message']}")
    
    # Test 4: Typography improvements
    print_header("4. Typography Improvement Suggestions")
    
    # Test with problematic typography
    improvements = suggest_typography_improvements(
        current_font_size=12,  # Too small
        current_line_height=14, # Too tight
        current_line_length=85, # Too long
        text_type="body_text",
        target_readability="optimal"
    )
    
    print(f"📊 Assessment: {improvements['assessment']}")
    print(f"🔧 Improvements needed: {len(improvements['improvements'])}")
    
    for improvement in improvements['improvements']:
        priority_emoji = "🔴" if improvement['priority'] == "HIGH" else "🟡"
        print(f"\n{priority_emoji} {improvement['area']} ({improvement['priority']})")
        print(f"   Issue: {improvement['issue']}")
        print(f"   Fix: {improvement['recommendation']}")
    
    print(f"\n💡 Recommended values:")
    for key, value in improvements['recommended'].items():
        print(f"   {key}: {value}")
    
    # Test 5: Reading metrics
    print_header("5. Reading Metrics Analysis")
    
    long_text = """Typography exists to honor content. Like typography, the aim of design is to clarify and order the written word, or any content intended to be read. Design gives text structure and hierarchy. It provides the road map that guides the reader through information. Typography is an essential tool for both objectives. Typography is writing with visual form. It gives written language a visual counterpart. Like writing, it can be clear or unclear, energetic or plain, overly elaborate or beautifully simple. Like writing, typography has both vernacular and more elevated forms."""
    
    metrics = calculate_reading_metrics(
        text=long_text,
        font_size=16,
        line_height=24,
        words_per_minute=200
    )
    
    print(f"📊 Text Statistics:")
    stats = metrics['text_statistics']
    print(f"   Words: {stats['word_count']}")
    print(f"   Characters: {stats['character_count']}")
    print(f"   Sentences: {stats['sentence_count']}")
    print(f"   Avg word length: {stats['average_word_length']} characters")
    print(f"   Avg sentence length: {stats['average_sentence_length']} words")
    
    print(f"\n⏱️  Reading Estimates:")
    reading = metrics['reading_estimates']
    print(f"   Reading time: {reading['reading_time_minutes']} minutes")
    print(f"   Difficulty: {reading['difficulty_level']}")
    print(f"   Reading speed: {reading['words_per_minute']} WPM")
    
    print(f"\n📐 Layout Estimates:")
    layout = metrics['typography_metrics']
    print(f"   Estimated lines: {layout['estimated_lines']}")
    print(f"   Estimated height: {layout['estimated_height_px']}px")
    
    # Test 6: Compare different scales
    print_header("6. Typographic Scale Comparison")
    
    scales_to_compare = ["minor_third", "major_third", "perfect_fourth", "golden_ratio"]
    
    for scale_name in scales_to_compare:
        scale = generate_typographic_scale(16, scale_name, 4)
        sizes = [details['size'] for details in scale['sizes'].values()]
        print(f"📐 {scale_name.replace('_', ' ').title()} ({scale['ratio']}): {' → '.join(map(str, sizes))}")
    
    print_header("Demo Complete! 🎉")
    print("The Typography MCP server provides:")
    print("• 5 typography analysis and validation tools")
    print("• 3 comprehensive resources based on Bringhurst's work")
    print("• Mathematical typographic scales and ratios")
    print("• Reading metrics and improvement suggestions")
    print("• Professional typography validation rules")
    print("\nStart the server with: uv run mcp dev typography-mcp-server.py")

if __name__ == "__main__":
    main()