"""
test
"""
import pyautogui
import mss

print("=== pyautogui (逻辑像素) ===")
print(f"size: {pyautogui.size()}")

print("\n=== mss (物理像素) ===")
with mss.mss() as sct:
    for i, m in enumerate(sct.monitors):
        print(f"Monitor {i}: {m}")

print("\n=== 鼠标当前位置 ===")
print(f"Position: {pyautogui.position()}")

