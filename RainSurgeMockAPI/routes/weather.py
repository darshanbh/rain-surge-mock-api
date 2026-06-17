from flask import Blueprint, jsonify, request
from routes import state

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
    if not scenario_name:
        return jsonify({"error": "Missing required field: scenario"}), 400
        
    weather_scenarios = state.DEFAULTS["weather"].get("weather_scenarios", [])
    matched_scenario = next((w for w in weather_scenarios if w["scenario"].lower() == scenario_name.lower()), None)
    
    if not matched_scenario:
        # Fallback to try partial matching or list of valid values
        valid_names = [w["scenario"] for w in weather_scenarios]
        return jsonify({
            "error": f"Scenario '{scenario_name}' not found",
            "valid_scenarios": valid_names
        }), 400
        
    state.active_weather = matched_scenario
    return jsonify({
        "status": "success",
        "message": f"Active weather scenario updated to {matched_scenario['scenario']}",
        "current_weather": state.active_weather
    }), 200
