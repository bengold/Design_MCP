"""Official WCAG data loader and utilities."""

import json
import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class WCAGCriterion:
    """Represents a WCAG success criterion."""
    number: str  # e.g., "1.1.1"
    id: str
    title: str
    level: str  # A, AA, AAA
    version: str  # 2.0, 2.1, 2.2
    description: str
    principle: str
    guideline: str
    exceptions: Optional[List[str]] = None


class WCAGDataLoader:
    """Loads and provides access to official WCAG criteria data."""
    
    def __init__(self):
        self._data = None
        self._criteria_by_number = {}
        self._criteria_by_level = {"A": [], "AA": [], "AAA": []}
        self._criteria_by_principle = {}
        self._load_data()
    
    def _load_data(self):
        """Load WCAG data from JSON file."""
        current_dir = os.path.dirname(__file__)
        data_file = os.path.join(current_dir, "wcag_criteria_complete.json")
        
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                self._data = json.load(f)
                self._process_criteria()
        except FileNotFoundError:
            print(f"WCAG data file not found: {data_file}")
            self._data = {"criteria": {}}
    
    def _process_criteria(self):
        """Process criteria data for efficient lookups."""
        for number, criterion_data in self._data.get("criteria", {}).items():
            criterion = WCAGCriterion(
                number=number,
                id=criterion_data["id"],
                title=criterion_data["title"],
                level=criterion_data["level"],
                version=criterion_data["version"],
                description=criterion_data["description"],
                principle=criterion_data["principle"],
                guideline=criterion_data["guideline"],
                exceptions=criterion_data.get("exceptions")
            )
            
            self._criteria_by_number[number] = criterion
            self._criteria_by_level[criterion.level].append(criterion)
            
            if criterion.principle not in self._criteria_by_principle:
                self._criteria_by_principle[criterion.principle] = []
            self._criteria_by_principle[criterion.principle].append(criterion)
    
    def get_criterion(self, number: str) -> Optional[WCAGCriterion]:
        """Get a specific criterion by number (e.g., '1.1.1')."""
        return self._criteria_by_number.get(number)
    
    def get_criteria_by_level(self, level: str) -> List[WCAGCriterion]:
        """Get all criteria for a specific level (A, AA, AAA)."""
        return self._criteria_by_level.get(level, [])
    
    def get_criteria_by_principle(self, principle: str) -> List[WCAGCriterion]:
        """Get all criteria for a specific principle."""
        return self._criteria_by_principle.get(principle, [])
    
    def get_all_criteria(self) -> List[WCAGCriterion]:
        """Get all WCAG criteria."""
        return list(self._criteria_by_number.values())
    
    def search_criteria(self, search_term: str) -> List[WCAGCriterion]:
        """Search criteria by title, description, or guideline."""
        search_term = search_term.lower()
        results = []
        
        for criterion in self._criteria_by_number.values():
            if (search_term in criterion.title.lower() or
                search_term in criterion.description.lower() or
                search_term in criterion.guideline.lower()):
                results.append(criterion)
        
        return results
    
    def get_criteria_for_techniques(self, technique_type: str) -> List[WCAGCriterion]:
        """Get criteria relevant to specific technique types (e.g., 'images', 'forms', 'color')."""
        technique_mappings = {
            "images": ["1.1.1", "1.4.5", "1.4.9"],
            "forms": ["1.3.1", "3.3.1", "3.3.2", "3.3.3", "3.3.4", "4.1.2"],
            "color": ["1.4.1", "1.4.3", "1.4.6", "1.4.11"],
            "keyboard": ["2.1.1", "2.1.2", "2.1.4", "2.4.3", "2.4.7"],
            "headings": ["1.3.1", "2.4.6", "2.4.10"],
            "links": ["2.4.4", "2.4.9", "4.1.2"],
            "language": ["3.1.1", "3.1.2"],
            "media": ["1.2.1", "1.2.2", "1.2.3", "1.2.4", "1.2.5", "1.2.6", "1.2.7", "1.2.8", "1.2.9"],
            "timing": ["2.2.1", "2.2.2", "2.2.3", "2.2.4", "2.2.5", "2.2.6"],
            "seizures": ["2.3.1", "2.3.2", "2.3.3"],
            "navigation": ["2.4.1", "2.4.2", "2.4.5", "2.4.8", "3.2.3", "3.2.4"],
            "input": ["1.3.5", "2.5.1", "2.5.2", "2.5.3", "2.5.4", "2.5.6", "3.3.7", "3.3.8"],
            "focus": ["2.4.7", "2.4.11", "2.4.12", "2.4.13"]
        }
        
        numbers = technique_mappings.get(technique_type.lower(), [])
        return [self._criteria_by_number[num] for num in numbers if num in self._criteria_by_number]
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get metadata about the WCAG data."""
        return self._data.get("metadata", {}) if self._data else {}
    
    def get_principles(self) -> List[str]:
        """Get all WCAG principles."""
        return ["Perceivable", "Operable", "Understandable", "Robust"]
    
    def get_guidelines_for_principle(self, principle: str) -> List[str]:
        """Get all guidelines for a specific principle."""
        criteria = self.get_criteria_by_principle(principle)
        guidelines = list(set(c.guideline for c in criteria))
        return sorted(guidelines)


# Global instance
wcag_data = WCAGDataLoader()