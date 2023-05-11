from bokeh.models import Button, Div
from bokeh.layouts import Row, Column

from src.layouts.layout import Layout

class MaxLayout(Layout):
    def __init__(self, duration, title="Max Strength Test"):
        Layout.__init__(self, title, duration)

        self._btn_left = Button(label="Waiting for Progressor...")
        self._btn_left.button_type = "danger"
        self._btn_right = Button(label="Waiting for Progressor...")
        self._btn_right.button_type = "danger"
        
        self.div_lh = Div(
            text="Left hand: ---",
            styles={"font-size": "200%", "color": "black", "text-align": "center"},
        )
        
        self.div_rh = Div(
            text="Right hand: ---",
            styles={"font-size": "200%", "color": "black", "text-align": "center"},
        )

        self.widgets = Column(
            self._btn_left,
            self.div_lh,
            self._btn_right,
            self.div_rh,
            self.countdown_timer
        )
        self.row = Row(self.widgets, self.fig_column)
        self.column = Column(self.title, self.row)

    @property    
    def btn_left(self):
        return self._btn_left
    
    @property    
    def btn_right(self):
        return self._btn_right
