"""Application entry point for the habit tracker API."""
import logging
import os

try:
    import werkzeug

    if not hasattr(werkzeug, "__version__"):
        # provide a reasonable default version string
        werkzeug.__version__ = "2.3.0"
except Exception as exc:
    # Log the problem but let Flask handle any real failure later
    logging.getLogger(__name__).warning(
        "Failed to set werkzeug.__version__: %s", exc,
    )

from flask import Flask
from .routes import bp


def create_app():
    """Create and configure the Flask application."""
    logging.basicConfig(level=logging.INFO)
    app = Flask(
        __name__,
        static_folder="../frontend",
        static_url_path="/",
    )
    # CSRF not required: our API uses no cookies or forms, only stateless JSON requests

    app.register_blueprint(bp, url_prefix="/api")

    @app.route("/")
    def index():
        return app.send_static_file("index.html")

    @app.route("/api/health")
    def health():
        return {"status": "ok"}, 200

    return app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # Binding to all interfaces is intentional for container/EC2 deployments.
    create_app().run(
        host="0.0.0.0",  # nosec B104
        port=port,
    )
