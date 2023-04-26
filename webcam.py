
import customtkinter as tk
import cv2
from PIL import Image
import numpy as np
import os


class Webcam:

    def __init__(self, video_label, width, height, radius, mess_up_dict, webcam_num=0):
        self.video_label = video_label

        self.mess_up_dict = mess_up_dict

        self.webcam_num = webcam_num
        self.width, self.height =  width, height
        
        self.ap_x, self.ap_y = int(self.width/2), int(self.height/2)
        self.radius = radius

        self.live = True
    
        # set filter to clear
        self.filter = 3

        self.initWebcam()
        self.showCamera()


    def initWebcam(self):
        self.vid = cv2.VideoCapture(self.webcam_num)
        self.vid.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
        self.vid.set(cv2.CAP_PROP_EXPOSURE, -6)
        
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)


    
    def showCamera(self):
        if self.live == True:
            # Capture the video frame by frame
            _, frame = self.vid.read()
        
            # Convert image from one color space to other
            self.image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            image_ap = cv2.circle(self.image, (self.ap_x, self.ap_y), self.radius, (255, 0, 0), 3)
        
            # Capture the latest frame and transform to image
            captured_image = Image.fromarray(image_ap)
        
            # Convert captured image to photoimage
            photo_image = tk.CTkImage(captured_image, size=(self.width, self.height))
        
            # Displaying photoimage in the label
            self.video_label.photo_image = photo_image
        
            # Configure image in the label
            self.video_label.configure(image=photo_image)
        
            # Repeat the same process after every 10 ms
            self.video_label.after(10, self.showCamera)
        



    def destroyCamera(self):
        self.vid.release()


    
    def setAperturePosition(self, x, y):
        self.ap_x = int(x)
        self.ap_y = int(y)
        
        # if event is closer than a radius to an edge, then set it to 1 radius away from edge
        if self.ap_x >= (self.width - self.radius):
            self.ap_x = int(self.width - self.radius)

        elif self.ap_x <= (self.radius):
            self.ap_x = int(self.radius)


        if self.ap_y >= (self.height - self.radius):
            self.ap_y = int(self.height - self.radius)

        elif self.ap_y <= (self.radius):
            self.ap_y = int(self.radius)



    def setApertureRadius(self, value):
        self.radius = int(value)

        # ensuring that aperture isn't off screen
        self.setAperturePosition(self.ap_x, self.ap_y)


    def getIntensitySquare(self):
        pixel_array = self.image[int(self.ap_y - self.radius):int(self.ap_y + self.radius), int(self.ap_x - self.radius):int(self.ap_x + self.radius)]

        if self.filter == 3: intensity_tot = np.sum(pixel_array) / (255 * 3)
        else: intensity_tot = np.sum(pixel_array[:, :, self.filter]) / 255

        intensity = (intensity_tot / (self.radius * 2)**2) * 100

        return intensity