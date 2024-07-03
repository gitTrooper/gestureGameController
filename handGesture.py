import cv2
import mediapipe as mp
import pyautogui

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

prev_x, prev_y = 0, 0
threshold = 30  # Set a threshold for significant movement
current_direction = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            x = int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * frame.shape[1])
            y = int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * frame.shape[0])

            if prev_x and prev_y:
                dx = x - prev_x
                dy = y - prev_y

                if abs(dx) > threshold:
                    if dx > 0:
                        current_direction = "Move Left"
                        pyautogui.press('left')
                        
                    else:
                        current_direction = "Move Right"
                        pyautogui.press('right')

                if abs(dy) > threshold:
                    if dy > 0:
                        current_direction = "Move Down"
                        pyautogui.press('down')
                    else:
                        current_direction = "Move Up"
                        pyautogui.press('up')

            prev_x, prev_y = x, y

            if current_direction:
                print(current_direction)

    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
