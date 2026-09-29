import cv2
from ultralytics import YOLO

MODEL_PATH = "/home/gopika/aquaclean/runs/detect/aquaclean_yolo26n_v1/weights/best.pt"
CAMERA = "/dev/video2"

model = YOLO(MODEL_PATH)

cap = cv2.VideoCapture(CAMERA, cv2.CAP_V4L2)

if not cap.isOpened():
    print("Could not open Rapoo camera")
    exit()

# Camera settings
cap.set(cv2.CAP_PROP_FOURCC,
        cv2.VideoWriter_fourcc(*"MJPG"))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 30)

print("Camera opened successfully")
print("Press q to quit")

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to read frame")
        break

    results = model(
        frame,
        conf=0.40,
        verbose=False
    )

    result = results[0]

    detections = []

    if result.boxes is not None:
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            confidence = float(box.conf[0])

            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])

            # Center of the bounding box
            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)

            detections.append({
                "x": cx,
                "y": cy,
                "confidence": confidence,
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2
            })

            # Draw box
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            # Draw centroid
            cv2.circle(
                frame,
                (cx, cy),
                6,
                (0, 0, 255),
                -1
            )

            label = f"waste {confidence:.2f} ({cx},{cy})"

            cv2.putText(
                frame,
                label,
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

    # Print detections to terminal
    if detections:
        print("Detections:", detections)

    cv2.imshow("AquaClean - Live YOLO", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

