"""
Entry point — this is what the GitHub Actions workflow runs once a day.

Flow:
  1. Fetch jobs from every source.
  2. Score + filter against Abdul Noman's real skills and target countries.
  3. Drop anything already seen in a previous run.
  4. Split into:
       - auto_applied  -> job listed a public apply email -> real email sent automatically
       - manual_queue  -> everything else -> listed in the daily email + WhatsApp ping,
                          for a one-click apply (protects against LinkedIn/Indeed bot bans)
  5. Send the daily summary email + WhatsApp notification.
  6. Save the updated seen-jobs list.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from config import (
    SEARCH_TERMS, ADZUNA_COUNTRIES, MAX_JOBS_PER_RUN,
    CANDIDATE_NAME, PORTFOLIO_URL,
)
from sources import fetch_all
from matcher import filter_and_score
from store import load_seen, save_seen
from ai_pitch import one_line_pitch, cover_email_body
from emailer import send_application_email, send_daily_summary
from whatsapp import send_whatsapp_summary

CANDIDATE_SUMMARY = (
    "Graphic designer, web developer, and senior embroidery digitizer with "
    "10+ years of experience: logo and vector design, Wilcom embroidery "
    "digitizing, WordPress/PHP websites, and recent work building AI chat "
    "and voice automation tools for a small business."
)


def main():
    print("Fetching jobs from all sources...")
    raw_jobs = fetch_all(SEARCH_TERMS, ADZUNA_COUNTRIES)
    print(f"Fetched {len(raw_jobs)} raw listings.")

    scored_jobs = filter_and_score(raw_jobs)
    print(f"{len(scored_jobs)} jobs matched the skill/location filter.")

    seen = load_seen()
    fresh_jobs = [j for j in scored_jobs if j["id"] not in seen]
    fresh_jobs = fresh_jobs[:MAX_JOBS_PER_RUN]
    print(f"{len(fresh_jobs)} are new since the last run.")

    auto_applied = []
    manual_queue = []

    for job in fresh_jobs:
        if job.get("apply_email"):
            body = cover_email_body(job, CANDIDATE_SUMMARY, CANDIDATE_NAME, PORTFOLIO_URL)
            success = send_application_email(job, body)
            if success:
                auto_applied.append(job)
            else:
                job["pitch"] = one_line_pitch(job, CANDIDATE_SUMMARY)
                manual_queue.append(job)
        else:
            job["pitch"] = one_line_pitch(job, CANDIDATE_SUMMARY)
            manual_queue.append(job)

    send_daily_summary(auto_applied, manual_queue)
    send_whatsapp_summary(len(auto_applied), len(manual_queue))

    seen.update(j["id"] for j in fresh_jobs)
    save_seen(seen)

    print(f"Done. Auto-applied: {len(auto_applied)}. Manual queue: {len(manual_queue)}.")


if __name__ == "__main__":
    main()
