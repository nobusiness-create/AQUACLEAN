import cv2
import os

CAMERA = "/dev/video2"

cap = cv2.VideoCapture(CAMERA, cv2.CAP_V4L2)

cap.set(cv2.CAP_PROP_FOURCC,
        cv2.VideoWriter_fourcc(*"MJPG"))

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 30)

if not cap.isOpened():
    print("Could not open camera")
    exit()

os.makedirs("test_frames", exist_ok=True)

count = 0

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to read frame")
        break

    cv2.imshow("AquaClean Capture", frame)

    key = cv2.waitKey(1) & 0xFF

    # Press s to save a frame
    if key == ord("s"):
        filename = f"test_frames/frame_{count}.jpg"
        cv2.imwrite(filename, frame)
        print("Saved:", filename)
        count += 1

    # Press q to quit
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

