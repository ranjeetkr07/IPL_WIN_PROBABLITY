
import streamlit as st
import pickle
import pandas as pd
from pathlib import Path

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="IPL Win Predictor",
    page_icon="🏏",
    layout="centered"
)

# ---------------- SIMPLE CSS DESIGN ----------------
st.markdown("""
<style>
.stApp {
    background: #101827;
    color: #f1f5f9;
}

.block-container {
    max-width: 950px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1, h2, h3, p, label {
    color: #f1f5f9 !important;
}

.header-box {
    background: #1e293b;
    border: 1px solid #334155;
    padding: 22px;
    border-radius: 14px;
    margin-bottom: 24px;
}

.header-box h1 {
    font-size: 30px;
    margin: 0;
}

.header-box p {
    color: #94a3b8 !important;
    margin: 8px 0 0;
}

.section-title {
    font-size: 20px;
    font-weight: 600;
    margin: 20px 0 12px;
}

div[data-baseweb="select"] > div {
    background-color: #1e293b !important;
    border: 1px solid #475569 !important;
    color: white !important;
}

div[data-baseweb="select"] * {
    color: white !important;
}

div[data-baseweb="popover"],
div[data-baseweb="menu"],
div[data-baseweb="option"] {
    background-color: #1e293b !important;
    color: white !important;
}

div[data-testid="stNumberInput"] input {
    background: #1e293b !important;
    color: white !important;
}

div[data-testid="stNumberInput"] button {
    background: #334155 !important;
    color: white !important;
}

.stButton > button {
    background: #0d9488;
    color: white;
    border: none;
    border-radius: 9px;
    height: 46px;
    font-size: 16px;
    font-weight: 600;
    width: 100%;
}

.stButton > button:hover {
    background: #0f766e;
    color: white;
    border: none;
}

[data-testid="stMetric"] {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 16px;
}

[data-testid="stMetricValue"] {
    color: #5eead4 !important;
}

div[data-testid="stProgressBar"] > div {
    background-color: #334155;
}

hr {
    border-color: #334155;
}

.footer {
    color: #94a3b8;
    text-align: center;
    font-size: 12px;
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TEAMS ----------------
teams = [
    "Sunrisers Hyderabad",
    "Mumbai Indians",
    "Royal Challengers Bangalore",
    "Kolkata Knight Riders",
    "Kings XI Punjab",
    "Chennai Super Kings",
    "Rajasthan Royals",
    "Delhi Capitals"
]

# ---------------- CITIES ----------------
cities = [
    "Hyderabad", "Bangalore", "Mumbai", "Indore",
    "Kolkata", "Delhi", "Chandigarh", "Jaipur",
    "Chennai", "Cape Town", "Port Elizabeth", "Durban",
    "Centurion", "East London", "Johannesburg", "Kimberley",
    "Bloemfontein", "Ahmedabad", "Cuttack", "Nagpur",
    "Dharamsala", "Visakhapatnam", "Pune", "Raipur",
    "Ranchi", "Abu Dhabi", "Sharjah", "Mohali", "Bengaluru"
]

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    model_path = Path(__file__).resolve().parent / "pipe.pkl"
    with open(model_path, "rb") as file:
        return pickle.load(file)

try:
    pipe = load_model()
except FileNotFoundError:
    st.error(
        "pipe.pkl file nahi mili. app.py aur pipe.pkl "
        "ko same folder mein rakhein."
    )
    st.stop()
except Exception as e:
    st.error(f"Model load nahi hua: {e}")
    st.stop()

# ---------------- HEADER ----------------
st.markdown("""
<div class="header-box">
    <h1>🏏 IPL Win Predictor</h1>
    <p>Predict match-winning probability using machine learning.</p>
</div>
""", unsafe_allow_html=True)

# ---------------- MATCH SETUP ----------------
st.markdown('<div class="section-title">Match Setup</div>',
            unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox(
        "Batting Team",
        sorted(teams)
    )

with col2:
    bowling_options = sorted(
        [team for team in teams if team != batting_team]
    )
    bowling_team = st.selectbox(
        "Bowling Team",
        bowling_options
    )

selected_city = st.selectbox(
    "Host City",
    sorted(cities)
)

# ---------------- MATCH SITUATION ----------------
st.markdown('<div class="section-title">Match Situation</div>',
            unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    target = st.number_input(
        "Target Runs",
        min_value=1,
        max_value=500,
        value=180,
        step=1
    )

    score = st.number_input(
        "Current Score",
        min_value=0,
        max_value=500,
        value=75,
        step=1
    )

with col2:
    overs = st.number_input(
        "Overs Completed",
        min_value=0.0,
        max_value=20.0,
        value=10.0,
        step=0.1,
        format="%.1f",
        help="Example: 10.3 means 10 overs and 3 balls."
    )

    wickets_out = st.number_input(
        "Wickets Lost",
        min_value=0,
        max_value=10,
        value=3,
        step=1
    )

st.caption("Overs example: 15.4 = 15 overs and 4 balls.")

# ---------------- PREDICT BUTTON ----------------
if st.button("Predict Winning Probability"):

    # Convert cricket overs notation to balls
    whole_overs = int(overs)
    extra_balls = round((overs - whole_overs) * 10)

    if extra_balls < 0 or extra_balls > 5:
        st.error(
            "Invalid overs! Decimal part must be between .0 and .5."
        )

    elif whole_overs == 20 and extra_balls != 0:
        st.error("Overs cannot exceed 20.")

    elif score >= target:
        st.success(
            f"{batting_team} has reached or exceeded the target!"
        )

    elif whole_overs * 6 + extra_balls >= 120:
        st.error("20 overs complete. No balls remain.")

    elif wickets_out >= 10:
        st.error("All 10 wickets have fallen.")

    else:
        balls_bowled = whole_overs * 6 + extra_balls
        balls_left = 120 - balls_bowled
        runs_left = int(target - score)
        wickets_remaining = 10 - int(wickets_out)

        overs_bowled = balls_bowled / 6

        crr = (
            float(score) / overs_bowled
            if overs_bowled > 0 else 0.0
        )

        rrr = (runs_left * 6) / balls_left

        # Input columns must match the training pipeline
        input_df = pd.DataFrame({
            "batting_team": [batting_team],
            "bowling_team": [bowling_team],
            "city": [selected_city],
            "runs_left": [runs_left],
            "balls_left": [balls_left],
            "wickets": [wickets_remaining],
            "total_runs_x": [int(target)],
            "crr": [crr],
            "rrr": [rrr]
        })

        try:
            result = pipe.predict_proba(input_df)[0]

            # Assumes class 0 = loss and class 1 = win
            loss = float(result[0])
            win = float(result[1])

            st.markdown("---")
            st.markdown(
                '<div class="section-title">Match Prediction</div>',
                unsafe_allow_html=True
            )

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    batting_team,
                    f"{win * 100:.1f}%"
                )
                st.progress(max(0.0, min(1.0, win)))

            with col2:
                st.metric(
                    bowling_team,
                    f"{loss * 100:.1f}%"
                )
                st.progress(max(0.0, min(1.0, loss)))

            st.markdown("---")
            st.markdown("### Match Summary")

            col1, col2, col3 = st.columns(3)

            col1.metric("Runs Required", runs_left)
            col2.metric("Balls Left", balls_left)
            col3.metric("Wickets Left", wickets_remaining)

            st.caption(
                f"Current Run Rate: {crr:.2f} | "
                f"Required Run Rate: {rrr:.2f}"
            )

            st.info(
                "This is a machine-learning estimate, not a guarantee. "
                "Prediction quality depends on the training data."
            )

        except Exception as e:
            st.error(f"Prediction error: {e}")
            st.warning(
                "Check the model's training columns, team names, "
                "city names and scikit-learn compatibility."
            )

# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">
    IPL Win Predictor · Python · Streamlit · Machine Learning
</div>
""", unsafe_allow_html=True)
