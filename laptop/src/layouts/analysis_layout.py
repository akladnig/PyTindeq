from bokeh.models import Div
from bokeh.layouts import Column

from src.test import TestResults
from src.templates.styles import Styles


class AnalysisLayout:
    def __init__(self):
        title = Div(
            text="Testing Analysis",
            styles=Styles.title,
        )
        """
        Grading is based on the IRCRA scale
        """
        self.grades = {
            1: "4",
            2: "6",
            3: "7",
            4: "9",
            5: "10",
            6: "12",
            7: "13",
            8: "15",
            9: "16",
            10: "18",
            11: "19-",
            12: "19+",
            13: "20",
            14: "21",
            15: "22-",
            16: "22+",
            17: "23",
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

        self.boulder_grades = {
            1: "VB",
            2: "VB",
            3: "VB",
            4: "VB",
            5: "VB",
            6: "VB",
            7: "VB",
            8: "VB",
            9: "VB",
            10: "VB",
            11: "V0-",
            12: "V0",
            13: "V0+",
            14: "V1",
            15: "V2-",
            16: "V2+",
            17: "V3",
            18: "V4",
            19: "V5",
            20: "V6",
            21: "V7-",
            22: "V8-",
            23: "V8",
            24: "V9",
            25: "V10",
            26: "V11",
            27: "V12",
            28: "V13-",
            29: "V13+",
            30: "V14-",
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

        prediction_title_text = "Predicted redpoint grades:"
        prediction_title = Div(
            text=prediction_title_text,
            sizing_mode="stretch_width",
            styles=Styles.heading,
        )
        prediction_intro_text = "<ul><li>If one predictor is far below the others, you might improve by focusing training here</li>"
        prediction_intro_text += "<li>If predictions are far below your real redpoint level, you might improve by focusing on technique and mental training</li></ul>"

        prediction_results = "<ul><li>Max strength: 0 to 0</li>"
        prediction_results += "<li>Endurance: 0 to 0</li>"
        prediction_results += "<li>Contact strength: 0 to 0</li></ul>"

        # self.cf_percent=(critical_load/self.cf_peak_load)*100

        prediction_intro = Div(
            text=prediction_intro_text,
            sizing_mode="stretch_width",
            styles=Styles.normal,
        )
        self._prediction_results = Div(
            text=prediction_results,
            sizing_mode="stretch_width",
            styles=Styles.normal,
        )
        results_title = Div(
            text="Results:",
            sizing_mode="stretch_width",
            styles=Styles.heading,
        )

        results_text = "<ul>\
        <li>Max strength left: 0.0% BW</li>\
        <li>Max strength right: 0.0% BW</li>\
        <li>Peak force: 0.0% BW</li>\
        <li>Critical force: 0.0% BW</li>\
        <li>Critical force: 0.0 of peak force</li>\
        <li>RFD left: 0.0% kg/s</li>\
        <li>RFD right: 0.0% kg/s</li></ul>"

        self._results = Div(
            text=results_text,
            sizing_mode="stretch_width",
            styles=Styles.normal,
        )
        self.column = Column(
            title,
            results_title,
            self._results,
            prediction_title,
            prediction_intro,
            self._prediction_results,
            margin=Styles.div_margin,
        )

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, results):
        self._results.text = "<ul>\
        <li>Body Weight: {:d}kg</li>\
        <li>Max strength left: {:.1f}% BW</li>\
        <li>Max strength right: {:.1f}% BW</li>\
        <li>Peak force: {:.1f}% BW</li>\
        <li>Critical force: {:.1f}% BW</li>\
        <li>Critical force: {:.1f}% of peak force</li>\
        <li>RFD left: {:.1f}% kg/s</li>\
        <li>RFD right: {:.1f}% kg/s</li></ul>\
        ".format(
            TestResults.body_weight,
            (TestResults.max_left / TestResults.body_weight) * 100,
            (TestResults.max_right / TestResults.body_weight) * 100,
            (TestResults.peak_load / TestResults.body_weight) * 100,
            (TestResults.critical_load / TestResults.body_weight) * 100,
            TestResults.critical_load / TestResults.peak_load,
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
        self._prediction_results.text = "<ul><li>Max strength: {} to {}</li>\
        <li>Endurance: {} to {}</li>\
        <li>Contact strength: {} to {}</li></ul>".format(
            self.grades[strength_min],
            self.grades[strength_max],
            self.grades[endurance_min],
            self.grades[endurance_max],
            self.grades[contact_strength_min],
            self.grades[contact_strength_max],
        )
