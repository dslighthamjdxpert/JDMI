# Job IQ Assessment Tool - Streamlit Application

## Overview

Interactive web application for assessing organizational job data maturity using the **Job IQ — Job Intelligence Index (powered by Oz)** framework. This tool allows prospects and customers to:

- Answer 7 dimension-based questions (5-7 minutes)
- Receive instant Job IQ score (0-28) and maturity level (1-5)
- View dimensional breakdown with radar chart visualization
- Get personalized recommendations based on gaps
- Benchmark against industry averages from research

## Features

### ✅ Assessment Flow
- **7 Unified Dimensions**: Coverage, Governance, Velocity, Architecture, Integration, Controls, Ability to Act
- **User-Friendly Form**: Clear questions with intuitive sliders, radio buttons, and checkboxes
- **Optional Organization Info**: Industry, size, contact details for follow-up

### 📊 Results Dashboard
- **Score Summary**: Total score, maturity level, and level description
- **Radar Chart**: Visual comparison of your scores vs. industry average
- **Dimensional Breakdown Table**: Color-coded scores with gap analysis
- **Personalized Recommendations**: Top 5 action items based on your gaps and maturity level
- **Benchmarking**: Compare to industry average (14.3/28 from research)
- **Key Insights**: Auto-generated insights (e.g., coverage-governance gap detection)

### 🎨 Design
- **Modern UI**: Clean, professional design with gradient score cards
- **Responsive Layout**: Works on desktop and tablet
- **JDX Branding**: Customizable colors and logos
- **Exportable Results**: PDF download (coming soon)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Navigate to the Streamlit directory:**
```bash
cd /Users/dslightham/Library/CloudStorage/Dropbox/4_Utility/CODE/JDX/2_Tactics/Campaigns/JDX_SkillsGov_Campaign_2025Q4/JobIQ/Streamlit
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Running the Application

### Local Development

Run the Streamlit app locally:

```bash
streamlit run app.py
```

The app will automatically open in your default browser at `http://localhost:8501`.

### Command-Line Options

- **Specify port:**
```bash
streamlit run app.py --server.port 8502
```

- **Disable auto-open browser:**
```bash
streamlit run app.py --server.headless true
```

- **Enable debug mode:**
```bash
streamlit run app.py --logger.level debug
```

## Deployment

### Streamlit Cloud (Recommended)

1. **Push code to GitHub:**
   - Create a repository for the JDX campaign
   - Push the `/JobIQ/Streamlit` folder contents

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select `app.py` as the main file
   - Deploy (free tier available)

3. **Custom Domain (optional):**
   - Configure custom domain in Streamlit Cloud settings
   - Example: `assessment.jdxpert.com`

### Docker (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t jobiq-assessment .
docker run -p 8501:8501 jobiq-assessment
```

## Project Structure

```
JobIQ/Streamlit/
├── app.py                  # Main Streamlit application
├── utils.py                # Scoring logic and recommendations
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

### File Descriptions

- **`app.py`**: Main application with UI, form logic, and results visualization
- **`utils.py`**: 
  - `calculate_jdmi_score()`: Scoring algorithm across 7 dimensions
  - `get_level_info()`: Maps scores to maturity levels
  - `get_recommendations()`: Generates personalized recommendations
  - `get_dimension_descriptions()`: Reference descriptions for each dimension

## Configuration

### Branding

Update branding elements in `app.py`:

```python
# Sidebar logo (line ~140)
st.image("https://your-logo-url.com/logo.png", use_container_width=True)

# Footer (line ~480)
st.markdown("""
    <div class="footer">
        <p><strong>Your Company Name</strong></p>
    </div>
""", unsafe_allow_html=True)
```

### Styling

Customize colors and styling in the `<style>` block (lines ~20-70 in `app.py`):

```css
.score-box {
    background: linear-gradient(135deg, #YOUR_COLOR_1 0%, #YOUR_COLOR_2 100%);
}
```

### Benchmarks

Update industry average benchmarks in `utils.py`:

