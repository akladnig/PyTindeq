import time

from enum import Enum

from src.templates.styles import Styles

class TimerState(Enum):
    IdleState = 1
    CountDownState = 2
    GoState = 3
    RestState = 4


class CountdownTimer:
    def __init__(self, reps, go_duration, rest_duration, layout, countdown_duration=5):
        self.state = TimerState.IdleState
        self._countdown_duration = countdown_duration
        self.go_duration = go_duration
        self.rest_duration = rest_duration
        self.idle_duration = 5

        self.layout = layout
        self._reps = reps
        self.duration = self.idle_duration
        self.time = time.time()
        self.layout.countdown_timer = (self.countdown_duration, 0, Styles.countdown_timer_idle)

    @staticmethod
    def update(parent, self, layout, test):
        if self.state == TimerState.IdleState:
            self.duration = self.idle_duration
            self.style = Styles.countdown_timer_idle
        elif self.state == TimerState.CountDownState:
            self.duration = self.countdown_duration
            self.style = Styles.countdown_timer_countdown
        elif self.state == TimerState.GoState:
            self.duration = self.go_duration
            self.style = Styles.countdown_timer_go
        elif self.state == TimerState.RestState:
            self.duration = self.rest_duration
            self.style = Styles.countdown_timer_rest

        if self.state != TimerState.IdleState:
            elapsed = time.time() - self.time
            remain = self.duration - elapsed
            ms = int(10 * (remain - int(remain))) * 10
            secs = int(remain)
        else:
            elapsed = 0
            remain = self.duration
            ms = 0
            secs = self.duration

        layout.countdown_timer = (secs, ms, self.style)

        if elapsed > self.duration:
            CountdownTimer.end(layout, self, test)

        if self.state == TimerState.CountDownState:
            if (remain <= 3.5) & (parent.st.running == False):
                parent.st.start("static/countdown.mp3", 3.5)
        elif self.state == TimerState.GoState:
            if (remain <= 1.1) & (remain > 0.5) & (parent.st.running == False):
                parent.st.start("static/end.wav", 1.1)
        elif self.state == TimerState.RestState:
            if (remain <= 3.5) & (parent.st.running == False) & (self._reps > 1):
                parent.st.start("static/countdown.mp3", 3.5)

    @staticmethod
    def end(layout, self, test):
        print(self.state, self._reps, test.complete)

        self.time = time.time()

        if self.state == TimerState.IdleState:
            self.time = time.time()
            self.state = TimerState.CountDownState

        elif self.state == TimerState.CountDownState:
            self.time = time.time()
            self.state = TimerState.GoState

        elif self.state == TimerState.GoState:
            self.time = time.time()
            if self.rest_duration == 0:
                self.state = TimerState.IdleState
            else:
                self.state = TimerState.RestState

        elif self.state == TimerState.RestState:
            if test.complete:
                self.state = TimerState.RestState
            else:
                self.time = time.time()
                self.state = TimerState.GoState
                self._reps -= 1
                if self._reps <= 0:
                    test.complete = True

    @property
    def reps(self):
        return self._reps
    
    @property
    def countdown_duration(self):
        return self._countdown_duration
    
    @countdown_duration.setter
    def countdown_duration(self, duration):
        self._countdown_duration = duration
