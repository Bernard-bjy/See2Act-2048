"""
尝试读取图像并显示
"""
import cv2

class Open_img:
    def __init__(self, path):
        self.path = path
        self.img = cv2.imread(self.path)    # 直接读取图像
        if self.img is None:
            print(f"无法读取图像，请检查路径: {self.path}")
        else:
            print(f"成功读取图像: {self.path}")
    
    def show_img(self):
        if self.img is not None:
            cv2.imshow('image', self.img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("没有图像可显示")

if __name__ == "__main__":
    image = Open_img('/Users/bijunyao/Desktop/AI Develop/2048决策智能体/截屏2026-04-15 22.24.38.png')
    image.show_img()

    
# cv2.imshow('image', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()