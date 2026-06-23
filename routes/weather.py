from flask import Blueprint, jsonify, request
from routes import state
import math

weather_bp = Blueprint('weather', __name__)

@weather_bp.route('/api/weather', methods=['GET'])
def get_weather():
    if not state.active_weather:
        return jsonify({"error": "No active weather scenario set"}), 500
    return jsonify(state.active_weather), 200

@weather_bp.route('/api/weather/scenario', methods=['POST'])
def set_weather_scenario():
    data = request.get_json(silent=True) or {}
    scenario_name = data.get('scenario')
    
    # Check if custom parameter overrides are provided
    is_custom = any(k in data for k in ["precip_mm", "humidity", "gust_speed", "gust_kph", "visibility", "vis_km", "condition_text"])
    
    if is_custom or (scenario_name and scenario_name.lower() not in [w["scenario"].lower() for w in state.DEFAULTS["weather"].get("weather_scenarios", [])]):
        # Dynamically build a custom scenario
        precip = data.get("precip_mm")
        if precip is None and "precip_mm" not in data:
            precip = 0.0
            
        humidity = data.get("humidity")
        if humidity is None and "humidity" not in data:
            humidity = 65
            
        gust = data.get("gust_speed") if "gust_speed" in data else data.get("gust_kph")
        if gust is None and "gust_speed" not in data and "gust_kph" not in data:
            gust = 5.0
            
        visibility = data.get("visibility") if "visibility" in data else data.get("vis_km")
        if visibility is None and "visibility" not in data and "vis_km" not in data:
            visibility = 10.0
            
        cond_text = data.get("condition_text") or data.get("scenario") or "Custom Weather"
        
        custom_scenario = {
            "scenario": scenario_name or "Custom Weather",
            "precip_mm": precip,
            "visibility": visibility,
            "gust_speed": gust,
            "humidity": humidity,
            "condition_text": cond_text
        }
        state.active_weather = custom_scenario
        return jsonify({
            "status": "success",
            "message": "Active weather scenario updated to custom overrides",
            "current_weather": state.active_weather
        }), 200
        
    # Match predefined scenario
    weather_scenarios = state.DEFAULTS["weather"].get("weather_scenarios", [])
    matched_scenario = next((w for w in weather_scenarios if w["scenario"].lower() == scenario_name.lower()), None)
    
    if not matched_scenario:
        valid_names = [w["scenario"] for w in weather_scenarios]
        return jsonify({
            "error": f"Scenario '{scenario_name}' not found",
            "valid_scenarios": valid_names
        }), 400
        
    state.active_weather = dict(matched_scenario)
    if "condition_text" not in state.active_weather:
        state.active_weather["condition_text"] = state.active_weather["scenario"]
        
    return jsonify({
        "status": "success",
        "message": f"Active weather scenario updated to {matched_scenario['scenario']}",
        "current_weather": state.active_weather
    }), 200

