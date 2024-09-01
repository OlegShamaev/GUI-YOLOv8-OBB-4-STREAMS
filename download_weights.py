import os
import requests
from tqdm import tqdm
from src.utils.general import ROOT

# URL для скачивания моделей
MODEL_URLS = {
    'yolov8n-obb.pt': 'https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8n-obb.pt',
    'yolov8s-obb.pt': 'https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8s-obb.pt',
    'yolov8m-obb.pt': 'https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8m-obb.pt',
    'yolov8l-obb.pt': 'https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8l-obb.pt',
    'yolov8x-obb.pt': 'https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8x-obb.pt',
}

# Определяем корневую директорию
MODEL_DIR = os.path.join(ROOT, 'models/weights')

# Создание папок, если они не существуют
os.makedirs(MODEL_DIR, exist_ok=True)

def download_file(url, dest_path):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte

    with open(dest_path, 'wb') as file, tqdm(
            desc=dest_path,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(block_size):
            bar.update(len(data))
            file.write(data)

def ask_user(prompt):
    while True:
        choice = input(prompt).strip().lower()
        if choice in {'y', 'n'}:
            return choice
        else:
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")

def main():
    for model_name, url in MODEL_URLS.items():
        # Определяем путь для сохранения файла
        dest_path = os.path.join(MODEL_DIR, model_name)

        if os.path.exists(dest_path):
            choice = ask_user(f"File {model_name} already exists. Do you want to replace it? (y/n): ")
            if choice != 'y':
                continue

        choice = ask_user(f"Download {model_name}? (y/n): ")
        if choice == 'y':
            print(f"Downloading {model_name}...")
            download_file(url, dest_path)
            print(f"Downloaded {model_name} to {dest_path}")

if __name__ == "__main__":
    main()
