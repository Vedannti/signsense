from gettext import install
import cv2
import time
import requests

# Open camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


# Dummy letters for testing
letters = ["A", "B", "C", "D", "E"]
index = 0

print("Camera started. Press Q to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if 'last_letter' not in globals():
        last_letter = None

    predicted_letter = letters[index]

    if predicted_letter != last_letter:
        try:
            requests.get(f"http://127.0.0.1:5000/update/{predicted_letter}")
            last_letter = predicted_letter
        except:
            pass

    # Show on camera window
    cv2.putText(frame,
                f"Detected: {predicted_letter}",
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2)

    cv2.imshow("Hand Detection (Dummy)", frame)

    if cv2.waitKey(1) & 0xFF == ord('n'):
        index = (index + 1) % len(letters)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
