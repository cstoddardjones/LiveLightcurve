import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import languages as lang

class Plot:
    def __init__(self, root, time_span, intensity_max, intensity_min, language):
        self.root = root
        
        self.current_language = language
        
        self.intensity = []
        self.time = []
        
        self.plotting = False
        self.paused = False

        self.time_span = time_span
        self.initial_time_span = 5
        self.intensity_max = intensity_max
        self.intensity_min = intensity_min


    
    def updateData(self, new_intensity, new_time):
        self.intensity.append(new_intensity)
        self.time.append(new_time)

        self.updatePlot()

    
    def createPlot(self):
        fig = Figure(figsize = (12, 4), dpi = 100)
    
        # adding the subplot
        self.ax = fig.add_subplot(111)
        #plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
        self.ax.margins(0, 0)
    
        # plotting the graph
        self.intensity_plot, = self.ax.plot(self.time, self.intensity)

        # formatting the plot
        self.ax.set_xlabel(lang.languages[self.current_language]['time'] + ' (' + lang.languages[self.current_language]['seconds_short'] + ')')
        self.ax.set_ylabel(lang.languages[self.current_language]['brightness'] + ' (%)')
        
        self.ax.set_ylim(self.intensity_min, self.intensity_max)
        self.xAxisScrolling()
    
        # creating the Tkinter canvas
        # containing the Matplotlib figure
        self.canvas = FigureCanvasTkAgg(fig, master = self.root)  
        self.canvas.draw()
    
        # placing the canvas on the Tkinter window
        self.canvas.get_tk_widget().grid(row=0, column=0, padx=0, pady=0, sticky='n', columnspan=3)



    def updatePlot(self):
        self.ax.set_xlabel(lang.languages[self.current_language]['time'] + ' (' + lang.languages[self.current_language]['seconds_short'] + ')')
        self.ax.set_ylabel(lang.languages[self.current_language]['brightness'] + ' (%)')

        self.intensity_plot.set_ydata(self.intensity)
        self.intensity_plot.set_xdata(self.time)

        self.xAxisScrolling()

        self.ax.set_ylim(self.intensity_min, self.intensity_max)

        self.canvas.draw()



    def updateLanguage(self, new_language):
        self.current_language = new_language
        self.updatePlot()



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
        self.plotting = False
        self.paused = False

        self.intensity = []
        self.time = []

        self.updatePlot()

    






    




