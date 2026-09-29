import cv2

CAMERA = "/dev/video2"

cap = cv2.VideoCapture(CAMERA, cv2.CAP_V4L2)

if not cap.isOpened():
    print("Could not open Rapoo camera")
    exit()

# Use MJPG because the camera supports 1280x720 @ 30 FPS in MJPG mode
fourcc = cv2.VideoWriter_fourcc(*"MJPG")
cap.set(cv2.CAP_PROP_FOURCC, fourcc)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 30)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

print("Camera opened successfully")
print("Resolution:", width, "x", height)
print("FPS:", fps)

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to read frame")
        break

    cv2.imshow("AquaClean Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

