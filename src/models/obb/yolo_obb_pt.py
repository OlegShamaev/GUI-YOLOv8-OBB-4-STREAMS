from ultralytics import YOLO
import numpy as np
import cv2 as cv

from src.models.base.yolov8_base import YoloPredictorBase, Model
from src.models.base.yolov8_base import ModelError
from src.utils.general import get_classes
from src.utils.logging_config import logger
from src.utils.db_config import save_detection_results
from src.utils.config import config

DB_CONF = config.last_state.db_confidence
DB_USE_CONF_MODEL = config.last_state.db_use_conf_model


class YoloObbPT(YoloPredictorBase):
    def __init__(self):
        self._model = None

    def init(self, model_path, class_txt_path, confidence_threshold=0.3, iou_threshold=0.45):
        """
        Инициализация детектора YOLOv8-OBB.
        """
        _yolo = YOLO(model_path)
        _class_names = get_classes(class_txt_path)

        self._model = Model(
            model=_yolo,
            confidence_threshold=confidence_threshold,
            iou_threshold=iou_threshold,
            input_size=(640, 640),
            class_names=_class_names,
        )

    def postprocess(self, model_output, class_names):
        detection_results = []
        i = 0
        for det in model_output[0].obb:
            try:
                name_cls = class_names[int(det.cls)]
            except:
                name_cls = f"Not_in_List: {int(det.cls)}"
                logger.exception(f"Class index {det.cls} not in the txt file")

            obj_dict = {
                "id": int(i),
                "class": name_cls,
                "class_index": int(det.cls),
                "confidence": float(det.conf),
                "bbox": np.array(det.xyxyxyxyn),
                "obb": True,
                "keypoints": np.array([]),
                "segmentation": np.array([]),
            }
            detection_results.append(obj_dict)
            i += 1
        return detection_results

    def inference(
        self,
        image,
        confi_thres=None,
        iou_thres=None,
    ):
        """
        Обработка изображения с помощью YOLOv8-OBB.
        """
        if self._model.model is None:
            raise ModelError("Model not initialized. Have you called init()?")
        if confi_thres is None:
            confi_thres = self._model.confidence_threshold
        if iou_thres is None:
            iou_thres = self._model.iou_threshold

        model_output = self._model.model(
            image,
            conf=confi_thres,
            iou=iou_thres,
            verbose=False,
            save=False
        )

        if model_output[0].obb.conf is not None and model_output[0].obb.conf.numel() > 0:
            # logger.debug(f"{model_output[0].obb=}")
            # logger.debug(f"{model_output=}")
            detection_results = self.postprocess(
                model_output=model_output,
                class_names=self._model.class_names,
            )
            return detection_results
        else:
            return []
