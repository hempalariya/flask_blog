from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.extensions import db
from app.models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

#Register: POST /api/auth/register
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or not data.get("username") or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Missing required fields: username, email, password"}), 400

    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already exists"}), 409

    if User.query.filter_by(email=data["email"].first()):
        return jsonify({"erro": "Email already registered"}), 409

    new_user = User(
        username=data["username"],
        email=data["email"]
    )

    new_user.set_password(data["password"])

    try:
        db.session.add(new_user),
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to create user", "details": str(e)}), 500

    return jsonify({
        "message": "User registered successfully",
        "user": new_user.to_dict()
    }), 201



#LOGIN: POST /api/auth/login
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error"}: "Email and password are required"), 400
    user = User.query.filter_by(email=data["email"]).first()

    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid email or password"}), 401

    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "message": "Login successful", 
        "access_token": access_token,
        "user": user.to_dict()
    }), 200