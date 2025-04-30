import serial
import time
import cv2
from ultralytics import YOLO

ser = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)

model = YOLO('marketpig.pt')

cap = cv2.VideoCapture(0)

last_detection_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    current_time = time.time()

    if current_time - last_detection_time >= 5:
        results = model(frame)

        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                width = x2 - x1
                height = y2 - y1
                confidence = box.conf

                if width > 350 or height > 350:
                    class_name = 'market-pig'
                    ser.write(b'S')
                else:
                    class_name = 'growing-pig'
                    ser.write(b'I')

                label = f"{class_name} {confidence.item():.2f}"
                print(f"Detected: {class_name} (W: {width}, H: {height}, Conf: {confidence.item():.2f})")

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                            0.6, (0, 255, 0), 2)

            last_detection_time = current_time

    cv2.imshow("Camera View", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(1)

cap.release()
cv2.destroyAllWindows()
