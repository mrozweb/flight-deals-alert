import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText

load_dotenv(dotenv_path=".env")

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.email_from = os.getenv("ENV_EMAIL_FROM")
        self.email_to = os.getenv("ENV_EMAIL_TO")
        self.email_password = os.getenv("ENV_EMAIL_PASSWORD")

    def send_deal_email(self, origin_city_iata, city, iata_code, old_price, new_price, out_date, out_time):
        saving = old_price - new_price

        body = f"""
        <html>
        <body style="font-family: Arial;">
            <h2>✈️ Flight Deal Found!</h2>
            <p><b>Route:</b> LHR → {iata_code} ({city})</p>
            <p><b>Old price:</b> <s>{old_price} €</s></p>
            <p style="color: green;"><b>New price:</b> {new_price} €</p>
            <p style="color: red;"><b>You save:</b> {saving} €</p>
            <hr>
            <p><b>🛫 Outbound:</b> {out_date} at {out_time}</p>
            <p><i>Book now before the price goes up!</i></p>
        </body>
        </html>
        """

        msg = MIMEText(body, "html", "utf-8")
        msg["Subject"] = f"Deal Found: {origin_city_iata} -> {iata_code} for {new_price} €"
        msg["From"] = self.email_from
        msg["To"] = self.email_to

        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(self.email_from, self.email_password)
            connection.send_message(msg)