import time

from src.layouts.layout import Layout
from src.analysis import Test, TestStatus

from enum import Enum

from bokeh.models import Div


class TimerState(Enum):
    IdleStatex = 1
    CountDownStatex = 2
    GoStatex = 3
    RestStatex = 4


class CountdownTimer:
    countdown_duration = 10
    def __init__(self, reps, duration, layout):
        self.statex = TimerState.IdleStatex
        self.go_duration = duration
        self.rest_duration = 3
        self.idle_duration = 10

        self.layout = layout
        self.reps = reps
        self.duration = 10
        self.time = time.time()
        self.layout.countdown_timer = (self.countdown_duration, 0, "orange")

        # self.countdown_timer = Div(
        #     text=f"{self.countdown_duration:02d}:{00:02d}",
        #     styles={
        #         "font-size": "800%",
        #         "color": "white",
        #         "background-color": "orange",
        #         "text-align": "center",
        #     },
        # )

    @staticmethod
    def update(parent, self, layout):
        if self.statex == TimerState.IdleStatex:
            self.duration = self.idle_duration
            self.colour = "orange"
        elif self.statex == TimerState.CountDownStatex:
            self.duration = self.countdown_duration
            self.colour = "orange"
        elif self.statex == TimerState.GoStatex:
            self.duration = self.go_duration
            self.colour = "green"
        elif self.statex == TimerState.RestStatex:
            self.duration = self.rest_duration
            self.colour = "red"

        if self.statex != TimerState.IdleStatex:
            elapsed = time.time() - self.time
            remain = self.duration - elapsed
            ms = int(10 * (remain - int(remain)))
            secs = int(remain)
        else:
            elapsed = 0
            remain = self.duration
            ms = 0
            secs = self.duration
            
        layout.countdown_timer = (secs, ms, self.colour)

        if elapsed > self.duration:
            CountdownTimer.end(self)

        if self.statex == TimerState.CountDownStatex:
            if (remain <= 3.5) & (parent.st.running == False):
                parent.st.start("laptop/static/countdown.mp3", 3.5)
        elif self.statex == TimerState.GoStatex:
            if (remain <= 1.1) & (remain > 0.5) & (parent.st.running == False):
                parent.st.start("laptop/static/end.wav", 1.1)
        elif self.statex == TimerState.RestStatex:
            if (remain <= 3.5) & (parent.st.running == False):
                parent.st.start("laptop/static/countdown.mp3", 3.5)

    @staticmethod
    def end(self):
        print(self.statex, self.reps, TestStatus.complete)
        self.time = time.time()

        if self.statex == TimerState.IdleStatex:
            self.time = time.time()
            self.statex = TimerState.CountDownStatex

        elif self.statex == TimerState.CountDownStatex:
            self.time = time.time()
            self.statex = TimerState.GoStatex

        elif self.statex == TimerState.GoStatex:
            self.time = time.time()
            self.statex = TimerState.RestStatex

        elif self.statex == TimerState.RestStatex:
            if TestStatus.complete:
                self.statex = TimerState.RestStatex
            else:
                self.time = time.time()
                self.statex = TimerState.GoStatex
                self.reps -= 1
                if self.reps <= 0:
                    TestStatus.complete = True
        else:
            pass
