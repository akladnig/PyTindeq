from src.tindeq import TindeqProgressor
from src.analysis import analyse_data, Test, TestStatus
from src.timers import CountdownTimer, TimerState
from src.cft_timers import  IdleState

# from src.cft import cft
from src.layouts.cft_layout import CftLayout
from src.cft_test import start_test_cft

from src.layouts.max_layout import MaxLayout
from src.max_test import start_test_max
# from src.controls.max_controls import max_onclick_left, max_onclick_right

from src.layouts.rfd_layout import RfdLayout
from src.layouts.user_layout import UserLayout

from src.playsounds import sound_thread

import numpy as np
import asyncio
import tornado
import threading

from bokeh.server.server import Server
from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler
from bokeh.plotting import figure, ColumnDataSource
from bokeh.layouts import row, column
from bokeh.models import Button, Slider, Div, Band, Whisker, Range1d

from bokeh.io import curdoc


class TindeqTests:
    def __init__(self):
        self.x = []
        self.y = []
        self.xnew = []
        self.ynew = []
        self.active = False
        self.total_reps = 24
        self.duration = 10 * self.total_reps
        self.state = IdleState
        self.statex = TimerState.IdleStatex
        self.test = Test.MaxLeft
        self.st = sound_thread()
        self.test_done = False
        self.analysed = False
        self.tindeq = None
        io_loop = tornado.ioloop.IOLoop.current()
        io_loop.add_callback(connect, self)

    def log_force_sample(self, time, weight):
        if self.active or TestStatus.active:
            # print(time)
            self.xnew.append(time)
            self.ynew.append(weight)
            self.x.append(time)
            self.y.append(weight)

    def reset(self):
        self.xnew, self.ynew = [], []

    def make_document(self, doc):
        self.cft_source = ColumnDataSource(data=dict(x=[], y=[]))
        self.max_source = ColumnDataSource(data=dict(x=[], y=[]))
        self.rfd_source = ColumnDataSource(data=dict(x=[], y=[]))

        TestStatus.active = False
        TestStatus.complete = False

        doc.title = "Tindeq Tests"
        '''
        User Details Layout
        '''
        user_layout = UserLayout()
        user_row = user_layout.row

        '''
        Critical Force Testing Layout
        '''
        self.cft_layout = CftLayout(7)
        self.timer_cft = CountdownTimer(1, 7, self.cft_layout)

        self.cft_fig = self.cft_layout.fig

        self.cft_fig.line(x="x", y="y", source=self.cft_source)

        self.cft_layout.fig = 90
        self.cft_layout.set_x_range(80)
        # self.cft_fig.x_range = Range1d(0, 80)
        
        def cft_on_slide(attr, old, new):
            print(attr, old, new)
            self.cft_layout.reps = new
            self.cft_layout.set_x_range(new*10)

        self.cft_slider = self.cft_layout.reps_slider
        self.cft_slider.on_change('value', cft_on_slide)

        def cft_onclick():
            self.test = Test.Cft
            self.total_reps = self.cft_layout.reps_slider.value
            print("clicked" +str(self.total_reps))
            self.cft_layout.set_x_range(100)
            self.cft_fig.x_range = Range1d(0, 180)

            self.duration = self.total_reps * 10
            io_loop = tornado.ioloop.IOLoop.current()
            io_loop.add_callback(start_test_cft, self, self.timer_cft, self.total_reps)

        self.cft_btn = self.cft_layout.btn
        self.cft_btn.on_click(cft_onclick)


        cft_column = self.cft_layout.column

        '''
        Rate of Force Development Testing
        '''
        self.rfd_layout = RfdLayout()
        self.timer_rfd = CountdownTimer(1,10, self.rfd_layout)

        def rfd_onclick_left():
            self.source.data = dict(x=[], y=[])
            self.rfdtest_left = True
            self.rfdtest_right = False

            def sctn():
                self.rfdtest_left = False

            s = threading.Timer(self.duration, sctn)
            s.start()
            io_loop = tornado.ioloop.IOLoop.current()
            io_loop.add_callback(start_test_max, self, self.timer_max)

        def rfd_onclick_right():
            self.source.data = dict(x=[], y=[])
            self.rfdtest_right = True
            self.rfdtest_left = False
            # self.btn_right.disabled=True
            # self.btn_left.disabled=True

            def sctn():
                self.rfdtest_right = False
                s = threading.Timer(self.duration, sctn)
                s.start()
                io_loop = tornado.ioloop.IOLoop.current()
                io_loop.add_callback(start_test_max, self, self.timer_max)

        self.rfd_btn_left = self.rfd_layout.btn_left
        self.rfd_btn_left.on_click(rfd_onclick_left)
        self.rfd_btn_right = self.rfd_layout.btn_right

        self.rfd_btn_right.on_click(rfd_onclick_right)

        rfd_fig = self.rfd_layout.fig
        rfd_fig.line(x="x", y="y", source=self.rfd_source)
        rfd_column = self.rfd_layout.column

        '''
        Max Strength Testing
        '''
        self.max_layout = MaxLayout(20)
        self.timer_max = CountdownTimer(1, 20, self.max_layout)

        self.max_fig = self.max_layout.fig
        self.max_fig.line(x="x", y="y", source=self.max_source)

        def max_onclick_left():
            self.max_source.data = dict(x=[], y=[])
            self.max_layoutest_left = True
            self.max_layoutest_right = False

            def sctn():
                self.max_layoutest_left = False

            s = threading.Timer(self.duration, sctn)
            s.start()
            io_loop = tornado.ioloop.IOLoop.current()
            io_loop.add_callback(start_test_max, self, self.timer_max)

        def max_onclick_right():
            self.max_source.data = dict(x=[], y=[])
            self.max_layoutest_right = True
            self.max_layoutest_left = False
            # self.btn_right.disabled=True
            # self.btn_left.disabled=True

            def sctn():
                self.max_layoutest_right = False
                s = threading.Timer(self.duration, sctn)
                s.start()
                io_loop = tornado.ioloop.IOLoop.current()
                io_loop.add_callback(start_test_max, self, self.timer_max)

        self.max_btn_left = self.max_layout.btn_left
        self.max_btn_left.on_click(max_onclick_left)
        self.max_btn_right = self.max_layout.btn_right
        self.max_btn_right.on_click(max_onclick_right)

        max_column =self. max_layout.column

        doc.add_root(column(user_row, max_column, cft_column, rfd_column))
        doc.add_periodic_callback(self.update, 50)

    def update(self):
        if self.test_done and not self.analysed:
            np.savetxt("test.txt", np.column_stack((self.x, self.y)))
            x = np.array(self.x)
            y = np.array(self.y)
            if self.test == Test.Cft:
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
            elif self.test == Test.MaxLeft:
                self.max_btn_left.label = "Max Test - Left - Complete"
                self.max_btn_left.button_type = "warning"        
            elif self.test == Test.MaxRight:
                self.max_btn_right.label = "Max Test - Right - Complete"
                self.max_btn_right.button_type = "warning" 

        else:
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
            if self.test == Test.Cft:                    
                self.cft_reps = self.total_reps
                # self.state.update(self)
                self.timer_cft.update(self, self.timer_cft, self.cft_layout)
                self.cft_source.stream({"x": self.xnew, "y": self.ynew})
            elif self.test == Test.MaxLeft:
                self.timer_max.update(self, self.timer_max, self.max_layout)
                self.max_source.stream({"x": self.xnew, "y": self.ynew})

            # nlaps = self.duration // 10
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

