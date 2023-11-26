import os

import cv2

import data_utils as utils

if __name__ == "__main__":
    yaml_file_path = "data/RSTD_filtered_yolov5/dataset.yaml"
    images_dir_path = "data/RSTD_filtered_yolov5/images/train"
    output_dir = "data/crop_output"
    count_value = 20

    classes = utils.read_yaml(yaml_file_path)["names"]

    # создаем выходную папку для кропов классов
    classes_dir_paths = {}

    utils.create_dir(output_dir)
    for num in classes:
        class_dir_path = os.path.join(output_dir, f"{num}-{classes[num]}")
        utils.create_dir(class_dir_path)
        classes_dir_paths[num] = class_dir_path

    # создаем счетчик ббоксов на каждый класс
    classes_count = [0] * len(classes)

    images_paths = utils.list_files(images_dir_path)

    for image_path in images_paths:
        label_txt_path = image_path.split(os.sep + "images" + os.sep)
        label_txt_path = f"{os.sep}labels{os.sep}".join(label_txt_path)
        label_txt_path = os.path.splitext(label_txt_path)[0] + ".txt"

        boxes = utils.parse_labels(label_txt_path)
        cropped_images = utils.crop_boxes(image_path, boxes)
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
