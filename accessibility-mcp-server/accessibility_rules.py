"""Core accessibility rules and validators based on WCAG guidelines."""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum


class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class WCAGLevel(Enum):
    A = "A"
    AA = "AA"
    AAA = "AAA"


@dataclass
class AccessibilityIssue:
    rule_id: str
    severity: Severity
    wcag_level: WCAGLevel
    message: str
    element: Optional[str] = None
    suggestion: Optional[str] = None
    wcag_criteria: Optional[str] = None


class AccessibilityRules:
    """Collection of accessibility rules based on WCAG 2.1 guidelines."""
    
    @staticmethod
    def check_img_alt_text(html_element: Dict[str, Any]) -> Optional[AccessibilityIssue]:
        """Check if images have alt text (WCAG 1.1.1)."""
        if html_element.get("tag") == "img":
            alt = html_element.get("attributes", {}).get("alt")
            if alt is None:
                return AccessibilityIssue(
                    rule_id="img-alt-missing",
                    severity=Severity.ERROR,
                    wcag_level=WCAGLevel.A,
                    message="Image missing alt attribute",
                    element=str(html_element),
                    suggestion="Add an alt attribute to describe the image. Use alt='' for decorative images.",
                    wcag_criteria="1.1.1"
                )
            elif alt.strip() == "" and not html_element.get("attributes", {}).get("role") == "presentation":
                return AccessibilityIssue(
                    rule_id="img-alt-empty",
                    severity=Severity.WARNING,
                    wcag_level=WCAGLevel.A,
                    message="Image has empty alt text",
                    element=str(html_element),
                    suggestion="If decorative, add role='presentation'. Otherwise, provide descriptive alt text.",
                    wcag_criteria="1.1.1"
                )
        return None
    
    @staticmethod
    def check_heading_hierarchy(headings: List[Dict[str, Any]]) -> List[AccessibilityIssue]:
        """Check for proper heading hierarchy (WCAG 1.3.1)."""
        issues = []
        if not headings:
            return issues
        
        # Check if first heading is h1
        if headings and headings[0].get("tag") != "h1":
            issues.append(AccessibilityIssue(
                rule_id="heading-no-h1",
                severity=Severity.WARNING,
                wcag_level=WCAGLevel.A,
                message="Page should start with an h1 heading",
                suggestion="Add an h1 as the main page heading",
                wcag_criteria="1.3.1"
            ))
        
        # Check for skipped heading levels
        prev_level = 0
        for heading in headings:
            tag = heading.get("tag", "")
            if tag.startswith("h") and len(tag) == 2:
                level = int(tag[1])
                if prev_level > 0 and level > prev_level + 1:
                    issues.append(AccessibilityIssue(
                        rule_id="heading-skipped-level",
                        severity=Severity.ERROR,
                        wcag_level=WCAGLevel.A,
                        message=f"Heading level skipped from h{prev_level} to h{level}",
                        element=str(heading),
                        suggestion=f"Use h{prev_level + 1} instead of h{level}",
                        wcag_criteria="1.3.1"
                    ))
                prev_level = level
        
        return issues
    
    @staticmethod
    def check_form_labels(form_element: Dict[str, Any]) -> Optional[AccessibilityIssue]:
        """Check if form inputs have associated labels (WCAG 1.3.1, 3.3.2)."""
        tag = form_element.get("tag")
        if tag in ["input", "select", "textarea"]:
            input_type = form_element.get("attributes", {}).get("type", "text")
            
            # Skip inputs that don't need labels
            if input_type in ["submit", "button", "reset", "hidden"]:
                return None
            
            # Check for label association
            input_id = form_element.get("attributes", {}).get("id")
            aria_label = form_element.get("attributes", {}).get("aria-label")
            aria_labelledby = form_element.get("attributes", {}).get("aria-labelledby")
            title = form_element.get("attributes", {}).get("title")
            
            if not any([input_id, aria_label, aria_labelledby, title]):
                return AccessibilityIssue(
                    rule_id="form-no-label",
                    severity=Severity.ERROR,
                    wcag_level=WCAGLevel.A,
                    message=f"{tag} element missing label",
                    element=str(form_element),
                    suggestion="Add a label element with for attribute, or use aria-label/aria-labelledby",
                    wcag_criteria="3.3.2"
                )
        return None
    
    @staticmethod
    def check_color_contrast() -> Optional[AccessibilityIssue]:
        """Check color contrast ratios (WCAG 1.4.3, 1.4.6)."""
        # This is a simplified check - real implementation would calculate actual contrast ratio
        # For now, we'll return a warning to manually check contrast
        return AccessibilityIssue(
            rule_id="color-contrast-check",
            severity=Severity.INFO,
            wcag_level=WCAGLevel.AA,
            message="Color contrast should be checked",
            suggestion="Ensure contrast ratio is at least 4.5:1 for normal text, 3:1 for large text",
            wcag_criteria="1.4.3"
        )
    
    @staticmethod
    def check_link_text(link_element: Dict[str, Any]) -> Optional[AccessibilityIssue]:
        """Check if links have descriptive text (WCAG 2.4.4)."""
        if link_element.get("tag") == "a":
            text = link_element.get("text", "").strip()
            aria_label = link_element.get("attributes", {}).get("aria-label")
            
            if not text and not aria_label:
                return AccessibilityIssue(
                    rule_id="link-no-text",
                    severity=Severity.ERROR,
                    wcag_level=WCAGLevel.A,
                    message="Link has no accessible text",
                    element=str(link_element),
                    suggestion="Add link text or aria-label attribute",
                    wcag_criteria="2.4.4"
                )
            
            # Check for non-descriptive link text
            generic_texts = ["click here", "read more", "learn more", "here", "link", "more"]
            if text.lower() in generic_texts and not aria_label:
                return AccessibilityIssue(
                    rule_id="link-generic-text",
                    severity=Severity.WARNING,
                    wcag_level=WCAGLevel.A,
                    message=f"Link text '{text}' is not descriptive",
                    element=str(link_element),
                    suggestion="Use descriptive link text that explains the destination",
                    wcag_criteria="2.4.4"
                )
        return None
    
    @staticmethod
    def check_language_attribute(html_element: Dict[str, Any]) -> Optional[AccessibilityIssue]:
        """Check if HTML has lang attribute (WCAG 3.1.1)."""
        if html_element.get("tag") == "html":
            lang = html_element.get("attributes", {}).get("lang")
            if not lang:
                return AccessibilityIssue(
                    rule_id="html-no-lang",
                    severity=Severity.ERROR,
                    wcag_level=WCAGLevel.A,
                    message="HTML element missing lang attribute",
                    suggestion="Add lang attribute to specify the page language (e.g., lang='en')",
                    wcag_criteria="3.1.1"
                )
        return None
    
    @staticmethod
    def check_aria_roles(element: Dict[str, Any]) -> Optional[AccessibilityIssue]:
        """Check for proper ARIA role usage (WCAG 4.1.2)."""
        role = element.get("attributes", {}).get("role")
        if role:
            # Valid ARIA roles (simplified list)
            valid_roles = {
                "button", "link", "navigation", "main", "banner", "contentinfo",
                "complementary", "search", "form", "region", "alert", "status",
                "dialog", "alertdialog", "menu", "menubar", "menuitem", "tab",
                "tablist", "tabpanel", "toolbar", "tree", "treegrid", "treeitem",
                "grid", "gridcell", "row", "columnheader", "rowheader", "list",
                "listitem", "heading", "img", "presentation", "none"
            }
            
            if role not in valid_roles:
                return AccessibilityIssue(
                    rule_id="aria-invalid-role",
                    severity=Severity.ERROR,
                    wcag_level=WCAGLevel.A,
                    message=f"Invalid ARIA role '{role}'",
                    element=str(element),
                    suggestion=f"Use a valid ARIA role from the WAI-ARIA specification",
                    wcag_criteria="4.1.2"
                )
        return None
    
    @staticmethod
    def check_keyboard_accessibility(element: Dict[str, Any]) -> Optional[AccessibilityIssue]:
        """Check for keyboard accessibility (WCAG 2.1.1)."""
        tag = element.get("tag")
        onclick = element.get("attributes", {}).get("onclick")
        role = element.get("attributes", {}).get("role")
        tabindex = element.get("attributes", {}).get("tabindex")
        
        # Check if non-interactive elements have click handlers without keyboard support
        if onclick and tag not in ["a", "button", "input", "select", "textarea"]:
            if not role in ["button", "link"] and tabindex is None:
                return AccessibilityIssue(
                    rule_id="keyboard-no-access",
                    severity=Severity.ERROR,
                    wcag_level=WCAGLevel.A,
                    message="Clickable element not keyboard accessible",
                    element=str(element),
                    suggestion="Add tabindex='0' and keyboard event handlers, or use a button element",
                    wcag_criteria="2.1.1"
                )
        return None
    
    @staticmethod
    def check_focus_visible(css_rules: List[str]) -> Optional[AccessibilityIssue]:
        """Check if focus indicators are visible (WCAG 2.4.7)."""
        # Look for outline: none without alternative focus styles
        for rule in css_rules:
            if "outline: none" in rule or "outline: 0" in rule:
                if not any(indicator in rule for indicator in ["border", "box-shadow", "background"]):
                    return AccessibilityIssue(
                        rule_id="focus-not-visible",
                        severity=Severity.WARNING,
                        wcag_level=WCAGLevel.AA,
                        message="Focus indicator may be removed without alternative",
                        suggestion="Provide visible focus indicators using border, box-shadow, or background changes",
                        wcag_criteria="2.4.7"
                    )
        return None
    
    @staticmethod
    def check_touch_target_size(element: Dict[str, Any]) -> Optional[AccessibilityIssue]:
        """Check touch target size (WCAG 2.5.5)."""
        tag = element.get("tag")
        role = element.get("attributes", {}).get("role")
        
        if tag in ["button", "a"] or role in ["button", "link"]:
            # This would need actual size calculation in real implementation
            return AccessibilityIssue(
                rule_id="touch-target-size",
                severity=Severity.INFO,
                wcag_level=WCAGLevel.AAA,
                message="Verify touch target is at least 44x44 CSS pixels",
                element=str(element),
                suggestion="Ensure interactive elements are large enough for touch interaction",
                wcag_criteria="2.5.5"
            )
        return None