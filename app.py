"""
Job IQ — Job Intelligence Index (powered by Oz)
Interactive Streamlit application for assessing organizational job data maturity
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import streamlit.components.v1 as components
import base64
import json
from fpdf import FPDF
from streamlit import cache_data
from streamlit_lottie import st_lottie
from utils import (
    calculate_jdmi_score,
    get_level_info,
    get_recommendations,
    get_dimension_descriptions,
)
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Job IQ — Job Intelligence Index",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
<style>
    :root {
        --c-verylight: #E8FDFF;
        --c-light: #BFFAFF;
        --c-mid: #76E9F3;
        --c-teal: #3AC1CC;
        --c-deeper: #308B9A;
        --c-dark: #0D5865;
        --c-text-dark: #3C3C3C;
        --c-text-light:#f9f9f9;
        --c-background: #f9f9f9;
        --c-button: #FF8743;
        /* Streamlit accent override (affects some widgets' default red) */
        --primary-color: #FF8743;
        --c-panel-light: #FFBCAC; /* light gray panels */
    }
    .stApp {
        background: var(--c-background) !important;
        color: var(--c-text-dark) !important;
    }
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--c-text-dark);
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: var(--c-text-dark);
        margin-bottom: 2rem;
    }
    .dimension-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: var(--c-text-dark);
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .score-box {
        padding: 2rem;
        border-radius: 0.5rem;
        background: var(--c-dark);
        color: var(--c-text-light);
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 24px rgba(0,0,0,0.25);
    }
    .score-number {
        font-size: 4rem;
        font-weight: 700;
        color: var(--c-text-light);
    }
    .level-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 2rem;
        font-weight: 600;
        margin: 0.5rem 0;
        background-color: var(--c-deeper);
        color: var(--c-text-dark);
    }
    .recommendation-box {
        padding: 1rem;
        border-left: 4px solid var(--c-mid);
        background-color: rgba(56, 139, 154, 0.35);
        margin: 0.5rem 0;
        border-radius: 0.25rem;
        color: var(--c-text-dark);
    }
    .footer {
        text-align: center;
        color: var(--c-text-dark);
        font-size: 0.875rem;
        margin-top: 3rem;
        padding: 2rem 0;
        border-top: 1px solid rgba(255,255,255,0.15);
    }
    a, a:visited {
        color: var(--c-light);
    }
    /* Buttons (primary and default) */
    .stButton > button,
    button[kind="primary"] {
        background-color: var(--c-button) !important;
        border: 1px solid var(--c-button) !important;
        color: var(--c-text-dark) !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    .stButton > button:hover,
    button[kind="primary"]:hover {
        filter: brightness(1.05);
    }
    /* Sidebar background and text */
    [data-testid="stSidebar"], section[data-testid="stSidebar"] {
        background-color: var(--c-dark) !important;
        color: var(--c-text-light) !important;
    }
    [data-testid="stSidebar"] * {
        color: var(--c-text-light) !important;
    }
    /* Top header bar */
    header[data-testid="stHeader"] {
        background: var(--c-dark) !important;
        color: var(--c-text-dark) !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    header[data-testid="stHeader"] * {
        color: var(--c-text-dark) !important;
    }
    /* Plotly charts: remove dark paper/background inside, style container as boxed panel */
    [data-testid="stPlotlyChart"] > div,
    .stPlotlyChart > div {
        background-color: transparent !important;
    }
    [data-testid="stPlotlyChart"] {
        background-color: var(--c-dark) !important;
        border-radius: 10px !important;
        padding: 1rem 1.25rem !important;
        color: var(--c-text-light) !important;
        overflow: hidden !important;
    }
    /* Light gray background for st-ca containers */
    .st-ca,
    .stApp .st-ca {
        background-color: var(--c-panel-light) !important;
    }
    /* ---- Form controls accent color overrides ---- */
    /* Radios and checkboxes */
    input[type="radio"],
    input[type="checkbox"] {
        accent-color: var(--c-button) !important;
    }
    /* Ensure question text/labels use dark text in main content */
    section.main label,
    section.main .stMarkdown,
    section.main .stMarkdown p,
    section.main [data-baseweb="radio"] label,
    section.main [data-baseweb="checkbox"] label,
    section.main [data-baseweb="slider"] [class*="Label"],
    section.main [data-baseweb="slider"] [class*="tick"],
    section.main [data-baseweb="slider"] [class*="mark"] {
        color: var(--c-text-dark) !important;
    }
    /* Specific emotion class override for text color */
    .stApp .st-emotion-cache-1j90q2q {
        color: var(--c-text-dark) !important;
    }
    /* Benchmarking metrics text color */
    .stMetric label, .stMetric div[data-testid="stMetricValue"], .stMetric div[data-testid="stMetricDelta"] {
        color: var(--c-text-dark) !important;
    }
    /* Alternative metric selectors */
    div[data-testid="stMetric"] label, div[data-testid="stMetric"] span, div[data-testid="stMetric"] div {
        color: var(--c-text-dark) !important;
    }
    /* Specific style override for selection container */
    .stApp .st-emotion-cache-11ofl8m {
        position: relative !important;
        display: flex !important;
        width: 100% !important;
        min-width: 0px !important;
        overflow: hidden !important;
        font-size: inherit !important;
        padding: 0.25rem 0.75rem !important;
        min-height: calc(-2px + 2.5rem) !important;
        -webkit-box-align: center !important;
        /* align-items: center; */
        cursor: pointer !important;
        list-style-type: none !important;
        background-color: rgba(0, 0, 0, 0.2) !important;
        border-radius: 0.5rem 0.5rem 0px 0px !important;
        transition: border-radius 200ms cubic-bezier(0.23, 1, 0.32, 1), background-color 150ms !important;
    }
    /* Sliders (Streamlit/BaseWeb) */
    div[data-baseweb="slider"] [role="slider"] {
        background-color: var(--c-button) !important;   /* thumb */
        border-color: var(--c-button) !important;
    }
    div[data-baseweb="slider"] > div > div {
        background-color: rgba(255, 135, 67, 0.30) !important; /* active track */
    }
    /* Select slider pills */
    .stSelectSlider [data-baseweb="tag"] {
        background-color: var(--c-button) !important;
        color: var(--c-text-dark) !important;
        border-color: var(--c-button) !important;
    }
    /* BaseWeb Radio refinements (circle + checked state) */
    div[data-baseweb="radio"] label > div:first-child {
        border-color: var(--c-button) !important;
    }
    div[data-baseweb="radio"] label[aria-checked="true"] > div:first-child {
        background-color: var(--c-button) !important;
        border-color: var(--c-button) !important;
    }
    div[data-baseweb="radio"] svg {
        color: var(--c-button) !important;
        fill: var(--c-button) !important;
    }
    /* Slider mark/label color */
    div[data-baseweb="slider"] [class*="tick"],
    div[data-baseweb="slider"] [class*="mark"],
    div[data-baseweb="slider"] [class*="Label"] {
        color: var(--c-button) !important;
    }
    /* Catch-all override for Streamlit danger/red bg (e.g., .st-b9) */
    .stApp .st-b9 {
        background-color: var(--c-button) !important;
        color: var(--c-text-dark) !important;
        border-color: var(--c-button) !important;
    }
    /* Specific emotion class overrides from examples */
    .stApp .st-emotion-cache-jigjfz {
        color: var(--c-button) !important;
    }
    .stApp .st-ey {
        background: linear-gradient(to right, var(--c-button) 0%, var(--c-button) 25%, rgba(172, 177, 195, 0.25) 25%, rgba(172, 177, 195, 0.25) 100%) !important;
    }
    /* Fallback: any element with inline red bg (covers background and background-image) */
    .stApp [style*="rgb(255, 75, 75)"],
    .stApp [style*="rgb(255,75,75)"],
    .stApp [style*="rgba(255, 75, 75"],
    .stApp [style*="#ff4b4b"] {
        background: var(--c-button) !important;
        background-color: var(--c-button) !important;
        background-image: none !important;
        color: var(--c-text-dark) !important;
        border-color: var(--c-button) !important;
    }
    /* Fallback: any inline red text color */
    .stApp [style*="color: rgb(255, 75, 75)"],
    .stApp [style*="color:rgb(255,75,75)"] {
        color: var(--c-button) !important;
    }
    /* Fallback: any inline red linear gradient track (generic matcher) */
    .stApp [style*="linear-gradient"][style*="255, 75, 75"],
    .stApp [style*="linear-gradient"][style*="255,75,75"] {
        background-image: linear-gradient(to right, var(--c-button) 0%, var(--c-button) 50%, rgba(172, 177, 195, 0.25) 50%, rgba(172, 177, 195, 0.25) 100%) !important;
    }
</style>
""",
    unsafe_allow_html=True,
)


