"""
Scores each job against Abdul Noman's real skill set, and flags whether
it looks relevant to one of the target countries / remote work.
"""

from config import SKILL_KEYWORDS, TARGET_COUNTRY_HINTS, MIN_SCORE_TO_KEEP


def score_job(job):
    text = f"{job.get('title','')} {job.get('description','')}".lower()
    matched = [kw for kw in SKILL_KEYWORDS if kw in text]
    return len(matched), matched


def looks_like_target_location(job):
    text = f"{job.get('location','')} {job.get('description','')}".lower()
    return any(hint in text for hint in TARGET_COUNTRY_HINTS)


def filter_and_score(jobs):
    """Returns jobs that meet the minimum score, each annotated with
    'score' and 'matched_keywords', sorted best-first."""
    kept = []
    for job in jobs:
        score, matched = score_job(job)
        if score < MIN_SCORE_TO_KEEP:
            continue
        if not looks_like_target_location(job):
            continue
        job["score"] = score
        job["matched_keywords"] = matched
        kept.append(job)

    kept.sort(key=lambda j: j["score"], reverse=True)
    return kept
