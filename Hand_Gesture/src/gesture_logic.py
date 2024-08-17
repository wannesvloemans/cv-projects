import math
import mediapipe as mp

mp_hands = mp.solutions.hands

def distance(point1, point2):
    """Calculate Euclidean distance between two points."""
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

def angle_between_three_points(p1, p2, p3):
    """Calculate angle between three points (p1, p2, p3) in radians."""
    # Vector from p1 to p2
    v1 = (p2.x - p1.x, p2.y - p1.y)
    # Vector from p2 to p3
    v2 = (p3.x - p2.x, p3.y - p2.y)
    
    # Dot product and magnitudes
    dot_product = v1[0] * v2[0] + v1[1] * v2[1]
    mag_v1 = math.sqrt(v1[0] ** 2 + v1[1] ** 2)
    mag_v2 = math.sqrt(v2[0] ** 2 + v2[1] ** 2)
    
    # Calculate angle in radians
    angle = math.acos(dot_product / (mag_v1 * mag_v2))
    return angle

def identify_gesture(landmarks):
    """Identify gestures based on hand landmarks."""
    thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
    index_finger_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_finger_tip = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_finger_tip = landmarks[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = landmarks[mp_hands.HandLandmark.PINKY_TIP]
    
    # Thumb Up Gesture
    if (thumb_tip.y < index_finger_tip.y and
        thumb_tip.y < middle_finger_tip.y and
        thumb_tip.y < ring_finger_tip.y and
        thumb_tip.y < pinky_tip.y):
        return "Thumb Up"
    
    # Peace Sign Gesture
    if (index_finger_tip.y < thumb_tip.y and
        middle_finger_tip.y < thumb_tip.y and
        abs(thumb_tip.x - ring_finger_tip.x) < 0.1 and
        #ring_finger_tip.y > thumb_tip.y and
        #pinky_tip.y > thumb_tip.y and
        distance(index_finger_tip, middle_finger_tip) > 0.1):
        #abs(index_finger_tip.x - middle_finger_tip.x) < 0.1):
        return "Peace Sign"
    
    # Stop Sign Gesture (All fingers extended)
    if (index_finger_tip.y < thumb_tip.y and
        middle_finger_tip.y < thumb_tip.y and
        ring_finger_tip.y < thumb_tip.y and
        pinky_tip.y < thumb_tip.y):
        return "Stop Sign"
    
    return "Unknown Gesture"
