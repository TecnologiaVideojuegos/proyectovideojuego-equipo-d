import arcade

from Clases.Parametros import *


class Item(arcade.Sprite):

    def __init__(self, filename, pos_x, pos_y, precio):
        super().__init__(filename, scale=sprite_scaling)

        self.center_x = pos_x
        self.center_y = pos_y
        self.precio = precio
        self.recogido = False
        self.num_colisiones = 0
