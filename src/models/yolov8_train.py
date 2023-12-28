from ultralytics import YOLO

model = YOLO("yolov8n.pt")

res = model.train(
    data="data/processed/RSTD_filtered_yolov5/dataset.yaml",
    epochs=20,
    batch=32,
    workers=12,
    patience=5,
    seed=20,
    imgsz=1024,
    project="models/models",
)
