from bokeh.models import Div, Spinner, TextInput
from bokeh.layouts import Column, Row

class UserLayout:
    def __init__(self):
        self.title = Div(
            text="User Details",
            styles={
                "font-size": "300%",
                "font_style": "bold",
                "color": "Blue",
                "text-align": "left",
                "width": "100%",
            }
        )
        self.name = TextInput(value="", title="Name", styles={"font-size": "150%", "color": "black", "text-align": "left"})
        self.weight = Spinner(title="Weight", low=50, high=120, step=1, value=70, width=80, styles={"font-size": "150%", "color": "black", "text-align": "left"})
        self.email = TextInput(value="", title="Email", styles={"font-size": "150%", "color": "black", "text-align": "left"})

        self.column = Column(self.title, self.name, self.weight, self.email)
        self.row = Row(self.column)