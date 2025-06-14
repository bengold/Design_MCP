"""MCP Server for UI Accessibility Rules and Best Practices."""

from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
import json
from accessibility_rules import AccessibilityRules, AccessibilityIssue, Severity, WCAGLevel
from wcag_data import wcag_data, WCAGCriterion


# Create the MCP server
mcp = FastMCP("UI Accessibility Checker", dependencies=["beautifulsoup4", "lxml", "cssselect"])


def parse_html_to_elements(html: str) -> List[Dict[str, Any]]:
    """Parse HTML string into a list of element dictionaries."""
    soup = BeautifulSoup(html, 'html.parser')
    elements = []
    
    for element in soup.find_all():
        elem_dict = {
            "tag": element.name,
            "attributes": dict(element.attrs),
            "text": element.get_text(strip=True) if element.string else ""
        }
        elements.append(elem_dict)
    
    return elements


def extract_headings(elements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Extract heading elements from the parsed elements."""
    return [e for e in elements if e["tag"] in ["h1", "h2", "h3", "h4", "h5", "h6"]]


@mcp.tool()
def check_html_accessibility(html: str, include_warnings: bool = True) -> Dict[str, Any]:
    """Check HTML content for accessibility issues based on WCAG guidelines.
    
    Args:
        html: HTML content to check
        include_warnings: Whether to include warnings in addition to errors
    
    Returns:
        Dictionary containing found issues categorized by severity
    """
    elements = parse_html_to_elements(html)
    issues = []
    
    # Run various accessibility checks
    for element in elements:
        # Check images for alt text
        issue = AccessibilityRules.check_img_alt_text(element)
        if issue:
            issues.append(issue)
        
        # Check form labels
        issue = AccessibilityRules.check_form_labels(element)
        if issue:
            issues.append(issue)
        
        # Check link text
        issue = AccessibilityRules.check_link_text(element)
        if issue:
            issues.append(issue)
        
        # Check language attribute
        issue = AccessibilityRules.check_language_attribute(element)
        if issue:
            issues.append(issue)
        
        # Check ARIA roles
        issue = AccessibilityRules.check_aria_roles(element)
        if issue:
            issues.append(issue)
        
        # Check keyboard accessibility
        issue = AccessibilityRules.check_keyboard_accessibility(element)
        if issue:
            issues.append(issue)
    
    # Check heading hierarchy
    headings = extract_headings(elements)
    heading_issues = AccessibilityRules.check_heading_hierarchy(headings)
    issues.extend(heading_issues)
    
    # Filter issues based on include_warnings
    if not include_warnings:
        issues = [i for i in issues if i.severity == Severity.ERROR]
    
    # Organize issues by severity
    result = {
        "total_issues": len(issues),
        "errors": [],
        "warnings": [],
        "info": [],
        "summary": {}
    }
    
    for issue in issues:
        issue_dict = {
            "rule_id": issue.rule_id,
            "message": issue.message,
            "wcag_level": issue.wcag_level.value,
            "wcag_criteria": issue.wcag_criteria,
            "suggestion": issue.suggestion
        }
        
        if issue.severity == Severity.ERROR:
            result["errors"].append(issue_dict)
        elif issue.severity == Severity.WARNING:
            result["warnings"].append(issue_dict)
        else:
            result["info"].append(issue_dict)
    
    result["summary"] = {
        "errors": len(result["errors"]),
        "warnings": len(result["warnings"]),
        "info": len(result["info"])
    }
    
    return result


@mcp.tool()
def check_color_contrast(foreground: str, background: str, font_size: float = 16, is_bold: bool = False) -> Dict[str, Any]:
    """Check if color contrast meets WCAG standards.
    
    Args:
        foreground: Foreground color in hex format (e.g., '#000000')
        background: Background color in hex format (e.g., '#FFFFFF')
        font_size: Font size in pixels
        is_bold: Whether the text is bold
    
    Returns:
        Contrast analysis with WCAG compliance information
    """
    # Simplified implementation - returns guidance
    # Real implementation would calculate actual contrast ratio
    
    is_large_text = font_size >= 18 or (font_size >= 14 and is_bold)
    
    return {
        "foreground": foreground,
        "background": background,
        "font_size": font_size,
        "is_bold": is_bold,
        "is_large_text": is_large_text,
        "wcag_requirements": {
            "AA": {
                "required_ratio": 3.0 if is_large_text else 4.5,
                "description": f"{'Large text' if is_large_text else 'Normal text'} requires {3.0 if is_large_text else 4.5}:1 contrast ratio"
            },
            "AAA": {
                "required_ratio": 4.5 if is_large_text else 7.0,
                "description": f"{'Large text' if is_large_text else 'Normal text'} requires {4.5 if is_large_text else 7.0}:1 contrast ratio for AAA"
            }
        },
        "recommendation": "Use a color contrast checker tool to verify the actual contrast ratio"
    }


@mcp.tool()
def suggest_aria_labels(element_type: str, context: str = "") -> Dict[str, Any]:
    """Suggest appropriate ARIA labels and attributes for UI elements.
    
    Args:
        element_type: Type of UI element (e.g., 'button', 'navigation', 'form')
        context: Additional context about the element's purpose
    
    Returns:
        ARIA suggestions and best practices
    """
    suggestions = {
        "button": {
            "attributes": ["aria-label", "aria-pressed", "aria-expanded"],
            "example": '<button aria-label="Close dialog" aria-pressed="false">X</button>',
            "best_practices": [
                "Use aria-label when button text isn't descriptive enough",
                "Add aria-pressed for toggle buttons",
                "Include aria-expanded for buttons that control collapsible content"
            ]
        },
        "navigation": {
            "attributes": ["role='navigation'", "aria-label"],
            "example": '<nav role="navigation" aria-label="Main navigation">...</nav>',
            "best_practices": [
                "Label navigation regions to distinguish between multiple nav elements",
                "Use landmarks to help screen reader users navigate"
            ]
        },
        "form": {
            "attributes": ["aria-label", "aria-labelledby", "aria-describedby", "aria-required", "aria-invalid"],
            "example": '<input aria-label="Email address" aria-required="true" aria-invalid="false">',
            "best_practices": [
                "Always associate labels with form controls",
                "Use aria-describedby for additional help text",
                "Mark required fields with aria-required",
                "Indicate validation states with aria-invalid"
            ]
        },
        "modal": {
            "attributes": ["role='dialog'", "aria-modal='true'", "aria-labelledby", "aria-describedby"],
            "example": '<div role="dialog" aria-modal="true" aria-labelledby="modal-title">...</div>',
            "best_practices": [
                "Trap focus within modal when open",
                "Provide a clear title with aria-labelledby",
                "Return focus to trigger element when closed"
            ]
        },
        "alert": {
            "attributes": ["role='alert'", "aria-live='assertive'", "aria-atomic='true'"],
            "example": '<div role="alert" aria-live="assertive">Error: Invalid email format</div>',
            "best_practices": [
                "Use for important, time-sensitive information",
                "Keep messages concise and actionable",
                "Consider using role='status' for less urgent updates"
            ]
        }
    }
    
    element_type_lower = element_type.lower()
    if element_type_lower in suggestions:
        result = suggestions[element_type_lower].copy()
        result["element_type"] = element_type
        result["context"] = context
        return result
    else:
        return {
            "element_type": element_type,
            "context": context,
            "message": f"No specific suggestions for '{element_type}'",
            "general_tips": [
                "Use semantic HTML elements when possible",
                "Add ARIA only when necessary to enhance accessibility",
                "Test with screen readers to verify implementation"
            ]
        }


@mcp.tool()
def generate_accessible_form(
    fields: List[Dict[str, str]], 
    form_title: str = "Form",
    include_aria: bool = True
) -> str:
    """Generate an accessible form template with proper labels and ARIA attributes.
    
    Args:
        fields: List of field dictionaries with 'name', 'type', and optional 'required'
        form_title: Title for the form
        include_aria: Whether to include ARIA attributes
    
    Returns:
        HTML template for an accessible form
    """
    form_html = f'<form role="form" aria-label="{form_title}">\n'
    form_html += f'  <h2 id="form-title">{form_title}</h2>\n'
    
    for field in fields:
        field_name = field.get("name", "field")
        field_type = field.get("type", "text")
        field_required = field.get("required", False)
        field_id = field_name.lower().replace(" ", "-")
        
        form_html += f'  <div class="form-field">\n'
        form_html += f'    <label for="{field_id}">\n'
        form_html += f'      {field_name}\n'
        if field_required:
            form_html += '      <span aria-label="required">*</span>\n'
        form_html += '    </label>\n'
        
        if field_type == "textarea":
            form_html += f'    <textarea id="{field_id}" name="{field_id}"'
        else:
            form_html += f'    <input type="{field_type}" id="{field_id}" name="{field_id}"'
        
        if include_aria:
            if field_required:
                form_html += ' aria-required="true"'
            form_html += f' aria-describedby="{field_id}-error"'
        
        form_html += '>\n'
        
        if include_aria:
            form_html += f'    <span id="{field_id}-error" role="alert" aria-live="polite"></span>\n'
        
        form_html += '  </div>\n\n'
    
    form_html += '  <button type="submit">Submit</button>\n'
    form_html += '</form>'
    
    return form_html


@mcp.tool()
def get_wcag_criterion(criterion_number: str) -> Dict[str, Any]:
    """Get detailed information about a specific WCAG success criterion.
    
    Args:
        criterion_number: WCAG criterion number (e.g., "1.1.1", "2.4.7")
    
    Returns:
        Detailed information about the criterion including description, level, and exceptions
    """
    criterion = wcag_data.get_criterion(criterion_number)
    
    if not criterion:
        return {
            "error": f"WCAG criterion {criterion_number} not found",
            "available_criteria": "Use search_wcag_criteria or list_wcag_criteria to find valid criteria"
        }
    
    return {
        "number": criterion.number,
        "id": criterion.id,
        "title": criterion.title,
        "level": criterion.level,
        "version": f"WCAG {criterion.version}",
        "description": criterion.description,
        "principle": criterion.principle,
        "guideline": criterion.guideline,
        "exceptions": criterion.exceptions or [],
        "conformance": {
            "Level A": "Must comply for basic accessibility",
            "Level AA": "Should comply for standard accessibility (recommended minimum)",
            "Level AAA": "May comply for enhanced accessibility (not required for general compliance)"
        }.get(f"Level {criterion.level}", "Unknown level")
    }


@mcp.tool()
def search_wcag_criteria(search_term: str) -> Dict[str, Any]:
    """Search WCAG success criteria by keyword.
    
    Args:
        search_term: Search term to find in criterion titles, descriptions, or guidelines
    
    Returns:
        List of matching WCAG criteria with summary information
    """
    criteria = wcag_data.search_criteria(search_term)
    
    if not criteria:
        return {
            "search_term": search_term,
            "results": [],
            "message": "No criteria found matching the search term"
        }
    
    results = []
    for criterion in criteria[:20]:  # Limit to first 20 results
        results.append({
            "number": criterion.number,
            "title": criterion.title,
            "level": criterion.level,
            "version": criterion.version,
            "principle": criterion.principle,
            "guideline": criterion.guideline,
            "brief_description": criterion.description[:200] + "..." if len(criterion.description) > 200 else criterion.description
        })
    
    return {
        "search_term": search_term,
        "total_results": len(criteria),
        "showing": len(results),
        "results": results
    }


@mcp.tool()
def list_wcag_criteria(level: str = "all", principle: str = "all") -> Dict[str, Any]:
    """List WCAG success criteria by level and/or principle.
    
    Args:
        level: Conformance level (A, AA, AAA, or "all")
        principle: WCAG principle (Perceivable, Operable, Understandable, Robust, or "all")
    
    Returns:
        List of WCAG criteria matching the specified filters
    """
    if level.upper() not in ["A", "AA", "AAA", "ALL"]:
        return {"error": "Level must be A, AA, AAA, or 'all'"}
    
    valid_principles = wcag_data.get_principles() + ["all"]
    if principle not in valid_principles:
        return {"error": f"Principle must be one of: {', '.join(valid_principles)}"}
    
    # Get criteria based on filters
    if level.upper() == "ALL" and principle.lower() == "all":
        criteria = wcag_data.get_all_criteria()
    elif level.upper() == "ALL":
        criteria = wcag_data.get_criteria_by_principle(principle)
    elif principle.lower() == "all":
        criteria = wcag_data.get_criteria_by_level(level.upper())
    else:
        all_for_principle = wcag_data.get_criteria_by_principle(principle)
        criteria = [c for c in all_for_principle if c.level == level.upper()]
    
    # Sort by criterion number
    criteria.sort(key=lambda x: [int(n) for n in x.number.split('.')])
    
    results = []
    for criterion in criteria:
        results.append({
            "number": criterion.number,
            "title": criterion.title,
            "level": criterion.level,
            "version": criterion.version,
            "principle": criterion.principle,
            "guideline": criterion.guideline
        })
    
    return {
        "filters": {"level": level, "principle": principle},
        "total_criteria": len(results),
        "criteria": results
    }


@mcp.tool()
def get_wcag_guidance_for_element(element_type: str, context: str = "") -> Dict[str, Any]:
    """Get WCAG guidance specific to a type of UI element.
    
    Args:
        element_type: Type of element (images, forms, links, buttons, etc.)
        context: Additional context about the element's use
    
    Returns:
        Relevant WCAG criteria and implementation guidance
    """
    criteria = wcag_data.get_criteria_for_techniques(element_type)
    
    if not criteria:
        available_types = ["images", "forms", "color", "keyboard", "headings", "links", 
                          "language", "media", "timing", "seizures", "navigation", "input", "focus"]
        return {
            "element_type": element_type,
            "context": context,
            "message": f"No specific guidance found for '{element_type}'",
            "available_types": available_types
        }
    
    # Sort by level (A first, then AA, then AAA)
    level_order = {"A": 1, "AA": 2, "AAA": 3}
    criteria.sort(key=lambda x: (level_order.get(x.level, 4), x.number))
    
    guidance = []
    for criterion in criteria:
        guidance.append({
            "number": criterion.number,
            "title": criterion.title,
            "level": criterion.level,
            "description": criterion.description,
            "guideline": criterion.guideline,
            "implementation_priority": {
                "A": "Required - Must implement for basic accessibility",
                "AA": "Recommended - Standard accessibility level",
                "AAA": "Enhanced - Additional accessibility improvement"
            }.get(criterion.level, "Unknown")
        })
    
    return {
        "element_type": element_type,
        "context": context,
        "applicable_criteria": len(guidance),
        "guidance": guidance,
        "summary": f"Found {len(guidance)} WCAG criteria applicable to {element_type}"
    }


@mcp.tool()
def validate_wcag_compliance_level(
    html: str, 
    target_level: str = "AA",
    include_suggestions: bool = True
) -> Dict[str, Any]:
    """Validate HTML against specific WCAG conformance level requirements.
    
    Args:
        html: HTML content to validate
        target_level: Target WCAG level (A, AA, AAA)
        include_suggestions: Whether to include fix suggestions
    
    Returns:
        Compliance analysis with specific criterion violations
    """
    if target_level.upper() not in ["A", "AA", "AAA"]:
        return {"error": "Target level must be A, AA, or AAA"}
    
    # Get all criteria for target level and below
    required_criteria = []
    if target_level.upper() in ["A", "AA", "AAA"]:
        required_criteria.extend(wcag_data.get_criteria_by_level("A"))
    if target_level.upper() in ["AA", "AAA"]:
        required_criteria.extend(wcag_data.get_criteria_by_level("AA"))
    if target_level.upper() == "AAA":
        required_criteria.extend(wcag_data.get_criteria_by_level("AAA"))
    
    # Run accessibility check
    elements = parse_html_to_elements(html)
    issues = []
    
    # Map our existing checks to WCAG criteria
    criterion_issues = {}
    
    for element in elements:
        # 1.1.1 - Non-text Content
        issue = AccessibilityRules.check_img_alt_text(element)
        if issue:
            criterion_issues.setdefault("1.1.1", []).append(issue)
        
        # 3.3.2 - Labels or Instructions
        issue = AccessibilityRules.check_form_labels(element)
        if issue:
            criterion_issues.setdefault("3.3.2", []).append(issue)
        
        # 2.4.4 - Link Purpose
        issue = AccessibilityRules.check_link_text(element)
        if issue:
            criterion_issues.setdefault("2.4.4", []).append(issue)
        
        # 3.1.1 - Language of Page
        issue = AccessibilityRules.check_language_attribute(element)
        if issue:
            criterion_issues.setdefault("3.1.1", []).append(issue)
        
        # 4.1.2 - Name, Role, Value
        issue = AccessibilityRules.check_aria_roles(element)
        if issue:
            criterion_issues.setdefault("4.1.2", []).append(issue)
        
        # 2.1.1 - Keyboard
        issue = AccessibilityRules.check_keyboard_accessibility(element)
        if issue:
            criterion_issues.setdefault("2.1.1", []).append(issue)
    
    # 1.3.1 - Heading hierarchy
    headings = extract_headings(elements)
    heading_issues = AccessibilityRules.check_heading_hierarchy(headings)
    if heading_issues:
        criterion_issues.setdefault("1.3.1", []).extend(heading_issues)
    
    # Build compliance report
    violations = []
    for criterion_number, criterion_issues_list in criterion_issues.items():
        criterion = wcag_data.get_criterion(criterion_number)
        if criterion and any(c.number == criterion_number for c in required_criteria):
            for issue in criterion_issues_list:
                violation = {
                    "criterion": criterion_number,
                    "criterion_title": criterion.title,
                    "criterion_level": criterion.level,
                    "issue": issue.message,
                    "severity": issue.severity.value,
                    "element": issue.element
                }
                if include_suggestions:
                    violation["suggestion"] = issue.suggestion
                violations.append(violation)
    
    # Calculate compliance
    total_required = len(required_criteria)
    violated_criteria = len(set(v["criterion"] for v in violations))
    compliance_percentage = ((total_required - violated_criteria) / total_required * 100) if total_required > 0 else 100
    
    return {
        "target_level": target_level.upper(),
        "compliance_status": "PASS" if len(violations) == 0 else "FAIL",
        "compliance_percentage": round(compliance_percentage, 1),
        "total_required_criteria": total_required,
        "violated_criteria": violated_criteria,
        "total_violations": len(violations),
        "violations": violations,
        "summary": f"{'✅ Passes' if len(violations) == 0 else '❌ Fails'} WCAG {target_level.upper()} with {violated_criteria} criteria violations"
    }


# Resources for accessibility guidelines
@mcp.resource("accessibility://wcag-quick-ref")
def get_wcag_quick_reference() -> str:
    """Get a quick reference guide for WCAG criteria by level."""
    metadata = wcag_data.get_metadata()
    
    output = f"""# WCAG Quick Reference
    
*Generated from official W3C WCAG repository*
*Total criteria: {metadata.get('total_criteria', 'Unknown')}*
*Versions covered: {', '.join(metadata.get('versions', []))}*

"""
    
    for level in ["A", "AA", "AAA"]:
        criteria = wcag_data.get_criteria_by_level(level)
        output += f"\n## Level {level} ({'Minimum' if level == 'A' else 'Standard' if level == 'AA' else 'Enhanced'})\n"
        
        for criterion in sorted(criteria, key=lambda x: [int(n) for n in x.number.split('.')]):
            # Truncate description for quick reference
            desc = criterion.description[:100] + "..." if len(criterion.description) > 100 else criterion.description
            output += f"- **{criterion.number} {criterion.title}**: {desc}\n"
    
    return output


@mcp.resource("accessibility://wcag-by-principle")
def get_wcag_by_principle() -> str:
    """Get WCAG criteria organized by principle."""
    output = "# WCAG 2.x Success Criteria by Principle\n\n*Based on official W3C WCAG guidelines*\n\n"
    
    for principle in wcag_data.get_principles():
        criteria = wcag_data.get_criteria_by_principle(principle)
        if not criteria:
            continue
            
        output += f"## {principle}\n\n"
        
        # Group by guideline
        guidelines = {}
        for criterion in criteria:
            if criterion.guideline not in guidelines:
                guidelines[criterion.guideline] = []
            guidelines[criterion.guideline].append(criterion)
        
        for guideline, guideline_criteria in guidelines.items():
            output += f"### {guideline}\n\n"
            for criterion in sorted(guideline_criteria, key=lambda x: [int(n) for n in x.number.split('.')]):
                output += f"- **{criterion.number} {criterion.title}** (Level {criterion.level})\n"
                output += f"  - {criterion.description[:150]}{'...' if len(criterion.description) > 150 else ''}\n\n"
    
    return output


@mcp.resource("accessibility://aria-patterns")
def get_aria_patterns() -> str:
    """Get common ARIA design patterns and examples."""
    return """# Common ARIA Design Patterns

## Buttons
```html
<!-- Simple button -->
<button type="button">Save</button>

<!-- Toggle button -->
<button type="button" aria-pressed="false">Mute</button>

<!-- Button with icon only -->
<button type="button" aria-label="Close dialog">
  <span aria-hidden="true">×</span>
</button>
```

## Navigation
```html
<!-- Main navigation -->
<nav aria-label="Main">
  <ul>
    <li><a href="/" aria-current="page">Home</a></li>
    <li><a href="/about">About</a></li>
  </ul>
</nav>

<!-- Breadcrumb -->
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li aria-current="page">Shoes</li>
  </ol>
</nav>
```

## Forms
```html
<!-- Required field -->
<label for="email">
  Email <span aria-label="required">*</span>
</label>
<input type="email" id="email" aria-required="true" aria-describedby="email-error">
<span id="email-error" role="alert" aria-live="polite"></span>

<!-- Field with help text -->
<label for="password">Password</label>
<input type="password" id="password" aria-describedby="password-help">
<div id="password-help">Must be at least 8 characters</div>
```

## Live Regions
```html
<!-- Status messages -->
<div role="status" aria-live="polite" aria-atomic="true">
  <p>Form saved successfully</p>
</div>

<!-- Error alerts -->
<div role="alert" aria-live="assertive">
  <p>Error: Invalid credit card number</p>
</div>
```

## Modals/Dialogs
```html
<div role="dialog" aria-modal="true" aria-labelledby="dialog-title" aria-describedby="dialog-desc">
  <h2 id="dialog-title">Confirm Delete</h2>
  <p id="dialog-desc">Are you sure you want to delete this item?</p>
  <button type="button">Cancel</button>
  <button type="button">Delete</button>
</div>
```"""


@mcp.resource("accessibility://testing-checklist")
def get_testing_checklist() -> str:
    """Get a comprehensive accessibility testing checklist."""
    return """# Accessibility Testing Checklist

## Automated Testing
- [ ] Run axe DevTools or similar automated checker
- [ ] Validate HTML markup
- [ ] Check for missing alt text
- [ ] Verify form labels
- [ ] Check heading hierarchy
- [ ] Verify color contrast ratios

## Keyboard Testing
- [ ] Tab through all interactive elements
- [ ] Check focus indicators are visible
- [ ] Verify focus order is logical
- [ ] Test keyboard shortcuts don't conflict
- [ ] Ensure no keyboard traps
- [ ] Test modal/dialog focus management

## Screen Reader Testing
- [ ] Test with NVDA (Windows) or JAWS
- [ ] Test with VoiceOver (macOS/iOS)
- [ ] Verify all content is announced
- [ ] Check form instructions are clear
- [ ] Test error messages are announced
- [ ] Verify live regions work correctly

## Visual Testing
- [ ] Zoom page to 200% - content still usable
- [ ] Test with Windows High Contrast mode
- [ ] Verify information isn't conveyed by color alone
- [ ] Check focus indicators have sufficient contrast
- [ ] Test with browser's reader mode

## Mobile/Touch Testing
- [ ] Touch targets are at least 44x44 pixels
- [ ] Test with touch + screen reader
- [ ] Verify gestures have alternatives
- [ ] Check horizontal scrolling is avoided

## Cognitive Testing
- [ ] Instructions are clear and simple
- [ ] Error messages are helpful
- [ ] Important actions are reversible
- [ ] Timeouts provide warnings
- [ ] Animations can be paused/stopped"""


@mcp.prompt()
def accessibility_audit_prompt(page_type: str = "website") -> str:
    """Generate a prompt for conducting an accessibility audit."""
    return f"""Please conduct a comprehensive accessibility audit for this {page_type}. 

Check for the following WCAG 2.1 compliance issues:

1. **Perceivable**
   - Missing alt text on images
   - Poor color contrast
   - Missing captions/transcripts for media
   - Information conveyed only through color

2. **Operable**
   - Keyboard accessibility issues
   - Missing skip links
   - No focus indicators
   - Time limits without warnings

3. **Understandable**
   - Missing form labels
   - Unclear error messages
   - Inconsistent navigation
   - Missing language declarations

4. **Robust**
   - Invalid HTML
   - Missing ARIA labels where needed
   - Improper ARIA usage

For each issue found, provide:
- The specific WCAG criterion violated
- Severity level (A, AA, or AAA)
- Clear description of the issue
- Recommended fix with code example

Prioritize issues by impact on users and ease of implementation."""


if __name__ == "__main__":
    mcp.run()