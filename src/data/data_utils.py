import os

import cv2
import yaml


def read_classes_txt(classes_txt_path):
    with open(classes_txt_path, "r") as file:
        classes = []
        for line in file:
            classes.append(line.strip())

    return classes


def zip_directory(folder_path, zip_file):
    for folder_name, subfolders, filenames in os.walk(folder_path):
        for filename in filenames:
            # Create complete filepath of file in directory
            file_path = os.path.join(folder_name, filename)
            # Add file to zip
            zip_file.write(file_path)


def list_files(directory_path):
    files = []
    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)
        if os.path.isfile(file_path):
            files.append(file_path)
        elif os.path.isdir(file_path):
            files.extend(list_files(file_path))
    return files


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
