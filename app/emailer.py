import smtplib
from email.mime.text import MIMEText
from typing import Optional
from app.config import settings

def send_email(to_email: str, subject: str, body: str) -> Optional[str]:
    if not settings.SMTP_HOST or not settings.SMTP_USER or not settings.SMTP_PASS or not settings.SMTP_FROM:
        return "SMTP not configured"
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = settings.SMTP_FROM
    msg["To"] = to_email

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.sendmail(settings.SMTP_FROM, [to_email], msg.as_string())
    return None