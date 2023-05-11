from bokeh.models import Button, Div, Slider, Range1d
from bokeh.layouts import Row, Column

from src.layouts.layout import Layout

class CftLayout(Layout):
    def __init__(self, duration, title="Critical Force Test"):
        Layout.__init__(self, title, duration)

        self._btn_start = Button(label="Waiting for Progressor...")
        self._btn_start.button_type = "danger"

        self._reps_slider = Slider(start=2, end=30, value=24, step=1, title="Reps")

        self._reps = Div(
            text=f"Rep {0}/{self._reps_slider.value}",
            styles={"font-size": "400%", "color": "black", "text-align": "center"},
        )

        msg = "<p><b>Results</b></p>"
        msg += "<p>peak load = {:.2f} +/- {:.2f} kg</p>".format(0, 0)
        msg += "<p>critical load = {:.2f} +/- {:.2f} kg</p>".format(0, 0)
        msg += "<p>asymptotic load = {:.2f} +/- {:.2f} kg</p>".format(0, 0)
        msg += "<p>W'' = {:.0f} J</p>".format(0)
        msg += "<p>Anaerobic function score = {:.1f}</p>".format(0)

        self._results = Div(
            text=msg,
            sizing_mode="stretch_width",
            styles={
                "font-size": "150%",
                "color": "black",
                "text-align": "left",
                "width": "100%",
            },
        )

        self.widgets = Column(
            self._reps_slider,
            self._btn_start,
            self._reps,
            self.countdown_timer,
            self._results
        )
        self.row = Row(self.widgets, self._fig_column)
        self.column = Column(self.title, self.row)

    @property    
    def btn(self):
        return self._btn_start

    @property
    def reps_slider(self):
        return self._reps_slider
    
    @reps_slider.setter
    def reps_slider(self, reps):
        self._reps_slider.value = reps
    
    @property
    def reps(self):
        return self._reps
    
    @reps.setter
    def reps(self, rep):
        self._reps.text = f"Rep {1 + self._reps_slider.value - rep}/{self._reps_slider.value}"

    