import cv2
import serial
import time
from ultralytics import YOLO

# --- CONFIGURATION ZONE ---
COM_PORT = 'COM8'
BAUD_RATE = 9600
MODEL_PATH = r'D:\Weera\runs\detect\Weed_Robot\model_v1\weights\best.pt'

# Servo Tuning (Adjust these after testing if the robot aims too far or too short)
# Assuming 90 is center. We limit movement to avoid breaking the physical frame.
PAN_MIN, PAN_MAX = 45, 135  # X-Axis servo range
TILT_MIN, TILT_MAX = 45, 135  # Y-Axis servo range


# --------------------------

def map_range(value, in_min, in_max, out_min, out_max):
    """Translates a pixel coordinate into a servo degree angle."""
    # Ensure value doesn't go out of bounds
    value = max(min(value, in_max), in_min)
    mapped_val = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    return int(mapped_val)


def main():
    print(f"Connecting to Arduino on {COM_PORT}...")
    try:
        arduino = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # Give Arduino 2 seconds to reboot after serial connection
        print("Arduino Connected!")
    except Exception as e:
        print(f"FAILED to connect to Arduino: {e}")
        print("Make sure the Arduino IDE Serial Monitor is CLOSED.")
        return

    print("Loading AI Model...")
    model = YOLO(MODEL_PATH)
    cap = cv2.VideoCapture(0)

    last_spray_time = 0
    COOLDOWN_PERIOD = 2.0  # Wait 2 seconds after spraying before moving again

    print("System Armed. Press 'q' to quit.")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        # Get frame dimensions (Standard is usually 640 width, 480 height)
        height, width, _ = frame.shape

        results = model(frame, conf=0.5)  # Increased confidence to 50% to prevent false fires
        annotated_frame = results[0].plot()

        current_time = time.time()
        weed_targeted_this_frame = False

        for result in results:
            boxes = result.boxes
            if len(boxes) > 0 and not weed_targeted_this_frame:

                # Check if system is ready to fire again
                if (current_time - last_spray_time) > COOLDOWN_PERIOD:
                    # Target the first weed in the list
                    box = boxes[0]
                    x1, y1, x2, y2 = box.xyxy[0].int().tolist()

                    # Calculate center pixel of the weed
                    cx = int((x1 + x2) / 2)
                    cy = int((y1 + y2) / 2)

                    # MAP PIXELS TO ANGLES
                    # Width (0-640) maps to Pan Servo
                    pan_angle = map_range(cx, 0, width, PAN_MIN, PAN_MAX)

                    # Height (0-480) maps to Tilt Servo
                    # Note: You might need to swap TILT_MIN and TILT_MAX here if your
                    # tilt servo moves "up" when it should move "down".
                    tilt_angle = map_range(cy, 0, height, TILT_MIN, TILT_MAX)

                    print(f"Weed Detected! Pixels:({cx},{cy}) -> Servos: Pan={pan_angle}°, Tilt={tilt_angle}°")

                    # Format command and send to Arduino: <X,Y,SPRAY>
                    command = f"<{pan_angle},{tilt_angle},1>\n"
                    arduino.write(command.encode('utf-8'))

                    # Update state
                    last_spray_time = time.time()
                    weed_targeted_this_frame = True

                    # Draw a red crosshair on the target being actively sprayed
                    cv2.drawMarker(annotated_frame, (cx, cy), (0, 0, 255), cv2.MARKER_CROSS, 20, 3)

        cv2.imshow("Turret Targeting System", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Safely shut down
    cap.release()
    cv2.destroyAllWindows()
    # Send a command to return to center and turn off pump before closing
    arduino.write("<90,90,0>\n".encode('utf-8'))
    arduino.close()


if __name__ == '__main__':
    main()