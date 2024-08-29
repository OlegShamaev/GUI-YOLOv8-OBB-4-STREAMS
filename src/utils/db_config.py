import psycopg2
import os
import shutil
import numpy as np
import uuid
import zipfile
import subprocess
from psycopg2 import sql
from datetime import datetime
from psycopg2 import sql, pool
from PIL import Image as PILImage
from src.utils.logging_config import logger
from src.utils.general import ROOT
from src.utils.config import config, db_settings


DB_HOST = db_settings.DB_HOST
DB_PORT = db_settings.DB_PORT
DB_NAME = db_settings.DB_NAME
DB_USER = db_settings.DB_USER
DB_PASS = db_settings.DB_PASS

DB_SAVE = config.last_state.db_save

PATH_DATA = os.path.join(ROOT, "data")
PATH_DB_IMAGES = os.path.join(ROOT, "data/db_images")
PATH_IMAGES = os.path.join(ROOT, "data/images")
PATH_LABELS = os.path.join(ROOT, "data/labels")


def check_disk_space(threshold_percentage=50, path="/"):
    """
    Проверяет, достаточно ли свободного места на диске по заданному проценту.

    :param threshold_percentage: Процент, ниже которого свободное место на диске считается недостаточным.
    :param path: Путь к директории, для которой нужно проверить свободное место. По умолчанию "/".
    :return: True, если свободного места достаточно, иначе False.
    """
    total, used, free = shutil.disk_usage(path)
    free_percentage = (free / total) * 100

    if free_percentage < threshold_percentage:
        return False
    return True


def get_disk_free_space(path="/"):
    """
    Возвращает оставшееся место на диске в байтах.

    :param path: Путь к директории, для которой нужно определить оставшееся место.
                 По умолчанию используется корневая директория "/".
    :return: total, used, free в байтах.
    """
    total, used, free = shutil.disk_usage(path)
    return total, used, free


def create_database_and_folders():
    create_folders()
    print("Creating database...")
    create_database(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
    print("Creating tables...")
    create_tables(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)


def create_folders():
    os.makedirs(PATH_DATA, exist_ok=True)
    os.makedirs(PATH_IMAGES, exist_ok=True)
    os.makedirs(PATH_LABELS, exist_ok=True)
    print(f"Путь к папке data: {PATH_DATA}")
    print(f"Путь к папке с изображениями: {PATH_IMAGES}")
    print(f"Путь к папке с метками: {PATH_LABELS}")


def clear_folder_images_and_labels():
    clear_folder(PATH_IMAGES)
    clear_folder(PATH_LABELS)


def dump_files():
    create_archive(PATH_DATA, [PATH_IMAGES, PATH_LABELS])
    clear_folder_images_and_labels()


def create_dump_database_with_clear():
    path_dump_folders = os.path.join(PATH_DATA, "dump_db")
    try:
        # Создание директории для дампа, если она не существует
        os.makedirs(path_dump_folders, exist_ok=True)

        # Путь к файлу дампа
        dump_file = os.path.join(path_dump_folders, "backup.dump")

        # Создание дампа базы данных
        create_db_dump(
            db_name=DB_NAME,
            db_user=DB_USER,
            db_password=DB_PASS,
            db_host=DB_HOST,
            db_port=DB_PORT,
            dump_file=dump_file,
        )

        # Создание архива с дампом и изображениями базы данных
        create_archive(PATH_DATA, [path_dump_folders, PATH_DB_IMAGES])
        print("Database dump created and archived successfully.")

        # Очистка таблиц базы данных
        clear_tables()

    except (psycopg2.DatabaseError, OSError, shutil.Error) as e:
        print(f"An error occurred: {e}")
    finally:
        # Удаление директории с дампом базы данных
        if os.path.exists(path_dump_folders):
            shutil.rmtree(path_dump_folders)
            print("Temporary dump directory removed.")
        print("Done!")


def create_archive(output_dir, folder_paths):
    """
    Создает архив из указанных папок, где каждая папка сохраняется как отдельный каталог в архиве.

    :param output_dir: Путь к директории, где будет сохранен архив.
    :param folder_paths: Список путей к папкам, которые нужно добавить в архив.
    """
    # Создание уникального имени файла архива
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_names = "_".join([os.path.basename(folder_path) for folder_path in folder_paths])
    arch_name = f"archive_{folder_names}_{timestamp}.zip"
    archive_path = os.path.join(output_dir, arch_name)
    print(f"Создание архива: {archive_path}")

    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for folder_path in folder_paths:
            if os.path.isdir(folder_path):
                base_folder_name = os.path.basename(folder_path)
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Включаем папку в имя файла в архиве
                        arcname = os.path.join(
                            base_folder_name, os.path.relpath(file_path, folder_path)
                        )
                        zipf.write(file_path, arcname)
            else:
                print(f"Путь {folder_path} не является директорией и будет пропущен.")

    print(f"Архив успешно создан: {archive_path}")


def clear_folder(folder_path):
    # Очистка файлов в папке PATH_DB_IMAGES
    if folder_path and os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Ошибка при удалении файла {file_path}: {e}")
        print(f"Файлы в папке {folder_path} успешно удалены.")


def create_database(dbname, user, password=None, host="localhost", port="5432"):
    try:
        # Подключение к PostgreSQL с учетом наличия пароля
        if password:
            conn = psycopg2.connect(
                dbname="postgres", user=user, password=password, host=host, port=port
            )
        else:
            conn = psycopg2.connect(dbname="postgres", user=user, host=host, port=port)

        conn.autocommit = True

        # Создание курсора для выполнения SQL-запросов
        cursor = conn.cursor()

        # Проверка, существует ли база данных
        cursor.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), [dbname])

        # Если база данных существует, выводим сообщение и выходим
        if cursor.fetchone():
            print(f"База данных '{dbname}' уже существует.")
        else:
            # Если база данных не существует, создаем её
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))
            print(f"База данных '{dbname}' успешно создана.")

        os.makedirs(PATH_DATA, exist_ok=True)
        os.makedirs(PATH_DB_IMAGES, exist_ok=True)
        print(f"Путь к папке с изображениями в базе данных: {PATH_DB_IMAGES}")

    except Exception as e:
        logger.exception(f"Ошибка: {e}")

    finally:
        # Закрытие соединения
        if "cursor" in locals():
            cursor.close()
        if "conn" in locals():
            conn.close()


