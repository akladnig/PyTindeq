from bokeh.models import Button, Div
from bokeh.layouts import Row, Column

from src.layouts.layout import Layout

class RfdLayout(Layout):
    def __init__(self, title = "Rate of Force Development Test", duration = 12):
        Layout.__init__(self, title, duration)

        self._btn_left = Button(label="Waiting for Progressor...")
        self._btn_left.button_type = "danger"
        self._btn_right = Button(label="Waiting for Progressor...")
        self._btn_right.button_type = "danger"
        
        self._div_lh = Div(
            text="Left hand: ---",
            styles={"font-size": "200%", "color": "black", "text-align": "center"},
        )
        
        self._div_rh = Div(
            text="Right hand: ---",
            styles={"font-size": "200%", "color": "black", "text-align": "center"},
        )
        self.widgets = Column(
            self._btn_left,
            self._div_lh,
            self._btn_right,
            self._div_rh,
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