# 😴 Drowsy Alert and Intervention System

A real-time drowsiness detection and intervention system built using **Raspberry Pi 4**, **OpenCV**, and **dlib**. The system monitors the driver's eye movements using a webcam and triggers alerts when drowsiness is detected, helping prevent road accidents caused by driver fatigue.

---

## 📌 Features

- Real-time face and eye detection using OpenCV and dlib
- Eye Aspect Ratio (EAR) based drowsiness detection
- Buzzer alert when drowsiness is detected
- Relay-controlled motor cut-off to simulate ignition intervention
- LED indicator for system status

---

## 🛠️ Hardware Requirements

| Component | Description |
|---|---|
| Raspberry Pi 4 | Central processing unit |
| Webcam | Captures real-time video for eye tracking |
| Buzzer | Audible alert on drowsiness detection |
| Relay Module | Controls motor/ignition cut-off |
| DC Motor | Simulates vehicle ignition intervention |
| LED | Visual alert indicator |
| Power Supply | 5V 3A USB-C for Raspberry Pi |

---

## 💻 Software Requirements

- Python 3
- OpenCV (`opencv-python`)
- dlib
- scipy
- RPi.GPIO
- NumPy

Install dependencies:
```bash
pip3 install opencv-python dlib scipy numpy
```

---

## 📁 Project Structure

```
code/
└── drowsy_alert_intervene.py   # Main detection and intervention script
```

---

## ⚙️ How It Works

1. Webcam captures real-time video frames
2. dlib detects facial landmarks (68 points)
3. Eye Aspect Ratio (EAR) is calculated using the formula:

```
EAR = (||P2-P6|| + ||P3-P5||) / (2 * ||P1-P4||)
```

4. If EAR falls below **0.3** for **20 consecutive frames**, drowsiness is detected
5. System triggers:
   - 🔴 LED turns ON
   - 🔊 Buzzer sounds for 5 seconds
   - ⚙️ Motor relay cuts off (simulates ignition cut)

---

## 🚀 How to Run

```bash
python3 drowsy_alert_intervene.py
```

> Make sure `shape_predictor_68_face_landmarks.dat` is in the same directory.

Press **'q'** to quit the application.

---

## 📊 Results

- Successfully detects drowsiness under controlled conditions
- System accuracy: ~90%
- Real-time performance on Raspberry Pi 4


