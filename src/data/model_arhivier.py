import os
import sys
import zipfile

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "data"))
from data_utils import zip_directory

if __name__ == "__main__":
    dir_path = "models/models/yolov8s_640"
    archive_path = "yolov8s_640.zip"

    zip_file = zipfile.ZipFile(archive_path, "w")
    zip_directory(dir_path, zip_file)
    zip_file.close()
