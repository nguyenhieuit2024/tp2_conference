from flask import jsonify

def error_response(message, code=400):
    return jsonify({"error": message}), code

def success_response(data=None, message="Success"):
    resp = {"message": message}
    if data:
        resp["data"] = data
    return jsonify(resp), 200
