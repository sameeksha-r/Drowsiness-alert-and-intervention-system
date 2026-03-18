import cv2
import dlib
import numpy as np
from scipy.spatial import distance as dist
import RPi.GPIO as GPIO
import time

# Set up GPIO for LED, buzzer, and motor control
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

LED_PIN = 17   # Define the GPIO pin connected to the LED
BUZZER_PIN = 22  # Define the GPIO pin connected to the buzzer
MOTOR_PIN = 27   # Define the GPIO pin connected to the relay controlling the motor

GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(MOTOR_PIN, GPIO.OUT)

# Test the LED and Buzzer
print("Testing LED and Buzzer...")
GPIO.output(LED_PIN, GPIO.HIGH)  # Turn on the LED
time.sleep(2)
GPIO.output(LED_PIN, GPIO.LOW)   # Turn off the LED
time.sleep(2)

GPIO.output(BUZZER_PIN, GPIO.HIGH)  # Turn on the buzzer
time.sleep(2)
GPIO.output(BUZZER_PIN, GPIO.LOW)   # Turn off the buzzer
time.sleep(2)

# Load dlib's face detector and facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Start video capture
cap = cv2.VideoCapture(0)  # Use 0 for the default camera

# Check if the video capture is successful
if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

# Define constants for EAR calculation and drowsiness detection
EAR_THRESHOLD = 0.3  # Threshold for drowsiness detection
CONSEC_FRAMES = 20    # Number of consecutive frames with low EAR to trigger alarm
frame_count = 0       # Counter for consecutive frames

# Function to calculate Eye Aspect Ratio (EAR)
def calculate_ear(eye):
    vertical_1 = dist.euclidean(eye[1], eye[5])
    vertical_2 = dist.euclidean(eye[2], eye[4])
    horizontal = dist.euclidean(eye[0], eye[3])
    ear = (vertical_1 + vertical_2) / (2.0 * horizontal)
    return ear

# Start video capture loop
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale image
    faces = detector(gray)

    for face in faces:
        # Get the landmarks for each face
        landmarks = predictor(gray, face)

        # Get the coordinates for the left and right eye
        left_eye = [(landmarks.part(i).x, landmarks.part(i).y) for i in range(36, 42)]
        right_eye = [(landmarks.part(i).x, landmarks.part(i).y) for i in range(42, 48)]

        # Convert eye coordinates to numpy array
        left_eye = np.array(left_eye)
        right_eye = np.array(right_eye)

        # Calculate EAR for both eyes
        left_ear = calculate_ear(left_eye)
        right_ear = calculate_ear(right_eye)
        
        # Average EAR for both eyes
        ear = (left_ear + right_ear) / 2.0

        # Draw the eyes using convex hulls (ensure the points are numpy arrays)
        cv2.polylines(frame, [cv2.convexHull(left_eye)], isClosed=True, color=(0, 255, 0), thickness=2)
        cv2.polylines(frame, [cv2.convexHull(right_eye)], isClosed=True, color=(0, 255, 0), thickness=2)

        # Check if the EAR is below the threshold for drowsiness detection
        if ear < EAR_THRESHOLD:
            frame_count += 1

            # Trigger the alert if eyes are closed for enough frames
            if frame_count >= CONSEC_FRAMES:
                cv2.putText(frame, "DROWSINESS DETECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
                # Trigger the buzzer and turn off the motor
                GPIO.output(BUZZER_PIN, GPIO.HIGH)  # Turn on the buzzer
                GPIO.output(MOTOR_PIN, GPIO.HIGH)  # Turn off the motor (relay off)
                GPIO.output(LED_PIN, GPIO.HIGH)  # Turn on the LED
                time.sleep(5)  # Buzzer will sound for 5 seconds
                GPIO.output(BUZZER_PIN, GPIO.LOW)  # Turn off the buzzer
        else:
            frame_count = 0  # Reset the frame count if the eyes are open
            GPIO.output(LED_PIN, GPIO.LOW)  # Turn off the LED
            GPIO.output(MOTOR_PIN, GPIO.LOW)  # Turn on the motor (relay on)

    # Display the frame with the detected landmarks and drowsiness alert
    cv2.imshow("Drowsiness Detection", frame)

    # Break the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the OpenCV window
cap.release()
cv2.destroyAllWindows()

# Clean up GPIO settings
GPIO.cleanup()