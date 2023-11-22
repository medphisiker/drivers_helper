import zipfile
import os


if __name__ == "__main__":
    # zip archive of RSTD Dataset
    zip_path = "data/archive.zip"
    dest_dir_path = "data/RTSD"

    # MS COCO FiftyOne structure
    frames_dir_src = "rtsd-frames"
    frames_dir = "data"

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(dest_dir_path)

    frames_dir_src = os.path.join(dest_dir_path, frames_dir_src)
    dst_dir_src = os.path.join(dest_dir_path, frames_dir)
        
    os.rename(frames_dir_src, dst_dir_src)
