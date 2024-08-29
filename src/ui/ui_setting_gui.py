# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file '
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt6.QtCore import (
    QCoreApplication,
    QMetaObject,
    QSize,
    Qt,
)
from PyQt6.QtGui import (
    QFont,
    QIcon,
)
from PyQt6.QtWidgets import (
    QAbstractScrollArea,
    QAbstractSpinBox,
    QComboBox,
    QDoubleSpinBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSizePolicy,
    QSlider,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
from PyQt6 import QtWidgets

from src.qt.stream.draw_area import BoxArea

from src.ui import apprcc_rc


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamilies(["Arial"])
        MainWindow.setFont(font)
        icon = QIcon()
        icon.addFile(":/images/icons/icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(
            "background-color: rgb(119, 118, 123);\n" "border-color: rgb(119, 118, 123);"
        )
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setFont(font)
        self.centralwidget.setStyleSheet(
            "background-color: rgb(119, 118, 123);\n" "border-color: rgb(119, 118, 123);"
        )
        self.horizontalLayout_4 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_8 = QGroupBox(self.centralwidget)
        self.groupBox_8.setObjectName("groupBox_8")
        self.groupBox_8.setFont(font)
        self.horizontalLayout_14 = QHBoxLayout(self.groupBox_8)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.comboBox_tabs = QComboBox(self.groupBox_8)
        self.comboBox_tabs.addItem("")
        self.comboBox_tabs.addItem("")
        self.comboBox_tabs.addItem("")
        self.comboBox_tabs.addItem("")
        self.comboBox_tabs.setObjectName("comboBox_tabs")
        self.comboBox_tabs.setFont(font)
        self.comboBox_tabs.setAutoFillBackground(False)
        self.comboBox_tabs.setStyleSheet(
            "QComboBox QAbstractItemView {\n"
            "font-size: 16px;\n"
            "outline:none;\n"
            "border:none;}\n"
            "\n"
            "QComboBox{\n"
            "font-size: 16px;\n"
            "\n"
            "color: rgb(218, 218, 218);\n"
            "border-width:0px;\n"
            "border-color:white;\n"
            "border-style:solid;\n"
            "background-color: rgba(200, 200, 200,50);}\n"
            "\n"
            "QComboBox::drop-down {\n"
            "margin-top:1;\n"
            "height:20;\n"
            "color: rgb(218, 218, 218);\n"
            "background-color: rgba(200, 200, 200,50);\n"
            "border-image: url(:/images/icons/roll_down.png);\n"
            "}\n"
            "\n"
            "QComboBox::disabled{\n"
            "color: rgb(0, 0, 0);\n"
            "}"
        )
        self.comboBox_tabs.setCurrentText("Camera 1")

        self.horizontalLayout_14.addWidget(self.comboBox_tabs)

        self.verticalLayout_2.addWidget(self.groupBox_8)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName("groupBox_3")
        self.groupBox_3.setMinimumSize(QSize(0, 0))
        font1 = QFont()
        font1.setFamilies(["Arial"])
        font1.setPointSize(13)
        font1.setBold(False)
        self.groupBox_3.setFont(font1)
        self.gridLayout = QGridLayout(self.groupBox_3)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_cam = QPushButton(self.groupBox_3)
        self.pushButton_cam.setObjectName("pushButton_cam")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_cam.sizePolicy().hasHeightForWidth())
        self.pushButton_cam.setSizePolicy(sizePolicy1)
        font2 = QFont()
        font2.setFamilies(["Arial"])
        font2.setBold(True)
        self.pushButton_cam.setFont(font2)
        self.pushButton_cam.setStyleSheet(
            "QPushButton{\n"
            "	image: url(:/images/icons/camera_on.png);\n"
            "font-size: 14px;\n"
            "font-weight: bold;\n"
            "color:white;\n"
            "text-align: center center;\n"
            "padding-left: 5px;\n"
            "padding-right: 5px;\n"
            "padding-top: 4px;\n"
            "padding-bottom: 4px;\n"
            "border-style: solid;\n"
            "border-width: 0px;\n"
            "border-color: rgba(255, 255, 255, 255);\n"
            "border-radius: 3px;\n"
            "background-color: rgba(200, 200, 200,0);}\n"
            "\n"
            "QPushButton:focus{outline: none;}\n"
            "\n"
            "QPushButton::pressed{\n"
            "                     font-size: 14px;\n"
            "                     font-weight: bold;\n"
            "                     color:rgb(200,200,200);\n"
            "                     text-align: center center;\n"
            "                     padding-left: 5px;\n"
            "                     padding-right: 5px;\n"
            "                     padding-top: 4px;\n"
            "                     padding-bottom: 4px;\n"
            "                     border-style: solid;\n"
            "                     border-width: 0px;\n"
            "                     border-color: rgba(255, 255, 255, 255);\n"
            "                   "
            "  border-radius: 3px;\n"
            "                     background-color:  #bf513b;}\n"
            "\n"
            "QPushButton::disabled{\n"
            "                     image: url(:/images/icons/camera_off.png);\n"
            "                     font-size: 14px;\n"
            "                     font-weight: bold;\n"
            "                     color:rgb(200,200,200);\n"
            "                     text-align: center center;\n"
            "                     padding-left: 5px;\n"
            "                     padding-right: 5px;\n"
            "                     padding-top: 4px;\n"
            "                     padding-bottom: 4px;\n"
            "                     border-style: solid;\n"
            "                     border-width: 0px;\n"
            "                     border-color: rgba(255, 255, 255, 255);\n"
            "                     border-radius: 3px;}\n"
            "QPushButton::hover {\n"
            "border-style: solid;\n"
            "border-width: 0px;\n"
            "border-radius: 0px;\n"
            "background-color: rgba(48,148,243,80);}url(:/images/icons/camera_on.png)"
        )

        self.gridLayout.addWidget(self.pushButton_cam, 0, 1, 1, 1)

        self.pushButton_file = QPushButton(self.groupBox_3)
        self.pushButton_file.setObjectName("pushButton_file")
        sizePolicy1.setHeightForWidth(self.pushButton_file.sizePolicy().hasHeightForWidth())
        self.pushButton_file.setSizePolicy(sizePolicy1)
        self.pushButton_file.setFont(font2)
        self.pushButton_file.setStyleSheet(
            "QPushButton{\n"
            "	image: url(:/images/icons/video.png);\n"
            "font-size: 14px;\n"
            "font-weight: bold;\n"
            "color:white;\n"
            "text-align: center center;\n"
            "padding-left: 5px;\n"
            "padding-right: 5px;\n"
            "padding-top: 4px;\n"
            "padding-bottom: 4px;\n"
            "border-style: solid;\n"
            "border-width: 0px;\n"
            "border-color: rgba(255, 255, 255, 255);\n"
            "border-radius: 3px;\n"
            "background-color: rgba(200, 200, 200,0);}\n"
            "\n"
            "QPushButton:focus{outline: none;}\n"
            "\n"
            "QPushButton::pressed{\n"
            "                     font-size: 14px;\n"
            "                     font-weight: bold;\n"
            "                     color:rgb(200,200,200);\n"
            "                     text-align: center center;\n"
            "                     padding-left: 5px;\n"
            "                     padding-right: 5px;\n"
            "                     padding-top: 4px;\n"
            "                     padding-bottom: 4px;\n"
            "                     border-style: solid;\n"
            "                     border-width: 0px;\n"
            "                     border-color: rgba(255, 255, 255, 255);\n"
            "                     bo"
            "rder-radius: 3px;\n"
            "                     background-color:  #bf513b;}\n"
            "\n"
            "QPushButton::disabled{\n"
            "                     image: url(:/images/icons/video_off.png);\n"
            "                     font-size: 14px;\n"
            "                     font-weight: bold;\n"
            "                     color:rgb(200,200,200);\n"
            "                     text-align: center center;\n"
            "                     padding-left: 5px;\n"
            "                     padding-right: 5px;\n"
            "                     padding-top: 4px;\n"
            "                     padding-bottom: 4px;\n"
            "                     border-style: solid;\n"
            "                     border-width: 0px;\n"
            "                     border-color: rgba(255, 255, 255, 255);\n"
            "                     border-radius: 3px;}\n"
            "QPushButton::hover {\n"
            "border-style: solid;\n"
            "border-width: 0px;\n"
            "border-radius: 0px;\n"
            "background-color: rgba(48,148,243,80);}"
        )

        self.gridLayout.addWidget(self.pushButton_file, 0, 0, 1, 1)

        self.verticalLayout_2.addWidget(self.groupBox_3)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.groupBox_2.setFont(font1)
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.comboBox_model = QComboBox(self.groupBox_2)
        self.comboBox_model.addItem("")
        self.comboBox_model.addItem("")
        self.comboBox_model.addItem("")
        self.comboBox_model.addItem("")
        self.comboBox_model.addItem("")
        self.comboBox_model.setObjectName("comboBox_model")
        self.comboBox_model.setFont(font)
        self.comboBox_model.setAutoFillBackground(False)
        self.comboBox_model.setStyleSheet(
            "QComboBox QAbstractItemView {\n"
            "font-size: 16px;\n"
            "outline:none;\n"
            "border:none;}\n"
            "\n"
            "QComboBox{\n"
            "font-size: 16px;\n"
            "\n"
            "color: rgb(218, 218, 218);\n"
            "border-width:0px;\n"
            "border-color:white;\n"
            "border-style:solid;\n"
            "background-color: rgba(200, 200, 200,50);}\n"
            "\n"
            "QComboBox::drop-down {\n"
            "margin-top:1;\n"
            "height:20;\n"
            "color: rgb(218, 218, 218);\n"
            "background-color: rgba(200, 200, 200,50);\n"
            "border-image: url(:/images/icons/roll_down.png);\n"
            "}\n"
            "\n"
            "QComboBox::disabled{\n"
            "color: rgb(0, 0, 0);\n"
            "}\n"
            ""
        )
        self.comboBox_model.setCurrentText("YOLOv8n")

        self.horizontalLayout_2.addWidget(self.comboBox_model)

        self.verticalLayout_2.addWidget(self.groupBox_2)

        self.groupBox_4 = QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName("groupBox_4")
        self.groupBox_4.setFont(font1)
        self.horizontalLayout_5 = QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.doubleSpinBox_conf = QDoubleSpinBox(self.groupBox_4)
        self.doubleSpinBox_conf.setObjectName("doubleSpinBox_conf")
        self.doubleSpinBox_conf.setFont(font)
        self.doubleSpinBox_conf.setStyleSheet(
            "QDoubleSpinBox{\n"
            "background:rgba(200, 200, 200,50);\n"
            "color:white;\n"
            "font-size: 14px;\n"
            "border-style: solid;\n"
            "border-width: 1px;\n"
            "border-color: rgba(200, 200, 200,100);\n"
            "border-radius: 3px;}\n"
            "\n"
            "QDoubleSpinBox::down-button{\n"
            "background:rgba(200, 200, 200,0);\n"
            "border-image: url(:/images/icons/botton_down.png);}\n"
            "QDoubleSpinBox::down-button::hover{\n"
            "background:rgba(200, 200, 200,100);\n"
            "border-image: url(:/images/icons/botton_down.png);}\n"
            "\n"
            "QDoubleSpinBox::up-button{\n"
            "background:rgba(200, 200, 200,0);\n"
            "border-image: url(:/images/icons/botton_up.png);}\n"
            "QDoubleSpinBox::up-button::hover{\n"
            "background:rgba(200, 200, 200,100);\n"
            "border-image: url(:/images/icons/botton_up.png);}"
        )
        self.doubleSpinBox_conf.setMaximum(1.000000000000000)
        self.doubleSpinBox_conf.setSingleStep(0.010000000000000)
        self.doubleSpinBox_conf.setStepType(QAbstractSpinBox.StepType.AdaptiveDecimalStepType)
        self.doubleSpinBox_conf.setValue(0.300000000000000)

        self.horizontalLayout_5.addWidget(self.doubleSpinBox_conf)

        self.horizontalSlider_conf = QSlider(self.groupBox_4)
        self.horizontalSlider_conf.setObjectName("horizontalSlider_conf")
        self.horizontalSlider_conf.setFont(font)
        self.horizontalSlider_conf.setStyleSheet(
            "QSlider{\n"
            "border-color: #bcbcbc;\n"
            "color:#d9d9d9;\n"
            "}\n"
            "QSlider::groove:horizontal {                                \n"
            "     border: 1px solid #999999;                             \n"
            "     height: 3px;                                           \n"
            "    margin: 0px 0;                                         \n"
            "     left: 5px; right: 5px; \n"
            " }\n"
            "QSlider::handle:horizontal {                               \n"
            "     border: 0px ; \n"
            "     border-image: url(:/images/icons/point.png);\n"
            "	 width:15px;\n"
            "     margin: -7px -7px -7px -7px;                  \n"
            "} \n"
            "QSlider::add-page:horizontal{\n"
            "background: #d9d9d9; \n"
            "\n"
            "}\n"
            "QSlider::sub-page:horizontal{                               \n"
            " background: #373737;                     \n"
            "}"
        )
        self.horizontalSlider_conf.setMaximum(99)
        self.horizontalSlider_conf.setSingleStep(1)
        self.horizontalSlider_conf.setPageStep(99)
        self.horizontalSlider_conf.setValue(30)
        self.horizontalSlider_conf.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_5.addWidget(self.horizontalSlider_conf)

        self.verticalLayout_2.addWidget(self.groupBox_4)

        self.groupBox_5 = QGroupBox(self.centralwidget)
        self.groupBox_5.setObjectName("groupBox_5")
        self.groupBox_5.setFont(font1)
        self.horizontalLayout_6 = QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.doubleSpinBox_iou = QDoubleSpinBox(self.groupBox_5)
        self.doubleSpinBox_iou.setObjectName("doubleSpinBox_iou")
        self.doubleSpinBox_iou.setFont(font)
        self.doubleSpinBox_iou.setStyleSheet(
            "QDoubleSpinBox{\n"
            "background:rgba(200, 200, 200,50);\n"
            "color:white;\n"
            "font-size: 14px;\n"
            "border-style: solid;\n"
            "border-width: 1px;\n"
            "border-color: rgba(200, 200, 200,100);\n"
            "border-radius: 3px;}\n"
            "\n"
            "QDoubleSpinBox::down-button{\n"
            "background:rgba(200, 200, 200,0);\n"
            "border-image: url(:/images/icons/botton_down.png);}\n"
            "QDoubleSpinBox::down-button::hover{\n"
            "background:rgba(200, 200, 200,100);\n"
            "border-image: url(:/images/icons/botton_down.png);}\n"
            "\n"
            "QDoubleSpinBox::up-button{\n"
            "background:rgba(200, 200, 200,0);\n"
            "border-image: url(:/images/icons/botton_up.png);}\n"
            "QDoubleSpinBox::up-button::hover{\n"
            "background:rgba(200, 200, 200,100);\n"
            "border-image: url(:/images/icons/botton_up.png);}"
        )
        self.doubleSpinBox_iou.setMaximum(1.000000000000000)
        self.doubleSpinBox_iou.setSingleStep(0.010000000000000)
        self.doubleSpinBox_iou.setStepType(QAbstractSpinBox.StepType.AdaptiveDecimalStepType)
        self.doubleSpinBox_iou.setValue(0.450000000000000)

        self.horizontalLayout_6.addWidget(self.doubleSpinBox_iou)

        self.horizontalSlider_iou = QSlider(self.groupBox_5)
        self.horizontalSlider_iou.setObjectName("horizontalSlider_iou")
        self.horizontalSlider_iou.setFont(font)
        self.horizontalSlider_iou.setStyleSheet(
            "QSlider{\n"
            "border-color: #bcbcbc;\n"
            "color:#d9d9d9;\n"
            "}\n"
            "QSlider::groove:horizontal {                                \n"
            "     border: 1px solid #999999;                             \n"
            "     height: 3px;                                           \n"
            "    margin: 0px 0;                                         \n"
            "     left: 5px; right: 5px; \n"
            " }\n"
            "QSlider::handle:horizontal {                               \n"
            "     border: 0px ; \n"
            "     border-image: url(:/images/icons/point.png);\n"
            "	 width:15px;\n"
            "     margin: -7px -7px -7px -7px;                  \n"
            "} \n"
            "QSlider::add-page:horizontal{\n"
            "background: #d9d9d9; \n"
            "\n"
            "}\n"
            "QSlider::sub-page:horizontal{                               \n"
            " background: #373737;                     \n"
            "}"
        )
        self.horizontalSlider_iou.setValue(45)
        self.horizontalSlider_iou.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_6.addWidget(self.horizontalSlider_iou)

        self.verticalLayout_2.addWidget(self.groupBox_5)

        self.groupBox_6 = QGroupBox(self.centralwidget)
        self.groupBox_6.setObjectName("groupBox_6")
        self.groupBox_6.setFont(font1)
        self.horizontalLayout_7 = QHBoxLayout(self.groupBox_6)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.doubleSpinBox_interval = QDoubleSpinBox(self.groupBox_6)
        self.doubleSpinBox_interval.setObjectName("doubleSpinBox_interval")
        self.doubleSpinBox_interval.setFont(font)
        self.doubleSpinBox_interval.setStyleSheet(
            "QDoubleSpinBox{\n"
            "background:rgba(200, 200, 200,50);\n"
            "color:white;\n"
            "font-size: 14px;\n"
            "border-style: solid;\n"
            "border-width: 1px;\n"
            "border-color: rgba(200, 200, 200,100);\n"
            "border-radius: 3px;}\n"
            "\n"
            "QDoubleSpinBox::down-button{\n"
            "background:rgba(200, 200, 200,0);\n"
            "border-image: url(:/images/icons/botton_down.png);}\n"
            "QDoubleSpinBox::down-button::hover{\n"
            "background:rgba(200, 200, 200,100);\n"
            "border-image: url(:/images/icons/botton_down.png);}\n"
            "\n"
            "QDoubleSpinBox::up-button{\n"
            "background:rgba(200, 200, 200,0);\n"
            "border-image: url(:/images/icons/botton_up.png);}\n"
            "QDoubleSpinBox::up-button::hover{\n"
            "background:rgba(200, 200, 200,100);\n"
            "border-image: url(:/images/icons/botton_up.png);}"
        )
        self.doubleSpinBox_interval.setDecimals(0)
        self.doubleSpinBox_interval.setMaximum(10.000000000000000)

        self.horizontalLayout_7.addWidget(self.doubleSpinBox_interval)

        self.horizontalSlider_interval = QSlider(self.groupBox_6)
        self.horizontalSlider_interval.setObjectName("horizontalSlider_interval")
        self.horizontalSlider_interval.setFont(font)
        self.horizontalSlider_interval.setStyleSheet(
            "QSlider{\n"
            "border-color: #bcbcbc;\n"
            "color:#d9d9d9;\n"
            "}\n"
            "QSlider::groove:horizontal {                                \n"
            "     border: 1px solid #999999;                             \n"
            "     height: 3px;                                           \n"
            "    margin: 0px 0;                                         \n"
            "     left: 5px; right: 5px; \n"
            " }\n"
            "QSlider::handle:horizontal {                               \n"
            "     border: 0px ; \n"
            "     border-image: url(:/images/icons/point.png);\n"
            "	 width:15px;\n"
            "     margin: -7px -7px -7px -7px;                  \n"
            "} \n"
            "QSlider::add-page:horizontal{\n"
            "background: #d9d9d9; \n"
            "\n"
            "}\n"
            "QSlider::sub-page:horizontal{                               \n"
            " background: #373737;                     \n"
            "}"
        )
        self.horizontalSlider_interval.setMaximum(10)
        self.horizontalSlider_interval.setPageStep(1)
        self.horizontalSlider_interval.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_7.addWidget(self.horizontalSlider_interval)

        self.verticalLayout_2.addWidget(self.groupBox_6)

        self.groupBox_9 = QGroupBox(self.centralwidget)
        self.groupBox_9.setObjectName("groupBox_9")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_9)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.pushButton_box_area = QPushButton(self.groupBox_9)
        self.pushButton_box_area.setObjectName("pushButton_box_area")
        self.pushButton_box_area.setStyleSheet(
            "QPushButton {\n"
            "    font-size: 14px;\n"
            "    font-weight: bold;\n"
            "    color: white;\n"
            "    text-align: center center;\n"
            "    padding: 4px 5px;\n"
            "    border-style: solid;\n"
            "    border-width: 2px;\n"
            "    border-color: white;\n"
            "    border-radius: 3px;\n"
            "    background-color: gray;\n"
            "}\n"
            "\n"
            "QPushButton:focus {\n"
            "    outline: none;\n"
            "}\n"
            "\n"
            "QPushButton::pressed {\n"
            "    font-size: 14px;\n"
            "    font-weight: bold;\n"
            "    color: rgb(200, 200, 200);\n"
            "    text-align: center center;\n"
            "    padding: 4px 5px;\n"
            "    border-style: solid;\n"
            "    border-width: 2px;\n"
            "    border-color: white;\n"
            "    border-radius: 3px;\n"
            "    background-color: #bf513b;\n"
            "}\n"
            "\n"
            "QPushButton::disabled {\n"
            "    font-size: 14px;\n"
            "    font-weight: bold;\n"
            "    color: black;\n"
            "    text-align: center center;\n"
            "    padding: 4px 5px;\n"
            "    border-style: solid;\n"
            "    border-width: 2px;\n"
            "    border-color: white;\n"
            "    border-radius: 3px;\n"
            "    background-color: gray;\n"
            "}\n"
            "\n"
            "QPush"
            "Button::hover {\n"
            "    border-style: solid;\n"
            "    border-width: 2px;\n"
            "    border-radius: 3px;\n"
            "    background-color: rgba(48, 148, 243, 80);\n"
            "}\n"
            ""
        )

        self.verticalLayout_5.addWidget(self.pushButton_box_area)

        self.radioButton_in = QRadioButton(self.groupBox_9)
        self.radioButton_in.setObjectName("radioButton_in")
        self.radioButton_in.setChecked(True)
        self.radioButton_in.setStyleSheet(
            "QRadioButton\n"
            "{font-size: 16px;\n"
            "	font-weight: bold;\n"
            " 		border-radius:9px;\n"
            "		background:rgba(66, 195, 255, 0);\n"
            "color: rgb(218, 218, 218);;}\n"
            "QRadioButton::indicator {\n"
            "	width: 20px;\n"
            "	height: 20px;\n"
            "}\n"
            "\n"
            "QRadioButton::indicator:unchecked {\n"
            "    image: url(:/images/icons/button-off.png);\n"
            "}\n"
            "\n"
            "QRadioButton::indicator:checked {\n"
            "    \n"
            "    image: url(:/images/icons/button-on.png);\n"
            "}\n"
            "\n"
            "QRadioButton::disabled{\n"
            "	color: rgb(0, 0, 0);\n"
            "}\n"
            ""
        )

        self.verticalLayout_5.addWidget(self.radioButton_in)

        self.radioButton_out = QRadioButton(self.groupBox_9)
        self.radioButton_out.setObjectName("radioButton_out")
        self.radioButton_out.setFont(font2)
        self.radioButton_out.setStyleSheet(
            "QRadioButton\n"
            "{font-size: 16px;\n"
            "	font-weight: bold;\n"
            " 		border-radius:9px;\n"
            "		background:rgba(66, 195, 255, 0);\n"
            "color: rgb(218, 218, 218);;}\n"
            "QRadioButton::indicator {\n"
            "	width: 20px;\n"
            "	height: 20px;\n"
            "}\n"
            "\n"
            "QRadioButton::indicator:unchecked {\n"
            "    image: url(:/images/icons/button-off.png);\n"
            "}\n"
            "\n"
            "QRadioButton::indicator:checked {\n"
            "    \n"
            "    image: url(:/images/icons/button-on.png);\n"
            "}\n"
            "\n"
            "QRadioButton::disabled{\n"
            "	color: rgb(0, 0, 0);\n"
            "}\n"
            ""
        )

        self.verticalLayout_5.addWidget(self.radioButton_out)

        self.pushButton_ok_area = QPushButton(self.groupBox_9)
        self.pushButton_ok_area.setObjectName("pushButton_ok_area")
        self.pushButton_ok_area.setStyleSheet(
            "QPushButton {\n"
            "    font-size: 14px;\n"
            "    font-weight: bold;\n"
            "    color: white;\n"
            "    text-align: center center;\n"
            "    padding: 4px 5px;\n"
            "    border-style: solid;\n"
            "    border-width: 2px;\n"
            "    border-color: white;\n"
            "    border-radius: 3px;\n"
            "    background-color: gray;\n"
            "}\n"
            "\n"
            "QPushButton:focus {\n"
            "    outline: none;\n"
            "}\n"
            "\n"
            "QPushButton::pressed {\n"
            "    font-size: 14px;\n"
            "    font-weight: bold;\n"
            "    color: rgb(200, 200, 200);\n"
            "    text-align: center center;\n"
            "    padding: 4px 5px;\n"
            "    border-style: solid;\n"
            "    border-width: 2px;\n"
            "    border-color: white;\n"
            "    border-radius: 3px;\n"
            "    background-color: #bf513b;\n"
            "}\n"
            "\n"
            "QPushButton::disabled {\n"
            "    font-size: 14px;\n"
            "    font-weight: bold;\n"
            "    color: black;\n"
            "    text-align: center center;\n"
            "    padding: 4px 5px;\n"
            "    border-style: solid;\n"
            "    border-width: 2px;\n"
            "    border-color: white;\n"
            "    border-radius: 3px;\n"
            "    background-color: gray;\n"
            "}\n"
            "\n"
            "QPush"
            "Button::hover {\n"
            "    border-style: solid;\n"
            "    border-width: 2px;\n"
            "    border-radius: 3px;\n"
            "    background-color: rgba(48, 148, 243, 80);\n"
            "}\n"
            ""
        )

        self.verticalLayout_5.addWidget(self.pushButton_ok_area)

        self.pushButton_cancel_area = QPushButton(self.groupBox_9)
        self.pushButton_cancel_area.setObjectName("pushButton_cancel_area")
        self.pushButton_cancel_area.setStyleSheet(
            "QPushButton {\n"
            "    font-size: 14px;\n"
            "    font-weight: bold;\n"
            "    color: white;\n"
            "    text-align: center center;\n"
            "    padding: 4px 5px;\n"
            "    border-style: solid;\n"
            "    border-width: 2px;\n"
            "    border-color: white;\n"
            "    border-radius: 3px;\n"
            "    background-color: gray;\n"
            "}\n"
            "\n"
            "QPushButton:focus {\n"
            "    outline: none;\n"
            "}\n"
            "\n"
            "QPushButton::pressed {\n"
            "    font-size: 14px;\n"
            "    font-weight: bold;\n"
            "    color: rgb(200, 200, 200);\n"
            "    text-align: center center;\n"
            "    padding: 4px 5px;\n"
            "    border-style: solid;\n"
            "    border-width: 2px;\n"
            "    border-color: white;\n"
            "    border-radius: 3px;\n"
            "    background-color: #bf513b;\n"
            "}\n"
            "\n"
            "QPushButton::disabled {\n"
            "    font-size: 14px;\n"
            "    font-weight: bold;\n"
            "    color: black;\n"
            "    text-align: center center;\n"
            "    padding: 4px 5px;\n"
            "    border-style: solid;\n"
            "    border-width: 2px;\n"
            "    border-color: white;\n"
            "    border-radius: 3px;\n"
            "    background-color: gray;\n"
            "}\n"
            "\n"
            "QPush"
            "Button::hover {\n"
            "    border-style: solid;\n"
            "    border-width: 2px;\n"
            "    border-radius: 3px;\n"
            "    background-color: rgba(48, 148, 243, 80);\n"
            "}\n"
            ""
        )

        self.verticalLayout_5.addWidget(self.pushButton_cancel_area)

        self.verticalLayout_2.addWidget(self.groupBox_9)

        self.groupBox_apply = QGroupBox(self.centralwidget)
        self.groupBox_apply.setObjectName("groupBox_apply")
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox_apply)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_apply = QPushButton(self.groupBox_apply)
        self.pushButton_apply.setObjectName("pushButton_apply")
        self.pushButton_apply.setStyleSheet(
            "QPushButton {\n"
            "    font-size: 14px;\n"
            "    font-weight: bold;\n"
            "    color: white;\n"
            "    text-align: center center;\n"
            "    padding: 4px 5px;\n"
            "    border-style: solid;\n"
            "    border-width: 2px;\n"
            "    border-color: white;\n"
            "    border-radius: 3px;\n"
            "    background-color: gray;\n"
            "}\n"
            "\n"
            "QPushButton:focus {\n"
            "    outline: none;\n"
            "}\n"
            "\n"
            "QPushButton::pressed {\n"
            "    font-size: 14px;\n"
            "    font-weight: bold;\n"
            "    color: rgb(200, 200, 200);\n"
            "    text-align: center center;\n"
            "    padding: 4px 5px;\n"
            "    border-style: solid;\n"
            "    border-width: 2px;\n"
            "    border-color: white;\n"
            "    border-radius: 3px;\n"
            "    background-color: #bf513b;\n"
            "}\n"
            "\n"
            "QPushButton::disabled {\n"
            "    font-size: 14px;\n"
            "    font-weight: bold;\n"
            "    color: black;\n"
            "    text-align: center center;\n"
            "    padding: 4px 5px;\n"
            "    border-style: solid;\n"
            "    border-width: 2px;\n"
            "    border-color: white;\n"
            "    border-radius: 3px;\n"
            "    background-color: gray;\n"
            "}\n"
            "\n"
            "QPush"
            "Button::hover {\n"
            "    border-style: solid;\n"
            "    border-width: 2px;\n"
            "    border-radius: 3px;\n"
            "    background-color: rgba(48, 148, 243, 80);\n"
            "}\n"
            ""
        )

        self.horizontalLayout_3.addWidget(self.pushButton_apply)

        self.verticalLayout_2.addWidget(self.groupBox_apply)

        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        # self.label_display = QLabel(self.centralwidget)
        self.label_display = BoxArea(self.centralwidget)
        self.label_display.setObjectName("label_display")
        self.label_display.setFont(font)
        self.label_display.setStyleSheet("background-color: rgb(0, 0, 0);")

        self.verticalLayout_3.addWidget(self.label_display)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.pushButton_play = QPushButton(self.centralwidget)
        self.pushButton_play.setObjectName("pushButton_play")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pushButton_play.sizePolicy().hasHeightForWidth())
        self.pushButton_play.setSizePolicy(sizePolicy2)
        self.pushButton_play.setMinimumSize(QSize(40, 40))
        self.pushButton_play.setFont(font)
        self.pushButton_play.setStyleSheet(
            "QPushButton {\n"
            "border-style: solid;\n"
            "border-width: 0px;\n"
            "border-radius: 0px;\n"
            "background-color: rgba(223, 223, 223, 0);\n"
            "}\n"
            "QPushButton::focus{outline: none;}\n"
            "QPushButton::hover {\n"
            "border-style: solid;\n"
            "border-width: 0px;\n"
            "border-radius: 0px;\n"
            "background-color: rgba(223, 223, 223, 150);\n"
            "}"
        )
        icon1 = QIcon()
        icon1.addFile(":/images/icons/pause.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon1.addFile(":/images/icons/run.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        icon1.addFile(":/images/icons/pause.png", QSize(), QIcon.Mode.Disabled, QIcon.State.Off)
        icon1.addFile(":/images/icons/run.png", QSize(), QIcon.Mode.Disabled, QIcon.State.On)
        icon1.addFile(":/images/icons/pause.png", QSize(), QIcon.Mode.Active, QIcon.State.Off)
        icon1.addFile(":/images/icons/run.png", QSize(), QIcon.Mode.Active, QIcon.State.On)
        icon1.addFile(":/images/icons/pause.png", QSize(), QIcon.Mode.Selected, QIcon.State.Off)
        icon1.addFile(":/images/icons/run.png", QSize(), QIcon.Mode.Selected, QIcon.State.On)
        self.pushButton_play.setIcon(icon1)
        self.pushButton_play.setIconSize(QSize(30, 30))
        self.pushButton_play.setCheckable(True)

        self.horizontalLayout_8.addWidget(self.pushButton_play)

        self.progressBar_play = QProgressBar(self.centralwidget)
        self.progressBar_play.setObjectName("progressBar_play")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.progressBar_play.sizePolicy().hasHeightForWidth())
        self.progressBar_play.setSizePolicy(sizePolicy3)
        self.progressBar_play.setMinimumSize(QSize(0, 0))
        font3 = QFont()
        font3.setFamilies(["Arial"])
        font3.setPointSize(12)
        font3.setBold(False)
        font3.setItalic(False)
        self.progressBar_play.setFont(font3)
        self.progressBar_play.setStyleSheet(
            "QProgressBar{ \n"
            "color: rgb(255, 255, 255); \n"
            "font:12pt;\n"
            " border-radius:2px; \n"
            "text-align:center; \n"
            "border:none; \n"
            "background-color: rgba(215, 215, 215,100);} \n"
            "\n"
            "QProgressBar:chunk{ \n"
            "border-radius:0px; \n"
            "background: rgba(55, 55, 55, 200);}"
        )
        self.progressBar_play.setMaximum(1000)
        self.progressBar_play.setValue(0)

        self.horizontalLayout_8.addWidget(self.progressBar_play)

        self.pushButton_stop = QPushButton(self.centralwidget)
        self.pushButton_stop.setObjectName("pushButton_stop")
        sizePolicy2.setHeightForWidth(self.pushButton_stop.sizePolicy().hasHeightForWidth())
        self.pushButton_stop.setSizePolicy(sizePolicy2)
        self.pushButton_stop.setMinimumSize(QSize(40, 40))
        self.pushButton_stop.setFont(font)
        self.pushButton_stop.setStyleSheet(
            "QPushButton {\n"
            "border-style: solid;\n"
            "border-width: 0px;\n"
            "border-radius: 0px;\n"
            "background-color: rgba(223, 223, 223, 0);\n"
            "}\n"
            "QPushButton::focus{outline: none;}\n"
            "QPushButton::hover {\n"
            "border-style: solid;\n"
            "border-width: 0px;\n"
            "border-radius: 0px;\n"
            "background-color: rgba(223, 223, 223, 150);}"
        )
        icon2 = QIcon()
        icon2.addFile(":/images/icons/stop.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_stop.setIcon(icon2)
        self.pushButton_stop.setIconSize(QSize(30, 30))

        self.horizontalLayout_8.addWidget(self.pushButton_stop)

        self.horizontalLayout_8.setStretch(0, 1)
        self.horizontalLayout_8.setStretch(1, 12)
        self.horizontalLayout_8.setStretch(2, 1)

        self.verticalLayout_3.addLayout(self.horizontalLayout_8)

        self.tableWidget_results = QTableWidget(self.centralwidget)
        if self.tableWidget_results.columnCount() < 4:
            self.tableWidget_results.setColumnCount(4)
        font4 = QFont()
        font4.setPointSize(12)
        font4.setBold(True)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setFont(font4)
        self.tableWidget_results.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setFont(font4)
        self.tableWidget_results.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setFont(font4)
        self.tableWidget_results.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setFont(font4)
        self.tableWidget_results.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.tableWidget_results.setObjectName("tableWidget_results")
        sizePolicy1.setHeightForWidth(self.tableWidget_results.sizePolicy().hasHeightForWidth())
        self.tableWidget_results.setSizePolicy(sizePolicy1)
        font5 = QFont()
        font5.setFamilies(["Arial"])
        font5.setPointSize(11)
        font5.setBold(False)
        font5.setItalic(False)
        self.tableWidget_results.setFont(font5)
        self.tableWidget_results.setAutoFillBackground(True)
        self.tableWidget_results.setStyleSheet("")
        self.tableWidget_results.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.tableWidget_results.setSizeAdjustPolicy(
            QAbstractScrollArea.SizeAdjustPolicy.AdjustToContentsOnFirstShow
        )
        self.tableWidget_results.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget_results.horizontalHeader().setProperty("showSortIndicator", False)
        self.tableWidget_results.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_3.addWidget(self.tableWidget_results)

        self.verticalLayout_3.setStretch(0, 15)
        self.verticalLayout_3.setStretch(1, 1)
        self.verticalLayout_3.setStretch(2, 4)

        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 12)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.label_status = QLabel(self.centralwidget)
        self.label_status.setObjectName("label_status")
        self.label_status.setFont(font)
        self.label_status.setStyleSheet(
            "QLabel\n"
            "{\n"
            "	font-size: 16px;\n"
            "	font-weight: light;\n"
            " 		border-radius:9px;\n"
            "		background:rgba(66, 195, 255, 0);\n"
            "color: rgb(218, 218, 218);\n"
            "}\n"
            ""
        )

        self.verticalLayout.addWidget(self.label_status)

        self.verticalLayout.setStretch(0, 9)

        self.horizontalLayout_4.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.comboBox_tabs.setCurrentIndex(-1)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "YOLOv8 GUI", None))

        self.groupBox_8.setTitle(QCoreApplication.translate("MainWindow", "Tabs", None))
        self.comboBox_tabs.setItemText(
            0, QCoreApplication.translate("MainWindow", "Camera 1", None)
        )
        self.comboBox_tabs.setItemText(
            1, QCoreApplication.translate("MainWindow", "Camera 2", None)
        )
        self.comboBox_tabs.setItemText(
            2, QCoreApplication.translate("MainWindow", "Camera 3", None)
        )
        self.comboBox_tabs.setItemText(
            3, QCoreApplication.translate("MainWindow", "Camera 4", None)
        )

        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", "Inputs", None))
        self.pushButton_cam.setText("")
        self.pushButton_file.setText("")

        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", "Models", None))
        self.comboBox_model.setItemText(
            0, QCoreApplication.translate("MainWindow", "YOLOv8n", None)
        )
        self.comboBox_model.setItemText(
            1, QCoreApplication.translate("MainWindow", "YOLOv8s", None)
        )
        self.comboBox_model.setItemText(
            2, QCoreApplication.translate("MainWindow", "YOLOv8m", None)
        )
        self.comboBox_model.setItemText(
            3, QCoreApplication.translate("MainWindow", "YOLOv8l", None)
        )
        self.comboBox_model.setItemText(
            4, QCoreApplication.translate("MainWindow", "YOLOv8x", None)
        )

        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", "Confidence", None))

        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", "IoU", None))

        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", "Frame Interval", None))

        self.groupBox_9.setTitle(QCoreApplication.translate("MainWindow", "Area", None))
        self.pushButton_box_area.setText(QCoreApplication.translate("MainWindow", "BOX", None))
        self.radioButton_in.setText(QCoreApplication.translate("MainWindow", "IN", None))
        self.radioButton_out.setText(QCoreApplication.translate("MainWindow", "OUT", None))
        self.pushButton_ok_area.setText(QCoreApplication.translate("MainWindow", "OK", None))
        self.pushButton_cancel_area.setText(
            QCoreApplication.translate("MainWindow", "Cancel", None)
        )
        self.groupBox_apply.setTitle("")
        self.pushButton_apply.setText(QCoreApplication.translate("MainWindow", "APPLY", None))
        self.label_display.setText("")
        self.pushButton_play.setText("")
        self.progressBar_play.setFormat("")
        self.pushButton_stop.setText("")
        ___qtablewidgetitem = self.tableWidget_results.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", "ID", None))
        ___qtablewidgetitem1 = self.tableWidget_results.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", "Class", None))
        ___qtablewidgetitem2 = self.tableWidget_results.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", "Confidence", None))
        ___qtablewidgetitem3 = self.tableWidget_results.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", "BBox", None))
        self.label_status.setText("")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
