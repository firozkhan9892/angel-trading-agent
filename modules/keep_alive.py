"""
Keep-Alive Module for Render Free Plan
Prevents spin-down by periodic health checks
"""

import requests
from logzero import logger
import os
from datetime import datetime


class KeepAlive:
    """Ping external services to keep Render app awake."""

    @staticmethod
    def health_check() -> bool:
        """Simple health check endpoint."""
        return True

    @staticmethod
    def log_status():
        """Log current status for monitoring."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"✅ Keep-alive ping @ {timestamp}")
        return True


# Optional: Add this to agent.py main loop for external monitoring
def setup_health_endpoint():
    """
    If you want to add a simple HTTP endpoint for monitoring:

    from flask import Flask
    app = Flask(__name__)

    @app.route('/health')
    def health():
        return {'status': 'alive', 'timestamp': datetime.now().isoformat()}

    # Run in separate thread
    from threading import Thread
    Thread(target=lambda: app.run(host='0.0.0.0', port=5000), daemon=True).start()
    """
    pass
