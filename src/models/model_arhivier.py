import os
import zipfile

from data_utils import zip_directory


if __name__ == "__main__":
    dir_path = "runs/detect/train"
    archive_path = "yolov8s_with_metrics.zip"

    zip_file = zipfile.ZipFile(archive_path, "w")
    zip_directory(dir_path, zip_file)
    zip_file.close()
