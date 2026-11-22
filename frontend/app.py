import math
import os

import requests
import streamlit as st

# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="HomeValue AI | Property Valuation",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

API_BASE_URL = os.getenv(
    "HOUSE_PRICE_API_URL",
    "http://127.0.0.1:8000"
).rstrip("/")

# ============================================================
# 2. SESSION STATE
# ============================================================

if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None

if "prediction_inputs" not in st.session_state:
    st.session_state.prediction_inputs = None

if "prediction_error" not in st.session_state:
    st.session_state.prediction_error = None

# ============================================================
# 3. WARM SAGE DESIGN SYSTEM
# ============================================================

st.html("""
<style>

    :root {
        --bg-main: #EEE5D8;
        --bg-soft: #F7F1E8;
        --card-bg: #FBF8F3;
        --card-edge: #D8CCBC;
        --text-main: #2F3A31;
        --text-soft: #6D756A;
        --sage: #6D7F57;
        --sage-dark: #556544;
        --sage-light: #E7E9DD;
        --forest: #43553D;
        --hero-glow: #D8E0CF;
        --success-bg: #E6EFE3;
        --success-text: #3F5B36;
        --error-bg: #F8E7E4;
        --error-text: #8A4A44;
        --note-bg: #ECE6D9;
        --note-text: #4B5849;
    }

    /* -------------------------------------------------
       MAIN APP
    ------------------------------------------------- */

    .stApp,
    [data-testid="stAppViewContainer"] {
        background: var(--bg-main) !important;
        color: var(--text-main) !important;
    }

    [data-testid="stHeader"] {
        background: rgba(238,229,216,0.96) !important;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* -------------------------------------------------
       TYPOGRAPHY
    ------------------------------------------------- */

    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp h4,
    .stApp h5,
    .stApp h6 {
        color: var(--text-main) !important;
        letter-spacing: -0.025em;
    }

    .stApp p,
    .stApp label,
    .stApp span,
    .stApp li {
        color: var(--text-main);
    }

    [data-testid="stCaptionContainer"],
    .stApp small {
        color: var(--text-soft) !important;
    }

    /* -------------------------------------------------
       HERO SECTION
    ------------------------------------------------- */

    .hv-hero {
        background:
            radial-gradient(
                circle at 88% 18%,
                rgba(132, 157, 115, 0.18),
                transparent 38%
            ),
            linear-gradient(
                130deg,
                #F8F2E9 0%,
                #F3EEE4 58%,
                #E6E1D2 100%
            );
        border: 1px solid #DDD2C2;
        border-radius: 24px;
        padding: 42px 44px;
        margin-bottom: 28px;
        box-shadow: 0 10px 28px rgba(86, 79, 64, 0.06);
    }

    .hv-eyebrow {
        color: var(--sage-dark);
        text-transform: uppercase;
        font-weight: 800;
        font-size: 12px;
        letter-spacing: 2px;
        margin-bottom: 14px;
    }

    .hv-title {
        font-size: clamp(34px, 4vw, 54px);
        font-weight: 850;
        color: var(--text-main);
        line-height: 1.12;
        margin-bottom: 14px;
        letter-spacing: -0.035em;
    }

    .hv-subtitle {
        color: #586457;
        font-size: 16px;
        line-height: 1.8;
        max-width: 700px;
    }

    .hv-tags {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin-top: 24px;
    }

    .hv-tag {
        padding: 8px 13px;
        background: rgba(255,255,255,0.72);
        border: 1px solid #D8D0C2;
        color: var(--sage-dark);
        border-radius: 30px;
        font-size: 12px;
        font-weight: 700;
        box-shadow: 0 2px 5px rgba(70, 63, 54, 0.03);
    }

    /* -------------------------------------------------
       FORM SHELL / CONTAINERS
    ------------------------------------------------- */

    [data-testid="stForm"] {
        background: var(--card-bg) !important;
        border: 1px solid var(--card-edge) !important;
        border-radius: 18px !important;
        padding: 15px !important;
        box-shadow: 0 7px 20px rgba(72, 66, 55, 0.04);
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        background: var(--card-bg) !important;
        border-color: var(--card-edge) !important;
        border-radius: 16px !important;
    }

    /* -------------------------------------------------
       NUMBER INPUTS
    ------------------------------------------------- */

    div[data-testid="stNumberInput"] [data-baseweb="input"] {
        background: #F9F6F0 !important;
        border: 1px solid #D6CBB8 !important;
        border-radius: 10px !important;
    }

    div[data-testid="stNumberInput"] input {
        background: #F9F6F0 !important;
        color: var(--text-main) !important;
        border-radius: 10px !important;
        font-weight: 500 !important;
    }

    div[data-testid="stNumberInput"] button {
        background: #EEF0E8 !important;
        color: var(--sage-dark) !important;
        border-color: #D3D8CB !important;
    }

    div[data-testid="stNumberInput"] button:hover {
        background: #E0E6D8 !important;
        color: var(--forest) !important;
    }

    [data-testid="stWidgetLabel"] p {
        color: #465246 !important;
        font-weight: 650;
    }

    /* -------------------------------------------------
       SLIDER
    ------------------------------------------------- */

    [data-testid="stSlider"] [role="slider"] {
        background: var(--sage) !important;
        border-color: var(--sage) !important;
        box-shadow: 0 0 0 2px #FFFFFF !important;
    }

    [data-testid="stSlider"] [data-baseweb="slider"] {
        color: var(--sage) !important;
    }

    /* -------------------------------------------------
       FORM BUTTON
    ------------------------------------------------- */

    div[data-testid="stFormSubmitButton"] button {
        width: 100% !important;
        min-height: 52px !important;
        border-radius: 12px !important;
        background: linear-gradient(
            120deg,
            #6C7E58,
            #566846
        ) !important;
        color: #FFFFFF !important;
        border: 1px solid #6C7E58 !important;
        font-size: 15px !important;
        font-weight: 750 !important;
        box-shadow: 0 5px 14px rgba(92, 110, 75, 0.16);
        transition: all 0.2s ease;
    }

    div[data-testid="stFormSubmitButton"] button:hover {
        background: linear-gradient(
            120deg,
            #7B8E65,
            #62764F
        ) !important;
        color: #FFFFFF !important;
        border-color: #7B8E65 !important;
        box-shadow: 0 7px 18px rgba(92, 110, 75, 0.22);
    }

    div[data-testid="stFormSubmitButton"] button:focus,
    div[data-testid="stFormSubmitButton"] button span,
    div[data-testid="stFormSubmitButton"] button p,
    div[data-testid="stFormSubmitButton"] button div {
        color: #FFFFFF !important;
    }

    /* -------------------------------------------------
       RESULT CARD
    ------------------------------------------------- */

    .hv-result {
        background: linear-gradient(
            135deg,
            #566846 0%,
            #6E815A 58%,
            #7E9370 100%
        );
        border: 1px solid #728865;
        border-radius: 18px;
        padding: 30px 28px;
        margin-bottom: 16px;
        box-shadow: 0 12px 28px rgba(92, 110, 75, 0.15);
    }

    .hv-result-label {
        text-transform: uppercase;
        color: #F1F7EA;
        font-weight: 750;
        font-size: 12px;
        letter-spacing: 1.5px;
    }

    .hv-result-price {
        font-size: clamp(30px, 3.8vw, 49px);
        font-weight: 850;
        line-height: 1.2;
        color: #FFFFFF;
        margin: 16px 0;
        overflow-wrap: anywhere;
    }

    .hv-result-note {
        font-size: 13px;
        line-height: 1.7;
        color: #F3F8EE;
    }

    /* -------------------------------------------------
       CUSTOM MESSAGE BOXES
    ------------------------------------------------- */

    .hv-success {
        background: var(--success-bg);
        border: 1px solid #CBDAC3;
        color: var(--success-text);
        border-radius: 12px;
        padding: 12px 14px;
        font-weight: 650;
        margin-bottom: 16px;
    }

    .hv-error {
        background: var(--error-bg);
        border: 1px solid #E8C9C4;
        color: var(--error-text);
        border-radius: 12px;
        padding: 12px 14px;
        font-weight: 650;
        margin-bottom: 16px;
        line-height: 1.6;
    }

    .hv-note {
        background: var(--note-bg);
        border: 1px solid #D4CBB9;
        color: var(--note-text);
        border-radius: 12px;
        padding: 14px 16px;
        line-height: 1.75;
        font-size: 13px;
        margin-top: 14px;
    }

    /* -------------------------------------------------
       DATA ROWS
    ------------------------------------------------- */

    .hv-data-row {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        gap: 12px;
        padding: 13px 0;
        border-bottom: 1px solid #E4DDD1;
    }

    .hv-data-row:last-child {
        border-bottom: none;
    }

    .hv-data-label {
        font-size: 13px;
        color: var(--text-soft);
    }

    .hv-data-value {
        font-size: 14px;
        color: var(--text-main);
        font-weight: 750;
        text-align: right;
    }

    /* -------------------------------------------------
       FOOTER
    ------------------------------------------------- */

    .hv-footer {
        text-align: center;
        color: #7C8078;
        font-size: 12px;
        border-top: 1px solid #D8CCBC;
        padding-top: 20px;
        margin-top: 38px;
    }

    /* -------------------------------------------------
       MOBILE
    ------------------------------------------------- */

    @media (max-width: 768px) {

        .block-container {
            padding: 1rem;
        }

        .hv-hero {
            padding: 25px 20px;
            margin-bottom: 20px;
        }

        .hv-result {
            padding: 22px 18px;
        }

        .hv-tags {
            gap: 7px;
        }

        .hv-tag {
            font-size: 11px;
        }
    }

</style>
""")

