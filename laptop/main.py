from src.tindeq import TindeqProgressor
from src.analysis import analyse_max, analyse_data, analyse_rfd, test_results
from src.timers import CountdownTimer, TimerState

from src.layouts.cft_layout import CftLayout
from src.layouts.max_layout import MaxLayout
from src.layouts.rfd_layout import RfdLayout
from src.layouts.user_layout import UserLayout
from src.layouts.analysis_layout import AnalysisLayout

from src.test import start_test, Test, TestResults

from src.playsounds import sound_thread

from datetime import date
import os

import numpy as np
import asyncio
import tornado

from bokeh.server.server import Server
from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler
from bokeh.plotting import ColumnDataSource
from bokeh.layouts import Column


class TindeqTests:
    def __init__(self):
        self.x = []
        self.y = []
        self.xnew = []
        self.ynew = []
        self.active = False
        # self.total_reps = 24
        self.total_reps = 24
        self.cft_go_duration = 7
        self.cft_rest_duration = 3
        self.cft_duration = 10 * self.total_reps
        self.max_go_duration = 5
        self.rfd_go_duration = 5
        self.max_rest_duration = 0
        self.rfd_rest_duration = 0
        self.state = TimerState.IdleState
        self.st = sound_thread()
        self.analysed = False
        self.tindeq = None
        io_loop = tornado.ioloop.IOLoop.current()
        io_loop.add_callback(connect, self)

    def log_force_sample(self, time, weight):
        # if Test.testing_active:
        # print("Time: {:.5f} Weight: {:.2f}".format(time, weight) )
        self.xnew.append(time)
        self.ynew.append(weight)
        self.x.append(time)
        self.y.append(weight)

    def reset(self):
        self.xnew, self.ynew = [], []

    def make_document(self, doc):
        self.cft_source = ColumnDataSource(data=dict(x=[], y=[]))
        self.max_source_l = ColumnDataSource(data=dict(x=[], y=[]))
        self.max_source_r = ColumnDataSource(data=dict(x=[], y=[]))
        self.rfd_source_l = ColumnDataSource(data=dict(x=[], y=[]))
        self.rfd_source_r = ColumnDataSource(data=dict(x=[], y=[]))

        doc.title = "Tindeq Tests"
        """
        User Details Layout
        """
        self._user_layout = UserLayout()
        user_column = self._user_layout.column

        TestResults.body_weight = self._user_layout.weight
        'Make the base path to store the data'
        _cwd = os.getcwd()
        self._path= os.path.join(_cwd, "data")

        """
        Critical Force Testing Layout
        """
        self.cft_layout = CftLayout(self.total_reps)

        "Sets the go period to 7 secs and rest period to 3 secs"
        self.timer_cft = CountdownTimer(
            self.total_reps,
            self.cft_go_duration,
            self.cft_rest_duration,
            self.cft_layout,
        )

        self.cft_fig = self.cft_layout.fig
        self.cft_fig.line(x="x", y="y", source=self.cft_source)

        def cft_onclick():
            Test.TestingStarted = True

            io_loop = tornado.ioloop.IOLoop.current()
            io_loop.add_callback(
                start_test, self, self.cft_layout, self.timer_cft, Test.Cft
            )

        self.cft_btn = self.cft_layout.btn
        self.cft_btn.on_click(cft_onclick)

        cft_column = self.cft_layout.column

        """
        Rate of Force Development Testing
        """
        self.rfd_layout = RfdLayout(
            self.rfd_go_duration, Test.RfdLeft, self.rfd_source_l, self.rfd_source_r
        )
        self.timer_rfd = CountdownTimer(
            1, self.rfd_go_duration, self.rfd_rest_duration, self.rfd_layout
        )

        self.rfd_fig = self.rfd_layout.fig

        def rfd_onclick_left():
            Test.TestingStarted = True
            Test.RfdLeft.complete = False

            self.rfd_source_l.data = dict(x=[], y=[])

            io_loop = tornado.ioloop.IOLoop.current()
            io_loop.add_callback(
                start_test, self, self.rfd_layout, self.timer_rfd, Test.RfdLeft
            )

        def rfd_onclick_right():
            Test.TestingStarted = True
            Test.RfdRight.complete = False

            self.rfd_source_r.data = dict(x=[], y=[])

            io_loop = tornado.ioloop.IOLoop.current()
            io_loop.add_callback(
                start_test, self, self.rfd_layout, self.timer_rfd, Test.RfdRight
            )

        self.rfd_btn_left = self.rfd_layout.btn_left
        self.rfd_btn_left.on_click(rfd_onclick_left)
        self.rfd_btn_right = self.rfd_layout.btn_right
        self.rfd_btn_right.on_click(rfd_onclick_right)

        rfd_column = self.rfd_layout.column

        """
        Max Strength Testing
        """
        self.max_layout = MaxLayout(
            self.max_go_duration, Test.MaxLeft, self.max_source_l, self.max_source_r
        )
        self.timer_max = CountdownTimer(
            1, self.max_go_duration, self.max_rest_duration, self.max_layout
        )

        self.max_fig = self.max_layout.fig

        def max_onclick_left():
            Test.TestingStarted = True

            self.max_source_l.data = dict(x=[], y=[])

            io_loop = tornado.ioloop.IOLoop.current()
            io_loop.add_callback(
                start_test, self, self.max_layout, self.timer_max, Test.MaxLeft
            )

        def max_onclick_right():
            Test.TestingStarted = True

            self.max_source_r.data = dict(x=[], y=[])

            io_loop = tornado.ioloop.IOLoop.current()
            io_loop.add_callback(
                start_test, self, self.max_layout, self.timer_max, Test.MaxRight
            )

        self.max_btn_left = self.max_layout.btn_left
        self.max_btn_left.on_click(max_onclick_left)
        self.max_btn_right = self.max_layout.btn_right
        self.max_btn_right.on_click(max_onclick_right)

        max_column = self.max_layout.column
        """
        Analysis Layout
        """
        self.analysis_layout = AnalysisLayout()
        analysis_column = self.analysis_layout.column

        doc.add_root(
            Column(user_column, max_column, rfd_column, cft_column, analysis_column)
        )
        doc.add_periodic_callback(self.update, 20)

    def update(self):
        """
        There are four testing states:
        - No testing started:               TestingStarted = false
        - Testing started and not active:   testing_complete = false and testing_active = false
        - Testing started and active:       testing_complete = false and testing_active = true
        - Testing complete:                 testing_complete = true  and testing_active = false
        """
        if not Test.TestingStarted:
            if self.tindeq is not None:
                self.cft_btn.label = "Start Test"
                self.cft_btn.button_type = "success"
                self.cft_btn.disabled = False

                self.max_btn_left.label = "Start Test"
                self.max_btn_left.button_type = "success"
                self.max_btn_left.disabled = False

                self.max_btn_right.label = "Start Test"
                self.max_btn_right.button_type = "success"
                self.max_btn_right.disabled = False

                self.rfd_btn_left.label = "Start Test"
                self.rfd_btn_left.button_type = "success"
                self.rfd_btn_left.disabled = False

                self.rfd_btn_right.label = "Start Test"
                self.rfd_btn_right.button_type = "success"
                self.rfd_btn_right.disabled = False

        elif Test.testing_active(self):
            if Test.Cft.active:
                if Test.Cft.complete:
                    self.cft_btn.label = "CFT Test Complete"
                    self.cft_btn.button_type = "warning"
                    Test.Cft.active = False

                    _filename =  self._user_layout.name.replace(" ", "_") + self._user_layout.grip_type.replace(" ", "_") + "_CFT_" + date.today().strftime("%d-%m-%y") + ".txt"
                    _full_fn = os.path.join(self._path, _filename)
                    np.savetxt(_full_fn, np.column_stack((self.x, self.y)))

                    results = analyse_data(self.x, self.y, 7, 3)
                    self.cft_layout.update_results(results)

                else:
                    if self.timer_cft.state == TimerState.GoState:
                        self.cft_layout.reps = self.timer_cft.reps
                    self.timer_cft.update(
                        self, self.timer_cft, self.cft_layout, Test.Cft
                    )
                    self.cft_source.stream({"x": self.xnew, "y": self.ynew})

            elif Test.MaxLeft.active:
                if Test.MaxLeft.complete:
                    self.max_btn_left.label = "Max Test - Left - Complete"
                    self.max_btn_left.button_type = "warning"
                    Test.MaxLeft.active = False

                    _filename =  self._user_layout.name.replace(" ", "_") + self._user_layout.grip_type.replace(" ", "_") + "_MaxLeft_" + date.today().strftime("%d-%m-%y") + ".txt"
                    _full_fn = os.path.join(self._path, _filename)
                    np.savetxt(_full_fn, np.column_stack((self.x, self.y)))

                    results = analyse_max(
                        self.max_source_l.data["x"], self.max_source_l.data["y"]
                    )
                    self.max_layout.update_results(results)

                else:
                    self.timer_max.update(
                        self, self.timer_max, self.max_layout, Test.MaxLeft
                    )
                    self.max_source_l.stream({"x": self.xnew, "y": self.ynew})

                    if len(self.max_source_l.data["y"]) > 1:
                        _, max_left = analyse_max(
                            self.max_source_l.data["x"], self.max_source_l.data["y"]
                        )

                        self.max_layout.div_lh = max_left
                        TestResults.max_left = max_left

            elif Test.MaxRight.active:
                if Test.MaxRight.complete:
                    self.max_btn_right.label = "Max Test - Right - Complete"
                    self.max_btn_right.button_type = "warning"
                    Test.MaxRight.active = False

                    _filename =  self._user_layout.name.replace(" ", "_") + self._user_layout.grip_type.replace(" ", "_") + "_MaxRight_" + date.today().strftime("%d-%m-%y") + ".txt"
                    _full_fn = os.path.join(self._path, _filename)
                    np.savetxt(_full_fn, np.column_stack((self.x, self.y)))

                    results = analyse_max(
                        self.max_source_r.data["x"], self.max_source_r.data["y"]
                    )
                    self.max_layout.update_results(results)

                else:
                    self.timer_max.update(
                        self, self.timer_max, self.max_layout, Test.MaxRight
                    )
                    self.max_source_r.stream({"x": self.xnew, "y": self.ynew})

                    if len(self.max_source_r.data["y"]) > 1:
                        _, max_right = analyse_max(
                            self.max_source_r.data["x"], self.max_source_r.data["y"]
                        )

                        self.max_layout.div_rh = max_right
                        TestResults.max_right = max_right

            elif Test.RfdLeft.active:
                if Test.RfdLeft.complete:
                    self.rfd_btn_left.label = "RFD Test Complete"
                    self.rfd_btn_left.button_type = "warning"
                    Test.RfdLeft.active = False

                    _filename =  self._user_layout.name.replace(" ", "_") + self._user_layout.grip_type.replace(" ", "_") + "_RFDLeft_" + date.today().strftime("%d-%m-%y") + ".txt"
                    _full_fn = os.path.join(self._path, _filename)
                    np.savetxt(_full_fn, np.column_stack((self.x, self.y)))
                               
                    results = analyse_rfd(
                        self.rfd_source_l.data["x"], self.rfd_source_l.data["y"]
                    )
                    self.rfd_layout.update_results(results)

                    (
                        fmax,
                        _,
                        _,
                        _,
                        _,
                        _,
                        _,
                        rfd_average,
                        _,
                        _,
                        time_to_peak_rfd
                    ) = results
                    # (fmax, rfd_max_x1, rfd_max_y1, rfd_max_t20, rfd_max_t80, f20, f80, rfd_average, tmeans, fmeans, time_to_peak_rfd) = analyse_rfd(x, y)
                    """
                    Reset the test if the load was applied too early
                    """

                    if fmax == 0:
                        Test.RfdRLeft.complete = False
                        self.rfd_btn_left.label = "Start RFD Test"
                        self.rfd_btn_left.button_type = "success"
                        self.reset()
                    else:
                        TestResults.rfd_left = np.round(fmax, 1)
                        self.rfd_layout.div_lh = (
                            TestResults.rfd_left,
                            rfd_average,
                            time_to_peak_rfd,
                        )

                else:
                    self.timer_rfd.update(
                        self, self.timer_rfd, self.rfd_layout, Test.RfdLeft
                    )
                    self.rfd_source_l.stream({"x": self.xnew, "y": self.ynew})

            elif Test.RfdRight.active:
                if Test.RfdRight.complete:
                    self.rfd_btn_right.label = "RFD Test Complete"
                    self.rfd_btn_right.button_type = "warning"
                    Test.RfdRight.active = False

                    _filename =  self._user_layout.name.replace(" ", "_") + "_" + self._user_layout.grip_type.replace(" ", "_") + "_RFDRight_" + date.today().strftime("%d-%m-%y") + ".txt"
                    _full_fn = os.path.join(self._path, _filename)
                    np.savetxt(_full_fn, np.column_stack((self.x, self.y)))
                               
                    results = analyse_rfd(
                        self.rfd_source_r.data["x"], self.rfd_source_r.data["y"]
                    )
                    self.rfd_layout.update_results(results)

                    (
                        fmax,
                        _,
                        _,
                        _,
                        _,
                        _,
                        _,
                        rfd_average,
                        _,
                        _,
                        time_to_peak_rfd
                    ) = results
                    # (fmax, rfd_max_x1, rfd_max_y1, rfd_max_t20, rfd_max_t80, f20, f80, rfd_average, tmeans, fmeans, time_to_peak_rfd) = analyse_rfd(x, y)
                    """
                    Reset the test if the load was applied too early
                    """

                    if fmax == 0:
                        Test.RfdRight.complete = False
                        self.rfd_btn_right.label = "Start RFD Test"
                        self.rfd_btn_right.button_type = "success"
                        self.reset()
                    else:
                        TestResults.rfd_right = np.round(fmax, 1)
                        self.rfd_layout.div_rh = (
                            TestResults.rfd_right,
                            rfd_average,
                            time_to_peak_rfd,
                        )

                else:
                    self.timer_rfd.update(
                        self, self.timer_rfd, self.rfd_layout, Test.RfdRight
                    )
                    self.rfd_source_r.stream({"x": self.xnew, "y": self.ynew})
        elif Test.testing_complete(self) and not Test.testing_active(self):
            self.analysis_layout.results = 0
            self.analysis_layout.prediction_results = test_results()

        self.reset()


async def connect(cft):
    tindeq = TindeqProgressor(cft)
    await tindeq.connect()
    cft.tindeq = tindeq
    await cft.tindeq.soft_tare()
    await asyncio.sleep(1)
    cft.reset()


tt = TindeqTests()
apps = {"/": Application(FunctionHandler(tt.make_document))}
server = Server(apps, port=5007)
server.start()

if __name__ == "__main__":
    io_loop = tornado.ioloop.IOLoop.current()
    print("Opening Bokeh application on http://localhost:5007/")
    io_loop.add_callback(server.show, "/")
    io_loop.start()
