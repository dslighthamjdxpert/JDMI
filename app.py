"""
Job Data Maturity Index (JDMI) Assessment Tool
Interactive assessment for organizational job data maturity
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import matplotlib.colors as mcolors
from utils import calculate_jdmi_score, get_level_info, get_recommendations

# Page config
st.set_page_config(page_title="JDMI Assessment", page_icon="📊", layout="wide")

# CSS styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Font family */
* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* Main app background - target multiple Streamlit containers */
.main, .main > div, .block-container, [data-testid="stAppViewContainer"] {
    background-color: #F9F9F9 !important;
}

/* Ensure main content area has correct background */
section[data-testid="stAppViewContainer"] > div:first-child,
.main .block-container {
    background-color: #F9F9F9 !important;
}

/* Global text color */
.stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6, label, 
.stRadio label, .stCheckbox label, div[data-testid="stMarkdownContainer"] {
    color: #3C3C3C !important;
}

/* Headers */
h1, h2, h3 {
    color: #3C3C3C !important;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: #F9F9F9 !important;
    position: relative;
}

[data-testid="stSidebar"]::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.1);
    pointer-events: none;
}

[data-testid="stSidebar"] > div:first-child {
    background-color: transparent !important;
    position: relative;
    z-index: 1;
}

/* Sidebar text color */
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4 {
    color: #3C3C3C !important;
}

/* Sidebar collapse button */
[data-testid="stSidebarCollapseButton"],
button[kind="header"] {
    color: #F9F9F9 !important;
}

[data-testid="stSidebarCollapseButton"] svg,
button[kind="header"] svg {
    fill: #F9F9F9 !important;
    stroke: #F9F9F9 !important;
}

/* Expander styling - darker grey to pop off background */
.st-emotion-cache-13k62yr,
[data-testid="stExpander"],
details {
    background-color: #E5E5E5 !important;
    border: 1px solid #D0D0D0 !important;
    border-radius: 0.5rem !important;
}

.streamlit-expanderHeader {
    background-color: #E5E5E5 !important;
}

/* Expander caret/arrow color */
.streamlit-expanderHeader svg {
    stroke: #F9F9F9 !important;
    fill: #F9F9F9 !important;
}

details summary svg {
    stroke: #F9F9F9 !important;
    fill: #F9F9F9 !important;
}

/* Button styling - brand orange with light text */
.stButton > button,
button[kind="primary"],
button[kind="secondary"] {
    background-color: #FF8743 !important;
    color: #F9F9F9 !important;
    border: none !important;
    font-weight: 500 !important;
}

.stButton > button:hover,
button[kind="primary"]:hover,
button[kind="secondary"]:hover {
    background-color: #E67532 !important;
    color: #F9F9F9 !important;
}

/* Ensure metric values and other numbers are visible on light background */
[data-testid="stMetricValue"],
[data-testid="stMetricDelta"],
.stMetric {
    color: #3C3C3C !important;
}

[data-testid="stMetricValue"] > div {
    color: #3C3C3C !important;
}

.score-box {
    padding: 2rem; border-radius: 0.5rem;
    background: linear-gradient(135deg, #3AC1CC 0%, #4089CE 100%);
    color: white; text-align: center; margin: 1rem 0;
    font-family: 'Inter', sans-serif;
}
.score-number { 
    font-size: 3rem; 
    font-weight: 700;
    font-family: 'Inter', sans-serif;
    color: white !important;
}
.rec-box {
    padding: 1rem; border-left: 4px solid #3AC1CC;
    background-color: #ffffff; margin: 0.5rem 0; border-radius: 0.25rem;
    font-family: 'Inter', sans-serif;
    color: #3C3C3C;
}
</style>
""", unsafe_allow_html=True)

# Session state
if 'completed' not in st.session_state:
    st.session_state.completed = False
if 'responses' not in st.session_state:
    st.session_state.responses = {}

