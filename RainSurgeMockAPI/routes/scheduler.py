from flask import Blueprint, jsonify
from routes import state
import datetime

scheduler_bp = Blueprint('scheduler', __name__)

@scheduler_bp.route('/api/scheduler/tick', methods=['POST'])
def trigger_tick():
    logs = []
    if state.active_cache:
        old_ttl = state.active_cache.get("ttl", 0)
        new_ttl = old_ttl + 1
        state.active_cache["ttl"] = new_ttl
        state.active_cache["cache_created_time"] = (
            datetime.datetime.utcnow() - datetime.timedelta(minutes=new_ttl)
        ).isoformat() + "Z"
        logs.append(f"Incremented cache age from {old_ttl} to {new_ttl} minutes")
        
        if new_ttl > 30:
            logs.append("Cache has expired (age > 30 min)")
            
    return jsonify({
        "status": "success",
        "message": "Scheduler execution tick simulated successfully",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "logs": logs,
        "current_cache_ttl": state.active_cache.get("ttl") if state.active_cache else None
    }), 200
