# Mediapipe Slouch Detector 📸

A lightweight Computer Vision script that uses your webcam to monitor your posture in real-time. Built with Python, OpenCV, and Google's MediaPipe, this tool maps your facial and body landmarks and tracks the vertical distance between your nose and your shoulders. 

If you hunch over your desk or drop your head for too long, the script triggers an OS-level audio beep to remind you to sit up straight.

## 🚀 Getting Started

### Prerequisites
You need Python 3.x installed along with the required vision libraries. Install them via pip:
`pip install opencv-python mediapipe`

*(Note: This script uses `winsound` for audio alerts, which is native to Windows. If you are on Mac/Linux, you will need to swap `winsound` for a library like `playsound`).*

### Running the Monitor
1. Open your terminal or command prompt.
2. Navigate to the project directory.
3. Run the script:
   `python monitor.py`
4. A webcam window will pop up. Press the `q` key on your keyboard while the window is focused to exit the program.

## ⚙️ Configuration & Calibration
Depending on the height and angle of your webcam, you may need to calibrate the slouch detection threshold. 

Open `monitor.py` and locate the slouch logic section:
`if neck_length < 0.15:`

* If it is beeping while you are sitting up straight, **decrease** the `0.15` value (e.g., `0.12`).
* If it is not catching your slouches, **increase** the value (e.g., `0.18`).

## 🛠️ Tech Stack
* **OpenCV (`cv2`):** Handles the real-time webcam video stream and frame-by-frame image rendering.
* **MediaPipe (`mediapipe`):** Runs the machine learning model that detects and maps human pose landmarks.

## 📝 License
This project is open-source and available under the [MIT License](LICENSE).

---
*Developed by [Shehan Fernando](https://github.com/shehandfernando)*
