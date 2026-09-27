from flask import jsonify

def register_error_handlers(app,jwt):
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "message": "Resource not found"
        }),404
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "message": "Method not allowed"
        }),405

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "message": "Internal server error"
        }),500    

# -------------------------
    # JWT Error Handlers
    # -------------------------

    @jwt.invalid_token_loader
    def invalid_token_callback(error):

        return jsonify({
            "success": False,
            "message": "Invalid token"
        }), 401

    @jwt.expired_token_loader
    def expired_token_callback(
        jwt_header,
        jwt_payload
    ):

        return jsonify({
            "success": False,
            "message": "Token has expired"
        }), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):

        return jsonify({
            "success": False,
            "message": "Authorization token is required"
        }), 401

    @jwt.revoked_token_loader
    def revoked_token_callback(
        jwt_header,
        jwt_payload
    ):

        return jsonify({
            "success": False,
            "message": "Token has been revoked"
        }), 401

    @jwt.needs_fresh_token_loader
    def fresh_token_required_callback(
        jwt_header,
        jwt_payload
    ):

        return jsonify({
            "success": False,
            "message": "Fresh token required"
        }), 401