from pyray import *


def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


class WindowState:
    def __init__(self):
        self.wid = 800
        self.hgt = 450
        self.mouse_pos = Vector2(-1, -1)
        self.left_click_down = False
        self.left_click_pressed = False
        self.last_dpi_scale = Vector2(1, 1)
        self.dpi_scale = Vector2(1, 1)
        self.max_dpi_scale = 1
        self.text_fields = []
        self.action_buttons = []
        self.line_plots = []
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
        for x in self.text_fields:
            x.draw(self)

    def draw_all_buttons(self):
        for x in self.action_buttons:
            x.draw(self)

    def draw_all_line_plots(self):
        for x in self.line_plots:
            x.draw(self)

    def draw_all(self):
        self.draw_all_text()
        self.draw_all_buttons()
        self.draw_all_line_plots()


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
    def __init__(self, text_field: TextField, action):
        self.tf = text_field
        self.action = action
        self.num_clicks = 0
        self.color = BLUE
        self.border_color = BLACK
        self.mouse_over_color = DARKBLUE
        self.mouse_down_color = Color(0, 82, 240, 255)  # Slightly lighter than DARKBLUE

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
            self.num_clicks += 1


class LinePlot:
    def __init__(
        self,
        title,
        units,
        rect,
        back_color=LIGHTGRAY,
        fore_color=BLACK,
        text_color=BLACK,
    ):
        self.title = title
        self.units = units
        self.rect = rect
        self.back_color = back_color
        self.fore_color = fore_color
        self.text_color = text_color
        self.data = []
        self.scaled_rect = None

    def send_value(self, val: float):
        num_points = len(self.data)
        if (
            num_points > 0
            and self.scaled_rect != None
            and num_points > self.scaled_rect.width
        ):
            self.data.pop(0)
        self.data.append(val)

    def send_list(self, vals: list[float]):
        for v in vals:
            self.send_value(v)

    def draw(self, ws: WindowState):
        text_size = int(20 * ws.max_dpi_scale)
        self.scaled_rect = Rectangle(
            self.rect.x,
            self.rect.y,
            self.rect.width * ws.dpi_scale.x,
            self.rect.height * ws.dpi_scale.y,
        )

        draw_rectangle_rec(self.scaled_rect, self.back_color)

        num_points = len(self.data)
        if num_points != 0:
            max_y = max(self.data) + 1
            min_y = min(self.data) - 1

            vectors = []
            for i in range(num_points):
                scaled_data = self.data[i]
                if max_y != min_y:
                    scaled_data = map_value(
                        self.data[i],
                        min_y,
                        max_y,
                        self.scaled_rect.y,
                        self.scaled_rect.y + self.scaled_rect.height,
                    )
                vectors.append(Vector2(self.scaled_rect.x + i, scaled_data))

            draw_line_strip(vectors, num_points, self.fore_color)

            text_x = int(self.scaled_rect.x)

            text_title_y = int(self.scaled_rect.y)
            text_title_wid = measure_text(self.title, text_size)
            draw_rectangle(
                text_x,
                text_title_y,
                text_title_wid,
                text_size,
                color_alpha(self.back_color, 0.8),
            )
            draw_text(self.title, text_x, text_title_y, text_size, self.text_color)

            str_max_y = f"{round(max_y, 3)} {self.units}"
            text_max_y = int(self.scaled_rect.y + (10 + text_size) * ws.max_dpi_scale)
            text_max_wid = measure_text(str_max_y, text_size)
            draw_rectangle(
                text_x,
                text_max_y,
                text_max_wid,
                text_size,
                color_alpha(self.back_color, 0.8),
            )
            draw_text(str_max_y, text_x, text_max_y, text_size, self.text_color)

            str_min_y = f"{round(min_y, 3)} {self.units}"
            text_min_y = int(
                (self.scaled_rect.y + self.scaled_rect.height)
                - text_size * ws.max_dpi_scale
            )
            text_min_wid = measure_text(str_min_y, text_size)
            draw_rectangle(
                text_x,
                text_min_y,
                text_min_wid,
                text_size,
                color_alpha(self.back_color, 0.8),
            )
            draw_text(str_min_y, text_x, text_min_y, text_size, self.text_color)
