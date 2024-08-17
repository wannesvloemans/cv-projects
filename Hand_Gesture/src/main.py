import os
import numpy as np
import cv2
import mediapipe as mp 
import gesture_logic as gl

# Ensure the correct path to the model file
model_path = os.path.abspath('./models/gesture_recognizer.task')

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

cap = cv2.VideoCapture(0)

def draw_traffic_light(frame, state):
    # Define the size and position of the traffic light box
    top_left_corner = (30, 30)
    box_width = 100
    box_height = 300
    box_bottom_right = (top_left_corner[0] + box_width, top_left_corner[1] + box_height)

    # Draw the outer rectangle for the traffic light
    cv2.rectangle(frame, top_left_corner, box_bottom_right, (0, 0, 0), -1)

    # Set up light positions centered within the box
    center_x = top_left_corner[0] + box_width // 2
    light_radius = 40
    light_positions = [
        (center_x, top_left_corner[1] + light_radius + 20),  # Top light
        (center_x, top_left_corner[1] + box_height // 2),    # Middle light
        (center_x, top_left_corner[1] + box_height - light_radius - 20)  # Bottom light
    ]
    
    # Define colors in BGR
    active_color = {
        "green": (0, 255, 0),  # Green
        "orange": (0, 165, 255), # Orange
        "red": (0, 0, 255)       # Red
    }
    inactive_color = (211, 211, 211)  # Light grey
    
    # Determine which light is on based on the state
    color_state = {
        "Thumb Up": "green",
        "Peace Sign": "orange",
        "Stop Sign": "red"
    }
    active = color_state.get(state, None)
    
    # Draw all lights
    for position, color in zip(light_positions, active_color.keys()):
        if color == active:
            # Draw the active light with a solid color
            cv2.circle(frame, position, light_radius, active_color[color], -1)
        else:
            # Draw the inactive light with grey color
            cv2.circle(frame, position, light_radius, inactive_color, -1)

while True:
    ret, frame = cap.read()
    
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (0,0), fx=1.5, fy=1.5)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)

    gesture = None  # Default state if no gesture is recognized
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = hand_landmarks.landmark
            gesture = gl.identify_gesture(landmarks)
    
    # Draw the traffic light in the upper right corner
    draw_traffic_light(frame, gesture)

    cv2.imshow("Video", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break 

cap.release()
cv2.destroyAllWindows()
