from flask import Blueprint, jsonify, request
from routes import state

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json(silent=True) or {}
    order_id = data.get('order_id')
    if not order_id:
        return jsonify({"error": "Missing required field: order_id"}), 400
        
    weather = state.active_weather
    weather_state = weather["scenario"] if weather else "Clear Weather"
    
    status = data.get('status') or data.get('order_status') or "Created"
    status = status.capitalize()
    
    rain_surge = data.get('rain_surge')
    if rain_surge is None:
        if state.active_rain_surge is not None:
            rain_surge = state.active_rain_surge
        elif weather_state == "Clear Weather":
            rain_surge = 0.0
        else:
            rain_surge = 30.0
            
    order = {
        "order_id": order_id,
        "weather_state": weather_state,
        "rain_surge": rain_surge,
        "order_status": status,
        "earnings_locked": True
    }
    
    state.active_orders[order_id] = order
    return jsonify({
        "status": "success",
        "message": f"Order {order_id} created successfully",
        "order": order
    }), 201

@orders_bp.route('/api/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    order = state.active_orders.get(order_id)
    
    if not order:
        default_orders = state.DEFAULTS["orders"].get("orders", [])
        matched = next((o for o in default_orders if o["order_id"] == order_id), None)
        if matched:
            order = dict(matched)
            state.active_orders[order_id] = order
            
    if not order:
        return jsonify({"error": f"Order {order_id} not found"}), 404
        
    return jsonify(order), 200

@orders_bp.route('/api/orders/<order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    data = request.get_json(silent=True) or {}
    new_status = data.get('status') or data.get('order_status')
    if not new_status:
        return jsonify({"error": "Missing required field: status"}), 400
        
    new_status = new_status.capitalize()
    valid_statuses = ["Created", "Accepted", "Completed"]
    if new_status not in valid_statuses:
        return jsonify({"error": f"Invalid status. Must be one of: {valid_statuses}"}), 400
        
    order = state.active_orders.get(order_id)
    if not order:
        default_orders = state.DEFAULTS["orders"].get("orders", [])
        matched = next((o for o in default_orders if o["order_id"] == order_id), None)
        if matched:
            order = dict(matched)
            state.active_orders[order_id] = order
            
    if not order:
        return jsonify({"error": f"Order {order_id} not found"}), 404
        
    old_status = order.get("order_status")
    order["order_status"] = new_status
    
    logs = []
    if new_status == "Completed":
        active_rule = state.active_business_rule_scenario
        if active_rule and active_rule.get("test_case") == "TS_RS_E2E_013":
            order["earnings_locked"] = True
            logs.append(f"TS_RS_E2E_013 Rule Active: Earnings locked at quotation rain surge of {order.get('rain_surge')}")
        else:
            order["earnings_locked"] = True
            logs.append(f"Earnings locked at quotation rain surge of {order.get('rain_surge')}")
            
    return jsonify({
        "status": "success",
        "message": f"Order {order_id} status updated from {old_status} to {new_status}",
        "order": order,
        "logs": logs
    }), 200
