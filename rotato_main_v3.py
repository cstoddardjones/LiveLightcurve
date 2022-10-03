import cv2
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import time
#from tkinter import filedialog
import pandas as pd


class Rotato:
    def __init__(self):
        
        # tkinter window
        self.root = tk.Toplevel()
        self.root.geometry("1000x750")
        self.root.title("Rotato")
        
        # https://www.geeksforgeeks.org/python-opencv-capture-video-from-camera/
        self.vid = cv2.VideoCapture(1)

        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

        # if no webcam is connected via usb, then use built in camera
        if (self.width == 0) or (self.height == 0):
            self.vid = cv2.VideoCapture(0)
            
            self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
            self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        
        
        # defining video size
        self.video_width = 400
        self.video_height = int((self.video_width/self.width) * self.height)
        
        self.vid.set(cv2.CAP_PROP_FPS, 1)
        
        self.vid.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)
        self.vid.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
        self.vid.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
        
        # adding video into tkinter
        self.video = tk.Label(self.root, width = self.video_width, height = self.video_height)

        self.centre_x = int(self.width/2)
        self.centre_y = int(self.height/2)
        self.ap_x = self.centre_x
        self.ap_y = self.centre_y
        
        self.white = (255, 255, 255)
        self.red   = (255,   0,   0)
        
        self.quit = False
        self.start_plotting = False
        self.paused = False
        
        self.intensity_list = []
        self.time_list = []
    
        
        '''# menu bar
        menu_bar = tk.Menu(self.root)
        
        data_menu = tk.Menu(menu_bar, tearoff = 0)
        data_menu.add_command(label = "Mess Up Data", command = self.MessUpData)
        
        menu_bar.add_cascade(label = 'Data', menu = data_menu)
        
        self.root.config(menu = menu_bar)'''
        
        self.fig = None
        
        # start/stop button
        self.start_stop_btn = tk.Button(self.root, text = 'Start Plotting', command = self.ToggleStartStop)
        
        # reset plot button
        self.reset_btn = tk.Button(self.root, text = 'Reset Plot', command = self.ResetPlot)
        
        # time span defining
        time_span_label = tk.Label(self.root, text = "Time span (s)")
        time_values = (1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120)
        self.time_span_spinbox = tk.Spinbox(self.root, from_ = 1, to = 120, values = time_values, width = 4)
        
        # setting initial value to 60s
        self.time_span_spinbox.delete(0, 'end')
        self.time_span_spinbox.insert(0, 60)
        
        # aperture radius slider
        aperture_radius_label = tk.Label(self.root, text = "Aperture Radius (pix)")
        self.aperture_radius_slider = tk.Scale(self.root, from_ = 1, to = 200, orient = 'horizontal')
        self.aperture_radius_slider.set(100)
        
        
        
        intensity_span_label = tk.Label(self.root, text = "Intensity Span (%)")
        intensity_min_label = tk.Label(self.root, text = "Min")
        intensity_max_label = tk.Label(self.root, text = "Max")
        self.intensity_min_spinbox = tk.Spinbox(self.root, from_ = 0, to = 100, increment = 5, width = 4)
        self.intensity_max_spinbox = tk.Spinbox(self.root, from_ = 0, to = 100, increment = 5, width = 4)
        
        self.intensity_max_spinbox.delete(0, 'end')
        self.intensity_max_spinbox.insert(0, 100)
        self.intensity_min_spinbox.delete(0, 'end')
        self.intensity_min_spinbox.insert(0, 0)
        
        
        
        mess_up_btn = tk.Button(self.root, text = "Mess Up Data", command = self.MessUpDataTk)
        
        # save button
        save_btn = tk.Button(self.root, text = "Save Data", command = self.SaveData)
        
        # quit button
        quit_btn = tk.Button(self.root, text = "Quit", command = self.Quit)
        
        
        # plotting lightcurve 
        self.Plot()
        
        
        
        settings_btns_col = 3
        settings_label_col = 1
        
        
        # adding widgets onto the window
        self.video.grid(row = 0, column = 0, rowspan = settings_btns_col + 1)
        
        self.video.bind('<Button 1>', self.SetApPos)
        
        self.start_stop_btn.grid(row = 7, column = 0)
        self.reset_btn.grid(row = 7, column = settings_label_col)
        save_btn.grid(row = 7, column = settings_label_col + 1)
        
        time_span_label.grid(row = 0, column = settings_label_col)
        self.time_span_spinbox.grid(row = 0, column = settings_btns_col)
        
        aperture_radius_label.grid(row = 1, column = settings_label_col)
        self.aperture_radius_slider.grid(row = 1, column = settings_btns_col - 1, columnspan = 2)
        
        intensity_span_label.grid(row = 2, column = settings_label_col, rowspan = settings_btns_col)
        intensity_min_label.grid(row = 3, column = settings_btns_col - 1)
        intensity_max_label.grid(row = 2, column = settings_btns_col - 1)
        self.intensity_min_spinbox.grid(row = 3, column = settings_btns_col)
        self.intensity_max_spinbox.grid(row = 2, column = settings_btns_col)
        #self.reset_y_btn
        
        mess_up_btn.grid(row = 4, column = settings_btns_col)
        
        
        
        quit_btn.grid(row = 8, column = 0)
        
        
        self.count = 0
        self.frame_data = 3
        
        self.rand_data_var = 0
        self.rand_gaps_var = 0
        self.add_noise_var = 0
        
        self.data_interval_period = 100
        self.data_interval_mu = 3
        self.data_interval_sigma = 0
        self.gaps_interval_mu = 0
        self.gaps_interval_sigma = 0
        self.gaps_length_mu = 0
        self.gaps_length_sigma = 0
        
        self.last_gap = 0
        self.gap_interval = 0
        self.gap_length = 0
        self.gap_bool = False
        self.gap_start = 0
        self.gap_end = 0
        
        

    def Quit(self):
        time_initial = time.time()
        self.start_plotting = False
        self.quit = True
        plt.close('all')
        self.root.quit()
        self.root.destroy()
        
        quit_time = time.time() - time_initial
        
    
    
    
    def ApertureIntensity(self, frame, x, y, radius):
        # gets intensity of a square aperture centred at x and y with total box width = radius*2
        # divided by area, divided by 255, multiplied by 100 for a max intensity = 100
        intensity = (np.sum(frame[int(y - radius):int(y + radius), int(x - radius):int(x + radius)]) / (radius * 2)**2) / 2.55
    
        return intensity
    
    
    
    def CircleApertureIntensity(self, frame, x, y, radius):
        pass
        
    
    
    def StartPlotting(self):
        self.start_plotting = True
        
        if self.paused == False:
            # defining the start time
            self.start_time = time.time()
        elif self.paused == True:
            pause_period = time.time() - self.pause_time
            self.start_time = self.start_time + pause_period
    
    
    
    def StopPlotting(self):
        self.start_plotting = False
        self.pause_time = time.time()
        
        self.paused = True
        
        
        
    def ToggleStartStop(self):
        if self.start_stop_btn['text'] == 'Start Plotting':
            self.StartPlotting()
            self.start_stop_btn.configure(text = "Stop Plotting")
        
        elif self.start_stop_btn['text'] == 'Stop Plotting':
            self.StopPlotting()
            self.start_stop_btn.configure(text = "Start Plotting")
    
    
    
    def ResetPlot(self):
        self.intensity_list = []
        self.time_list = []
        self.start_time = time.time()
        self.last_gap = 0
        
        if self.rand_gaps_var == 1:
            self.gap_interval = abs(np.random.normal(self.gaps_interval_mu, self.gaps_interval_sigma))
            self.gap_length = abs(np.random.normal(self.gaps_length_mu, self.gaps_length_sigma))
            
            self.gap_start = self.gap_interval
            self.gap_end = self.gap_start + self.gap_length
        
        self.StopPlotting()
        self.start_stop_btn.configure(text = "Start Plotting")
        self.start_plotting = False
        self.paused = False
        self.Plot()
     
    
    
    def SetApPos(self, event):
        
        video_ratio = self.video_width/self.width
        
        self.ap_x = int(event.x / video_ratio)
        self.ap_y = int(event.y / video_ratio)
        
        if self.ap_x > (self.width - self.radius):
            self.ap_x = int(self.width - self.radius)
        
        elif self.ap_x < self.radius:
            self.ap_x = self.radius
        
        else:
            pass
        
        if self.ap_y > (self.height - self.radius):
            self.ap_y = int(self.height - self.radius)
        
        elif self.ap_y < self.radius:
            self.ap_y = self.radius
        
        else:
            pass
    
    
    
    def xAxisScrolling(self):
        # if total time running is greater than defined max size, then scroll with plot
        if len(self.time_list) > 0:
            if max(self.time_list) > self.time_span:
                self.ax.set_xlim(max(self.time_list) - self.time_span, max(self.time_list))
            else:
                self.ax.set_xlim(0, max(self.time_list))
        
        else:
            self.ax.set_xlim(0, 1)
            
        

    def Plot(self):
        if self.fig == None:
            self.fig = Figure(figsize = (10, 4), dpi = 100)
            
            self.ax = self.fig.add_subplot(111)
            self.intensity_plot, = self.ax.plot(self.time_list, self.intensity_list)
            
            self.ax.set_xlabel('Time (s)')
            self.ax.set_ylabel('Light Intensity (%)')
            
            
            
            # defining max x width on plot
            self.time_span = int(self.time_span_spinbox.get())
            
            self.xAxisScrolling()

            # setting the y limit
            self.ax.set_ylim(int(self.intensity_min_spinbox.get()), int(self.intensity_max_spinbox.get()))
            
            self.canvas = FigureCanvasTkAgg(self.fig, master = self.root)
            self.canvas.get_tk_widget().grid(row = 5, column = 0, columnspan = 6)
            
        
            self.canvas.draw()
        
        else:
            self.intensity_plot.set_ydata(self.intensity_list)
            self.intensity_plot.set_xdata(self.time_list)
            
            self.ax.set_ylim(int(self.intensity_min_spinbox.get()), int(self.intensity_max_spinbox.get()))

            # defining max x width on plot
            self.time_span = int(self.time_span_spinbox.get())
            self.xAxisScrolling()
            
            self.canvas.draw()
    
    
    
    def SetWindowData(self):
        # get frame with aperture and the intensity within the aperture
        intensity = self.ApertureIntensity(self.gray_frame, self.ap_x, self.ap_y, self.radius)
        
        if self.add_noise_var == 0:
            self.intensity_list.append(intensity)
        
        else:
            intensity_noise = np.random.normal(intensity, self.add_noise_sigma)
            self.intensity_list.append(intensity_noise)
            
                    
        # getting elapsed time
        time_elapsed = time.time() - self.start_time
        self.time_list.append(time_elapsed)
        
        self.Plot()
        
        # resetting count
        self.count = 0
        
        if self.rand_data_var == 1:
            self.frame_data = int(abs(np.random.normal(self.data_interval_mu, self.data_interval_sigma)))
            
            # ensuring that 0 frames is not chosen
            if self.frame_data == 0:
                self.frame_data = 1
                

        # displaying video frame again after 100ms
        self.video.after(int(self.data_interval_period / 10), self.ShowFrames)
                
    
    
    def ShowFrames(self):
        if self.quit == False:
        
            self.radius = self.aperture_radius_slider.get()
            
            # Capture the video frame by frame
            # converting the frame to grayscale too
            self.gray_frame = cv2.cvtColor(self.vid.read()[1], cv2.COLOR_BGR2GRAY)
            
            # adding a circle to display the aperture
            gray_frame_ap = cv2.circle(self.gray_frame, (self.ap_x, self.ap_y), self.radius, self.red, 5)
            
            # resizing the video
            gray_frame_resized = cv2.resize(gray_frame_ap, (self.video_width, self.video_height))
            
            img = ImageTk.PhotoImage(image = Image.fromarray(gray_frame_resized))
            self.video.imgtk = img
            self.video.configure(image = img)
            
            self.count += 1
    
            # skip plotting for every 3 frames to try to reduce lag
            if (self.start_plotting == True) and (self.count % self.frame_data == 0):
                if len(self.time_list) != 0:
                    if (self.time_list[-1] >= self.gap_start) and (self.time_list[-1] <= self.gap_end):
                        
                        self.gap_bool = True
                        
                        # setting intensity to nan during gap
                        self.intensity_list.append(np.nan)
                        
                        # getting elapsed time
                        time_elapsed = time.time() - self.start_time
                        self.time_list.append(time_elapsed)
                        
                        self.Plot()
                        
                        # resetting count
                        self.count = 0
                        
                        if self.rand_data_var == 1:
                            self.frame_data = abs(np.random.normal(self.data_interval_mu, self.data_interval_sigma))
                            
                            # ensuring that 0 frames is not chosen
                            if self.frame_data == 0:
                                self.frame_data = 1
                    
                        # displaying video frame again after 100ms
                        self.video.after(int(self.data_interval_period / 10), self.ShowFrames)
                    
                    
                    else:
                        if self.gap_bool == True:
                            # defining the next gap
                            self.gap_interval = abs(np.random.normal(self.gaps_interval_mu, self.gaps_interval_sigma))
                            self.gap_length = abs(np.random.normal(self.gaps_length_mu, self.gaps_length_sigma))
                            
                            self.last_gap = self.gap_end
                            
                            self.gap_start = self.last_gap + self.gap_interval
                            self.gap_end = self.gap_start + self.gap_length
                            
                            print(self.gap_start, self.gap_end)
                            
                            self.gap_bool = False
                            
                        
                        self.SetWindowData()
                    
                
                elif len(self.time_list) == 0:
                    self.SetWindowData()
            
    
                
                    
            else:
                # displaying video frame again after 100ms
                self.video.after(int(self.data_interval_period / 10), self.ShowFrames)
        
        else:
            return
        


    def MessUpDataTk(self):
        # setting up a window for the messing up of data
        mess_up_win = tk.Toplevel()
        mess_up_win.geometry("300x300")
        mess_up_win.title("Mess Up Data")
        
        # defining data interval label + spinbox
        data_int_label = tk.Label(mess_up_win, text = "Data Interval Period (ms)")
        self.data_int_spin = tk.Spinbox(mess_up_win, from_ = 50, to = 1000, increment = 10, width = 4)
        data_int_label.grid(sticky = "E", row = 1, column = 0)
        self.data_int_spin.grid(sticky = "W", row = 1, column = 1)
        
    
        # setting checkbox value
        self.rand_data_btn_var = tk.IntVar(value = self.rand_data_var)
        self.rand_gaps_btn_var = tk.IntVar(value = self.rand_gaps_var)
        self.add_noise_btn_var = tk.IntVar(value = self.add_noise_var)
        
        # adding randomise data interval stuff
        rand_data_avg_label = tk.Label(mess_up_win, text = "Average Interval")
        self.rand_data_avg_spin = tk.Spinbox(mess_up_win, from_ = 0, to = 1000, increment = 10, width = 4)
        rand_data_std_label = tk.Label(mess_up_win, text = "Standard Deviation")
        self.rand_data_std_spin = tk.Spinbox(mess_up_win, from_ = 0, to = 1000, increment = 10, width = 4)
        
        # adding randomise gap length and intervals
        rand_gaps_avg_label = tk.Label(mess_up_win, text = "Average Gap Length")
        self.rand_gaps_avg_spin = tk.Spinbox(mess_up_win, from_ = 0, to = 1000, increment = 10, width = 4)
        rand_gaps_std_label = tk.Label(mess_up_win, text = "Standard Deviation")
        self.rand_gaps_std_spin = tk.Spinbox(mess_up_win, from_ = 0, to = 1000, increment = 10, width = 4)
        rand_gaps_int_label = tk.Label(mess_up_win, text = "Gap Interval")
        self.rand_gaps_int_spin = tk.Spinbox(mess_up_win, from_ = 0, to = 1000, increment = 10, width = 4)
        rand_gaps_int_std_label = tk.Label(mess_up_win, text = "Standard Deviation")
        self.rand_gaps_int_std_spin = tk.Spinbox(mess_up_win, from_ = 0, to = 1000, increment = 10, width = 4)
        
        # adding add noise standard deviation
        add_noise_std_label = tk.Label(mess_up_win, text = 'Standard Deviation')
        self.add_noise_std_spin = tk.Spinbox(mess_up_win, from_ = 0, to = 100, increment = 1, width = 4)
        
        
        # setting rows
        randomise_data_row = 3
        randomise_gaps_row = 6
        add_noise_row = 9
        
        def RandomiseDataTk():
            if (self.rand_data_btn_var.get() == 1):
                rand_data.select()
                
                rand_gaps.grid_forget()
                add_noise.grid_forget()
                save_btn.grid_forget()
                
                rand_data_avg_label.grid(sticky = "E", row = randomise_data_row + 1, column = 0)
                self.rand_data_avg_spin.grid(sticky = "W", row = randomise_data_row + 1, column = 1)
                rand_data_std_label.grid(sticky = "E", row = randomise_data_row + 2, column = 0)
                self.rand_data_std_spin.grid(sticky = "W", row = randomise_data_row + 2, column = 1)
                
                add_noise.grid(sticky = "W", row = randomise_data_row + 8, column = 0)
                rand_gaps.grid(sticky = "W", row = randomise_data_row + 3, column = 0)
                save_btn.grid(row = randomise_data_row + 10, column = 0, columnspan = 2)
                
                add_noise_row =+ 3
                randomise_gaps_row =+ 3

            
            else:                
                rand_data_avg_label.grid_forget()
                self.rand_data_avg_spin.grid_forget()
                rand_data_std_label.grid_forget()
                self.rand_data_std_spin.grid_forget()
                
                rand_gaps.grid_forget()
                add_noise.grid_forget()
                save_btn.grid_forget()

                rand_gaps.grid(sticky = "W", row = randomise_data_row + 1, column = 0)
                add_noise.grid(sticky = "W", row = randomise_data_row + 2, column = 0)
                save_btn.grid(row = randomise_data_row + 10, column = 0, columnspan = 2) 
        
                add_noise_row =- 3
                randomise_gaps_row =- 3
                
                
        def RandomiseGapsTk():
            save_btn.grid_forget()
            if self.rand_gaps_btn_var.get() == 1:
                rand_gaps.select()
                
                add_noise.grid_forget()
                
                rand_gaps_avg_label.grid(sticky = "E", row = randomise_gaps_row + 1, column = 0)
                self.rand_gaps_avg_spin.grid(sticky = "W", row = randomise_gaps_row + 1, column = 1)
                rand_gaps_std_label.grid(sticky = "E", row = randomise_gaps_row + 2, column = 0)
                self.rand_gaps_std_spin.grid(sticky = "W", row = randomise_gaps_row + 2, column = 1)
                rand_gaps_int_label.grid(sticky = "E", row = randomise_gaps_row + 3, column = 0)
                self.rand_gaps_int_spin.grid(sticky = "W", row = randomise_gaps_row + 3, column = 1)
                rand_gaps_int_std_label.grid(sticky = "E", row = randomise_gaps_row + 4, column = 0)
                self.rand_gaps_int_std_spin.grid(sticky = "W", row = randomise_gaps_row + 4, column = 1)
                
                add_noise.grid(sticky = "W", row = randomise_gaps_row + 5, column = 0)
                add_noise_row =+ 5
            
            else:
                rand_gaps_avg_label.grid_forget()
                self.rand_gaps_avg_spin.grid_forget()
                rand_gaps_std_label.grid_forget()
                self.rand_gaps_std_spin.grid_forget()
                rand_gaps_int_label.grid_forget()
                self.rand_gaps_int_spin.grid_forget()
                rand_gaps_int_std_label.grid_forget()
                self.rand_gaps_int_std_spin.grid_forget()
            
            add_noise.grid(sticky = "W", row = randomise_gaps_row + 8, column = 0)
            save_btn.grid(row = randomise_gaps_row + 10, column = 0, columnspan = 2) 
            
            add_noise_row =- 5       
                
            
        def AddNoiseTk():
            save_btn.grid_forget()
            
            if (self.add_noise_btn_var.get() == 1):
                add_noise.select()
                
                add_noise_std_label.grid(sticky = "E", row = add_noise_row + 2, column = 0)
                self.add_noise_std_spin.grid(sticky = "W", row = add_noise_row + 2, column = 1)
                
            else:                
                add_noise_std_label.grid_forget()
                self.add_noise_std_spin.grid_forget()

                
            save_btn.grid(row = add_noise_row + 10, column = 0, columnspan = 2)
                
        
        
                        
        
        
         
                
                
                
        
        def SavePreferences():
            self.data_interval_period = int(self.data_int_spin.get())
            
            self.data_interval_mu = int(self.rand_data_avg_spin.get())
            self.data_interval_sigma = float(self.rand_data_std_spin.get())
            
            self.gaps_interval_mu = float(self.rand_gaps_avg_spin.get())
            self.gaps_interval_sigma = float(self.rand_gaps_std_spin.get())
            self.gaps_length_mu = float(self.rand_gaps_int_spin.get())
            self.gaps_length_sigma = float(self.rand_gaps_int_std_spin.get())
            
            self.add_noise_sigma = float(self.add_noise_std_spin.get())
            
            self.rand_data_var = float(self.rand_data_btn_var.get())
            self.rand_gaps_var = float(self.rand_gaps_btn_var.get())
            self.add_noise_var = float(self.add_noise_btn_var.get())
            
            self.gap_interval = abs(np.random.normal(self.gaps_interval_mu, self.gaps_interval_sigma))
            self.gap_length = abs(np.random.normal(self.gaps_length_mu, self.gaps_length_sigma))
            
            self.gap_start = self.last_gap + self.gap_interval
            self.gap_end = self.gap_start + self.gap_length
            
            # close the window
            mess_up_win.destroy()
        
        
        add_noise = tk.Checkbutton(mess_up_win, text = 'Add Noise?', variable = self.add_noise_btn_var, command = AddNoiseTk)
        add_noise.grid(sticky = "W", row = randomise_data_row + 2, column = 0)

        rand_gaps = tk.Checkbutton(mess_up_win, text = "Add randomised gaps?", variable = self.rand_gaps_btn_var, command = RandomiseGapsTk)
        rand_gaps.grid(sticky = "W", row = randomise_data_row + 1, column = 0)
        
        rand_data = tk.Checkbutton(mess_up_win, text = "Randomise data obtaining interval?", variable = self.rand_data_btn_var, command = RandomiseDataTk)
        rand_data.grid(sticky = "W", row = randomise_data_row, column = 0)
        
        
        save_btn = tk.Button(mess_up_win, text = "Save", command = SavePreferences)
        save_btn.grid(row = randomise_data_row + 10, column = 0, columnspan = 2)
            
        
        # setting initial values for spinboxes
        self.data_int_spin.delete(0, 'end')
        self.rand_data_avg_spin.delete(0, 'end')
        self.rand_data_std_spin.delete(0, 'end')
        self.rand_gaps_avg_spin.delete(0, 'end')
        self.rand_gaps_std_spin.delete(0, 'end')
        self.rand_gaps_int_spin.delete(0, 'end')
        self.rand_gaps_int_std_spin.delete(0, 'end')
        
        self.data_int_spin.insert(0, self.data_interval_period)
        self.rand_data_avg_spin.insert(0, self.data_interval_mu)
        self.rand_data_std_spin.insert(0, self.data_interval_sigma)
        self.rand_gaps_avg_spin.insert(0, self.gaps_interval_mu)
        self.rand_gaps_std_spin.insert(0, self.gaps_interval_sigma)
        self.rand_gaps_int_spin.insert(0, self.gaps_length_mu)
        self.rand_gaps_int_std_spin.insert(0, self.gaps_length_sigma)
        
        
        if self.add_noise_var == 1:
            add_noise.select()
            
            rand_gaps.grid_forget()
            rand_data.grid_forget()
            save_btn.grid_forget()
                
            add_noise_std_label.grid(sticky = "E", row = add_noise_row + 1, column = 0)
            self.add_noise_std_spin.grid(sticky = "W", row = add_noise_row + 1, column = 1)
            
            #rand_data.grid(sticky = "W", row = randomise_data_row)
            #rand_gaps.grid(sticky = "W", row = randomise_gaps_row, column = 0)
            save_btn.grid(row = add_noise_row + 10, column = 0, columnspan = 2) 
        
        
        # ensuring that the variables are plotted right
        if self.rand_data_var == 1:
            rand_data.select()
            
            rand_gaps.grid_forget()
            save_btn.grid_forget()
                
            rand_data_avg_label.grid(sticky = "E", row = randomise_data_row + 1, column = 0)
            self.rand_data_avg_spin.grid(sticky = "W", row = randomise_data_row + 1, column = 1)
            rand_data_std_label.grid(sticky = "E", row = randomise_data_row + 2, column = 0)
            self.rand_data_std_spin.grid(sticky = "W", row = randomise_data_row + 2, column = 1)
            
            rand_gaps.grid(sticky = "W", row = randomise_gaps_row, column = 0)
            rand_data.grid(sticky = "W", row = randomise_data_row)
            save_btn.grid(row = add_noise_row + 10, column = 0, columnspan = 2)
            
        if self.rand_gaps_var == 1:
            rand_gaps.select()
            
            rand_gaps_avg_label.grid(sticky = "E", row = randomise_gaps_row + 1, column = 0)
            self.rand_gaps_avg_spin.grid(sticky = "W", row = randomise_gaps_row + 1, column = 1)
            rand_gaps_std_label.grid(sticky = "E", row = randomise_gaps_row + 2, column = 0)
            self.rand_gaps_std_spin.grid(sticky = "W", row = randomise_gaps_row + 2, column = 1)
            rand_gaps_int_label.grid(sticky = "E", row = randomise_gaps_row + 3, column = 0)
            self.rand_gaps_int_spin.grid(sticky = "W", row = randomise_gaps_row + 3, column = 1)
            rand_gaps_int_std_label.grid(sticky = "E", row = randomise_gaps_row + 4, column = 0)
            self.rand_gaps_int_std_spin.grid(sticky = "W", row = randomise_gaps_row + 4, column = 1)
            
            #rand_gaps.grid(sticky = "W", row = randomise_gaps_row, column = 0)
            #rand_data.grid(sticky = "W", row = randomise_data_row)
            save_btn.grid(row = add_noise_row + 10, column = 0, columnspan = 2) 
            
    
    
    def SaveData(self):
        if self.start_plotting == True:
            # stop plotting if it hasn't
            self.StopPlotting()
        
        # selecting where to save the data
        save_location = tk.filedialog.askdirectory(title = 'Save data')
        save_file = save_location + '/rotato_data.csv'
        
        # converting data into a pandas dataframe
        data = {'Time' : self.time_list, 
                'Intensity' : self.intensity_list}
        df = pd.DataFrame(data)
        
        # saving dataframe as a csv
        df.to_csv(save_file, index = False)

        
        
    def MainLoop(self):        
        # defining the start time
        self.start_time = time.time()
        
        if self.quit == False:
            # displaying the frames
            self.ShowFrames()
            
            self.root.mainloop()
        else:
            self.Quit()


Rotato().MainLoop()

