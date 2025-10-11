# 🧰 Setup Guide for `ftw-python-ingestion`

This guide walks you through installing **Python**, **Git**, and **uv**, then cloning and running the repository
➡️ [Repo link](https://github.com/ogbinar/ftw-python-ingestion)

---

## 1️⃣ Install Python

### 🪟 Windows

1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download the **latest Python 3.11 or 3.12** installer.
3. **Check** ✅ “Add Python to PATH” during installation.
4. Verify installation:

   ```bash
   python --version
   ```

### 🐧 Linux (Ubuntu / Debian)

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
python3 --version
```

### 🍎 macOS

Install using [Homebrew](https://brew.sh):

```bash
brew install python
python3 --version
```

---

## 2️⃣ Install Git

Git is required to clone the repository.

### Windows

* Download and install from [git-scm.com/downloads](https://git-scm.com/downloads)
* Verify:

  ```bash
  git --version
  ```

### Linux

```bash
sudo apt install git -y
git --version
```

### macOS

```bash
brew install git
git --version
```

---

## 3️⃣ Install `uv` (Python project manager)

👉 Official instructions: [docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)

### Universal one-liner

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

After installation, verify:

```bash
uv --version
```

If not found, restart your terminal or add `~/.local/bin` to your PATH.

---

## 4️⃣ Clone the repository

```bash
git clone https://github.com/ogbinar/ftw-python-ingestion.git
cd ftw-python-ingestion
```

---

## 5️⃣ Create and activate a virtual environment

```bash
uv venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
```

---

## 6️⃣ Install dependencies

```bash
uv pip install -r requirements.txt
```

If you plan to use **Playwright** (for `05-webscrape-pw.py`):

```bash
python -m playwright install
```

---

## 7️⃣ Run the example scripts

Each script shows a different data ingestion method.

```bash
python 01-flat-files.py      # Read CSV, TSV, JSON, XML, YAML, HTML
python 02-database.py        # Query SQLite (Chinook DB)
python 03-api.py             # Fetch data from a JSON API
python 04-webscrape-bs.py    # Scrape with BeautifulSoup
python 05-webscrape-api.py   # Scrape hidden JSON API
python 05-webscrape-pw.py    # Scrape Lazada (Playwright)
```

All output files will appear in the `output/` folder.

---

## 8️⃣ Optional: folder prep

```bash
mkdir -p data output
```

Place your inputs (like `chinook.db` or sample CSVs) in the `data/` folder.

# 🧠 Data Ingestion in Python — Mini Lecture and Guide

This repository demonstrates **five fundamental ways to bring data into Python**, from simple flat files to dynamic web scraping.
Each script introduces a new data ingestion concept and a set of important libraries for data engineers and analysts.

---

## 🗂️ 01 — Flat Files (`01-flat-files.py`)

### 💡 Concept

Reading **structured and semi-structured files** (CSV, TSV, JSON, XML, YAML, HTML) into **pandas DataFrames** — the foundation of most data work.

### 🧰 Key Libraries

* **pandas** – handles tabular data, file I/O, and transformations.
* **yaml** – parses YAML configuration-style data.

### 🧠 Core Idea

> Data often comes in different formats — pandas can unify them all into a consistent DataFrame structure.

### 🏃 Example

```python
pd.read_csv("data/test.csv")
pd.read_json("data/test.json")
pd.read_xml("data/test.xml")
pd.read_html("data/test.html")[0]
```

---

## 🏦 02 — Database Access (`02-database.py`)

### 💡 Concept

Querying a **relational database** directly from Python, using **Ibis** to abstract SQL.

### 🧰 Key Libraries

* **ibis** – a high-level data query framework that works across multiple backends (SQLite, Postgres, DuckDB, etc.).
* **pandas** – to collect query results and export to CSV.

### 🧠 Core Idea

> Instead of writing SQL manually, you can express queries with Python syntax — portable across databases.

### 🏃 Example

```python
con = ibis.sqlite.connect("data/chinook.db")
invoices = con.table("invoices")
customers = con.table("customers")
joined = invoices.join(customers, "CustomerId")
result = joined.group_by("Country").aggregate(avg_invoice=invoices.Total.mean())
```

---

## ☁️ 03 — API Data (`03-api.py`)

### 💡 Concept

Accessing **remote APIs** that serve **JSON** data over HTTP — a common pattern for weather, finance, or social media data.

### 🧰 Key Libraries

* **requests** – makes HTTP requests easily.
* **pandas** – normalizes and structures JSON responses.

### 🧠 Core Idea

> APIs provide machine-readable data. You can treat them as live data sources for analytics pipelines.

### 🏃 Example

```python
response = requests.get("https://api.open-meteo.com/v1/forecast", params={"latitude": 14.6, "longitude": 121.0})
data = response.json()
df = pd.json_normalize(data)
```

---

## 🌐 04 — Web Scraping (HTML) (`04-webscrape-bs.py`)

### 💡 Concept

Extracting **structured information from web pages** using HTML parsing.

### 🧰 Key Libraries

* **requests** – fetches the HTML content.
* **BeautifulSoup (bs4)** – parses and navigates the HTML DOM.
* **pandas** – stores the extracted table data.

### 🧠 Core Idea

> When data isn’t available via API, you can extract it from a site’s HTML structure — carefully and ethically.

### 🏃 Example

```python
soup = BeautifulSoup(requests.get(url).text, "html.parser")
table = soup.find("table", {"class": "wikitable"})
rows = [[td.get_text(strip=True) for td in tr.find_all("td")] for tr in table.find_all("tr")]
df = pd.DataFrame(rows)
```

---

## ⚙️ 05 — Web API Scraping (Hidden JSON) (`05-webscrape-api.py`)

### 💡 Concept

Some websites fetch data dynamically from hidden **JSON endpoints** — the same APIs the browser uses.

### 🧰 Key Libraries

* **requests** – calls the hidden API directly.
* **pandas** – converts JSON into CSV-ready format.

### 🧠 Core Idea

> Instead of parsing HTML, you can often find the underlying API and access clean, structured JSON data.

### 🏃 Example

```python
r = requests.get("https://quotes.toscrape.com/api/quotes?page=1")
data = r.json()
df = pd.DataFrame([{"text": q["text"], "author": q["author"]["name"]} for q in data["quotes"]])
```

---

## 🤖 06 — Dynamic Web Scraping with Playwright (`05-webscrape-pw.py`)

### 💡 Concept

Handling **JavaScript-rendered sites** where HTML content loads dynamically after page load.

### 🧰 Key Libraries

* **Playwright** – automates browsers (Chromium, Firefox, WebKit).
* **pandas** – structures the collected data.
* **re** – cleans and extracts specific text patterns.

### 🧠 Core Idea

> When traditional scraping fails (because of JavaScript), use a **headless browser** to load and interact with the page like a human.

### 🏃 Example

```python
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.lazada.com.ph/")
    page.wait_for_selector(".card-jfy-item-desc")
    # extract product info from visible cards...
```

---

## 🎓 Key Takeaways

| Technique        | Data Source     | Toolset                     | Concept                |
| ---------------- | --------------- | --------------------------- | ---------------------- |
| Flat Files       | Local files     | `pandas`, `yaml`            | DataFrames from files  |
| Database         | SQL / SQLite    | `ibis`                      | Pythonic SQL           |
| Public API       | REST JSON       | `requests`, `pandas`        | Remote data ingestion  |
| Web HTML         | Web pages       | `requests`, `BeautifulSoup` | HTML scraping          |
| Hidden API       | Dynamic sites   | `requests`                  | JSON endpoint scraping |
| Browser Scraping | JS-driven pages | `Playwright`                | Headless automation    |

---

### 💬 Instructor Notes

* Start with **pandas** for flat file reading — it’s the “hello world” of data ingestion.
* Move to **Ibis** to understand data abstraction and query portability.
* Explore **requests** + **BeautifulSoup** to grasp HTTP and HTML parsing.
* Use **Playwright** for advanced, real-world scraping tasks.

> Together, these form the core ingestion toolkit for any data engineer or data scientist.
