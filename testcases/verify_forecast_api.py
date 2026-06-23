import requests
import json
import sys

BASE_URL = "http://127.0.0.1:5000"

def run_ts_simulation_logic(precip, humidity, wind_gust, visibility):
    try:
        precip = float(precip) if precip is not None else 0.0
    except (ValueError, TypeError):
        precip = 0.0
    try:
        humidity = float(humidity) if humidity is not None else 65.0
    except (ValueError, TypeError):
        humidity = 65.0
    try:
        wind_gust = float(wind_gust) if wind_gust is not None else 0.0
    except (ValueError, TypeError):
        wind_gust = 0.0
    try:
        visibility = float(visibility) if visibility is not None else 10.0
    except (ValueError, TypeError):
        visibility = 10.0

    level = 0
    # Level 0: Dry or Evaporating Rain
    if precip == 0.0 or (precip < 0.5 and humidity < 65.0):
        level = 0
    # Level 1: Light Rain / Drizzle
    elif 0.5 <= precip <= 2.5:
        level = 1
    # Level 2: Moderate / Steady Rain
    elif 2.5 < precip <= 7.5:
        level = 2
    # Level 3: Severe / Heavy Rain
    elif precip > 7.5:
        level = 3

    # Hazard Escalators
    if level == 2 and (wind_gust > 40.0 or visibility < 3.0):
        level = 3

    return level

def test_forecast_endpoint(q_param, expected_precip, expected_humidity, expected_level):
    url = f"{BASE_URL}/forecast.json?q={q_param}"
    print(f"Testing /forecast.json?q={q_param} ...")
    r = requests.get(url)
    if r.status_code != 200:
        print(f"FAIL: Expected 200, got {r.status_code}")
        return False
        
    data = r.json()
    
    # Verify structure
    if "location" not in data or "current" not in data:
        print("FAIL: Missing location or current object")
        return False
        
    current = data["current"]
    precip = current.get("precip_mm")
    humidity = current.get("humidity")
    wind_gust = current.get("gust_kph")
    visibility = current.get("vis_km")
    
    print(f"  Received: precip={precip}, humidity={humidity}, gust={wind_gust}, vis={visibility}")
    
    # Handle equivalence partitioning testing (where type might be string, null, etc.)
    # We only assert equality if types permit it
    if expected_precip is not None and not isinstance(expected_precip, str):
        if abs(float(precip) - float(expected_precip)) > 0.001:
            print(f"FAIL: Precip mismatch! Expected {expected_precip}, got {precip}")
            return False
            
    # Run TS simulation logic and check if it produces the expected level
    level = run_ts_simulation_logic(precip, humidity, wind_gust, visibility)
    if level != expected_level:
        print(f"FAIL: Level mismatch! TS logic computed Level {level}, expected Level {expected_level}")
        return False
        
    print(f"  SUCCESS (Computed Level: {level})\n")
    return True

def test_failure(fail_type, expected_status):
    url = f"{BASE_URL}/forecast.json?fail={fail_type}"
    print(f"Testing Failure: {fail_type} (Expected status: {expected_status}) ...")
    r = requests.get(url)
    print(f"  Status: {r.status_code}")
    if r.status_code != expected_status:
        print(f"FAIL: Expected status {expected_status}, got {r.status_code}")
        return False
    print("  SUCCESS\n")
    return True

def main():
    print("==================================================")
    print("STARTING WEATHER MOCK API VERIFICATION")
    print("==================================================")
    
    # 0. Reset scenario
    requests.post(f"{BASE_URL}/api/scenario/reset")
    
    # 1. Test coordinate lookups mapping to zone weather states
    # Bangalore coord -> Zone A -> Moderate Rain (precip=5.0, humidity=80, Level=2)
    if not test_forecast_endpoint("12.9716,77.5946", 5.0, 80, 2):
        sys.exit(1)
        
    # Chennai coord -> Chennai Zone -> Clear (precip=0.0, humidity=60, Level=0)
    if not test_forecast_endpoint("13.0827,80.2707", 0.0, 60, 0):
        sys.exit(1)

    # Delhi coord -> Delhi Zone -> Clear (precip=0.0, Level=0)
    if not test_forecast_endpoint("28.6139,77.2090", 0.0, 60, 0) :
        sys.exit(1)

    # 2. Test dynamic custom overrides (boundary values)
    boundaries = [
        # (precip, humidity, gust, vis, expected_level)
        (0.49, 60, 5.0, 10.0, 0),  # precip < 0.5 & humidity < 65 -> Level 0
        (0.49, 70, 5.0, 10.0, 0),  # precip < 0.5 but humidity >= 65 -> Level 0 (wait, in TS logic: precip < 0.5 and humidity < 65 is Level 0. What if humidity >= 65? It defaults to level 0 because precip is not >= 0.5)
        (0.50, 60, 5.0, 10.0, 1),  # precip >= 0.5 & precip <= 2.5 -> Level 1
        (0.51, 60, 5.0, 10.0, 1),  # Level 1
        (2.49, 60, 5.0, 10.0, 1),  # Level 1
        (2.50, 60, 5.0, 10.0, 1),  # Level 1
        (2.51, 60, 5.0, 10.0, 2),  # precip > 2.5 & precip <= 7.5 -> Level 2
        (7.49, 60, 5.0, 10.0, 2),  # Level 2
        (7.50, 60, 5.0, 10.0, 2),  # Level 2
        (7.51, 60, 5.0, 10.0, 3),  # precip > 7.5 -> Level 3
        # Test Hazard Escalation: Moderate Rain (Level 2) upgraded to Level 3 if gust > 40
        (5.0, 80, 45.0, 10.0, 3),  # Level 2 -> Level 3 (gust > 40)
        (5.0, 80, 5.0, 2.5, 3),    # Level 2 -> Level 3 (visibility < 3)
    ]
    
    for precip, humidity, gust, vis, expected_level in boundaries:
        print(f"Injecting: precip={precip}, humidity={humidity}, gust={gust}, vis={vis} ...")
        requests.post(f"{BASE_URL}/api/weather/scenario", json={
            "precip_mm": precip,
            "humidity": humidity,
            "gust_kph": gust,
            "vis_km": vis
        })
        if not test_forecast_endpoint("12.9716,77.5946", precip, humidity, expected_level):
            sys.exit(1)
            
    # 3. Test Failure simulations
    failures = [
        ("timeout", 408),
        ("http500", 500),
        ("http429", 429),
        ("malformed", 400),
        ("null", 500),
        ("invalidApiKey", 401),
        ("missingApiKey", 403),
    ]
    for fail_type, expected_status in failures:
        if not test_failure(fail_type, expected_status):
            sys.exit(1)
            
    print("==================================================")
    print("ALL WEATHER MOCK API TESTS COMPLETED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    main()
