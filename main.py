import sys

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QLabel,
    QGridLayout,
    QWidgetAction,
    QMessageBox,
    QCheckBox,
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QTimer, Qt, pyqtSlot, QMutexLocker, QMutex, QEvent

from src.ui.setting_window import SettingWindow
from src.ui.tab_widget import TabWindow
from src.utils.logging_config import logger
from src.utils.db_config import (
    create_connection_pool,
    terminate_idle_connections,
    check_disk_space,
)
from src.utils.config import config

DB_SAVE = config.last_state.db_save
PREFERENCE = config.last_state.preference


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multi-Camera AI Viewer")
        # Загрузка последней открытой вкладки
        self.tab_widget = QTabWidget()
        self.load_last_state()
        self.start_check()
        DB_SAVE = config.last_state.db_save
        self.conn_pool = create_connection_pool() if DB_SAVE == "DataBase" else None
        self.setCentralWidget(self.tab_widget)
        self.create_menu()
        self.create_tabs()
        self.installEventFilter(self)

        # Таймер для отслеживания времени на вкладке
        self.timer = QTimer(self)
        self.timer.setInterval(10000)  # 10 секунд
        self.timer.timeout.connect(self.handle_tab_timeout)

        # Подключение сигнала изменения вкладки
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        # Подключение сигнала обновления вкладки
        self.settings_window.settings_signal.connect(self.update_tab)

        # Мьютексы для контроля обновлений
        self.label_mutexes = [QMutex() for _ in range(4)]

        self.loading_message_box = QMessageBox(self)
        self.loading_message_box.setStandardButtons(QMessageBox.StandardButton.NoButton)
        self.loading_message_box.setWindowTitle("Информация")
        self.loading_message_box.setText("Загрузка источников...")
        self.loading_message_box.setIcon(QMessageBox.Icon.Information)
        self.loading_message_box.setModal(True)  # Сделать диалог модальным
        self.loading_message_box.show()

        # Начать последовательное открытие вкладок
        self.tab_switch_timer = QTimer(self)
        self.tab_switch_timer.setInterval(2000)  # 2 секунды
        self.tab_switch_timer.timeout.connect(self.switch_tabs)

        self.tab_switch_index = 0
        self.total_tabs = len(self.tab_widget) - 1  # количество вкладок
        self.return_to_saved_tab = self.current_tab_index
        self.is_switching = True  # Флаг для управления переключением вкладок

        # Запуск переключения вкладок после создания всех вкладок
        QTimer.singleShot(100, self.start_tab_switching)

    def start_check(self):
        if config.last_state.db_save != "Disabled" and not check_disk_space(
            threshold_percentage=50, path="/"
        ):
            config.last_state.db_save = "Disabled"
            logger.warning("Недостаточно места на диске для сохранения")
            print("Недостаточно места на диске для сохранения")
            QMessageBox.warning(
                self,
                "Предупреждение",
                "Недостаточно места на диске\n Вызовете администратора.\n Для продолжения нажмите ОК",
            )

    def start_tab_switching(self):
        if self.total_tabs > 0:
            self.loading_message_box.show()  # Показать сообщение о загрузке
            self.tab_widget.setCurrentIndex(1)  # Начинаем с первой вкладки после All Cameras
            self.tab_switch_timer.start()

    def switch_tabs(self):
        self.tab_widget.setCurrentIndex(self.tab_switch_index + 1)
        self.tab_switch_index += 1

        if self.tab_switch_index >= self.total_tabs:
            self.tab_switch_timer.stop()
            self.tab_widget.setCurrentIndex(
                self.return_to_saved_tab
            )  # Вернуться к сохраненной вкладке
            self.loading_message_box.hide()  # Скрыть сообщение о загрузке
            self.is_switching = False

    def create_menu(self):
        menubar = self.menuBar()

        # Создаем меню "AiWorkers"
        aiworkers_menu = menubar.addMenu("AiWorkers")
        cameras = ["Cam 1", "Cam 2", "Cam 3", "Cam 4"]
        self.aiworkers_checkboxes = {}  # Переменные для чекбоксов

        for cam in cameras:
            # Создаем действие для чекбокса с названием камеры и опцией "All Camera"
            all_camera_action = QWidgetAction(self)
            all_camera_checkbox = QCheckBox(f"{cam} All Camera", self)
            all_camera_checkbox.setChecked(True)  # Установить по умолчанию
            all_camera_action.setDefaultWidget(all_camera_checkbox)

            # Добавляем действие в меню "AiWorkers"
            aiworkers_menu.addAction(all_camera_action)

            # Сохраняем чекбоксы в словарь
            self.aiworkers_checkboxes[cam] = {
                "all_camera": all_camera_checkbox,
            }

            # Подключаем логику для чекбоксов
            all_camera_checkbox.stateChanged.connect(
                lambda state, cam=cam: self.on_checkbox_changed(cam, "all_camera", state)
            )

    def on_checkbox_changed(self, cam, checkbox_type, state):
        index = int(cam.split(" ")[1]) - 1
        if self.current_tab_index == 0 and checkbox_type == "all_camera":
            if state:
                self.resume_processing_for_thread(index)
            else:
                self.pause_processing_for_thread(index)

    @pyqtSlot(int)
    def update_tab(self, i):
        camera = self.backgrounds[i]
        camera.stop_video()
        camera.update_tab_out(i)

    def create_tabs(self):
        all_cameras_tab = QWidget()
        grid_layout = QGridLayout()
        self.video_widgets = []
        self.all_camera_labels = []

        for i in range(4):
            if self.conn_pool is not None:
                db = self.conn_pool.getconn()
                db.autocommit = True
            else:
                db = None
            video_widget = TabWindow(tab_index=i, db=db, parent=self)
            self.video_widgets.append(video_widget)
            label = QLabel(self)
            self.all_camera_labels.append(label)
            grid_layout.addWidget(label, i // 2, i % 2)
            video_widget.frame_ready.connect(self.update_all_camera_label(i))

        all_cameras_tab.setLayout(grid_layout)
        self.tab_widget.addTab(all_cameras_tab, "All Cameras")

        self.backgrounds = []
        for i in range(4):
            background = QWidget()
            layout = QVBoxLayout()
            video_widget = self.video_widgets[i]
            layout.addWidget(video_widget)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
            background.setLayout(layout)
            self.tab_widget.addTab(background, f"Camera {i + 1}")
            self.backgrounds.append(video_widget)

        if PREFERENCE:
            self.settings_window = SettingWindow(parent=self, main_window=self)
            self.settings_tab = QWidget()
            settings_layout = QVBoxLayout()
            settings_layout.addWidget(self.settings_window)
            self.settings_tab.setLayout(settings_layout)
            self.tab_widget.addTab(self.settings_tab, "Settings")

    def update_all_camera_label(self, index):
        def update_label(image):
            # logger.debug(f"Updating label for camera {index}")
            with QMutexLocker(self.label_mutexes[index]):
                pixmap = QPixmap.fromImage(image)
                label_size = self.all_camera_labels[index].size()
                scaled_pixmap = pixmap.scaled(
                    label_size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
                self.all_camera_labels[index].setPixmap(scaled_pixmap)

        return update_label

    def start_processing(self):
        logger.debug("Starting processing for all video widgets")
        for widget in self.video_widgets:
            widget.start_process()

    @pyqtSlot(int)
    def on_tab_changed(self, index):
        logger.debug(f"Tab changed to index {index}")
        self.current_tab_index = index
        if index == 0:
            # Вкладка "All Cameras"
            logger.debug("Resuming all processing")
            self.resume_all_processing()
            self.timer.stop()
            logger.debug("Processing resumed for all cameras")
        elif index == 5:
            # Вкладка настройки
            self.pause_all_processing_except(index - 1)
            self.timer.stop()
            return
        else:
            # Вкладка одной камеры
            logger.debug(f"Resuming processing for camera {index}")
            self.timer.start()
            self.resume_processing_for_thread(index - 1)

    def handle_tab_timeout(self):
        if self.current_tab_index != 0:
            logger.debug(f"Handling timeout for tab {self.current_tab_index}")
            self.pause_all_processing_except(self.current_tab_index - 1)
            self.timer.stop()
            logger.debug("Processing paused due to tab timeout")

    def resume_all_processing(self):
        logger.debug("Resuming processing for all threads")
        for index in range(4):
            if self.aiworkers_checkboxes[f"Cam {index+1}"]["all_camera"].isChecked():
                self.resume_processing_for_thread(index)
                logger.debug(f"Resuming processing for thread {index}")
            else:
                self.video_widgets[index].pause_ai_processing()
                logger.debug(f"Pausing processing for thread {index}")

    def pause_all_processing_except(self, except_index):
        for i, widget in enumerate(self.video_widgets):
            if i != except_index:
                widget.pause_ai_processing()
        logger.debug(f"Pausing all processing except tab {except_index}")

    def resume_processing_for_thread(self, index):
        self.video_widgets[index].resume_ai_processing()
        logger.debug(f"Resuming processing for thread {index}")

    def pause_processing_for_thread(self, index):
        self.video_widgets[index].pause_ai_processing()
        logger.debug(f"Pausing processing for thread {index}")

    def save_last_state(self):
        logger.debug("Saving last state")
        config.last_state.state_close_connection_pool = self.state_close_connection_pool
        if self.current_tab_index == 5:
            config.last_state.last_opened_tab = 0
        else:
            config.last_state.last_opened_tab = self.current_tab_index

        config.to_json()

    def load_last_state(self):

        self.state_close_connection_pool = config.last_state.state_close_connection_pool
        self.current_tab_index = config.last_state.last_opened_tab
        self.tab_widget.setCurrentIndex(self.current_tab_index)

        if DB_SAVE == "DataBase":
            if not self.state_close_connection_pool:
                terminate_idle_connections()
            self.state_close_connection_pool = False
            self.save_last_state()

    def close_connection_pool(self):
        if self.conn_pool is not None:
            try:
                self.conn_pool.closeall()
                logger.debug("Пул соединений успешно закрыт")
            except Exception as e:
                logger.error(f"Ошибка при закрытии пула соединений: {str(e)}")

    def closeEvent(self, event):
        self.close_connection_pool()
        self.state_close_connection_pool = True
        self.save_last_state()
        logger.debug("Application closed")
        super().closeEvent(event)

    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Escape:
            # Проверяем, активна ли вкладка настроек
            if self.current_tab_index == 5:
                # Передаём событие в label_display, который находится в settings_window
                self.settings_window.label_display.keyPressEvent(event)
                return True  # Событие обработано
        return super().eventFilter(source, event)


class Application(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.main_window = MainWindow()
        self.main_window.showMaximized()


if __name__ == "__main__":
    logger.debug("Starting application")
    app = Application(sys.argv)
    exit_code = app.exec()
    sys.exit(exit_code)
