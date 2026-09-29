import cv2

from vision.detector import WasteDetector
from navigation.navigation import Navigator


CAMERA = "/dev/video2"

detector = WasteDetector()
navigator = Navigator()

cap = cv2.VideoCapture(CAMERA, cv2.CAP_V4L2)

if not cap.isOpened():
    print("Could not open camera")
    exit()

cap.set(
    cv2.CAP_PROP_FOURCC,
    cv2.VideoWriter_fourcc(*"MJPG")
)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 30)

print("AquaClean Vision + Navigation")
print("Press q to quit")

while True:

    ret, frame = cap.read()

    if not ret:
        print("Failed to read frame")
        break

    # YOLO detections
    detections = detector.detect(frame)

    # Select / maintain one target
    target = navigator.choose_target(detections)

    # Decide navigation behaviour
    navigation = navigator.decide(target)

    print(
        f"STATE={navigation['state']} | "
        f"STEERING={navigation['steering']:.2f} | "
        f"FORWARD={navigation['forward']:.2f}"
    )

    # Draw every detection
    for detection in detections:

        x1 = detection["x1"]
        y1 = detection["y1"]
        x2 = detection["x2"]
        y2 = detection["y2"]

        cx = detection["x"]
        cy = detection["y"]

        confidence = detection["confidence"]

        # All detected wastes
        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 180, 0),
            2
        )

        cv2.circle(
            frame,
            (cx, cy),
            5,
            (0, 180, 0),
            -1
        )

        cv2.putText(
            frame,
            f"waste {confidence:.2f}",
            (x1, max(y1 - 8, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 180, 0),
            2
        )

    # Highlight the selected target
    if target:

        x1 = target["x1"]
        y1 = target["y1"]
        x2 = target["x2"]
        y2 = target["y2"]

        cx = target["x"]
        cy = target["y"]

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 255),
            4
        )

        cv2.circle(
            frame,
            (cx, cy),
            9,
            (0, 0, 255),
            -1
        )

        cv2.putText(
            frame,
            "TARGET",
            (x1, max(y1 - 30, 25)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )

    # Camera centre line
    center_x = frame.shape[1] // 2

    cv2.line(
        frame,
        (center_x, 0),
        (center_x, frame.shape[0]),
        (255, 0, 0),
        2
    )

    # Navigation status
    nav_text = (
        f"{navigation['state']}   "
        f"STEER={navigation['steering']:.2f}   "
        f"FWD={navigation['forward']:.2f}"
    )

    cv2.putText(
        frame,
        nav_text,
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (0, 255, 255),
        2
    )

    cv2.imshow(
        "AquaClean Vision + Navigation",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

