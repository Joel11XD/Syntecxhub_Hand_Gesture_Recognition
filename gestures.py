import sys
sys.dont_write_bytecode = False

import math


# ---------------------------------------------------------
# Gesture Table
# ---------------------------------------------------------

GESTURE_TABLE = [
    ("FIST", "STOP"),
    ("OPEN PALM", "PAUSE"),
    ("THUMBS UP", "APPROVE"),
    ("THUMBS DOWN", "REJECT"),
    ("POINT UP", "UP"),
    ("POINT DOWN", "DOWN"),
    ("POINT LEFT", "LEFT"),
    ("POINT RIGHT", "RIGHT"),
    ("VICTORY", "PLAY"),
    ("ROCK", "ROCK")
]


# ---------------------------------------------------------
# Basic Geometry
# ---------------------------------------------------------

def distance(p1, p2):
    return math.sqrt(
        (p1.x - p2.x) ** 2 +
        (p1.y - p2.y) ** 2 +
        (p1.z - p2.z) ** 2
    )


def angle(a, b, c):
    """
    Returns the angle ABC in degrees.
    """

    ba = (
        a.x - b.x,
        a.y - b.y,
        a.z - b.z
    )

    bc = (
        c.x - b.x,
        c.y - b.y,
        c.z - b.z
    )

    dot_product = (
        ba[0] * bc[0] +
        ba[1] * bc[1] +
        ba[2] * bc[2]
    )

    magnitude_ba = math.sqrt(
        ba[0] ** 2 +
        ba[1] ** 2 +
        ba[2] ** 2
    )

    magnitude_bc = math.sqrt(
        bc[0] ** 2 +
        bc[1] ** 2 +
        bc[2] ** 2
    )

    if magnitude_ba == 0 or magnitude_bc == 0:
        return 0

    cosine = dot_product / (
        magnitude_ba * magnitude_bc
    )

    cosine = max(-1.0, min(1.0, cosine))

    return math.degrees(
        math.acos(cosine)
    )


# ---------------------------------------------------------
# Palm Size
# ---------------------------------------------------------

def get_palm_size(landmarks):

    wrist = landmarks[0]
    middle_mcp = landmarks[9]

    return distance(
        wrist,
        middle_mcp
    )


# ---------------------------------------------------------
# Finger Extension Detection
# ---------------------------------------------------------

def is_finger_extended(
        landmarks,
        mcp_index,
        pip_index,
        dip_index,
        tip_index
):

    mcp = landmarks[mcp_index]
    pip = landmarks[pip_index]
    dip = landmarks[dip_index]
    tip = landmarks[tip_index]

    # Joint angles
    pip_angle = angle(
        mcp,
        pip,
        dip
    )

    dip_angle = angle(
        pip,
        dip,
        tip
    )

    # Finger length
    finger_length = (
        distance(mcp, pip) +
        distance(pip, dip) +
        distance(dip, tip)
    )

    # Direct MCP → tip distance
    straight_distance = distance(
        mcp,
        tip
    )

    # A straight finger has a much larger
    # direct distance compared with a curled finger.
    straightness = (
        straight_distance / finger_length
        if finger_length > 0
        else 0
    )

    # Strong extension requirements
    return (
        pip_angle > 150 and
        dip_angle > 145 and
        straightness > 0.72
    )


# ---------------------------------------------------------
# Thumb Detection
# ---------------------------------------------------------

def is_thumb_extended(landmarks):

    thumb_cmc = landmarks[1]
    thumb_mcp = landmarks[2]
    thumb_ip = landmarks[3]
    thumb_tip = landmarks[4]

    wrist = landmarks[0]

    thumb_angle_1 = angle(
        thumb_cmc,
        thumb_mcp,
        thumb_ip
    )

    thumb_angle_2 = angle(
        thumb_mcp,
        thumb_ip,
        thumb_tip
    )

    thumb_length = (
        distance(thumb_cmc, thumb_mcp) +
        distance(thumb_mcp, thumb_ip) +
        distance(thumb_ip, thumb_tip)
    )

    direct_distance = distance(
        thumb_cmc,
        thumb_tip
    )

    straightness = (
        direct_distance / thumb_length
        if thumb_length > 0
        else 0
    )

    # Thumb should be relatively straight
    # and extended away from the wrist.
    return (
        thumb_angle_1 > 135 and
        thumb_angle_2 > 145 and
        straightness > 0.65 and
        distance(thumb_tip, wrist)
        > distance(thumb_ip, wrist) * 1.10
    )


# ---------------------------------------------------------
# Finger State Detection
# ---------------------------------------------------------

def get_finger_states(landmarks):

    thumb = is_thumb_extended(
        landmarks
    )

    index = is_finger_extended(
        landmarks,
        5, 6, 7, 8
    )

    middle = is_finger_extended(
        landmarks,
        9, 10, 11, 12
    )

    ring = is_finger_extended(
        landmarks,
        13, 14, 15, 16
    )

    pinky = is_finger_extended(
        landmarks,
        17, 18, 19, 20
    )

    return [
        int(thumb),
        int(index),
        int(middle),
        int(ring),
        int(pinky)
    ]


