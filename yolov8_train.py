from ultralytics import YOLO

model = YOLO("yolov8s.pt")

res = model.train(
    data="data/RSTD_filtered_yolov5/dataset.yaml",
    epochs=20,
    batch=32,
    workers=12,
    patience=5,
    save_period=2,
    seed=20,
    imgsz=640,
)
