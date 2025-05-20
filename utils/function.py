from flask import jsonify, Response
from datetime import datetime


def send_response(status: int = 200, messages: str = "", data="null") -> tuple[Response, int]:
    response = {
        "success": "true",
        "length": len(data) if data is not None else 0,
        "status": status,
        "messages": messages,
        "data": data
    }
    print(response)
    return jsonify(response), status

def send_error(status: int = 400, message: str = "") -> tuple[Response, int]:
    response = {
        "success": "false",
        "length": 0,
        "status": status,
        "message": message,
        "data": "null"
    }
    return jsonify(response), status

def check_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False