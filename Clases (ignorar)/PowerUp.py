import arcade


class PowerUp(arcade.Sprite):
    def __init__(self, sprite, pos_x, pos_y, tiempo_vida):
        super().__init__(sprite)
        self.center_x = pos_x
        self.center_y = pos_y
        self.tiempo_vida = tiempo_vida
