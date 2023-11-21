import json


def read_json(filename: str):
    with open(filename) as f_in:
        dct_data = json.load(f_in)

    return dct_data


if __name__ == "__main__":
    input_rtsd_json_labels_path = "data/RTSD/label_map.json"
    output_cvat_json_path = "data/RSTD_cvat_val/label.json"

    label_to_num_mapping = read_json(input_rtsd_json_labels_path)

    # создаем словарь для CVAT опысывающего классы
    cvat_json = []
    for val, key in enumerate(label_to_num_mapping):
        cvat_json.append({"name": key, "attributes": []})

    # записываем словарь в json-файл
    with open(output_cvat_json_path, "w") as file:
        json.dump(cvat_json, file, indent=4)
