import cv2
import os

# CHANGE THIS LABEL EACH TIME: A / B / C
label = "C"

save_path = f"dataset/{label}"
os.makedirs(save_path, exist_ok=True)

camera = cv2.VideoCapture(0)
count = 0

print("Press 's' to SAVE image")
print("Press 'q' to QUIT")

while True:
    ret, frame = camera.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    # ROI for hand
    x1, y1 = 100, 100
    x2, y2 = 400, 400
    roi = frame[y1:y2, x1:x2]

    # Draw ROI box
    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

    cv2.imshow("Data Collection", frame)

    key = cv2.waitKey(1)

    if key == ord('s'):
        img_name = f"{save_path}/{count}.jpg"
        cv2.imwrite(img_name, roi)
        print(f"Saved: {img_name}")
        count += 1

    elif key == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
