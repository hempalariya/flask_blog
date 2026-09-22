from flask import Blueprint, jsonify

#Blueprint(name, import_name, url_prefix)
#'main is the internal name of this blueprint
#url_prefix ensures all routes in this blueprint automatically start with /

main_bp = Blueprint("main", __name__, url_prefix="/api")

@main_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "success",
        "message": "Modular Flask API is up and running"
    }), 200