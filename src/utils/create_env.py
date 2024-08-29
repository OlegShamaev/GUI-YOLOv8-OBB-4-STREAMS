def create_env_file():
    # Запрашиваем у пользователя параметры базы данных
    db_user = input("Введите имя пользователя базы данных (DB_USER): ")
    db_pass = (
        input("Введите пароль базы данных (DB_PASS) (или оставьте пустым для None): ") or "None"
    )
    db_name = (
        input("Введите имя базы данных (DB_NAME) (по умолчанию vtormet_yolo_db ): ")
        or "vtormet_yolo_db"
    )
    db_port = input("Введите порт базы данных (DB_PORT) (по умолчанию 5432): ") or "5432"
    db_host = (
        input("Введите хост базы данных (DB_HOST) (по умолчанию localhost ): ") or "localhost"
    )

    # Создаем строки для .env файла
    env_content = f"""
DB_USER={db_user}
DB_PASS={db_pass}
DB_NAME={db_name}
DB_PORT={db_port}
DB_HOST={db_host}
"""

    # Записываем содержимое в .env файл
    with open(".env", "w") as env_file:
        env_file.write(env_content.strip())

    print(".env файл успешно создан.")
