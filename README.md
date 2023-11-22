# Описание проекта

Прототип помощника для водителей, который будет оповещать их о дорожных знаках.

# Развернуть рабочее окружение

Проект использует `poetry` для управления зависимостями.
Устанавливаем `poetry` в нашу систему если он не установлен согласно офф. документации ([ссылка](https://python-poetry.org/docs/)).

Для создания виртуального рабочего окружения с `poetry` выполняем команду:
```
poetry install
```

Для его активации выполняем команду:
```
poetry shell
```

# Скачиваем датасет

Скачиваем датасет `Russian traffic sign images dataset (RSTD)` c `Kaggle` ([ссылка](https://www.kaggle.com/datasets/watchman/rtsd-dataset)).

# Преобразование данных

* разархивируем датасет и преобразуем его структуру под `FiftyOne's MS COCO ` формат (`RTSD_arhive_unzip.py`)
* преобразуем `train` и `val` подвыборки датасета `RSTD` с помощью `RTSD_dataset_COCO_to_CVAT_convert.py` из `MS COCO` -> `CVAT images`
* создаем файл `label.json` описания классов для `task` на разметку в `CVAT` (`convert_labels_to_CVAT_json.py`) для 
  1. `data/RSTD_cvat_train`
  2. `data/RSTD_cvat_val`
* архивируем папки с картинками (`images_folder_arhivier.py`) для 
  1. `data/RSTD_cvat_train`
  2. `data/RSTD_cvat_val`

# Загрузить данные в CVAT

Загрузим в `CVAT` `train`-подвыборку с помощью `cvat-cli` выполнив команду:
```
cvat-cli --auth USER --server-host IP-ADRESS --server-port 8080 create "RSTD_train" --labels data/RSTD_cvat_train/label.json --image_quality 100 --annotation_path data/RSTD_cvat_train/labels.xml --annotation_format "CVAT 1.1" local data/RSTD_cvat_train/data.zip
```
где 
* `USER` - логин администратора `CVAT`
* `IP-ADRESS` - ip-адрес сервера на котором располагается `CVAT`

для выполнения команды `CVAT` попросит нас ввести пароль администратора под логином которого мы выполняем данную команду.

Загрузим в `CVAT` `val`-подвыборку с помощью `cvat-cli` выполнив команду:
```
cvat-cli --auth USER --server-host IP-ADRESS --server-port 8080 create "RSTD_val" --labels data/RSTD_cvat_val/label.json --image_quality 100 --annotation_path data/RSTD_cvat_val/labels.xml --annotation_format "CVAT 1.1" local data/RSTD_cvat_val/data.zip
```
# Распределение классов в RTSD датасете

После этого средствами `CVAT` мы собрали статистику по встречаемости классов, оказалось что некоторых классов пренебрежимо мало.

![RTSD_train_subset_classes_distribution](repo_pics/RTSD_train_subset_classes_distribution.jpg)

Выбрали классы которые по количеству размеченных на них bbox составляли не менее 1% от всех bbox датасета.

Данные классы перечислены в `include_classes.txt`.

# Фильтрация классов по количеству представителей

* профильтруем датасет по классам, выполнив скрипт `RTSD_dataset_CVAT_filter_by_labels.py` для 
  1. `data/RSTD_cvat_train`
  2. `data/RSTD_cvat_val`

получим датасеты только с тем классами, которые мы решили оставить:
  1. `data/RTSD_train_cvat_filtered`
  2. `data/RTSD_val_cvat_filtered`

* создаем файл `label.json` описания классов для `task` на разметку в `CVAT` (`create_labels_for_CVAT_json.py`) для 
  1. `data/RTSD_train_cvat_filtered`
  2. `data/RTSD_val_cvat_filtered`

* архивируем папки с картинками (`images_folder_arhivier.py`) для 
  1. `data/RTSD_train_cvat_filtered`
  2. `data/RTSD_val_cvat_filtered`

# Загрузить данные с отобранными классами в CVAT

Загрузим в `CVAT` `train`-подвыборку с помощью `cvat-cli` выполнив команду:

```
cvat-cli --auth USER --server-host IP-ADRESS --server-port 8080 create "RSTD_train_filtered" --labels data/RTSD_train_cvat_filtered/labels.json --image_quality 100 --annotation_path data/RTSD_train_cvat_filtered/labels.xml --annotation_format "CVAT 1.1" local data/RTSD_train_cvat_filtered/data.zip
```
где 
* `USER` - логин администратора `CVAT`
* `IP-ADRESS` - ip-адрес сервера на котором располагается `CVAT`


Загрузим в `CVAT` `val`-подвыборку с помощью `cvat-cli` выполнив команду:
```
cvat-cli --auth USER --server-host IP-ADRESS --server-port 8080 create "RSTD_val_filtered" --labels data/RTSD_val_cvat_filtered/labels.json --image_quality 100 --annotation_path data/RTSD_val_cvat_filtered/labels.xml --annotation_format "CVAT 1.1" local data/RTSD_val_cvat_filtered/data.zip
```

# Преобразовать train и val подвыборки для обучения YOLOv8

Преобразуем датасеты с отобранными классами 
  1. `data/RTSD_train_cvat_filtered`
  2. `data/RTSD_val_cvat_filtered`

в формат датасета `YOLOv5` c помощью скрипта `RTSD_dataset_CVAT_to_YOLOv5_convert.py`.

В результате получим датасет `data/RSTD_filtered_yolov5` который будет содержать сразу `train` и `val` подвыборки.

# Скачаем датасеты с отобранными классами
download dataset
```
cvat-cli --auth USER --server-host IP-ADRESS  --server-port 8080 dump --format "COCO 1.0" --with-images True 117 RTSD_val_coco.zip
```

# Обучение модели

Для обучения модели запустим скрипт `yolov8_train.py`.

В результате была обучена модель на распознавание данных классов:

```
5_19_1
2_1
5_16
5_15_2
3_24
2_4
3_27
1_23
4_1_1
5_20
3_20
5_15_3
5_15_1
5_15_2_2
1_17
4_2_3
5_15_5
4_2_1
4_1_4
7_3
6_4
6_16
```

## Полученные метрики модели

* Сonfusion matrix normalized
![confusion_matrix_normalized](repo_pics/confusion_matrix_normalized.png)

* precision(B), recall(B), mAP50(B), mAP50-95(B), val/box_loss, val/cls_loss, val/dfl_loss
![metrics](repo_pics/metrics.png)

* Precision-Recall curve
![PR_curve](repo_pics/PR_curve.png)

* F1-confidence calibration curve
![F1_curve](repo_pics/F1_curve.png)

* Precision-confidence calibration curve
![P_curve](repo_pics/P_curve.png)

* Precision-confidence calibration curve
![R_curve](repo_pics/R_curve.png)

Скачать веса модели можно по данной ссылке ([ссылка](https://disk.yandex.ru/d/X7PqqG7LZUhI7Q)).

## Таблица результатов

|                   epoch |          train/box_loss |          train/cls_loss |          train/dfl_loss |    metrics/precision(B) |       metrics/recall(B) |        metrics/mAP50(B) |     metrics/mAP50-95(B) |            val/box_loss |            val/cls_loss |            val/dfl_loss |                  lr/pg0 |                  lr/pg1 |                  lr/pg2 |
|-------------------------|-------------------------|-------------------------|-------------------------|-------------------------|-------------------------|-------------------------|-------------------------|-------------------------|-------------------------|-------------------------|-------------------------|-------------------------|-------------------------|
|                       1 |                  1.1951 |                   1.924 |                 0.87289 |                  0.8043 |                 0.73304 |                 0.81532 |                 0.54547 |                  1.0532 |                 0.73359 |                 0.84458 |                0.003331 |                0.003331 |                0.003331 |
|                       2 |                  1.1279 |                 0.78341 |                 0.85876 |                 0.86066 |                 0.79731 |                 0.87331 |                 0.60527 |                 0.98853 |                  0.6219 |                 0.83879 |               0.0063344 |               0.0063344 |               0.0063344 |
|                       3 |                  1.1366 |                 0.78185 |                 0.85923 |                 0.81829 |                 0.76181 |                  0.8445 |                 0.57339 |                  1.0305 |                 0.68911 |                  0.8482 |               0.0090079 |               0.0090079 |               0.0090079 |
|                       4 |                  1.1216 |                 0.76634 |                 0.85871 |                 0.84733 |                  0.8112 |                 0.87869 |                 0.60698 |                 0.97985 |                 0.60946 |                 0.83493 |                0.008515 |                0.008515 |                0.008515 |
|                       5 |                   1.068 |                 0.69116 |                 0.84955 |                 0.87803 |                 0.83308 |                 0.90284 |                 0.63765 |                  0.9425 |                 0.56029 |                 0.83056 |                0.008515 |                0.008515 |                0.008515 |
|                       6 |                  1.0294 |                 0.64936 |                  0.8444 |                 0.89646 |                 0.85373 |                 0.92533 |                 0.66401 |                 0.90926 |                 0.51441 |                 0.82605 |                 0.00802 |                 0.00802 |                 0.00802 |
|                       7 |                 0.99954 |                 0.61327 |                 0.83935 |                 0.89169 |                 0.87098 |                  0.9297 |                 0.67282 |                 0.89183 |                 0.49306 |                 0.82314 |                0.007525 |                0.007525 |                0.007525 |
|                       8 |                 0.98244 |                  0.5922 |                 0.83575 |                 0.90387 |                 0.87649 |                 0.93931 |                 0.68753 |                 0.86974 |                 0.46874 |                   0.819 |                 0.00703 |                 0.00703 |                 0.00703 |
|                       9 |                 0.96148 |                 0.56786 |                 0.83308 |                  0.9069 |                 0.89098 |                 0.94655 |                 0.69725 |                 0.85612 |                 0.45487 |                 0.81734 |                0.006535 |                0.006535 |                0.006535 |
|                      10 |                 0.94665 |                 0.55006 |                 0.83134 |                 0.90275 |                 0.90689 |                 0.94994 |                 0.70286 |                 0.84456 |                 0.44035 |                 0.81547 |                 0.00604 |                 0.00604 |                 0.00604 |
|                      11 |                 0.94842 |                 0.54839 |                 0.83332 |                 0.90591 |                 0.89889 |                 0.94919 |                 0.70349 |                 0.84516 |                 0.44487 |                 0.81651 |                0.005545 |                0.005545 |                0.005545 |
|                      12 |                 0.93366 |                 0.53215 |                 0.83213 |                 0.91506 |                 0.90287 |                 0.95492 |                 0.71157 |                 0.83771 |                 0.43374 |                 0.81543 |                 0.00505 |                 0.00505 |                 0.00505 |
|                      13 |                 0.92272 |                  0.5177 |                 0.83084 |                 0.92451 |                 0.90575 |                  0.9556 |                 0.71452 |                 0.82874 |                 0.42542 |                 0.81316 |                0.004555 |                0.004555 |                0.004555 |
|                      14 |                 0.91073 |                 0.50286 |                 0.82878 |                 0.91906 |                 0.91454 |                 0.95912 |                 0.71901 |                 0.82135 |                 0.41793 |                 0.81197 |                 0.00406 |                 0.00406 |                 0.00406 |
|                      15 |                 0.89642 |                 0.48861 |                  0.8262 |                  0.9254 |                 0.91502 |                 0.95992 |                  0.7252 |                 0.81437 |                 0.41211 |                 0.81062 |                0.003565 |                0.003565 |                0.003565 |
|                      16 |                 0.88399 |                 0.47459 |                 0.82475 |                 0.92878 |                 0.91588 |                 0.96247 |                 0.72677 |                  0.8081 |                 0.40607 |                 0.80999 |                 0.00307 |                 0.00307 |                 0.00307 |
|                      17 |                 0.87013 |                 0.45941 |                 0.82238 |                 0.93486 |                 0.91953 |                 0.96567 |                 0.73125 |                 0.80485 |                 0.40044 |                 0.80924 |                0.002575 |                0.002575 |                0.002575 |
|                      18 |                 0.85588 |                 0.44461 |                 0.82019 |                 0.93013 |                  0.9254 |                 0.96666 |                 0.73371 |                 0.80207 |                 0.39526 |                 0.80865 |                 0.00208 |                 0.00208 |                 0.00208 |
|                      19 |                 0.83945 |                 0.42945 |                 0.81814 |                  0.9287 |                 0.92807 |                 0.96861 |                 0.73764 |                 0.79885 |                 0.39125 |                 0.80803 |                0.001585 |                0.001585 |                0.001585 |
|                      20 |                  0.8248 |                 0.41468 |                 0.81698 |                 0.93057 |                 0.92947 |                 0.96961 |                 0.73911 |                 0.79494 |                 0.38833 |                 0.80735 |                 0.00109 |                 0.00109 |                 0.00109 |
