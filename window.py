import customtkinter as tk
import tkinter
from tkinter import filedialog
import time

import webcam
import plot
import spinner
import settings_window
import languages as lang


class RotatoWindow(tk.CTk):
    
    def __init__(self):
        super().__init__()
        
        self.win_width, self.win_height = 1300, 750

        self.webcam_width, self.webcam_height = 320, 240
        
        self.time_span = 60
        self.min_ap_radius, self.max_ap_radius = 10, 120
        self.init_ap_radius = 50
        self.min_intensity, self.max_intensity = 0, 100

        self.current_language = 'English'
        self.languages = lang.languages

        self.createWindow()
        self.createMenu()
        self.createWebcam()
        self.createParameterEntries()
        self.createButtons()
        self.createPlot()

        self.protocol("WM_DELETE_WINDOW", self.quit)



    def createWindow(self):
        self.geometry(str(self.win_width) + 'x' + str(self.win_height))
        self.minsize(self.win_width, self.win_height)

        self.title(self.languages[self.current_language]['rotato'])
        
        tk.set_appearance_mode("dark")
        tk.set_default_color_theme("dark-blue")

        # creating the grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # main frame
        self.frame = tk.CTkFrame(self)
        self.frame.grid(row=0, column=0, padx=30, pady=20, sticky='nsew')

        # creating the grid system
        self.frame.grid_columnconfigure((0), weight=1)
        self.frame.grid_columnconfigure((1, 2), weight=8)
        
        self.frame.grid_rowconfigure(0, weight=5)
        self.frame.grid_rowconfigure(1, weight=1)


    def createMenu(self):
        # Create menu bar
        self.menu_bar = tkinter.Menu(self)
        
        # Create Rotato menu
        self.rotato_menu = tkinter.Menu(self.menu_bar, tearoff=0)
        self.language_menu = tkinter.Menu(self.rotato_menu, tearoff=0)
        self.language_var = tkinter.StringVar()
        self.language_var.set(self.current_language)
        self.language_var.trace('w', self.changeLanguage)
        self.language_menu.add_radiobutton(label='English', variable=self.language_var, value='English')
        self.language_menu.add_radiobutton(label='Cymraeg', variable=self.language_var, value='Cymraeg')
        
        self.rotato_menu.add_cascade(label=self.languages[self.current_language]['language'], menu=self.language_menu)
        self.rotato_menu.add_separator()
        self.rotato_menu.add_command(label=self.languages[self.current_language]['settings'], command=self.openSettings)
        
        # Create Help menu
        self.help_menu = tkinter.Menu(self.menu_bar, tearoff=0)
        
        # Add menu options to menu bar
        self.menu_bar.add_cascade(label=self.languages[self.current_language]['rotato'], menu=self.rotato_menu)
        self.menu_bar.add_cascade(label=self.languages[self.current_language]['help'], menu=self.help_menu)
        
        # Set menu bar
        self.config(menu=self.menu_bar)


    def createPlot(self):
        self.plot = plot.Plot(self.frame, self.time_span, self.max_intensity, self.min_intensity, self.current_language)
        self.plot.createPlot()

        # begin clock
        self.runClock()


    def createWebcam(self):
        self.webcam_label = tk.CTkLabel(self.frame, text="")
        self.webcam_label.grid(row=1, column=1, padx=20, pady=5, sticky='nsew')
        self.webcam_label.bind('<Button 1>', self.aperture_position_cmd)

        self.video = webcam.Webcam(self.webcam_label, self.webcam_width, self.webcam_height, self.init_ap_radius)


    def createParameterEntries(self):
        parameter_frame = tk.CTkFrame(self.frame)
        parameter_frame.grid(row=1, column=2, padx=20, pady=5, sticky='nsew')

        # creating the grid system
        parameter_frame.grid_rowconfigure((0, 1, 3), weight=2)
        parameter_frame.grid_rowconfigure(2, weight=1)

        parameter_frame.grid_columnconfigure(0, weight=20)
        parameter_frame.grid_columnconfigure(1, weight=1)

        # time span
        self.time_span_label = tk.CTkLabel(parameter_frame, text=self.languages[self.current_language]['time_span'])
        self.time_span_label.grid(row=0, column=0, padx=30, pady=10, sticky='n')

        self.time_span_input = spinner.IntSpinbox(parameter_frame, min_val=1, max_val=120, init_val=self.time_span, interval=5, unit='s')
        self.time_span_input.grid(row=0, column=1, padx=30, pady=10, sticky='n')

        # aperture radius
        self.aperture_radius_label = tk.CTkLabel(parameter_frame, text=self.languages[self.current_language]['ap_radius'])
        self.aperture_radius_label.grid(row=1, column=0, padx=30, pady=10, sticky='n')

        aperture_radius_slider = tk.CTkSlider(parameter_frame, from_=self.min_ap_radius, to=self.max_ap_radius, number_of_steps=self.max_ap_radius-self.min_ap_radius, command=self.video.setApertureRadius)
        aperture_radius_slider.grid(row=1, column=1, padx=30, pady=10, sticky='n')
        aperture_radius_slider.set(self.init_ap_radius)

        # intensity limit
        self.intensity_limit_label = tk.CTkLabel(parameter_frame, text=self.languages[self.current_language]['brightness_lim'])
        self.intensity_limit_label.grid(row=2, column=0, padx=30, pady=10, sticky='n', rowspan=2)

        self.max_intensity_input = spinner.IntSpinbox(parameter_frame, min_val=self.min_intensity, max_val=self.max_intensity, init_val=self.max_intensity, interval=5, unit="%")
        self.max_intensity_input.grid(row=2, column=1, padx=30, pady=5, sticky='n')

        self.min_intensity_input = spinner.IntSpinbox(parameter_frame, min_val=self.min_intensity, max_val=self.max_intensity, init_val=self.min_intensity, interval=5, unit="%")
        self.min_intensity_input.grid(row=3, column=1, padx=30, pady=5, sticky='n')

        # filter
        self.filter_label = tk.CTkLabel(parameter_frame, text=self.languages[self.current_language]['filter'])
        self.filter_label.grid(row=4, column=0, padx=30, pady=10, sticky='n')

        self.filter_btns = tk.CTkSegmentedButton(parameter_frame, values = [self.languages[self.current_language]['clear'], self.languages[self.current_language]['red_short'], self.languages[self.current_language]['green_short'], self.languages[self.current_language]['blue_short']], command=self.filter_cmd)
        self.filter_btns.grid(row=4, column=1, padx=30, pady=10, sticky='n')
        self.filter_btns.set("Clear")

        # mess up data
        #self.mess_data_btn = tk.CTkButton(parameter_frame, text=self.languages[self.current_language]['mess_up_data'], command=self.mess_data_cmd)
        #self.mess_data_btn.grid(row=5, column=0, padx=20, pady=10, sticky='n', columnspan=2)


    def createButtons(self):
        btns_frame = tk.CTkFrame(self.frame)
        btns_frame.grid(row=1, column=0, padx=20, pady=5, sticky='nsew')

        btns_frame.grid_columnconfigure((0, 1), weight=1)
        btns_frame.grid_rowconfigure((0, 1, 2), weight=1)

        # start/stop button
        self.stop_start_btn = tk.CTkButton(btns_frame, text=self.languages[self.current_language]['start'], command=self.start_stop_cmd)
        self.stop_start_btn.grid(row=0, column=0, padx=20, pady=10, sticky='nsew', columnspan=2)

        # reset button
        self.reset_btn = tk.CTkButton(btns_frame, text=self.languages[self.current_language]['reset'], command=self.reset_cmd)
        self.reset_btn.grid(row=1, column=0, padx=20, pady=10, sticky='nsew', columnspan=2)

        # save data button
        self.save_data_btn = tk.CTkButton(btns_frame, text=self.languages[self.current_language]['save_data'], command=self.save_data_cmd)
        self.save_data_btn.grid(row=2, column=0, padx=20, pady=10, sticky='nsew')

        # save plot button
        self.save_plot_btn = tk.CTkButton(btns_frame, text=self.languages[self.current_language]['save_plot'], command=self.save_plot_cmd)
        self.save_plot_btn.grid(row=2, column=1, padx=20, pady=10, sticky='nsew')


    def aperture_position_cmd(self, event):
        self.video.setAperturePosition(event.x, event.y)


    def start_stop_cmd(self):
        if self.stop_start_btn.cget('text') == self.languages[self.current_language]['start']: self.startPlotting()
        elif self.stop_start_btn.cget('text') == self.languages[self.current_language]['stop']: self.stopPlotting()
                    

    def startPlotting(self):
        self.plot.plotting = True
        self.stop_start_btn.configure(text = self.languages[self.current_language]["stop"])

        if self.plot.paused == False:
            self.start_time = time.time()
        
        elif self.plot.paused == True:
            pause_period = time.time() - self.pause_time
            self.start_time = self.start_time + pause_period


    def stopPlotting(self):
        self.plot.plotting = False
        self.plot.paused = True
        self.pause_time = time.time()
        self.stop_start_btn.configure(text = self.languages[self.current_language]["start"])


    def reset_cmd(self):
        self.plot.paused = False

        self.stopPlotting()
        self.plot.resetPlot()


    def filter_cmd(self, value):
        if value == self.languages[self.current_language]['red_short']: self.video.setFilter(0)
        elif value == self.languages[self.current_language]['green_short']: self.video.setFilter(1)
        elif value == self.languages[self.current_language]['blue_short']: self.video.setFilter(2)
        else: self.video.setFilter()


    def mess_data_cmd(self):
        print('mess data')


    def save_data_cmd(self):
        print('save data')
        self.plot.updatePlotTest()

    
    def save_plot_cmd(self):
        print('save plot')
        self.plot.updatePlotTest()

    
    def openSettings(self):
        if self.plot.plotting == True:
            self.stopPlotting()

        self.settings_window = settings_window.SettingsWindow(self, self.updateSettings, self.plot, self.video, self.current_language)
        self.settings_window.grab_set()


    def updateSettings(self, new_settings):
        webcam_number = new_settings

        self.video.release()
        self.video = webcam.Webcam(self.webcam_label, self.webcam_width, self.webcam_height, self.init_ap_radius, webcam_num=webcam_number)


    def changeLanguage(self, *args):
        self.current_language = self.language_var.get()

        self.title(self.languages[self.current_language]['rotato'])
        self.menu_bar.entryconfig(0, label = self.languages[self.current_language]['rotato'])
        self.menu_bar.entryconfig(1, label = self.languages[self.current_language]['help'])
        self.rotato_menu.entryconfig(0, label = self.languages[self.current_language]['language'])
        self.rotato_menu.entryconfig(2, label = self.languages[self.current_language]['settings'])

        self.time_span_label.configure(text=self.languages[self.current_language]['time_span'])
        self.aperture_radius_label.configure(text=self.languages[self.current_language]['ap_radius'])
        self.intensity_limit_label.configure(text=self.languages[self.current_language]['brightness_lim'])
        self.filter_label.configure(text=self.languages[self.current_language]['filter'])
        self.filter_btns.configure(values=[self.languages[self.current_language]['clear'], self.languages[self.current_language]['red_short'], self.languages[self.current_language]['green_short'], self.languages[self.current_language]['blue_short']])
        self.mess_data_btn.configure(text=self.languages[self.current_language]['mess_up_data'])

        if self.plot.plotting == True: self.stop_start_btn.configure(text=self.languages[self.current_language]['stop'])
        else: self.stop_start_btn.configure(text=self.languages[self.current_language]['start'])
        self.reset_btn.configure(text=self.languages[self.current_language]['reset'])
        self.save_data_btn.configure(text=self.languages[self.current_language]['save_data'])
        self.save_plot_btn.configure(text=self.languages[self.current_language]['save_plot'])

        self.plot.updateLanguage(self.current_language)




    def runClock(self):
        if self.plot.plotting == True:
            # setting limits
            self.plot.time_span = self.time_span_input.get()
            self.plot.intensity_max = self.max_intensity_input.get()
            self.plot.intensity_min = self.min_intensity_input.get()

            # updating intensity and time
            intensity = self.video.getIntensitySquare()
            time_val = time.time() - self.start_time
            self.plot.updateData(intensity, time_val)
        
        self.after(50, self.runClock)


    def quit(self):
        self.plot.plotting = False
        self.video.live = False
        self.video.vid.release()
        self.destroy()




#UI = RotatoWindow()
#UI.mainloop()