def init_session_state():
    """Initialize session state variables"""
    if "assessment_complete" not in st.session_state:
        st.session_state.assessment_complete = False
    if "results_ready" not in st.session_state:
        st.session_state.results_ready = False
    if "responses" not in st.session_state:
        st.session_state.responses = {}
    if "scores" not in st.session_state:
        st.session_state.scores = None
    if "level_info" not in st.session_state:
        st.session_state.level_info = None


def scroll_to_top():
    """Force the viewport to scroll to the top after layout is rendered."""
    components.html(
        """
        <script>
        (function() {
          const goTop = () => {
            try {
              // Disable automatic scroll restoration
              if ('scrollRestoration' in window.history) {
                window.history.scrollRestoration = 'manual';
              }

              const doc = window.parent && window.parent.document ? window.parent.document : document;

              // Try Streamlit main container first
              let main = doc.querySelector('section.main')
                        || doc.querySelector('main')
                        || doc.body;

              if (main && main.scrollTo) {
                main.scrollTo({ top: 0, left: 0, behavior: 'auto' });
              }

              // Also scroll window as a fallback
              window.scrollTo(0, 0);
              if (window.parent && window.parent.scrollTo) {
                window.parent.scrollTo(0, 0);
              }
            } catch (e) {
              window.scrollTo(0, 0);
            }
          };

          // Run immediately and once more after layout has likely settled
          goTop();
          setTimeout(goTop, 150);
        })();
        </script>
        """,
        height=0,
    )


