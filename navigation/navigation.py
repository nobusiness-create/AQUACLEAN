import math


class Navigator:
    """
    Navigation logic for a forward-facing camera.

    The camera is mounted on the robot and looks forward.

    Output:
        state
        steering  -> -1.0 (left) to +1.0 (right)
        forward   -> 0.0 to 1.0
        target    -> currently selected waste
    """

    def __init__(
        self,
        deadband=0.08,
        lock_distance=0.18,
        max_lost_frames=8,
        collection_area=18000,
        collection_y_ratio=0.78,
    ):
        self.deadband = deadband
        self.lock_distance = lock_distance
        self.max_lost_frames = max_lost_frames

        # Temporary values.
        # These must be calibrated with the real robot.
        self.collection_area = collection_area
        self.collection_y_ratio = collection_y_ratio

        self.locked_target = None
        self.lost_frames = 0

    # ---------------------------------------------------------
    # TARGET SELECTION
    # ---------------------------------------------------------

    def choose_target(self, detections):
        """
        Select a target and maintain target lock.

        If a previous target is still visible nearby,
        keep following it.

        Otherwise choose the best new target.
        """

        if not detections:
            self.lost_frames += 1

            if self.lost_frames > self.max_lost_frames:
                self.locked_target = None

            return self.locked_target

        self.lost_frames = 0

        # If we already have a target, try to keep it.
        if self.locked_target is not None:

            previous_x = self.locked_target["x"]
            previous_y = self.locked_target["y"]

            frame_width = detections[0]["frame_width"]
            frame_height = detections[0]["frame_height"]

            best_match = None
            best_distance = float("inf")

            for detection in detections:

                dx = (
                    detection["x"] - previous_x
                ) / frame_width

                dy = (
                    detection["y"] - previous_y
                ) / frame_height

                distance = math.sqrt(
                    dx * dx + dy * dy
                )

                if distance < best_distance:
                    best_distance = distance
                    best_match = detection

            # Keep the existing target if it has not moved
            # too far between consecutive frames.
            if (
                best_match is not None
                and best_distance <= self.lock_distance
            ):
                self.locked_target = best_match
                return best_match

        # No valid lock -> choose a new target.
        target = self._select_new_target(detections)

        self.locked_target = target

        return target

    def _select_new_target(self, detections):
        """
        Choose a new target.

        Preference:
        1. Near the center of the forward view
        2. Higher confidence
        3. Larger apparent size
        """

        if not detections:
            return None

        frame_width = detections[0]["frame_width"]
        frame_height = detections[0]["frame_height"]

        best_target = None
        best_score = -1

        max_area = frame_width * frame_height

        for detection in detections:

            # -------------------------------------------------
            # CENTER SCORE
            # -------------------------------------------------

            normalized_x = (
                detection["x"] / frame_width
            )

            center_error = abs(
                normalized_x - 0.5
            )

            center_score = 1.0 - min(
                center_error * 2.0,
                1.0
            )

            # -------------------------------------------------
            # CONFIDENCE SCORE
            # -------------------------------------------------

            confidence_score = detection["confidence"]

            # -------------------------------------------------
            # SIZE SCORE
            # -------------------------------------------------

            area_ratio = (
                detection["area"] / max_area
            )

            # Keep this contribution small.
            size_score = min(
                area_ratio * 8.0,
                1.0
            )

            # -------------------------------------------------
            # TOTAL SCORE
            # -------------------------------------------------

            score = (
                0.50 * center_score
                + 0.35 * confidence_score
                + 0.15 * size_score
            )

            if score > best_score:
                best_score = score
                best_target = detection

        return best_target

    # ---------------------------------------------------------
    # MOVEMENT DECISION
    # ---------------------------------------------------------

    def decide(self, target):
        """
        Convert selected target into navigation data.
        """

        if target is None:

            return {
                "state": "SEARCH",
                "steering": 0.0,
                "forward": 0.0,
                "target": None,
            }

        frame_width = target["frame_width"]
        frame_height = target["frame_height"]

        target_x = target["x"]
        target_y = target["y"]

        # ---------------------------------------------
        # HORIZONTAL STEERING ERROR
        # ---------------------------------------------

        center_x = frame_width / 2

        steering = (
            target_x - center_x
        ) / center_x

        steering = max(
            -1.0,
            min(1.0, steering)
        )

        # Small deadband
        if abs(steering) < self.deadband:
            steering = 0.0

        # ---------------------------------------------
        # APPROACH / COLLECTION
        # ---------------------------------------------

        y_ratio = target_y / frame_height

        collection_ready = (
            target["area"] >= self.collection_area
            and y_ratio >= self.collection_y_ratio
            and steering == 0.0
        )

        if collection_ready:

            return {
                "state": "COLLECT",
                "steering": 0.0,
                "forward": 0.0,
                "target": target,
            }

        # ---------------------------------------------
        # FORWARD SPEED
        # ---------------------------------------------

        image_area = (
            frame_width * frame_height
        )

        area_ratio = (
            target["area"] / image_area
        )

        if area_ratio > 0.12:
            forward = 0.20

        elif area_ratio > 0.06:
            forward = 0.35

        else:
            forward = 0.60

        return {
            "state": "APPROACH",
            "steering": steering,
            "forward": forward,
            "target": target,
        }
