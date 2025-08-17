"""
Inventory package initialization.

This file makes the `inventory` folder a Python package. It exposes the
Flask application instance (`app`) and the `init_database` function for
use by external tools
"""

from .app import app, init_database

__all__ = ["app", "init_database"]
