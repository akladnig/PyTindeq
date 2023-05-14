from bokeh.models import Div, Spinner, TextInput, Select, TextAreaInput
from bokeh.layouts import Column, Row

from src.templates.styles import Styles

class UserLayout:
    def __init__(self):
        title = Div(
            text="User Details",
            styles=Styles.title,
        )
        _grip_types = ["Half Crimp", "4 Finger Open", "3 Finger Drag", "Lock Off"]
        _name = TextInput(
            title="Name",
            value="",
            styles=Styles.normal,
        )
        self._weight = Spinner(
            title="Weight",
            low=50,
            high=120,
            step=1,
            value=70,
            width=80,
            styles=Styles.normal,
        )
        _grip_type = Select(
            title="Grip Type",
            value="Half Crimp",
            options=_grip_types,
            styles=Styles.normal,
        )
        _notes = TextAreaInput(
            title="Notes",
            rows=8,
            cols=40,
            styles=Styles.normal,
        )
        title_row = Row(title)
        column_1 = Column(_name, self._weight, margin=(0, 100, 0, 50))
        column_2 = Column(_grip_type, _notes)
        user_row = Row(column_1, column_2)
        self.column = Column(title_row, user_row)

    @property
    def weight(self):
        return self._weight.value
