from flask import Blueprint, jsonify
from models import db, ActivityLog

logs_bp = Blueprint('logs', __name__)

# Lấy danh sách nhật ký hoạt động
@logs_bp.route('/logs', methods=['GET'])
def get_activity_logs():
    logs = ActivityLog.query.all()
    logs_list = [{
        "log_id": log.log_id,
        "employee_id": log.employee_id,
        "product_id": log.product_id,
        "action": log.action,
        "log_timestamp": log.log_timestamp.strftime('%Y-%m-%d %H:%M:%S')
    } for log in logs]
    return jsonify({"logs": logs_list}), 200
