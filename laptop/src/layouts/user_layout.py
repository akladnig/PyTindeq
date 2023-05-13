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
        grip_types = ["Half Crimp", "4 Finger Open", "3 Finger Drag"]
        name = TextInput(
            title="Name",
            value="",
            styles={"font-size": "150%", "color": "black", "text-align": "left"},
        )
        weight = Spinner(
            title="Weight",
            low=50,
            high=120,
            step=1,
            value=70,
            width=80,
            styles={"font-size": "150%", "color": "black", "text-align": "left"},
        )
        email = TextInput(
            title="Email",
            value="",
            styles={"font-size": "150%", "color": "black", "text-align": "left"},
        )
        grip_type = Select(
            title="Grip Type",
            value="Half Crimp",
            options=grip_types,
            styles={"font-size": "150%", "color": "black", "text-align": "left"},
        )
        notes = TextAreaInput(
            title="Notes",
            rows=6,
            styles={"font-size": "150%", "color": "black", "text-align": "left"},
        )
        title_row = Row(title)
        column_1 = Column(name, weight, email, margin=(0, 100, 0, 50))
        column_2 = Column(grip_type, notes)
        user_row = Row(column_1, column_2)
        self.column = Column(title_row, user_row)
