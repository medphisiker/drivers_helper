import os
import zipfile


def zip_directory(folder_path, zip_file):
    for folder_name, subfolders, filenames in os.walk(folder_path):
        for filename in filenames:
            # Create complete filepath of file in directory
            file_path = os.path.join(folder_name, filename)
            # Add file to zip
            zip_file.write(file_path)


if __name__ == "__main__":
    dir_path = "data/RSTD_cvat_train/data"

    archive_path = dir_path + ".zip"
    zip_file = zipfile.ZipFile(archive_path, "w")
    zip_directory(dir_path, zip_file)
    zip_file.close()
