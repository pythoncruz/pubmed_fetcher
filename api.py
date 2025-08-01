# get_papers_list/api.py

import httpx
from typing import List, Dict, Any

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

async def fetch_paper_ids(query: str, max_papers: int = 50) -> List[str]:
    """
    Fetches PubMed IDs (PMIDs) for a given search query.

    Args:
        query: The search term, following PubMed's advanced query syntax.
        max_papers: The maximum number of paper IDs to return.

    Returns:
        A list of PubMed IDs as strings.
    """
    search_url = f"{BASE_URL}esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_papers,
        "retmode": "json",
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(search_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return data.get("esearchresult", {}).get("idlist", [])

async def fetch_paper_details(pmids: List[str]) -> Dict[str, Any]:
    """
    Fetches the full details for a list of PubMed IDs.

    Args:
        pmids: A list of PubMed IDs.

    Returns:
        A dictionary containing the paper details from the API.
    """
    if not pmids:
        return {}
        
    summary_url = f"{BASE_URL}efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml", 
    }
    async with httpx.AsyncClient() as client:
        # Using POST for potentially long lists of IDs
        response = await client.post(summary_url, data=params)
        response.raise_for_status()
        # We return the raw text to be parsed by a dedicated parser
        return response.text