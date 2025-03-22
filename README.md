# ✈️ Cheap Flight Notificator (aka **FlightPulse**)

**FlightPulse** is a Python-based application that helps users track and receive email alerts for the cheapest flight deals based on their preferences. Built using modular architecture, it integrates with the **Amadeus API** for real-time flight data, **Sheety** for easy data storage via Google Sheets, and Gmail SMTP for user notifications.

---

## 🎯 Description
> ***"I will unsheathe my sword by creating the code in my name."***  
> <sub>— Miloš Grujić</sub>

This project is designed to simulate a full-featured **deal notifier for flights**, allowing users to register their information and receive timely email alerts when cheap flight opportunities arise.

In a production environment, the flow would look like this:

1. ✍️ **User signs up** via a Google Form and fills in:
   - Name & email
   - Home airport (current location)
   - List of desired destination cities
   - (Optionally) their "reference low price" for each destination

2. 🧠 The app pulls in this data from a Google Sheet using Sheety, then:
   - Automatically populates missing IATA codes
   - Calls the **Amadeus Flight Offers Search API** to retrieve upcoming flights from their home city to each desired destination
   - Compares current prices to the reference price

3. ✉️ If a deal is found (price below or near reference), it:
   - Sends a **personalized email** to the user
   - Includes current price, departure and arrival details
   - Optionally logs the deal for reporting

4. 🧼 All user and flight data is kept in sync via Sheety and can be viewed/edited by the user via the same Google Sheet.

---

## 🧩 Features

- 🔐 Secure API token management (OAuth2 for Amadeus)
- 🛫 Dynamic IATA code lookup for cities
- 📈 Live flight offer search via Amadeus API
- 📊 Data persistence via Sheety (Google Sheets backend)
- 📬 Personalized deal notifications via email (SMTP)
- 🔁 Auto-updates flight prices & IATA codes in the sheet
- 🧱 Modular OOP structure for easy extensibility
- 📄 Environment variable support via `.env` file

---

## 🚀 Technologies Used

- Python 3
- Amadeus Self-Service API (OAuth2)
- Sheety (Google Sheets API wrapper)
- Gmail SMTP
- `requests`, `dotenv`, `smtplib`, `email.mime`
- `datetime`, `logging`

---

## 🛣️ Future Features & Expansion Ideas

This project is built to be modular and highly extendable. Here’s what can be easily added in the next steps:

- ✅ Web-based user registration with Flask or Django
- 🕓 Scheduled runs via cron jobs or cloud functions
- 📅 More flexible date ranges per user (e.g., “anywhere in July”)
- 📉 Historical price tracking and trend predictions
- 📈 Charted price insights sent to users
- 🌍 Multi-user, multi-region support
- 🔔 Telegram, SMS, or push notifications
- 🔒 Admin interface for managing users, cities, limits
- 🌐 Frontend dashboard showing recent deals

---

## 🖼️ Demo

GIF demo coming soon...

---

## 📂 Project Structure

flight-deal-notificator/ ├── main.py # Main execution logic ├── data_manager.py # Handles Google Sheet read/write ├── flight_data.py # Flight data model & parser ├── flight_search.py # Amadeus API logic ├── notification_manager.py # Email notifications ├── .env.example # Example environment config ├── requirements.txt # Dependencies └── assets/ └── demo.gif # Demo GIF (coming soon)

---

## ⚙️ Setup Instructions

1. **Clone the repo**  

   git clone https://github.com/Gruyanidas/Flight_Pulse.git
   
2. **Install dependencies**

    pip install -r requirements.txt

3. **Create .env file**

    Copy from .env.example and fill in your credentials:

    Amadeus API keys
    Sheety Bearer token
    Gmail login credentials

Prepare your Google Sheet via Sheety
Make sure your Google Sheet includes:

    A prices sheet with cities and reference lowest prices
    A users sheet with name, email, and (optionally) flight preferences

Run the app

    python main.py

 ## 📫 Contact

Made with ❤️ by Miloš Grujić (aka Gruyanidas)
## 📧 milosgrujic1987@gmail.com
## 🪪 License

MIT — feel free to use and adapt, but please credit the original author where possible.


