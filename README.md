# ✈️ Flight Deals Alert

A Python automation tool that searches for cheap flights, compares them against your target prices, and notifies you by email when a deal is found. Runs automatically every day via GitHub Actions.

---

## 📋 Table of Contents

- [Features](#-features)
- [How It Works](#-how-it-works)
- [Project Structure](#-project-structure)
- [Setup](#-setup)
- [Environment Variables](#-environment-variables)
- [GitHub Actions](#-github-actions)
- [Usage](#-usage)
- [Tech Stack](#-tech-stack)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

---

## ✨ Features

- 🔍 **Automated flight search** using [SerpAPI](https://serpapi.com) (Google Flights engine)
- 💰 **Price comparison** against target prices stored in a Google Sheet via [Sheety](https://sheety.co)
- 📧 **Email notifications** when a deal is found
- 🕒 **Scheduled runs** — checks for deals daily via GitHub Actions
- 💾 **Response caching** to reduce API calls and speed up repeated searches
- 🔐 **Secure secrets management** — no API keys in the code

---

## 🔄 How It Works

1. **Fetch destinations** — pulls the list of cities and target prices from a Google Sheet (via Sheety)
2. **Search flights** — queries SerpAPI for each destination
3. **Compare prices** — checks if any flight is cheaper than the target price
4. **Notify users** — sends an email with the deal details
5. **Repeat daily** — runs automatically via GitHub Actions cron

---

## 📁 Project Structure

```
flight-deals-alert/
├── .github/
│   └── workflows/
│       ├── scheduled.yml        # Daily automated run
│       └── test.yml             # Run tests on push/PR
├── .env                         # Local secrets (NOT pushed)
├── .env.example                 # Template for env vars (pushed)
├── .gitignore                   # Excluded files
├── LICENSE                      # MIT License
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── main.py                      # Entry point
├── data_manager.py              # Handles Sheety (Google Sheets) data
├── flight_data.py               # Flight data class
├── flight_search.py             # SerpAPI flight search logic
└── notification_manager.py      # Email sending logic
```

---

## 🛠 Setup

### Prerequisites

- Python 3.11 or higher
- A [SerpAPI](https://serpapi.com) account (free tier available)
- A [Sheety](https://sheety.co) account linked to a Google Sheet
- An email account with **app password** enabled (e.g., Gmail)

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example file and fill in your real values:

```bash
cp .env.example .env
```

Then edit `.env` with your real credentials (see [Environment Variables](#-environment-variables)).

### 5. Run Locally

```bash
python main.py
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root with the following variables:
## ⚙️ GitHub Actions

This project includes two workflows:

### 1. `scheduled.yml` — Daily Flight Check

Runs automatically every day at **9:00 UTC**. Can also be triggered manually.

- Installs dependencies
- Runs `main.py` with secrets injected
- Uses GitHub Secrets for all sensitive values

### 2. `test.yml` — Run Tests

Runs on every push and pull request to `main`, plus manual trigger.

- Installs dependencies + pytest
- Runs the test suite

---

## 🔑 Adding GitHub Secrets

Since `.env` is not pushed, add each variable as a GitHub Secret:

1. Go to your repo → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add each `ENV_*` variable with its real value

| Secret Name | Value |
|-------------|-------|
| `ENV_SERP_API_KEY` | your SerpAPI key |
| `ENV_SERP_ENDPOINT_GET` | `https://serpapi.com/search` |
| `ENV_SHEETY_ENDPOINT_GET` | your Sheety GET URL |
| `ENV_SHEETY_ENDPOINT_PUT` | your Sheety PUT URL |
| `ENV_SHEETY_ENDPOINT_POST` | your Sheety POST URL |
| `ENV_SHEETY_USERNAME` | your Sheety username |
| `ENV_SHEETY_PASSWORD` | your Sheety password |
| `ENV_SHEETY_AUTH` | your basic auth token |
| `ENV_EMAIL_FROM` | your email |
| `ENV_EMAIL_TO` | recipient email |
| `ENV_EMAIL_PASSWORD` | your app password |
| `ENV_CURRENCY` | `EUR` / `USD` / `GBP` |

---

## 🚀 Usage

### Run Locally

```bash
python main.py
```

### Run in GitHub Actions

1. Go to the **Actions** tab
2. Select **Scheduled Flight Deal Check**
3. Click **Run workflow** → **Run workflow**

---

## 🧰 Tech Stack

| Tool | Purpose |
|------|---------|
| [Python 3.12](https://www.python.org) | Core language |
| [SerpAPI](https://serpapi.com) | Flight search |
| [Sheety](https://sheety.co) | Google Sheets API wrapper |
| [requests](https://requests.readthedocs.io) | HTTP client |
| [requests-cache](https://requests-cache.readthedocs.io) | API response caching |
| [smtplib](https://docs.python.org/3/library/smtplib.html) | Email sending |
| [GitHub Actions](https://github.com/features/actions) | Automation / scheduling |

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `KeyError: 'ENV_SERP_API_KEY'` | Missing secret — add it in GitHub Secrets or `.env` |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| Email not sending | Use an **app password**, not your account password |
| SerpAPI quota exceeded | Check your plan at serpapi.com |
| Workflow didn't run on schedule | Scheduled workflows only run on the default branch (`main`) |
| Cron ran at wrong time | GitHub cron is in **UTC**, not local time |

5. Open a Pull Request

---

## 📄 License

---

## 📬 Contact

**mrozweb**

Project Link: [https://github.com/mrozweb/flight-deals-alert](https://github.com/mrozweb/flight-deals-alert)

---

⭐ If you found this project useful, give it a star!This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [SerpAPI](https://serpapi.com) for the flight search API
- [Sheety](https://sheety.co) for the Google Sheets integration
- [GitHub Actions](https://github.com/features/actions) for free automation

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)

| Variable | Description | Example |
|----------|-------------|---------|
| `ENV_SERP_API_KEY` | Your SerpAPI key | `abc123...` |
| `ENV_SERP_ENDPOINT_GET` | SerpAPI search endpoint | `https://serpapi.com/search` |

> ⚠️ **Never commit your `.env` file.** It's already excluded in `.gitignore`.

---

| `ENV_SHEETY_ENDPOINT_GET` | Sheety GET endpoint (prices) | `https://api.sheety.co/.../prices` |
| `ENV_SHEETY_ENDPOINT_PUT` | Sheety PUT endpoint (update) | `https://api.sheety.co/.../prices` |
| `ENV_SHEETY_ENDPOINT_POST` | Sheety POST endpoint (users) | `https://api.sheety.co/.../users` |
| `ENV_SHEETY_USERNAME` | Sheety username | `your_username` |
| `ENV_SHEETY_PASSWORD` | Sheety password | `your_password` |
| `ENV_SHEETY_AUTH` | Base64 basic auth token | `base64string` |
| `ENV_EMAIL_FROM` | Sender email address | `you@gmail.com` |
| `ENV_EMAIL_TO` | Recipient email address | `recipient@gmail.com` |
| `ENV_EMAIL_PASSWORD` | Email app password | `xxxx xxxx xxxx xxxx` |
| `ENV_CURRENCY` | Currency for price comparison | `EUR`, `USD`, `GBP` |
### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/flight-deals-alert.git
cd flight-deals-alert
```
```

### 3. Install Dependencies


### 2. Create a Virtual Environment

```bash

# Activate on Windows
.venv\Scripts\activate

# Activate on macOS / Linux
source .venv/bin/activate

