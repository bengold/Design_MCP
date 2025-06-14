#!/usr/bin/env python3
"""
Demo script showing the enhanced WCAG MCP Server capabilities.
Run with: uv run python demo.py
"""

from server import (
    get_wcag_criterion, 
    search_wcag_criteria,
    get_wcag_guidance_for_element,
    validate_wcag_compliance_level,
    check_html_accessibility,
    suggest_aria_labels
)
from wcag_data import wcag_data
import json

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print('='*60)

def print_section(title):
    print(f"\n📋 {title}")
    print('-' * 40)

def main():
    print("🌟 WCAG Accessibility MCP Server Demo")
    print("Enhanced with official W3C WCAG Repository data")
    
    # Show WCAG data overview
    print_header("WCAG Data Overview")
    metadata = wcag_data.get_metadata()
    print(f"📊 Total WCAG Criteria: {metadata.get('total_criteria', 'Unknown')}")
    print(f"📅 Versions Covered: {', '.join(metadata.get('versions', []))}")
    print(f"🎯 Level A: {len(wcag_data.get_criteria_by_level('A'))} criteria")
    print(f"🎯 Level AA: {len(wcag_data.get_criteria_by_level('AA'))} criteria")
    print(f"🎯 Level AAA: {len(wcag_data.get_criteria_by_level('AAA'))} criteria")
    
    # Test 1: Look up specific WCAG criterion
    print_header("1. WCAG Criterion Lookup")
    criterion = get_wcag_criterion("1.1.1")
    print(f"Criterion: {criterion['number']} - {criterion['title']}")
    print(f"Level: {criterion['level']} | Version: {criterion['version']}")
    print(f"Principle: {criterion['principle']}")
    print(f"Description: {criterion['description'][:150]}...")
    print(f"Exceptions: {len(criterion['exceptions'])} listed")
    
    # Test 2: Search WCAG criteria
    print_header("2. Search WCAG Criteria")
    search_results = search_wcag_criteria("keyboard")
    print(f"🔍 Search term: 'keyboard'")
    print(f"📊 Results found: {len(search_results.get('results', []))}")
    for i, result in enumerate(search_results.get('results', [])[:3]):
        print(f"{i+1}. {result['number']} - {result['title']} (Level {result['level']})")
    
    # Test 3: Element-specific guidance
    print_header("3. Element-Specific WCAG Guidance")
    guidance = get_wcag_guidance_for_element("images")
    print(f"🖼️ Element type: images")
    print(f"📋 Applicable criteria: {guidance['applicable_criteria']}")
    for criterion in guidance.get('guidance', [])[:3]:
        print(f"• {criterion['number']} - {criterion['title']} (Level {criterion['level']})")
        print(f"  {criterion['implementation_priority']}")
    
    # Test 4: HTML Accessibility Check
    print_header("4. HTML Accessibility Analysis")
    test_html = """
    <html lang="en">
    <body>
        <h1>Welcome to Our Site</h1>
        <img src="logo.png" alt="Company Logo">
        <nav aria-label="Main navigation">
            <a href="/home">Home</a>
            <a href="/about">About</a>
        </nav>
        <form>
            <label for="email">Email Address</label>
            <input type="email" id="email" required aria-required="true">
            <button type="submit">Subscribe</button>
        </form>
    </body>
    </html>
    """
    
    basic_check = check_html_accessibility(test_html)
    print(f"🔍 Basic accessibility check:")
    print(f"📊 Total issues: {basic_check['total_issues']}")
    print(f"❌ Errors: {basic_check['summary']['errors']}")
    print(f"⚠️  Warnings: {basic_check['summary']['warnings']}")
    print(f"ℹ️  Info: {basic_check['summary']['info']}")
    
    # Test 5: WCAG Compliance Validation
    print_header("5. WCAG Compliance Validation")
    compliance = validate_wcag_compliance_level(test_html, "AA")
    print(f"🎯 Target Level: WCAG {compliance['target_level']}")
    print(f"✅ Status: {compliance['compliance_status']}")
    print(f"📊 Compliance: {compliance['compliance_percentage']}%")
    print(f"📋 Total violations: {compliance['total_violations']}")
    print(f"📝 {compliance['summary']}")
    
    # Test 6: ARIA Suggestions
    print_header("6. ARIA Guidance")
    aria_guidance = suggest_aria_labels("button", "close dialog button")
    print(f"🔧 Element type: {aria_guidance['element_type']}")
    print(f"📝 Context: {aria_guidance['context']}")
    print(f"🏷️  Suggested attributes: {', '.join(aria_guidance['attributes'])}")
    print(f"💡 Example: {aria_guidance['example']}")
    
    print_header("Demo Complete! 🎉")
    print("The MCP server is ready to use with:")
    print("• 9 accessibility tools")
    print("• 4 comprehensive resources") 
    print("• Complete WCAG 2.0-2.2 criteria database")
    print("• Official W3C data integration")
    print("\nStart the server with: uv run mcp dev server.py")

if __name__ == "__main__":
    main()