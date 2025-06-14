#!/usr/bin/env python3
"""
Deep analysis of Bringhurst's "The Elements of Typographic Style" PDF.
Extract comprehensive typography rules, techniques, and detailed guidance.
"""

try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

import re
import json
from collections import defaultdict

def extract_full_text_from_pdf(pdf_path, max_pages=None):
    """Extract complete text from PDF file."""
    if not PDF_AVAILABLE:
        return "PyPDF2 not available for PDF processing"
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            total_pages = len(pdf_reader.pages)
            
            if max_pages is None:
                max_pages = total_pages
            
            print(f"📖 Extracting from {min(max_pages, total_pages)} of {total_pages} pages...")
            
            for page_num in range(min(max_pages, total_pages)):
                if page_num % 20 == 0:
                    print(f"   Processing page {page_num + 1}...")
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
            
            return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def extract_detailed_rules(text):
    """Extract detailed typography rules and guidelines from the text."""
    rules = {
        "spacing_rules": [],
        "font_guidelines": [],
        "punctuation_rules": [],
        "layout_principles": [],
        "historical_context": [],
        "technical_specifications": [],
        "design_examples": [],
        "measurement_standards": []
    }
    
    # Patterns to look for specific typography rules
    patterns = {
        "spacing": [
            r"space[s]?\s+(?:between|around|before|after)\s+([^.]+)",
            r"(?:leading|line\s+height|interline\s+space)\s+(?:should|must|is)\s+([^.]+)",
            r"(?:letter\s+spacing|tracking|kerning)\s+(?:of|for|should)\s+([^.]+)",
            r"(?:word\s+spacing|inter\s*word)\s+(?:should|must|is)\s+([^.]+)"
        ],
        "measurements": [
            r"(\d+(?:\.\d+)?\s*(?:pt|px|em|%|mm|inches?))\s+(?:for|of|in)\s+([^.]+)",
            r"(?:measure|line\s+length|column\s+width)\s+(?:of|should\s+be)\s+([^.]+)",
            r"(?:x-height|cap\s+height|ascender|descender)\s+(?:of|should|is)\s+([^.]+)"
        ],
        "font_usage": [
            r"(?:use|choose|select)\s+([^.]+?)\s+(?:for|when|in)\s+([^.]+)",
            r"(?:serif|sans\s*serif|italic|bold|roman)\s+(?:fonts?|typefaces?)\s+(?:are|should)\s+([^.]+)",
            r"(?:font\s+size|type\s+size)\s+(?:of|should|for)\s+([^.]+)"
        ],
        "punctuation": [
            r"(?:quotation\s+marks?|quotes?|apostrophes?)\s+(?:should|must|are)\s+([^.]+)",
            r"(?:em\s+dash|en\s+dash|hyphen)\s+(?:is|should|for)\s+([^.]+)",
            r"(?:ellipsis|periods?)\s+(?:should|must|are)\s+([^.]+)"
        ]
    }
    
    # Extract rules using patterns
    category_mapping = {
        "spacing": "spacing_rules",
        "measurements": "measurement_standards", 
        "font_usage": "font_guidelines",
        "punctuation": "punctuation_rules"
    }
    
    for category, pattern_list in patterns.items():
        rule_category = category_mapping.get(category, f"{category}_rules")
        if rule_category not in rules:
            rules[rule_category] = []
            
        for pattern in pattern_list:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    rule = " ".join(match).strip()
                else:
                    rule = match.strip()
                
                if len(rule) > 10 and len(rule) < 200:  # Filter reasonable length rules
                    rules[rule_category].append(rule)
    
    return rules

def extract_typeface_recommendations(text):
    """Extract specific typeface recommendations and classifications."""
    typefaces = {
        "serif_fonts": [],
        "sans_serif_fonts": [],
        "script_fonts": [],
        "display_fonts": [],
        "monospace_fonts": [],
        "font_classifications": {},
        "usage_recommendations": {}
    }
    
    # Common typeface names to look for
    serif_patterns = [
        r"(Garamond|Caslon|Baskerville|Bodoni|Didot|Times|Minion|Sabon|Palatino|Goudy)",
        r"(Centaur|Jenson|Bembo|Galliard|Granjon|Plantin|Imprint|Perpetua)"
    ]
    
    sans_patterns = [
        r"(Helvetica|Univers|Frutiger|Futura|Gill\s+Sans|Optima|Stone\s+Sans)",
        r"(Franklin|Meta|Thesis|Syntax|Avenir|Myriad)"
    ]
    
    # Extract typeface mentions
    for pattern in serif_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if match not in typefaces["serif_fonts"]:
                typefaces["serif_fonts"].append(match)
    
    for pattern in sans_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if match not in typefaces["sans_serif_fonts"]:
                typefaces["sans_serif_fonts"].append(match)
    
    return typefaces

