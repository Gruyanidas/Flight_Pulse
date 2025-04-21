from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flight_data import FlightData
import os, dotenv, smtplib
import logging
logging.basicConfig(level=logging.INFO)
dotenv.load_dotenv()

class NotificationManager:
    """Responsible for comparing prices and sending notification mail to a user"""

    def __init__(self, sheet_data:dict, cheapest_flight:FlightData):
        self.sheet_data = sheet_data["lowestPrice"]
        self.cheapest_flight = cheapest_flight
        self.smtp_address = os.getenv("MY_SMTP_ADRESS")
        self.my_email = os.getenv("GOOGLE_EMAIL")
        self.google_pass = os.getenv("GOOGLE_PASS_KEY")
        self.test_mail = os.getenv("MY_TEST_EMAIL")
        self.fire_symbol = "\U0001F525"

    def is_it_worth_it(self) -> bool:
        if isinstance(self.cheapest_flight, str): #IMPORTANT in case that find_cheapest_flight returns string "NO_DATA"
            print("No valid flight data to compare.")
            return False
        if self.sheet_data >= self.cheapest_flight.price:
            print(f"Wow! You got lucky! Current price is almost like a {self.sheet_data}!")
            return True
        else:
            return False

    def build_message_body(self, destination: str) -> str:
        return (f"There is a great deal going on for a {destination}! "
                f"Current price is {self.cheapest_flight.price}\n"
                f"Departure date: {self.cheapest_flight.departure_date}, "
                f"Arrival: {self.cheapest_flight.arrival_date}")

    def inform_user(self, destination:str, email:str, username:str):
        msg = MIMEMultipart()
        msg["Subject"] = f"{self.fire_symbol} HEY {username}!!! HOT DEAL ALERT! {self.fire_symbol}!"
        msg["From"] = self.my_email
        msg["To"] = email
        msg["Reply-To"] = self.my_email
        message_body = self.build_message_body(destination=destination)

        msg.attach(MIMEText(_text=message_body, _subtype="plain", _charset="utf-8"))  # Ensure body is UTF-8 encoded
        # SENDING EMAIL AS AN INFO
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=self.my_email, password=self.google_pass)
            connection.sendmail(from_addr=self.my_email, to_addrs=email, msg=msg.as_string())

        logging.info(f"Mail sent successfully to {email} for destination {destination}")
