"""
Split the game board into individual cells. 
"""
import cv2
import matplotlib.pyplot as plt

class SplitBoard:
    def __init__(self, board_img):
        self.board_img = board_img
        self.cell_images = []
    
    def split_into_cells(self):
        """
        Split the board image into 16 individual cell images.
        return 4x4 list of cell images
        """
        h, w = self.board_img.shape[:2]
        
        # caculate the size of each cell
        tile_h = h // 4
        tile_w = w // 4

        tiles = []
        for row in range(4):
            row_tiles = []
            for col in range(4):
                # caculate the coordinates of the current cell
                y1 = row * tile_h
                y2 = (row + 1) * tile_h if row < 3 else h   # ensure the last tile includes any remaining pixels
                x1 = col * tile_w
                x2 = (col + 1) * tile_w if col < 3 else w   # ensure the last tile includes any remaining pixels

                # crop the tile with a margin
                margin = 5  # Adjust the margin as needed
                tile = self.board_img[y1+margin:y2-margin, x1+margin:x2-margin]
                
                row_tiles.append(tile)
            tiles.append(row_tiles)
        return tiles
    
    def visualize_tiles(self, tiles):
        """
        Visualize the split tiles by drawing rectangles on the original board image.
        """
        fig, axes = plt.subplots(4, 4, figsize=(10, 10))

        for i in range(4):
            for j in range(4):
                axes[i, j].imshow(cv2.cvtColor(tiles[i][j], cv2.COLOR_BGR2RGB))
                axes[i, j].set_title(f"{i},{j}")
                axes[i, j].axis('off')

        plt.tight_layout()
        plt.show()