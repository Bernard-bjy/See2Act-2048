"""
This module provides functionality for converting mss screenshots to OpenCV format.
"""
import cv2
import numpy as np
import mss

class ScreenCapture:
    def __init__(self):
        self.screenshot = None
    
    def capture_screen(self):
        """Capture the screen and save it as an image file."""
        with mss.mss() as sct:
            monitor = sct.monitors[2]  # Capture the second monitor
            self.screenshot = sct.grab(monitor)
            print(f"Screenshot captured: {self.screenshot}")

        return self.screenshot
    
    def to_opencv(self):
        """Convert the captured screenshot to an OpenCV format (HSV)."""
        if self.screenshot is not None:
            # Convert mss screenshot to OpenCV format
            img_bgr = np.array(self.screenshot)[:, :, :3]  # Convert BGRA to BGR format
            img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
            return img_hsv
        else:
            print("No screenshot captured yet.")
            return None

if __name__ == "__main__":
    screen_capture = ScreenCapture()
    screen_capture.capture_screen()
    img_hsv = screen_capture.to_opencv()