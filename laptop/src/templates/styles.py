from bokeh.models import Styles

class Styles:
    title = Styles(
        font_size="300%",
        font_style="bold",
        color="blue",
        text_align="left",
        width="100%",
        margin_top="20px",
    )

    heading = Styles(
        font_size="200%",
        font_style="bold",
        color="black",
        text_align="left",
        width="100%",
    )

    heading1 = Styles(
        font_size="250%",
        font_style="bold",
        color="blue",
        text_align="left",
        width="100%",
        # margin_right="-20px"
    )

    heading2 = Styles(
        font_size="200%",
        font_style="bold",
        color="black",
        text_align="left",
        width="100%",
    )
    normal = Styles(
        font_size="150%",
        color="black",
        text_align="left",
        width="100%",
    )
    button = Styles(
        align_self="center",
    )
    div_margin = (0,20, 20, 20)
    rfd_div_margin = (-5,20, 0, 20)
    button_margin = (0, 0, 0, 0)
    reps = Styles(
        font_size="300%",
        color="black",
        text_align="center",
        width="100%",
    )

    figure = Styles(
        font_size="150%",
        color="white",
        text_align="left",
        width="100%",
    )

    countdown_timer_idle = Styles(
        font_size="800%",
        color="white",
        background_color="orange",
        text_align="center",
    )
    countdown_timer_countdown = Styles(
        font_size="800%",
        color="white",
        background_color="orange",
        text_align="center",
    )
    countdown_timer_go = Styles(
        font_size="800%",
        color="white",
        background_color="green",
        text_align="center",
    )
    countdown_timer_rest = Styles(
        font_size="800%",
        color="white",
        background_color="red",
        text_align="center",
    )