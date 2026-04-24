"""
recognize the color of the number plate
"""
import cv2
import numpy as np

# color_num map
color_num_map = {
    (193,179,165): 0,
    (234, 222, 209): 2,
    (232, 217, 188): 4,
    (238, 161, 102): 8,
    (240, 129, 81): 16,
    (241, 101, 78): 32,
    (241, 71, 45): 64,
    (232, 198, 95): 128,
    (0, 128, 0): 256,
    (232, 191, 64): 512,
    (128, 128, 0): 1024,
    (241, 183, 36): 2048,
    }

class NumColorRecognizer:
    def __init__(self, debug=False):
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
            debug_img = tile_img.copy()
            cv2.rectangle(debug_img, (sx, sy), (sx+sw, sy+sh), (0, 255, 0), 2)  # Draw the sample box
            cv2.putText(debug_img, f"Avg RGB: {avg_rgb}", (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            cv2.imshow(f"Tile Debug RGB{avg_rgb}", debug_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        # Find the closest color in the color_num_map
        best_match = None
        min_distance = float('inf')
        for color, num in color_num_map.items():
            # Calculate the Euclidean distance between the average color and the current color in the map
            distance = sum((a - b) ** 2 for a, b in zip(avg_rgb, color)) ** 0.5
            if distance < min_distance:
                min_distance = distance
                best_match = num
        
        if min_distance > 35:  # Threshold for color matching, adjust as needed
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