def extract_layout_systems(text):
    """Extract information about layout systems and grids."""
    layout_systems = {
        "grid_systems": [],
        "margin_rules": [],
        "column_guidelines": [],
        "page_proportions": [],
        "binding_considerations": []
    }
    
    # Look for grid and layout information
    grid_patterns = [
        r"(?:grid|baseline|modular)\s+(?:system|approach|method)\s+([^.]+)",
        r"(?:column|margin|gutter)\s+(?:width|size|spacing)\s+(?:should|of)\s+([^.]+)",
        r"(?:page|text\s+block|type\s+area)\s+(?:proportion|ratio|size)\s+([^.]+)"
    ]
    
    for pattern in grid_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            rule = match.strip()
            if len(rule) > 10 and len(rule) < 150:
                layout_systems["grid_systems"].append(rule)
    
    return layout_systems

def extract_historical_context(text):
    """Extract historical typography information and context."""
    historical = {
        "type_designers": [],
        "historical_periods": [],
        "type_foundries": [],
        "influential_books": [],
        "cultural_context": []
    }
    
    # Look for designer names
    designer_patterns = [
        r"(Claude\s+Garamond|William\s+Caslon|John\s+Baskerville|Giambattista\s+Bodoni)",
        r"(Frederic\s+Goudy|Eric\s+Gill|Jan\s+Tschichold|Hermann\s+Zapf)",
        r"(Adrian\s+Frutiger|Max\s+Miedinger|Paul\s+Renner)"
    ]
    
    for pattern in designer_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if match not in historical["type_designers"]:
                historical["type_designers"].append(match)
    
    return historical

def extract_technical_specifications(text):
    """Extract technical typography specifications and measurements."""
    technical = {
        "opentype_features": [],
        "character_encoding": [],
        "font_metrics": [],
        "printing_specifications": [],
        "digital_considerations": []
    }
    
    # Look for technical terms
    technical_patterns = [
        r"(OpenType|TrueType|PostScript|Unicode|kerning\s+pairs)",
        r"(x-height|cap\s+height|ascender|descender|baseline)",
        r"(em\s+square|units\s+per\s+em|font\s+metrics)",
        r"(ligature|small\s+caps|oldstyle\s+figures|swash)"
    ]
    
    for pattern in technical_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if match not in technical["opentype_features"]:
                technical["opentype_features"].append(match)
    
    return technical

def extract_specific_measurements(text):
    """Extract specific numerical measurements and ratios."""
    measurements = {
        "line_spacing_ratios": [],
        "margin_proportions": [],
        "font_size_recommendations": [],
        "column_width_guidelines": [],
        "paper_sizes": []
    }
    
    # Look for specific measurements
    measurement_patterns = [
        r"(\d+(?:\.\d+)?)\s*(?:to|:)\s*(\d+(?:\.\d+)?)\s+(?:ratio|proportion)",
        r"(\d+(?:\.\d+)?)\s*(?:pt|px|mm|cm|inches?)\s+(?:leading|line\s+height)",
        r"(\d+(?:\.\d+)?)\s*(?:characters?|words?)\s+per\s+line",
        r"(\d+(?:\.\d+)?)\s*percent\s+(?:of|for)\s+([^.]+)"
    ]
    
    for pattern in measurement_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                measurement = " ".join(match).strip()
            else:
                measurement = match.strip()
            measurements["line_spacing_ratios"].append(measurement)
    
    return measurements

def analyze_chapters_and_sections(text):
    """Extract chapter structure and main topics."""
    chapters = {}
    
    # Look for chapter headings (numbers followed by titles)
    chapter_pattern = r'(?:CHAPTER\s+)?(\d+(?:\.\d+)?)\s+([A-Z][A-Z\s&,\-\']+)(?:\n|$)'
    matches = re.findall(chapter_pattern, text, re.MULTILINE)
    
    for number, title in matches:
        chapters[number] = title.strip()
    
    # Also look for section headings
    section_pattern = r'(\d+\.\d+(?:\.\d+)?)\s+([A-Z][A-Za-z\s&,\-\']+)(?:\n|$)'
    section_matches = re.findall(section_pattern, text, re.MULTILINE)
    
    sections = {}
    for number, title in section_matches:
        sections[number] = title.strip()
    
    return {"chapters": chapters, "sections": sections}

