import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Register Blueprints
from routes.weather import weather_bp
from routes.cache import cache_bp
from routes.scheduler import scheduler_bp
from routes.quotation import quotation_bp
from routes.orders import orders_bp
from routes.earnings import earnings_bp
from routes.reports import reports_bp
from routes.app_status import app_status_bp
from routes.business_rules import business_rules_bp

app.register_blueprint(weather_bp)
app.register_blueprint(cache_bp)
app.register_blueprint(scheduler_bp)
app.register_blueprint(quotation_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(earnings_bp)
app.register_blueprint(reports_bp)
app.register_blueprint(app_status_bp)
app.register_blueprint(business_rules_bp)

# Global Failure Simulation Hook
@app.before_request
def handle_failure_simulation():
    fail_param = request.args.get('fail')
    if fail_param:
        if fail_param == 'timeout':
            return jsonify({"error": "Request timeout simulated", "code": "TIMEOUT"}), 408
        elif fail_param == 'http500':
            return jsonify({"error": "Internal server error simulated", "code": "INTERNAL_SERVER_ERROR"}), 500
        elif fail_param == 'http429':
            return jsonify({"error": "Too many requests simulated", "code": "TOO_MANY_REQUESTS"}), 429
        elif fail_param == 'malformed':
            return "malformed json string: {invalid:}", 400, {'Content-Type': 'application/json'}
        elif fail_param == 'null':
            return jsonify({"current": None}), 500
        elif fail_param == 'invalidApiKey':
            return jsonify({"error": "Invalid API key simulated", "code": "UNAUTHORIZED"}), 401
        elif fail_param == 'missingApiKey':
            return jsonify({"error": "Missing API key simulated", "code": "FORBIDDEN"}), 403

# Global Scenario Reset Endpoint
@app.route('/api/scenario/reset', methods=['POST'])
def reset_scenario():
    from routes import state
    state.reset_state()
    return jsonify({
        "status": "success",
        "message": "All active mock states reset to default",
        "active_weather": state.active_weather["scenario"] if state.active_weather else None,
        "active_cache": state.active_cache["scenario"] if state.active_cache else None,
        "active_zones_count": len(state.active_zones),
        "active_business_rule_scenario": state.active_business_rule_scenario
    }), 200

# Root welcome check endpoint
@app.route('/')
def home():
    return jsonify({
        "service": "Rain Surge Mock API Service",
        "version": "1.0",
        "status": "online"
    })

if __name__ == '__main__':
    # Start flask server
    app.run(host='0.0.0.0', port=5000, debug=True)
