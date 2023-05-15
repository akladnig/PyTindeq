from bokeh.models import Button, Div
from bokeh.layouts import Row, Column

from src.layouts.layout import Layout
from src.test import Test
from src.templates.styles import Styles


class RfdLayout(Layout):
    def __init__(self, duration, name, source_left, source_right):
        title = "Rate of Force Development Test"
        Layout.__init__(self, title, duration)

        _left_heading = Div(
            text="Left hand  ",
            styles=Styles.heading1,
        )

        self._btn_left = Button(label="Start Test", styles=Styles.button)
        self._btn_left.button_type = "danger"
        self._btn_left.disabled = True

        _heading_row_left = Row(_left_heading, self._btn_left, align="start")

        self._div_lh_peak = Div(
            text="Peak: 0 kg/s",
            styles=Styles.heading2,
            margin=Styles.rfd_div_margin,
        )

        self._div_lh_average = Div(
            text="Average: 0 kg/s",
            styles=Styles.heading2,
            margin=Styles.rfd_div_margin,
        )

        self._div_lh_time_to_peak = Div(
            text="Time to peak: 0 ms",
            styles=Styles.heading2,
            margin=Styles.rfd_div_margin,
        )
        _right_heading = Div(
            text="Right hand",
            styles=Styles.heading1,
        )

        self._btn_right = Button(label="Start Test", styles=Styles.button)
        self._btn_right.button_type = "danger"
        self._btn_right.disabled = True

        _heading_row_right = Row(_right_heading, self._btn_right, align="start")

        self._div_rh_peak = Div(
            text="Peak: 0 kg/s",
            styles=Styles.heading2,
            margin=Styles.rfd_div_margin,
        )

        self._div_rh_average = Div(
            text="Average: 0 kg/s",
            styles=Styles.heading2,
            margin=Styles.rfd_div_margin,
        )
        self._div_rh_time_to_peak = Div(
            text="Time to peak: 0 ms",
            styles=Styles.heading2,
            margin=Styles.rfd_div_margin,
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
            # _heading_row_left,
            _left_heading,
            self._btn_left,
            self._div_lh_peak,
            self._div_lh_average,
            self._div_lh_time_to_peak,
            # _heading_row_right,
            _right_heading,
            self._btn_right,
            self._div_rh_peak,
            self._div_rh_average,
            self._div_rh_time_to_peak,
            self.countdown_timer,
            width_policy="min"
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
        (peak, average, time_to_peak) = value
        self._div_lh_peak.text = "Peak: {:.0f} kg/s".format(peak)
        self._div_lh_average.text = "Average: {:.0f} kg/s".format(average)
        self._div_lh_time_to_peak.text = "Time to peak: {:d} ms".format(time_to_peak)

    @property
    def div_rh(self):
        return self._div_rh

    @div_rh.setter
    def div_rh(self, value):
        (peak, average, time_to_peak) = value
        self._div_rh_peak.text = "Peak: {:.0f} kg/s".format(peak)
        self._div_rh_average.text = "Average: {:.0f} kg/s".format(average)
        self._div_rh_time_to_peak.text = "Time to peak: {:d} ms".format(time_to_peak)

    def update_results(self, results):
        (
            fmax,
            rfd_max_x1,
            rfd_max_y1,
            rfd_max_t20,
            rfd_max_t80,
            f20,
            f80,
            rfd_average,
            tmeans,
            fmeans,
            time_to_peak_rfd,
        ) = results
        self._fig.circle(rfd_max_x1, rfd_max_y1, color="red", size=5, line_alpha=0)
        self._fig.line(
            [rfd_max_t20, rfd_max_t80], [f20, f80], line_color="red", line_width=2
        )
