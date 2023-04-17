import customtkinter as tk
import cv2

import languages as lang

class WebcamSelector:
    def __init__(self, root, language):
        self.root = root
        self.current_language = language
        self.languages = lang.languages
        self.cameras = self.get_available_cameras()
        self.selected_camera = tk.StringVar(value=list(self.cameras.keys())[0] if self.cameras else "")
        self.create_widgets()


    def create_widgets(self):
        if not self.cameras:
            self.label = tk.CTkLabel(self.root, text="No cameras found")
            self.label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
            return

        self.camera_label = tk.CTkLabel(self.root, text=self.languages[self.current_language]['select_camera'])
        self.camera_label.grid(row=2, column=0, padx=10, pady=10)

        self.camera_menu = tk.CTkOptionMenu(self.root, values=list(self.cameras.keys()))
        self.camera_menu.grid(row=2, column=1, padx=10, pady=10)


    def get_available_cameras(self):
        cameras = {}
        for i in range(5):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                cameras[self.languages[self.current_language]['camera'] + ' ' + str(i) ] = i
                cap.release()
        return cameras