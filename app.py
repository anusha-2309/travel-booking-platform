from flask import Flask
from routes.user_routes import user_bp, bcrypt
from routes.package_routes import package_bp
from routes.booking_routes import booking_bp
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta

app = Flask(__name__)

# -----------------------------
# Enable CORS (VERY IMPORTANT for frontend)
# -----------------------------
CORS(app)

# -----------------------------
# JWT Configuration
# -----------------------------
app.config["JWT_SECRET_KEY"] = "super-secret-key-change-this"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)

bcrypt.init_app(app)
jwt = JWTManager(app)

# -----------------------------
# Register Blueprints
# -----------------------------
app.register_blueprint(user_bp)
app.register_blueprint(package_bp)
app.register_blueprint(booking_bp)

# -----------------------------
# Home Route
# -----------------------------
@app.route('/')
def home():
    return "Travel Backend Running 🚀"

# -----------------------------
# Run App
# -----------------------------
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)