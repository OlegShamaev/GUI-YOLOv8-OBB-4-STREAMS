# Advanced Video Processing Application
_______________________________________

- автор `Шамаев Олег Сергеевич`
- email `MlOpsEngineer@yandex.ru`
- фреймворк GUI - `PyQt6`
- фреймворк обработки `Ultralytics `
_______________________________________
## ОПИСАНИЕ:


- это мощное и гибкое приложение, разработанное с использованием PyQt6, предназначенное для обработки видео потоков в реальном времени с использованием модели YOLOv8-OBB. 
- Приложение отображает результаты обнаружения непосредственно в исходном видеопотоке, гарантируя, что даже на недорогих системах видеопоток остается плавным и без сбоев. Такой подход сводит к минимуму затраты на обработку, обычно связанные с анализом видео в режиме реального времени, обеспечивая эффективную производительность без ущерба для плавности воспроизведения видео. Оптимизируя процесс рендеринга, приложение обеспечивает бесперебойный просмотр, поддерживая постоянную частоту кадров даже при ограниченных аппаратных ресурсах.
- Приложение поддерживает обработку видео с камер и видео файлов обеспечивая высокоэффективную детекцию объектов и сохранение результатов. 
- Оно ориентировано на пользователей, которым требуется точная и быстрая обработка видеоданных для аналитики и мониторинга.

- Основные возможности:

    - Многокамерная обработка:
        - В приложении предусмотрено 6 вкладок.
        - Первая вкладка отображает все камеры одновременно (`All Cameras`).
        - Четыре следующие вкладки предназначены для работы с каждой камерой отдельно.
        - Последняя вкладка используется для настройки параметров.

    -  Оптимизация нагрузки:
        - Обработка видео осуществляется только на активной вкладке, что снижает нагрузку на систему.
        - На вкладке `All Camera` обрабатываются все камеры одновременно. Однако в меню `Ai Workers` вы можете приостановить обработку любой из камер.
        - На вкладке `Settings `обработка всех камер ставится на паузу.

    - Сохранение сеансов:
        - Настройки последнего сеанса сохраняются и восстанавливаются при следующем запуске.
        - Приложение запоминает последнюю открытую вкладку и восстанавливает её при перезапуске.

    - Логирование:
        - Приложение ведет детализированный лог в файл, позволяющий отслеживать работу и выявлять ошибки.

    - Интеграция модели `YOLOv8-OBB`:
        - Подключена и настроена модель OBB (Oriented Bounding Box) для точной детекции объектов.

    - Обработка по интервалам кадров:
        - Реализована возможность настройки Frame Interval для пропуска кадров, что позволяет снизить нагрузку на обработку.

    - Запись результатов:
        - Результаты детекции могут записываться в базу данных `PostgreSQL` или в файлы в формате, совместимом с `YOLOv6-OBB` (`labels.txt` и `images.jpeg`).
        - Можно настроить запись в зависимости от порога уверенности модели.

    - Управление детекцией:
        - Возможность включения или отключения детекции по каждому процессу на вкладке `All Camera`.
        - Поддержка выбора области детекции с возможностью настройки обработки внутри или снаружи выбранной области.

    - Файл конфигурации:
        - Приложение использует `JSON` файл конфигурации, позволяющий гибко настраивать:
            - Видимость вкладки настроек.
            - Способ записи результатов (в базу данных или файл).
            - Порог уверенности для записи.
            - Использование порога уверенности модели для записи.

    - Рефакторинг под нужды заказчика:
        - Приложение можно доработать для удовлетворения конкретных требований и задач заказчика.


- Структура интерфейса

    - `All Camera`s: Вкладка для отображения всех камер одновременно. Позволяет следить за всеми видео потоками в одном окне.

        <ul>
        <li>AiWorkers:</li>
        <ul>
            <li>☑️ Cam1 AllCamera</li>
            <li>☑️ Cam2 AllCamera</li>
            <li>☑️ Cam3 AllCamera</li>
            <li>☑️ Cam4 AllCamera</li>
        </ul>
        </ul>

    - `Camera 1-4`: Индивидуальные вкладки для каждой камеры.
    - `Settings`: Вкладка настройки видео потоков. Позволяет настраивать параметры детекции, записи и интерфейса.
s
        <ul>
        <li>Supported Input Sources:</li>
        <ul>
            <li>☑️ local files: images or videos</li>
            <li>☑️ Camera</li>
            <li>☑️ RTSP-Stream</li>
        </ul>
        <li>Supported Models:</li>
        <ul>
            <li>☑️ YOLOv8n</li>
            <li>☑️ YOLOv8s</li>
            <li>☑️ YOLOv8m</li>
            <li>☑️ YOLOv8l</li>
            <li>☑️ YOLOv8x</li>
        </ul>
        <li>Display Areas:</li>
        <ul>
            <li>☑️ IN</li>
            <li>☑️ OUT</li>
        </ul>
        </ul>


