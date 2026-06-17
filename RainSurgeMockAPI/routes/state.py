import json
import os

# Base paths
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# Default template loads
DEFAULTS = {
    "weather": load_json("weather.json"),
    "boundaries": load_json("boundaries.json"),
    "failures": load_json("failures.json"),
    "cache": load_json("cache.json"),
    "zones": load_json("zones.json"),
    "quotations": load_json("quotations.json"),
    "orders": load_json("orders.json"),
    "earnings": load_json("earnings.json"),
    "settlements": load_json("settlements.json"),
    "reports": load_json("reports.json"),
    "app_ui": load_json("app_ui.json"),
    "app_earnings": load_json("app_earnings.json"),
    "app_business_logic": load_json("app_business_logic.json"),
    "business_rules": load_json("business_rules.json"),
}

# Configurable LSP Pricing settings
lsp_pricing_config = {
    "NORMAL": 0.0,
    "WATCH": 15.0,
    "SURGE": 30.0,
    "CRITICAL": 50.0
}

# In-memory active states
active_weather = None
active_cache = None
active_zones = []
active_business_rule_scenario = None
active_orders = {}
active_rain_surge = 0.0

def calculateRainSeverity(payload):
    current = payload.get("current", {})
    precip = current.get("precip_mm") or 0.0
    visibility = current.get("vis_km") or 10.0
    gust = current.get("gust_kph") or 0.0
    condition_obj = current.get("condition", {})
    condition = ""
    if isinstance(condition_obj, dict):
        condition = condition_obj.get("text", "").lower()
    else:
        condition = str(condition_obj).lower()

    score = 0
    
    # 1. PRECIPITATION SCORE (0-50)
    if precip >= 50:
        score += 50
    elif precip >= 20:
        score += 40
    elif precip >= 8:
        score += 30
    elif precip >= 3:
        score += 20
    elif precip >= 0.5:
        score += 10
        
    # 2. VISIBILITY SCORE (0-20)
    if visibility <= 1:
        score += 20
    elif visibility <= 3:
        score += 15
    elif visibility <= 5:
        score += 10
    elif visibility <= 8:
        score += 5
        
    # 3. WIND SCORE (0-15)
    if gust >= 70:
        score += 15
    elif gust >= 50:
        score += 10
    elif gust >= 35:
        score += 5
        
    # 4. WEATHER TEXT SCORE (0-15)
    if "thunder" in condition or "storm" in condition:
        score += 15
    elif "heavy" in condition:
        score += 10
    elif "rain" in condition:
        score += 5
        
    return min(score, 100)

def getRainSurgeLevel(severity_score):
    if severity_score < 10:
        return "NORMAL"
    elif severity_score < 30:
        return "WATCH"
    elif severity_score < 50:
        return "SURGE"
    else:
        return "CRITICAL"

def reset_state():
    global active_weather, active_cache, active_zones, active_business_rule_scenario, active_orders, active_rain_surge
    active_rain_surge = 0.0
    
    # 1. Reset Weather (Default to Clear Weather scenario)
    weather_scenarios = DEFAULTS["weather"].get("weather_scenarios", [])
    active_weather = next((w for w in weather_scenarios if w["scenario"] == "Clear Weather"), None)
    if not active_weather and weather_scenarios:
        active_weather = weather_scenarios[0]
        
    # 2. Reset Cache (Default to Valid Cache or first cache scenario)
    cache_scenarios = DEFAULTS["cache"].get("cache_scenarios", [])
    active_cache = next((c for c in cache_scenarios if c["scenario"] == "Valid Cache"), None)
    if not active_cache and cache_scenarios:
        active_cache = cache_scenarios[0]
        
    # 3. Reset Zones (Load all default zones)
    active_zones = [dict(z) for z in DEFAULTS["zones"].get("zones", [])]
    
    # 4. Reset Business Rules (No active override scenario by default)
    active_business_rule_scenario = None
    
    # 5. Reset Orders (Empty dynamic orders dict)
    active_orders = {}

# Initialize on import
reset_state()
