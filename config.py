"""
Configuration file for Job IQ Assessment Tool
Customize branding, benchmarks, and settings here
"""

# ===========================
# BRANDING & STYLING
# ===========================

COMPANY_NAME = "JDX"
PRODUCT_NAME = "Job IQ — Job Intelligence Index (powered by Oz)"
LOGO_URL = "https://via.placeholder.com/150x50/667eea/ffffff?text=JDX"  # Replace with your logo URL

# Primary brand colors (used in gradients and accents)
PRIMARY_COLOR_1 = "#0D5865"  # Dark teal
PRIMARY_COLOR_2 = "#3AC1CC"  # Teal

# Contact information
CONTACT_EMAIL = "info@jdxpert.com"
CONTACT_PHONE = ""
WEBSITE_URL = "https://jdxpert.com"
BOOKING_URL = "https://jdxpert.com/demo"

# Social media (optional)
LINKEDIN_URL = "https://www.linkedin.com/company/jdxpert"
TWITTER_URL = ""


# ===========================
# ASSESSMENT CONFIGURATION
# ===========================

# Assessment metadata
ASSESSMENT_VERSION = "1.0"
FRAMEWORK_VERSION = "Job IQ v1.0"
RESEARCH_SAMPLE_SIZE = 227
RESEARCH_REPORT_NAME = "State of Job & Skills Data Governance 2026"

# Scoring parameters
MAX_SCORE = 28
NUM_DIMENSIONS = 7
MAX_SCORE_PER_DIMENSION = 4

# Maturity level thresholds (score ranges)
LEVEL_THRESHOLDS = {
    1: (0, 5),      # Ad Hoc: 0-5
    2: (6, 10),     # Emerging: 6-10
    3: (11, 16),    # Defined: 11-16
    4: (17, 21),    # Governed: 17-21
    5: (22, 28)     # Optimized: 22-28
}


# ===========================
# BENCHMARKS (from research)
# ===========================

# Overall benchmarks
BENCHMARK_MEAN_SCORE = 14.28
BENCHMARK_MEDIAN_SCORE = 14.0

# Dimension averages (0-4 scale)
# Order: Coverage, Governance, Velocity, Architecture, Integration, Controls, Ability to Act
BENCHMARK_DIMENSION_SCORES = [1.95, 2.08, 1.94, 1.93, 2.52, 2.08, 1.78]

# Maturity level distribution (percentages)
BENCHMARK_LEVEL_DISTRIBUTION = {
    1: 4.0,   # Ad Hoc: 4%
    2: 37.0,  # Emerging: 37%
    3: 49.8,  # Defined: 49.8%
    4: 7.9,   # Governed: 7.9%
    5: 1.3    # Optimized: 1.3%
}

# High-coverage paradox metrics
HIGH_COVERAGE_THRESHOLD = 75  # % of jobs with skills defined
HIGH_COVERAGE_ORGS_COUNT = 54
HIGH_COVERAGE_PLANNING_OVERHAUL_PCT = 57.4  # % planning major governance changes


# ===========================
# FEATURE FLAGS
# ===========================

# Enable/disable features
ENABLE_PDF_DOWNLOAD = False  # PDF generation not yet implemented
ENABLE_EMAIL_DELIVERY = False  # Email delivery not yet implemented
ENABLE_ORG_INFO_COLLECTION = True  # Collect optional organization info
ENABLE_BENCHMARKING = True  # Show benchmark comparisons
ENABLE_INSIGHTS = True  # Show auto-generated insights
SHOW_INDUSTRY_AVERAGE_ON_RADAR = True  # Add benchmark line to radar chart


# ===========================
# UI/UX SETTINGS
# ===========================

# Assessment form
DEFAULT_EXPANDED_INFO = False  # Expand "About Job IQ" section by default
SHOW_PROGRESS_BAR = False  # Show completion progress (not yet implemented)

# Results page
SHOW_DIMENSION_DESCRIPTIONS = True  # Show "What is this dimension?" tooltips
SHOW_LEVEL_CHARACTERISTICS = True  # Show detailed level characteristics
NUM_RECOMMENDATIONS = 5  # Number of recommendations to display

# Visualization
RADAR_CHART_HEIGHT = 450  # pixels
USE_GRADIENT_COLORS = True  # Use gradient colors in visualizations


# ===========================
# COPY/MESSAGING
# ===========================

# Main tagline
TAGLINE = "Job Intelligence Index, powered by Oz — Calculated from job data quality, governance, usage, and architecture"

# Call-to-action buttons
CTA_PRIMARY = "Calculate My Job IQ"
CTA_SECONDARY = "Schedule Consultation"
CTA_RETAKE = "Retake Assessment"
CTA_DOWNLOAD = "Download Report (PDF)"

# Key message (shown in sidebar or intro)
KEY_MESSAGE = """
Our research shows that **coverage ≠ maturity**. 91% of organizations with high skills 
coverage still plan major governance overhauls because data becomes static and ungoverned.
"""


# ===========================
# DATA COLLECTION (future)
# ===========================

# Backend API endpoints (if implementing data collection)
API_BASE_URL = ""  # e.g., "https://api.jdxpert.com"
API_ENDPOINT_SUBMIT_ASSESSMENT = "/api/assessments"
API_ENDPOINT_SEND_EMAIL = "/api/send-results"

# Analytics/tracking
ENABLE_ANALYTICS = False
GOOGLE_ANALYTICS_ID = ""  # e.g., "G-XXXXXXXXXX"


# ===========================
# ADMIN/DEBUG
# ===========================

DEBUG_MODE = False  # Show debug info (scores, session state)
LOG_ASSESSMENTS_LOCALLY = False  # Save assessments to local CSV (for testing)
LOCAL_DATA_PATH = "./data/assessments.csv"


# ===========================
# HELPER FUNCTIONS
# ===========================

def get_level_from_score(score):
    """Map a score to its maturity level"""
    for level, (min_score, max_score) in LEVEL_THRESHOLDS.items():
        if min_score <= score <= max_score:
            return level
    return 1  # Default to Ad Hoc if out of range


def get_percentile(score):
    """Estimate percentile based on score (rough approximation)"""
    if score >= 22:
        return "Top 5%"
    elif score >= 20:
        return "Top 10%"
    elif score >= 17:
        return "Top 25%"
    elif score >= 14:
        return "Top 50%"
    else:
        return "Bottom 50%"

