# creating the path for module errors
import sys
from pathlib import Path

PROJECT_ROOT = Path().resolve().parent  # go up one level
sys.path.append(str(PROJECT_ROOT))

import pytest
import pandas as pd
from rpis.modelling import fit_degradation_model, predict_lap_time

def test_fit_degradation_model():
    # Fake data
    df = pd.DataFrame({
        'LapNumber': [1, 2, 3, 4, 5],
        'LapTime': pd.to_timedelta(["90s", "91s", "92s", "93s", "94s"])
    })
    model, b, a = fit_degradation_model(df)
    assert b > 0  # degradation slope should be positive

def test_predict_lap_time():
    df = pd.DataFrame({
        'LapNumber': [1, 2, 3],
        'LapTime': pd.to_timedelta(["90s", "91s", "92s"])
    })
    model, _, _ = fit_degradation_model(df)
    prediction = predict_lap_time(model, 2)
    assert isinstance(prediction, float)