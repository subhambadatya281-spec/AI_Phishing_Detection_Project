import smtplib
from email.mime.text import MIMEText

EMAIL = "yourgmail@gmail.com"
PASSWORD = "YOUR_APP_PASSWORD"

def send_alert(url, result, risk):

    subject = "⚠️ Phishing Website Detected"

    body = f"""
URL: {url}

Result: {result}

Risk Score: {risk}%
"""

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = EMAIL

    try:

        server = smtplib.SMTP("smtp.gmail.com", 587)

        server.starttls()

        server.login(
            EMAIL,
            PASSWORD
        )

        server.send_message(msg)

        server.quit()

        print("Email Alert Sent")

    except Exception as e:

        print("Email Error:", e)