"""
Color contrast ratio calculator based on WCAG formulas.
"""

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_relative_luminance(r, g, b):
    """Calculate relative luminance according to WCAG formula."""
    def linearize(c):
        c = c / 255.0
        if c <= 0.03928:
            return c / 12.92
        else:
            return pow((c + 0.055) / 1.055, 2.4)
    
    r_linear = linearize(r)
    g_linear = linearize(g) 
    b_linear = linearize(b)
    
    return 0.2126 * r_linear + 0.7152 * g_linear + 0.0722 * b_linear

def calculate_contrast_ratio(color1, color2):
    """Calculate contrast ratio between two hex colors."""
    rgb1 = hex_to_rgb(color1)
    rgb2 = hex_to_rgb(color2)
    
    lum1 = rgb_to_relative_luminance(*rgb1)
    lum2 = rgb_to_relative_luminance(*rgb2)
    
    # Ensure lighter color is the numerator
    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)
    
    contrast_ratio = (lighter + 0.05) / (darker + 0.05)
    return contrast_ratio

def evaluate_contrast(foreground, background, font_size=16, is_bold=False):
    """Evaluate color contrast according to WCAG standards."""
    ratio = calculate_contrast_ratio(foreground, background)
    
    # Determine if it's large text
    is_large_text = font_size >= 18 or (font_size >= 14 and is_bold)
    
    # WCAG requirements
    aa_threshold = 3.0 if is_large_text else 4.5
    aaa_threshold = 4.5 if is_large_text else 7.0
    
    aa_pass = ratio >= aa_threshold
    aaa_pass = ratio >= aaa_threshold
    
    return {
        "foreground": foreground,
        "background": background,
        "contrast_ratio": round(ratio, 2),
        "font_size": font_size,
        "is_bold": is_bold,
        "is_large_text": is_large_text,
        "wcag_aa": {
            "required": aa_threshold,
            "passes": aa_pass,
            "status": "✅ PASS" if aa_pass else "❌ FAIL"
        },
        "wcag_aaa": {
            "required": aaa_threshold, 
            "passes": aaa_pass,
            "status": "✅ PASS" if aaa_pass else "❌ FAIL"
        },
        "overall_grade": "AAA" if aaa_pass else "AA" if aa_pass else "FAIL"
    }

if __name__ == "__main__":
    # Test the specific colors requested
    result = evaluate_contrast("#FAFAFA", "#FFFFFF", 16, False)
    
    print("🎨 Color Contrast Analysis")
    print("=" * 40)
    print(f"Foreground: {result['foreground']}")
    print(f"Background: {result['background']}")
    print(f"Contrast Ratio: {result['contrast_ratio']}:1")
    print()
    print(f"Font size: {result['font_size']}px")
    print(f"Bold: {result['is_bold']}")
    print(f"Large text: {result['is_large_text']}")
    print()
    print("WCAG Compliance:")
    print(f"• Level AA: {result['wcag_aa']['status']} (requires {result['wcag_aa']['required']}:1)")
    print(f"• Level AAA: {result['wcag_aaa']['status']} (requires {result['wcag_aaa']['required']}:1)")
    print()
    print(f"Overall Grade: {result['overall_grade']}")
    
    if result['overall_grade'] == 'FAIL':
        print()
        print("⚠️  Recommendations:")
        print("• Use darker foreground or lighter background colors")
        print("• Consider increasing font size to 18px+ for better readability")
        print("• Use bold font weight if possible")