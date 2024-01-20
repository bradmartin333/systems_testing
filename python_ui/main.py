import random as rand
from window_utils import *

ws = WindowState()

val = 0


def test_function():
    global val
    val = rand.random()


ws.text_fields = [
    TextField("HELLO SMALL", Vector2(20, 10), 20),
    TextField("HELLO LARGE", Vector2(20, 120), 60),
]
ws.action_buttons.append(
    ActionButton(TextField("HELLO MEDIUM", Vector2(20, 50), 40), test_function)
)
ws.line_plots.append(
    LinePlot("Test", "mV", Rectangle(10, 200, ws.wid - 20, 100), BLUE, WHITE)
)
ws.line_plots.append(
    LinePlot("Test 2", "kJ", Rectangle(10, 300, ws.wid - 20, 100), PURPLE, WHITE)
)

init_window(ws.wid, ws.hgt, "Systems UI")
set_target_fps(60)
while not window_should_close():
    ws.update()

    ws.line_plots[0].send_value(val)
    ws.line_plots[-1].send_value(1 - val)
    ws.text_fields[0].text = f"{ws.action_buttons[0].num_clicks} clicks"
    ws.text_fields[-1].text = str(round(get_time(), 2))

    begin_drawing()
    clear_background(WHITE)
    ws.draw_all()
    end_drawing()
close_window()
