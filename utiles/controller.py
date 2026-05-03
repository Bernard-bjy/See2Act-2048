"""
game control
"""
import pyautogui
import time
import mss
from pynput import keyboard
from utiles.num_color_recognize import *
from utiles.greedy_algorithm import *
from utiles.split_board import SplitBoard


class GameControl:
    def __init__(self):
        self.recognizer = NumColorRecognizer()
        self.solver = GreedyAlgorithm()
        self.key_map = {
            'up': 'w',
            'down': 's',
            'left': 'a',
            'right': 'd'
        }

        self.sub_monitor = {
            'left': 266,
            'top': -1080,
            'width': 1920,
            'height': 1080
        }

        # path of btn
        self.reset_btn_path = '/Users/bijunyao/Desktop/AI Develop/2048决策智能体/2048项目包/Try again.png'

        # pyautogui.FAILSAFE = True
        self.running = True
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def on_press(self, key):
        try:
            if hasattr(key, 'char') and key.char.lower() == 'q':
                self.running = False
                print("Q pressed, stopping......")
        except:
            pass



    def execute(self, direction):
        key = self.key_map[direction]
        pyautogui.press(key)
        print(f"Excuted: {direction}, {key}")

    def play_move(self, screenshot):
        tiles = SplitBoard.split_into_cells(screenshot)
        board = self.recognizer.board_to_matrix(tiles)

        best_direction = self.solver.get_best_move(board)

        # press the key
        self.execute(best_direction)

        return best_direction, board
    
    def auto_play(self, screenshot_func, interval=0.5, max_moves=1000):
        print("starting auto_play in 3 seconds")
        time.sleep(3)

        for i in range(max_moves):
            # if not self.running:
            #     break

            try:
                if not self.running:
                    break

                screenshot = screenshot_func()

                self.best_direction, board = self.play_move(screenshot)

                if self.solver.count_empty_cells(board) == 0:
                    can_move = any(
                        self.solver.simulate_move(board, d)[1]
                        for d in self.solver.best_direction
                    )
                    if not can_move:
                        print("game over")
                        break
                # game animation interval
                time.sleep(0.8)  # change to achieve the goal
            
            except Exception as e:
                print("Error, Break")
                break
        
        self.listener.stop()

        print(f"played{i+1}moves")
    
    def find_button_on_sub_screen(self):
        template = cv2.imread(self.reset_btn_path)
        if template is None:
            print(f"Failed to load template")
            return None
        # print(f"Template loaded")
        
        # mss capture the sub_monitor
        with mss.mss() as sct:
            screenshot = sct.grab(self.sub_monitor)
            img = np.frombuffer(screenshot.rgb, dtype=np.uint8)
            img = img.reshape(screenshot.height, screenshot.width, 3)
            # print(f"Reshaped: {img.shape}")

            img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            # print("Converted RGB to BGR")
        
        # save debug_screenshot
        debug_path = '/Users/bijunyao/Desktop/AI Develop/2048决策智能体/debug_sub_screen.png'
        cv2.imwrite(debug_path, img_bgr)
        # print("Debug screenshot saved")


        # template matching
        result = cv2.matchTemplate(img_bgr, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # print(f"Match confidence:{max_val: .3f}")

        if max_val < 0.5:
            print("Button not found")
            return None
        
        # btn center(Physical pixels)
        h, w = template.shape[:2]
        btn_x_sub = max_loc[0] + w // 2
        btn_y_sub = max_loc[1] + h // 2

        # convert to global coordinates
        btn_x_global = btn_x_sub + self.sub_monitor['left']
        btn_y_global = btn_y_sub + self.sub_monitor['top']

        # print(f"Button at global: {btn_x_global}, {btn_y_global}")

        return(btn_x_global, btn_y_global)

    def click_reset(self):
        pos = self.find_button_on_sub_screen()
        if pos:
            pyautogui.click(pos)
            print("Clicked reset button")
            return True
        print("No button position returned")
        return False