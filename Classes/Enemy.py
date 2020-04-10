from JOTPK.Classes import Character
from random import *


class Enemy(Character):
    def __init__(self, pos_x, pos_y, speed, hp):
        super().__init__(pos_x, pos_y, speed, hp)
        self.drop_list = []  # items, todavía por definir, lista de objetos (clase)

    def drop(self):
        """
        Elige un item al azar del drop list y lo retorna
        None -> String
        """
        return self.drop_list[randint(0, len(self.drop_list)-1)]  # no tengo en cuenta droprate