def render_intro():
    """Render introduction section"""
    st.markdown(
        '<div class="main-header">Job IQ Assessment, powered by Oz</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="sub-header">Job Intelligence Index — Calculated from job data quality, governance, usage, and architecture</div>',
        unsafe_allow_html=True,
    )

    with st.expander("About Job IQ", expanded=False):
        st.markdown(
            """
        The **Job Intelligence Index (Job IQ)** measures your organization's maturity across seven critical dimensions:
        
        1. **Coverage/Completeness** — Do you have the data inventoried?
        2. **Governance/Ownership** — Is there a repeatable process and accountability?
        3. **Freshness/Velocity** — How quickly can you respond to business needs?
        4. **Architecture Alignment** — Is there scaffolding (levels, families, paths)?
        5. **System Integration** — Is data synchronized or siloed?
        6. **Controls/Compliance** — Are there guardrails for quality and compliance?
        7. **Ability to Act** — Can stakeholders extract insights and drive decisions?
        
        **Key Insight:** Our research shows that **coverage ≠ maturity**. 91% of organizations with high skills 
        coverage still plan major governance overhauls because data becomes static and ungoverned.
        
        This assessment takes 5-7 minutes and provides personalized recommendations.
        """
        )


def render_assessment_form():
    """Render the assessment form with all 7 dimensions"""

    st.markdown("---")
    st.markdown("### Answer the following questions about your organization")

    responses = {}

    # Dimension 1: Coverage/Completeness
    st.markdown(
        '<div class="dimension-header">1. Coverage/Completeness of Skills Data</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        "*What percentage of your job descriptions include defined skills or competencies?*"
    )
    responses["coverage"] = st.select_slider(
        "Coverage Percentage",
        options=["<25%", "25-49%", "50-74%", "75-89%", "≥90%"],
        key="coverage",
        label_visibility="collapsed",
    )

    # Dimension 2: Governance/Ownership
    st.markdown(
        '<div class="dimension-header">2. Governance Cadence/Process Ownership</div>',
        unsafe_allow_html=True,
    )
    st.markdown("*How do you currently manage job and skills data?*")
    responses["governance"] = st.radio(
        "Operating Model",
        options=[
            "Ongoing governed program with clear ownership and regular reviews",
            "Primarily project-based with temporary ownership",
            "Decentralized — each function manages independently",
            "We do not actively manage job/skills data today",
        ],
        key="governance",
        label_visibility="collapsed",
    )

    # Dimension 3: Freshness/Velocity
    st.markdown(
        '<div class="dimension-header">3. Freshness/Change Velocity</div>',
        unsafe_allow_html=True,
    )
    st.markdown("*When you need to update a job description, how quickly can it go live?*")
    responses["velocity"] = st.select_slider(
        "Time to Publish",
        options=[
            "More than 30 days",
            "15-30 days",
            "8-14 days",
            "3-7 days",
            "Less than 3 days",
        ],
        key="velocity",
        label_visibility="collapsed",
    )

    # Dimension 4: Architecture Alignment
    st.markdown(
        '<div class="dimension-header">4. Architecture Alignment</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        "*Which of the following are linked to your job/skills data? (Select all that apply)*"
    )
    responses["arch_mobility"] = st.checkbox(
        "Internal mobility and career paths", key="arch_mobility"
    )
    responses["arch_comp"] = st.checkbox(
        "Compensation and job leveling", key="arch_comp"
    )
    responses["arch_planning"] = st.checkbox("Workforce planning", key="arch_planning")

    # Dimension 5: System Integration
    st.markdown(
        '<div class="dimension-header">5. System Fragmentation/Integration</div>',
        unsafe_allow_html=True,
    )
    st.markdown("*Are job data updates automatically propagated across your HR systems?*")
    responses["integration"] = st.radio(
        "System Synchronization",
        options=[
            "All core systems fully synchronized (HRIS, ATS, Comp, LMS)",
            "Most systems integrated (3 of 4)",
            "Some systems connected, but significant manual work",
            "Systems operate independently (manual exports/imports)",
        ],
        key="integration",
        label_visibility="collapsed",
    )

    # Dimension 6: Controls/Compliance
    st.markdown(
        '<div class="dimension-header">6. Controls/Compliance (including Bias)</div>',
        unsafe_allow_html=True,
    )
    st.markdown("*Which governance controls are in place? (Select all that apply)*")
    responses["control_ownership"] = st.checkbox(
        "Clear ownership of job/skills content", key="control_ownership"
    )
    responses["control_approvals"] = st.checkbox(
        "Formal approval workflows", key="control_approvals"
    )
    responses["control_lineage"] = st.checkbox(
        "Version history and audit trails", key="control_lineage"
    )
    responses["control_bias"] = st.checkbox(
        "Bias review and compliance checks", key="control_bias"
    )

    # Dimension 7: Ability to Act
    st.markdown(
        '<div class="dimension-header">7. Ability to Act (Analytics/Insights)</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("*Skills data drives decisions for:* (Select all)")
        responses["act_reskilling"] = st.checkbox(
            "Reskilling/upskilling programs", key="act_reskilling"
        )
        responses["act_mobility"] = st.checkbox(
            "Internal mobility decisions", key="act_mobility"
        )
        responses["act_comp"] = st.checkbox(
            "Compensation decisions", key="act_comp"
        )
        responses["act_hiring"] = st.checkbox(
            "Hiring/requisition requirements", key="act_hiring"
        )
        responses["act_planning"] = st.checkbox(
            "Workforce planning", key="act_planning"
        )

    with col2:
        st.markdown("*We track these metrics:* (Select all)")
        responses["metric_cycle"] = st.checkbox(
            "Cycle times (JD → Req → Hire)", key="metric_cycle"
        )
        responses["metric_exception"] = st.checkbox(
            "Exception rates / MTTR", key="metric_exception"
        )
        responses["metric_ttp"] = st.checkbox(
            "Time-to-publish", key="metric_ttp"
        )
        responses["metric_mobility"] = st.checkbox(
            "Internal mobility rate", key="metric_mobility"
        )

    st.markdown("---")

    # Organization info (optional) — disabled per request
    # with st.expander("Optional: Organization Information", expanded=False):
    #     col1, col2 = st.columns(2)
    #     with col1:
    #         responses["org_name"] = st.text_input(
    #             "Organization Name (optional)", key="org_name"
    #         )
    #         responses["industry"] = st.selectbox(
    #             "Industry",
    #             [
    #                 "",
    #                 "Technology",
    #                 "Healthcare",
    #                 "Financial Services",
    #                 "Manufacturing",
    #                 "Retail",
    #                 "Education",
    #                 "Professional Services",
    #                 "Other",
    #             ],
    #             key="industry",
    #         )
    #     with col2:
    #         responses["org_size"] = st.selectbox(
    #             "Organization Size",
    #             ["", "< 500", "500-2,000", "2,000-5,000", "5,000-10,000", "> 10,000"],
    #             key="org_size",
    #         )
    #         responses["email"] = st.text_input(
    #             "Email (optional, for results)", key="email"
    #         )

    return responses


def render_results(responses, scores, level_info):
    """Render the results section"""

    st.markdown("---")
    st.markdown('<h2 id="results-header">Your Job IQ Results</h2>', unsafe_allow_html=True)

    # Score and Level
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # Load wizard image
        _assets_dir = Path(__file__).parent
        _wizard_img = _assets_dir / "oz-grabbing-hat@3x.png"
        img_html = ""
        if _wizard_img.exists():
            # Convert to base64 for embedding in HTML
            with open(_wizard_img, "rb") as f:
                img_data = base64.b64encode(f.read()).decode()
            img_html = f'<img src="data:image/png;base64,{img_data}" style="width: 180px; height: auto;" alt="Wizard">'

        st.markdown(
            f"""
        <div class="score-box">
            <div style="text-align: center; margin-bottom: 1rem;">
                {img_html}
            </div>
            <div style="font-size: 1rem; margin-bottom: 0.5rem; text-align: center;">Your Job IQ</div>
            <div class="score-number" style="text-align: center;">{scores['total']}<span style="font-size: 1.5rem; opacity: 0.8;"> / 28</span></div>
            <div style="font-size: 1.5rem; margin-top: 1rem; text-align: center;">Level {level_info['number']}: {level_info['name']}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Level description
    st.markdown(f"### {level_info['name']} Maturity")
    st.markdown(level_info["description"])

    # Dimension breakdown
    st.markdown("---")
    st.markdown("### Dimensional Breakdown")

    # Radar chart inside styled panel
    fig = create_radar_chart(scores)
    st.plotly_chart(fig, use_container_width=True)

    # Recommendations
    st.markdown("---")
    st.markdown("### Personalized Recommendations")

    recommendations = get_recommendations(scores, level_info["number"])

    for i, rec in enumerate(recommendations, 1):
        st.markdown(
            f"""
        <div class="recommendation-box">
            <strong>{i}. {rec['title']}</strong><br/>
            {rec['description']}
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Benchmarking
    st.markdown("---")
    st.markdown("### Benchmarking")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Your Level", f"Level {level_info['number']}")

    with col2:
        # Based on research data
        avg_score = 14.28
        st.metric("Industry Average", "14.3 / 28", f"{scores['total'] - avg_score:+.1f}")

    with col3:
        # Percentile estimate
        if scores["total"] >= 20:
            percentile = "Top 10%"
        elif scores["total"] >= 14:
            percentile = "Top 50%"
        else:
            percentile = "Bottom 50%"
        st.metric("Estimated Percentile", percentile)

    # Key insights
    st.markdown("---")
    st.markdown("### Key Insights")

    insights = []

    # High coverage paradox check
    if scores["dim1"] >= 3 and scores["total"] < 20:
        insights.append(
            "Warning — Coverage vs. Governance Gap Detected: You have high skills coverage but lack the governance to operationalize it. This is the #1 pain point we see—91% of orgs with high coverage still plan major overhauls."
        )

    # Lowest dimension
    dim_names_short = [
        "Coverage",
        "Governance",
        "Velocity",
        "Architecture",
        "Integration",
        "Controls",
        "Ability to Act",
    ]
    dim_scores = [
        scores['dim1'], scores['dim2'], scores['dim3'], scores['dim4'],
        scores['dim5'], scores['dim6'], scores['dim7']
    ]
    lowest_dim_idx = dim_scores.index(min(dim_scores))
    if dim_scores[lowest_dim_idx] <= 1:
        insights.append(
            f"Priority Gap: {dim_names_short[lowest_dim_idx]} is your lowest-scoring dimension. Addressing this will have the highest impact on your overall maturity."
        )

    # Velocity gap
    if scores["dim3"] <= 1:
        insights.append(
            "Velocity Bottleneck: Taking 15+ days to update jobs creates friction in hiring and comp decisions. Streamlining your approval process should be a priority."
        )

    # Ability to act gap
    if scores["dim7"] <= 1:
        insights.append(
            "Data Trapped: Your job/skills data isn't driving decisions or being measured. Without analytics and process linkage, you can't demonstrate ROI."
        )

    if insights:
        for insight in insights:
            st.markdown(insight)
    else:
        st.markdown(
            "✅ **Strong Foundation**: Your scores are well-balanced across dimensions. Focus on incremental improvements to reach the next maturity level."
        )

    # Action buttons at the bottom of results
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("Retake Assessment", use_container_width=True):
            st.session_state.assessment_complete = False
            st.session_state.results_ready = False
            st.session_state.responses = {}
            st.session_state.scores = None
            st.session_state.level_info = None
            st.rerun()

    with col2:
        if st.button("Download Report (PDF)", use_container_width=True):
            try:
                pdf_bytes = create_pdf_report(st.session_state.scores, st.session_state.level_info)

                st.download_button(
                    label="📄 Download Your Job IQ Report",
                    data=pdf_bytes,
                    file_name=f"Job_IQ_Report_{st.session_state.scores['total']}_points.pdf",
                    mime="application/pdf"
                )
                st.success("PDF report generated successfully!")
            except Exception as e:
                st.error(f"Error generating PDF: {str(e)}")

    with col3:
        if st.button("Schedule Consultation", type="primary", use_container_width=True):
            st.markdown("[Book a meeting →](https://jdxpert.com/book-a-demo/?utm_campaign=skills-gov-2025&utm_source=job-iq-app&utm_medium=referral&utm_content=book-demo)")


def create_pdf_report(scores, level_info):
    """Generate a PDF report with Job IQ assessment results"""
    pdf = FPDF()
    pdf.add_page()

    # Set up fonts and colors
    pdf.set_font("Arial", "B", 20)
    pdf.set_text_color(13, 88, 101)  # JDX teal color

    # Title
    pdf.cell(0, 20, "Job IQ Assessment Report", ln=True, align="C")
    pdf.ln(10)

    # Score section
    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(60, 60, 60)  # Dark gray
    pdf.cell(0, 12, "Your Results:", ln=True)
    pdf.ln(5)

    # Main score
    pdf.set_font("Arial", "B", 24)
    pdf.set_text_color(255, 135, 67)  # JDX orange
    pdf.cell(0, 15, f"Job IQ Score: {scores['total']}/28", ln=True, align="C")
    pdf.ln(5)

    # Level info
    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 12, f"Level {level_info['number']}: {level_info['name']}", ln=True, align="C")
    pdf.ln(10)

    # Benchmarking
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 12, "Industry Benchmarking:", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", "", 12)
    avg_score = 14.28
    percentile = "Top 10%" if scores["total"] >= 20 else ("Top 50%" if scores["total"] >= 14 else "Bottom 50%")

    pdf.cell(0, 8, f"Your Score: {scores['total']}/28", ln=True)
    pdf.cell(0, 8, f"Industry Average: 14.3/28", ln=True)
    pdf.cell(0, 8, f"Estimated Percentile: {percentile}", ln=True)
    pdf.ln(10)

    # Dimension breakdown
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 12, "Dimension Scores:", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", "", 12)
    dimensions = [
        "Coverage", "Governance", "Velocity", "Architecture",
        "Integration", "Controls", "Ability to Act"
    ]

    for i, dimension in enumerate(dimensions, 1):
        pdf.cell(0, 8, f"{dimension}: {scores[f'dim{i}']}/4", ln=True)

    pdf.ln(10)

    # Footer
    pdf.set_font("Arial", "I", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, "Generated by JDX Job IQ Assessment", ln=True, align="C")
    pdf.cell(0, 8, "Learn more at jdxpert.com", ln=True, align="C")

    return pdf.output(dest="S").encode("latin1")


def create_radar_chart(scores):
    """Create a radar chart for dimension scores"""

    categories = [
        "Coverage",
        "Governance",
        "Velocity",
        "Architecture",
        "Integration",
        "Controls",
        "Ability to Act",
    ]

    values = [
        scores["dim1"],
        scores["dim2"],
        scores["dim3"],
        scores["dim4"],
        scores["dim5"],
        scores["dim6"],
        scores["dim7"],
    ]

    # Close the radar chart
    values_closed = values + [values[0]]
    categories_closed = categories + [categories[0]]

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=values_closed,
            theta=categories_closed,
            fill="toself",
            name="Your Score",
            line=dict(color="#76E9F3", width=2),
            fillcolor="rgba(118, 233, 243, 0.30)",
        )
    )

    # Add benchmark line (average from research)
    avg_values = [1.95, 2.08, 1.94, 1.93, 2.52, 2.08, 1.78]
    avg_values_closed = avg_values + [avg_values[0]]

    fig.add_trace(
        go.Scatterpolar(
            r=avg_values_closed,
            theta=categories_closed,
            fill="toself",
            name="Industry Avg",
            line=dict(color="#3C3C3C", width=2, dash="dash"),
            fillcolor="rgba(60, 60, 60, 0.15)",
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 4],
                tickvals=[0, 1, 2, 3, 4],
                showticklabels=True,
                tickfont=dict(color="#3C3C3C", size=12),
                gridcolor="#E0E0E0",
            ),
            angularaxis=dict(
                tickfont=dict(color="var(--c-text-light)", size=11),
            )
        ),
        showlegend=True,
        legend=dict(
            x=0.5,
            y=-0.15,
            xanchor="center",
            yanchor="top",
            orientation="h",
            font=dict(color="var(--c-text-light)", size=12),
        ),
        title="Job IQ Dimension Scores",
        title_font=dict(color="var(--c-text-light)", size=16),
        height=450,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=40, t=60, b=120),  # Add bottom margin for legend
    )

    return fig