def create_tables(dbname, user, password=None, host="localhost", port="5432"):
    try:
        # Подключение к PostgreSQL с учетом наличия пароля
        if password:
            conn = psycopg2.connect(
                dbname=dbname, user=user, password=password, host=host, port=port
            )
        else:
            conn = psycopg2.connect(dbname=dbname, user=user, host=host, port=port)

        conn.autocommit = True

        # Создание курсора для выполнения SQL-запросов
        cursor = conn.cursor()

        # SQL-запросы для создания таблиц
        create_images_table = """
        CREATE TABLE IF NOT EXISTS Images (
            id SERIAL PRIMARY KEY,
            file_name VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

        create_objects_table = """
        CREATE TABLE IF NOT EXISTS Objects (
            id SERIAL PRIMARY KEY,
            image_id INT,
            class_label VARCHAR(50),
            x1 FLOAT,
            y1 FLOAT,
            x2 FLOAT,
            y2 FLOAT,
            x3 FLOAT,
            y3 FLOAT,
            x4 FLOAT,
            y4 FLOAT,
            confidence FLOAT,
            FOREIGN KEY (image_id) REFERENCES Images(id) ON DELETE CASCADE
        );
        """

        # Создание таблиц
        cursor.execute(create_images_table)
        cursor.execute(create_objects_table)

        print("Таблицы 'Images' и 'Objects' успешно созданы или уже существуют.")

    except Exception as e:
        logger.exception(f"Ошибка: {e}")

    finally:
        # Закрытие соединения
        if "cursor" in locals():
            cursor.close()
        if "conn" in locals():
            conn.close()


def clear_tables(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT):
    print("Очистка таблиц...")
    try:
        # Подключение к PostgreSQL с учетом наличия пароля
        if password:
            conn = psycopg2.connect(
                dbname=dbname, user=user, password=password, host=host, port=port
            )
        else:
            conn = psycopg2.connect(dbname=dbname, user=user, host=host, port=port)

        conn.autocommit = True

        # Создание курсора для выполнения SQL-запросов
        cursor = conn.cursor()

        # SQL-запросы для очистки таблиц
        clear_images_table = "TRUNCATE TABLE Images RESTART IDENTITY CASCADE;"
        clear_objects_table = "TRUNCATE TABLE Objects RESTART IDENTITY CASCADE;"

        # Очистка таблиц
        cursor.execute(clear_images_table)
        cursor.execute(clear_objects_table)

        print("Таблицы 'Images' и 'Objects' успешно очищены.")

        clear_folder(PATH_DB_IMAGES)

    except Exception as e:
        logger.exception(f"Ошибка: {e}")
        print(f"Ошибка при очистке таблиц: {e}")

    finally:
        # Закрытие соединения
        if "cursor" in locals():
            cursor.close()
        if "conn" in locals():
            conn.close()


def create_connection_pool():
    try:
        connection_pool = pool.ThreadedConnectionPool(
            minconn=1,
            maxconn=4,
            user=DB_USER,
            password=DB_PASS,
            host="localhost",
            port="5432",
            database=DB_NAME,
        )
        logger.debug("Пул соединений успешно создан.")
        return connection_pool
    except Exception as e:
        logger.exception(f"Ошибка при создании пула соединений: {e}")
        return None


def terminate_idle_connections():
    try:
        # Создаем временное соединение для выполнения команды
        with psycopg2.connect(
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
        ) as conn:
            with conn.cursor() as cursor:
                # Выполняем команду для завершения неактивных соединений
                cursor.execute(
                    """
                        SELECT pg_terminate_backend(pid)
                        FROM pg_stat_activity
                        WHERE state = 'idle' AND pid <> pg_backend_pid();
                    """
                )
                conn.commit()
                print("Неактивные соединения завершены.")
    except Exception as e:
        print(f"Ошибка при завершении неактивных соединений: {e}")

    finally:
        # Закрытие соединения
        if "cursor" in locals():
            cursor.close()
        if "conn" in locals():
            conn.close()


def save_detection_results(detection_results, image, cursor=None):
    if DB_SAVE == "Disabled":
        return
    try:
        # Создание уникального имени файла изображения
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = uuid.uuid4().hex  # Генерация UUID
        image_name = f"image_{timestamp}_{unique_id}.jpeg"

        # Сохранение изображения в папку data/images/
        image_dir = PATH_DB_IMAGES if DB_SAVE == "DataBase" else PATH_IMAGES
        # Преобразование массива NumPy в объект изображения Pillow
        image_pil = PILImage.fromarray(np.uint8(image))
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
        image_path = os.path.join(image_dir, image_name)

        if DB_SAVE == "DataBase" and cursor is not None:
            # Вставка данных изображения в таблицу Images
            cursor.execute(
                sql.SQL("INSERT INTO Images (file_name) VALUES (%s) RETURNING id"), [image_name]
            )
            image_id = cursor.fetchone()[0]  # Получение ID вставленной записи

            # Вставка результатов детекции в таблицу Objects
            for result in detection_results:
                # logger.debug(result)
                bbox = result["bbox"][0]

                # Преобразование всех значений в обычные float
                bbox_floats = [float(coord) for point in bbox for coord in point]

                cursor.execute(
                    sql.SQL(
                        """
                        INSERT INTO Objects (
                            image_id, class_label, x1, y1, x2, y2, x3, y3, x4, y4, confidence
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    ),
                    [
                        image_id,
                        result["class"],
                        bbox_floats[0],  # x1
                        bbox_floats[1],  # y1
                        bbox_floats[2],  # x2
                        bbox_floats[3],  # y2
                        bbox_floats[4],  # x3
                        bbox_floats[5],  # y3
                        bbox_floats[6],  # x4
                        bbox_floats[7],  # y4
                        float(result["confidence"]),
                    ],
                )
        elif DB_SAVE == "File":
            # Сохранение результатов детекции в текстовый файл
            if not os.path.exists(PATH_LABELS):
                os.makedirs(PATH_LABELS)

            file_path = os.path.join(PATH_LABELS, f"{os.path.splitext(image_name)[0]}.txt")

            with open(file_path, "w") as file:
                for result in detection_results:
                    bbox = result["bbox"][0]
                    bbox_floats = [float(coord) for point in bbox for coord in point]
                    class_index = result["class_index"]
                    line = f"{class_index} {bbox_floats[0]} {bbox_floats[1]} {bbox_floats[2]} {bbox_floats[3]} {bbox_floats[4]} {bbox_floats[5]} {bbox_floats[6]} {bbox_floats[7]}\n"
                    file.write(line)

        else:
            logger.error(
                "Результаты детекции не будут сохранены. Неизвестное значение в Config или cursor: None"
            )
            return

        image_pil.save(image_path, format="JPEG")
        logger.info(f"Результаты детекции успешно сохранены для изображения '{image_name}'.")

    except Exception as e:
        logger.exception(f"Ошибка при сохранении результатов детекции: {e}")


