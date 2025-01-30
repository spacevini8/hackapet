# Mock the 'board' module if not using hardware
try:
    import board
except ImportError:
    print("No hardware platform detected. Using mock board.")

import displayio
import adafruit_d