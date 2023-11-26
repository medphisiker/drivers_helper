import fiftyone as fo
import os


def get_fiftyones_json_path(json_src_path):
    json_dir = os.path.split(json_src_path)[0]
    fiftyones_json_name = "labels.json"
    result_json_path = os.path.join(json_dir, fiftyones_json_name)

    return result_json_path


if __name__ == "__main__":
    dataset_name = "RSTD"
    dataset_dir = "data/RTSD"
    subset = "train"  # 'train', 'val'
    json_path_src = "data/RTSD/train_anno.json"

    # rename annotation MS COCO json to FiftyOne's MS COCO naming standardА
    json_path = get_fiftyones_json_path(json_path_src)
    os.rename(json_path_src, json_path)

    # Load the dataset, using tags to mark the samples in each split
    dataset = fo.Dataset(dataset_name)

    dataset.add_dir(
        dataset_dir=dataset_dir,
        dataset_type=fo.types.COCODetectionDataset,
        tags=subset,
    )

    # return source json with labels name
    os.rename(json_path, json_path_src)

    # View summary info about the dataset
    print(dataset)

    # Print the first few samples in the dataset
    print(dataset.head())

    # Export the dataset
    dataset.export(
        export_dir=f"data/RSTD_cvat_{subset}", dataset_type=fo.types.CVATImageDataset
    )
