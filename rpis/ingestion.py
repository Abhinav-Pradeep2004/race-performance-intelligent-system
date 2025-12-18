# creating the path for module errors
import sys
from pathlib import Path

PROJECT_ROOT = Path().resolve().parent  # go up one level
sys.path.append(str(PROJECT_ROOT))

import fastf1
from fastf1 import plotting

fastf1.Cache.enable_cache(r"F:\race-performance-intelligent-system\data\cache")

# Download the data and cache data
"""
    Loads an F1 race session using FastF1.
    session_type: "R" = Race, "Q" = Qualifying, "FP1", "FP2", "FP3"
    """

def load_race_session(year, grand_prix, session_type="R"):
    session = fastf1.get_session(year, grand_prix, session_type)
    session.load()

    return session

def get_laps(session):
    return session.laps

def get_driver_fastest_lap(session, driver_code):
    lap = session.laps.pick_driver(driver_code).pick_fastest()
    return lap

def get_driver_telemetry(lap):
    return lap.get_car_data().add_distance()