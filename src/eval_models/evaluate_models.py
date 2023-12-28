import os
import shutil

from ultralytics import YOLO


def evaluate_model(model_path, dataset_yaml_path, device="cpu"):
    model = YOLO(model_path)
    metrics = model.val(data=dataset_yaml_path, batch=1, device=device)

    # собираем результаты
    results = {}
    results["preprocess"] = metrics.speed["preprocess"]
    results["inference"] = metrics.speed["inference"]
    results["loss"] = metrics.speed["loss"]
    results["postprocess"] = metrics.speed["postprocess"]
    results["working_time"] = (
        results["preprocess"]
        + results["inference"]
        + results["loss"]
        + results["postprocess"]
    )
    results["bbox map50-95"] = metrics.box.map
    results["bbox map50"] = metrics.box.map50
    results["bbox map75"] = metrics.box.map75

    if os.path.isdir(model_path):
        results["size Mb"] = get_dir_size_in_mb(model_path)
        shutil.rmtree(model_path)

    else:
        results["size Mb"] = get_file_size_in_mb(model_path)
        os.remove(model_path)

    return results


def get_file_size_in_mb(file_path):
    model_size = os.path.getsize(file_path) / 1024**2
    return model_size


def get_dir_size_in_mb(directory):
    file_sizes = 0
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            size_in_bytes = os.path.getsize(file_path)
            size_in_mb = size_in_bytes / 1024 / 1024
            file_sizes += size_in_mb

    return file_sizes


def convert_and_eval_model(
    model_path,
    model_name,
    dataset_yaml_path,
    device,
    report_table,
    format,
    simplify=False,
    half=False,
):
    if format != "torch":
        model = YOLO(model_path)
        model_path = model.export(format=format, simplify=simplify, half=half)

    results = {}
    results["model_name"] = f"{model_name}_{format}"
    if simplify:
        results["model_name"] += "_simplify"
    if half:
        results["model_name"] += "_half"
    results.update(evaluate_model(model_path, dataset_yaml_path, device))

    for key in results:
        report_table[key].append(results[key])

    return report_table
