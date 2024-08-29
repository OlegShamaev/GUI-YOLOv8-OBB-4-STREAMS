import logging
import os
import glob
from logging.handlers import RotatingFileHandler
from src.utils.general import ROOT

LOG_DIR = os.path.join(ROOT, "logs")


def clear_log_directory(log_dir):
    # Проверка наличия папки и создание, если она не существует
    if not os.path.isdir(log_dir):
        print(f"Directory {log_dir} does not exist. Creating it.")
        os.makedirs(log_dir, exist_ok=True)

    # Получение списка файлов в папке
    files = glob.glob(os.path.join(log_dir, "*"))

    # Удаление файлов, кроме error.log
    for f in files:
        if os.path.basename(f) != "error.log":
            try:
                os.remove(f)
                print(f"Removed {f}")
            except Exception as e:
                print(f"Failed to remove {f}: {e}")


# Функция для настройки логирования
def setup_logging():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    # Очистка папки с логами
    clear_log_directory(LOG_DIR)

    # Создание главного логгера
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Установить минимальный уровень логирования

    # Обработчик для записи ошибок в файл error.log
    error_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, "error.log"), mode="w", maxBytes=10 * 1024 * 1024, backupCount=1
    )
    error_handler.setLevel(logging.ERROR)
    error_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s"
    )
    error_handler.setFormatter(error_formatter)
    logger.addHandler(error_handler)

    # Обработчик для записи всех остальных сообщений в файл app.log
    info_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, "app.log"), mode="w", maxBytes=10 * 1024 * 1024, backupCount=1
    )
    info_handler.setLevel(logging.DEBUG)
    info_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s"
    )
    info_handler.setFormatter(info_formatter)
    logger.addHandler(info_handler)

    return logger


# Настроить и получить логгер
logger = setup_logging()
