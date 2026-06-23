from flask import Blueprint, jsonify, request
from routes import state

earnings_bp = Blueprint('earnings', __name__)

@earnings_bp.route('/api/earnings', methods=['GET'])
def get_earnings():
    earnings_data = state.DEFAULTS["earnings"].get("earnings", [])
    scenario_param = request.args.get('scenario')
    
    processed_scenarios = []
    for e in earnings_data:
        copied = dict(e)
        if state.active_rain_surge > 0.0:
            copied["rain_surge_earnings"] = state.active_rain_surge
            copied["total_earnings"] = copied.get("base_earnings", 80.0) + state.active_rain_surge
        processed_scenarios.append(copied)
        
    if scenario_param:
        matched = next((e for e in processed_scenarios if scenario_param.lower() in e["scenario"].lower()), None)
        if matched:
            return jsonify(matched), 200
        return jsonify({"error": f"Earnings scenario '{scenario_param}' not found"}), 404
        
    return jsonify({
        "earnings_scenarios": processed_scenarios,
        "used_by": state.DEFAULTS["earnings"].get("used_by", [])
    }), 200
