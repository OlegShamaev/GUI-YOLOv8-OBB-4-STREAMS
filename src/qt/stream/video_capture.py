from PyQt6.QtCore import QThread, pyqtSignal, QMutex, QWaitCondition
import asyncio
import cv2 as cv
import time
import asyncio
from src.utils.logging_config import logger


class VideoProcessingThread(QThread):
    send_video_info = pyqtSignal(dict)
    send_frame = pyqtSignal(list)
    send_play_progress = pyqtSignal(int)

    def __init__(self):
        super(VideoProcessingThread, self).__init__()
        self.thread_name = "VideoFileThread"
        self.threadFlag = False
        self.paused = False
        self.mutex = QMutex()
        self.condition = QWaitCondition()

    def set_start_config(self, video_source):
        self.threadFlag = True
        self.get_video_source(video_source)

    def get_video_source(self, video_source):
        self.video_source = video_source

    def get_video_info(self, video_cap):
        video_info = {}
        fileFlag = False
        video_info["FPS"] = video_cap.get(cv.CAP_PROP_FPS)
        video_info["length"] = int(video_cap.get(cv.CAP_PROP_FRAME_COUNT))
        video_info["size"] = (
            int(video_cap.get(cv.CAP_PROP_FRAME_WIDTH)),
            int(video_cap.get(cv.CAP_PROP_FRAME_HEIGHT)),
        )
        if video_info["length"] > 0:
            fileFlag = True
        return video_info, fileFlag

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

    def stop_capture(self):
        self.resume_process()
        self.threadFlag = False

    async def async_run(self):
        try:
            cap = cv.VideoCapture(self.video_source)
            if not cap.isOpened():
                raise IOError("Couldn't open stream")

            video_info, fileFlag = self.get_video_info(cap)
            self.send_video_info.emit(video_info)

            if fileFlag:
                fps = video_info["FPS"]
                frame_time = 1.0 / fps

            idx_frame = 0
            while self.threadFlag:

                self.mutex.lock()
                while self.paused:
                    self.condition.wait(self.mutex)
                self.mutex.unlock()

                if fileFlag:
                    start_time = time.time()
                ret, frame = cap.read()
                if ret is False or self.threadFlag is False:
                    break
                self.send_frame.emit([idx_frame, frame])
                idx_frame += 1

                if fileFlag:
                    self.send_play_progress.emit(int(idx_frame / video_info["length"] * 1000))
                    elapsed_time = time.time() - start_time
                    sleep_time = frame_time - elapsed_time
                    if sleep_time > 0:
                        time.sleep(sleep_time)

                await asyncio.sleep(0.01)

            self.send_frame.emit([None, None])
            cap.release()

        except Exception as e:
            logger.error(f"Error in VideoFileThread: {e}")

    def run(self):
        asyncio.run(self.async_run())
