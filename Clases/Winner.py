from Clases.Credits import *
from Clases.Game import *


class Winner(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("WINNER", screen_width // 2, 500,
                         arcade.color.WHITE, 70, anchor_x="center")
        arcade.draw_text("Esc - Menu\n\nR - Volver a jugar\n\nEnter - Créditos", screen_width // 2, screen_height // 3,
                         arcade.color.WHITE, font_size=30, anchor_x="center", align="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            menu_view = Menu()
            self.window.show_view(menu_view)
        if key == arcade.key.R:
            game_view = Game()
            game_view.setup()
            self.window.show_view(game_view)
        if key == arcade.key.ENTER:
            credit = Credits()
            self.window.show_view(credit)
