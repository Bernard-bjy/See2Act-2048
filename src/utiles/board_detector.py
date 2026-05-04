"""
This module provides functionality for detecting the 2048 game board in screenshots.
"""
import cv2
import numpy as np
from utiles import mss_to_opencv

class BoardDetector:
    def __init__(self,hsv):
        self.hsv = hsv
        self.board_contour = None
        self.mask = None
    
    def locate_board_by_color(self, img_hsv):
        """
        Locate the game board in the screenshot using color detection.
        """
        # Define the lower and upper bounds for the board color in HSV
        lower_bound = np.array([10, 40, 130])
        upper_bound = np.array([25, 80, 190])

        # Create a mask for the board color
        mask = cv2.inRange(img_hsv, lower_bound, upper_bound)
        self.mask = mask

        return self.mask
    
    def find_board_contour(self, mask = None):
        if mask is None:
            mask = self.mask
        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            print("No contours found for the board color.")
            return None
        
        # Find the largest contour which is likely to be the game board
        largest_contour = max(contours, key=cv2.contourArea)

        # Get the bounding rectangle of the largest contour
        x, y, w, h = cv2.boundingRect(largest_contour)

        aspect_ratio = w / float(h)
        print(f"Largest contour:{w}x{h}, aspect ratio: {aspect_ratio:.3f}")
        if 0.7 < aspect_ratio < 1.6:  # Check if the aspect ratio is close to 1 (square)
            self.board_contour = largest_contour
            return (x, y, w, h)
        else:
            print("The detected contour does not have a square aspect ratio.")
            self.board_contour = None

        return None
    
    def visualize_detection(self, img_bgr, board_contour):
        """
        Visualize the detected board contour on the original image.
        """
        if board_contour is None:
            print("No board contour to visualize.")
            return img_bgr
        x, y, w, h = board_contour
        # Draw a rectangle around the detected board and contour
        result = img_bgr.copy()
        cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 3)
        #
        cv2.putText(result, '2048 Board Detected', (x, y - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
        # Display the result
        cv2.imshow("Board Detection", result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        return result
    
if __name__ == "__main__":
    # Example usage
    capture = mss_to_opencv.ScreenCapture()
    capture.capture_screen()
    img_hsv = capture.to_opencv()

    board_detector = BoardDetector(img_hsv)
    board_contour = board_detector.locate_board_by_color(img_hsv)

    if board_contour is not None:
        img_bgr = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)
        board_detector.visualize_detection(img_bgr, board_contour)