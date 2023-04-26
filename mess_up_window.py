import customtkinter as tk

import languages as lang
import hidden_sliders as hi_sli
import translate as trans

class MessUpWindow(tk.CTkToplevel):
    def __init__(self, master, callback, language, init_params):
        super().__init__(master)

        self.protocol("WM_DELETE_WINDOW", self.quit)

        self.current_language = language
        self.languages = lang.languages

        self.init_params = init_params

        self.title(trans.trans('mess_up_data', self.current_language))
        self.geometry("300x475")

        self.createWidgets()
        
        self.save_btn = tk.CTkButton(self, text=trans.trans('save', self.current_language), command=lambda: callback(self.save_mess_up()))
        self.save_btn.pack(pady=20)
        
    
    def createWidgets(self):
        noise_init_data = [{'label': '', 'from': 0, 'to': 25, 'steps': 100, 'initial': self.init_params['noise']['val'], 'add_value': False, 'unit': ''}]
        self.noise_frame = hi_sli.SliderFrame(self, self.init_params['noise']['check'], noise_init_data, trans.trans('add_noise', self.current_language))
        self.noise_frame.frame.pack(pady=10)

        interval_init_data = [{'label': trans.trans('time_interval', self.current_language), 'from': 50, 'to': 250, 'steps': 100, 'initial': self.init_params['interval']['val']['interval'], 'add_value': True, 'unit': 'ms'},
                              {'label': trans.trans('randomise_time', self.current_language), 'from': 0, 'to': 100, 'steps': 100, 'initial': self.init_params['interval']['val']['vary'], 'add_value': False, 'unit': ''},]
        self.interval_frame = hi_sli.SliderFrame(self, self.init_params['interval']['check'], interval_init_data, trans.trans('vary_interval', self.current_language))
        self.interval_frame.frame.pack(pady=10)
        
        gap_init_data = [{'label': trans.trans('gap_duration', self.current_language), 'from': 0, 'to': 25, 'steps': 100, 'initial': self.init_params['gap']['val']['duration'], 'add_value': False, 'unit': ''}, 
                         {'label': trans.trans('gap_frequency', self.current_language), 'from': 0, 'to': 25, 'steps': 100, 'initial': self.init_params['gap']['val']['frequency'], 'add_value': False, 'unit': ''}]
        self.gap_frame = hi_sli.SliderFrame(self, self.init_params['gap']['check'], gap_init_data, trans.trans('add_gaps', self.current_language))
        self.gap_frame.frame.pack(pady=10)


    def quit(self):
        self.destroy()

    
    def save_mess_up(self):
        self.quit()

        noise_check, noise_slider = self.noise_frame.get_data()
        interval_check, interval_slider = self.interval_frame.get_data()
        gap_check, gap_sliders = self.gap_frame.get_data()

        return noise_check, noise_slider, interval_check, interval_slider, gap_check, gap_sliders




