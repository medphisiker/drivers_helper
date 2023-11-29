import json
import yaml
from data_utils import read_json


if __name__ == "__main__":
    input_rtsd_json_labels_path = "./data/label_map.json"
    output_yolo_yaml_path = "./data/yolo/dataset.yaml"

    label_to_num_mapping = read_json(input_rtsd_json_labels_path)

    # создаем словарь для yaml опысывающего датасет в формате
    # YOLO-Ultralytics
    # (https://openvinotoolkit.github.io/datumaro/stable/docs/data-formats/formats/yolo_ultralytics.html)
    yolo_yaml = {}
    yolo_yaml["train"] = "./images/train"
    yolo_yaml["val"] = "./images/val"
    yolo_yaml["names"] = {}
    for val, key in enumerate(label_to_num_mapping):
        yolo_yaml["names"].update({val: key})

    # записываем словарь в yaml-файлF
    yaml_string = yaml.dump(yolo_yaml)
    with open(output_yolo_yaml_path, "w") as file:
        file.write(yaml_string)
