from JOTPK.Classes import Weapon


class Character:
    def __init__(self, heart_number, pos_x, pos_y, speed, hp):  # add weapon

        self.heart_number = heart_number
        self.weapon = Weapon
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed = speed
        self.hp = hp
        self.dead = False

    def attack(self):
        pass

    def get_vida(self):
        """
        Devuelve la vida del personaje
        None -> int
        """
        return self.hp

    def take_dmg(self):
        pass

    def set_vida(self, new_hp):
        """
        Cambia la vida del personaje
        Int -> None
        """
        self.hp = new_hp


