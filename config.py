import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./esd_measurements.db")
SCOPE_IP = os.getenv("SCOPE_IP", "192.168.0.92")
MOCK_SCOPE = os.getenv("MOCK_SCOPE", "true").lower() == "true"
SCREENSHOT_DIR = os.getenv("SCREENSHOT_DIR", "data/screenshots")
