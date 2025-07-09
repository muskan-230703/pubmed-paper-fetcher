import argparse
import csv
from pubmed_fetcher.api import fetch_pubmed_ids, fetch_details

def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers with non-academic pharma authors.")
    parser.add_argument("query", type=str, help="Search query for PubMed")
    parser.add_argument("-f", "--file", type=str, help="Output CSV file name")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug output")
    args = parser.parse_args()

    if args.debug:
        print(f"[DEBUG] Query: {args.query}")

    ids = fetch_pubmed_ids(args.query)
    if args.debug:
        print(f"[DEBUG] Fetched {len(ids)} paper IDs")

    papers = fetch_details(ids)

    if args.file:
        with open(args.file, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["PubmedID", "Title", "Publication Date", "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"])
            for paper in papers:
                authors = "; ".join([a.name for a in paper.non_academic_authors])
                affiliations = "; ".join(paper.company_affiliations)
                writer.writerow([paper.pubmed_id, paper.title, paper.publication_date, authors, affiliations, paper.corresponding_email or ""])
    else:
        for paper in papers:
            print("-" * 80)
            print(f"PubmedID: {paper.pubmed_id}\nTitle: {paper.title}\nDate: {paper.publication_date}")
            print(f"Non-academic Authors: {[a.name for a in paper.non_academic_authors]}")
            print(f"Company Affiliations: {paper.company_affiliations}")
            print(f"Corresponding Email: {paper.corresponding_email}")

if __name__ == "__main__":
    main()
