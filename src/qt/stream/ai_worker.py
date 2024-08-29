from PyQt6.QtCore import QThread, pyqtSignal, QMutex, QWaitCondition
from src.models.obb.yolo_obb_pt import YoloObbPT
from src.data_type.video_buffer import LatestFrame
from src.utils.general import ROOT, add_image_id
import os
import asyncio


class AiWorkerThread(QThread):
    send_ai_output = pyqtSignal(list)

    def __init__(self, tab_index: int = 0):
        super(AiWorkerThread, self).__init__()
        self.thread_name = "AiWorkerThread"
        self.threadFlag = False
        self.paused = False
        self.mutex = QMutex()
        self.condition = QWaitCondition()
        self.tab_index = tab_index

    def set_start_config(
        self,
        model_name="yolov8n",
        confidence_threshold=0.5,
        iou_threshold=0.45,
        frame_interval=0,
    ):
        self.threadFlag = True
        self.latest_frame = LatestFrame()
        self.confi_thr = confidence_threshold
        self.iou_thr = iou_threshold
        self.frame_interval = frame_interval
        self.model_name = model_name
        self._init_yolo()

    def set_iou_threshold(self, iou_threshold):
        self.iou_thr = iou_threshold

    def set_confidence_threshold(self, confidence_threshold):
        self.confi_thr = confidence_threshold

    def set_model_name(self, model_name):
        self.model_name = model_name

    def _init_yolo(self):
        self.obb_detector = YoloObbPT()
        self.obb_detector.init(
            model_path=os.path.join(ROOT, f"models/weights/{self.model_name}-obb.pt"),
            class_txt_path=os.path.join(ROOT, f"models/classes.txt"),
            confidence_threshold=self.confi_thr,
            iou_threshold=self.iou_thr,
        )

    def get_frame(self, frame_list):
        self.latest_frame.put(frame=frame_list[1], frame_id=frame_list[0], realtime=True)

    def stop_process(self):
        self.resume_process()  # To exit the wait condition if paused
        self.threadFlag = False

    def pause_process(self):
        self.mutex.lock()
        self.paused = True
        self.mutex.unlock()

    def resume_process(self):
        self.mutex.lock()
        self.paused = False
        self.condition.wakeAll()
        self.mutex.unlock()

    def is_paused(self):
        return self.paused

    async def async_run(self):
        first_frame = True
        frame_count = 0

        while self.threadFlag:
            frame_id, frame = self.latest_frame.get()
            if frame_id is None:
                break

            self.mutex.lock()
            while self.paused:
                self.condition.wait(self.mutex)
            self.mutex.unlock()

            if self.frame_interval == 0 or frame_count == self.frame_interval + 1 or first_frame:
                model_output = []

                model_output = self.obb_detector.inference(frame, self.confi_thr, self.iou_thr)

                model_output = add_image_id(model_output, frame_id)

                # logger.debug(f"AI: {self.tab_index} Frame ID: {frame_id}")
                frame_count = 0
                first_frame = False

            self.send_ai_output.emit(model_output)

            if self.frame_interval != 0:
                frame_count += 1

            await asyncio.sleep(0.01)

    def run(self):
        asyncio.run(self.async_run())
