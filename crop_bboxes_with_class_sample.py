import os

import cv2
import yaml

from data_utils import list_files


# Open the file
def read_yaml(yaml_file_path):
    with open(yaml_file_path, "r") as stream:
        # Convert YAML document to Python object
        data = yaml.safe_load(stream)

    return data


def parse_labels(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    boxes = []
    for line in lines:
        parts = line.strip().split()
        class_id = int(parts[0])
        x_center = float(parts[1])
        y_center = float(parts[2])
        width = float(parts[3])
        height = float(parts[4])
        boxes.append((class_id, x_center, y_center, width, height))

    return boxes


def crop_boxes(image_path, boxes):
    image = cv2.imread(image_path)
    cropped_images = []
    for box in boxes:
        class_id, x_center, y_center, width, height = box
        x_center *= image.shape[1]
        y_center *= image.shape[0]
        width *= image.shape[1]
        height *= image.shape[0]
        x_start = int(x_center - width / 2)
        y_start = int(y_center - height / 2)
        cropped_image = image[
            y_start : y_start + int(height), x_start : x_start + int(width)
        ]
        cropped_images.append(cropped_image)

    return cropped_images


def create_dir(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


if __name__ == "__main__":
    yaml_file_path = "data/RSTD_filtered_yolov5/dataset.yaml"
    images_dir_path = "data/RSTD_filtered_yolov5/images/train"
    output_dir = "data/crop_output"
    count_value = 20

    classes = read_yaml(yaml_file_path)["names"]

    # создаем выходную папку для кропов классов
    classes_dir_paths = {}

    create_dir(output_dir)
    for num in classes:
        class_dir_path = os.path.join(output_dir, classes[num])
        create_dir(class_dir_path)
        classes_dir_paths[num] = class_dir_path

    # создаем счетчик ббоксов на каждый класс
    classes_count = [0] * len(classes)

    images_paths = list_files(images_dir_path)

    for image_path in images_paths:
        label_txt_path = image_path.split(os.sep + "images" + os.sep)
        label_txt_path = f"{os.sep}labels{os.sep}".join(label_txt_path)
        label_txt_path = os.path.splitext(label_txt_path)[0] + ".txt"

        boxes = parse_labels(label_txt_path)
        cropped_images = crop_boxes(image_path, boxes)
        for bbox, cropped_image in zip(boxes, cropped_images):
            class_id = bbox[0]
            if classes_count[class_id] < count_value:
                classes_count[class_id] += 1
                crop_filename = f"{classes[class_id]}_cnt_{classes_count[class_id]}.jpg"
                crop_path = os.path.join(classes_dir_paths[class_id], crop_filename)
                cv2.imwrite(crop_path, cropped_image)

        if sum(classes_count) == count_value * len(classes_count):
            print("Нужное количество crop'ов набрано")
            break

    print("Обработка завершена")
