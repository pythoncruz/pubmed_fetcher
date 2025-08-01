# get_papers_list/models.py

from typing import List, Optional
from pydantic import BaseModel, Field

class Author(BaseModel):
    """Represents a single author of a paper."""
    name: str
    affiliation: str

class Paper(BaseModel):
    """Represents a research paper with processed author information."""
    pubmed_id: str = Field(..., alias="PubmedID")
    title: str = Field(..., alias="Title")
    publication_date: str = Field(..., alias="PublicationDate")
    non_academic_authors: List[str] = Field(..., alias="Non-academic Author(s)")
    company_affiliations: List[str] = Field(..., alias="Company Affiliation(s)")
    corresponding_author_email: Optional[str] = Field(None, alias="Corresponding Author Email")