def load_lottie_file(filepath: str):
    """Load a Lottie animation from a JSON file"""
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None


def render_results_ready_message():
    """Show results ready message with link to full results"""

    # Load and display the wizard Lottie animation
    # Place your Lottie JSON file (wizard Oz on broomstick) in the same directory as this app.py file
    # and name it "wizard_broomstick.json" or update the filename below
    _assets_dir = Path(__file__).parent
    lottie_file = _assets_dir / "wizard_broomstick.json"

    lottie_data = load_lottie_file(str(lottie_file))

    if lottie_data:
        # Center the animation with background using CSS variable
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.markdown(
                """
                <div style="background-color: var(--c-background); padding: 20px; border-radius: 10px; display: flex; justify-content: center;">
                """,
                unsafe_allow_html=True
            )
            st_lottie(lottie_data, height=200, key="wizard_animation")
            st.markdown(
                """
                </div>
                <style>
                /* Target the Lottie iframe specifically */
                iframe.stCustomComponentV1.st-emotion-cache-1tvzk6f {
                    background-color: var(--c-background) !important;
                    border: none !important;
                    border-radius: 10px !important;
                }
                /* Alternative selectors */
                iframe[data-testid="stCustomComponentV1"] {
                    background-color: var(--c-background) !important;
                }
                /* If the iframe has transparent background, this should show through */
                div[data-testid="stCustomComponentV1"] {
                    background-color: var(--c-background) !important;
                }
                </style>
                """,
                unsafe_allow_html=True
            )
    else:
        # Fallback to balloons if Lottie file not found
        st.balloons()

    st.markdown("## 🎉 Your Job IQ Assessment is Complete!")

    st.success("Your personalized results are ready to view!")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📊 View My Job IQ Results",
                    type="primary",
                    use_container_width=True):
            st.session_state.assessment_complete = True
            st.rerun()

    # Optional: Show a teaser/preview
    st.markdown("---")
    st.markdown("### What you'll discover:")
    st.markdown("- Your Job IQ Score (0-28)")
    st.markdown("- Your maturity level and characteristics")
    st.markdown("- Personalized recommendations")
    st.markdown("- Industry benchmarking")


