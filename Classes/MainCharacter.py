from Classes import Character
from Classes import Weapon

class MainCharacter(Character):
    def __init__(self, pos_x, pos_y, speed, hp, money):
        super().__init__(pos_x, pos_y, speed, hp)
        self.money = money
        self.weapon = Weapon

    def get_money(self):
        """
        Retorna el dinero que tiene el personaje
        """
        return self.money

    def get_speed(self):
        """
        Retorna la velocidad del personaje
        """
        return self.speed

    def set_speed(self, new_speed):
        """
        Cambia la velocidad del personaje
        """
        self.speed = new_speed