# ============================================================
# 4. HERO SECTION
# ============================================================

st.html("""
<section class="hv-hero">

    <div class="hv-eyebrow">
        Intelligent Property Valuation
    </div>

    <div class="hv-title">
        HomeValue AI
    </div>

    <div class="hv-subtitle">
        Discover your property's estimated value with
        machine learning. Enter your property details,
        analyze important features, and generate an
        instant price estimate.
    </div>

    <div class="hv-tags">
        <span class="hv-tag">Machine Learning</span>
        <span class="hv-tag">8 Property Features</span>
        <span class="hv-tag">Random Forest</span>
        <span class="hv-tag">Instant Estimation</span>
    </div>

</section>
""")

# ============================================================
# 5. MAIN DASHBOARD COLUMNS
# ============================================================

left_col, right_col = st.columns(
    [1.25, 1],
    gap="large"
)

# ============================================================
# 6. LEFT COLUMN - PROPERTY FORM
# ============================================================

with left_col:

    st.subheader("Property Information")

    st.caption(
        "Complete the following details to calculate "
        "an estimated property value."
    )

    with st.form(
        "property_form",
        clear_on_submit=False
    ):

        # ----------------------------------------------------
        # PROPERTY QUALITY
        # ----------------------------------------------------

        with st.container(border=True):

            st.markdown("#### 01 — Property Quality")

            overall_qual = st.slider(
                "Overall Construction Quality",
                min_value=1,
                max_value=10,
                value=5,
                help=(
                    "Overall quality of materials "
                    "and finishes, from 1 to 10."
                ),
            )

        # ----------------------------------------------------
        # INTERIOR SPACE
        # ----------------------------------------------------

        with st.container(border=True):

            st.markdown("#### 02 — Interior Space")

            st.caption(
                "Provide interior measurements "
                "in square feet."
            )

            input_col1, input_col2 = st.columns(2)

            with input_col1:

                gr_liv_area = st.number_input(
                    "Above-Ground Living Area",
                    min_value=0.0,
                    value=1500.0,
                    step=50.0,
                    help="Total above-ground living area."
                )

                first_flr_sf = st.number_input(
                    "First Floor Area",
                    min_value=0.0,
                    value=1000.0,
                    step=50.0
                )

                total_bsmt_sf = st.number_input(
                    "Total Basement Area",
                    min_value=0.0,
                    value=800.0,
                    step=50.0
                )

            with input_col2:

                second_flr_sf = st.number_input(
                    "Second Floor Area",
                    min_value=0.0,
                    value=500.0,
                    step=50.0
                )

                bsmt_fin_sf1 = st.number_input(
                    "Finished Basement Area",
                    min_value=0.0,
                    value=400.0,
                    step=50.0
                )

        # ----------------------------------------------------
        # LAND AND GARAGE
        # ----------------------------------------------------

        with st.container(border=True):

            st.markdown("#### 03 — Land & Parking")

            land_col, garage_col = st.columns(2)

            with land_col:

                lot_area = st.number_input(
                    "Lot Area (sq ft)",
                    min_value=0.0,
                    value=8000.0,
                    step=100.0
                )

            with garage_col:

                garage_area = st.number_input(
                    "Garage Area (sq ft)",
                    min_value=0.0,
                    value=500.0,
                    step=25.0
                )

        # ----------------------------------------------------
        # PREDICTION BUTTON
        # ----------------------------------------------------

        submitted = st.form_submit_button(
            "Estimate Property Value",
            type="primary",
            use_container_width=True
        )

