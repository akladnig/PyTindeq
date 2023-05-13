import numpy as np

from bokeh.models import Button, Div, Whisker, Band
from bokeh.layouts import Row, Column
from bokeh.plotting import ColumnDataSource

from src.layouts.layout import Layout

class CftLayout(Layout):
    def __init__(self, total_reps, title="Critical Force Test"):
        duration = total_reps*10+5
        Layout.__init__(self, title, duration)

        self._btn_start = Button(label="Waiting for Progressor...")
        self._btn_start.button_type = "danger"
        self._btn_start.disabled = True


        self._total_reps = total_reps
        self._reps = Div(
            text=f"Rep {0}/{self._total_reps}",
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
    def reps(self):
        return self._reps
    
    @reps.setter
    def reps(self, rep):
        self._reps.text = f"Rep {1 + self._total_reps - rep}/{self._total_reps}"

    @property
    def results(self):
        return self._results
    
    @results.setter
    def results(self, text):
        self._results.text = text

    def update_results(self, results):
        (
            tmeans,
            fmeans,
            e_fmeans,
            msg,
            critical_load,
            load_asymptote,
            predicted_force,
        ) = results
        self._results.text = "<p><b>Results</b></p>" + msg

        fill_src = ColumnDataSource(
            dict(
                x=tmeans,
                upper=predicted_force,
                lower=load_asymptote * np.ones_like(tmeans),
            )
        )
        self._fig.add_layout(
            Band(
                base="x",
                lower="lower",
                upper="upper",
                source=fill_src,
                fill_alpha=0.7,
            )
        )
        self._fig.circle(tmeans, fmeans, color="red", size=5, line_alpha=0)

        esource = ColumnDataSource(
            dict(x=tmeans, upper=fmeans + e_fmeans, lower=fmeans - e_fmeans)
        )
        self._fig.add_layout(
            Whisker(
                source=esource,
                base="x",
                upper="upper",
                lower="lower",
                level="overlay",
            )
        )

    