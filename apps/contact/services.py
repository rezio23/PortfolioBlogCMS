import json
import logging
from html import escape
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from django.conf import settings
from django.utils import timezone


logger = logging.getLogger(__name__)


def _format_created_at(contact_message):
    if not contact_message.created_at:
        return "Unknown"
    return timezone.localtime(contact_message.created_at).strftime("%Y-%m-%d %H:%M:%S %Z")


def build_telegram_contact_message(contact_message):
    return "\n".join(
        [
            "<b>New contact message</b>",
            f"<b>Name:</b> {escape(contact_message.name)}",
            f"<b>Email:</b> {escape(contact_message.email)}",
            f"<b>Subject:</b> {escape(contact_message.subject)}",
            f"<b>Sent:</b> {_format_created_at(contact_message)}",
            "",
            "<b>Message:</b>",
            escape(contact_message.message),
        ]
    )


def send_contact_message_to_telegram(contact_message):
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CONTACT_CHAT_ID

    if not token or not chat_id:
        return False

    payload = json.dumps(
        {
            "chat_id": chat_id,
            "text": build_telegram_contact_message(contact_message),
            "parse_mode": "HTML",
        }
    ).encode("utf-8")
    request = Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=settings.TELEGRAM_API_TIMEOUT) as response:
            body = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, OSError, json.JSONDecodeError) as exc:
        logger.warning("Telegram contact notification failed: %s", exc)
        return False

    if not body.get("ok"):
        logger.warning("Telegram contact notification failed: %s", body)
        return False

    return True