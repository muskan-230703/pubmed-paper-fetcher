def is_non_academic(affiliation: str) -> bool:
    if not affiliation:
        return False
    academic_keywords = ["university", "institute", "college", "school", "department", "hospital", "clinic", "center"]
    return not any(keyword in affiliation.lower() for keyword in academic_keywords)

def is_company(affiliation: str) -> bool:
    company_keywords = ["pharma", "biotech", "therapeutics", "labs", "inc", "ltd", "gmbh", "llc"]
    return any(keyword in affiliation.lower() for keyword in company_keywords)
