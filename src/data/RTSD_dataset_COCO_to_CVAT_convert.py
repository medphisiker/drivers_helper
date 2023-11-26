import os

import fiftyone as fo
from data_utils import get_fiftyones_json_path

if __name__ == "__main__":
    dataset_name = "RSTD"
    dataset_dir = "data/interim/RTSD"
    subset = "train"  # 'train', 'val'
    json_path_src = "data/interim/RTSD/train_anno.json"

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
        export_dir=f"{dataset_dir}_cvat_{subset}",
        dataset_type=fo.types.CVATImageDataset,
    )
