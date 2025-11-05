# Quick Start - Run JDMI Assessment Locally

## Simple 3-Step Setup

### 1️⃣ Install Dependencies
```bash
cd "/Users/dslightham/Library/CloudStorage/Dropbox/4_Utility/CODE/JDX/2_Tactics/Campaigns/JDX_SkillsGov_Campaign_2025Q4/Streamlit"
pip3 install -r requirements.txt
```

### 2️⃣ Run the App
```bash
python3 -m streamlit run app.py
```

### 3️⃣ Open in Browser
The app will automatically open at: **http://localhost:8501**

---

## What You'll See

1. **Assessment Form** — 7 dimension questions (5-7 minutes)
2. **Results Dashboard** — Score, level, radar chart, recommendations
3. **Benchmarking** — Compare to industry average (from your 227-org research)

---

## Stop the App

Press `Ctrl + C` in the terminal

---

## Troubleshooting

**Dependencies not installing?**
```bash
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt
```

**Port already in use?**
```bash
streamlit run app.py --server.port 8502
```

**Browser doesn't open?**
Manually go to: http://localhost:8501

---

That's it! 🚀

