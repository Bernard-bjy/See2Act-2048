"""
recognize the color of the number plate
"""
import cv2
import numpy as np

# color_num_map(rgb)
color_num_map = {
    (193,179,165): 0,
    (234, 222, 209): 2,
    (232, 217, 188): 4,
    (238, 161, 102): 8,
    (240, 129, 81): 16,
    (241, 101, 78): 32,
    (241, 71, 45): 64,
    (232, 198, 95): 128,
    (232, 195, 80): 256,
    (232, 191, 64): 512,
    (231, 186, 49): 1024,
    (241, 183, 36): 2048,
    }

class NumColorRecognizer:

    # Color format
    # Not yellow: match with rgb
    rgb_map = {
    (193,179,165): 0,
    (234, 222, 209): 2,
    (232, 217, 188): 4,
    (238, 161, 102): 8,
    (240, 129, 81): 16,
    (241, 101, 78): 32,
    (241, 71, 45): 64
    }

    # yellow: match with hsv(caculate from rgb)
    yellow_hsv_map = [
        (128, 0.00, 0.55, 0),      # s < 62%
        (256, 0.55, 0.60, 0),     # 62% <= s < 69%
        (512, 0.60, 0.66, 0),     # 69% <= s < 75%
        (1024, 0.66, 0.72, 0),    # 75% <= s < 82%
        (2048, 0.72, 1.01, 0.93)     # 82% <= s < 101% and v >=93%
    ]
    yellow_reference_rgb = (231, 186, 49) # value of 1024(just reference, could be any yellow tile)
    yellow_rgb_radius = 20 # just exp, radius can be changed

    def __init__(self, debug=True):
        self.debug = debug
    
    def get_bg_sample_box(self, cell_x, cell_y, cell_w, cell_h, ratio = 0.1):
        """
        Get a sample box for background color sampling.
        return the coordinates of the sample box (x, y, w, h).
        """
        sample_size = min(cell_w, cell_h) * ratio  # Sample box size as a fraction of the cell size
        x = int(cell_x + (cell_w - sample_size) / 2)  # Center the sample box within the cell
        y = int(cell_y + (cell_h * (1 - ratio)) - sample_size)  # Place the sample box near the bottom of the cell
        w = int(sample_size)
        h = int(sample_size)
        return x, y, w, h

    def rgb_to_hsv(self,r, g, b):
        r, g, b = r / 255, g / 255, b/255
        mx = max(r, g, b)
        mn = min(r, g, b)
        D_value = mx - mn
        if D_value == 0:
            h = 0
        elif mx == r:
            h = (g - b) / D_value % 6
        elif mx == g:
            h = (b - r) / D_value + 2
        else:
            h = (r - g) / D_value + 4
        s = 0 if mx == 0 else D_value / mx
        v = mx
        return (h, s, v)
    
    # def is_yellow(self, rgb):
    #     r, g, b = rgb
    #     center = self.yellow_reference_rgb
    #     distance = sum((a - b) ** 2 for a, b in zip(rgb, center)) ** 0.5
    #     return distance < self.yellow_rgb_radius
    
    # def recognize_yellow_tile(self, hsv):
    #     for num, s_min, s_max, v_min in self.yellow_hsv_map:
    #         if s_min <= hsv[1] < s_max:
    #             # if num == 2048 and hsv[2] < v_min:
    #             #     return 1024
    #             return num
    #     closest_num = min(self.yellow_hsv_map, key=lambda x: abs(hsv[1] - (x[1] + x[2]) / 2))
    #     return closest_num[0]

    def recognize_tile(self, tile_img):
        """
        Recognize the number on a tile based on its color.(BGR format)
        return the number on the tile, or None if the color is not recognized.
        """
        h, w = tile_img.shape[:2]
        # 1. Get the sample box for background color sampling
        sx, sy, sw, sh = self.get_bg_sample_box(0, 0, w, h) # Get the cooerdinates of the sample box
        # 2. Extract the sample box region from the tile image
        sample = tile_img[sy:sy+sh, sx:sx+sw]  # Extract the sample box region
        # 3. Calculate the average color in the sample box
        avg_color = np.mean(sample, axis=(0, 1)).astype(int)  # Average color in BGR format
        avg_rgb = tuple(int(x) for x in avg_color[::-1])  # Convert to RGB format

        if self.debug:
            hsv_h, hsv_s, hsv_v = self.rgb_to_hsv(*avg_rgb)
            print(f"Debug: avg_rgb={avg_rgb}, h={hsv_h:.3f}, s={hsv_s:.3f}, v={hsv_v:.3f}")

        # if self.debug:
        #     debug_img = tile_img.copy()
        #     cv2.rectangle(debug_img, (sx, sy), (sx+sw, sy+sh), (0, 255, 0), 2)  # Draw the sample box
        #     cv2.putText(debug_img, f"Avg RGB: {avg_rgb}", (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        #     cv2.imshow(f"Tile Debug RGB{avg_rgb}", debug_img)
        #     cv2.waitKey(0)
        #     cv2.destroyAllWindows()

        # yellow check (h > 0.6)
        hsv_h, hsv_s, hsv_v = self.rgb_to_hsv(*avg_rgb)
        if hsv_h > 0.6:
            for num, s_min, s_max, v_min in self.yellow_hsv_map:
                if s_min <= hsv_s < s_max:
                    # if num == 2048 and hsv_v < v_min:
                    #     return 1024
                    return num
            closest_num = min(self.yellow_hsv_map, key=lambda x: abs(hsv_s - (x[1] + x[2]) / 2))
            return closest_num[0]
        
        # if self.is_yellow(avg_rgb):
        #     hsv_h, hsv_s, hsv_v = self.rgb_to_hsv(*avg_rgb)
        #     result = self.recognize_yellow_tile((hsv_h, hsv_s, hsv_v))
           
        #     # if self.debug:
        #     #     print(f"Yellow tile detected: avg_rgb={avg_rgb}, hsv=({hsv_h:.1f}, {hsv_s:.1f}, {hsv_v:.1f}), recognized number={result}")

        #     return result
            

        # not yellow, match with rgb map
        best_match = None
        min_distance = float('inf')
        for color, num in self.rgb_map.items():
            # Calculate the Euclidean distance between the average color and the current color in the map
            distance = sum((a - b) ** 2 for a, b in zip(avg_rgb, color)) ** 0.5
            if distance < min_distance:
                min_distance = distance
                best_match = num
        
        if min_distance > 35:
            print(f"Warning, unknown color: avg_rgb={avg_rgb}, best_match={best_match}, distance={min_distance:.1f}")
            # Print the recognized color and number
            print(f"Tile color:RGB={avg_rgb}, best_match={best_match}, distance={min_distance:.1f}  ")


        return best_match
    
    def board_to_matrix(self, tiles):
        """
        Convert a 4x4 list of tiles to a matrix.
        tiles: split_board.split_into_cells() returns a 4x4 list of tile images.
        return a 4x4 matrix of numbers on the tiles.
        """
        matrix = np.zeros((4, 4), dtype=int)
        for i in range(4):
            for j in range(4):
                matrix[i, j] = self.recognize_tile(tiles[i][j])
        return matrix

if __name__ == "__main__":
    # Example usage
    # Load a sample tile image (replace with actual tile image path)
    tile_img = cv2.imread("sample_tile.png")
    
    recognizer = NumColorRecognizer()
    number = recognizer.recognize_tile(tile_img)
    print(f"Recognized number on the tile: {number}")
