import cv2
import os
from ultralytics import YOLO, solutions

model = YOLO("yolov8n.pt")
names = model.model.names

cap = cv2.VideoCapture("vid/cars.mp4")
assert cap.isOpened(), "Error reading video file"
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

# Video writer
video_writer = cv2.VideoWriter("speed_estimation.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

line_pts = [(0, h//2), (w, h//2)]

# Init speed-estimation obj
speed_obj = solutions.SpeedEstimator(
    reg_pts=[(0, h//2), (w, h//2)],
    names=names,
    view_img=True,
    line_thickness = 1,
    region_thickness = 1,
    
)


while cap.isOpened():
    success, im0 = cap.read()
    if not success:
        print("video processing has been successfully completed.")
        break

    tracks = model.track(im0, persist=True, show=False)

    im0 = speed_obj.estimate_speed(im0, tracks)
   
    video_writer.write(im0)

cap.release()
video_writer.release()
cv2.destroyAllWindows()