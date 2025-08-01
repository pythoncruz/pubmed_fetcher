# get_papers_list/analyzer.py

import re
from typing import List, Tuple

# Keywords that suggest an academic or non-profit institution
ACADEMIC_KEYWORDS = [
    'university', 'college', 'school', 'institute', 'hospital', 'academic',
    'medical center', 'research center', 'foundation'
]

# Keywords that strongly suggest a corporate affiliation
COMPANY_KEYWORDS = [
    'inc', 'ltd', 'llc', 'corp', 'pharmaceuticals', 'biotech',
    'therapeutics', 'diagnostics', 'solutions', 'ventures'
]

def is_corporate_affiliation(affiliation: str) -> bool:
    """
    Determines if an affiliation is likely corporate based on keywords.

    Args:
        affiliation: The affiliation string of an author.

    Returns:
        True if the affiliation seems corporate, False otherwise.
    """
    if not isinstance(affiliation, str) or not affiliation:
        return False

    lower_affiliation = affiliation.lower()

    # If it contains a strong company keyword, it's likely corporate
    if any(keyword in lower_affiliation for keyword in COMPANY_KEYWORDS):
        return True

    # If it contains an academic keyword, it's likely not corporate
    if any(keyword in lower_affiliation for keyword in ACADEMIC_KEYWORDS):
        return False
    
    # As a final check, if it has a mix, we assume non-corporate unless a strong indicator is present.
    # Simple heuristic: If it doesn't sound academic, it might be corporate.
    # This can be expanded with a more sophisticated list of companies.
    # For now, we return True if no academic keywords were found.
    return not any(keyword in lower_affiliation for keyword in ACADEMIC_KEYWORDS)


def analyze_authors(authors: List[Tuple[str, str]]) -> Tuple[List[str], List[str]]:
    """
    Analyzes a list of authors to find non-academic ones and their companies.

    Args:
        authors: A list of tuples, where each tuple is (author_name, affiliation).

    Returns:
        A tuple containing two lists: non-academic author names and their company affiliations.
    """
    non_academic_authors = []
    company_affiliations = set()

    for name, affiliation in authors:
        if is_corporate_affiliation(affiliation):
            non_academic_authors.append(name)
            company_affiliations.add(affiliation)
            
    return non_academic_authors, sorted(list(company_affiliations))