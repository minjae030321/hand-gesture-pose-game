# Hand Gesture and Pose Controlled Game

This project is a gesture and pose-based game where players control a cannon's angle, power, and firing mechanism using hand gestures. The objective is to hit a randomly placed target by dynamically adjusting the cannon's settings.

---

## Features

- **Hand Gesture Control**: Adjust cannon angle and fire using hand gestures.
- **Pose-Based Power Control**: Detects hand pose angles to calculate firing power dynamically.
- **Interactive Gameplay**:
  - Physics-based projectile motion with gravity and wind effects.
  - Randomly placed targets regenerate upon successful hits.
- **Dynamic Visuals**: Tkinter-based interface integrated with real-time webcam feedback.

---

## Prerequisites

1. **Python Environment**: Python 3.x installed.
2. **Required Libraries**:
   ```bash
   pip install opencv-python numpy pillow cvzone
   ```
3. **Image Resources**:
- `canon.png`: Cannon image.
- `apple.png`: Target image.
- Ensure these images are in the same directory as the script.

---

## Setup and Execution

1. Clone the repository:
```bash
git clone https://github.com/minjae030321/hand-gesture-pose-game.git
```
2. Place the required images (`canon.png` and `apple.png`) in the same directory as the script.
3. Run the script:
  ```bash
  python computer_vision_game.py
  ```
4. Ensure your webcam is properly connected and accessible.

---

## How to Play

- **Cannon Movement**:
- Raise **1 finger**: Increase cannon angle.
- Raise **
  2 fingers**: Decrease cannon angle.
- **Fire Cannon**:
  - Raise **3 fingers**:
    - Hold to charge power.
    - Release to fire.
- **Objective**:
  - Hit the target to score points. Each successful hit regenerates the target at a new random location.

### Additional Features:
- **Power Gauge**: A red bar indicates the current firing power.
- **Wind Effect**: A blue bar visualizes wind direction and intensity, affecting the projectile's trajectory.
- **Projectile Physics**: Includes gravity and wind acceleration for realistic motion.

---

## Code Overview

### Key Components:

1. **Hand and Pose Detection**:
   - Detects gestures and calculates power using `HandTrackingModule` and `PoseModule`.
2. **Tkinter Game Interface**:
   - Visualizes cannon, angle, power gauge, wind bar, and targets.
3. **Game Logic**:
   - Manages cannon control, projectile physics, and target regeneration.
   - Dynamically updates the score and handles stage transitions.

---

## Known Issues

- Ensure the webcam is properly connected before running the script.
- The performance may vary depending on system specifications and webcam quality.
- Missing required images (`canon.png`, `apple.png`) will cause the game to fail.

---

## Future Improvements

- Add multi-hand support for advanced gameplay.
- Introduce moving targets or dynamic obstacles for increased difficulty.
- Optimize gesture detection for smoother and more accurate control.

---

For additional support or feedback, please create an issue in the repository.

