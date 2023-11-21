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

* раархивируем датасет и преобразуем его структуру под `FiftyOne's MS COCO ` формат (`RTSD_arhive_unzip.py`).
* преобразуем ``train` и `val` подвыборки датасета `RSTD` с помощью `RTSD_dataset_COCO_to_CVAT_convert.py` из `MS COCO` -> `CVAT images`.
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

filtered val
```
cvat-cli --auth USER --server-host IP-ADRESS  --server-port 8080 create "RSTD_val_filtered" --labels data/RTSD_val_cvat_filtered/labels.json --image_quality 100 --annotation_path data/RTSD_val_cvat_filtered/labels.xml --annotation_format "CVAT 1.1" local data.zip
```

download dataset
```
cvat-cli --auth USER --server-host IP-ADRESS  --server-port 8080 dump --format "COCO 1.0" --with-images True 117 RTSD_val_coco.zip
```