# ============================================================
# 7. PROCESS PROPERTY PREDICTION
# ============================================================

if submitted:

    st.session_state.prediction_error = None
    st.session_state.prediction_result = None
    st.session_state.prediction_inputs = None

    if gr_liv_area <= 0:

        st.session_state.prediction_error = (
            "Above-ground living area must be "
            "greater than zero."
        )

    elif lot_area <= 0:

        st.session_state.prediction_error = (
            "Lot area must be greater than zero."
        )

    elif bsmt_fin_sf1 > total_bsmt_sf:

        st.session_state.prediction_error = (
            "Finished basement area cannot exceed "
            "total basement area."
        )

    else:

        house_data = {
            "OverallQual": overall_qual,
            "GrLivArea": gr_liv_area,
            "TotalBsmtSF": total_bsmt_sf,
            "SecondFlrSF": second_flr_sf,
            "BsmtFinSF1": bsmt_fin_sf1,
            "FirstFlrSF": first_flr_sf,
            "LotArea": lot_area,
            "GarageArea": garage_area,
        }

        try:

            with st.spinner(
                "Analyzing property information..."
            ):

                response = requests.post(
                    f"{API_BASE_URL}/predict",
                    json=house_data,
                    timeout=120
                )

                response.raise_for_status()

                result = response.json()

                predicted_price = float(
                    result["predicted_price"]
                )

                if not math.isfinite(predicted_price):
                    raise ValueError(
                        "The prediction is not finite."
                    )

                st.session_state.prediction_result = (
                    predicted_price
                )

                st.session_state.prediction_inputs = (
                    house_data
                )

        except requests.exceptions.ConnectionError:

            st.session_state.prediction_error = (
                "Cannot connect to the backend. "
                "Make sure FastAPI is running on port 8000."
            )

        except requests.exceptions.Timeout:

            st.session_state.prediction_error = (
                "The server took too long to respond. "
                "Please try again."
            )

        except requests.exceptions.HTTPError as error:

            st.session_state.prediction_error = (
                f"API request failed "
                f"({error.response.status_code}). "
                "Check the FastAPI terminal."
            )

        except (
            requests.exceptions.RequestException,
            ValueError,
            TypeError,
            KeyError,
        ):

            st.session_state.prediction_error = (
                "An unexpected prediction error occurred. "
                "Please check the backend terminal."
            )

