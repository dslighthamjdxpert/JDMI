# JDMI Assessment Tool

Interactive web application for assessing organizational job data maturity using the **Job Data Maturity Index (JDMI)** framework.

## 🚀 Run Locally (Easiest Method)

### Option 1: One-Click Start
```bash
cd Streamlit
./START_HERE.sh
```

That's it! The script will:
- Check your Python installation
- Install dependencies if needed
- Start the app
- Open your browser to http://localhost:8501

### Option 2: Manual Start
```bash
cd Streamlit
pip3 install -r requirements.txt
python3 -m streamlit run app.py
```

## 📋 What You'll Get

1. **7-Dimension Assessment** (5-7 minutes)
   - Coverage/Completeness
   - Governance/Ownership
   - Freshness/Velocity
   - Architecture Alignment
   - System Integration
   - Controls/Compliance
   - Ability to Act

2. **Results Dashboard**
   - JDMI Score (0-28) and Maturity Level (1-5)
   - Radar chart comparing your scores to industry benchmarks
   - Dimensional breakdown table
   - Top 5 personalized recommendations
   - Benchmarking vs. 227-org research data

## 🛠 Requirements

- **Python 3.8+** (you have 3.12.8 ✓)
- **Dependencies**: streamlit, plotly, pandas, numpy
  - Auto-installed by `START_HERE.sh`
  - Or manually: `pip3 install -r requirements.txt`

## 📊 Scoring Logic

Same algorithm as your research (`JDMI.py`):
- **7 dimensions** × **4 points each** = **28 max score**
- **5 maturity levels**:
  - Level 1 (0-5): Ad Hoc
  - Level 2 (6-10): Emerging
  - Level 3 (11-16): Defined
  - Level 4 (17-21): Governed
  - Level 5 (22-28): Optimized

## 🎨 Features

- ✅ Interactive form with intuitive UI
- ✅ Real-time scoring and visualization
- ✅ Radar chart comparing to industry avg (14.28)
- ✅ Personalized recommendations based on gaps
- ✅ Benchmarking against 227-org research
- ✅ Auto-generated insights (coverage paradox detection)
- ✅ Retake assessment functionality
- ✅ Optional org info collection for lead capture

## 🌐 Next Steps: Deploy to Web

Once you've tested locally, you can deploy to production:

### Streamlit Cloud (Free, Recommended)
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repo and deploy
4. Get public URL: `https://your-app.streamlit.app`

### Custom Domain
Point `assessment.jdxpert.com` to your Streamlit app via CNAME.

## 📁 File Structure

```
Streamlit/
├── app.py              # Main Streamlit application
├── utils.py            # Scoring logic and recommendations
├── requirements.txt    # Python dependencies
├── START_HERE.sh       # One-click start script
├── QUICKSTART.md       # Quick reference guide
└── README.md           # This file
```

## 🔧 Troubleshooting

**App won't start?**
```bash
python3 --version  # Check Python (need 3.8+)
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

**Port already in use?**
```bash
python3 -m streamlit run app.py --server.port 8502
```

**Dependencies failing?**
```bash
python3 -m pip install streamlit plotly pandas numpy
```

## 📞 Support

Questions? Issues?
- **Email**: info@jdxpert.com
- **GitHub**: Create an issue in your repo

---

**Framework Version**: JDMI v1.0  
**Research**: 227 organizations, State of Job & Skills Data Governance 2026  
**Last Updated**: November 2025
