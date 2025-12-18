# creating the path for module errors
import sys
from pathlib import Path

PROJECT_ROOT = Path().resolve().parent  # go up one level
sys.path.append(str(PROJECT_ROOT))

import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

from rpis.ingestion import load_race_session
from rpis.processing import clean_laps, segment_stints, compute_stint_summary
from rpis.modelling import build_compound_models, ensure_compound_models, compare_strategies

# -------------------------------
# Streamlit App Layout
# -------------------------------

st.title("Race Performance Intelligence System (RPIS)")

# Sidebar controls
year = st.sidebar.selectbox("Select Year", [2023, 2024])
gp = st.sidebar.text_input("Grand Prix Name", "Bahrain")
session_type = st.sidebar.selectbox("Session Type", ["R", "Q"])

driver = st.sidebar.text_input("Driver Code", "VER")

# Load session
session = load_race_session(year, gp, session_type)
laps = clean_laps(session.laps)
segmented = segment_stints(laps)

# -------------------------------
# Lap-time evolution plot
# -------------------------------
driver_laps = segmented[segmented['Driver'] == driver]

fig = px.scatter(
    driver_laps,
    x="LapNumber",
    y=driver_laps['LapTime'].dt.total_seconds(),
    color="Compound",
    title=f"Lap Time Evolution - {driver}"
)
st.plotly_chart(fig)

# -------------------------------
# Stint summary table
# -------------------------------
summary = compute_stint_summary(segmented)
st.subheader("Stint Summary")
st.dataframe(summary[summary['Driver'] == driver])

# -------------------------------
# Strategy comparison
# -------------------------------
st.subheader("Strategy Comparison")

models = build_compound_models(segmented)
models = ensure_compound_models(models)

strategies = {
    "1-stop: S-H": [("SOFT", 15), ("HARD", 35)],
    "2-stop: S-M-H": [("SOFT", 10), ("MEDIUM", 20), ("HARD", 20)]
}

comparison = compare_strategies(strategies, models, pit_loss=22)
st.dataframe(comparison)