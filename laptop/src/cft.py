from bokeh.models import Button, Slider, Div, Range1d
from bokeh.layouts import row, column
from bokeh.plotting import figure

from .cft_timers import IdleState, CountDownState, GoState, RestState
from .timers import CountdownTimer

class cft:
    def __init__(self):
        duration = 240
        title = Div(
            text="Critical Force Test",
            styles={
                "font-size": "300%",
                "font_style": "bold",
                "color": "Blue",
                "text-align": "left",
                "width": "100%",
            },
        )
        self.btn = Button(label="Waiting for Progressor...")
        self.btn.button_type = "danger"
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

        self.fig = figure(
            title="Real-time Data",
            height=400,
            sizing_mode="stretch_width",
            x_axis_label="Seconds",
            y_axis_label="kg",
        )
        self.fig.line([0, 0], [0, 10])
        self.fig.x_range = Range1d(0, duration)

        duration_slider = Slider(start=2, end=30, value=24, step=1, title="Reps")

        laps = Div(
            text=f"Rep {0}/{duration_slider.value}",
            styles={"font-size": "400%", "color": "black", "text-align": "center"},
        )

        self.countdown_timer = CountdownTimer(24, duration, None).countdown_timer

        msg = "<p><b>Results</b></p>"
        msg += "<p>peak load = {:.2f} +/- {:.2f} kg</p>".format(0, 0)
        msg += "<p>critical load = {:.2f} +/- {:.2f} kg</p>".format(0, 0)
        msg += "<p>asymptotic load = {:.2f} +/- {:.2f} kg</p>".format(0, 0)
        msg += "<p>W'' = {:.0f} J</p>".format(0)
        msg += "<p>Anaerobic function score = {:.1f}</p>".format(0)

        self.results_div = Div(
            text=msg,
            sizing_mode="stretch_width",
            styles={
                "font-size": "150%",
                "color": "black",
                "text-align": "left",
                "width": "100%",
            },
        )
        widgets = column(
            duration_slider,
            self.btn,
            laps,
            countdown_timer,
            self.results_div,
        )
        fig_column = column(self.fig, fig_div, sizing_mode="stretch_both")
        row = row(widgets, fig_column)
        self.column = column(title, row)