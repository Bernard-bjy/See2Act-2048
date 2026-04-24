"""
recognize the color of the number plate
"""
import cv2
import numpy as np

# color_num map
color_num_map = {
    (193,179,165): 0,
    (182, 171, 161): 2,
    (184, 169, 152): 4,
    (245, 205, 177): 8,
    (247, 187, 162): 16,
    (248, 182, 169): 32,
    (248, 164, 149): 64,
    (240, 214, 154): 128,
    (0, 128, 0): 256,
    (238, 200, 114): 512,
    (128, 128, 0): 1024,
    (240, 205, 125): 2048,
    }

class NumColorRecognizer:
    def __init__(self):
        pass
    
    def recognize_tile(self, tile_img):
        """
        Recognize the number on a tile based on its color.(BGR format)
        return the number on the tile, or None if the color is not recognized.
        """
        # Find the center region of the tile to avoid edge effects
        h, w = tile_img.shape[:2]
        
        # Debug visualization
        debug = tile_img.copy()
        cv2.rectangle(debug, (w//3, h//3), (2*w//3, 2*h//3), (0, 255, 0), 2)
        cv2.imshow("Tile Debug", debug)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        center_color = tile_img[h//3:2*h//3, w//3:2*w//3]  # Get the color

        # # Avoid edge effects by focusing on the center region of the tile
        # margin = 0.2  # Adjust the margin as needed

        # y1 = int(h * margin)
        # y2 = int(h * (1 - margin))
        # x1 = int(w * margin)
        # x2 = int(w * (1 - margin))

        # # Ensure the coordinates are within the image bounds
        # bg_region = tile_img[y1:y2, x1:x2]  # Get the background region

        # # Find the median color
        # median_color = np.median(bg_region, axis=(0,1))  # Median color in BGR format
        # rgb = tuple(int(x) for x in median_color[::-1])  # Convert to RGB format

        # Calculate the average color in the center region
        avg_color = np.mean(center_color, axis=(0, 1)) # Average color in BGR format
        avg_rgb = tuple(int(x) for x in avg_color[::-1])  # Convert to RGB format

        # Find the closest color in the color_num_map
        best_match = None
        min_distance = float('inf')
        for color, num in color_num_map.items():
            # Calculate the Euclidean distance between the average color and the current color in the map
            distance = sum((a - b) ** 2 for a, b in zip(avg_rgb, color)) ** 0.5
            if distance < min_distance:
                min_distance = distance
                best_match = num
        
        if min_distance >10:  # Threshold for color matching, adjust as needed
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
