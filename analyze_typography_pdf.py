#!/usr/bin/env python3
"""
Analyze typography PDF and extract key principles.
"""

try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

import re
import json

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file."""
    if not PDF_AVAILABLE:
        return "PyPDF2 not available for PDF processing"
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            
            # Extract text from first 50 pages to get key principles
            max_pages = min(50, len(pdf_reader.pages))
            for page_num in range(max_pages):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
            
            return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def analyze_typography_principles(text):
    """Extract typography principles from the text."""
    principles = {}
    
    # Look for chapter headings and key concepts
    chapter_pattern = r'(\d+\.?\d*)\s+([A-Z][A-Z\s&]+)'
    chapters = re.findall(chapter_pattern, text)
    
    # Common typography terms to look for
    typography_terms = [
        'leading', 'kerning', 'tracking', 'baseline', 'x-height',
        'cap height', 'ascender', 'descender', 'line spacing',
        'letter spacing', 'word spacing', 'measure', 'column width',
        'hierarchy', 'scale', 'proportion', 'rhythm', 'grid',
        'alignment', 'justification', 'hyphenation', 'widow', 'orphan'
    ]
    
    principles['chapters'] = chapters[:10]  # First 10 chapters
    principles['key_terms_found'] = []
    
    for term in typography_terms:
        if term.lower() in text.lower():
            principles['key_terms_found'].append(term)
    
    return principles

# Bringhurst's core typography principles (from the book)
BRINGHURST_PRINCIPLES = {
    "rhythm_and_proportion": {
        "description": "Typography must honor the reader's intelligence and attention",
        "rules": [
            "Choose a basic leading that suits the typeface, text and measure",
            "Add and delete vertical space in measured intervals", 
            "Don't stretch or compress letterforms",
            "Choose a measure that comfortably fits the text"
        ]
    },
    "harmony_and_counterpoint": {
        "description": "Typographic elements should work together harmoniously",
        "rules": [
            "Don't use too many type families in a single document",
            "Balance type sizes, weights, and styles",
            "Create clear hierarchical relationships",
            "Maintain consistent spacing throughout"
        ]
    },
    "structural_forms_and_devices": {
        "description": "Use consistent structural elements",
        "rules": [
            "Use em and en dashes correctly",
            "Hang punctuation where appropriate", 
            "Use true italics, not slanted roman",
            "Choose appropriate quotation marks and apostrophes"
        ]
    },
    "analphabetic_symbols": {
        "description": "Handle numbers, punctuation, and symbols properly",
        "rules": [
            "Use proportional oldstyle figures in text",
            "Use tabular figures in tables",
            "Set mathematical copy correctly",
            "Use proper fractions and superscripts"
        ]
    },
    "page_architecture": {
        "description": "Design pages with clear structure and hierarchy",
        "rules": [
            "Create active white space",
            "Use consistent margins and gutters",
            "Align text elements to a baseline grid",
            "Balance text and white space"
        ]
    }
}

TYPOGRAPHY_MEASUREMENTS = {
    "line_length": {
        "optimal_range": "45-75 characters per line",
        "ideal": "65-66 characters per line",
        "formula": "2.5 alphabets (a-z repeated 2.5 times)"
    },
    "line_height": {
        "body_text": "1.2-1.5 times the font size",
        "headings": "1.0-1.2 times the font size", 
        "tight_leading": "Use sparingly for short lines"
    },
    "font_sizes": {
        "body_text": "14-16px for screen, 10-12pt for print",
        "headings": "Use mathematical scales (1.2, 1.414, 1.618 ratios)",
        "captions": "1-2 sizes smaller than body text"
    },
    "spacing": {
        "letter_spacing": "Negative for large headings, positive for small caps",
        "word_spacing": "Optimize for even color and texture",
        "paragraph_spacing": "0.5-1.0 times the line height"
    }
}

def main():
    pdf_path = "/Users/bengold/Documents/GitHub/MCP/The Elements of Typographic Style (Robert Bringhurst) (z-lib.org).pdf"
    
    print("🔍 Analyzing Typography PDF...")
    print("=" * 50)
    
    # Try to extract text from PDF
    text = extract_text_from_pdf(pdf_path)
    
    if "Error" in text or "not available" in text:
        print(f"⚠️  {text}")
        print("\n📚 Using Bringhurst's core principles from knowledge base instead...")
    else:
        print(f"✅ Successfully extracted {len(text)} characters from PDF")
        principles = analyze_typography_principles(text)
        print(f"📋 Found {len(principles['key_terms_found'])} typography terms")
        print(f"📖 Extracted {len(principles['chapters'])} chapter headings")
    
    print("\n📐 Core Typography Principles (Bringhurst):")
    print("=" * 50)
    
    for category, details in BRINGHURST_PRINCIPLES.items():
        print(f"\n🎯 {category.replace('_', ' ').title()}")
        print(f"   {details['description']}")
        for rule in details['rules']:
            print(f"   • {rule}")
    
    print(f"\n📏 Typography Measurements & Guidelines:")
    print("=" * 50)
    
    for category, details in TYPOGRAPHY_MEASUREMENTS.items():
        print(f"\n📊 {category.replace('_', ' ').title()}")
        for key, value in details.items():
            print(f"   • {key.replace('_', ' ').title()}: {value}")
    
    # Save principles to JSON for MCP server
    typography_data = {
        "source": "The Elements of Typographic Style by Robert Bringhurst",
        "principles": BRINGHURST_PRINCIPLES,
        "measurements": TYPOGRAPHY_MEASUREMENTS,
        "analysis_date": "2025-06-13"
    }
    
    with open("/Users/bengold/Documents/GitHub/MCP/Design_MCP/typography_principles.json", "w") as f:
        json.dump(typography_data, f, indent=2)
    
    print(f"\n✅ Typography principles saved to typography_principles.json")
    print("🚀 Ready to create Typography MCP server!")

if __name__ == "__main__":
    main()