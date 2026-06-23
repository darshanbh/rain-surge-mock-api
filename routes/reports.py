from flask import Blueprint, jsonify, request
from routes import state

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/api/reports', methods=['GET'])
def get_reports():
    reports_data = state.DEFAULTS["reports"].get("reports", [])
    scenario_param = request.args.get('scenario')
    
    processed_reports = []
    for r in reports_data:
        copied = dict(r)
        if state.active_rain_surge > 0.0:
            copied["rain_surge"] = state.active_rain_surge
            copied["quotation_total"] = 100.0 + state.active_rain_surge
            copied["earnings_total"] = 80.0 + (state.active_rain_surge * 0.5)
        processed_reports.append(copied)
        
    if scenario_param:
        matched = next((r for r in processed_reports if scenario_param.lower() in r["scenario"].lower()), None)
        if matched:
            return jsonify(matched), 200
        return jsonify({"error": f"Reporting scenario '{scenario_param}' not found"}), 404
        
    return jsonify({
        "reporting_scenarios": processed_reports,
        "used_by": state.DEFAULTS["reports"].get("used_by", [])
    }), 200
