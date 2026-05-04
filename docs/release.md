# 🎮 See2Act-2048 v1.0.0 - MVP Release

Vision-based autonomous playing system for 2048 game with robust perception-decision-act loop.

---

## ✨ Core Features

- **Real-time Screen Capture**: High-performance screen grabbing using MSS + OpenCV
- **Visual Board Detection**: HSV color-space based game board localization
- **Tile Recognition**: Background color sampling approach for number identification
- **Automated Decision Making**: Greedy algorithm with heuristics (monotonicity, smoothness, max tile position)
- **Keyboard Control Simulation**: Automated arrow key press execution

---

## 🏗️ System Architecture

```mermaid
flowchart LR
    subgraph Perception
        A[MSS Screen Capture]
        B[HSV Board Detection]
    end
    subgraph Processing
        C[Split 4x4 Grid]
        D[Recognize Numbers]
    end
    subgraph Decision to Act
        E[Greedy Algorithm]
        F[Simulate Key Press]
    end

    A --> B --> C --> D --> E --> F
```

**Modules:**
- `mss_to_opencv.py` - Screen capture pipeline
- `board_detector.py` - Game board localization
- `split_board.py` - Grid cell extraction
- `num_color_recognize.py` - Tile number recognition
- `greedy_algorithm.py` - Decision engine
- `controller.py` - Keyboard action execution

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| Screen capture latency | ~30-50ms |
| Board detection success rate | >95% |
| Max moves per game (safety cap) | 1000 |

---

## ⚠️ Known Issues

- **Algorithm limitation**: The greedy strategy rarely reaches the 2048 tile (success rate <5% in early tests)

---

## 🗺️ Roadmap

| Version | Planned Features |
|---------|---------------|
| v1.1.0 | Expectimax algorithm with depth-3 search |
| v1.2.0 | Monte Carlo Tree Search (MCTS) implementation |
| v2.0.0 | Deep learning-based end-to-end decision model |
| v2.1.0 | Multi-threading optimization for real-time performance |

---

## 🛠️ Tech Stack

- **Language**: Python 3.11
- **OS**: macOS
- **Key Libraries**: OpenCV-Python, MSS, NumPy, PyAutoGUI

---

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/Bernard-bjy/See2Act-2048.git
cd See2Act-2048

# Install dependencies
pip install -r requirements.txt

# Ensure a 2048 game window is visible on screen (e.g., open https://play2048.co/)
# Then run
python main.py
```

---

## 📦 Example requirements.txt

```text
opencv-python>=4.5
mss>=6.0.0
numpy>=1.19
pyautogui>=0.9.53
```

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.