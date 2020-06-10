import arcade


class Moneda(arcade.Sprite):
    def __init__(self, sprite_moneda, valor, pos_x, pos_y, tiempo_vida):
        super().__init__(sprite_moneda)
        self.center_x = pos_x
        self.center_y = pos_y
        self.valor = valor
        self.tiempo_vida = tiempo_vida