# Sidebar
with st.sidebar:
    st.markdown("### 📊 JDMI Assessment")
    st.markdown("---")
    
    st.markdown("#### About This Tool")
    st.markdown("""
    This assessment uses the **Job Data Maturity Index (JDMI)** framework developed from research with 227+ organizations.
    
    **Time:** 5-7 minutes  
    **Questions:** 7 dimensions  
    **Output:** Personalized report with recommendations
    """)
    
    st.markdown("---")
    st.markdown("#### Assessment Dimensions")
    st.markdown("""
    1. 📋 Coverage/Completeness
    2. ⚙️ Governance/Ownership
    3. ⚡ Freshness/Velocity
    4. 🏗️ Architecture Alignment
    5. 🔗 System Integration
    6. 🛡️ Controls/Compliance
    7. 📊 Ability to Act
    """)
    
    st.markdown("---")
    st.markdown("#### Need Help?")
    st.markdown("""
    - 📧 [Contact JDX](mailto:info@jdxpert.com)
    - 🌐 [Visit Website](https://jdxpert.com)
    - 📅 [Schedule Demo](https://jdxpert.com/demo)
    """)
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; font-size: 0.8rem; color: #666;">
    <p><strong>JDMI v1.0</strong></p>
    <p>Based on 227+ org research</p>
    <p>© 2025 JDX</p>
    </div>
    """, unsafe_allow_html=True)

# Header
st.title("📊 Job Data Maturity Index Assessment")
st.markdown("*Benchmark your organization's job and skills data governance maturity*")

with st.expander("ℹ️ About the JDMI"):
    st.markdown("""
    The **JDMI** measures maturity across 7 dimensions:
    1. **Coverage/Completeness** — Do you have the data?
    2. **Governance/Ownership** — Repeatable process and accountability?
    3. **Freshness/Velocity** — How quickly can you update?
    4. **Architecture Alignment** — Job levels, families, paths?
    5. **System Integration** — Synchronized or siloed?
    6. **Controls/Compliance** — Quality and compliance guardrails?
    7. **Ability to Act** — Can you extract insights and drive decisions?
    
    **Key Finding:** 91% of organizations with high skills coverage still plan governance overhauls 
    because data becomes static technical debt. Coverage ≠ maturity.
    """)

if not st.session_state.completed:
    # ASSESSMENT FORM
    st.markdown("---")
    st.markdown("### Assessment Questions (5-7 minutes)")
    
    responses = {}
    
    # Q1: Coverage
    st.markdown("#### 1️⃣ Coverage/Completeness of Skills Data")
    st.markdown("*What % of job descriptions include defined skills/competencies?*")
    responses['coverage'] = st.select_slider(
        "coverage_pct", ["<25%", "25-49%", "50-74%", "75-89%", "≥90%"],
        label_visibility="collapsed")
    
    # Q2: Governance
    st.markdown("#### 2️⃣ Governance Cadence/Process Ownership")
    st.markdown("*How do you manage job and skills data?*")
    responses['governance'] = st.radio(
        "governance_model",
        ["Ongoing governed program with clear ownership and regular reviews",
         "Primarily project-based with temporary ownership",
         "Decentralized — each function manages independently",
         "We do not actively manage job/skills data today"],
        label_visibility="collapsed")
    
    # Q3: Velocity
    st.markdown("#### 3️⃣ Freshness/Change Velocity")
    st.markdown("*Time to update and publish a job description:*")
    responses['velocity'] = st.select_slider(
        "velocity_time",
        ["More than 30 days", "15-30 days", "8-14 days", "3-7 days", "Less than 3 days"],
        label_visibility="collapsed")
    
    # Q4: Architecture
    st.markdown("#### 4️⃣ Architecture Alignment")
    st.markdown("*Which are linked to your job/skills data? (Select all)*")
    responses['arch_mobility'] = st.checkbox("Internal mobility and career paths", key="arch_mobility")
    responses['arch_comp'] = st.checkbox("Compensation and job leveling", key="arch_comp")
    responses['arch_planning'] = st.checkbox("Workforce planning", key="arch_planning")
    
    # Q5: Integration
    st.markdown("#### 5️⃣ System Fragmentation/Integration")
    st.markdown("*Are job data updates automatically propagated across systems?*")
    responses['integration'] = st.radio(
        "integration_sync",
        ["All core systems fully synchronized (HRIS, ATS, Comp, LMS)",
         "Most systems integrated (3 of 4)",
         "Some systems connected, but significant manual work",
         "Systems operate independently (manual exports/imports)"],
        label_visibility="collapsed")
    
    # Q6: Controls
    st.markdown("#### 6️⃣ Controls/Compliance")
    st.markdown("*Which governance controls are in place? (Select all)*")
    responses['control_ownership'] = st.checkbox("Clear ownership of job/skills content", key="control_ownership")
    responses['control_approvals'] = st.checkbox("Formal approval workflows", key="control_approvals")
    responses['control_lineage'] = st.checkbox("Version history and audit trails", key="control_lineage")
    responses['control_bias'] = st.checkbox("Bias review and compliance checks", key="control_bias")
    
    # Q7: Ability to Act
    st.markdown("#### 7️⃣ Ability to Act (Analytics/Insights)")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("*Skills data drives decisions for:*")
        responses['act_reskilling'] = st.checkbox("Reskilling/upskilling programs", key="act_reskilling")
        responses['act_mobility'] = st.checkbox("Internal mobility decisions", key="act_mobility")
        responses['act_comp'] = st.checkbox("Compensation decisions", key="act_comp")
        responses['act_hiring'] = st.checkbox("Hiring requirements", key="act_hiring")
        responses['act_planning'] = st.checkbox("Workforce planning", key="act_planning")
    with col2:
        st.markdown("*We track these metrics:*")
        responses['metric_cycle'] = st.checkbox("Cycle times (JD → Req → Hire)", key="metric_cycle")
        responses['metric_exception'] = st.checkbox("Exception rates / MTTR", key="metric_exception")
        responses['metric_ttp'] = st.checkbox("Time-to-publish", key="metric_ttp")
        responses['metric_mobility'] = st.checkbox("Internal mobility rate", key="metric_mobility")
    
    # Optional org info
    with st.expander("📋 Optional: Organization Information"):
        col1, col2 = st.columns(2)
        with col1:
            responses['org_name'] = st.text_input("Organization Name")
            responses['industry'] = st.selectbox("Industry", 
                ["", "Technology", "Healthcare", "Financial Services", "Manufacturing", 
                 "Retail", "Education", "Professional Services", "Other"])
        with col2:
            responses['org_size'] = st.selectbox("Organization Size",
                ["", "< 500", "500-2,000", "2,000-5,000", "5,000-10,000", "> 10,000"])
            responses['email'] = st.text_input("Email (for results)")
    
    st.markdown("---")
    
    # Submit button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("📊 Calculate My JDMI Score", type="primary", use_container_width=True):
            scores = calculate_jdmi_score(responses)
            level_info = get_level_info(scores['total'])
            st.session_state.responses = responses
            st.session_state.scores = scores
            st.session_state.level_info = level_info
            st.session_state.completed = True
            st.rerun()

else:
    # RESULTS PAGE
    scores = st.session_state.scores
    level_info = st.session_state.level_info
    
    # Scroll to top when results page loads
    st.markdown("""
    <script>
        window.parent.document.querySelector('section.main').scrollTo(0, 0);
    </script>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("## 📊 Your JDMI Results")
    
    # Score card
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div class="score-box">
            <div style="font-size: 1rem; margin-bottom: 0.5rem;">Your JDMI Score</div>
            <div class="score-number">{scores['total']}<span style="font-size: 1.5rem; opacity: 0.8;"> / 28</span></div>
            <div style="font-size: 1.5rem; margin-top: 1rem;">Level {level_info['number']}: {level_info['name']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(level_info['description'])
    
    # Dimensional Scores Table
    st.markdown("---")
    st.markdown("### Dimensional Breakdown")
    
    # Scores table with custom color gradient
    values = [scores['dim1'], scores['dim2'], scores['dim3'], scores['dim4'],
             scores['dim5'], scores['dim6'], scores['dim7']]
    dim_names = ['Coverage', 'Governance', 'Velocity', 'Architecture', 
                'Integration', 'Controls', 'Ability to Act']
    df = pd.DataFrame({
        'Dimension': dim_names,
        'Score': values,
        'Max': [4] * 7,
        'Gap': [4 - s for s in values]
    })
    
    # Create custom colormap using brand colors: Red-Orange -> Orange -> Blue -> Teal -> Green-Teal
    colors = ['#D74A28', '#FF8743', '#4089CE', '#3AC1CC', '#72CAB5']
    n_bins = 100
    cmap = mcolors.LinearSegmentedColormap.from_list('jdx_colors', colors, N=n_bins)
    
    st.dataframe(df.style.background_gradient(subset=['Score'], cmap=cmap, vmin=0, vmax=4),
                use_container_width=True, hide_index=True)
    
    # Recommendations
    st.markdown("---")
    st.markdown("### 🎯 Personalized Recommendations")
    
    recs = get_recommendations(scores, level_info['number'])
    for i, rec in enumerate(recs, 1):
        st.markdown(f"""
        <div class="rec-box">
            <strong>{i}. {rec['title']}</strong><br/>
            {rec['description']}
        </div>
        """, unsafe_allow_html=True)
    
    # Benchmarking
    st.markdown("---")
    st.markdown("### 📈 Benchmarking")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Your Level", f"Level {level_info['number']}")
    with col2:
        st.metric("Industry Average", "14.3 / 28", f"{scores['total'] - 14.28:+.1f}")
    with col3:
        percentile = "Top 5%" if scores['total'] >= 22 else "Top 10%" if scores['total'] >= 20 else "Top 50%" if scores['total'] >= 14 else "Bottom 50%"
        st.metric("Estimated Percentile", percentile)
    
    # Key insights
    st.markdown("---")
    st.markdown("### 💡 Key Insights")
    if scores['dim1'] >= 3 and scores['total'] < 20:
        st.markdown("⚠️ **Coverage vs. Governance Gap**: High skills coverage but lack governance to operationalize it—91% of orgs here plan major overhauls.")
    if scores['dim3'] <= 1:
        st.markdown("🐌 **Velocity Bottleneck**: Taking 15+ days to update jobs creates friction. Streamline approval process.")
    if scores['dim7'] <= 1:
        st.markdown("📊 **Data Trapped**: Job/skills data isn't driving decisions. Without analytics, you can't demonstrate ROI.")
    
    # Action buttons
    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🔄 Retake Assessment", use_container_width=True):
            st.session_state.completed = False
            st.session_state.responses = {}
            st.rerun()
    with col2:
        st.markdown("[📅 Schedule Consultation →](https://jdxpert.com/demo)")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #9ca3af; padding: 2rem 0;">
<p><strong>Job Data Maturity Index (JDMI)</strong> by JDX</p>
<p>Based on research with 227+ organizations | Framework v1.0</p>
</div>
""", unsafe_allow_html=True)