# ---------------------------------------------------------
# Alternative Finger Curl Check
# ---------------------------------------------------------

def finger_tip_to_palm_ratio(
        landmarks,
        tip_index
):

    wrist = landmarks[0]
    palm_center = landmarks[9]
    tip = landmarks[tip_index]

    palm_size = distance(
        wrist,
        palm_center
    )

    if palm_size == 0:
        return 0

    return distance(
        tip,
        palm_center
    ) / palm_size


# ---------------------------------------------------------
# Direction Detection
# ---------------------------------------------------------

def get_pointing_direction(landmarks):

    index_mcp = landmarks[5]
    index_pip = landmarks[6]
    index_tip = landmarks[8]

    dx = index_tip.x - index_mcp.x
    dy = index_tip.y - index_mcp.y

    # Check actual finger length.
    finger_length = math.sqrt(
        dx ** 2 +
        dy ** 2
    )

    if finger_length < 0.08:
        return None

    # Make sure the index is reasonably straight.
    index_angle = angle(
        index_mcp,
        index_pip,
        index_tip
    )

    if index_angle < 140:
        return None

    # Vertical directions
    if abs(dy) > abs(dx) * 1.10:

        if dy < -0.04:
            return "UP"

        if dy > 0.04:
            return "DOWN"

    # Horizontal directions
    elif abs(dx) > abs(dy) * 1.10:

        if dx > 0.04:
            return "RIGHT"

        if dx < -0.04:
            return "LEFT"

    return None


# ---------------------------------------------------------
# Gesture Recognition
# ---------------------------------------------------------

def recognize_gesture(hand_landmarks):

    landmarks = hand_landmarks.landmark

    fingers = get_finger_states(
        landmarks
    )

    thumb = fingers[0]
    index = fingers[1]
    middle = fingers[2]
    ring = fingers[3]
    pinky = fingers[4]


    # =====================================================
    # FIST
    # =====================================================

    if (
        thumb == 0 and
        index == 0 and
        middle == 0 and
        ring == 0 and
        pinky == 0
    ):

        return "FIST", "STOP"


    # =====================================================
    # THUMBS UP / THUMBS DOWN
    # Thumb ONLY
    # =====================================================

    if (
        thumb == 1 and
        index == 0 and
        middle == 0 and
        ring == 0 and
        pinky == 0
    ):

        thumb_tip = landmarks[4]
        index_mcp = landmarks[5]

        # THUMBS UP
        if thumb_tip.y < index_mcp.y - 0.03:
            return "THUMBS UP", "APPROVE"

        # THUMBS DOWN
        if thumb_tip.y > index_mcp.y + 0.03:
            return "THUMBS DOWN", "REJECT"


    # =====================================================
    # OPEN PALM
    # Works for palm side and back side of the hand
    # =====================================================

    if (
        index == 1 and
        middle == 1 and
        ring == 1 and
        pinky == 1
    ):

        palm_size = get_palm_size(landmarks)

        if palm_size > 0:

            # Check that the four fingers are clearly
            # separated from the palm.
            index_distance = distance(
                landmarks[8],
                landmarks[9]
            )

            middle_distance = distance(
                landmarks[12],
                landmarks[9]
            )

            ring_distance = distance(
                landmarks[16],
                landmarks[9]
            )

            pinky_distance = distance(
                landmarks[20],
                landmarks[9]
            )

            # Average distance of the four fingers
            average_distance = (
                index_distance +
                middle_distance +
                ring_distance +
                pinky_distance
            ) / 4

            # Thumb distance from the palm
            thumb_distance = distance(
                landmarks[4],
                landmarks[9]
            )

            # Open palm:
            # - four fingers are extended
            # - thumb is either detected as extended
            #   OR physically away from the palm
            if (
                average_distance > palm_size * 0.90 and
                (
                    thumb == 1 or
                    thumb_distance > palm_size * 0.70
                )
            ):

                return "OPEN PALM", "PAUSE"


    # VICTORY
    # Index + Middle only
    # =====================================================

    if (
        index == 1 and
        middle == 1 and
        ring == 0 and
        pinky == 0
    ):

        return "VICTORY", "PLAY"


    # =====================================================
    # ROCK
    # Index + Pinky only
    # =====================================================

    if (
        index == 1 and
        middle == 0 and
        ring == 0 and
        pinky == 1
    ):

        return "ROCK", "ROCK"


    # =====================================================
    # POINTING
    # ONLY INDEX EXTENDED
    # =====================================================

    if (
        index == 1 and
        middle == 0 and
        ring == 0 and
        pinky == 0
    ):

        direction = get_pointing_direction(
            landmarks
        )

        if direction == "UP":
            return "POINT UP", "UP"

        if direction == "DOWN":
            return "POINT DOWN", "DOWN"

        if direction == "LEFT":
            return "POINT LEFT", "LEFT"

        if direction == "RIGHT":
            return "POINT RIGHT", "RIGHT"


    # =====================================================
    # UNKNOWN
    # =====================================================

    return "UNKNOWN", "NONE"