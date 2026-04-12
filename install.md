
# 🧠 English Premier League VAR Analysis

This project analyzes the impact and trends of VAR (Video Assistant Referee) decisions in the English Premier League using Python and Jupyter Notebooks.

---

## 📁 Project Structure

```
.
├── data/                     # Raw data files (CSV, etc.)
├── notebooks/               # Jupyter notebooks (.ipynb)
├── images/                  # Visualizations for reports
├── .env                     # Environment variables (not committed)
├── requirements.txt         # Python dependencies
├── venv/                    # Virtual environment (optional, gitignored)
└── README.md                # You're reading it!
```

---

## 🛠 Installation Guide

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/English-Premier-League-VAR-Analysis.git
cd English-Premier-League-VAR-Analysis
```

### 2️⃣ Set Up Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate         # macOS/Linux
# OR
venv\Scripts\activate          # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

> If `requirements.txt` doesn’t exist yet:
```bash
pip install pandas matplotlib seaborn jupyter ipykernel
pip freeze > requirements.txt
```

### 4️⃣ (Optional) Add .env File

Create a `.env` file for any API keys or environment variables you want to use:

```env
DEBUG_MODE=True
```

---

## 🧪 Run Notebooks in VS Code

1. Open the project folder in **Visual Studio Code**.
2. Make sure the **Python** extension is installed.
3. Press `Cmd/Ctrl + Shift + P` → **"Python: Select Interpreter"** → choose `./venv` interpreter.
4. Open a notebook (`.ipynb`) and run cells normally.
5. If needed, set your kernel to `venv` (or whatever name you used).

---

## 🧼 Useful Commands

```bash
# Activate venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate         # Windows

# Run Jupyter Notebook (in browser)
jupyter notebook

# Freeze current environment
pip freeze > requirements.txt
```

---

## 📌 Notes

- Make sure `.env` is listed in `.gitignore`
- Data sources are stored locally in `/data`
- Visuals generated go in `/images`

---

## 📬 Contact

Maintained by [Adam Bahrin](https://github.com/adamhkb)  
Open to suggestions, PRs, and collaborations!
