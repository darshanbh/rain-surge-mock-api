from flask import Blueprint, jsonify, request
from routes import state

business_rules_bp = Blueprint('business_rules', __name__)

@business_rules_bp.route('/api/business-rules', methods=['GET'])
def get_business_rules():
    rules_data = state.DEFAULTS["business_rules"].get("business_rules", [])
    return jsonify({
        "business_rules": rules_data,
        "active_scenario": state.active_business_rule_scenario
    }), 200

@business_rules_bp.route('/api/business-rules/scenario', methods=['POST'])
def set_business_rule_scenario():
    data = request.get_json(silent=True) or {}
    scenario_id = data.get('scenario_id') or data.get('test_case')
    
    if not scenario_id:
        return jsonify({"error": "Missing 'scenario_id' or 'test_case' parameter"}), 400
        
    rules_data = state.DEFAULTS["business_rules"].get("business_rules", [])
    
    matched = None
    for rule in rules_data:
        if (rule.get("scenario_id").lower() == scenario_id.lower() or 
            rule.get("test_case").lower() == scenario_id.lower()):
            matched = rule
            break
            
    if not matched:
        return jsonify({
            "error": f"Business rule scenario '{scenario_id}' not found",
            "available_scenarios": [r["scenario_id"] for r in rules_data]
        }), 400
        
    state.active_business_rule_scenario = matched
    return jsonify({
        "status": "success",
        "message": f"Active business rule scenario updated to {matched['scenario_id']} ({matched['test_case']})",
        "active_scenario": state.active_business_rule_scenario
    }), 200
