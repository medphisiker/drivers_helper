import os
import zipfile


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
