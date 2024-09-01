from src.qt.stream.video_capture import VideoProcessingThread
from src.qt.stream.visualize import VideoVisualizationThread
from src.qt.stream.ai_worker import AiWorkerThread
from src.ui.ui_setting_gui import Ui_MainWindow

from src.utils.logging_config import logger
from src.utils.config import config

import sys
import cv2 as cv

from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6 import QtWidgets, QtGui


class SettingWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    settings_signal = pyqtSignal(int)

    def __init__(self, parent=None, main_window=None):

        super(SettingWindow, self).__init__(parent)
        self.setupUi(self)
        self.main_window = main_window
        self.ai_thread = AiWorkerThread(tab_index=4)
        self.display_thread = VideoVisualizationThread()
        self.video_processing_thread = VideoProcessingThread()

        self.conf_thr = 0.3
        self.iou_thr = 0.45
        self.frame_interval = 0
        self.tab_out = None
        self.source_in = None
        self.source_value = None
        self.model_name = "yolov8n"
        self.in_out_area = "IN"
        self.display_area = None
        self.play_pause_flag = False

        self.init_slots()
        self.buttons_states("waiting_for_setting")

    def init_slots(self):
        self.radioButton_in.toggled.connect(lambda: self.get_area_in_out(self.radioButton_in))
        self.radioButton_out.toggled.connect(lambda: self.get_area_in_out(self.radioButton_out))
        self.doubleSpinBox_conf.valueChanged.connect(
            lambda x: self.update_parameter(x, "doubleSpinBox_conf")
        )
        self.doubleSpinBox_interval.valueChanged.connect(
            lambda x: self.update_parameter(x, "doubleSpinBox_interval")
        )
        self.doubleSpinBox_iou.valueChanged.connect(
            lambda x: self.update_parameter(x, "doubleSpinBox_iou")
        )
        self.horizontalSlider_conf.valueChanged.connect(
            lambda x: self.update_parameter(x, "horizontalSlider_conf")
        )
        self.horizontalSlider_interval.valueChanged.connect(
            lambda x: self.update_parameter(x, "horizontalSlider_interval")
        )
        self.horizontalSlider_iou.valueChanged.connect(
            lambda x: self.update_parameter(x, "horizontalSlider_iou")
        )
        self.comboBox_tabs.currentIndexChanged.connect(self.choose_tab)
        self.comboBox_model.currentTextChanged.connect(self.choose_model)
        self.pushButton_cam.clicked.connect(lambda: self.process_camera())
        self.pushButton_file.clicked.connect(lambda: self.process_file())
        self.pushButton_stop.clicked.connect(self.stop_video)
        self.pushButton_box_area.clicked.connect(self.show_box_area)
        self.pushButton_ok_area.clicked.connect(self.ok_area)
        self.pushButton_cancel_area.clicked.connect(self.cancel_area)
        self.pushButton_apply.clicked.connect(self.apply_changes)
        self.pushButton_play.clicked.connect(self.play_pause)

    def update_progress_bar(self, value):
        self.progressBar_play.setValue(value)

    def resizeEvent(self, event: QtGui.QResizeEvent):
        self.screen_size = (self.label_display.width(), self.label_display.height())
        self.display_thread.get_screen_size(self.screen_size)
        QtWidgets.QMainWindow.resizeEvent(self, event)

    def play_pause(self):
        if self.play_pause_flag == False:
            self.ai_thread.pause_process()
            self.video_processing_thread.pause_process()
        elif self.play_pause_flag == True:
            self.ai_thread.resume_process()
            self.video_processing_thread.resume_process()
        self.play_pause_flag = not self.play_pause_flag

    def update_parameter(self, x, flag):
        if flag == "doubleSpinBox_conf":
            self.horizontalSlider_conf.setValue(int(x * 100))
            self.conf_thr = float(x)
        elif flag == "doubleSpinBox_interval":
            self.horizontalSlider_interval.setValue(int(x))
            self.frame_interval = int(x)
            self.video_processing_thread.set_frame_interval(self.frame_interval)
        elif flag == "doubleSpinBox_iou":
            self.horizontalSlider_iou.setValue(int(x * 100))
            self.iou_thr = float(x)
        elif flag == "horizontalSlider_conf":
            self.doubleSpinBox_conf.setValue(x / 100)
            self.conf_thr = float(x / 100)
        elif flag == "horizontalSlider_interval":
            self.doubleSpinBox_interval.setValue(x)
            self.frame_interval = int(x)
            self.video_processing_thread.set_frame_interval(self.frame_interval)
        elif flag == "horizontalSlider_iou":
            self.doubleSpinBox_iou.setValue(x / 100)
            self.iou_thr = float(x / 100)
        elif flag == "area":
            self.display_area = self.label_display.get_relative_corners()
        elif flag == "cancel":
            self.display_area = None
        if self.ai_thread.isRunning:
            self.ai_thread.set_confidence_threshold(self.conf_thr)
            self.ai_thread.set_iou_threshold(self.iou_thr)
        if self.display_thread.isRunning:
            self.display_thread.set_display_area(self.display_area)
            self.display_thread.set_in_out_area(self.in_out_area)

    def choose_tab(self):
        self.tab_out = self.comboBox_tabs.currentText()
        self.tab_out = self.tab_out.lower()

    def choose_model(self):
        self.model_name = self.comboBox_model.currentText()
        self.model_name = self.model_name.lower()

    def buttons_states(self, work_state):
        if work_state == "waiting_for_setting":
            self.radioButton_in.setDisabled(True)
            self.radioButton_out.setDisabled(True)
            self.comboBox_tabs.setDisabled(False)
            self.comboBox_model.setDisabled(False)
            self.pushButton_cam.setDisabled(False)
            self.pushButton_file.setDisabled(False)
            self.pushButton_play.setDisabled(True)
            self.pushButton_stop.setDisabled(True)
            self.pushButton_box_area.setDisabled(True)
            self.pushButton_ok_area.setDisabled(True)
            self.pushButton_cancel_area.setDisabled(True)
            self.pushButton_apply.setDisabled(True)
            self.doubleSpinBox_conf.setDisabled(False)
            self.horizontalSlider_conf.setDisabled(False)
            self.doubleSpinBox_interval.setDisabled(False)
            self.horizontalSlider_interval.setDisabled(False)
            self.doubleSpinBox_iou.setDisabled(False)
            self.horizontalSlider_iou.setDisabled(False)
            self.doubleSpinBox_interval.setDisabled(False)
            self.horizontalSlider_interval.setDisabled(False)
        elif work_state == "processing":
            self.pushButton_play.click
            self.radioButton_in.setDisabled(False)
            self.radioButton_out.setDisabled(False)
            self.comboBox_tabs.setDisabled(False)
            self.comboBox_model.setDisabled(True)
            self.pushButton_cam.setDisabled(True)
            self.pushButton_file.setDisabled(True)
            self.pushButton_play.setDisabled(False)
            self.pushButton_stop.setDisabled(False)
            self.pushButton_box_area.setDisabled(False)
            self.pushButton_ok_area.setDisabled(True)
            self.pushButton_cancel_area.setDisabled(True)
            self.pushButton_apply.setDisabled(False)
            self.doubleSpinBox_conf.setDisabled(False)
            self.horizontalSlider_conf.setDisabled(False)
            self.doubleSpinBox_interval.setDisabled(True)
            self.horizontalSlider_interval.setDisabled(False)
            self.doubleSpinBox_iou.setDisabled(False)
            self.horizontalSlider_iou.setDisabled(False)
            self.doubleSpinBox_interval.setDisabled(False)
            self.horizontalSlider_interval.setDisabled(False)

    def show_box_area(self):
        self.label_display.toggle_rect(True)
        self.pushButton_ok_area.setEnabled(True)
        self.pushButton_box_area.setEnabled(False)
        self.pushButton_cancel_area.setEnabled(True)
        self.pushButton_apply.setEnabled(False)

    def ok_area(self):
        self.update_parameter(x=None, flag="area")
        self.label_display.toggle_rect(False)
        self.pushButton_apply.setEnabled(True)
        self.pushButton_box_area.setEnabled(False)
        self.pushButton_ok_area.setEnabled(False)

    def get_area_in_out(self, btn):
        if btn.text() == "IN":
            if btn.isChecked() == True:
                self.in_out_area = "IN"
        elif btn.text() == "OUT":
            if btn.isChecked() == True:
                self.in_out_area = "OUT"

    def cancel_area(self):
        self.update_parameter(x=None, flag="cancel")
        self.label_display.reset_rect_to_original()
        self.label_display.toggle_rect(False)
        self.pushButton_box_area.setEnabled(True)
        self.pushButton_ok_area.setEnabled(False)
        self.pushButton_cancel_area.setEnabled(False)

    def process_camera(self):
        self.source_value = self.get_stream_source()
        self.start_processing()
        self.source_in = "camera"

    def process_file(self):
        self.source_value = self.get_file_path()
        self.start_processing()
        self.source_in = "file"

    def start_processing(self):
        if self.source_value is not None:
            logger.info(f"SOURCE: {self.source_value}")
            self.ai_thread.set_start_config(
                model_name=self.model_name,
                confidence_threshold=self.conf_thr,
                iou_threshold=self.iou_thr,
                frame_interval=self.frame_interval,
            )

            self.video_processing_thread.set_start_config(video_source=self.source_value)
            self.display_thread.set_start_config(
                [self.label_display.width(), self.label_display.height()]
            )

            self.video_processing_thread.send_frame.connect(self.display_thread.get_fresh_frame)
            self.video_processing_thread.send_frame.connect(self.ai_thread.get_frame)
            self.video_processing_thread.send_play_progress.connect(self.update_progress_bar)
            self.ai_thread.send_ai_output.connect(self.display_thread.get_ai_output)
            self.display_thread.send_ai_output.connect(self.update_statistic_table)
            self.display_thread.send_displayable_frame.connect(self.update_display_frame)

            self.ai_thread.start()
            self.display_thread.start()
            self.video_processing_thread.start()

            self.buttons_states("processing")

    def stop_video(self):        
        self.cancel_area()        
        if self.ai_thread.isRunning():
            self.ai_thread.send_ai_output.disconnect(self.display_thread.get_ai_output)
            self.ai_thread.stop_process()
            self.ai_thread.quit()
            self.ai_thread.wait()
        if self.display_thread.isRunning():
            self.display_thread.send_displayable_frame.disconnect(self.update_display_frame)
            self.display_thread.stop_display()
            self.display_thread.quit()
            self.display_thread.wait()
        if self.video_processing_thread.isRunning():
            self.video_processing_thread.send_frame.disconnect(self.display_thread.get_fresh_frame)
            self.video_processing_thread.stop_capture()
            self.video_processing_thread.quit()
            self.video_processing_thread.wait()
        self.clean_table()        
        self.label_display.clear()
        self.buttons_states("waiting_for_setting")

    def update_display_frame(self, showImage):
        self.label_display.set_pixmap(QtGui.QPixmap.fromImage(showImage))

    def clean_table(self):
        while self.tableWidget_results.rowCount() > 0:
            self.tableWidget_results.removeRow(0)

    def update_statistic_table(self, ai_output):
        self.clean_table()
        self.tableWidget_results.setRowCount(0)
        if ai_output == []:
            return
        for box in ai_output:
            each_item = [
                str(box["id"]),
                str(box["class"]),
                "{:.1f}%".format(box["confidence"] * 100),
                str(box["bbox"]),
            ]
            row = self.tableWidget_results.rowCount()
            self.tableWidget_results.insertRow(row)
            for j in range(len(each_item)):
                item = QtWidgets.QTableWidgetItem(str(each_item[j]))
                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
                )
                self.tableWidget_results.setItem(row, j, item)

    def get_stream_source(self):
        while True:
            # Сначала определим локально подключенные камеры
            local_cameras = ["not selected"]
            index = 0
            while True:
                cap = cv.VideoCapture(index)
                if not cap.read()[0]:
                    break
                else:
                    local_cameras.append(f"Camera {index}")
                cap.release()
                index += 1

            # Создадим диалоговое окно для выбора камеры
            dialog = QtWidgets.QDialog(self)
            dialog.setWindowTitle("Select Camera or Enter RTSP")
            layout = QtWidgets.QVBoxLayout(dialog)

            # Добавим выпадающий список с найденными камерами и поле для ввода RTSP
            combo_box = QtWidgets.QComboBox(dialog)
            combo_box.addItems(local_cameras)
            combo_box.setCurrentText("not selected")
            layout.addWidget(combo_box)

            line_edit = QtWidgets.QLineEdit(dialog)
            line_edit.setPlaceholderText("Enter Camera ID or RTSP URL")
            layout.addWidget(line_edit)

            # Добавим кнопки OK и Cancel
            button_box = QtWidgets.QDialogButtonBox(
                QtWidgets.QDialogButtonBox.StandardButton.Ok
                | QtWidgets.QDialogButtonBox.StandardButton.Cancel,
                dialog,
            )
            layout.addWidget(button_box)

            button_box.accepted.connect(dialog.accept)
            button_box.rejected.connect(dialog.reject)

            if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                selected_camera = combo_box.currentText()
                entered_text = line_edit.text()

                if entered_text:
                    if entered_text.isdigit():
                        return int(entered_text)
                    elif entered_text.startswith("rtsp://"):
                        return entered_text
                    else:
                        QtWidgets.QMessageBox.warning(
                            self, "Invalid Input", "Please enter a valid Camera ID or RTSP URL."
                        )
                else:
                    if selected_camera and selected_camera != "not selected":
                        return int(selected_camera.split()[1])
                    else:
                        QtWidgets.QMessageBox.warning(
                            self,
                            "No Camera Selected",
                            "Please select a camera from the list or enter a Camera ID or RTSP URL.",
                        )
            else:
                return None

    def get_file_path(self):
        img_fm = (
            ".tif",
            ".tiff",
            ".jpg",
            ".jpeg",
            ".gif",
            ".png",
            ".eps",
            ".raw",
            ".cr2",
            ".nef",
            ".orf",
            ".sr2",
            ".bmp",
            ".ppm",
            ".heif",
        )
        vid_fm = (".flv", ".avi", ".mp4", ".3gp", ".mov", ".webm", ".ogg", ".qt", ".avchd")
        file_list = " *".join(img_fm + vid_fm)
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "choose an image or video file", "./data", f"Files({file_list})"
        )
        if file_name == "":
            return None

        return file_name
    
    def reset_settings(self):
        self.source_in = None
        self.source_value = None
        self.stop_video()

    def apply_changes(self):
        # Проверка выбора вкладки
        if self.comboBox_tabs.currentIndex() == -1:
            QtWidgets.QMessageBox.warning(
                self, "Ошибка", "Пожалуйста, выберите вкладку перед сохранением."
            )
            return
        tab_index = self.comboBox_tabs.currentIndex()
        cam_number = f"cam_{tab_index + 1}"
        config.tabs[cam_number].tab_out = tab_index
        config.tabs[cam_number].confidence_threshold = self.doubleSpinBox_conf.value()
        config.tabs[cam_number].iou_threshold = self.doubleSpinBox_iou.value()
        config.tabs[cam_number].frame_interval = int(self.doubleSpinBox_interval.value())
        config.tabs[cam_number].source_in = self.source_in
        config.tabs[cam_number].source_value = self.source_value
        config.tabs[cam_number].yolo_name = self.comboBox_model.currentText().lower()
        config.tabs[cam_number].in_out_area = self.in_out_area
        config.tabs[cam_number].display_area = self.display_area

        config.to_json()

        QtWidgets.QMessageBox.information(self, "Сохранение", "Настройки успешно сохранены.")

        # Сброс настроек к начальному состоянию
        self.reset_settings()

        self.settings_signal.emit(self.comboBox_tabs.currentIndex())
        # Переход на выбранную вкладку
        if self.main_window:
            self.main_window.tab_widget.setCurrentIndex(tab_index + 1)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = SettingWindow()
    mainWindow.show()
    sys.exit(app.exec())
