# get_papers_list/processor.py

import asyncio
import xml.etree.ElementTree as ET
from typing import List, Optional, Tuple

from . import api, analyzer
from .models import Paper

def parse_author_details(author_list_element: ET.Element) -> Tuple[List[Tuple[str, str]], Optional[str]]:
    """Parses author names, affiliations, and corresponding author email."""
    authors = []
    corresponding_email = None
    
    for author_element in author_list_element.findall('Author'):
        last_name = author_element.findtext('LastName', '')
        fore_name = author_element.findtext('ForeName', '')
        name = f"{fore_name} {last_name}".strip()

        affiliation_info = author_element.find('AffiliationInfo')
        affiliation = affiliation_info.findtext('Affiliation', '') if affiliation_info is not None else 'N/A'
        
        authors.append((name, affiliation))

        # Check for corresponding author tag and email
        if author_element.get('ValidYN') == 'Y' and corresponding_email is None:
             if '@' in affiliation:
                # Email is sometimes in the affiliation string
                email_match = ET.re.search(r'[\w\.-]+@[\w\.-]+', affiliation)
                if email_match:
                    corresponding_email = email_match.group(0)

    return authors, corresponding_email


async def process_query(query: str, debug: bool = False) -> List[Paper]:
    """
    The main processing pipeline. Fetches and filters papers based on a query.

    Args:
        query: The user's search query for PubMed.
        debug: If True, prints debug information.

    Returns:
        A list of Paper objects that match the criteria.
    """
    if debug:
        print(f"Fetching paper IDs for query: '{query}'")
    
    try:
        pmids = await api.fetch_paper_ids(query)
        if not pmids:
            if debug:
                print("No paper IDs found for the query.")
            return []
        
        if debug:
            print(f"Found {len(pmids)} paper IDs. Fetching details...")

        xml_data = await api.fetch_paper_details(pmids)
        if not xml_data:
            return []
            
    except Exception as e:
        if debug:
            print(f"An API error occurred: {e}")
        return []

    root = ET.fromstring(xml_data)
    filtered_papers = []

    for article_element in root.findall('.//PubmedArticle'):
        medline_citation = article_element.find('MedlineCitation')
        article = medline_citation.find('Article')
        
        pmid = medline_citation.findtext('PMID')
        title = article.findtext('ArticleTitle', 'No Title Found')
        
        pub_date_element = article.find('.//PubDate')
        year = pub_date_element.findtext('Year', 'N/A')
        month = pub_date_element.findtext('Month', '')
        day = pub_date_element.findtext('Day', '')
        pub_date = f"{year}-{month}-{day}".strip('-')

        author_list = article.find('AuthorList')
        if author_list is None:
            continue

        all_authors, email = parse_author_details(author_list)
        non_academic_authors, companies = analyzer.analyze_authors(all_authors)

        if non_academic_authors:
            paper_data = {
                "PubmedID": pmid,
                "Title": title,
                "PublicationDate": pub_date,
                "Non-academic Author(s)": ", ".join(non_academic_authors),
                "Company Affiliation(s)": ", ".join(companies),
                "Corresponding Author Email": email,
            }
            filtered_papers.append(Paper.model_validate(paper_data))

    if debug:
        print(f"Processing complete. Found {len(filtered_papers)} papers with non-academic authors.")
        
    return filtered_papers