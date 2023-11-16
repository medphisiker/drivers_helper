import fiftyone as fo
import os

name = "RSTD"
dataset_dir = "data/archive"

# Load the dataset, using tags to mark the samples in each split
dataset = fo.Dataset(name)

dataset.add_dir(
    dataset_dir=dataset_dir,
    dataset_type=fo.types.COCODetectionDataset,
    tags="train",
)

# View summary info about the dataset
print(dataset)

# Print the first few samples in the dataset
print(dataset.head())

# Export the dataset
dataset.export(
    export_dir="yolo",
    dataset_type=fo.types.YOLOv5Dataset
)
