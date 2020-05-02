import arcade

#Introducción

class MyApplication(arcade.Window):

    def __init__(self, width, height):
        super().__init__(width, height, "introduccion")

        self.introduccion = arcade.load_sound("song21.mp3")


def main():
    window = MyApplication(300, 300)
    arcade.run()


#Tema de batalla
    
    class MyApplication(arcade.Window):

    def __init__(self, width, height):
        super().__init__(width, height, "batalla")

        self.batalla = arcade.load_sound("Track_01.ogg")


def main():
    window = MyApplication(300, 300)
    arcade.run()



#Tema de Game Over

class MyApplication(arcade.Window):

    def __init__(self, width, height):
        super().__init__(width, height, "gameover")

        self.gameover = arcade.load_sound("game_over_bad_chest.wav")


def main():
    window = MyApplication(300, 300)
    arcade.run()


#Tema de la tienda

class MyApplication(arcade.Window):

    def __init__(self, width, height):
        super().__init__(width, height, "tienda")

        self.tienda = arcade.load_sound("GreenSalon.ogg")

    def on_key_press(self, key, modifiers):
        
        arcade.play_sound(self.introduccion_sound)


def main():
    window = MyApplication(300, 300)
    arcade.run()


# Tema de la victoria

class MyApplication(arcade.Window):

    def __init__(self, width, height):
        super().__init__(width, height, "victoria")

        self.victoria = arcade.load_sound("Victory!.wav")


def main():
    window = MyApplication(300, 300)
    arcade.run()


#Tema de boss final

class MyApplication(arcade.Window):

    def __init__(self, width, height):
        super().__init__(width, height, "bosssfinal")

        self.bossfinal = arcade.load_sound("track_08.ogg")


def main():
    window = MyApplication(300, 300)
    arcade.run()

main()
