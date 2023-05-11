import threading
import tornado

from src.max_test import start_test_max

def max_onclick_left(self):
    self.duration = 20
    self.source.data = dict(x=[], y=[])
    self.max_layoutest_left = True
    self.max_layoutest_right = False

    def sctn():
        self.max_layoutest_left = False

    s = threading.Timer(self.duration, sctn)
    s.start()
    io_loop = tornado.ioloop.IOLoop.current()
    io_loop.add_callback(start_test_max, self)

def max_onclick_right(self):
    self.duration = 20
    self.source.data = dict(x=[], y=[])
    self.max_layoutest_right = True
    self.max_layoutest_left = False
    # self.btn_right.disabled=True
    # self.btn_left.disabled=True

    def sctn():
        self.max_layoutest_right = False
        s = threading.Timer(self.duration, sctn)
        s.start()
        io_loop = tornado.ioloop.IOLoop.current()
        io_loop.add_callback(start_test_max, self)

