from collections import defaultdict

import pandas as pd
from evaluate_models import convert_and_eval_model

if __name__ == "__main__":
    model_path = "yolov8s.pt"
    model_name = "yolov8s_640"
    dataset_yaml_path = "coco.yaml"
    device = "cpu"
    report_path = "reports/report_coco_yolov8s_640.csv"

    # openvino не поддерживает simplify
    cfg = [
        {"format": "torch", "simplify": False, "half": False},
        {"format": "openvino", "simplify": False, "half": False},
        {"format": "openvino", "simplify": False, "half": True},
        {"format": "onnx", "simplify": False, "half": False},
        {"format": "onnx", "simplify": True, "half": False},
        {"format": "onnx", "simplify": True, "half": True},
    ]

    report_table = defaultdict(list)

    # оценка модели
    for row in cfg:
        report_table = convert_and_eval_model(
            model_path, model_name, dataset_yaml_path, device, report_table, **row
        )

    report_table = pd.DataFrame.from_dict(report_table)
    report_table.to_csv(report_path)
