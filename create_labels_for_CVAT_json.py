import json
from data_utils import read_classes_txt


if __name__ == "__main__":
    classes_txt_path = "include_classes.txt"
    output_cvat_json_path = "data/RTSD_train_cvat_filtered/labels.json"

    include_classes = read_classes_txt(classes_txt_path)

    # создаем словарь для CVAT опысывающего классы
    cvat_json = []
    for class_name in include_classes:
        cvat_json.append({"name": class_name, "attributes": []})

    # записываем словарь в json-файл
    with open(output_cvat_json_path, "w") as file:
        json.dump(cvat_json, file, indent=4)
