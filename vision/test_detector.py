import cv2

from detector import WasteDetector


CAMERA = "/dev/video2"

detector = WasteDetector()

cap = cv2.VideoCapture(CAMERA, cv2.CAP_V4L2)

if not cap.isOpened():
    print("Could not open Rapoo camera")
    exit()

cap.set(
    cv2.CAP_PROP_FOURCC,
    cv2.VideoWriter_fourcc(*"MJPG")
)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 30)

print("AquaClean detector test")
print("Press q to quit")

while True:

    ret, frame = cap.read()

    if not ret:
        print("Failed to read frame")
        break

    detections = detector.detect(frame)

    for detection in detections:

        x1 = detection["x1"]
        y1 = detection["y1"]
        x2 = detection["x2"]
        y2 = detection["y2"]

        cx = detection["x"]
        cy = detection["y"]

        confidence = detection["confidence"]

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        cv2.circle(
            frame,
            (cx, cy),
            6,
            (0, 0, 255),
            -1
        )

        label = f"waste {confidence:.2f}  ({cx},{cy})"

        cv2.putText(
            frame,
            label,
            (x1, max(y1 - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

    best_target = detector.get_best_target(detections)

    if best_target:
        print(
            f"Target: "
            f"x={best_target['x']} "
            f"y={best_target['y']} "
            f"area={best_target['area']} "
            f"confidence={best_target['confidence']:.2f}"
        )
    else:
        print("No waste detected")

    cv2.imshow("AquaClean Detector", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

