import fiftyone as fo
from data_utils import read_classes_txt

if __name__ == "__main__":
    dataset_name = "RTSD_yolo_filtered"
    dataset_dir = {
        "train": "data/processed/RTSD_train_cvat_filtered",
        "val": "data/processed/RTSD_val_cvat_filtered",
    }
    classes_txt_path = "include_classes.txt"
    output_dir = "data/processed/RSTD_filtered_yolov5"

    include_classes = read_classes_txt(classes_txt_path)

    for subset in ["train", "val"]:
        print(f"Loading {subset} subset")

        # Load the dataset, using Аtags to mark the samples in each split
        dataset = fo.Dataset(f"{dataset_name}_{subset}")

        dataset.add_dir(
            dataset_dir=dataset_dir[subset],
            dataset_type=fo.types.CVATImageDataset,
            tags=subset,
        )

        # View summary info about the dataset
        print(dataset)

        # Print the first few samples in the dataset
        print(dataset.head())

        # Export the dataset
        print(f"Exporting {subset} subset")

        dataset.export(
            export_dir=output_dir,
            dataset_type=fo.types.YOLOv5Dataset,
            split=subset,
            classes=include_classes,
        )

        del dataset
