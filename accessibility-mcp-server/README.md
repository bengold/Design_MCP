# UI Accessibility MCP Server

An MCP (Model Context Protocol) server that provides tools and resources for checking UI accessibility based on **official WCAG 2.0-2.2 guidelines** from the W3C repository.

## Features

### Core Accessibility Tools

1. **`check_html_accessibility`** - Analyzes HTML content for accessibility issues
   - Checks for missing alt text on images
   - Validates heading hierarchy
   - Ensures form inputs have labels
   - Checks link text descriptiveness
   - Validates ARIA roles and attributes
   - Detects keyboard accessibility issues

2. **`check_color_contrast`** - Evaluates color contrast ratios
   - Provides WCAG AA and AAA requirements
   - Accounts for text size and weight
   - Returns specific contrast ratio requirements

3. **`suggest_aria_labels`** - Suggests appropriate ARIA attributes
   - Provides context-specific ARIA patterns
   - Includes best practices and examples
   - Covers buttons, navigation, forms, modals, and alerts

4. **`generate_accessible_form`** - Creates accessible form templates
   - Generates forms with proper labels
   - Includes ARIA attributes
   - Handles required fields appropriately

### Official WCAG Tools ⭐ NEW

5. **`get_wcag_criterion`** - Get detailed information about specific WCAG success criteria
   - Official descriptions from W3C repository
   - Includes exceptions and conformance levels
   - Covers WCAG 2.0, 2.1, and 2.2

6. **`search_wcag_criteria`** - Search through all 87 WCAG criteria by keyword
   - Find criteria by title, description, or guideline
   - Returns structured results with metadata

7. **`list_wcag_criteria`** - List criteria by conformance level and/or principle
   - Filter by A, AA, AAA levels
   - Organize by Perceivable, Operable, Understandable, Robust principles

8. **`get_wcag_guidance_for_element`** - Get element-specific WCAG guidance
   - Targeted advice for images, forms, links, navigation, etc.
   - Implementation priorities by conformance level

9. **`validate_wcag_compliance_level`** - Comprehensive WCAG compliance validation
   - Test against specific conformance levels (A, AA, AAA)
   - Maps violations to specific WCAG criteria
   - Provides compliance percentage and detailed reports

### Resources

- **`accessibility://wcag-quick-ref`** - Complete WCAG quick reference (generated from official data)
- **`accessibility://wcag-by-principle`** - WCAG criteria organized by the 4 principles
- **`accessibility://aria-patterns`** - Common ARIA design patterns with examples
- **`accessibility://testing-checklist`** - Comprehensive accessibility testing checklist

### Prompts

- **`accessibility_audit_prompt`** - Generates prompts for conducting accessibility audits

## Installation

1. Make sure you have Python 3.10+ installed
2. Install the package using uv (recommended):

```bash
cd accessibility-mcp-server
uv sync
```

Or with pip:

```bash
cd accessibility-mcp-server
pip install -e .
```

## Usage

### Running the Server

```bash
# Using uv (recommended)
uv run mcp dev server.py

# Or directly with Python
python server.py
```

### Installing in Claude Desktop

```bash
uv run mcp install server.py --name "Accessibility Checker"
```

### Example Usage

Once connected to an MCP client, you can use the tools like this:

#### Basic Accessibility Checks

1. **Check HTML for accessibility issues:**
```
Use the check_html_accessibility tool to analyze this HTML:
<html>
<body>
  <img src="logo.png">
  <h3>Welcome</h3>
  <input type="email" placeholder="Email">
  <a href="/more">Click here</a>
</body>
</html>
```

2. **Get ARIA suggestions:**
```
Use the suggest_aria_labels tool for a "navigation" element with context "main site navigation"
```

3. **Generate an accessible form:**
```
Use the generate_accessible_form tool with fields:
- name: "Full Name", type: "text", required: true
- name: "Email", type: "email", required: true
- name: "Message", type: "textarea", required: false
```

#### Official WCAG Tools

4. **Look up specific WCAG criteria:**
```
Use get_wcag_criterion with criterion_number "1.1.1" to learn about Non-text Content requirements
```

5. **Search for WCAG criteria by topic:**
```
Use search_wcag_criteria with search_term "color contrast" to find all contrast-related criteria
```

6. **Get element-specific guidance:**
```
Use get_wcag_guidance_for_element with element_type "forms" to get all WCAG requirements for forms
```

7. **Validate WCAG compliance:**
```
Use validate_wcag_compliance_level with your HTML and target_level "AA" to get a detailed compliance report
```

## WCAG Coverage

This server includes **all 87 official WCAG success criteria** from versions 2.0, 2.1, and 2.2:

### WCAG 2.0 (61 criteria)
- Complete foundational accessibility requirements
- Levels A, AA, and AAA criteria

### WCAG 2.1 (17 additional criteria) 
- Mobile accessibility improvements
- Cognitive and low vision enhancements
- Motor disabilities support

### WCAG 2.2 (9 additional criteria)
- Enhanced authentication requirements
- Improved focus management
- Better cognitive accessibility support

### Active Validation Rules
The server currently performs automated checks for:
- **1.1.1** - Non-text Content (alt text)
- **1.3.1** - Info and Relationships (headings, labels)
- **1.4.3** - Contrast (Minimum)
- **2.1.1** - Keyboard accessibility
- **2.4.4** - Link Purpose
- **2.4.7** - Focus Visible  
- **3.1.1** - Language of Page
- **3.3.2** - Labels or Instructions
- **4.1.2** - Name, Role, Value (ARIA)

*All 87 criteria are available for lookup, search, and guidance through the WCAG tools.*

## Development

To extend the server with additional accessibility rules:

1. Add new rule methods to `accessibility_rules.py`
2. Integrate them into the `check_html_accessibility` tool in `server.py`
3. Add corresponding tests

## Future Enhancements

- Real color contrast calculation
- CSS analysis for focus indicators
- Automated fix suggestions with code snippets
- Integration with automated testing tools
- Support for checking React/Vue/Angular components
- PDF accessibility checking
- Video/audio content accessibility verification