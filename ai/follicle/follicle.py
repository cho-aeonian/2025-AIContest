import cv2
from ultralytics import YOLO
import tkinter as tk
from PIL import Image, ImageTk

model = YOLO('follicle.pt')
cap = cv2.VideoCapture("follicle.mp4")

fps = cap.get(cv2.CAP_PROP_FPS)
frame_delay = int(1000 / fps) if fps > 0 else 200

root = tk.Tk()
root.title("Follicle GUI")
root.geometry("800x480")

frame_top = tk.Frame(root)
frame_top.pack()

camera_label = tk.Label(frame_top)
camera_label.grid(row=0, column=0, padx=5, pady=5)

capture_label = tk.Label(frame_top)
capture_label.grid(row=0, column=1, padx=5, pady=5)

box_count_label = tk.Label(root, text="follicle count:", font=("Arial", 10))
box_count_label.pack(pady=5)

capture_button = tk.Button(root, text="capture", command=lambda: capture_frame(), font=("Arial", 10), width=10, height=2)
capture_button.pack(pady=5)

IMG_WIDTH = 380
IMG_HEIGHT = 210
captured_image = None
last_frame = None

def update_frame():
    global last_frame
    
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        root.after(frame_delay, update_frame)
        return

    frame_resized = cv2.resize(frame, (IMG_WIDTH, IMG_HEIGHT))
    last_frame = frame_resized.copy()

    img = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=img)
    camera_label.imgtk = imgtk
    camera_label.configure(image=imgtk)

    root.after(frame_delay, update_frame)

def capture_frame():
    global captured_image, last_frame
    
    if last_frame is None:
        return

    results = model(last_frame)
    num_boxes = sum(len(result.boxes) for result in results)

    box_count_label.config(text=f"follicle-count: {num_boxes}")

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cls_id = int(box.cls.item())  
            label = model.names.get(cls_id, "Unknown")
            confidence = box.conf.item()

            if label == "Unknown":
                continue

            cv2.rectangle(last_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(last_frame, f'{label} {confidence:.2f}', (x1, y1 - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    img = cv2.cvtColor(last_frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=img)
    capture_label.imgtk = imgtk
    capture_label.configure(image=imgtk)
    captured_image = img

update_frame()
root.mainloop()
