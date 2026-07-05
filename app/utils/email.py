import os
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USER)
FROM_NAME = os.getenv("FROM_NAME", "BharatProblemBase")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")


def send_reset_email(to_email: str, token: str) -> bool:
    if not SMTP_USER or not SMTP_PASS:
        logger.warning(f"SMTP not configured. Reset link for {to_email}: {FRONTEND_URL}/reset-password?token={token}&email={to_email}")
        return False

    reset_url = f"{FRONTEND_URL}/reset-password?token={token}&email={to_email}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Reset Your Password - BharatProblemBase"
    msg["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
    msg["To"] = to_email

    html = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"></head>
    <body style="margin:0;padding:0;background:#f8fafc;font-family:'Helvetica Neue',Arial,sans-serif;">
      <div style="max-width:520px;margin:40px auto;background:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.08);">
        <div style="background:linear-gradient(135deg,#06b6d4,#0891b2);padding:32px;text-align:center;">
          <h1 style="color:#ffffff;font-size:22px;margin:0;">BharatProblemBase</h1>
        </div>
        <div style="padding:32px;">
          <h2 style="color:#1e293b;font-size:20px;margin:0 0 12px;">Reset Your Password</h2>
          <p style="color:#64748b;font-size:14px;line-height:1.6;margin:0 0 24px;">
            We received a request to reset your password. Click the button below to set a new password.
          </p>
          <div style="text-align:center;margin:0 0 24px;">
            <a href="{reset_url}" style="display:inline-block;background:#06b6d4;color:#ffffff;padding:12px 32px;border-radius:10px;text-decoration:none;font-weight:600;font-size:14px;">
              Reset Password
            </a>
          </div>
          <p style="color:#94a3b8;font-size:12px;line-height:1.5;margin:0 0 8px;">
            This link expires in 10 minutes. If you didn't request this, you can safely ignore this email.
          </p>
          <p style="color:#94a3b8;font-size:12px;line-height:1.5;margin:0;">
            If the button doesn't work, copy and paste this URL into your browser:<br>
            <a href="{reset_url}" style="color:#06b6d4;word-break:break-all;">{reset_url}</a>
          </p>
        </div>
      </div>
    </body>
    </html>
    """

    text = f"Reset your password: {reset_url}\n\nThis link expires in 10 minutes."

    msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(FROM_EMAIL, to_email, msg.as_string())
        logger.info(f"Reset email sent to {to_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
        logger.warning(f"Fallback - Reset link: {reset_url}")
        return False


def send_otp_email(to_email: str, otp: str) -> bool:
    if not SMTP_USER or not SMTP_PASS:
        logger.warning(f"SMTP not configured. OTP for {to_email}: {otp}")
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Your Verification Code - BharatProblemBase"
    msg["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
    msg["To"] = to_email

    html = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"></head>
    <body style="margin:0;padding:0;background:#f8fafc;font-family:'Helvetica Neue',Arial,sans-serif;">
      <div style="max-width:520px;margin:40px auto;background:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.08);">
        <div style="background:linear-gradient(135deg,#06b6d4,#0891b2);padding:32px;text-align:center;">
          <h1 style="color:#ffffff;font-size:22px;margin:0;">BharatProblemBase</h1>
        </div>
        <div style="padding:32px;text-align:center;">
          <h2 style="color:#1e293b;font-size:20px;margin:0 0 12px;">Verification Code</h2>
          <p style="color:#64748b;font-size:14px;line-height:1.6;margin:0 0 24px;">
            Use this code to verify your account:
          </p>
          <div style="background:#f0fdfa;border:2px dashed #06b6d4;border-radius:12px;padding:16px;margin:0 0 24px;">
            <span style="font-size:32px;font-weight:700;color:#06b6d4;letter-spacing:8px;">{otp}</span>
          </div>
          <p style="color:#94a3b8;font-size:12px;margin:0;">This code expires in 10 minutes.</p>
        </div>
      </div>
    </body>
    </html>
    """

    msg.attach(MIMEText(f"Your OTP: {otp}", "plain"))
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(FROM_EMAIL, to_email, msg.as_string())
        logger.info(f"OTP email sent to {to_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send OTP email to {to_email}: {e}")
        logger.warning(f"OTP for {to_email}: {otp}")
        return False
