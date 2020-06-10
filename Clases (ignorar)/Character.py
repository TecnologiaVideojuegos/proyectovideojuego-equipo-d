import arcade


class Character(arcade.Sprite):
    def __init__(self, filename, scale, number_of_hearts, speed):
        super().__init__(filename, scale)

        self.speed = speed
        self.number_of_hearts = number_of_hearts
        self.dead = False
