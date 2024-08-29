# Advanced Video Processing Application
- автор `Шамаев Олег Сергеевич`
- фреймворк GUI - `PyQt6`
- фреймворк обработки `Ultralytics `

## ОПИСАНИЕ:

### Vtormet-CV — это мощное и гибкое приложение, разработанное с использованием PyQt6, предназначенное для обработки видеопотоков в реальном времени с использованием модели YOLOv8-OBB. Приложение поддерживает обработку видео с камер, видеофайлов и потоков с YouTube, обеспечивая высокоэффективную детекцию объектов и сохранение результатов. Оно ориентировано на пользователей, которым требуется точная и быстрая обработка видеоданных для аналитики и мониторинга.


- Основные возможности

    - Многокамерная обработка:
        В приложении предусмотрено 6 вкладок.
        Первая вкладка отображает все камеры одновременно (`All Cameras`).
        Четыре следующие вкладки предназначены для работы с каждой камерой отдельно.
        Последняя вкладка используется для настройки параметров.

   -  Оптимизация нагрузки:
        Обработка видео осуществляется только на активной вкладке, что снижает нагрузку на систему.
        На вкладке `All Camera` обрабатываются все камеры одновременно.
        На вкладке `Settings `обработка всех камер ставится на паузу.

    - Сохранение сеансов:
        Настройки последнего сеанса сохраняются и восстанавливаются при следующем запуске.
        Приложение запоминает последнюю открытую вкладку и восстанавливает её при перезапуске.

    - Логирование:
        Приложение ведет детализированный лог в файл, позволяющий отслеживать работу и выявлять ошибки.

    - Интеграция модели `YOLOv8-OBB`:
        Подключена и настроена модель OBB (Oriented Bounding Box) для точной детекции объектов.

    - Обработка по интервалам кадров:
        Реализована возможность настройки Frame Interval для пропуска кадров, что позволяет снизить нагрузку на обработку.

    - Запись результатов:
        Результаты детекции могут записываться в базу данных `PostgreSQL` или в файлы в формате, совместимом с `YOLOv6-OBB` (`labels.txt` и `images.jpeg`).
        Можно настроить запись в зависимости от порога уверенности модели.

    - Управление детекцией:
        Возможность включения или отключения детекции по каждому процессу на вкладке `All Camera`.
        Поддержка выбора области детекции с возможностью настройки обработки внутри или снаружи выбранной области.

    - Файл конфигурации:
        Приложение использует `JSON` файл конфигурации, позволяющий гибко настраивать:
            Видимость вкладки настроек.
            Способ записи результатов (в базу данных или файл).
            Порог уверенности для записи.
            Использование порога уверенности модели для записи.

    Рефакторинг под нужды заказчика:
        Приложение было адаптировано и доработано для удовлетворения конкретных требований и задач заказчика.


- Структура интерфейса

    - `All Camera`s: Вкладка для отображения всех камер одновременно. Позволяет следить за всеми видеопотоками в одном окне.
    - `Camera 1-4`: Индивидуальные вкладки для каждой камеры, где можно настроить и просматривать видеопоток отдельно.
    - `Settings`: Вкладка для управления настройками приложения. Позволяет настраивать параметры детекции, записи и интерфейса.



---------------------------------------------------------------------------------------------------------------
## Project Organization
<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── db_image       <- Data Base images.
│   ├── images         <- Images.
│   ├── labels         <- Labels.
│   └── video          <- start video and other video.
│
├── docs               <- A default mkdocs project; see mkdocs.org for details
│
├── logs               <- Logs
|
├── models             
|    └──weights        <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for vtormet_cv
│                         and configuration for tools like black
│
├── src                <- Modules
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
```

---------------------------------------------------------------------------------------------------------------


## `Config.json` - backup файла в папке backup

### Стартовый конфигурационный файл 
1. preference - отображать вкладку настроек `true` или `false`
2. db_confidence - порог уверенности выше которого идет запись в БД от `0` - `1`
3. db_use_conf_mode - использовать для записи в БД порог уверенности установленный для детекции модели `true` или `false`
4. db_save - запись в БД `DataBase`, в файл в формате YOLO `File`, не вести запись `Disabled`

- остальные параметры изменяются программой

## `Makefile` Список команд и их описание 

- `make help` ------------> Выводит список доступных команд.

- `make create_venv` -----> Создает виртуальное окружение для изоляции зависимостей проекта.

- `make requirements` ----> Устанавливает необходимые библиотеки из файла requirements.txt.

- `make clear` ------------> Удаляет скомпилированные файлы Python и временные директории.

- `make lint` ------------> Проверяет код на соответствие стилю и наличию ошибок с помощью flake8 и isort.

- `make db_create` -> Создает базу данных PostgreSQL и необходимые директории.

- `make folders_create` --> Создает директории для хранения данных.

- `make clear_db` --> Очищает таблицы базы данных и удаляет изображения.

- `make clear_folders` ---> Очищает директории с изображениями и метками.

- `make dump_db` ---------> Создает дамп базы данных и изображений.

- `make dump_files` ------> Создает дамп директорий с изображениями и метками.
