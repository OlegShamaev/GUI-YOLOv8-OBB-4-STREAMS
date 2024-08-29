from src.data_type.video_buffer import FrameBuffer
from src.utils.visualize import draw_results
from src.utils.logging_config import logger
from src.utils.config import config

from PyQt6.QtCore import QThread, pyqtSignal, QMutex, QWaitCondition
from PyQt6.QtGui import QImage
import cv2 as cv
import numpy as np
import copy


class VideoVisualizationThread(QThread):
    send_displayable_frame = pyqtSignal(QImage)
    send_ai_output = pyqtSignal(list)

    def __init__(self, db=None):
        super(VideoVisualizationThread, self).__init__()
        self.thread_name = "VideoVisualizationThread"
        self.db = db
        self.threadFlag = False
        self.paused = False
        self.mutex = QMutex()
        self.condition = QWaitCondition()

    def set_start_config(self, screen_size, tab_index=None):
        self.tab_index = tab_index
        self.threadFlag = True
        self.frame_buffer = FrameBuffer(10)
        self.ai_output = []
        self.get_screen_size(screen_size)
        self.get_area()

    def set_display_area(self, area):
        self.area = area

    def set_in_out_area(self, in_out_area):
        self.in_out_area = in_out_area

    def get_fresh_frame(self, frame_list):
        self.frame_buffer.put(
            frame=copy.deepcopy(frame_list[1]), frame_id=frame_list[0], realtime=True
        )

    def get_ai_output(self, ai_output):
        self.ai_output = copy.deepcopy(ai_output)

    def get_screen_size(self, screen_size):
        self.iw, self.ih = screen_size

    def get_area(self):
        if self.tab_index is not None:
            tab = f"cam_{self.tab_index + 1}"
            self.in_out_area = config.tabs[tab].in_out_area
            if config.tabs[tab].display_area is not None:
                self.area = config.tabs[tab].display_area
            else:
                self.area = None
        else:
            self.area = None
            self.in_out_area = "IN"

    def is_paused(self):
        return self.paused

    def pause_process(self):
        self.mutex.lock()
        self.paused = True
        self.mutex.unlock()

    def resume_process(self):
        self.mutex.lock()
        self.paused = False
        self.condition.wakeAll()
        self.mutex.unlock()

    def stop_display(self):
        self.resume_process()
        self.threadFlag = False

    def run(self):
        logger.info("Start video visualization")

        if self.db is not None:
            db_cursor = self.db.cursor()
        else:
            db_cursor = None

        while self.threadFlag:

            self.mutex.lock()
            while self.paused:
                self.condition.wait(self.mutex)
            self.mutex.unlock()

            frame_id, frame = self.frame_buffer.get()

            if frame_id is not None:
                frame = draw_results(
                    frame,
                    self.ai_output,
                    self.area,
                    self.in_out_area,
                    db_cursor=db_cursor,
                )
                # logger.debug("draw finish")
                show_image = self.convert_cv_qt(frame, self.ih, self.iw)
                self.send_displayable_frame.emit(show_image)
                self.send_ai_output.emit(self.ai_output)
            else:
                break
        blank_image = np.zeros((self.ih, self.iw, 3))
        blank_image = cv.cvtColor(blank_image.astype("uint8"), cv.COLOR_BGR2RGBA)
        show_image = QImage(
            blank_image.data,
            blank_image.shape[1],
            blank_image.shape[0],
            QImage.Format.Format_RGBA8888,
        )
        self.send_displayable_frame.emit(show_image)
        self.send_ai_output.emit([])

        if db_cursor is not None:
            if "cursor" in locals():
                db_cursor.close()

    def convert_cv_qt(self, image, screen_height, screen_width):
        h, w, _ = image.shape
        scale = min(screen_width / w, screen_height / h)
        nw, nh = int(scale * w), int(scale * h)
        image_resized = cv.resize(image, (nw, nh))
        image_paded = np.full(shape=[screen_height, screen_width, 3], fill_value=0)
        dw, dh = (screen_width - nw) // 2, (screen_height - nh) // 2
        image_paded[dh : nh + dh, dw : nw + dw, :] = image_resized
        image_paded = cv.cvtColor(image_paded.astype("uint8"), cv.COLOR_BGR2RGBA)
        return QImage(
            image_paded.data,
            image_paded.shape[1],
            image_paded.shape[0],
            QImage.Format.Format_RGBA8888,
        )
