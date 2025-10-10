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

 