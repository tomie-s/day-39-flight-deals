# Flight Deals Tracker

A Python automation tool that monitors flight prices and sends email alerts when cheap flights are found — for any destination on your list.

---

## How It Works

1. Reads a list of destinations and target prices from a **Google Sheet** (via Sheety API)
2. Searches for the cheapest available flights using the **Amadeus API** (direct and non-direct)
3. If a price drop is found below the target, sends an **email alert** to all users on the notification list

## Tech Stack

- **Python** — core application logic
- **Amadeus API** — flight search and pricing data
- **Sheety API** — Google Sheets as a lightweight database for destinations and users
- **SMTP** — automated email notifications

## Project Structure

```
├── main.py                  # Entry point
├── flight_search.py         # Amadeus API integration
├── flight_data.py           # Flight data model
├── data_manager.py          # Sheety API (read/write destinations & users)
└── notification_manager.py  # Email notification logic
```

## Setup

```bash
# Install dependencies
pip install requests

# Set environment variables
AMADEUS_API_KEY=your_key
AMADEUS_API_SECRET=your_secret
SHEETY_ENDPOINT=your_endpoint
EMAIL_PROVIDER_PASSWORD=your_password

# Run
python main.py
```

## Features

- Searches both **direct and connecting flights**
- Handles **IATA code lookup** for destination cities automatically
- Sends **formatted email alerts** with price, route, and dates
- Easily extensible destination list via Google Sheets — no code changes needed

---

Built as part of the [100 Days of Code: Python Bootcamp](https://www.udemy.com/course/100-days-of-code/) — Day 39.
