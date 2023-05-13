from bokeh.models import Div
from bokeh.layouts import Column

from src.test import TestResults


class AnalysisLayout:
    def __init__(self):
        title = Div(
            text="Testing Analysis",
            styles={
                "font-size": "300%",
                "font_style": "bold",
                "color": "Blue",
                "text-align": "left",
                "width": "100%",
            },
        )

        self.grades = {
            1: "3",
            2: "6",
            3: "8",
            4: "9",
            5: "10",
            6: "12",
            7: "13",
            8: "14",
            9: "16",
            10: "17",
            11: "18",
            12: "19",
            13: "20",
            14: "21",
            15: "22",
            16: "23",
            17: "24",
            18: "24",
            19: "25",
            20: "26",
            21: "27",
            22: "28",
            23: "29",
            24: "30",
            25: "31",
            26: "32",
            27: "33",
            28: "34",
            29: "35",
            30: "36",
        }

        french_grades = {
            1: "1",
            2: "2",
            3: "2+",
            4: "3-",
            5: "3",
            6: "3+",
            7: "4",
            8: "4+",
            9: "5",
            10: "5+",
            11: "6a",
            12: "6a+",
            13: "6b",
            14: "6b+",
            15: "6c",
            16: "6c+",
            17: "7a",
            18: "7a+",
            19: "7b",
            20: "7b+",
            21: "7c",
            22: "7c+",
            23: "8a",
            24: "8a+",
            25: "8b",
            26: "8b+",
            27: "8c",
            28: "8c+",
            29: "9a",
            30: "9a+",
        }

        prediction_intro_text = (
            "<strong>Predicted redpoint grades:</strong><br><ul>"
        )
        prediction_intro_text += "<li>If one predictor is far below the others, you might improve by focusing training here</li>"
        prediction_intro_text += "<li>If predictions are far below your real redpoint level, you might improve by focusing on technique and mental traning</li></ul>"

        prediction_results = "<ul><li>Max strength: 0 - 0</li>"
        prediction_results += "<li>Endurance: 0 - 0</li>"
        prediction_results += "<li>Contact strength: 0 - 0</li></ul>"

        # self.cf_percent=(critical_load/self.cf_peak_load)*100

        prediction_intro = Div(
            text=prediction_intro_text,
            sizing_mode="stretch_width",
            styles={
                "font-size": "150%",
                "color": "black",
                "text-align": "left",
                "width": "100%",
            },
        )
        self._prediction_results = Div(
            text=prediction_results,
            sizing_mode="stretch_width",
            styles={
                "font-size": "150%",
                "color": "black",
                "text-align": "left",
                "width": "100%",
            },
        )
        results_title = Div(
            text="<strong>Results:</strong>",
            sizing_mode="stretch_width",
            styles={
                "font-size": "150%",
                "color": "black",
                "text-align": "left",
                "width": "100%",
            },
        )

        results_text = "<ul>\
        <li>Max strength left: 0.00% BW</li>\
        <li>Max strength right: 0.00% BW</li>\
        <li>Peak force: 0.00% BW</li>\
        <li>Critical force: 0.00% BW</li>\
        <li>Critical force: 0.00 of peak force</li>\
        <li>RFD left: 0.00% kg/s</li>\
        <li>RFD right: 0.00% kg/s</li></ul>"

        self._results = Div(
            text=results_text,
            sizing_mode="stretch_width",
            styles={
                "font-size": "150%",
                "color": "black",
                "text-align": "left",
                "width": "100%",
            },
        )
        self.column = Column(
            title,
            results_title,
            self._results,
            prediction_intro,
            self._prediction_results,
        )

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, results):
        self._results.text = "<ul>\
        <li>Body Weight: {:d}kg</li>\
        <li>Max strength left: {:.2f}% BW</li>\
        <li>Max strength right: {:.2f}% BW</li>\
        <li>Peak force: {:.2f}% BW</li>\
        <li>Critical force: {:.2f}% BW</li>\
        <li>Critical force: {:.2f}% of peak force</li>\
        <li>RFD left: {:.2f}% kg/s</li>\
        <li>RFD right: {:.2f}% kg/s</li></ul>\
        ".format(
            TestResults.body_weight,
            (TestResults.max_left / TestResults.body_weight) * 100,
            (TestResults.max_right / TestResults.body_weight) * 100,
            (TestResults.peak_load / TestResults.body_weight) * 100,
            (TestResults.critical_load / TestResults.body_weight) * 100,
            TestResults.critical_load_percent,
            TestResults.rfd_left,
            TestResults.rfd_right,
        )

    @property
    def prediction_results(self):
        return self._prediction_results

    @prediction_results.setter
    def prediction_results(self, results):
        (
            strength_min,
            strength_max,
            endurance_min,
            endurance_max,
            contact_strength_min,
            contact_strength_max,
        ) = results
        self._prediction_results.text = "<ul><li>Max strength: {} - {}</li>\
        <li>Endurance: {} - {}</li>\
        <li>Contact strength: {} - {}</li></ul>".format(
            self.grades[strength_min],
            self.grades[strength_max],
            self.grades[endurance_min],
            self.grades[endurance_max],
            self.grades[contact_strength_min],
            self.grades[contact_strength_max],
        )
