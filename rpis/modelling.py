# creating the path for module errors
import sys
from pathlib import Path

PROJECT_ROOT = Path().resolve().parent  # go up one level
sys.path.append(str(PROJECT_ROOT))

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


# ---------------------------------------------------------
# 1. Fit tyre degradation model for a single stint
# ---------------------------------------------------------

def fit_degradation_model(stint_laps):
    """
    Fits a simple linear tyre degradation model:
    lap_time = a + b * lap_in_stint
    Returns: model, degradation_per_lap (b), base_lap_time (a)
    """
    laps = stint_laps.copy()

    # Lap index within the stint
    laps['LapInStint'] = laps['LapNumber'] - laps['LapNumber'].min() + 1

    X = laps[['LapInStint']]
    y = laps['LapTime'].dt.total_seconds()

    model = LinearRegression()
    model.fit(X, y)

    return model, model.coef_[0], model.intercept_


# ---------------------------------------------------------
# 2. Predict lap time using the model
# ---------------------------------------------------------

def predict_lap_time(model, lap_in_stint):
    """
    Predicts lap time (in seconds) for a given lap number in the stint.
    Uses a DataFrame to avoid sklearn warnings.
    """
    X = pd.DataFrame({'LapInStint': [lap_in_stint]})
    return float(model.predict(X))


# ---------------------------------------------------------
# 3. Simulate a full stint
# ---------------------------------------------------------

def simulate_stint(model, num_laps):
    """
    Simulates a stint of num_laps using the degradation model.
    Returns total stint time in seconds.
    """
    total = 0
    for lap in range(1, num_laps + 1):
        total += predict_lap_time(model, lap)
    return total


# ---------------------------------------------------------
# 4. Simulate a full race strategy
# ---------------------------------------------------------

def simulate_strategy(stint_plan, degradation_models, pit_loss=22):
    """
    Simulates a full race strategy.
    stint_plan: list of (compound, laps)
    degradation_models: dict {compound: model}
    pit_loss: time lost per pit stop (seconds)
    """
    total_time = 0
    num_stops = len(stint_plan) - 1

    for compound, laps in stint_plan:
        model = degradation_models[compound]
        total_time += simulate_stint(model, laps)

    total_time += num_stops * pit_loss
    return total_time


# ---------------------------------------------------------
# 5. Build tyre models for ALL compounds using ALL drivers
# ---------------------------------------------------------

def build_compound_models(segmented_laps, min_laps_per_compound=10):
    """
    Builds tyre degradation models for each compound (SOFT, MEDIUM, HARD)
    using laps from all drivers.
    Returns: dict {compound: model}
    """
    models = {}
    compounds = segmented_laps['Compound'].dropna().unique()

    for compound in compounds:
        compound_laps = segmented_laps[segmented_laps['Compound'] == compound].copy()

        if len(compound_laps) < min_laps_per_compound:
            continue

        compound_laps['LapInStint'] = (
            compound_laps.groupby(['Driver', 'Stint'])['LapNumber']
            .transform(lambda x: x - x.min() + 1)
        )

        X = compound_laps[['LapInStint']]
        y = compound_laps['LapTime'].dt.total_seconds()

        model = LinearRegression()
        model.fit(X, y)

        models[compound] = model

    return models



# ---------------------------------------------------------
# 6. Ensure all compounds exist (fallback logic)
# ---------------------------------------------------------

def ensure_compound_models(models):
    """
    Ensures we have models for SOFT, MEDIUM, HARD.
    If any are missing, approximate from existing ones.
    """
    compounds = ['SOFT', 'MEDIUM', 'HARD']

    for comp in compounds:
        if comp not in models:
            # Fallback priority: HARD → MEDIUM → SOFT
            if 'HARD' in models:
                models[comp] = models['HARD']
            elif 'MEDIUM' in models:
                models[comp] = models['MEDIUM']
            elif 'SOFT' in models:
                models[comp] = models['SOFT']

    return models


# ---------------------------------------------------------
# 7. Compare multiple strategies
# ---------------------------------------------------------

def compare_strategies(strategies, models, pit_loss=22):
    """
    Compare multiple strategies.
    strategies: dict {name: [(compound, laps), ...]}
    Returns: DataFrame with total times and delta to best.
    """
    results = []

    for name, stint_plan in strategies.items():
        total_time = simulate_strategy(stint_plan, models, pit_loss=pit_loss)
        results.append({
            'Strategy': name,
            'TotalTimeSec': total_time
        })

    df = pd.DataFrame(results)
    df['DeltaToBest'] = df['TotalTimeSec'] - df['TotalTimeSec'].min()
    df = df.sort_values('TotalTimeSec').reset_index(drop=True)

    return df