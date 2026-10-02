# ✋ HAND-VISION – Hand Gesture Recognition System

### 🤖 AI-Based Real-Time Hand Gesture Recognition

HAND-VISION is a real-time hand gesture recognition system developed in Python using **OpenCV** and **MediaPipe**.

The system uses a webcam to detect a single hand, track its **21 hand landmarks**, analyze finger positions, and recognize predefined hand gestures. Each recognized gesture is mapped to a corresponding action and displayed through a simple real-time interface.

The project uses a modular structure, keeping the main application and gesture recognition logic separate for easier maintenance and future expansion.

---

## ✨ Features

- 🎥 Real-time webcam hand detection
- ✋ Single-hand gesture recognition
- 🤖 MediaPipe hand landmark tracking
- 🧠 Rule-based gesture classification
- ✋ 10 predefined gestures
- 🧭 Four directional pointing gestures
- ☝️ Index-finger-only directional pointing
- 👍 Thumbs Up and Thumbs Down recognition
- ⚡ Gesture-to-action mapping
- 📖 Interactive Help screen
- ⌨️ Keyboard (H/Q) controls
- 🖥️ Resizable application window
- 🧩 Separate gesture recognition module
- 🔧 Easy-to-modify gesture recognition logic

---

## 👋 Supported Gestures

The current version supports **10 gestures**.

| ✋ Gesture | ⚡ Action |
|---|---|
| ✊ **FIST** | 🛑 **STOP** |
| 🖐️ **OPEN PALM** | ⏸️ **PAUSE** |
| 👍 **THUMBS UP** | ✅ **APPROVE** |
| 👎 **THUMBS DOWN** | ❌ **REJECT** |
| ☝️ **POINT UP** | ⬆️ **UP** |
| ☝️ **POINT DOWN** | ⬇️ **DOWN** |
| ☝️ **POINT LEFT** | ⬅️ **LEFT** |
| ☝️ **POINT RIGHT** | ➡️ **RIGHT** |
| ✌️ **VICTORY** | ▶️ **PLAY** |
| 🤘 **ROCK** | 🤘 **ROCK** |

The gesture-action mapping is also available through the application's Help screen.

---

## 🧠 How It Works

HAND-VISION follows a real-time computer vision pipeline:

```text
🎥 Webcam
     ↓
🖼️ Video Frame
     ↓
🔄 BGR → RGB Conversion
     ↓
🤖 MediaPipe Hand Detection
     ↓
📍 21 Hand Landmarks
     ↓
🖐️ Finger Position Analysis
     ↓
🧠 Rule-Based Gesture Recognition
     ↓
⚡ Action Mapping
     ↓
🖥️ Real-Time Display
````

The system analyzes finger positions, angles, distances and the index-finger direction to identify the gesture.

---

## 🔄 System Workflow

```text
👋 User Shows One Hand
          ↓
🎥 Webcam Captures Frame
          ↓
🤖 MediaPipe Detects Hand
          ↓
📍 21 Landmarks Generated
          ↓
🖐️ Finger Positions Analyzed
          ↓
🧠 Gesture Rules Applied
          ↓
⚡ Action Identified
          ↓
🖥️ Gesture + Action Displayed
```

---

## 🔍 Gesture Recognition

MediaPipe provides **21 landmarks** for the detected hand.

These landmarks are analyzed to determine:

* Which fingers are extended
* Which fingers are folded
* Finger joint angles
* Finger length and straightness
* Index-finger direction
* Thumb position

The information is then compared against predefined gesture rules.

---

## 🖥️ Application Interface

HAND-VISION currently provides two main interface modes.

### 📷 Camera Screen

The camera screen provides:

* Real-time webcam view
* MediaPipe hand landmarks
* Detected gesture
* Corresponding action
* Keyboard controls
* Centered HAND-VISION title
* Compact information panel

Example:

```text
              HAND-VISION
       Hand Gesture Recognition


       [ Real-Time Camera View ]


┌─────────────────────────────┐
│ Gesture: POINT RIGHT        │
│ Action:  RIGHT              │
└─────────────────────────────┘
                         H - Help
                         Q - Exit
