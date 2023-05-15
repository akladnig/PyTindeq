from bokeh.models import Button, Div
from bokeh.layouts import Row, Column

from src.layouts.layout import Layout
from src.test import Test
from src.templates.styles import Styles


class MaxLayout(Layout):
    def __init__(self, duration, name, source_left, source_right):
        self._name = name
        title = "Max Strength Test"

        Layout.__init__(self, title, duration)

        self._btn_left = Button(label="Start Test", styles=Styles.button)
        self._btn_left.button_type = "danger"
        self._btn_left.disabled = True

        self._btn_right = Button(label="Start Test", styles=Styles.button)
        self._btn_right.button_type = "danger"
        self._btn_right.disabled = True

        self._div_lh = Div(
            text="Left hand:  0.0 kg",
            styles=Styles.heading2,
            margin=Styles.div_margin,
        )

        self._div_rh = Div(
            text="Right hand: 0.0 kg",
            styles=Styles.heading2,
            margin=Styles.div_margin,
        )

        self._fig.line(
            legend_label="Left",
            x="x",
            y="y",
            source=source_left,
            line_color="blue",
        )
        self._fig.line(
            legend_label="Right",
            x="x",
            y="y",
            source=source_right,
            line_color="Green",
        )
        self._fig.legend.location = "top_left"

        widgets = Column(
            self._btn_left,
            self._div_lh,
            self._btn_right,
            self._div_rh,
            self.countdown_timer,
        )
        row = Row(widgets, self.fig_column)
        self.column = Column(
            self.title,
            row,
            margin=Styles.div_margin,
        )

    @property
    def btn_left(self):
        return self._btn_left

    @property
    def btn_right(self):
        return self._btn_right

    @property
    def div_lh(self):
        return self._div_lh

    @div_lh.setter
    def div_lh(self, value):
        self._div_lh.text = "Left hand: {:.1f}kg".format(value)

    @property
    def div_rh(self):
        return self._div_rh

    @div_rh.setter
    def div_rh(self, value):
        self._div_rh.text = "Right hand: {:.1f}kg".format(value)

    def update_results(self, results):
        (x, y) = results
        self._fig.circle(
            x,
            y,
            color="red",
            size=5,
            line_alpha=0,
        )
