import customtkinter as tk
import tkinter

class SliderFrame:
    def __init__(self, master, checkbox_val, slider_data, title, add_values=False, values_units=None):
        # Store the slider data (a list of dictionaries)
        self.slider_data = slider_data

        self.master = master
        self.title = title

        self.add_values = add_values
        self.values_units = values_units
        
        # Create the frame for the check box and sliders
        self.frame = tk.CTkFrame(master)
        
        # Create a check box and add it to the frame
        self.chk_value = tkinter.IntVar()
        self.chk = tk.CTkSwitch(self.frame, text=title, variable=self.chk_value, command=self.show_hide_sliders)

        self.chk_value.set(checkbox_val)

        self.chk.pack()
        
        # Create the sliders and their corresponding labels, but don't show them yet
        self.sliders = []
        for slider in self.slider_data:
            slider_label = tk.CTkLabel(self.frame, text=slider['label'])
            
            #self.slider_var = tkinter.StringVar()
            #self.slider_var.set(str(slider['initial']))
            if slider['add_value']:
                value_template = '{} ' + str(slider['unit'])
                slider_val_widget = tk.CTkLabel(self.frame, text=value_template.format(int(slider['initial'])))
                
            
                slider_widget = tk.CTkSlider(
                                            self.frame, 
                                            from_=slider['from'], 
                                            to=slider['to'], 
                                            number_of_steps=slider['steps'],
                                            command=lambda val: slider_val_widget.configure(text=value_template.format(int(val)))
                                            )
                                            

                slider_widget.set(slider['initial'])

                self.sliders.append({'label': slider_label, 'widget': slider_widget, 'var_label': slider_val_widget})

            else:
                slider_widget = tk.CTkSlider(
                                            self.frame, 
                                            from_=slider['from'], 
                                            to=slider['to'], 
                                            number_of_steps=slider['steps'],
                                            )
            
                slider_widget.set(slider['initial'])

                self.sliders.append({'label': slider_label, 'widget': slider_widget})
        
        self.show_hide_sliders()
    

    '''def sliderCmd(self, value):
        print(value)
        self.slider_var.set(str(value))

        self.master.update()'''



    def show_hide_sliders(self):
        if self.chk_value.get() == 1:
            # Show the sliders and labels
            for i in range(len(self.sliders)):
                if self.sliders[i]['label'].cget('text') != '': self.sliders[i]['label'].pack()
                if self.slider_data[i]['add_value']: self.sliders[i]['var_label'].pack()
                self.sliders[i]['widget'].pack(pady=5)
                

        else:
            # Hide the sliders and labels
            for i in range(len(self.sliders)):
                if self.sliders[i]['label'].cget('text') != '': self.sliders[i]['label'].pack_forget()
                if self.slider_data[i]['add_value']: self.sliders[i]['var_label'].pack_forget()
                self.sliders[i]['widget'].pack_forget()
                
        
        self.master.update()
    

    def get_data(self):
        check_box = self.chk_value.get()

        sliders_val = []

        for slider in self.sliders:
            if check_box == 0: sliders_val.append(0)
            else: sliders_val.append(slider['widget'].get())

        return check_box, sliders_val