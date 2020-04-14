from Classes import Item


class Weapon(Item):
    def __init__(self, name, price, dmg, weapon_type):
        super().__init__(price)
        self.dmg = dmg
        self.name = name
        self.powerUps_list = []
        self.weapon_type = weapon_type

    def has_power_up(self, item):
        """
        Checkea si un arma tiene powerUp
        String -> boolean
        """
        pass

    def apply_power_up(self, item):
        """
        Aplica powerUp a arma
        String -> None
        """
        if item in self.powerUps_list:
            pass
