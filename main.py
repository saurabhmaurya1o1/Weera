import cv2
from ultralytics import YOLO


def main():

    model_path = r'D:\Weera\runs\detect\Weed_Robot\model_v1\weights\best.pt'
    print("Loading AI Model...")
    model = YOLO(model_path)
    print("Model Loaded Successfully!")
    
    cap = cv2.VideoCapture(0)

    print("Opening webcam. Press 'q' inside the video window to quit.")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Failed to grab frame from webcam.")
            break

        results = model(frame, conf=0.4)

        # 4. Extract data and calculate center (cx, cy)
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Get the bounding box coordinates
                x1, y1, x2, y2 = box.xyxy[0].int().tolist()

                # Calculate the exact center point for the water pump to aim at
                cx = int((x1 + x2) / 2)
                cy = int((y1 + y2) / 2)

                # Print the targeting coordinates to the terminal
                # box.cls[0] gets the class ID (0-15) of the weed
                weed_id = int(box.cls[0])
                print(f"Target Acquired! Weed ID: {weed_id} | Aiming at X: {cx}, Y: {cy}")

        # 5. Visualize the results on screen (draws boxes and labels)
        annotated_frame = results[0].plot()

        # Draw a targeting crosshair at the center of the screen (optional, for aesthetics)
        height, width, _ = annotated_frame.shape
        cv2.line(annotated_frame, (int(width / 2) - 20, int(height / 2)), (int(width / 2) + 20, int(height / 2)),
                 (0, 255, 0), 2)
        cv2.line(annotated_frame, (int(width / 2), int(height / 2) - 20), (int(width / 2), int(height / 2) + 20),
                 (0, 255, 0), 2)

        # 6. Show the video feed
        cv2.imshow("Weed Detection Robot - Live Targeting System", annotated_frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()