def create_db_dump(db_name, db_user, db_password, db_host, db_port, dump_file):
    """
    Создает дамп базы данных PostgreSQL в указанный файл.

    :param db_name: Имя базы данных.
    :param db_user: Имя пользователя базы данных.
    :param db_password: Пароль пользователя базы данных.
    :param db_host: Хост базы данных.
    :param db_port: Порт базы данных.
    :param dump_file: Имя файла, в который будет сохранен дамп.
    """
    try:
        # Устанавливаем соединение с базой данных
        conn = psycopg2.connect(
            dbname=db_name, user=db_user, password=db_password, host=db_host, port=db_port
        )
        conn.close()

        # Определяем путь к pg_dump
        pg_dump_path = subprocess.run(
            ["which", "pg_dump"], capture_output=True, text=True
        ).stdout.strip()

        if not pg_dump_path:
            raise FileNotFoundError(
                "pg_dump не найден. Убедитесь, что PostgreSQL установлен и pg_dump доступен в PATH."
            )

        # Формируем команду для создания дампа
        dump_command = [
            pg_dump_path,
            "-h",
            db_host,
            "-p",
            str(db_port),
            "-U",
            db_user,
            "-F",
            "c",  # Формат дампа (c - custom)
            "-f",
            dump_file,
            db_name,
        ]

        # Устанавливаем переменную окружения для пароля
        env = {"PGPASSWORD": db_password}

        # Выполняем команду создания дампа
        subprocess.run(dump_command, env=env, check=True)
        print(f"Дамп базы данных '{db_name}' успешно создан в файле '{dump_file}'.")

    except (FileNotFoundError, Exception, psycopg2.DatabaseError) as error:
        print(f"Ошибка при создании дампа базы данных: {error}")
        raise error
