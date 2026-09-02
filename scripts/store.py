"""
Keeps track of which job IDs have already been processed, so the same
job doesn't get emailed or applied to twice. Stored as a plain JSON file
inside the repo, committed back after every run by the GitHub Actions
workflow.
"""

import json
import os
from config import SEEN_JOBS_FILE


def load_seen():
    if not os.path.exists(SEEN_JOBS_FILE):
        return set()
    with open(SEEN_JOBS_FILE, "r") as f:
        try:
            return set(json.load(f))
        except Exception:
            return set()


def save_seen(seen_ids):
    os.makedirs(os.path.dirname(SEEN_JOBS_FILE), exist_ok=True)
    with open(SEEN_JOBS_FILE, "w") as f:
        json.dump(sorted(seen_ids), f, indent=2)
