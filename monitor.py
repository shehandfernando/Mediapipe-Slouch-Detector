import cv2
import mediapipe as mp
import math
import winsound

# Initialize MediaPipe Pose detection
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Open the webcam
cap = cv2.VideoCapture(0)

# Variables to track slouching
bad_posture_frames = 0
FRAMES_TOLERANCE = 30 # How many frames you can slouch before it beeps (approx 1 second)

def calculate_distance(p1, p2):
    """Calculates the distance between two points."""
    return math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)

print("Starting Posture Monitor... Press 'q' to quit.")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Convert the image to RGB (MediaPipe requires RGB)
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    status_text = "Good Posture"
    color = (0, 255, 0) # Green

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        
        # Get coordinates for the Nose and Shoulders
        nose = landmarks[mp_pose.PoseLandmark.NOSE.value]
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        
        # Calculate the midpoint of the shoulders
        shoulder_midpoint_y = (left_shoulder.y + right_shoulder.y) / 2
        
        # Calculate the vertical distance between the nose and the shoulders
        # (Y-coordinates go from 0 at the top to 1 at the bottom)
        neck_length = shoulder_midpoint_y - nose.y 

        # --- THE SLOUCH LOGIC ---
        # If your head drops too close to your shoulders, it triggers a warning.
        # You may need to tweak this 0.15 threshold depending on your camera angle!
        if neck_length < 0.15:
            status_text = "SLOUCHING!"
            color = (0, 0, 255) # Red
            bad_posture_frames += 1
        else:
            bad_posture_frames = 0 # Reset if you sit up straight

        # Beep if slouching for too long
        if bad_posture_frames > FRAMES_TOLERANCE:
            winsound.Beep(1000, 500) # Frequency 1000Hz, Duration 500ms
            bad_posture_frames = 0 # Reset to avoid continuous ear-piercing beeps

        # Draw the skeleton on your body
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Display the text on the screen
    cv2.putText(frame, status_text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    
    # Show the video window
    cv2.imshow('Posture Monitor', frame)

    # Quit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()