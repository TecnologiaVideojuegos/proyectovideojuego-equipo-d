from Clases.Menu import *
import arcade


def main():
    window = arcade.Window(screen_width, screen_height, screen_title)
    menu = Menu()
    window.show_view(menu)
    arcade.run()


if __name__ == "__main__":
    main()
