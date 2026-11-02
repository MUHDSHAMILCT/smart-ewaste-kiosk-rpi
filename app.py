"""
E-Waste Kiosk — Flask Application Factory
"""

import os
import sys
import logging
from pathlib import Path
from flask import Flask, render_template, send_from_directory

# Automatically load environment variables from .env if present
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent / ".env")
except ImportError:
    pass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s"
)

BASE_DIR = Path(__file__).resolve().parent


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder=str(BASE_DIR / "frontend" / "templates"),
        static_folder=str(BASE_DIR / "frontend" / "static"),
        static_url_path="/static"
    )

    # ─── Configuration ────────────────────────────────────────────────────────
    app.secret_key = os.environ.get("SECRET_KEY", "kiosk-ewaste-secret-2024")
    app.config["MAX_CONTENT_LENGTH"] = 32 * 1024 * 1024  # 32MB upload limit
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

    # ─── Database Init ────────────────────────────────────────────────────────
    from backend.database.models import init_db
    init_db()

    # ─── Register Blueprints ──────────────────────────────────────────────────
    from backend.routes.auth    import auth_bp
    from backend.routes.devices import devices_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(devices_bp)

    # ─── Storage file serving ─────────────────────────────────────────────────
    storage_dir = BASE_DIR / "storage"

    @app.route("/storage/<path:filename>")
    def serve_storage(filename):
        return send_from_directory(str(storage_dir), filename)

    # ─── SPA catch-all: serve index.html for all non-API routes ───────────────
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_index(path):
        return render_template("index.html")

    return app


if __name__ == "__main__":
    import sys

    port     = int(os.environ.get("PORT", 5000))
    host     = os.environ.get("HOST", "0.0.0.0")
    debug    = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    mock_hw  = os.environ.get("MOCK_HARDWARE", "true").lower() != "false"

    print(f"""
=======================================================
  ENCYCLE BANK SYSTEM - Starting Up
=======================================================
  URL  : http://{host}:{port}
  Mode : {'MOCK (Development)' if mock_hw else 'HARDWARE (Raspberry Pi)'}
  Debug: {debug}
=======================================================
""")

    app = create_app()
    app.run(host=host, port=port, debug=debug, threaded=True)
