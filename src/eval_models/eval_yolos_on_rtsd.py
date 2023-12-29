from collections import defaultdict

import pandas as pd
from evaluate_models import convert_and_eval_model

if __name__ == "__main__":
    models_paths = [
        "models/models/yolov8n_1024/weights/best.pt",
        "models/models/yolov8n_640/weights/last.pt",
        "models/models/yolov8s_640/weights/best.pt",
    ]
    models_names = [
        "yolov8n_1024",
        "yolov8n_640",
        "yolov8s_640",
    ]
    dataset_yaml_path = "data/processed/RSTD_filtered_yolov5/dataset.yaml"
    device = "cpu"
    report_path = "reports/report_rtsd_yolos.csv"

    # openvino не поддерживает simplify
    # у onnx и у openvino half пока не имеет смысла
    cfg = [
        {"format": "torch", "simplify": False, "half": False},
        {"format": "openvino", "simplify": False, "half": False},
        {"format": "onnx", "simplify": False, "half": False},
        {"format": "onnx", "simplify": True, "half": False},
    ]

    report_table = defaultdict(list)

    for model_path, model_name in zip(models_paths, models_names):
        # оценка модели
        for row in cfg:
            report_table = convert_and_eval_model(
                model_path, model_name, dataset_yaml_path, device, report_table, **row
            )

    report_table = pd.DataFrame.from_dict(report_table)
    report_table.to_csv(report_path)
