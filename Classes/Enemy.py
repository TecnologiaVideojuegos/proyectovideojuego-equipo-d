from JOTPK.Classes import Character
from random import *


class Enemy(Character):
    def __init__(self, heart_number, pos_x, pos_y, speed, hp):
        super().__init__(heart_number, pos_x, pos_y, speed, hp)
        self.drop_list = []  # items, todavía por definir, lista de objetos (clase)

    def drop(self, drop_list):
        """
        Elige un item al azar del drop list y lo retorna
        List -> String
        """
        return drop_list[randint(0, len(drop_list)-1)]  # no tengo en cuenta droprate

