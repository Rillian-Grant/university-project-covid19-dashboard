"""Copy of code in covid19_dashboard/__init__.py but with imports that work when not installed"""

from covid19_dashboard import app
from covid19_dashboard.config import config

if __name__ == "__main__":
    app.run(
        debug=config["flask_debug"],
        host=config["host"],
        port=config["port"]
    )
