from bokeh.models import Div, Spinner, TextInput, Select, TextAreaInput
from bokeh.layouts import Column, Row


class UserLayout:
    def __init__(self):
        title = Div(
            text="User Details",
            styles={
                "font-size": "300%",
                "font_style": "bold",
                "color": "Blue",
                "text-align": "left",
                "width": "100%",
            },
        )
        _grip_types = ["Half Crimp", "4 Finger Open", "3 Finger Drag"]
        _name = TextInput(
            title="Name",
            value="",
            styles={"font-size": "150%", "color": "black", "text-align": "left"},
        )
        self._weight = Spinner(
            title="Weight",
            low=50,
            high=120,
            step=1,
            value=70,
            width=80,
            styles={"font-size": "150%", "color": "black", "text-align": "left"},
        )
        _email = TextInput(
            title="Email",
            value="",
            styles={"font-size": "150%", "color": "black", "text-align": "left"},
        )
        _grip_type = Select(
            title="Grip Type",
            value="Half Crimp",
            options=_grip_types,
            styles={"font-size": "150%", "color": "black", "text-align": "left"},
        )
        _notes = TextAreaInput(
            title="Notes",
            rows=6,
            styles={"font-size": "150%", "color": "black", "text-align": "left"},
        )
        title_row = Row(title)
        column_1 = Column(_name, self._weight, _email, margin=(0, 100, 0, 50))
        column_2 = Column(_grip_type, _notes)
        user_row = Row(column_1, column_2)
        self.column = Column(title_row, user_row)

    @property
    def weight(self):
        return self._weight.value
