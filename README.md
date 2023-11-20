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

# Загрузить данные в CVAT

train
```
cvat-cli --auth USER --server-host IP-ADRESS  --server-port 8080 create "RSTD_train" --labels data/cvat/labels.json --image_quality 100 --annotation_path data/cvat/labels.xml --annotation_format "CVAT 1.1" local data.zip
```

val
```
cvat-cli --auth USER --server-host IP-ADRESS  --server-port 8080 create "RSTD_val" --labels data/cvat/labels.json --image_quality 100 --annotation_path data/cvat/labels.xml --annotation_format "CVAT 1.1" local data.zip
```

download dataset
```
cvat-cli --auth USER --server-host IP-ADRESS  --server-port 8080 dump --format "YOLO 1.1" 117 RTSD_val_yolo.zip
```



