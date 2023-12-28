from collections import defaultdict

import pandas as pd
from evaluate_models import convert_and_eval_model

if __name__ == "__main__":
    models_paths = [
        "yolov8n.pt",
        "yolov8s.pt",
        "yolov8m.pt",
        "yolov8l.pt",
        "yolov8x.pt",
    ]
    models_names = [
        "yolov8n_640",
        "yolov8s_640",
        "yolov8m_640",
        "yolov8l_640",
        "yolov8x_640",
    ]
    dataset_yaml_path = "coco.yaml"
    device = "cpu"
    report_path = "reports/report_coco_yolos_640.csv"

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
