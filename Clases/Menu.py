from Clases.Game import *
from Clases.Parametros import *


class Menu(arcade.View):

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("VIR-ED", screen_width // 2, screen_height // 2,
                         arcade.color.WHITE, font_size=30, anchor_x="center")
        arcade.draw_text("Click para empezar", screen_width // 2, screen_height // 3,
                         arcade.color.WHITE, font_size=30, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = Game()
        game_view.setup()
        self.window.show_view(game_view)