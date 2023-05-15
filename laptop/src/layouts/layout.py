from bokeh.models import Div, Range1d
from bokeh.layouts import Column, Row
from bokeh.plotting import figure

from src.templates.styles import Styles


class Layout:
    def __init__(self, title, duration):
        self.title = Div(
            text=title,
            styles=Styles.title,
        )
        self._duration = duration
        # This is a seriously dodgy workaround for the stretch_width bug
        fig_div = Div(
            text="Figure-------------------------------------------------------------------------------------------------------------------------------------------------------------------x",
            height=0,
            sizing_mode="stretch_width",
            styles=Styles.figure,
        )

        self._countdown_timer = Div(
            text=f"{10:02d}:{00:02d}",
            styles=Styles.countdown_timer_idle,
        )

        self._fig = figure(
            title="Real-time Data",
            height=500,
            sizing_mode="stretch_width",
            x_axis_label="Seconds",
            y_axis_label="kg",
        )

        """
        Draws a vertical line to force the plot to show
        """
        self._fig.line([0, 0], [0, 10], line_color="white", alpha=0)
        self._fig.x_range = Range1d(-0.5, self._duration)
        widgets = Column(
            self._countdown_timer,
        )
        self._fig_column = Column(self._fig, fig_div, sizing_mode="stretch_both", width_policy="max")
        self.row = Row(widgets, self._fig_column)
        column = Column(self.title, self.row)

    @property
    def countdown_timer(self):
        return self._countdown_timer

    @countdown_timer.setter
    def countdown_timer(self, values):
        secs, ms, style = values
        # print("countdown timer: {:02d}:{:02d}".format(secs,ms))
        self._countdown_timer.text = f"{secs:02d}:{ms:02d}"
        self._countdown_timer.styles = style

    @property
    def fig_column(self):
        return self._fig_column

    @property
    def fig(self):
        return self._fig

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, duration):
        self._duration = duration
