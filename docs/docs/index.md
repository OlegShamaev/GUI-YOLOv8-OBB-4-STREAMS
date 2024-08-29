# Advanced Video Processing Application
- автор `Шамаев Олег Сергеевич`
- фреймворк GUI - `PyQt6`
- фреймворк обработки `Ultralytics `

## ОПИСАНИЕ:


- это мощное и гибкое приложение, разработанное с использованием PyQt6, предназначенное для обработки видео потоков в реальном времени с использованием модели YOLOv8-OBB. 
- Приложение поддерживает обработку видео с камер, видеофайлов и потоков с YouTube, обеспечивая высокоэффективную детекцию объектов и сохранение результатов. 
- Оно ориентировано на пользователей, которым требуется точная и быстрая обработка видеоданных для аналитики и мониторинга.

- Основные возможности:

    - Многокамерная обработка:
        - В приложении предусмотрено 6 вкладок.
        - Первая вкладка отображает все камеры одновременно (`All Cameras`).
        - Четыре следующие вкладки предназначены для работы с каждой камерой отдельно.
        - Последняя вкладка используется для настройки параметров.

    -  Оптимизация нагрузки:
        - Обработка видео осуществляется только на активной вкладке, что снижает нагрузку на систему.
        - На вкладке `All Camera` обрабатываются все камеры одновременно.
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
        - Приложение было адаптировано и доработано для удовлетворения конкретных требований и задач заказчика.


- Структура интерфейса

    - `All Camera`s: Вкладка для отображения всех камер одновременно. Позволяет следить за всеми видео потоками в одном окне.
    - `Camera 1-4`: Индивидуальные вкладки для каждой камеры.
    - `Settings`: Вкладка настройки видео потоков. Позволяет настраивать параметры детекции, записи и интерфейса.



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
├── docs               <- A default mkdocs project; see mkdocs.org for details
│   ├── docs           <- Docs .md files
|   ├── mkdocs.yml     <- Configuration file MkDocs
|   ├── README-DOCS.md <- README MkDocs use
|   ├── ui
|   └── utils
├── logs               <- Logs
|
├── models             
|    ├─ weights        <- Trained model file format yolov8n-obb.pt
│    └─ classes.txt    <- Classes for models
|
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
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