import zipfile

from data_utils import zip_directory

if __name__ == "__main__":
    dir_path = "data/interim/RTSD_cvat_train/data"

    archive_path = dir_path + ".zip"
    zip_file = zipfile.ZipFile(archive_path, "w")
    zip_directory(dir_path, zip_file)
    zip_file.close()
