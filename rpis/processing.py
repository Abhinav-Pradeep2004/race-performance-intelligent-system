# creating the path for module errors
import sys
from pathlib import Path

PROJECT_ROOT = Path().resolve().parent  # go up one level
sys.path.append(str(PROJECT_ROOT))

import pandas as pd

def clean_laps(laps_df):
    """
    Cleans and prepares laps data for analysis.
    Removes in/out laps and laps with missing times.
    """
    laps = laps_df.copy()
    laps = laps[laps['LapTime'].notna()]
    laps = laps[~laps['PitInTime'].notna()]   # remove in-laps
    laps = laps[~laps['PitOutTime'].notna()]  # remove out-laps
    return laps


def segment_stints(laps_df):
    """
    Segments stints based on tyre compound and pit stops.
    Returns a DataFrame with stint number assigned to each lap.
    """
    laps = laps_df.copy()
    laps = laps.sort_values(['Driver', 'LapNumber'])

    laps['Stint'] = 1
    for driver in laps['Driver'].unique():
        driver_laps = laps[laps['Driver'] == driver]
        stint = 1
        last_compound = None

        for idx, row in driver_laps.iterrows():
            if last_compound is None:
                last_compound = row['Compound']
            else:
                # New stint if compound changes or pit stop occurred
                if row['Compound'] != last_compound or pd.notna(row['PitInTime']):
                    stint += 1
                    last_compound = row['Compound']

            laps.at[idx, 'Stint'] = stint

    return laps


def compute_stint_summary(laps_df):
    """
    Computes average pace, tyre compound, and lap counts for each stint.
    """
    summary = laps_df.groupby(['Driver', 'Stint']).agg({
        'LapTime': 'mean',
        'Compound': 'first',
        'LapNumber': ['min', 'max', 'count']
    })

    summary.columns = ['AvgLapTime', 'Compound', 'StartLap', 'EndLap', 'LapCount']
    summary = summary.reset_index()

    return summary