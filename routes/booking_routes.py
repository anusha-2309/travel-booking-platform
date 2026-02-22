from flask import Blueprint, request, jsonify
from config import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId

booking_bp = Blueprint('bookings', __name__)

# -------------------------
# BOOK A PACKAGE (Protected)
# -------------------------
@booking_bp.route('/book', methods=['POST'])
@jwt_required()
def book_package():
    data = request.json
    current_user = get_jwt_identity()

    # Validate request body
    if not data or "package_id" not in data:
        return jsonify({"error": "package_id is required"}), 400

    try:
        package = db.packages.find_one(
            {"_id": ObjectId(data["package_id"])}
        )
    except:
        return jsonify({"error": "Invalid package ID format"}), 400

    if not package:
        return jsonify({"error": "Package not found"}), 404

    # Save booking reference
    db.bookings.insert_one({
        "user_email": current_user,
        "package_id": data["package_id"]
    })

    return jsonify({"message": "Package booked successfully"}), 201


# -------------------------
# VIEW MY BOOKINGS (Protected)
# -------------------------
@booking_bp.route('/my-bookings', methods=['GET'])
@jwt_required()
def my_bookings():
    current_user = get_jwt_identity()

    user_bookings = db.bookings.find({"user_email": current_user})

    result = []

    for booking in user_bookings:

        # Skip old or corrupted records safely
        package_id = booking.get("package_id")
        if not package_id:
            continue

        try:
            package = db.packages.find_one(
                {"_id": ObjectId(package_id)},
                {"_id": 0}
            )
        except:
            continue

        if package:
            result.append(package)

    return jsonify(result), 200