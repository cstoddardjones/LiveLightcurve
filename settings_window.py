import customtkinter as tk

import get_cameras
import webcam
import languages as lang

class SettingsWindow(tk.CTkToplevel):
    def __init__(self, parent, callback, plot, video, language):
        super().__init__(parent)

        self.language = language
        self.languages = lang.languages

        self.plot = plot
        self.video = video

        self.title(self.languages[language]['settings'])
        self.geometry("300x200")

        self.camera_obj = get_cameras.WebcamSelector(self, language)
        self.video.initWebcam()
        
        
        self.save_btn = tk.CTkButton(self, text=self.languages[language]['save'], command=lambda: callback(self.save_settings()))
        self.save_btn.grid(row=5, column=0, padx=10, pady=10, columnspan=2)

    
    def save_settings(self):


        #self.video.webcam_num = self.camera_obj.cameras[self.camera_obj.selected_camera.get()]
        #self.video.initWebcam()
        webcam_number = self.camera_obj.cameras[self.camera_obj.selected_camera.get()]

        self.destroy()

        return webcam_number
