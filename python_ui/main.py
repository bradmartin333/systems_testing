from pyray import *


class WindowState:
    wid = 800
    hgt = 450

    last_dpi_scale = Vector2(1, 1)
    dpi_scale = Vector2(1, 1)
    max_dpi_scale = 1

    text_fields = []

    def __init__(self):
        self.update()

    def update(self):
        self.dpi_scale = get_window_scale_dpi()
        if self.last_dpi_scale != self.dpi_scale:
            self.last_dpi_scale = self.dpi_scale
            self.max_dpi_scale = max(self.dpi_scale.x, self.dpi_scale.y)
            set_window_size(
                int(self.wid * self.dpi_scale.x), int(self.hgt * self.dpi_scale.y)
            )

    def draw_all_text(self):
        for t in self.text_fields:
            draw_text(
                t.text,
                int(t.position.x * self.dpi_scale.x),
                int(t.position.y * self.dpi_scale.y),
                int(t.size * self.max_dpi_scale),
                t.tint,
            )


class TextField:
    def __init__(self, text, position, size, tint=BLACK):
        self.text = text
        self.position = position
        self.size = size
        self.tint = tint


ws = WindowState()
ws.text_fields = [
    TextField("HELLO SMALL", Vector2(10, 10), 20),
    TextField("HELLO MEDIUM", Vector2(10, 50), 40),
    TextField("HELLO LARGE", Vector2(10, 100), 60),
]

init_window(ws.wid, ws.hgt, "REM Rest")

while not window_should_close():
    ws.update()
    begin_drawing()
    clear_background(DARKGRAY)
    ws.draw_all_text()
    end_drawing()
close_window()
