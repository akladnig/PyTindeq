from src.tindeq import TindeqProgressor
from src.analysis import analyse_data, Test
from src.timers import CountdownTimer, TimerState

from src.layouts.cft_layout import CftLayout
from src.layouts.test_layout import TestLayout
from src.layouts.user_layout import UserLayout

from src.start_test import start_test

from src.playsounds import sound_thread

import numpy as np
import asyncio
import tornado
import threading

from bokeh.server.server import Server
from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler
from bokeh.plotting import ColumnDataSource
from bokeh.layouts import row, Column
from bokeh.models import Button, Slider, Div, Band, Whisker, Range1d


class TindeqTests:
    def __init__(self):
        self.x = []
        self.y = []
        self.xnew = []
        self.ynew = []
        self.active = False
        # self.total_reps = 24
        self.total_reps = 2
        self.cft_go_duration = 7
        self.cft_rest_duration = 3
        self.cft_duration = 10 * self.total_reps
        self.max_go_duration = 5
        self.rfd_go_duration = 5
        self.max_rest_duration = 0
        self.rfd_rest_duration = 0
        # self.state = IdleState
        self.state = TimerState.IdleState
        self.st = sound_thread()
        self.analysed = False
        self.tindeq = None
        io_loop = tornado.ioloop.IOLoop.current()
        io_loop.add_callback(connect, self)

    def log_force_sample(self, time, weight):
        if Test.testing_active:
            # print(time)
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
        user_layout = UserLayout()
        user_column = user_layout.column

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

        # def cft_on_slide(attr, old, new):
        #     print(attr, old, new)
        #     self.cft_layout.reps = new

        # self.cft_slider = self.cft_layout.reps_slider
        # self.cft_slider.on_change('value', cft_on_slide)

        def cft_onclick():
            Test.TestingStarted = True
            Test.Cft.active = True
            print("clicked " + str(self.total_reps))
            io_loop = tornado.ioloop.IOLoop.current()
            io_loop.add_callback(
                start_test, self, self.timer_cft, Test.Cft
            )

        self.cft_btn = self.cft_layout.btn
        self.cft_btn.on_click(cft_onclick)

        cft_column = self.cft_layout.column

        """
        Rate of Force Development Testing
        """
        self.rfd_layout = TestLayout(self.rfd_go_duration, Test.RfdLeft)
        self.timer_rfd = CountdownTimer(
            1, self.rfd_go_duration, self.rfd_rest_duration, self.rfd_layout
        )

        self.rfd_fig = self.rfd_layout.fig

        def rfd_onclick_left():
            Test.TestingStarted = True
            Test.RfdLeft.active = True
            Test.RfdLeft.complete = False     
            self.rfd_fig.line(
                legend_label="Left",
                x="x",
                y="y",
                source=self.rfd_source_l,
                line_color="blue",
            )
            self.rfd_source_l.data = dict(x=[], y=[])
            self.rfdtest_left = True
            self.rfdtest_right = False

            def sctn():
                self.rfdtest_left = False

            s = threading.Timer(self.rfd_go_duration, sctn)
            s.start()
            io_loop = tornado.ioloop.IOLoop.current()
            io_loop.add_callback(start_test, self, self.timer_rfd, Test.RfdLeft)

        def rfd_onclick_right():
            Test.TestingStarted = True
            Test.RfdRight.active = True          
            self.rfd_fig.line(
                legend_label="Right",
                x="x",
                y="y",
                source=self.rfd_source_r,
                line_color="green",
            )
            self.rfd_source_r.data = dict(x=[], y=[])
            self.rfdtest_right = True
            self.rfdtest_left = False
            # self.btn_right.disabled=True
            # self.btn_left.disabled=True

            def sctn():
                self.rfdtest_right = False

            s = threading.Timer(self.rfd_go_duration, sctn)
            s.start()
            io_loop = tornado.ioloop.IOLoop.current()
            io_loop.add_callback(start_test, self, self.timer_rfd, Test.RfdRight)

        self.rfd_btn_left = self.rfd_layout.btn_left
        self.rfd_btn_left.on_click(rfd_onclick_left)
        self.rfd_btn_right = self.rfd_layout.btn_right
        self.rfd_btn_right.on_click(rfd_onclick_right)

        rfd_column = self.rfd_layout.column

        """
        Max Strength Testing
        """
        self.max_layout = TestLayout(self.max_go_duration, Test.MaxLeft)
        self.timer_max = CountdownTimer(
            1, self.max_go_duration, self.max_rest_duration, self.max_layout
        )

        self.max_fig = self.max_layout.fig

        def max_onclick_left():
            Test.TestingStarted = True
            Test.MaxLeft.active = True          
            self.max_fig.line(
                legend_label="Left",
                x="x",
                y="y",
                source=self.max_source_l,
                line_color="blue",
            )
            self.max_source_l.data = dict(x=[], y=[])
            # self.max_layoutest_left = True
            # self.max_layoutest_right = False

            # def sctn():
            #     self.max_layoutest_left = False

            # s = threading.Timer(self.max_go_duration, sctn)
            # s.start()
            io_loop = tornado.ioloop.IOLoop.current()
            io_loop.add_callback(start_test, self, self.timer_max, Test.MaxLeft)

        def max_onclick_right():
            Test.TestingStarted = True
            Test.MaxRight.active = True
            self.max_fig.line(
                legend_label="Right",
                x="x",
                y="y",
                source=self.max_source_r,
                line_color="green",
            )
            self.max_source_r.data = dict(x=[], y=[])
            # self.max_layoutest_right = True
            # self.max_layoutest_left = False
            # self.btn_right.disabled=True
            # self.btn_left.disabled=True

            # def sctn():
            #     self.max_layoutest_right = False

            # s = threading.Timer(self.max_go_duration, sctn)
            # s.start()
            io_loop = tornado.ioloop.IOLoop.current()
            io_loop.add_callback(start_test, self, self.timer_max, Test.MaxRight)

        self.max_btn_left = self.max_layout.btn_left
        self.max_btn_left.on_click(max_onclick_left)
        self.max_btn_right = self.max_layout.btn_right
        self.max_btn_right.on_click(max_onclick_right)

        max_column = self.max_layout.column

        doc.add_root(Column(user_column, max_column, cft_column, rfd_column))
        doc.add_periodic_callback(self.update, 50)

    def update(self):
        """
        There are three testing states:
        - No testing started:           testing_complete = false and testing_active = false
        - Testing commenced and active: testing_complete = false and testing_active = true
        - Testing complete:             testing_complete = true  and testing_active = false
        """
        if not Test.TestingStarted:
            if self.tindeq is not None:
                self.cft_btn.label = "Start CFT Test"
                self.cft_btn.button_type = "success"
                self.max_btn_left.label = "Start Max Test - Left"
                self.max_btn_left.button_type = "success"
                self.max_btn_right.label = "Start Max Test - Right"
                self.max_btn_right.button_type = "success"
                self.rfd_btn_left.label = "Start RFD Test - Left"
                self.rfd_btn_left.button_type = "success"
                self.rfd_btn_right.label = "Start RFD Test - Right"
                self.rfd_btn_right.button_type = "success"
        elif not Test.testing_complete(self) and Test.testing_active(self):
            if Test.Cft.active:
                # print("cft active")
                if Test.Cft.complete:
                    print("Cft Test ", Test.Cft.active, Test.Cft.complete)
                    self.cft_btn.label = "CFT Test Complete"
                    self.cft_btn.button_type = "warning"
                    Test.Cft.active = False

                    np.savetxt("test.txt", np.column_stack((self.x, self.y)))
                    x = np.array(self.x)
                    y = np.array(self.y)
                    results = analyse_data(x, y, 7, 3)
                    (
                        tmeans,
                        fmeans,
                        e_fmeans,
                        msg,
                        critical_load,
                        load_asymptote,
                        predicted_force,
                    ) = results
                    self.cft_layout.results = "<p><b>Results</b></p>" + msg

                    fill_src = ColumnDataSource(
                        dict(
                            x=tmeans,
                            upper=predicted_force,
                            lower=load_asymptote * np.ones_like(tmeans),
                        )
                    )
                    self.cft_fig.add_layout(
                        Band(
                            base="x",
                            lower="lower",
                            upper="upper",
                            source=fill_src,
                            fill_alpha=0.7,
                        )
                    )
                    self.cft_fig.circle(tmeans, fmeans, color="red", size=5, line_alpha=0)

                    esource = ColumnDataSource(
                        dict(x=tmeans, upper=fmeans + e_fmeans, lower=fmeans - e_fmeans)
                    )
                    self.cft_fig.add_layout(
                        Whisker(
                            source=esource,
                            base="x",
                            upper="upper",
                            lower="lower",
                            level="overlay",
                        )
                    )
                else:
                    self.cft_reps = self.total_reps
                    self.timer_cft.update(self, self.timer_cft, self.cft_layout, Test.Cft)
                    self.cft_source.stream({"x": self.xnew, "y": self.ynew})

            elif Test.MaxLeft.active:
                if Test.MaxLeft.complete:
                    print(
                        "update max left ", Test.MaxLeft.active, Test.MaxLeft.complete
                    )
                    self.max_btn_left.label = "Max Test - Left - Complete"
                    self.max_btn_left.button_type = "warning"
                    Test.MaxLeft.active = False

                    x_max=np.array(self.max_source_l.data["x"], dtype=float)
                    y_max=np.array(self.max_source_l.data["y"], dtype=float)
                    max_index = np.argmax(np.array(self.max_source_l.data["y"], dtype=float))
                    self.max_fig.circle(x_max[max_index], y_max[max_index], color="red", size=5, line_alpha=0)
                else:
                    self.timer_max.update(
                        self, self.timer_max, self.max_layout, Test.MaxLeft
                    )
                    self.max_source_l.stream({"x": self.xnew, "y": self.ynew})

                    if len(self.max_source_l.data["y"]) > 1:
                        max_left = np.round(
                            np.max(np.array(self.max_source_l.data["y"], dtype=float)), 2
                        )
                        self.max_layout.div_lh = max_left

            elif Test.MaxRight.active:
                if Test.MaxRight.complete:
                    self.max_btn_right.label = "Max Test - Right - Complete"
                    self.max_btn_right.button_type = "warning"
                    Test.MaxRight.active = False

                    x_max=np.array(self.max_source_r.data["x"], dtype=float)
                    y_max=np.array(self.max_source_r.data["y"], dtype=float)
                    max_index = np.argmax(np.array(self.max_source_r.data["y"], dtype=float))
                    self.max_fig.circle(x_max[max_index], y_max[max_index], color="red", size=5, line_alpha=0)
                else:
                    self.timer_max.update(
                        self, self.timer_max, self.max_layout, Test.MaxRight
                    )
                    self.max_source_r.stream({"x": self.xnew, "y": self.ynew})

                    if len(self.max_source_r.data["y"]) > 1:
                        max_right = np.round(
                            np.max(np.array(self.max_source_r.data["y"], dtype=float)), 2
                        )
                        self.max_layout.div_rh = max_right

            elif Test.RfdLeft.active:
                if Test.RfdLeft.complete:
                    print(
                        "update rfd left ", Test.RfdLeft.active, Test.RfdLeft.complete
                    )
                    self.rfd_btn_left.label = "Rfd Test - Left - Complete"
                    self.rfd_btn_left.button_type = "warning"
                    Test.RfdLeft.active = False

                    x=np.array(self.rfd_source_l.data["x"], dtype=float)
                    y=np.array(self.rfd_source_l.data["y"], dtype=float)
                    rfd_index = np.argmax(np.array(self.rfd_source_l.data["y"], dtype=float))
                    self.rfd_fig.circle(x[rfd_index], y[rfd_index], color="red", size=5, line_alpha=0)

                    ymax=np.max(x)
                    f80=(ymax*0.8)
                    f20=(ymax*0.2)
                    ix= np.where( y>f80 )[0]                
                    t80 = x[ix[0]]
                    ix= np.where( y>f20)[0]                
                    t20 = x[ix[0]]  
                    f=(f80-f20)
                    t= t80-t20

                    self.rfd_left= np.round(f/t,2)
                    self.rfd_layout.div_lh = self.rfd_left
                    self.rfd_fig.line([t20,t80], [f20,f80], line_color="red", line_width=2)
                              
                else:
                    self.timer_rfd.update(
                        self, self.timer_rfd, self.rfd_layout, Test.RfdLeft
                    )
                    self.rfd_source_l.stream({"x": self.xnew, "y": self.ynew})

                    if len(self.rfd_source_l.data["y"]) > 1:
                        rfd_left = np.round(
                            np.max(np.array(self.rfd_source_l.data["y"], dtype=float)), 2
                        )
                        self.rfd_layout.div_lh = rfd_left

            elif Test.RfdRight.active:
                if Test.RfdRight.complete:
                    self.rfd_btn_right.label = "Rfd Test - Right - Complete"
                    self.rfd_btn_right.button_type = "warning"
                    Test.RfdRight.active = False

                    x=np.array(self.rfd_source_r.data["x"], dtype=float)
                    y=np.array(self.rfd_source_r.data["y"], dtype=float)
                    rfd_index = np.argmax(np.array(self.rfd_source_r.data["y"], dtype=float))
                    self.rfd_fig.circle(x[rfd_index], y[rfd_index], color="red", size=5, line_alpha=0)

                    ymax=np.max(x)
                    f80=(ymax*0.8)
                    f20=(ymax*0.2)
                    ix= np.where( y>f80 )[0]                
                    t80 = x[ix[0]]
                    ix= np.where( y>f20)[0]                
                    t20 = x[ix[0]]  
                    f=(f80-f20)
                    t= t80-t20

                    self.rfd_right= np.round(f/t,2)
                    self.rfd_layout.div_rh = self.rfd_right
                    self.rfd_fig.line([t20,t80], [f20,f80], line_color="red", line_width=2)
                else:
                    self.timer_rfd.update(
                        self, self.timer_rfd, self.rfd_layout, Test.RfdRight
                    )
                    self.rfd_source_r.stream({"x": self.xnew, "y": self.ynew})

                    if len(self.rfd_source_r.data["y"]) > 1:
                        rfd_right = np.round(
                            np.max(np.array(self.rfd_source_r.data["y"], dtype=float)), 2
                        )
                        self.rfd_layout.div_rh = rfd_right

        elif not Test.testing_complete(self) and not self.analysed:
            np.savetxt("test.txt", np.column_stack((self.x, self.y)))
            x = np.array(self.x)
            y = np.array(self.y)
            if Test.Cft.active:
                self.cft_btn.label = "CFT Test Complete"
                self.cft_btn.button_type = "warning"

                results = analyse_data(x, y, 7, 3)
                (
                    tmeans,
                    fmeans,
                    e_fmeans,
                    msg,
                    critical_load,
                    load_asymptote,
                    predicted_force,
                ) = results
                self.cft_results_div.text = "<p><b>Results</b></p>" + msg

                fill_src = ColumnDataSource(
                    dict(
                        x=tmeans,
                        upper=predicted_force,
                        lower=load_asymptote * np.ones_like(tmeans),
                    )
                )
                self.cft_fig.add_layout(
                    Band(
                        base="x",
                        lower="lower",
                        upper="upper",
                        source=fill_src,
                        fill_alpha=0.7,
                    )
                )
                self.cft_fig.circle(tmeans, fmeans, color="red", size=5, line_alpha=0)

                esource = ColumnDataSource(
                    dict(x=tmeans, upper=fmeans + e_fmeans, lower=fmeans - e_fmeans)
                )
                self.cft_fig.add_layout(
                    Whisker(
                        source=esource,
                        base="x",
                        upper="upper",
                        lower="lower",
                        level="overlay",
                    )
                )
                self.analysed = True
        self.reset()


async def connect(cft):
    tindeq = TindeqProgressor(cft)
    await tindeq.connect()
    cft.tindeq = tindeq
    await cft.tindeq.soft_tare()
    await asyncio.sleep(5)


tt = TindeqTests()
apps = {"/": Application(FunctionHandler(tt.make_document))}
server = Server(apps, port=5007)
server.start()

if __name__ == "__main__":
    io_loop = tornado.ioloop.IOLoop.current()
    print("Opening Bokeh application on http://localhost:5007/")
    io_loop.add_callback(server.show, "/")
    io_loop.start()
