import cv2
import os
import matplotlib.pyplot as plt

import data_utils as utils
from data_utils import list_files

if __name__ == "__main__":
    crop_dir_path = "data/crop_output"
    yaml_file_path = "data/RSTD_filtered_yolov5/dataset.yaml"
    class_samples_num = 20

    # получаем пути к картинкам
    classes = utils.read_yaml(yaml_file_path)["names"]
    classes_dir_paths = {}
    for num in classes:
        class_dir_path = os.path.join(crop_dir_path, f"{num}-{classes[num]}")
        classes_dir_paths[num] = class_dir_path

    # считываем примеры кропов классов
    images = []
    for num in classes:
        images_paths = list_files(classes_dir_paths[num])[:class_samples_num]

        for image_path in images_paths:
            image = cv2.imread(image_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            images.append(image)

    # визуализация
    fig, axs = plt.subplots(
        len(classes), class_samples_num, figsize=(class_samples_num, len(classes))
    )
    # visualize hard coded params
    left = 0.1
    bottom = 0.01
    right = 0.99
    top = 0.99
    wspace = 0
    hspace = 0

    for i, ax in enumerate(axs.flat):
        ax.imshow(images[i])
        ax.axis("off")
        if i % class_samples_num == 0:
            # ax.set_title(classes[i // class_samples_num])
            ax.text(
                0.01,
                0.5 * (bottom + top),
                classes[i // class_samples_num],
                horizontalalignment="right",
                verticalalignment="center",
                rotation="vertical",
                transform=ax.transAxes,
            )

    plt.subplots_adjust(left, bottom, right, top, wspace, hspace)
    plt.savefig("classes_visualize.jpg", dpi=400)