def main():
    """Main application logic"""

    init_session_state()

    # Sidebar
    with st.sidebar:
        # JDX Logo at top of sidebar
        _assets_dir = Path(__file__).parent
        _jdx_logo = _assets_dir / "JDX White.png"
        if _jdx_logo.exists():
            st.image(str(_jdx_logo), use_container_width=True)
        else:
            # Fallback text if logo not found
            st.markdown("**JDX**", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("### About This Assessment")
        st.markdown(
            """
        This assessment uses the **Job Intelligence Index (Job IQ)** framework developed from research with 227+ 
        organizations on job and skills data governance.
        
        **Time:** 5-7 minutes  
        **Questions:** 7 dimensions  
        **Output:** Personalized report with recommendations
        """
        )

        st.markdown("---")
        st.markdown("### Need Help?")
        st.markdown(
            """
        - [Contact JDX](https://jdxpert.com/contact/?utm_campaign=skills-gov-2025&utm_source=job-iq-app&utm_medium=referral&utm_content=contact)
        - [Learn More](https://jdxpert.com/?utm_campaign=skills-gov-2025&utm_source=job-iq-app&utm_medium=referral&utm_content=homepage)
        - [Schedule Consultation](https://jdxpert.com/book-a-demo/?utm_campaign=skills-gov-2025&utm_source=job-iq-app&utm_medium=referral&utm_content=book-demo)
        """
        )

    if st.session_state.assessment_complete:
        # Show full results page
        render_results(
            st.session_state.responses,
            st.session_state.scores,
            st.session_state.level_info,
        )
    elif st.session_state.results_ready:
        # Show "results ready" message with button to view full results
        render_intro()  # Keep intro for context
        render_results_ready_message()
    else:
        # Show assessment form and button
        render_intro()

        responses = render_assessment_form()

        # Submit button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Calculate My Job IQ", type="primary", use_container_width=True):
                with st.spinner("Calculating your Job IQ..."):
                    # Calculate scores
                    scores = calculate_jdmi_score(responses)
                    level_info = get_level_info(scores["total"])

                    # Store in session state
                    st.session_state.responses = responses
                    st.session_state.scores = scores
                    st.session_state.level_info = level_info
                    st.session_state.results_ready = True

                    # Clear cache and force clean refresh
                    cache_data.clear()

                st.rerun()

    # Footer
    st.markdown(
        """
    <div class="footer">
        <p><strong>Job IQ — Job Intelligence Index</strong> by JDX</p>
        <p>Based on research with 227+ organizations | Framework v1.0</p>
        <p>© 2025 JDXpert. All rights reserved.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
