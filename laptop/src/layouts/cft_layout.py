import numpy as np

from bokeh.models import Button, Div, Whisker, Band
from bokeh.layouts import Row, Column
from bokeh.plotting import ColumnDataSource

from src.layouts.layout import Layout
from src.templates.styles import Styles


class CftLayout(Layout):
    def __init__(self, total_reps, title="Critical Force Test"):
        duration = total_reps * 10
        Layout.__init__(self, title, duration)

        self._btn_start = Button(label="Waiting for Progressor...")
        self._btn_start.button_type = "danger"
        self._btn_start.disabled = True

        self._total_reps = total_reps
        self._reps = Div(
            text=f"Rep {0}/{self._total_reps}",
            styles=Styles.reps,
        )
        _results_title = Div(
            text="Results:",
            sizing_mode="stretch_width",
            styles=Styles.heading,
        )
        self.results_text = (0, [0.0], [0.0], 0, 0, 0, 0, 0, 0)

        self._results = Div(    
            text=self.results_text,
            sizing_mode="stretch_width",
            styles=Styles.normal,
        )

        self.widgets = Column(
            self._btn_start,
            self._reps,
            self.countdown_timer,
            _results_title,
            self._results,
        )
        self.row = Row(self.widgets, self._fig_column)
        self.column = Column(self.title, self.row)

    @property
    def btn(self):
        return self._btn_start

    @property
    def total_reps(self):
        return self._total_reps

    @property
    def reps(self):
        return self._reps

    @reps.setter
    def reps(self, rep):
        # print("Reps Setter: ", rep)
        self._reps.text = f"Rep {1 + self._total_reps - rep}/{self._total_reps}"

    @property
    def results_text(self):
        return self._results_text

    @results_text.setter
    def results_text(self, results):
        (
            tmeans,
            fmeans,
            std_fmeans,
            critical_load,
            std_critical_load,
            load_asymptote,
            std_load_asymptote,
            wprime_alt,
            predicted_force,
        ) = results
        if critical_load == 0:
            anaerobic_function = 0
        else:
            anaerobic_function = wprime_alt / critical_load

        if np.any(fmeans):
            _text = "<p>Peak load = {:.1f} +/- {:.1f} kg</p>".format(
                fmeans[0], std_fmeans[0]
            )
        else:
            _text = "<p>Peak load = {:.1f} +/- {:.1f} kg</p>".format(0, 0)

        _text += "<p>Critical load = {:.1f} +/- {:.1f} kg</p>".format(
            critical_load, std_critical_load
        )
        _text += "<p>Asymptotic load = {:.1f} +/- {:.1f} kg</p>".format(
            load_asymptote, std_load_asymptote
        )
        _text += "<p>W' = {:.0f} J</p>".format(wprime_alt)
        _text += "<p>Anaerobic function score = {:.1f}</p>".format(anaerobic_function)
        self._results_text = _text

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
            std_fmeans,
            critical_load,
            std_critical_load,
            load_asymptote,
            std_load_asymptote,
            wprime_alt,
            predicted_force,
        ) = results

        self.results_text = results
        self._results.text = self.results_text
        if np.any(fmeans):
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
                dict(x=tmeans, upper=fmeans + std_fmeans, lower=fmeans - std_fmeans)
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
