from JOTPK.Classes import Character
from JOTPK.Classes import Weapon

class MainCharacter(Character):
    def __init__(self, heart_number, pos_x, pos_y, speed, hp, money):
        super().__init__(heart_number, pos_x, pos_y, speed, hp)
        self.money = money

    def get_money(self):
        """
        Retorna el dinero que tiene el personaje
        """
        return self.money

    def get_heart_number(self):
        """
        Retorna el numero de vidas que tiene el personaje
        """
        return self.heart_number

    def get_speed(self):
        """
        Retorna la velocidad del personaje
        """
        return self.speed

    def set_heart_number(self, new_heart_number):
        """
        Cambia el numero de vidas del personaje
        """
        self.heart_number = new_heart_number

    def set_speed(self, new_speed):
        """
        Cambia la velocidad del personaje
        """
        self.speed = new_speed






