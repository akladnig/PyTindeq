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
        
        self._div_lh = Div(
            text="Left hand:  0.00 kg" ,
            styles={"font-size": "200%", "color": "black", "text-align": "center"},
        )
        
        self._div_rh = Div(
            text="Right hand: 0.00 kg",
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
    
    @property
    def div_lh(self):
        return self._div_lh
    
    @div_lh.setter
    def div_lh(self, value):
        self._div_lh.text = 'Left hand:  '+str(value)  +' kg'

    @property
    def div_rh(self):
        return self._div_rh
    
    @div_rh.setter
    def div_rh(self, value):
        self._div_rh.text = 'Right hand: '+str(value)  +' kg'