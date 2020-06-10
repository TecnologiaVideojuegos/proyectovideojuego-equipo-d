from Clases.Game import *
from Clases.Menu import *


class Credits(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("CREDITOS", screen_width / 2, 530,
                         arcade.color.WHITE, font_size=60, anchor_x="center", align="center")
        arcade.draw_text("Jefe de Proyecto: Óscar García\n\nProgramadores: Fernando Parra\n\n\n\nDiseño: Diego "
                         "Plaza\n\nSonido: Alejandro Cedillo\n\nTester: Juan Carlos", screen_width / 2, 150,
                         arcade.color.WHITE, font_size=30, anchor_x="center", align="left")
        arcade.draw_text("Jorge Fernández", 330, 330,
                         arcade.color.WHITE, font_size=30)
        arcade.draw_text("Enter - Volver", 500, 50,
                         arcade.color.WHITE, font_size=15)

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            menu_view = Menu()
            self.window.show_view(menu_view)
        if key == arcade.key.R:
            game_view = Game()
            game_view.setup()
            self.window.show_view(game_view)
        if key == arcade.key.ENTER:
            win = Winner()
            self.window.show_view(win)
