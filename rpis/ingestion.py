# creating the path for module errors
import os
import fastf1

# Use a relative cache directory inside your project
cache_dir = os.path.join(os.path.dirname(__file__), "..", "data", "cache")
os.makedirs(cache_dir, exist_ok=True)

fastf1.Cache.enable_cache("/tmp/f1cache")

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