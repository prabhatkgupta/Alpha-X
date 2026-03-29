"""Send notifications via Telegram Bot API (no sandbox / Meta setup)."""

import json
import os
import ssl
import urllib.error
import urllib.request

import certifi

from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


def _telegram_ssl_context():
    """
    Use certifi's CA bundle (fixes many macOS / Python SSL: CERTIFICATE_VERIFY_FAILED).
    Set TELEGRAM_INSECURE_SSL=1 only if a corporate proxy replaces certs (insecure).
    """
    if os.getenv("TELEGRAM_INSECURE_SSL", "").strip().lower() in ("1", "true", "yes"):
        return ssl._create_unverified_context()
    return ssl.create_default_context(cafile=certifi.where())


class TelegramClient:
    """Client for sending messages through a Telegram bot."""

    def __init__(self):
        self.bot_token = TELEGRAM_BOT_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID

    def _api_url(self, method: str) -> str:
        return f"https://api.telegram.org/bot{self.bot_token}/{method}"

    def send_message(self, text: str) -> bool:
        if not self.bot_token or not self.chat_id:
            print("❌ TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID is not set")
            return False

        payload = json.dumps(
            {"chat_id": self.chat_id, "text": text, "disable_web_page_preview": True}
        ).encode("utf-8")

        req = urllib.request.Request(
            self._api_url("sendMessage"),
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            ctx = _telegram_ssl_context()
            with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
                raw = resp.read().decode("utf-8")
            data = json.loads(raw)
            if not data.get("ok"):
                print(f"❌ Telegram API error: {data.get('description', raw)}")
                return False
            print("✅ Message sent successfully (Telegram)")
            return True
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            print(f"❌ Telegram HTTP error: {e.code} {body}")
            return False
        except Exception as e:
            print(f"❌ Error sending Telegram message: {e}")
            return False

    def send_weekly_report(self, report: str) -> bool:
        message = f"🎯 Your Weekly Insights\n\n{report}"
        max_len = 4096
        if len(message) > max_len:
            print("⚠️ Message too long, truncating...")
            message = message[: max_len - 40] + "\n\n... (truncated)"
        return self.send_message(message)

    def send_monthly_report(self, report: str) -> bool:
        message = f"🎯 Hey, Your Monthly Insights\n\n{report}"
        max_len = 4096
        if len(message) > max_len:
            print("⚠️ Message too long, truncating...")
            message = message[: max_len - 40] + "\n\n... (truncated)"
        return self.send_message(message)

    def test_connection(self) -> bool:
        return self.send_message("🤖 Alpha-X Test\n\nIf you received this, Telegram setup works!")
