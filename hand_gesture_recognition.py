import sys
sys.dont_write_bytecode = True

import cv2
import mediapipe as mp
import time
import ctypes

from gestures import recognize_gesture, GESTURE_TABLE


# ---------------------------------------------------------
# HAND-VISION
# AI-Based Hand Gesture Recognition System
# Syntecxhub Internship - Task 3
# ---------------------------------------------------------


# ---------------------------------------------------------
# MediaPipe Setup
# ---------------------------------------------------------

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


# ---------------------------------------------------------
# Camera Setup
# ---------------------------------------------------------

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("[ERROR] Could not access webcam.")
    exit()

print("HAND-VISION launched successfully.")
print("Webcam connected.\n")


# ---------------------------------------------------------
# MediaPipe Hand Model
# ---------------------------------------------------------

with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6
) as hands:

    help_mode = False

    # -----------------------------------------------------
    # Window
    # -----------------------------------------------------

    window_name = "HAND-VISION - Gesture Recognition"

    cv2.namedWindow(
        window_name,
        cv2.WINDOW_NORMAL
    )

    # -----------------------------------------------------
    # Set window to approximately 3/4 of the screen
    # and place it in the centre
    # -----------------------------------------------------

    screen_width = ctypes.windll.user32.GetSystemMetrics(0)
    screen_height = ctypes.windll.user32.GetSystemMetrics(1)

    window_width = int(screen_width * 0.80)
    window_height = int(screen_height * 0.80)

    window_x = (screen_width - window_width) // 2
    window_y = (screen_height - window_height) // 2 - 40

    cv2.resizeWindow(
        window_name,
        window_width,
        window_height
    )

    cv2.moveWindow(
        window_name,
        window_x,
        window_y
    )

    # -----------------------------------------------------
    # Main Loop
    # -----------------------------------------------------

    while cap.isOpened():

        success, frame = cap.read()

        if not success:
            print("[ERROR] Could not read webcam frame.")
            break

        # Mirror camera
        frame = cv2.flip(frame, 1)

        # Convert BGR -> RGB
        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # Process hand
        results = hands.process(rgb_frame)

        gesture_name = "NO HAND"
        action_name = "NONE"

        # -------------------------------------------------
        # Hand Detection
        # -------------------------------------------------

        if results.multi_hand_landmarks:

            hand_landmarks = results.multi_hand_landmarks[0]

            # Draw hand landmarks
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )

            # Recognize gesture
            gesture_name, action_name = recognize_gesture(
                hand_landmarks
            )

        # -------------------------------------------------
        # Frame Size
        # -------------------------------------------------

        height, width, _ = frame.shape

        # =================================================
        # HELP SCREEN
        # =================================================

        if help_mode:

            frame[:] = (22, 22, 22)

            # Header
            cv2.rectangle(
                frame,
                (0, 0),
                (width, 70),
                (35, 35, 35),
                -1
            )

            # Centered title
            title = "HAND-VISION  |  HELP"

            title_size = cv2.getTextSize(
                title,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                2
            )[0]

            title_x = (width - title_size[0]) // 2

            cv2.putText(
                frame,
                title,
                (title_x, 45),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

            # Table headings
            cv2.putText(
                frame,
                "GESTURE",
                (70, 110),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 0, 255),
                2
            )

            cv2.putText(
                frame,
                "ACTION",
                (330, 110),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 0, 255),
                2
            )

            # Gesture table
            y = 145

            for gesture_name_table, action_name_table in GESTURE_TABLE:

                cv2.putText(
                    frame,
                    gesture_name_table,
                    (70, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.48,
                    (240, 240, 240),
                    1
                )

                cv2.putText(
                    frame,
                    action_name_table,
                    (330, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.48,
                    (240, 240, 240),
                    1
                )

                y += 30

            # -------------------------------------------------
            # Help Controls Box
            # -------------------------------------------------

            control_width = 180
            control_height = 65

            control_x = width - control_width - 15
            control_y = height - control_height - 15

            # Box background
            cv2.rectangle(
                frame,
                (control_x, control_y),
                (control_x + control_width, control_y + control_height),
                (30, 30, 30),
                -1
            )

            # Box border
            cv2.rectangle(
                frame,
                (control_x, control_y),
                (control_x + control_width, control_y + control_height),
                (80, 80, 80),
                1
            )

            # H - Back to Camera
            cv2.putText(
                frame,
                "H - Back to Camera",
                (control_x + 12, control_y + 27),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                (0, 0, 255),
                1
            )

            # Q - Exit
            cv2.putText(
                frame,
                "Q - Exit",
                (control_x + 12, control_y + 52),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.48,
                (210, 210, 210),
                1
            )

        # =================================================
        # CAMERA SCREEN
        # =================================================

        else:

            # -------------------------------------------------
            # Header
            # -------------------------------------------------

            cv2.rectangle(
                frame,
                (0, 0),
                (width, 75),
                (25, 25, 25),
                -1
            )

            # Centered HAND-VISION title
            title = "HAND-VISION"

            title_size = cv2.getTextSize(
                title,
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                2
            )[0]

            title_x = (width - title_size[0]) // 2

            cv2.putText(
                frame,
                title,
                (title_x, 38),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (255, 255, 255),
                2
            )

            # Subtitle
            subtitle = "Real-Time Gesture Recognition"

            subtitle_size = cv2.getTextSize(
                subtitle,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                1
            )[0]

            subtitle_x = (width - subtitle_size[0]) // 2

            cv2.putText(
                frame,
                subtitle,
                (subtitle_x, 62),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                (180, 180, 180),
                1
            )

            # -------------------------------------------------
            # Smaller Information Panel
            # -------------------------------------------------

            panel_width = 285
            panel_height = 78

            panel_x = 15
            panel_y = height - panel_height - 15

            # Panel
            cv2.rectangle(
                frame,
                (panel_x, panel_y),
                (panel_x + panel_width, panel_y + panel_height),
                (30, 30, 30),
                -1
            )

            # Red accent
            cv2.rectangle(
                frame,
                (panel_x, panel_y),
                (panel_x + 4, panel_y + panel_height),
                (0, 0, 255),
                -1
            )

            # Gesture
            cv2.putText(
                frame,
                f"Gesture: {gesture_name}",
                (panel_x + 15, panel_y + 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.52,
                (255, 255, 255),
                1
            )

            # Action
            cv2.putText(
                frame,
                f"Action:  {action_name}",
                (panel_x + 15, panel_y + 57),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.52,
                (200, 200, 200),
                1
            )

            # -------------------------------------------------
            # Controls Box
            # -------------------------------------------------

            control_width = 150
            control_height = 65

            control_x = width - control_width - 15
            control_y = height - control_height - 15

            # Box background
            cv2.rectangle(
                frame,
                (control_x, control_y),
                (control_x + control_width, control_y + control_height),
                (30, 30, 30),
                -1
            )

            # Box border
            cv2.rectangle(
                frame,
                (control_x, control_y),
                (control_x + control_width, control_y + control_height),
                (80, 80, 80),
                1
            )

            # H - Help
            cv2.putText(
                frame,
                "H - Help",
                (control_x + 15, control_y + 27),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.48,
                (0, 0, 255),
                1
            )

            # Q - Exit
            cv2.putText(
                frame,
                "Q - Exit",
                (control_x + 15, control_y + 52),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.48,
                (210, 210, 210),
                1
            )

        # -------------------------------------------------
        # Display
        # -------------------------------------------------

        cv2.imshow(
            window_name,
            frame
        )

        # -------------------------------------------------
        # Keyboard Controls
        # -------------------------------------------------

        key = cv2.waitKey(1) & 0xFF

        # Q = Exit
        if key == ord("q"):

            print("\nHAND-VISION closed successfully.")
            break

        # H = Toggle Help
        elif key == ord("h"):

            help_mode = not help_mode


# ---------------------------------------------------------
# Cleanup
# ---------------------------------------------------------

cap.release()
cv2.destroyAllWindows()