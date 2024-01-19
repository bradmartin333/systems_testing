from window_utils import *


def test_function():
    print("HOLA!!!!")


ws = WindowState()
ws.text_fields = [
    TextField("HELLO SMALL", Vector2(20, 10), 20),
    TextField("HELLO LARGE", Vector2(20, 120), 60),
]
ws.button_actions.append(
    ActionButton(TextField("HELLO MEDIUM", Vector2(20, 50), 40), test_function)
)

init_window(ws.wid, ws.hgt, "Systems UI")
set_target_fps(60)
while not window_should_close():
    ws.update()
    ws.text_fields[0].text = f"{ws.button_actions[0].value} clicks!"
    ws.text_fields[-1].text = str(round(get_time(), 2))
    begin_drawing()
    clear_background(WHITE)
    ws.draw_all()
    end_drawing()
close_window()
