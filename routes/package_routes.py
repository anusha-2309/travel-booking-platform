from flask import Blueprint, request, jsonify
from config import db, redis_client
from flask_jwt_extended import jwt_required
from bson import ObjectId
import json

package_bp = Blueprint('packages', __name__)

# -------------------------
# ADD TRAVEL PACKAGE (Protected)
# -------------------------
@package_bp.route('/add-package', methods=['POST'])
@jwt_required()
def add_package():
    data = request.json

    db.packages.insert_one({
        "title": data["title"],
        "destination": data["destination"],
        "price": data["price"],
        "duration": data["duration"]
    })

    # Clear cache when new package is added
    redis_client.delete("all_packages")

    return jsonify({"message": "Travel package added successfully"}), 201


# -------------------------
# VIEW ALL PACKAGES (Public + Cached)
# -------------------------
@package_bp.route('/packages', methods=['GET'])
def get_packages():
    print("ROUTE HIT")

    # 1️⃣ Check Redis cache first
    cached_packages = redis_client.get("all_packages")

    if cached_packages:
        print("Serving from Redis 🚀")
        return jsonify(json.loads(cached_packages)), 200

    # 2️⃣ If not cached → Fetch from MongoDB
    print("Serving from MongoDB 🗄️")

    packages = []

    for pkg in db.packages.find():
        packages.append({
            "id": str(pkg["_id"]),
            "title": pkg["title"],
            "destination": pkg["destination"],
            "price": pkg["price"],
            "duration": pkg["duration"]
        })

    # 3️⃣ Store in Redis for 60 seconds
    redis_client.setex("all_packages", 60, json.dumps(packages))

    return jsonify(packages), 200