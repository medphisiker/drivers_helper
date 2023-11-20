import json


if __name__ == "__main__":
    include_classes = (
        "5_19_1",
        "2_1",
        "5_16",
        "5_15_2",
        "3_24",
        "2_4",
        "3_27",
        "1_23",
        "4_1_1",
        "5_20",
        "3_20",
        "5_15_3",
        "5_15_1",
        "5_15_2_2",
        "1_17",
        "4_2_3",
        "5_15_5",
        "4_2_1",
        "4_1_4",
        "7_3",
        "6_4",
        "6_16",
        "5_5",
        "1_25",
        "8_2_1",
        "2_3_2",
        "3_1",
    )
    output_cvat_json_path = "./data/RTSD_val_cvat_filtered/labels.json"

    # создаем словарь для CVAT опысывающего классы
    cvat_json = []
    for class_name in include_classes:
        cvat_json.append({"name": class_name, "attributes": []})

    # записываем словарь в json-файл
    with open(output_cvat_json_path, "w") as file:
        json.dump(cvat_json, file, indent=4)