```

The information panel is intentionally kept compact so that it does not unnecessarily cover the user's hand.

### 📖 Help Screen

Press **H** while the camera is running to open the Help screen.

The Help screen provides a list of supported gestures and their corresponding actions.

* **H** → Return to camera
* **Q** → Exit application

---

## 📁 Project Structure

```text
Syntecxhub_Hand_Gesture_Recognition/
│
├── 📄 hand_gesture_recognition.py
├── 📄 gestures.py
├── 📄 requirements.txt
└── 📄 README.md
```

### Main Files

**`hand_gesture_recognition.py`**

This is the main application and **webcam demo script** for the project.

It handles:

* 🎥 Webcam access
* 🖼️ Video frame capture
* 🔄 Image conversion
* 🤖 MediaPipe hand processing
* ✋ Hand landmark display
* 🧠 Gesture recognition calls
* 🖥️ User interface
* 📖 Help screen
* ⌨️ Keyboard controls

**`gestures.py`**

This module contains the gesture recognition logic.

It handles:

* 🖐️ Finger detection
* 📐 Finger angle calculations
* 📏 Landmark distance calculations
* 🧭 Direction detection
* 🧠 Gesture classification
* ⚡ Gesture-to-action mapping
* 📋 Gesture table used by the Help screen

Keeping the recognition logic separate from the main application makes the project easier to modify.

New gestures can be added by updating the gesture table and recognition rules in `gestures.py`.

---

## 🛠️ Technologies Used

* **Python 3.11** = Main programming language
* **OpenCV** = Webcam access, image processing and interface
* **MediaPipe** = Hand landmark detection and tracking
* **NumPy** = Handling numerical data
* **Math** = Distance and angle calculations
* **Sys** = Python system settings

---

## 📦 Requirements

The project uses the following tested versions:

```text
opencv-python==4.11.0.86
mediapipe==0.10.21
numpy==1.26.4
```

These versions should be kept together for the current project setup. The Python libraries are listed in `requirements.txt`.

---

## ⚙️ Installation

### 1. Open the project folder

```bash
cd Syntecxhub_Hand_Gesture_Recognition
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

---

## ▶️ Run the Project

The `hand_gesture_recognition.py` file is the main **webcam demo script** for HAND-VISION. It runs the complete system using webcam input for real-time hand gesture recognition.

Run:
```bash
python hand_gesture_recognition.py
```

When the application starts successfully, the terminal displays:

```text
HAND-VISION launched successfully.
Webcam connected.
```

The HAND-VISION application window will then open and begin real-time gesture recognition.

When **Q** is pressed:

```text
HAND-VISION closed successfully.
```

---

## 💡 Example Interaction

### Step 1: 🎥 Start the application.
### Step 2: ✋ Place one hand in front of the webcam.
### Step 3: 🤖 MediaPipe detects the hand and its landmarks.
### Step 4: 🧠 The system analyzes the finger positions.
### Step 5: ⚡ HAND-VISION identifies the gesture and corresponding action.
### Step 6: 📖 Press **H** to view the gesture guide.
### Step 7: 📷 Press **H** again to return to the camera.
### Step 8: ❌ Press **Q** to close the application.

---

## 🚀 Future Improvements

* 🧠 Machine-learning-based gesture classification
* 🎯 Improved recognition accuracy
* 🔄 Gesture smoothing for more stable results
* ✋ Additional hand gestures
* 🖥️ Gesture-based computer controls
* 📜 Gesture history
* ✋ Multi-hand gesture recognition
* ➕ Custom gesture creation

---

## 🎓 Internship Information

| Category                | Details                                       |
| ----------------------- | --------------------------------------------- |
| 🏢 **Organization**     | **Syntecxhub**                                |
| 💼 **Program**          | **AI Internship**                             |
| 📋 **Task**             | **Task 3 – Hand Gesture Recognition**         |
| 🤖 **Project**          | **HAND-VISION – Hand Gesture Recognition System** |
| 🐍 **Language**         | **Python**                                    |
| 👁️ **Computer Vision** | **OpenCV + MediaPipe**                        |

---

## 👨‍💻 Author

Developed as part of the **Syntecxhub AI Internship**.

---

## 📜 License

This project is created for educational and internship purposes.

---

<div align="center">

## ✋ HAND-VISION

**Turning Hand Gestures Into Digital Actions 🤖⚡**

**Built with Python • OpenCV • MediaPipe**

</div>

 
