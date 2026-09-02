"""
Optional layer: if an ANTHROPIC_API_KEY secret is set, this asks Claude to
write a short, specific one-line pitch for each job, and a short cover-email
body for jobs going into the auto-apply bucket.

If no key is set, everything falls back to a simple template — the system
still works fully without this, just with slightly generic wording.
"""

import os
import requests

API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-haiku-4-5-20251001"


def _call_claude(prompt, max_tokens=200):
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return None
    try:
        r = requests.post(
            API_URL,
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": MODEL,
                "max_tokens": max_tokens,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=30,
        )
        r.raise_for_status()
        data = r.json()
        return "".join(
            block.get("text", "") for block in data.get("content", [])
            if block.get("type") == "text"
        ).strip()
    except Exception as e:
        print(f"[ai_pitch] Claude call skipped ({e})")
        return None


def one_line_pitch(job, candidate_summary):
    prompt = (
        f"Candidate background: {candidate_summary}\n\n"
        f"Job title: {job['title']}\n"
        f"Company: {job['company']}\n"
        f"Job description (excerpt): {job.get('description','')[:600]}\n\n"
        "Write exactly one short sentence (under 25 words) explaining why this "
        "candidate is a good fit for this specific job. Be concrete, not generic. "
        "Return only the sentence, nothing else."
    )
    result = _call_claude(prompt, max_tokens=80)
    if result:
        return result
    matched = ", ".join(job.get("matched_keywords", [])[:4])
    return f"Matches your background in {matched}."


def cover_email_body(job, candidate_summary, candidate_name, portfolio_url):
    prompt = (
        f"Write a short, warm, professional job application email body (under 120 words), "
        f"no subject line, no greeting placeholder brackets. "
        f"Candidate: {candidate_name}. Background: {candidate_summary}. "
        f"Portfolio: {portfolio_url}. "
        f"Applying for: {job['title']} at {job['company']}. "
        f"Job description excerpt: {job.get('description','')[:600]}\n\n"
        "Sign off with the candidate's name only, no extra contact details (those are added separately)."
    )
    result = _call_claude(prompt, max_tokens=250)
    if result:
        return result

    return (
        f"Hello,\n\n"
        f"I'm writing to apply for the {job['title']} position at {job['company']}. "
        f"I'm a graphic designer, web developer, and senior embroidery digitizer with "
        f"10+ years of experience, and I believe my background lines up well with this role.\n\n"
        f"You can see samples of my work here: {portfolio_url}\n\n"
        f"I've attached my CV and would welcome the chance to discuss further.\n\n"
        f"Best regards,\n{candidate_name}"
    )
