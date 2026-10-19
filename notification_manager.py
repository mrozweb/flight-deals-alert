import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText

load_dotenv(dotenv_path=".env")


class NotificationManager:
    # This class sends flight-deal email notifications to one or more recipients.

    def __init__(self):
        self.email_from = os.getenv("ENV_EMAIL_FROM")
        self.email_password = os.getenv("ENV_EMAIL_PASSWORD")

        if not self.email_from or not self.email_password:
            raise ValueError(
                "Missing ENV_EMAIL_FROM or ENV_EMAIL_PASSWORD in .env"
            )

    def send_deal_email(self, emails_to, origin_city_iata, city, iata_code,
                        old_price, new_price, out_date, out_time, stops):
        # Normalize to list
        if isinstance(emails_to, str):
            emails_to = [emails_to]

        # Removes None and empty strings
        # Trims whitespace from each item
        # Ensures all items are strings
        emails_to = [str(e).strip() for e in emails_to if e and str(e).strip()]

        if not emails_to:
            print("No valid recipients")
            return

        print(f"Sending to: {emails_to}", flush=True)

        saving = old_price - new_price

        # Flight type
        if stops == 0:
            flight_type = "Direct flight"
        elif stops == 1:
            flight_type = "Indirect (1 stop)"
        else:
            flight_type = f"Indirect ({stops} stops)"

        # HTML body
        body = f"""
        <html>
        <body style="font-family: Arial;">
            <h2>✈️ Flight Deal Found!</h2>
            <p><b>Route:</b> {origin_city_iata} → {iata_code} ({city})</p>
            <p><b>Flight type:</b> {flight_type}</p>
            <p><b>Old price:</b> <s>{old_price:.0f} €</s></p>
            <p style="color: green;"><b>New price:</b> {new_price:.0f} €</p>
            <p style="color: red;"><b>You save:</b> {saving:.0f} €</p>
            <hr>
            <p><b>🛫 Outbound:</b> {out_date} at {out_time}</p>
            <p><i>Book now before the price goes up!</i></p>
        </body>
        </html>
        """

        # One email per recipient
        for recipient in emails_to:
            msg = MIMEText(body, "html", "utf-8")
            msg["Subject"] = (
                f"{flight_type} deal: {origin_city_iata} → {iata_code} ({city}) for {new_price:.0f} €"
            )
            msg["From"] = self.email_from
            msg["To"] = recipient

            try:
                with smtplib.SMTP("smtp.gmail.com", 587, timeout=10) as connection: # Without timeouts: infinite call.
                    connection.starttls()
                    connection.login(self.email_from, self.email_password)
                    connection.send_message(msg)
                print(f"Email sent to {recipient}", flush=True)
            except Exception as e:
                print(f"Failed for {recipient}: {type(e).__name__}: {e}", flush=True)