from pyray import *


class WindowState:
    wid = 800
    hgt = 450

    mouse_pos = Vector2(-1, -1)
    left_click_down = False
    left_click_pressed = False

    last_dpi_scale = Vector2(1, 1)
    dpi_scale = Vector2(1, 1)
    max_dpi_scale = 1

    text_fields = []
    button_actions = []

    def __init__(self):
        self.update()

    def update(self):
        self.mouse_pos = get_mouse_position()
        self.left_click_down = is_mouse_button_down(MouseButton.MOUSE_BUTTON_LEFT)
        self.left_click_pressed = is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT)
        self.dpi_scale = get_window_scale_dpi()
        if self.last_dpi_scale != self.dpi_scale:
            self.last_dpi_scale = self.dpi_scale
            self.max_dpi_scale = max(self.dpi_scale.x, self.dpi_scale.y)
            set_window_size(
                int(self.wid * self.dpi_scale.x), int(self.hgt * self.dpi_scale.y)
            )

    def draw_all_text(self):
        for t in self.text_fields:
            t.draw(self)

    def draw_all_buttons(self):
        for b in self.button_actions:
            b.draw(self)

    def draw_all(self):
        self.draw_all_text()
        self.draw_all_buttons()


class TextField:
    def __init__(self, text, position, size=20, tint=BLACK):
        self.text = text
        self.position = position
        self.size = size
        self.tint = tint

    def draw(self, ws: WindowState):
        draw_text(
            self.text,
            int(self.position.x * ws.dpi_scale.x),
            int(self.position.y * ws.dpi_scale.y),
            int(self.size * ws.max_dpi_scale),
            self.tint,
        )


class ActionButton:
    value = 0

    color = BLUE
    border_color = BLACK
    mouse_over_color = DARKBLUE
    mouse_down_color = Color(0, 82, 240, 255)  # Slightly lighter than DARKBLUE

    def __init__(self, text_field: TextField, action):
        self.tf = text_field
        self.action = action

    def draw(self, ws: WindowState):
        p = 10 * ws.max_dpi_scale
        x = self.tf.position.x * ws.dpi_scale.x
        y = self.tf.position.y * ws.dpi_scale.y
        wid = measure_text(self.tf.text, self.tf.size) * ws.dpi_scale.x
        hgt = self.tf.size * ws.dpi_scale.y
        border = Rectangle(x - p, y - p, wid + p * 2, hgt + p * 2)
        active_area = Rectangle(x - p / 2, y - p / 2, wid + p, hgt + p)

        mouse_over = check_collision_point_rec(ws.mouse_pos, active_area)
        current_color = self.mouse_over_color if mouse_over else self.color
        current_color = (
            self.mouse_down_color
            if ws.left_click_down and mouse_over
            else current_color
        )

        draw_rectangle_rec(border, self.border_color)
        draw_rectangle_rec(active_area, current_color)

        self.tf.draw(ws)

        if mouse_over and ws.left_click_pressed:
            self.action()
            self.value += 1
