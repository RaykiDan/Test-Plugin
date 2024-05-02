from src.plugin_interface import PluginInterface
from src.models.model_apps import Model
from PyQt6 import QtWidgets, QtCore, QtGui
from .ui_widget import Ui_Form
import cv2


class Controller(QtWidgets.QWidget):
    def __init__(self, model):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.model = model
        self.image = None
        self.video = None
        self.set_stylesheet()
        self.connect_button()

    def set_stylesheet(self):
        self.ui.cam0.setStyleSheet(self.model.style_label_title())
        self.ui.cam1.setStyleSheet(self.model.style_label_title())
        self.ui.cam0Screen.setStyleSheet(self.model.style_label())
        self.ui.cam1Screen.setStyleSheet(self.model.style_label())
        self.ui.open.setStyleSheet(self.model.style_pushbutton())
        self.ui.param.setStyleSheet(self.model.style_pushbutton())

    def connect_button(self):
        self.ui.open.clicked.connect(self.on_click_open)
        self.ui.param.clicked.connect(self.cam_params)

    def on_click_open(self):
        source_type, cam_type, media_source, params_name = self.model.select_media_source()
        print(f'{source_type, cam_type, media_source, params_name}')
        if cam_type:
            if params_name:
                self.moildev = self.model.connect_to_moildev(parameter_name=params_name)
            self.image_original = cv2.imread(media_source)
            self.image = self.image_original.copy()
            self.videoCapture = cv2.VideoCapture(media_source)
            self.show_to_ui()

    def open_cam(self):
        source_type, cam_type, media_source, params_name = self.model.select_media_source()
        self.cam = self.model.moil_camera('opencv_usb_cam', 0)
        self.ui.cam0Screen.setCurrentIndex(1)
        self.camera_thread_original = VideoThread(self.cam)
        self.camera_thread.start()

    #def load_image(self):
    #    file = self.model.select_file()
    #    if file:
    #        if file:
    #            self.moildev = self.model.connect_to_moildev(parameter_name=file)
    #        self.image_original = cv2.imread(file)
    #        self.image = self.image_original.copy()
    #        self.show_to_ui()

    def show_to_ui(self):
        # map_x, map_y = self.moildev.maps_anypoint_mode1(0, 0, 4)
        # draw_image = self.model.draw_polygon(self.image, map_x, map_y)

        self.model.show_image_to_label(self.ui.cam0Screen, self.image, 800)
        self.model.show_image_to_label(self.ui.cam1Screen, self.image, 800)

    def cam_params(self):
        self.model.form_camera_parameter()

class Test(PluginInterface):
    def __init__(self):
        super().__init__()
        self.widget = None
        self.description = "This is a plugins application"

    def set_plugin_widget(self, model):
        self.widget = Controller(model)
        return self.widget

    def set_icon_apps(self):
        return "icon.png"

    def change_stylesheet(self):
        self.widget.set_stylesheet()
