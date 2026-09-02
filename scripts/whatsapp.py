"""
Sends a short WhatsApp notification using CallMeBot (free service).

One-time setup needed before this works — see README.md, "WhatsApp setup".
"""

import os
import requests


def send_whatsapp_summary(auto_applied_count, manual_queue_count):
    phone = os.environ.get("WHATSAPP_PHONE")
    apikey = os.environ.get("CALLMEBOT_APIKEY")
    if not phone or not apikey:
        print("[whatsapp] WHATSAPP_PHONE or CALLMEBOT_APIKEY not set — skipping.")
        return

    if auto_applied_count == 0 and manual_queue_count == 0:
        text = "Job search ran today — no new matching jobs. Check back tomorrow."
    else:
        text = (
            f"Job search update: {auto_applied_count} application(s) sent automatically, "
            f"{manual_queue_count} more ready for you to review and click-apply. "
            f"Full list is in your email."
        )

    try:
        requests.get(
            "https://api.callmebot.com/whatsapp.php",
            params={"phone": phone, "text": text, "apikey": apikey},
            timeout=20,
        )
    except Exception as e:
        print(f"[whatsapp] failed to send: {e}")
