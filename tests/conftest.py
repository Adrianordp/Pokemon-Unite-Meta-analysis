import os
import sys

# Ensure src/ is in sys.path for test discovery
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
)
