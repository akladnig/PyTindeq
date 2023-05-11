from bokeh.models import Button, Div, Range1d
from bokeh.layouts import Column, Row
from bokeh.plotting import figure

class Layout:

    def __init__(self, title, duration):
        self.title = Div(
            text=title,
            styles={
                "font-size": "300%",
                "font_style": "bold",
                "color": "Blue",
                "text-align": "left",
                "width": "100%",
            }
        )
        self._duration = duration
            # This is a seriously dodgy workaround for the stretch_width bug
        fig_div = Div(
            text="Figure-------------------------------------------------------------------------------------------------------------------------------------------------------------------x",
            sizing_mode="stretch_width",
            styles={
                "font-size": "150%",
                "color": "white",
                "text-align": "left",
                "width": "100%",
            },
        )

        print("Layout " + str(self._duration))
        self._countdown_timer = Div(
            text=f"{10:02d}:{00:02d}",
            styles={
                "font-size": "800%",
                "color": "white",
                "background-color": "orange",
                "text-align": "center",
            },
        )

        self._fig = figure(
            title="Real-time Data",
            height=400,
            sizing_mode="stretch_width",
            x_axis_label="Seconds",
            y_axis_label="kg",
        )
        '''
        Draws a vertical line to force the plot to show
        '''
        self._fig.line([0, 0], [0, 10])
        self._fig.x_range = Range1d(0, self._duration)
        widgets = Column(
            self._countdown_timer,
        )
        self._fig_column = Column(self._fig, fig_div, sizing_mode="stretch_both")
        self.row = Row(widgets, self._fig_column)
        column = Column(self.title, self.row)

    @property 
    def countdown_timer(self):
        return self._countdown_timer
    
    @countdown_timer.setter
    def countdown_timer(self, values):
        secs, ms, colour = values
        self._countdown_timer.text=f"{secs:02d}:{ms:02d}"
        self._countdown_timer.styles["background-color"] = colour
    
    @property 
    def fig_column(self):
        return self._fig_column
    
    @property 
    def fig(self):
        return self._fig
    
    # @fig.setter
    # def fig(self, duration):
    #     print("fig.setter")
    #     self._fig.x_range = duration
     
    @property 
    def duration(self):
        return self._duration
    
    @duration.setter 
    def duration(self, duration):
        self._duration = duration 

    