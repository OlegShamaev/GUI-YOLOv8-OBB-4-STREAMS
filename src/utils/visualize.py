import cv2 as cv
import numpy as np
import math
from src.utils.logging_config import logger
from src.utils.config import config
from src.utils.db_config import save_detection_results


rng = np.random.default_rng(3)
PALLETE = rng.uniform(0, 255, size=(81, 3))
FONT_SCALE = 1e-3
THICKNESS_SCALE = 6e-4
DB_CONF = config.last_state.db_confidence
DB_USE_CONF_MODEL = config.last_state.db_use_conf_model

SKELETON = [
    [15, 13],
    [13, 11],
    [16, 14],
    [14, 12],
    [11, 12],
    [5, 11],
    [6, 12],
    [5, 6],
    [5, 7],
    [6, 8],
    [7, 9],
    [8, 10],
    [1, 2],
    [0, 1],
    [0, 2],
    [1, 3],
    [2, 4],
    [3, 5],
    [4, 6],
]


def draw_results(
    image,
    model_results,
    area=None,
    in_out_area="IN",
    db_cursor=None,
):
    # logger.debug("Starting draw_results")

    img_cpy = image.copy()

    height, width, _ = img_cpy.shape
    # logger.debug(f"Image shape: {img_cpy.shape}")

    txt_color_light = (255, 255, 255)
    txt_color_dark = (0, 0, 0)
    font = cv.FONT_HERSHEY_SIMPLEX
    font_scale = min(width, height) * FONT_SCALE
    if font_scale <= 0.4:
        font_scale = 0.41
    elif font_scale > 2:
        font_scale = 2.0
    thickness = math.ceil(min(width, height) * THICKNESS_SCALE)

    if area is not None:
        area_real = np.array(list(area.values()))
        area_abs = [(int(point[0] * width), int(point[1] * height)) for point in area_real]
        area_abs = np.array(area_abs, dtype=np.int32)
        color = (0, 0, 255)
        # Построение ориентированных ограничивающих рамок
        cv.drawContours(img_cpy, [area_abs], 0, color, int(thickness * 5 * font_scale))
        if model_results == []:
            # logger.warning("No model results to draw")
            return img_cpy
        model_results = filter_model_result_by_area(model_results, area_real)

    detection_results = []
    flag_db = False
    if not model_results == []:
        # logger.debug("Processing OBB results")
        for obj in model_results:
            if area is not None and not (
                (obj["in_area"] and in_out_area == "IN")
                or (not obj["in_area"] and in_out_area == "OUT")
            ):
                continue

            class_name = obj["class"]
            bbox = obj["bbox"][0]
            id = int(obj["id"])
            confi = int(float(obj["confidence"]) * 100)
            color = PALLETE[id % PALLETE.shape[0]]
            text = f"{class_name}-{confi}%"
            txt_size = cv.getTextSize(text, font, 0.4, 1)[0]
            # Преобразование относительных координат в абсолютные
            abs_bbox = [(int(point[0] * width), int(point[1] * height)) for point in bbox]
            abs_bbox = np.array(abs_bbox, dtype=np.int32)
            txt_size = cv.getTextSize(text, font, 0.4, 1)[0]
            # Построение ориентированных ограничивающих рамок
            cv.drawContours(img_cpy, [abs_bbox], 0, color, int(thickness * 5 * font_scale))

            # Отрисовка текста на изображении
            x0, y0 = abs_bbox[0]
            cv.rectangle(
                img_cpy,
                (x0, y0 + 1),
                (x0 + txt_size[0] + 1, y0 + int(1.5 * txt_size[1])),
                color,
                -1,
            )
            cv.putText(
                img_cpy,
                text,
                (x0, y0 + txt_size[1]),
                font,
                font_scale,
                txt_color_dark,
                thickness=thickness + 1,
            )
            cv.putText(
                img_cpy,
                text,
                (x0, y0 + txt_size[1]),
                font,
                font_scale,
                txt_color_light,
                thickness=thickness,
            )
            if DB_USE_CONF_MODEL or obj["confidence"] >= DB_CONF:
                logger.info(f"Saving to DB: {DB_USE_CONF_MODEL=} {DB_CONF} {confi}")
                flag_db = True
                detection_results.append(obj)

        if flag_db:
            save_detection_results(
                detection_results=detection_results, image=image, cursor=db_cursor
            )

    # logger.info("Finished draw_results")
    return img_cpy


def filter_model_result_by_area(model_results, bounding_area):
    """
    Проверяет, попадают ли все объекты модели в ограничивающую область.

    Args:
        model_results: Результат детекции модели в формате OBB или AABB.
        bounding_area: Словарь с координатами четырех углов ограничивающей области.

    Returns:
       model_results: Обновленный список объектов с добавленным флагом "in_area".
    """

    for obj in model_results:
        detection = obj["bbox"]
        obb = "obb" in obj and obj["obb"]
        if check_detection_in_area_list(detection, bounding_area, obb):
            obj["in_area"] = True
        else:
            obj["in_area"] = False
    return model_results


def check_detection_in_area_list(detection, bounding_area, obb=False):
    """
    Проверяет, попадает ли хотя бы два угла объекта в ограничивающую область.

    Args:
        detection: Результат детекции модели YOLO в формате OBB или AABB.
            Для OBB: список координат углов.
            Для AABB: кортеж (x1, y1, x2, y2).
        bounding_area: Список координат углов ограничивающей области.
        obb: Флаг, указывающий, является ли результат детекции OBB (True) или AABB (False).

    Returns:
        bool: True, если хотя бы два угла попадают в область, иначе False.
    """

    detection_points = (
        np.array(detection)
        if obb
        else np.array(
            [
                [detection[0], detection[1]],
                [detection[2], detection[1]],
                [detection[0], detection[3]],
                [detection[2], detection[3]],
            ]
        )
    )
    bounding_points = np.array(bounding_area)

    # Проверка для каждого угла детекции
    inside_count = np.sum(
        np.all(
            np.logical_and(
                detection_points[:, None, :] >= bounding_points.min(axis=0),
                detection_points[:, None, :] <= bounding_points.max(axis=0),
            ),
            axis=2,
        )
    )

    return inside_count >= 2
