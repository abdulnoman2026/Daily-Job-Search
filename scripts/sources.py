"""
Pulls raw job listings from public, ToS-friendly job board APIs.
Every job returned here is normalised into the same simple shape:

{
    "id": "unique-string",
    "title": "...",
    "company": "...",
    "location": "...",
    "url": "...",
    "description": "...",
    "source": "adzuna" | "remotive" | "remoteok" | "arbeitnow",
    "apply_email": "someone@company.com" or None
}

Note on scope: LinkedIn and Indeed are deliberately NOT scraped here.
Both actively block and ban automated access, and doing this at scale
risks Abdul Noman's own account. This script only uses sources that
publish an official, public API.
"""

import os
import re
import requests

EMAIL_RE = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")


def _find_email(text):
    if not text:
        return None
    match = EMAIL_RE.search(text)
    return match.group(0) if match else None


def fetch_adzuna(search_term, country, max_days_old=2):
    app_id = os.environ.get("ADZUNA_APP_ID")
    app_key = os.environ.get("ADZUNA_APP_KEY")
    if not app_id or not app_key:
        return []

    url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"
    params = {
        "app_id": app_id,
        "app_key": app_key,
        "what": search_term,
        "max_days_old": max_days_old,
        "results_per_page": 20,
        "content-type": "application/json",
    }
    try:
        r = requests.get(url, params=params, timeout=20)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        print(f"[adzuna] {country} / {search_term}: skipped ({e})")
        return []

    jobs = []
    for item in data.get("results", []):
        desc = item.get("description", "")
        jobs.append({
            "id": f"adzuna-{item.get('id')}",
            "title": item.get("title", "").strip(),
            "company": (item.get("company") or {}).get("display_name", "Unknown"),
            "location": (item.get("location") or {}).get("display_name", country.upper()),
            "url": item.get("redirect_url"),
            "description": desc,
            "source": "adzuna",
            "apply_email": _find_email(desc),
        })
    return jobs


def fetch_remotive(search_term):
    try:
        r = requests.get(
            "https://remotive.com/api/remote-jobs",
            params={"search": search_term},
            timeout=20,
        )
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        print(f"[remotive] {search_term}: skipped ({e})")
        return []

    jobs = []
    for item in data.get("jobs", []):
        desc = item.get("description", "")
        jobs.append({
            "id": f"remotive-{item.get('id')}",
            "title": item.get("title", "").strip(),
            "company": item.get("company_name", "Unknown"),
            "location": item.get("candidate_required_location", "Remote"),
            "url": item.get("url"),
            "description": desc,
            "source": "remotive",
            "apply_email": _find_email(desc),
        })
    return jobs


def fetch_remoteok():
    try:
        r = requests.get(
            "https://remoteok.com/api",
            headers={"User-Agent": "Mozilla/5.0 (job-search-agent)"},
            timeout=20,
        )
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        print(f"[remoteok]: skipped ({e})")
        return []

    jobs = []
    for item in data:
        if "id" not in item:
            continue  # first element is a legal notice, not a job
        desc = item.get("description", "")
        jobs.append({
            "id": f"remoteok-{item.get('id')}",
            "title": item.get("position", "").strip(),
            "company": item.get("company", "Unknown"),
            "location": item.get("location", "Remote"),
            "url": item.get("url"),
            "description": desc,
            "source": "remoteok",
            "apply_email": _find_email(desc),
        })
    return jobs


def fetch_arbeitnow():
    try:
        r = requests.get("https://www.arbeitnow.com/api/job-board-api", timeout=20)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        print(f"[arbeitnow]: skipped ({e})")
        return []

    jobs = []
    for item in data.get("data", []):
        desc = item.get("description", "")
        jobs.append({
            "id": f"arbeitnow-{item.get('slug')}",
            "title": item.get("title", "").strip(),
            "company": item.get("company_name", "Unknown"),
            "location": item.get("location", "Remote / EU"),
            "url": item.get("url"),
            "description": desc,
            "source": "arbeitnow",
            "apply_email": _find_email(desc),
        })
    return jobs


def fetch_all(search_terms, adzuna_countries):
    """Pulls from every source for every search term and returns one flat list."""
    all_jobs = []

    for term in search_terms:
        for country in adzuna_countries:
            all_jobs.extend(fetch_adzuna(term, country))
        all_jobs.extend(fetch_remotive(term))

    # These two boards don't support a per-term query well, so fetch once each.
    all_jobs.extend(fetch_remoteok())
    all_jobs.extend(fetch_arbeitnow())

    # de-duplicate by id
    seen_ids = set()
    unique_jobs = []
    for job in all_jobs:
        if job["id"] not in seen_ids:
            seen_ids.add(job["id"])
            unique_jobs.append(job)
    return unique_jobs
