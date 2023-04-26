import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

import languages as lang
import mess_up_data as mess
import translate as trans

class Plot:
    def __init__(self, root, time_span, intensity_max, intensity_min, mess_up_dict, language):
        self.root = root
        
        self.current_language = language

        self.mess_up_dict = mess_up_dict
        
        self.intensity = []
        self.time = []
        
        self.plotting = False
        self.paused = False

        self.is_gap = False
        self.add_gaps = False

        self.time_span = time_span
        self.initial_time_span = 5
        self.intensity_max = intensity_max
        self.intensity_min = intensity_min

    
    def updateData(self, new_intensity, new_time):
        self.time.append(new_time)
        
        if self.is_gap:
            self.intensity.append(np.nan)
        else:
            noisy_intensity = mess.addNoise(new_intensity, self.mess_up_dict['noise']['val'])
            self.intensity.append(noisy_intensity)

        self.updatePlot()
    

    def toggleGaps(self):
        # checks if mess_up_dict value and add_gaps are the same
        if self.mess_up_dict['gap']['check'] != self.add_gaps:
            if self.mess_up_dict['gap']['check'] == 1:
                self.add_gaps = True

                self.setNextGap()

            else: 
                self.add_gaps = False
                self.is_gap = False


    def setNextGap(self):
        gap_duration, gap_time_int = mess.nextGap(self.mess_up_dict['gap']['val']['duration'], self.mess_up_dict['gap']['val']['frequency'])

        if len(self.time) > 0: self.gap_start = self.time[-1] + gap_time_int
        else: self.gap_start = gap_time_int

        self.gap_end = self.gap_start + gap_duration

        print(self.gap_start, self.gap_end)
    

    def checkGap(self):
        if len(self.time) != 0:
            if (self.time[-1] >= self.gap_start) and (self.is_gap == False):
                self.is_gap = True
            
            if (self.time[-1] >= self.gap_end) and (self.is_gap == True):
                self.is_gap = False

                self.setNextGap()


    def createPlot(self):
        self.fig = Figure(figsize = (12, 4), dpi = 100)
    
        # adding the subplot
        self.ax = self.fig.add_subplot(111)
        #plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
        self.ax.margins(0, 0)
    
        # plotting the graph
        self.intensity_plot, = self.ax.plot(self.time, self.intensity)

        # formatting the plot
        self.ax.set_xlabel(trans.trans('time', self.current_language) + ' (' + trans.trans('seconds_short', self.current_language) + ')')
        self.ax.set_ylabel(trans.trans('brightness', self.current_language) + ' (%)')
        
        self.ax.set_ylim(self.intensity_min, self.intensity_max)
        self.xAxisScrolling()
    
        # creating the Tkinter canvas
        # containing the Matplotlib figure
        self.canvas = FigureCanvasTkAgg(self.fig, master = self.root)  
        self.canvas.draw()
    
        # placing the canvas on the Tkinter window
        self.canvas.get_tk_widget().grid(row=0, column=0, padx=0, pady=0, sticky='n', columnspan=3)


    def updatePlot(self):
        if self.add_gaps: self.checkGap()

        # adding new time interval to plot
        self.intensity_plot.set_xdata(self.time)

        # adding new intensity to plot
        self.intensity_plot.set_ydata(self.intensity)
        
        # updatig the x-axis limits
        self.xAxisScrolling()

        self.ax.set_ylim(self.intensity_min, self.intensity_max)

        self.canvas.draw()


    def updateLanguage(self, new_language):
        self.current_language = new_language

        self.ax.set_xlabel(trans.trans('time', self.current_language) + ' (' + trans.trans('seconds_short', self.current_language) + ')')
        self.ax.set_ylabel(trans.trans('brightness', self.current_language) + ' (%)')

        self.canvas.draw()


    def updatePlotTest(self):
        #self.intensity_plot.set_ydata(self.intensity)
        #self.intensity_plot.set_xdata(self.time)

        self.intensity_plot.set_ydata([0,10,20,30,40,50])
        self.intensity_plot.set_xdata([0,1,2,3,4,5])

        self.ax.set_ylim(self.intensity_min, self.intensity_max)

        self.canvas.draw()
    

    def xAxisScrolling(self):
        # if total time running is greater than defined max size, then scroll with plot
        if (len(self.time) > 0):
            if max(self.time) > self.time_span:
                self.ax.set_xlim(max(self.time) - self.time_span, max(self.time))
            else:
                if self.time[-1] > self.initial_time_span:
                    self.ax.set_xlim(0, max(self.time))
                else:
                    self.ax.set_xlim(0, self.initial_time_span)
        
        else:
            self.ax.set_xlim(0, self.initial_time_span)


    def resetPlot(self):
        #print(self.time)
        print([j-i for i, j in zip(self.time[:-1], self.time[1:])])
        print(np.average([j-i for i, j in zip(self.time[:-1], self.time[1:])]))

        self.plotting = False
        self.paused = False

        self.intensity = []
        self.time = []

        if self.add_gaps: 
            self.is_gap = False
            self.setNextGap()

        self.updatePlot()

    






    