@weather_bp.route('/forecast.json', methods=['GET'])
def forecast_json():
    # Parse query params
    q = request.args.get('q', '')
    
    # Base active weather
    weather = state.active_weather or {
        "scenario": "Clear",
        "precip_mm": 0.0,
        "visibility": 10.0,
        "gust_speed": 5.0,
        "humidity": 60,
        "condition_text": "Clear"
    }
    
    # If a custom scenario override is active, we return it directly for testing.
    is_custom_active = state.active_weather and (
        state.active_weather.get("scenario") == "Custom Weather" or
        "Custom" in state.active_weather.get("scenario", "")
    )
    
    # Geolocation or Zone name matching (only if NOT custom weather override)
    if q and not is_custom_active:
        # Check if q is coordinates (lat, lng)
        if ',' in q:
            try:
                q_list = request.args.getlist('q')
                coord_str = None
                for q_val in q_list:
                    if ',' in q_val:
                        coord_str = q_val
                        break
                if not coord_str:
                    coord_str = q
                    
                parts = coord_str.split(',')
                lat = float(parts[0].strip())
                lng = float(parts[1].strip())
                
                # Find closest zone
                closest_zone_name = None
                min_dist = float('inf')
                for zone_name, coords in state.ZONE_COORDINATES.items():
                    dist = (lat - coords[0])**2 + (lng - coords[1])**2
                    if dist < min_dist:
                        min_dist = dist
                        closest_zone_name = zone_name
                
                if closest_zone_name:
                    matched_zone = next((z for z in state.active_zones if z["scenario"].lower() == closest_zone_name.lower()), None)
                    if matched_zone:
                        weather_state = matched_zone.get("weather_state", "Clear")
                        weather_scenarios = state.DEFAULTS["weather"].get("weather_scenarios", [])
                        matched_weather = next((w for w in weather_scenarios if w["scenario"].lower() == weather_state.lower()), None)
                        if matched_weather:
                            weather = dict(matched_weather)
                            if "condition_text" not in weather:
                                weather["condition_text"] = weather["scenario"]
            except Exception:
                pass
        else:
            # Match directly by zone name
            matched_zone = next((z for z in state.active_zones if z["scenario"].lower() == q.lower()), None)
            if matched_zone:
                weather_state = matched_zone.get("weather_state", "Clear")
                weather_scenarios = state.DEFAULTS["weather"].get("weather_scenarios", [])
                matched_weather = next((w for w in weather_scenarios if w["scenario"].lower() == weather_state.lower()), None)
                if matched_weather:
                    weather = dict(matched_weather)
                    if "condition_text" not in weather:
                        weather["condition_text"] = weather["scenario"]

    # Extract weather metrics
    precip = weather.get("precip_mm", 0.0)
    humidity = weather.get("humidity", 65)
    gust = weather.get("gust_speed") if "gust_speed" in weather else weather.get("gust_kph")
    if gust is None:
        gust = 5.0
    visibility = weather.get("visibility") if "visibility" in weather else weather.get("vis_km")
    if visibility is None:
        visibility = 10.0
    cond_text = weather.get("condition_text") or weather.get("scenario") or "Clear"
    
    # Construct standard WeatherAPI response
    response_payload = {
        "location": {
            "name": "Mock Location",
            "region": "Mock Region",
            "country": "Mock Country",
            "lat": 13.0827,
            "lon": 80.2707,
            "tz_id": "Asia/Kolkata",
            "localtime_epoch": 1782208800,
            "localtime": "2026-06-23 12:44"
        },
        "current": {
            "last_updated_epoch": 1782208800,
            "last_updated": "2026-06-23 12:44",
            "temp_c": 28.0,
            "temp_f": 82.4,
            "is_day": 1,
            "condition": {
                "text": cond_text,
                "icon": "//cdn.weatherapi.com/weather/64x64/day/113.png",
                "code": 1000
            },
            "wind_mph": 6.9,
            "wind_kph": 11.1,
            "wind_degree": 90,
            "wind_dir": "E",
            "pressure_mb": 1010.0,
            "pressure_in": 29.83,
            "precip_mm": precip,
            "precip_in": precip / 25.4 if isinstance(precip, (int, float)) else 0.0,
            "humidity": humidity,
            "cloud": 0,
            "feelslike_c": 30.0,
            "feelslike_f": 86.0,
            "vis_km": visibility,
            "vis_miles": visibility / 1.609 if isinstance(visibility, (int, float)) else 6.0,
            "uv": 6.0,
            "gust_mph": gust / 1.609 if isinstance(gust, (int, float)) else 3.1,
            "gust_kph": gust
        }
    }
    return jsonify(response_payload), 200

@weather_bp.route('/api/zone/weather', methods=['POST'])
def set_zone_weather():
    data = request.get_json(silent=True) or {}
    zone_name = data.get('zone')
    weather_state = data.get('weather_state')
    
    if not zone_name or not weather_state:
        return jsonify({"error": "Missing required fields: 'zone' and 'weather_state'"}), 400
        
    # Check if the weather state is valid
    weather_scenarios = state.DEFAULTS["weather"].get("weather_scenarios", [])
    valid_states = [w["scenario"] for w in weather_scenarios]
    matched_weather_scenario = next((w for w in weather_scenarios if w["scenario"].lower() == weather_state.lower()), None)
    
    if not matched_weather_scenario:
        return jsonify({
            "error": f"Weather state '{weather_state}' is invalid",
            "valid_states": valid_states
        }), 400
        
    # Find and update the zone in memory
    matched_zone = next((z for z in state.active_zones if z["scenario"].lower() == zone_name.lower()), None)
    if not matched_zone:
        return jsonify({
            "error": f"Zone '{zone_name}' not found",
            "available_zones": [z["scenario"] for z in state.active_zones]
        }), 400
        
    # Update weather state for the matched zone and any synchronized aliases (Chennai / Zone B)
    target_names = [zone_name.lower()]
    if zone_name.lower() in ["chennai", "zone b"]:
        target_names = ["chennai", "zone b"]
        
    for z in state.active_zones:
        if z["scenario"].lower() in target_names:
            z["weather_state"] = matched_weather_scenario["scenario"]
            
    return jsonify({
        "status": "success",
        "message": f"Updated weather for zone '{matched_zone['scenario']}' to '{matched_weather_scenario['scenario']}'",
        "zone": matched_zone
    }), 200

@weather_bp.route('/api/zones', methods=['GET'])
def get_all_zones():
    return jsonify({
        "zones": state.active_zones
    }), 200

