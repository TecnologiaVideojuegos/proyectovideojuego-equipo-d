import arcade

#Daño cuerpo a cuerpo

class MyApplication(arcade.Window):

    def __init__(self, width, height):
        super().__init__(width, height, "dañocuerpoacurpo")

        self.dañocuerpoacurpo = arcade.load_sound("Socapex - Swordsmall_1.wav")


def main():
    window = MyApplication(300, 300)
    arcade.run()


#Daño letal

class MyApplication(arcade.Window):

    def __init__(self, width, height):
        super().__init__(width, height, "dañoletal")

        self.dañoletal = arcade.load_sound("Socapex - small knock.wav")


def main():
    window = MyApplication(300, 300)
    arcade.run()


#Daño recibido

class MyApplication(arcade.Window):

    def __init__(self, width, height):
        super().__init__(width, height, "dañorecibido")

        self.dañorecibido = arcade.load_sound("Socapex - hurt.wav")


def main():
    window = MyApplication(300, 300)
    arcade.run()


#Disparos

class MyApplication(arcade.Window):

    def __init__(self, width, height):
        super().__init__(width, height, "disparos")

        self.disparos = arcade.load_sound("Socapex - Swordsmall_1.wav")


def main():
    window = MyApplication(300, 300)
    arcade.run()


#Pasos

class MyApplication(arcade.Window):

    def __init__(self, width, height):
        super().__init__(width, height, "pasos")

        self.pasos = arcade.load_sound("sfx_step_grass_l.flac")


def main():
    window = MyApplication(300, 300)
    arcade.run()


#Escudo quitado

class MyApplication(arcade.Window):

    def __init__(self, width, height):
        super().__init__(width, height, "escudoquitado")

        self.escudoquitado = arcade.load_sound("Socapex - blub_hurt2.wav")


def main():
    window = MyApplication(300, 300)
    arcade.run()


