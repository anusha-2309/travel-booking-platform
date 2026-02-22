from flask import Blueprint, request, jsonify
from config import db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

user_bp = Blueprint('users', __name__)
bcrypt = Bcrypt()

# -------------------------
# REGISTER ROUTE
# -------------------------
@user_bp.route('/register', methods=['POST'])
def register():
    data = request.json

    # Check if user already exists
    existing_user = db.users.find_one({"email": data["email"]})
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    # Hash password
    hashed_pw = bcrypt.generate_password_hash(data["password"]).decode('utf-8')

    # Insert into MongoDB
    db.users.insert_one({
        "name": data["name"],
        "email": data["email"],
        "password": hashed_pw
    })

    return jsonify({"message": "User registered successfully"}), 201


# -------------------------
# LOGIN ROUTE (UPDATED WITH JWT)
# -------------------------
@user_bp.route('/login', methods=['POST'])
def login():
    data = request.json

    user = db.users.find_one({"email": data["email"]})

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Check hashed password
    if bcrypt.check_password_hash(user["password"], data["password"]):
        
        # 🔥 Generate JWT token
        access_token = create_access_token(identity=user["email"])

        return jsonify({
            "message": "Login successful",
            "access_token": access_token
        }), 200
    else:
        return jsonify({"error": "Invalid password"}), 401


# -------------------------
# PROTECTED PROFILE ROUTE
# -------------------------
@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()

    return jsonify({
        "message": "Profile accessed successfully",
        "user": current_user
    }), 200