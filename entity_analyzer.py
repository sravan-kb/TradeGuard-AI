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

# Filter SEBI — keep companies only
sebi_df_filtered = sebi_df[
    ~sebi_df["Entity / Individual Name"].astype(str).str.strip().str.match(
        r"^(Mr\.|Mrs\.|Ms\.|Dr\.)",
        re.IGNORECASE
    )
]

company_keywords = [
    "limited", "ltd", "private", "corp", "inc",
    "m/s", "llp", "enterprises", "services", "trading"
]

sebi_df_filtered = sebi_df_filtered[
    sebi_df_filtered["Entity / Individual Name"]
    .astype(str).str.lower()
    .str.contains("|".join(company_keywords), na=False)
]

sebi_companies = (
    sebi_df_filtered["Entity / Individual Name"]
    .astype(str).str.upper()
)

PERSON_INDICATORS = [
    "mr ", "mrs ", "ms ", "dr ",
    "president", "minister", "general",
    "colonel", "senator", "chairman"
]

BLOCKED_TERMS = [
    "india", "china", "russia", "iran", "usa", "america",
    "pakistan", "korea", "africa", "europe", "asia",
    "ukraine", "israel", "syria", "cuba", "sudan"
]

COMPANY_KEYWORDS = [
    "limited", "ltd", "private", "pvt", "corp", "inc",
    "llp", "llc", "enterprises", "services", "trading",
    "industries", "solutions", "technologies", "bank",
    "finance", "capital", "group", "holdings", "international",
    "motors", "chemicals", "pharma", "energy", "consulting",
    "ventures", "associates", "partners", "systems", "networks"
]


def normalize_company_name(name):
    name = str(name).upper()
    remove_words = [
        "LIMITED", "LTD", "PRIVATE", "PVT", "CORPORATION",
        "CORP", "INC", "LLP", "LLC", "&", ",", "."
    ]
    for word in remove_words:
        name = name.replace(word, " ")
    name = re.sub(r"\s+", " ", name)
    return name.strip()


def is_person(name):
    name_lower = name.lower().strip()

    # Check for person title indicators
    for indicator in PERSON_INDICATORS:
        if indicator in name_lower:
            return True

    # If 2-3 words and no company keyword — likely a person
    words = name_lower.split()
    if len(words) in [2, 3]:
        has_company_keyword = any(
            keyword in name_lower
            for keyword in COMPANY_KEYWORDS
        )
        if not has_company_keyword:
            return True

    return False


def check_entity(company_name):

    company_name = company_name.strip()

    if not company_name:
        return {
            "ofac_match": False, "sebi_match": False,
            "matched_ofac": [], "matched_sebi": [],
            "error": "Please enter a company or vendor name."
        }

    if len(company_name) < 4:
        return {
            "ofac_match": False, "sebi_match": False,
            "matched_ofac": [], "matched_sebi": [],
            "error": "Please enter a full company or vendor name."
        }

    if company_name.lower().strip() in BLOCKED_TERMS:
        return {
            "ofac_match": False, "sebi_match": False,
            "matched_ofac": [], "matched_sebi": [],
            "error": "Please enter a company or vendor name, not a country or region."
        }

    if is_person(company_name):
        return {
            "ofac_match": False, "sebi_match": False,
            "matched_ofac": [], "matched_sebi": [],
            "error": "Please enter a company or vendor name, not a person's name."
        }

    search_name = normalize_company_name(company_name)

    # OFAC Check
    entities_only = ofac_df[ofac_df[2].astype(str).str.strip() == "-0-"]
    ofac_names = entities_only[1].astype(str).str.upper()
    ofac_matches = []
    for name in ofac_names:
        normalized = normalize_company_name(name)
        if search_name in normalized:
            ofac_matches.append(name)

    # SEBI Check
    sebi_matches = []
    for name in sebi_companies:
        normalized = normalize_company_name(name)
        if search_name in normalized:
            sebi_matches.append(name)

    ofac_matches = ofac_matches[:3]
    sebi_matches = sebi_matches[:3]

    return {
        "ofac_match": len(ofac_matches) > 0,
        "sebi_match": len(sebi_matches) > 0,
        "matched_ofac": ofac_matches,
        "matched_sebi": [
            s.strip().replace("M/s ", "").replace("M/S ", "")
            for s in sebi_matches
        ],
        "error": None
    }