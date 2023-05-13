from bokeh.models import Button, Div
from bokeh.layouts import Row, Column

from src.layouts.layout import Layout
from src.test import Test


class TestLayout(Layout):
    def __init__(self, duration, name, source_left, source_right):
        self._name = name
        if name == Test.MaxLeft or name == Test.MaxRight:
            title = "Max Strength Test"
        elif name == Test.RfdLeft or name == Test.RfdRight:
            title = "Rate of Force Development Test"
        Layout.__init__(self, title, duration)

        self._btn_left = Button(label="Waiting for Progressor...")
        self._btn_left.button_type = "danger"
        self._btn_left.disabled = True
        
        self._btn_right = Button(label="Waiting for Progressor...")
        self._btn_right.button_type = "danger"
        self._btn_right.disabled = True


        if name == Test.MaxLeft or name == Test.MaxRight:
            self._div_lh = Div(
                text="Left hand:  0.00 kg",
                styles={"font-size": "200%", "color": "black", "text-align": "center"},
            )

            self._div_rh = Div(
                text="Right hand: 0.00 kg",
                styles={"font-size": "200%", "color": "black", "text-align": "center"},
            )
        elif name == Test.RfdLeft or name == Test.RfdRight:
            self._div_lh = Div(
                text="Left hand: 0.00 kg/s",
                styles={"font-size": "200%", "color": "black", "text-align": "center"},
            )

            self._div_rh = Div(
                text="Right hand: 0.00 kg/s",
                styles={"font-size": "200%", "color": "black", "text-align": "center"},
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
        self.column = Column(self.title, row)

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
        if self._name == Test.MaxLeft or self._name == Test.MaxRight:
            self._div_lh.text = "Left hand:  " + str(value) + " kg"

        elif self._name == Test.RfdLeft or self._name == Test.RfdRight:
            self._div_lh.text = "Left hand: " + str(value) + " kg/s"

    @property
    def div_rh(self):
        return self._div_rh

    @div_rh.setter
    def div_rh(self, value):
        if self._name == Test.MaxLeft or self._name == Test.MaxRight:
            self._div_rh.text = "Right hand:  " + str(value) + " kg"

        elif self._name == Test.RfdLeft or self._name == Test.RfdRight:
            self._div_rh.text = "Right hand: " + str(value) + " kg/s"
