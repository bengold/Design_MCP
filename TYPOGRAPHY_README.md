# Typography MCP Server

A comprehensive MCP (Model Context Protocol) server for typography analysis and design guidance based on **"The Elements of Typographic Style"** by Robert Bringhurst.

## Features

### Typography Analysis Tools

1. **`analyze_typography`** - Comprehensive typography analysis
   - Line length evaluation (optimal 45-75 characters)
   - Line height ratio analysis (1.2-1.5 for body text)
   - Text rhythm and readability assessment
   - Bringhurst principle compliance

2. **`generate_typographic_scale`** - Mathematical type scales
   - 12 different scale ratios (minor third, golden ratio, etc.)
   - Harmonious font size progression
   - Usage recommendations for each scale level
   - Line height suggestions for each size

3. **`validate_typography_rules`** - Professional validation
   - Rule-based typography checking
   - Bringhurst principle compliance scoring
   - Context-aware validation (body, heading, caption)
   - Letter spacing and measure validation

4. **`suggest_typography_improvements`** - Smart recommendations
   - Specific improvement suggestions
   - Priority-based issue identification
   - Target readability optimization
   - Before/after value recommendations

5. **`calculate_reading_metrics`** - Reading analysis
   - Reading time estimation
   - Text difficulty assessment
   - Layout metric calculations
   - Word and sentence statistics

### Typography Resources

- **`typography://bringhurst-principles`** - Core principles from the master
- **`typography://measurements-guide`** - Professional measurements & guidelines  
- **`typography://scales-reference`** - Mathematical scale ratios and usage

### Typography Prompt

- **`typography_review_prompt`** - Generate prompts for design reviews

## Based on Bringhurst's Principles

### 🎯 Rhythm and Proportion
- Choose appropriate leading for typeface and measure
- Add/delete vertical space in measured intervals
- Don't stretch or compress letterforms
- Choose comfortable measure for text

### 🎯 Harmony and Counterpoint  
- Don't use too many type families
- Balance type sizes, weights, and styles
- Create clear hierarchical relationships
- Maintain consistent spacing

### 🎯 Structural Forms and Devices
- Use em and en dashes correctly
- Hang punctuation where appropriate
- Use true italics, not slanted roman
- Choose proper quotation marks

### 🎯 Analphabetic Symbols
- Use proportional oldstyle figures in text
- Use tabular figures in tables
- Set mathematical copy correctly
- Use proper fractions and superscripts

### 🎯 Page Architecture
- Create active white space
- Use consistent margins and gutters
- Align text to baseline grid
- Balance text and white space

## Typography Guidelines

### Line Length (Measure)
- **Optimal range**: 45-75 characters per line
- **Ideal**: 65-66 characters per line
- **Formula**: 2.5 alphabets (a-z repeated 2.5 times)

### Line Height (Leading)
- **Body text**: 1.2-1.5 times the font size
- **Headings**: 1.0-1.2 times the font size
- **Tight leading**: Use sparingly for short lines

### Font Sizes
- **Body text**: 14-16px for screen, 10-12pt for print
- **Headings**: Use mathematical scales (1.2, 1.414, 1.618 ratios)
- **Captions**: 1-2 sizes smaller than body text

### Spacing
- **Letter spacing**: Negative for large headings, positive for small caps
- **Word spacing**: Optimize for even color and texture
- **Paragraph spacing**: 0.5-1.0 times the line height

## Mathematical Type Scales

### Available Scales
- **Minor Second** (1.067): Subtle progression
- **Major Second** (1.125): Gentle scale
- **Minor Third** (1.200): Subtle, elegant
- **Major Third** (1.250): Balanced, versatile ⭐
- **Perfect Fourth** (1.333): Strong hierarchy
- **Tritone** (1.414): Bold contrast
- **Perfect Fifth** (1.500): Dramatic scale
- **Golden Ratio** (1.618): Natural harmony ⭐
- **Major Sixth** (1.667): Wide spacing
- **Minor Seventh** (1.778): Very bold
- **Major Seventh** (1.875): Extreme contrast
- **Octave** (2.000): Maximum contrast

### Scale Usage Examples
**Major Third Scale (base 16px):**
- 10.2px → Small captions, fine print
- 12.8px → Captions, metadata  
- 16.0px → Body text (base)
- 20.0px → Subheadings, lead paragraphs
- 25.0px → Section headings
- 31.2px → Page titles, major headings

## Installation

```bash
# Install dependencies (if using full MCP server)
pip install "mcp[cli]"

# Run the server
uv run mcp dev typography-mcp-server.py

# Run standalone demo
python3 typography_demo_standalone.py
```

## Example Usage

### Basic Typography Analysis
```python
analyze_typography(
    text="Your sample text here",
    font_size=16,
    line_height=24,
    line_length_chars=68
)
```

### Generate Type Scale
```python
generate_typographic_scale(
    base_size=16,
    scale_name="golden_ratio",
    levels=6
)
```

### Validate Typography
```python
validate_typography_rules(
    font_family="Georgia",
    font_size=16,
    line_height=24,
    line_length_chars=68,
    context="body_text"
)
```

## Quick Typography Checklist

### ✅ Essential Checks
- [ ] Line length: 45-75 characters
- [ ] Line height: 1.2-1.5 ratio for body text
- [ ] Font size: 14-16px for body text
- [ ] Consistent type scale progression
- [ ] Proper hierarchy established
- [ ] Adequate white space

### 📐 Advanced Checks  
- [ ] Mathematical scale ratios used
- [ ] Letter spacing optimized
- [ ] Punctuation and symbols correct
- [ ] Baseline grid alignment
- [ ] Text color and contrast proper

## Source

Based on **"The Elements of Typographic Style"** by Robert Bringhurst - the definitive guide to typography principles and practice.

> "Typography exists to honor content." - Robert Bringhurst

## Files

- `typography-mcp-server.py` - Full MCP server implementation
- `typography_demo_standalone.py` - Standalone demo (no MCP dependencies)
- `typography_principles.json` - Extracted Bringhurst principles
- `analyze_typography_pdf.py` - PDF analysis tool
- `TYPOGRAPHY_README.md` - This documentation