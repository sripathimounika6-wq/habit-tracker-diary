try:
    import werkzeug
    if not hasattr(werkzeug, "__version__"):
        # provide a reasonable default version string
        werkzeug.__version__ = "2.3.0"
except Exception:
    # if werkzeug import fails for any reason, ignore and let Flask raise later
    pass


from flask import Flask
from .routes import bp
import logging
import os


def create_app():
    logging.basicConfig(level=logging.INFO)
    app = Flask(__name__, static_folder="../frontend", static_url_path="/")
    app.register_blueprint(bp, url_prefix="/api")

    @app.route("/")
    def index():
        return app.send_static_file("index.html")

    @app.route("/api/health")
    def health():
        return {"status": "ok"}, 200

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
