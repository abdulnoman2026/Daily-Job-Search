"""
Central configuration — edit this file to change what the agent searches for.
No coding needed elsewhere; everything that changes often lives here.
"""

# ---- Who is applying -------------------------------------------------
CANDIDATE_NAME = "Abdul Noman"
CANDIDATE_EMAIL = "nomankazi887@gmail.com"     # shown inside application emails
CANDIDATE_PHONE = "+92 335 2646059"
PORTFOLIO_URL = "https://abdulnoman-portfolio.netlify.app"

# ---- Roles / keywords to search for -----------------------------------
# The agent searches for each of these terms, one at a time, per country.
SEARCH_TERMS = [
    "graphic designer",
    "web developer",
    "embroidery digitizer",
    "vector artist",
    "wordpress developer",
    "frontend developer",
    "UI designer",
    "AI automation developer",
    "chatbot developer",
]

# Keywords used to SCORE how well a job matches Abdul Noman's real CV.
# The more of these that appear in a job's title/description, the higher it scores.
SKILL_KEYWORDS = [
    "graphic design", "graphic designer", "logo design", "vector", "illustrator",
    "photoshop", "adobe", "embroidery", "digitizing", "digitizer", "wilcom",
    "web developer", "web development", "wordpress", "html", "css", "javascript",
    "php", "responsive", "frontend", "front-end", "ui design", "ui/ux",
    "chatbot", "ai agent", "automation", "python", "email automation",
    "freelance", "remote",
]

# ---- Where to search ----------------------------------------------------
# Adzuna country codes: gb (UK), us (USA), ca (Canada).
# Adzuna does not currently cover UAE or Portugal, so those two are
# covered instead through the remote-job boards below (Remotive, RemoteOK,
# Arbeitnow), which list globally-remote and EU roles.
ADZUNA_COUNTRIES = ["gb", "us", "ca"]

# Simple text match used to flag a job as being for one of the target countries
# when scanning remote-job boards that don't have a country filter.
TARGET_COUNTRY_HINTS = [
    "united kingdom", "uk", "u.k.", "usa", "united states", "u.s.",
    "canada", "dubai", "uae", "united arab emirates", "portugal", "remote",
]

# ---- Matching threshold --------------------------------------------------
MIN_SCORE_TO_KEEP = 2          # a job needs at least this many keyword matches
MAX_JOBS_PER_RUN = 20          # safety cap so one run can't flood your inbox
MAX_AGE_DAYS = 2               # only look at jobs posted in the last N days

# ---- Files ----------------------------------------------------------------
SEEN_JOBS_FILE = "data/seen_jobs.json"
CV_ATTACHMENT_PATH = "assets/Abdul_Noman_CV.docx"
