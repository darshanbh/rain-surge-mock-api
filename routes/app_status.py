from flask import Blueprint, jsonify
from routes import state

app_status_bp = Blueprint('app_status', __name__)

@app_status_bp.route('/api/app-status', methods=['GET'])
def get_app_status():
    weather = state.active_weather
    weather_state = weather["scenario"] if weather else "Clear Weather"
    
    show_rain = False
    if state.active_rain_surge > 0.0:
        show_rain = True
    elif weather_state != "Clear Weather" and weather_state != "Clear":
        show_rain = True
        
    if not show_rain:
        return jsonify({
            "show_rain_icon": False,
            "show_raining_carousel": False,
            "weather_state": weather_state
        }), 200
    else:
        return jsonify({
            "show_rain_icon": True,
            "show_raining_carousel": True,
            "weather_state": weather_state
        }), 200
