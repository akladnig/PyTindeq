from bokeh.models import Div, Spinner, TextInput, Select, TextAreaInput, Tooltip, HelpButton
from bokeh.layouts import Column, Row

from src.templates.styles import Styles

class UserLayout:
    def __init__(self):
        title = Div(
            text="User Details",
            styles=Styles.title,
        )
        _grip_types = ["Half Crimp", "4 Finger Open", "3 Finger Drag", "Lock Off"]
        self._name = TextInput(
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
        self._grip_type = Select(
            title="Grip Type",
            value="Half Crimp",
            options=_grip_types,
            styles=Styles.normal,
        )
        _grades_tooltip = Tooltip(content="The grade that you've redpointed at least three climbs", position="right")
        self._grades=Spinner(
            title="Redpoint Grade",
            description="_grades_tooltip",        
            low=1,
            high=39,
            step=1,
            value=24,
            width=80,
            styles=Styles.normal,   
        )
        _grades_help = HelpButton(tooltip=_grades_tooltip)
        self._notes = TextAreaInput(
            title="Notes",
            rows=8,
            cols=40,
            styles=Styles.normal,
        )
        title_row = Row(title)
        column_1 = Column(self._name, self._weight, self._grades, _grades_help, margin=(0, 100, 0, 50))
        column_2 = Column(self._grip_type, self._notes)
        user_row = Row(column_1, column_2)
        self.column = Column(title_row, user_row)

    @property
    def weight(self):
        return self._weight.value
    
    @property
    def name(self):
        return self._name.value

    @property
    def grades(self):
        return self._grades.value
    
    @property
    def grip_type(self):
        return self._grip_type.value
    
    @property
    def notes(self):
        return self._notes.value