def main():
    pdf_path = "/Users/bengold/Documents/GitHub/MCP/The Elements of Typographic Style (Robert Bringhurst) (z-lib.org).pdf"
    
    print("🔍 Deep Analysis of Bringhurst's Typography Bible")
    print("=" * 60)
    
    # Extract complete text (or at least much more)
    text = extract_full_text_from_pdf(pdf_path, max_pages=200)  # Increase to 200 pages
    
    if "Error" in text or "not available" in text:
        print(f"⚠️  {text}")
        return
    
    print(f"✅ Extracted {len(text):,} characters from PDF")
    
    # Analyze document structure
    print(f"\n📚 Analyzing Document Structure...")
    structure = analyze_chapters_and_sections(text)
    print(f"📖 Found {len(structure['chapters'])} chapters")
    print(f"📄 Found {len(structure['sections'])} sections")
    
    # Extract detailed rules
    print(f"\n🔍 Extracting Detailed Typography Rules...")
    detailed_rules = extract_detailed_rules(text)
    
    rule_counts = {k: len(v) for k, v in detailed_rules.items() if isinstance(v, list)}
    total_rules = sum(rule_counts.values())
    print(f"📋 Extracted {total_rules} detailed rules:")
    for category, count in rule_counts.items():
        if count > 0:
            print(f"   • {category.replace('_', ' ').title()}: {count}")
    
    # Extract typeface information
    print(f"\n🎨 Analyzing Typeface Recommendations...")
    typefaces = extract_typeface_recommendations(text)
    print(f"📝 Found {len(typefaces['serif_fonts'])} serif fonts")
    print(f"📝 Found {len(typefaces['sans_serif_fonts'])} sans serif fonts")
    
    # Extract layout systems
    print(f"\n📐 Extracting Layout Systems...")
    layout_systems = extract_layout_systems(text)
    print(f"🏗️  Found {len(layout_systems['grid_systems'])} grid system rules")
    
    # Extract historical context
    print(f"\n📜 Gathering Historical Context...")
    historical = extract_historical_context(text)
    print(f"👨‍🎨 Found {len(historical['type_designers'])} type designers")
    
    # Extract technical specifications
    print(f"\n⚙️  Analyzing Technical Specifications...")
    technical = extract_technical_specifications(text)
    print(f"🔧 Found {len(technical['opentype_features'])} technical features")
    
    # Extract measurements
    print(f"\n📏 Extracting Specific Measurements...")
    measurements = extract_specific_measurements(text)
    print(f"📊 Found {len(measurements['line_spacing_ratios'])} measurement specifications")
    
    # Compile comprehensive typography data
    comprehensive_data = {
        "source": "The Elements of Typographic Style by Robert Bringhurst (Deep Analysis)",
        "extraction_stats": {
            "total_characters": len(text),
            "total_rules_extracted": total_rules,
            "chapters_analyzed": len(structure['chapters']),
            "sections_analyzed": len(structure['sections'])
        },
        "document_structure": structure,
        "detailed_rules": detailed_rules,
        "typeface_recommendations": typefaces,
        "layout_systems": layout_systems,
        "historical_context": historical,
        "technical_specifications": technical,
        "measurements": measurements,
        "analysis_date": "2025-06-13"
    }
    
    # Save comprehensive data
    output_file = "/Users/bengold/Documents/GitHub/MCP/Design_MCP/bringhurst_comprehensive.json"
    with open(output_file, "w") as f:
        json.dump(comprehensive_data, f, indent=2)
    
    print(f"\n✅ Comprehensive typography data saved to bringhurst_comprehensive.json")
    
    # Show sample extractions
    print(f"\n📋 Sample Extracted Rules:")
    print("-" * 40)
    
    for category, rules in detailed_rules.items():
        if rules and len(rules) > 0:
            print(f"\n🎯 {category.replace('_', ' ').title()}:")
            for rule in rules[:3]:  # Show first 3 rules
                print(f"   • {rule}")
    
    if typefaces['serif_fonts']:
        print(f"\n📝 Serif Fonts Mentioned:")
        print(f"   {', '.join(typefaces['serif_fonts'][:10])}")
    
    if typefaces['sans_serif_fonts']:
        print(f"\n📝 Sans Serif Fonts Mentioned:")
        print(f"   {', '.join(typefaces['sans_serif_fonts'][:10])}")
    
    if historical['type_designers']:
        print(f"\n👨‍🎨 Type Designers Referenced:")
        print(f"   {', '.join(historical['type_designers'][:5])}")
    
    print(f"\n🚀 Ready to create Enhanced Typography MCP Server!")
    print(f"📊 Total data points: {total_rules + len(typefaces['serif_fonts']) + len(typefaces['sans_serif_fonts']) + len(historical['type_designers'])}")

if __name__ == "__main__":
    main()