from ultralytics import YOLO


class WasteDetector:
    """
    AquaClean YOLO waste detector.

    Input:
        OpenCV BGR frame

    Output:
        List of waste detections.
    """

    def __init__(
        self,
        model_path="/home/gopika/aquaclean/runs/detect/aquaclean_yolo26n_v1/weights/best.pt",
        confidence=0.40,
    ):
        self.model = YOLO(model_path)
        self.confidence = confidence

    def detect(self, frame):
        """
        Detect waste in one frame.

        Returns:
            list[dict]
        """

        frame_height, frame_width = frame.shape[:2]

        results = self.model(
            frame,
            conf=self.confidence,
            verbose=False
        )

        result = results[0]

        detections = []

        if result.boxes is None:
            return detections

        for box in result.boxes:

            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()

            x1 = int(x1)
            y1 = int(y1)
            x2 = int(x2)
            y2 = int(y2)

            confidence = float(box.conf[0])

            box_width = x2 - x1
            box_height = y2 - y1

            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            area = box_width * box_height

            detection = {
                "label": "waste",
                "confidence": confidence,

                "x": center_x,
                "y": center_y,

                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2,

                "box_width": box_width,
                "box_height": box_height,
                "area": area,

                "frame_width": frame_width,
                "frame_height": frame_height,
            }

            detections.append(detection)

        return detections

    def get_best_target(self, detections):
        """
        Select one target for navigation.

        Current policy:
        highest-confidence detection.
        """

        if not detections:
            return None

        return max(
            detections,
            key=lambda d: d["confidence"]
        )

