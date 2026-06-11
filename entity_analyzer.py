import pandas as pd
import re

# Load OFAC data once
ofac_df = pd.read_csv(
    "data/SDN.CSV",
    header=None,
    encoding="latin1"
)

# Load SEBI data once
sebi_df = pd.read_excel(
    "data/prs_ra_sebi.xls",
    engine="xlrd"
)

# Filter SEBI — keep companies only (remove Mr. Mrs. Ms. Dr.)
sebi_companies = sebi_df[
    ~sebi_df["Entity / Individual Name"].astype(str).str.strip().str.match(
        r"^(Mr\.|Mrs\.|Ms\.|Dr\.)", re.IGNORECASE
    )
]["Entity / Individual Name"].astype(str).str.upper()

PERSON_INDICATORS = [
    "mr ", "mrs ", "ms ", "dr ",
    "president", "minister",
    "general", "colonel",
    "senator", "chairman"
]


def is_person(name):
    name_lower = name.lower().strip()
    for indicator in PERSON_INDICATORS:
        if indicator in name_lower:
            return True
    return False


def check_entity(company_name):

    company_name = company_name.strip()

    if not company_name:
        return {
            "ofac_match": False,
            "sebi_match": False,
            "matched_ofac": None,
            "matched_sebi": None,
            "error": "Please enter a company or vendor name."
        }

    if len(company_name) < 4:
        return {
            "ofac_match": False,
            "sebi_match": False,
            "matched_ofac": None,
            "matched_sebi": None,
            "error": "Please enter a full company or vendor name."
        }

    if is_person(company_name):
        return {
            "ofac_match": False,
            "sebi_match": False,
            "matched_ofac": None,
            "matched_sebi": None,
            "error": "Please enter a company or vendor name, not a person's name."
        }

    search_name = company_name.upper()
    pattern = r"\b" + re.escape(search_name) + r"\b"

    # OFAC Check
    entities_only = ofac_df[ofac_df[2].astype(str).str.strip() == "-0-"]
    ofac_names = entities_only[1].astype(str).str.upper()
    ofac_matches = ofac_names[ofac_names.str.contains(pattern, na=False, regex=True)]

    # SEBI Check
    sebi_matches = sebi_companies[sebi_companies.str.contains(pattern, na=False, regex=True)]

    return {
        "ofac_match": len(ofac_matches) > 0,
        "sebi_match": len(sebi_matches) > 0,
        "matched_ofac": entities_only[1].iloc[ofac_matches.index[0]] if len(ofac_matches) > 0 else None,
        "matched_sebi": sebi_df["Entity / Individual Name"].astype(str).str.strip().str.replace(r'^M/s\s*', '', flags=re.IGNORECASE, regex=True).iloc[sebi_matches.index[0]] if len(sebi_matches) > 0 else None,
        "error": None
    }