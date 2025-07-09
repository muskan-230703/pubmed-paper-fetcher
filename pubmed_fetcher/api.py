import requests
from .types import Author, Paper
from .utils import is_non_academic, is_company
import xml.etree.ElementTree as ET

def fetch_pubmed_ids(query: str, retmax: int = 50) -> list:
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {"db": "pubmed", "term": query, "retmax": retmax, "retmode": "json"}
    res = requests.get(url, params=params)
    res.raise_for_status()
    return res.json().get("esearchresult", {}).get("idlist", [])

def fetch_details(pubmed_ids: list) -> list:
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {"db": "pubmed", "id": ",".join(pubmed_ids), "retmode": "xml"}
    res = requests.get(url, params=params)
    res.raise_for_status()
    return parse_papers(res.text)

def parse_papers(xml_data: str) -> list:
    root = ET.fromstring(xml_data)
    papers = []
    for article in root.findall(".//PubmedArticle"):
        pmid = article.findtext(".//PMID")
        title = article.findtext(".//ArticleTitle")
        date = article.findtext(".//PubDate/Year") or "Unknown"

        authors = []
        company_affiliations = set()
        emails = []

        for author in article.findall(".//Author"):
            name_parts = [author.findtext("ForeName"), author.findtext("LastName")]
            name = " ".join(filter(None, name_parts)).strip()
            affiliation = author.findtext(".//Affiliation") or ""
            email = None
            if "@" in affiliation:
                parts = affiliation.split()
                for part in parts:
                    if "@" in part:
                        email = part.strip('.,;')
                        break
            if is_non_academic(affiliation):
                authors.append(Author(name=name, affiliation=affiliation, email=email))
            if is_company(affiliation):
                company_affiliations.add(affiliation)
            if email:
                emails.append(email)

        if authors and company_affiliations:
            papers.append(Paper(
                pubmed_id=pmid,
                title=title,
                publication_date=date,
                non_academic_authors=authors,
                company_affiliations=list(company_affiliations),
                corresponding_email=emails[0] if emails else None
            ))
    return papers