```python
# Line ~280 in create_radar_chart()
avg_values = [1.95, 2.08, 1.94, 1.93, 2.52, 2.08, 1.78]  # Update with your data
```

## Usage Notes

### For Marketing/Sales:

1. **Lead Capture**: Email field in optional org info section
2. **CTA Integration**: "Schedule Consultation" button links to booking page
3. **Follow-Up**: Use scores to personalize outreach (e.g., "You scored 12—here's how we help orgs at Level 3")
4. **Content Marketing**: Share example reports on LinkedIn, in emails

### For Product:

1. **Integration**: Can embed as iframe or link from main product
2. **User Flow**: "Upload 5 Jobs" → See JD Score → Take Job IQ → Schedule Consult
3. **Data Collection**: Capture responses for product analytics (add backend)

### For Research:

1. **Validation**: Compare self-assessment scores to actual survey responses
2. **Refinement**: A/B test dimension questions and scoring logic
3. **Benchmarking**: Aggregate scores over time to update industry averages

## Customization Guide

### Adding a New Dimension

1. **Add question in `app.py`** (in `render_assessment_form()`):
```python
st.markdown('<div class="dimension-header">8️⃣ New Dimension</div>', unsafe_allow_html=True)
responses['new_dim'] = st.radio("Question text", options=["Option 1", "Option 2"])
```

2. **Add scoring logic in `utils.py`** (in `calculate_jdmi_score()`):
```python
scores['dim8'] = scoring_logic_here
scores['total'] = sum([scores['dim1'], ..., scores['dim8']])
```

3. **Update visualization** (in `create_radar_chart()`):
```python
categories = ['Coverage', 'Governance', ..., 'New Dimension']
values = [scores['dim1'], ..., scores['dim8']]
```

### Changing Level Thresholds

Edit `get_level_info()` in `utils.py`:

```python
if total_score >= 22:  # Change threshold here
    return {'number': 5, 'name': 'Optimized', ...}
```

## Troubleshooting

### Common Issues

**App won't start:**
- Check Python version: `python --version` (need 3.8+)
- Reinstall dependencies: `pip install --force-reinstall -r requirements.txt`

**Charts not displaying:**
- Plotly version conflict: `pip install --upgrade plotly`
- Check browser console for JavaScript errors

**Session state errors:**
- Clear browser cache or use incognito mode
- Restart Streamlit: `Ctrl+C` then `streamlit run app.py`

**Styling not applying:**
- Verify CSS in `st.markdown(..., unsafe_allow_html=True)` blocks
- Check browser developer tools for CSS conflicts

## Roadmap / Enhancements

### Phase 1 (MVP) ✅
- [x] 7-dimension assessment form
- [x] JDMI scoring logic
- [x] Results dashboard with visualizations
- [x] Personalized recommendations
- [x] Benchmarking vs. industry average

### Phase 2 (Post-Launch)
- [ ] PDF report generation and download
- [ ] Email delivery of results
- [ ] Backend data collection (store responses)
- [ ] Admin dashboard (view all assessments)
- [ ] A/B testing framework for questions

### Phase 3 (Integration)
- [ ] Embed in JDX product (iframe)
- [ ] API endpoint for programmatic scoring
- [ ] Integration with CRM (auto-create leads)
- [ ] "Upload 5 Jobs" → JDMI flow
- [ ] Retake assessment comparison (show progress)

### Phase 4 (Advanced)
- [ ] Multi-language support
- [ ] Industry-specific benchmarks
- [ ] Predictive recommendations using ML
- [ ] Collaboration mode (team assessments)

## Support

For questions or issues:

- **Technical Issues**: [your-tech-email@jdxpert.com]
- **Product Feedback**: [your-product-email@jdxpert.com]
- **General Inquiries**: [info@jdxpert.com]

## License

© 2025 JDXpert. All rights reserved.

---

**Framework Version**: Job IQ v1.0  
**Research Basis**: 227 organizations, State of Job & Skills Data Governance 2026  
**Last Updated**: November 2025

