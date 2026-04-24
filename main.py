"""
test
"""
import cv2
from utiles import mss_to_opencv
from utiles import board_detector
from utiles.split_board import *
from utiles.num_color_recognize import *


def main():
    # Capture the screen
    capture = mss_to_opencv.ScreenCapture()
    capture.capture_screen()

    # Convert the captured screenshot to HSV format 
    img_hsv = capture.to_opencv()

    # Color filtering
    detector = board_detector.BoardDetector(img_hsv)
    detector.mask = detector.locate_board_by_color(img_hsv)

    # Find the board contour
    board_contour = detector.find_board_contour()

    # Visualize the detection
    img_bgr = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)
    result = detector.visualize_detection(img_bgr, board_contour)

    # Extract the board region if the contour is found
    x, y, w, h = board_contour
    board_img = img_bgr[y:y+h, x:x+w]

    # Save the result
    if board_contour is not None:
        cv2.imwrite("board_detection_result.png", result)
        print(f"Board location: {board_contour}")
    else:
        print("Board not detected.")

    if board_img is not None and w > 0 and h > 0:
        board_img = img_bgr[y:y+h, x:x+w]
        cv2.imshow("Extracted Board", board_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.imwrite("extracted_board.png", board_img)
        print("Extracted board image saved as 'extracted_board.png'.")
    else:
        print("No board image to save.")

    # Split the board into cells
    splitter = SplitBoard(board_img)
    tiles = splitter.split_into_cells()
    splitter.visualize_tiles(tiles)

    # Convert the tiles to a matrix of numbers
    matrix = NumColorRecognizer().board_to_matrix(tiles)
    # Print the resulting matrix
    print("Recognized board matrix:")
    print(matrix)


if __name__ == "__main__":
    main()