import fiftyone as fo
from fiftyone import ViewField as F
from data_utils import read_classes_txt


if __name__ == "__main__":
    name = "RTSD"
    dataset_dir = "data/interim/RTSD_cvat_val"
    classes_txt_path = "include_classes.txt"
    export_dir_name = "data/processed/RTSD_val_cvat_filtered"

    include_classes = read_classes_txt(classes_txt_path)

    # Load the dataset, using tags to mark the samples in each split
    dataset = fo.Dataset(name)

    dataset.add_dir(
        dataset_dir=dataset_dir,
        dataset_type=fo.types.CVATImageDataset,
        tags="val",
    )

    # View summary info about the dataset
    print(dataset)

    # Print the first few samples in the dataset
    print(dataset.head())

    # Populate metadata on all samples
    dataset.compute_metadata()

    # Фильтруем датасет по классам
    filtered_view = dataset.filter_labels(
        "detections", F("label").is_in(include_classes)
    )

    # Export the dataset
    filtered_view.export(
        export_dir=export_dir_name, dataset_type=fo.types.CVATImageDataset
    )
