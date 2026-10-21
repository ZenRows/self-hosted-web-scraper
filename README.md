# How to Build a Self-Hosted Web Scraper From Scratch

A Python web scraper built from scratch with Requests, BeautifulSoup, and Playwright, then tested against protected sites and a documented rate limit to show where a self-hosted scraper stops working. Includes the same targets retrieved through Zenrows Fetch for comparison.

This repository accompanies the Zenrows article [How to Build a Self-Hosted Web Scraper From Scratch](https://www.zenrows.com/blog/self-hosted-web-scraper).

## Features

- Static page scraper using Requests and BeautifulSoup with rotating user agents, full browser header sets, and exponential backoff retries
- Randomized delays between requests to avoid frequency-based blocks
- Structured extraction into dataclasses, written out to CSV
- Playwright headless browser rendering for pages that populate their content with JavaScript
- Diagnostic tests against three protected sites, showing Cloudflare challenge, Varnish edge block, JavaScript challenge, and DataDome responses
- A rate-limit test against GitHub's documented 60 requests per hour for unauthenticated clients
- The same protected targets retrieved through Zenrows Fetch with `mode=auto`
- Every test runs as its own stage, so you can run one step at a time

## Prerequisites

- Python 3.10 or above
- A Zenrows API key for `zenrows_fetch.py` only, available on the [free plan](https://app.zenrows.com/register)
- Chromium, installed through Playwright during setup

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/ZenRows/self-hosted-web-scraper.git
cd self-hosted-web-scraper
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the environment

```bash
# macOS and Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Install the Chromium browser

```bash
python3 -m playwright install chromium
```

## Configuration

Copy `.env.example` to `.env` in the project root and add your key:

```bash
cp .env.example .env
```

```
ZENROWS_API_KEY=your_zenrows_api_key
```

Only `zenrows_fetch.py` reads this. `scraper.py` runs without any credentials.

Get a key by [signing up for Zenrows](https://app.zenrows.com/register). The free plan includes 5,000 credits every month, with no credit card required.

## Project structure

```
.
├── scraper.py
├── zenrows_fetch.py
├── requirements.txt
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
```

- `scraper.py` is the full build: static scraping, Playwright rendering, the protected site tests, and the rate-limit test, each as a stage
- `zenrows_fetch.py` retrieves the same protected targets through Zenrows Fetch
- `.env.example` is the template for your `.env` file

## How it works

The project moves through four stages, each one testing the scraper against a harder target.

```
Static HTML page
  ↓
Requests + BeautifulSoup → works
  ↓
JavaScript-rendered page
  ↓
Requests returns empty fields → Playwright renders → works
  ↓
Protected pages (Cloudflare, Varnish, DataDome)
  ↓
Requests returns 403 → Playwright times out, gets a challenge page, or returns a shell
  ↓
Rate-limited endpoint
  ↓
59 requests succeed, the 60th returns 403
  ↓
Zenrows Fetch (mode=auto) → full content on the protected targets
```

The parsing logic stays the same throughout. Only the fetch layer changes between stages.

## Running the project

### The scraper stages

Name the stage to run. With no argument, `scraper.py` runs `static`.

```bash
python3 scraper.py static      # scrape three pages of the demo store into products.csv
python3 scraper.py dynamic     # Requests on the JavaScript-rendered page (empty fields)
python3 scraper.py rendered    # Playwright on the JavaScript-rendered page
python3 scraper.py protected   # Requests on the three protected targets
python3 scraper.py ratelimit   # up to 70 requests to GitHub's API until the hourly limit hits
python3 scraper.py browser     # Playwright on the three protected targets
```

### The Zenrows comparison

```bash
python3 zenrows_fetch.py
```

## Output

`python3 scraper.py static` writes `products.csv` to the project root with the name, price, and URL of every product scraped across three pages. The other stages print their results to the terminal: empty fields from Requests on the JavaScript page, the rendered products from Playwright, 403s and challenge pages from the protected targets, and the rate-limit cutoff.

`zenrows_fetch.py` prints the response size and page title for each protected target.

Responses from live sites vary by IP, session, time, and each site's configuration, so your output may not match the article exactly.

## Technologies

- Python
- Requests
- BeautifulSoup
- Playwright
- Zenrows

## Related article

This repository accompanies the Zenrows article:

**How to Build a Self-Hosted Web Scraper From Scratch**

https://www.zenrows.com/blog/self-hosted-web-scraper
