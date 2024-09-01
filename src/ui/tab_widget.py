from src.qt.stream.video_capture import VideoProcessingThread
from src.qt.stream.visualize import VideoVisualizationThread
from src.qt.stream.ai_worker import AiWorkerThread

from src.ui.ui_tab_widget import Ui_TabWindow

from PyQt6.QtCore import pyqtSignal, QEvent
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtGui import QImage
from src.utils.logging_config import logger
from src.utils.config import config


class TabWindow(QtWidgets.QMainWindow, Ui_TabWindow):

    frame_ready = pyqtSignal(QImage)

    def __init__(self, tab_index: int, db=None, parent=None):

        super(TabWindow, self).__init__(parent)
        self.setupUi(self)
        self.tab_index = tab_index
        self.ai_thread = AiWorkerThread(tab_index=self.tab_index)
        self.display_thread = VideoVisualizationThread(db=db)
        self.video_processing_thread = VideoProcessingThread()

        self.get_config()

    def get_config(self):
        self.cam_number = f"cam_{self.tab_index + 1}"
        self.conf_thr = config.tabs[self.cam_number].confidence_threshold
        self.iou_thr = config.tabs[self.cam_number].iou_threshold
        self.frame_interval = config.tabs[self.cam_number].frame_interval
        self.source_value = config.tabs[self.cam_number].source_value
        self.model_name = config.tabs[self.cam_number].yolo_name

    def start_process(self):
        logger.info(f" {self.cam_number} SOURCE: {self.source_value}")

        if self.source_value is not None:
            self.ai_thread.set_start_config(
                model_name=self.model_name,
                confidence_threshold=self.conf_thr,
                iou_threshold=self.iou_thr,
                frame_interval=self.frame_interval,
            )

            self.video_processing_thread.set_start_config(video_source=self.source_value)
            self.display_thread.set_start_config(
                [self.label_display.width(), self.label_display.height()], tab_index=self.tab_index
            )

            self.video_processing_thread.send_frame.connect(self.display_thread.get_fresh_frame)
            self.video_processing_thread.send_frame.connect(self.ai_thread.get_frame)
            self.ai_thread.send_ai_output.connect(self.display_thread.get_ai_output)
            self.display_thread.send_displayable_frame.connect(self.update_display_frame)

            self.ai_thread.start()
            self.display_thread.start()
            self.video_processing_thread.start()

            self.display_thread.send_displayable_frame.connect(self.on_frame_ready)

    def on_frame_ready(self, image: QImage):
        self.frame_ready.emit(image)

    def update_tab_out(self, tab_out):
        self.tab_index = tab_out
        self.get_config()
        self.init_process()
        self.start_process()

    def init_process(self):
        self.ai_thread.__init__()
        self.display_thread.__init__()
        self.video_processing_thread.__init__()
    
    def showEvent(self, event: QEvent):
        super(TabWindow, self).showEvent(event)
        if not event.spontaneous() and not self.display_thread.isRunning():
            self.start_process()

    def resizeEvent(self, event: QtGui.QResizeEvent):
        self.screen_size = (self.label_display.width(), self.label_display.height())
        self.display_thread.get_screen_size(self.screen_size)
        QtWidgets.QMainWindow.resizeEvent(self, event)

    def stop_video(self):
        if self.ai_thread.isRunning():
            self.ai_thread.send_ai_output.disconnect(self.display_thread.get_ai_output)
            self.ai_thread.stop_process()
        if self.display_thread.isRunning():
            self.display_thread.send_displayable_frame.disconnect(self.update_display_frame)
            self.display_thread.stop_display()
        if self.video_processing_thread.isRunning():
            self.video_processing_thread.send_frame.disconnect(self.display_thread.get_fresh_frame)
            self.video_processing_thread.stop_capture()
        self.ai_thread.quit()
        self.display_thread.quit()
        self.video_processing_thread.quit()
        self.label_display.clear()

    def update_display_frame(self, showImage):
        self.label_display.setPixmap(QtGui.QPixmap.fromImage(showImage))

    def resume_ai_processing(self):
        if self.ai_thread.isRunning():
            if not self.ai_thread.is_paused():
                logger.debug(f"AI ALREADY RUNNING {self.tab_index}")
                return
            else:
                self.ai_thread.resume_process()
                logger.debug(f"AI RESUMED {self.tab_index}")
        else:
            self.ai_thread.start()
            logger.debug(f"AI STARTED {self.tab_index}")

    def pause_ai_processing(self):
        if not self.ai_thread.isRunning():
            logger.debug(f"AI NOT RUNNING {self.tab_index}")
            return
        elif self.ai_thread.is_paused():
            logger.debug(f"AI ALREADY PAUSED {self.tab_index}")
        else:
            self.ai_thread.pause_process()
            logger.debug(f"AI PAUSED {self.tab_index}")
