import time

class IdleState:
    bkg = "orange"

    @staticmethod
    def update(parent):
        parent.cft_countdown_timer.styles["background-color"] = parent.state.bkg
        parent.cft_countdown_timer.text = "10:00"

    @staticmethod
    def end(parent):
        print(parent.reps)
        parent.state_start = time.time()
        parent.state = CountDownState


class CountDownState:
    bkg = "orange"
    duration = 10

    @staticmethod
    def update(parent):
        # count down timer
        elapsed = time.time() - parent.state_start
        remain = CountDownState.duration - elapsed
        fs = int(10 * (remain - int(remain)))
        secs = int(remain)
        parent.cft_countdown_timer.text = f"{secs:02d}:{fs:02d}"
        parent.cft_countdown_timer.styles["background-color"] = parent.state.bkg
        if elapsed > CountDownState.duration:
            CountDownState.end(parent)
        if (remain <= 3.5) & (parent.st.running == False):
            parent.st.start("laptop/static/countdown.mp3", 3.5)

    @staticmethod
    def end(parent):
        print(parent.reps)

        parent.state_start = time.time()
        parent.state = GoState


class GoState:
    bkg = "green"
    duration = 7

    @staticmethod
    def update(parent):
        # count down timer
        elapsed = time.time() - parent.state_start
        remain = GoState.duration - elapsed
        fs = int(10 * (remain - int(remain)))
        secs = int(remain)
        parent.cft_countdown_timer.text = f"{secs:02d}:{fs:02d}"
        parent.cft_countdown_timer.styles["background-color"] = parent.state.bkg
        if elapsed > GoState.duration:
            GoState.end(parent)
        if (remain <= 1.1) & (remain > 0.5) & (parent.st.running == False):
            parent.st.start("laptop/static/end.wav", 1.1)

    @staticmethod
    def end(parent):
        print(parent.reps)

        parent.state_start = time.time()
        parent.state = RestState


class RestState:
    bkg = "red"
    duration = 3

    @staticmethod
    def update(parent):
        # count up timer
        # count down timer
        elapsed = time.time() - parent.state_start
        remain = RestState.duration - elapsed
        fs = int(10 * (remain - int(remain)))
        secs = int(remain)
        parent.cft_countdown_timer.text = f"{secs:02d}:{fs:02d}"
        parent.cft_countdown_timer.styles["background-color"] = parent.state.bkg
        if elapsed > RestState.duration:
            RestState.end(parent)
        if (remain <= 3.5) & (parent.st.running == False):
            parent.st.start("laptop/static/countdown.mp3", 3.5)

    @staticmethod
    def end(parent):
        if parent.test_done:
            parent.state = IdleState
        else:
            print(parent.reps)

            parent.state_start = time.time()
            parent.state = GoState
            parent.reps -= 1