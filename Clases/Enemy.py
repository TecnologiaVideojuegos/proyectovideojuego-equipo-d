from Clases.Character import *


class Enemy(Character):
    def __init__(self, filename, scale, pos_x, pos_y, number_of_hearts, speed):
        super().__init__(filename, scale, number_of_hearts, speed)
        self.center_x = pos_x
        self.center_y = pos_y

    def movement(self, player):

        if self.center_x < player.center_x:
            self.center_x += self.speed
        if self.center_x > player.center_x:
            self.center_x -= self.speed
        if self.center_y < player.center_y:
            self.center_y += self.speed
        if self.center_y > player.center_y:
            self.center_y -= self.speed
