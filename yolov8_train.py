from ultralytics import YOLO

model = YOLO("yolov8s.pt")

res = model.train(
    data="data/yolo/dataset.yaml",
    epochs=80,
    batch=64,
    workers=12,
    patience=5,
    save_period=2,
    seed=20,
    imgsz=640,
)
