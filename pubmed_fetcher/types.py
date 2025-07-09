from typing import List, Optional
from dataclasses import dataclass

@dataclass
class Author:
    name: str
    affiliation: Optional[str] = None
    email: Optional[str] = None

@dataclass
class Paper:
    pubmed_id: str
    title: str
    publication_date: str
    non_academic_authors: List[Author]
    company_affiliations: List[str]
    corresponding_email: Optional[str] = None
