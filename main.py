"""
test
"""
import cv2
import mss
from utiles import mss_to_opencv
from utiles import board_detector
from utiles.split_board import *
from utiles.num_color_recognize import *
from utiles.greedy_algorithm import *
from utiles.controller import *


def sceenshot_confirm():
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
    # splitter.visualize_tiles(tiles)

    # Convert the tiles to a matrix of numbers
    matrix = NumColorRecognizer().board_to_matrix(tiles)
    # Print the resulting matrix
    print("Recognized board matrix:")
    print(matrix)

def main():
    capture = mss_to_opencv.ScreenCapture()
    # detector = board_detector.BoardDetector()
    recognizer = NumColorRecognizer()
    solver = GreedyAlgorithm()
    controller = GameControl()

    # parameter
    Max_games = 1 # change as needed, ready for getting data to the data analyst
    Max_per_game_count = 10000
    game_count = 0 # finished game
    move_count = 0
    

    print(f"Starting in 3 seconds, max games: {Max_games}")
    time.sleep(3)


    try:
        # muti game
        while game_count < Max_games:
            game_count += 1
            move_count = 0
            print(f"======Game: {game_count}/{Max_games} ======")

            # singal game
            while move_count < Max_per_game_count:
                # capture the screen
                capture.capture_screen()
                img_hsv = capture.to_opencv()

                # detect the board
                detector = board_detector.BoardDetector(img_hsv)
                detector.mask = detector.locate_board_by_color(img_hsv)
                board_contour = detector.find_board_contour()
                
                # game over
                if board_contour is None:
                    print("Board lost - Game Over!")

                    time.sleep(0.5)

                    if game_count < Max_games:
                        if controller.click_reset():
                            print("Game restarted")
                        else:
                            print("Failed to find reset button")

                    # with mss.mss() as sct:
                    #     # print("all monitors: ", sct.monitors)
                    #     monitor = sct.monitors[2]
                    #     # print("selected monitor: ", monitor)

                    # region = (
                    #     monitor['left'],
                    #     max(0, monitor['top']),
                    #     monitor['width'],
                    #     monitor['height']
                    # )

                    # reset_btn = pyautogui.locateOnScreen('/Users/bijunyao/Desktop/AI Develop/2048决策智能体/2048项目包/Try again.png', confidence=0.5,region=region)
                    # # pyautogui.screenshot('/Users/bijunyao/Desktop/AI Develop/2048决策智能体/debug_gameover.png')
                    # # print(f"Debug screenshot saved: {r'/Users/bijunyao/Desktop/AI Develop/2048决策智能体/debug_gameover.png'}")
                    # print(f"Found: {reset_btn}")

                    # if reset_btn is not None:
                    #     pyautogui.click(reset_btn)
                    #     print('Clicked reset button')
                    # else:
                    #     print("Reset button not found")
                    
                        time.sleep(2)
                    else:
                        print("Max games reached")
                
                    break

                x, y, w, h = board_contour

                # extract board
                img_bgr = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)
                board_img = img_bgr[y:y+h, x:x+w]

                # split
                splitter = SplitBoard(board_img)
                tiles = splitter.split_into_cells()

                # convert to matrix
                board_matrix = recognizer.board_to_matrix(tiles)
                print(board_matrix)

                # decision
                best_direction = solver.get_best_move(board_matrix)

                # if best_direction is None:
                #     print("no available move!")
                #     break

                print(f"best moves:{best_direction}")

                # press the key
                controller.execute(best_direction)
                
                move_count += 1

                # wait for animation
                time.sleep(0.3)
            
            print(f"Game: {game_count} finished, moves: {move_count}")

    except KeyboardInterrupt:
        print(f"Stopped by user. Total games: {game_count}")
    except Exception as e:
        print(f"error:{e}")

    else:
        print(f"Total games played: {game_count}")

if __name__ == "__main__":
    main()