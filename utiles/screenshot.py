"""
This module provides functionality for taking screenshots of the current screen. It uses the `PIL` library to capture the screen and save the screenshot as an image file
"""
from PIL import ImageGrab
from PIL import Image
import datetime
import cv2
import numpy as np
import mss
from io import BytesIO
import os

class ScreenCapture:
    def __init__(self):
        self.screenshot = None
    
    def capture_screen_second(self):
        """Capture the screen and save it as an image file."""
        with mss.mss() as sct:
            monitor = sct.monitors[2]  # Capture the second monitor
            self.screenshot = sct.grab(monitor)
            # self.full_screenshot = sct.grab(sct.monitors[0])  # Capture the entire screen (all monitors)

        return self.screenshot

    def capture_screen_primary(self, ltrp=None):
        """Capture the screen and save it as an image file. Optionally, specify a region to capture using the ltrp parameter (left, top, right, bottom)."""
        if ltrp is None:
            self.screenshot = ImageGrab.grab()
        else:
            self.screenshot = ImageGrab.grab(bbox=ltrp)

        # Generate a timestamp for the filename
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.filename = f'screenshot_{self.timestamp}.png'

        return self.screenshot
    
    def to_opencv(self):
        """Convert the captured screenshot to an OpenCV format (BGR)."""
        if self.screenshot is not None:
            # Convert PIL Image to OpenCV format
            img_cv = cv2.cvtColor(np.array(self.screenshot), cv2.COLOR_BGR2HSV)
            
            # Add timestamp to the image if it exists
            if self.timestamp:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # Add timestamp to the image
                cv2.putText(img_cv, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            return img_cv
       
        else:
            print("No screenshot captured yet.")
            return None
    
    def save_screenshot(self, folder_path = '.'):
        """Save the captured screenshot to the specified path."""
        if self.screenshot is not None:
            full_path = f"{folder_path}/{self.filename}"
            self.screenshot.save(full_path)
            print(f"Screenshot saved to {full_path}")
        else:
            print("No screenshot captured yet.")


if __name__ == "__main__":
    screen_capture = ScreenCapture()
    # screen_capture.capture_screen_primary()
    screen_capture.capture_screen_second()
    img_cv = screen_capture.to_opencv()
    # cv2.imshow('Screenshot', img_cv)
    # screen_capture.save_screenshot('/Users/bijunyao/Desktop/AI Develop/2048决策智能体')
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    