# ============================================================
# 8. RIGHT COLUMN - VALUATION RESULTS
# ============================================================

with right_col:

    st.subheader("Property Valuation")

    prediction = st.session_state.prediction_result

    # --------------------------------------------------------
    # PREDICTION CARD
    # --------------------------------------------------------

    if prediction is None:

        st.html("""
        <section class="hv-result">

            <div class="hv-result-label">
                Estimated Property Value
            </div>

            <div class="hv-result-price">
                $ —
            </div>

            <div class="hv-result-note">
                Your estimated property value will
                appear here after you submit your
                property information.
            </div>

        </section>
        """)

    else:

        st.html(f"""
        <section class="hv-result">

            <div class="hv-result-label">
                Estimated Property Value
            </div>

            <div class="hv-result-price">
                ${prediction:,.2f}
            </div>

            <div class="hv-result-note">
                Estimated using Random Forest Regression
                on historical housing data.
            </div>

        </section>
        """)

        st.html("""
        <div class="hv-success">
            Your property valuation is ready.
        </div>
        """)

    # --------------------------------------------------------
    # ERROR MESSAGE
    # --------------------------------------------------------

    if st.session_state.prediction_error:

        st.html(f"""
        <div class="hv-error">
            {st.session_state.prediction_error}
        </div>
        """)

    # --------------------------------------------------------
    # PROPERTY SNAPSHOT
    # --------------------------------------------------------

    with st.container(border=True):

        st.markdown("#### Property Overview")

        details = st.session_state.prediction_inputs

        if details is None:

            st.caption(
                "Current values entered in the form"
            )

            details = {
                "OverallQual": overall_qual,
                "GrLivArea": gr_liv_area,
                "TotalBsmtSF": total_bsmt_sf,
                "LotArea": lot_area,
                "GarageArea": garage_area,
            }

        else:

            st.caption(
                "Property details used for your estimate"
            )

        st.html(f"""
        <div class="hv-data-row">
            <span class="hv-data-label">
                Overall Quality
            </span>
            <span class="hv-data-value">
                {details['OverallQual']} / 10
            </span>
        </div>

        <div class="hv-data-row">
            <span class="hv-data-label">
                Living Area
            </span>
            <span class="hv-data-value">
                {details['GrLivArea']:,.0f} sq ft
            </span>
        </div>

        <div class="hv-data-row">
            <span class="hv-data-label">
                Basement Area
            </span>
            <span class="hv-data-value">
                {details['TotalBsmtSF']:,.0f} sq ft
            </span>
        </div>

        <div class="hv-data-row">
            <span class="hv-data-label">
                Lot Area
            </span>
            <span class="hv-data-value">
                {details['LotArea']:,.0f} sq ft
            </span>
        </div>

        <div class="hv-data-row">
            <span class="hv-data-label">
                Garage Area
            </span>
            <span class="hv-data-value">
                {details['GarageArea']:,.0f} sq ft
            </span>
        </div>
        """)

    # --------------------------------------------------------
    # MODEL DETAILS
    # --------------------------------------------------------

    with st.container(border=True):

        st.markdown("#### Prediction Technology")

        st.html("""
        <div class="hv-data-row">
            <span class="hv-data-label">
                Prediction Model
            </span>
            <span class="hv-data-value">
                Random Forest
            </span>
        </div>

        <div class="hv-data-row">
            <span class="hv-data-label">
                Input Features
            </span>
            <span class="hv-data-value">
                8 Features
            </span>
        </div>

        <div class="hv-data-row">
            <span class="hv-data-label">
                Price Currency
            </span>
            <span class="hv-data-value">
                USD
            </span>
        </div>

        <div class="hv-data-row">
            <span class="hv-data-label">
                Prediction Engine
            </span>
            <span class="hv-data-value">
                FastAPI + Scikit-Learn
            </span>
        </div>
        """)

        st.html("""
        <div class="hv-note">
            This estimate is generated using an educational
            machine-learning model trained on historical
            housing data. It should not be treated as a
            formal real-estate appraisal.
        </div>
        """)

# ============================================================
# 9. FOOTER
# ============================================================

st.html("""
<footer class="hv-footer">

    HomeValue AI · Machine Learning Property Valuation

    <div style="margin-top:6px;">
        Built with Python, Streamlit, FastAPI
        and Scikit-Learn
    </div>

</footer>
""")