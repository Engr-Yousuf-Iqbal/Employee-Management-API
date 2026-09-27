from flask import jsonify


def success_response(
    message,
    data=None,
    status_code=200
):

    return jsonify({
        "success": True,
        "message": message,
        "data": data
    }), status_code


def error_response(
    message,
    status_code=400,
    errors=None
):

    response = {
        "success": False,
        "message": message
    }

    if errors:
        response["errors"] = errors

    return jsonify(response), status_code