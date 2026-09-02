"""
Sends real emails through Gmail's SMTP server:
  1. Tailored application emails (with CV attached) for jobs that have a
     public apply-by-email address.
  2. One daily summary email listing every other matched job, with a
     ready-to-click link and a one-line "why this fits" note.
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from config import CANDIDATE_NAME, CANDIDATE_EMAIL, CANDIDATE_PHONE, CV_ATTACHMENT_PATH


def _smtp_connection():
    gmail_address = os.environ["GMAIL_ADDRESS"]
    gmail_app_password = os.environ["GMAIL_APP_PASSWORD"]
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(gmail_address, gmail_app_password)
    return server, gmail_address


def send_application_email(job, body_text):
    """Sends a real application email with the CV attached. Returns True/False."""
    server, gmail_address = _smtp_connection()

    msg = MIMEMultipart()
    msg["From"] = gmail_address
    msg["To"] = job["apply_email"]
    msg["Subject"] = f"Application: {job['title']} — {CANDIDATE_NAME}"

    full_body = (
        f"{body_text}\n\n"
        f"{CANDIDATE_NAME}\n{CANDIDATE_EMAIL} | {CANDIDATE_PHONE}"
    )
    msg.attach(MIMEText(full_body, "plain"))

    if os.path.exists(CV_ATTACHMENT_PATH):
        with open(CV_ATTACHMENT_PATH, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        filename = os.path.basename(CV_ATTACHMENT_PATH)
        part.add_header("Content-Disposition", f"attachment; filename={filename}")
        msg.attach(part)

    try:
        server.sendmail(gmail_address, [job["apply_email"], gmail_address], msg.as_string())
        return True
    except Exception as e:
        print(f"[emailer] failed to send application for {job['title']}: {e}")
        return False
    finally:
        server.quit()


def send_daily_summary(auto_applied, manual_queue):
    server, gmail_address = _smtp_connection()

    lines = []
    lines.append(f"Job search run — {len(auto_applied)} auto-applied, {len(manual_queue)} to review.\n")

    if auto_applied:
        lines.append("=== AUTO-APPLIED (email sent automatically) ===")
        for job in auto_applied:
            lines.append(f"- {job['title']} at {job['company']} ({job['location']}) -> {job['apply_email']}")
        lines.append("")

    if manual_queue:
        lines.append("=== READY TO APPLY (click to submit yourself — LinkedIn/Indeed-style forms) ===")
        for job in manual_queue:
            pitch = job.get("pitch", "")
            lines.append(f"- {job['title']} at {job['company']} ({job['location']}) [score {job['score']}]")
            lines.append(f"  {pitch}")
            lines.append(f"  {job['url']}")
            lines.append("")

    body = "\n".join(lines) if (auto_applied or manual_queue) else "No new matching jobs today."

    msg = MIMEMultipart()
    msg["From"] = gmail_address
    msg["To"] = gmail_address
    msg["Subject"] = f"Daily job search: {len(auto_applied)} applied, {len(manual_queue)} to review"
    msg.attach(MIMEText(body, "plain"))

    try:
        server.sendmail(gmail_address, [gmail_address], msg.as_string())
    except Exception as e:
        print(f"[emailer] failed to send daily summary: {e}")
    finally:
        server.quit()
