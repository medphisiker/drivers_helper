import fiftyone as fo
from fiftyone import ViewField as F
import os

name = "RTSD"
dataset_dir = "data/rstd"
include_classes = (
    "5_19_1",
    "2_1",
    "5_16",
    "5_15_2",
    "3_24",
    "2_4",
    "3_27",
    "1_23",
    "4_1_1",
    "5_20",
    "3_20",
    "5_15_3",
    "5_15_1",
    "5_15_2_2",
    "1_17",
    "4_2_3",
    "5_15_5",
    "4_2_1",
    "4_1_4",
    "7_3",
    "6_4",
    "6_16",
    "5_5",
    "1_25",
    "8_2_1",
    "2_3_2",
    "3_1",
)

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

# Populate metadata on all samples
dataset.compute_metadata()

# Фильтруем датасет по классам
filtered_view = dataset.filter_labels("detections", F("label").is_in(include_classes)
)

# Export the dataset
filtered_view.export(export_dir="RTSD_val_cvat_filtered", dataset_type=fo.types.CVATImageDataset)