---------------------------------------------------------------------------------------------------------------
## Project Organization
<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>


```
├── main.py            <- This is the main entry point of the project.
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make db' and other
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── db_image       <- Data Base images.
│   ├── images         <- Images.
│   ├── labels         <- Labels.
│   └── video          <- start video and other video.
│
├── docs               <- A default mkdocs project; see mkdocs.org for details.
│   ├── docs           <- Docs .md files.
|   ├── mkdocs.yml     <- Configuration file MkDocs.
|   └── README-DOCS.md <- README MkDocs use.
|
├── logs               <- Logs
|
├── models             
|    ├─ weights        <- Trained model file format yolov8n-obb.pt
│    └─ classes.txt    <- Classes for models
|
├── notebooks          <- Jupyter notebooks
│
├── pyproject.toml     <- Project configuration file with package metadata for project
│                         and configuration for tools like black
│
├── src                <- Modules
│   ├── data_type
|   ├── models
|   ├── qt
|   ├── ui
|   └── utils
|
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8, Black, isort
```

---------------------------------------------------------------------------------------------------------------


## Getting started


Файлы моделей сохраняются в папке  **models/weights/** .

Файлы моделей должны быть в формате **PyTorch** .

Имена моделей должны быть **`yolov8n-obb.pt` `yolov8s-obb.pt` `yolov8m-obb.pt` `yolov8l-obb.pt` `yolov8x-obb.pt`**

Файлы `classes.txt` сохраняются в папке  **models/** .

Скачать Ultralytics pre-trained models скрипт download_weights.py (диалог выбора в терминале)

## Configuration file
Резервная копия файла находится в папке  `backup/config.json`

### Config.json


1. **preference** - отображение вкладки настроек  `true` или `false`


2. **db_confidence** - порог уверенности, выше которого происходит запись в базу данных, от `0` до `1`.


3. **db_use_conf_model** - для записи в базу данных использовать порог уверенности, установленный для обнаружения модели `true` или `false`


4. **db_save** - для записи в базу данных используйте `DataBase`, для записи в файл в формате YOLO используйте `File`, для отмены записи используйте `Disabled`.

- остальные параметры изменяются программой.

## Makefile

### Help
- Список команд и их описание

```shell
make help
```

### Install
- Настройка среды интерпретатора Python

```shell
make create_venv
```

- Установка необходимых пакетов с помощью pip

```shell
make requirements
```

### Ultralytics models 
- Скачать Ultralytics pre-trained models

```shell
make get_models
```

### Start
- Запуск приложения

```shell
make run
```

### Debug
- Удаляет скомпилированные файлы Python и временные каталоги.

```shell
make clear
```

- Проверяет код на соответствие стилю и наличие ошибок с помощью flake8 и isort.

```shell
make lint
```


### Data Base 
Наше приложение по умолчанию использует базу данных **PostgreSQL**. Для использования другой базы данных настройте файл  **src/utils/db_config.py** .


#### Configuration

- Создайте файл **.env** для безопасного хранения учетных данных базы данных:

```shell
make db_env
```

- Переменные файла **.env**

```shell


    DB_USER=your-user


    DB_PASS=your-pass


    DB_NAME=vtormet_yolo_db


    DB_PORT=5432


    DB_HOST=localhost  
```

#### Creating
- Создание базы данных и таблиц для записи результатов обнаружения:

```shell
make db_create
```


- Создание каталогов для записи результатов обнаружения в файлы:

```shell
make folders_create
```
#### Dump

- Data Base
Создает дамп базы данных и изображений в архив в папке data и очищает таблицы базы данных:

```shell
make dump_db
```

- Files
Создает дамп каталогов с изображениями и метками и очищает их:

```shell
make dump_files
```

#### Clean
- Очищает таблицы базы данных и удаляет изображения:

```shell
make clear_db
```

- Очищает каталоги с изображениями и метками:

```shell
make clear_folders
```



### MkDocs
#### Install

```shell
make install_docs
```
#### Create site
MkDocs - это генератор статических сайтов, который создает веб-сайт из файлов Markdown.

```shell
make build_docs
```

#### Start site
MkDocs запускает сайт документации по адрес [ http://127.0.0.1:8000/]( http://127.0.0.1:8000/)

```shell
make serve_docs
```