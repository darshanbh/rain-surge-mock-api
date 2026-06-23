from flask import Blueprint, jsonify, request
from routes import state
import datetime

cache_bp = Blueprint('cache', __name__)

@cache_bp.route('/api/cache', methods=['GET'])
def get_cache():
    if not state.active_cache:
        return jsonify({"error": "No active cache state set"}), 500
    return jsonify(state.active_cache), 200

@cache_bp.route('/api/cache/age', methods=['POST'])
def set_cache_age():
    data = request.get_json(silent=True) or {}
    scenario_name = data.get('scenario')
    ttl_val = data.get('ttl') or data.get('age_minutes')
    
    cache_scenarios = state.DEFAULTS["cache"].get("cache_scenarios", [])
    
    if scenario_name:
        # Try finding scenario by exact or clean match
        clean_name = scenario_name.lower().replace(" ", "").replace("=", "").replace("-", "")
        matched = None
        for s in cache_scenarios:
            s_clean = s["scenario"].lower().replace(" ", "").replace("=", "").replace("-", "")
            if clean_name in s_clean or s_clean in clean_name:
                matched = s
                break
                
        if not matched:
            return jsonify({
                "error": f"Cache scenario '{scenario_name}' not found",
                "valid_scenarios": [s["scenario"] for s in cache_scenarios]
            }), 400
            
        state.active_cache = dict(matched)
        
    elif ttl_val is not None:
        try:
            ttl_int = int(ttl_val)
            weather_state = "Clear Weather"
            if state.active_weather:
                weather_state = state.active_weather["scenario"]
                
            state.active_cache = {
                "scenario": f"Dynamic TTL = {ttl_int}",
                "ttl": ttl_int,
                "weather_state": weather_state,
                "cache_created_time": (datetime.datetime.utcnow() - datetime.timedelta(minutes=ttl_int)).isoformat() + "Z"
            }
        except ValueError:
            return jsonify({"error": "Invalid TTL/age value, must be integer"}), 400
    else:
        return jsonify({"error": "Missing 'scenario' or 'ttl/age_minutes' field"}), 400
        
    return jsonify({
        "status": "success",
        "message": f"Active cache scenario updated to {state.active_cache['scenario']}",
        "current_cache": state.active_cache
    }), 200
