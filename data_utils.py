import os


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
