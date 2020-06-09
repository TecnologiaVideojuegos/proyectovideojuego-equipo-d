import arcade

from Clases.Parametros import *


class Weapon(arcade.Sprite):
    def __init__(self, weapon, pos_x, pos_y, angle):
        super().__init__(weapon)
        self.sprite_scale = sprite_scaling / 1.5
        self.center_x = pos_x
        self.center_y = pos_y
        self.angle = angle

    def update_self(self, player_sprite, delta_time):
        if player_sprite.shooting_right or (player_sprite.change_x == 0 and player_sprite.change_y == 0):
            self.center_x = player_sprite.center_x + 15
            self.center_y = player_sprite.center_y - 5
            self.angle = 90

        if player_sprite.shooting_left:
            self.center_x = player_sprite.center_x - 13
            self.center_y = player_sprite.center_y - 4
            self.angle = 270

        if player_sprite.shooting_down:
            self.center_x = player_sprite.center_x + 5
            self.center_y = player_sprite.center_y - 12
            self.angle = 0

        if player_sprite.shooting_up:
            self.center_x = player_sprite.center_x + 8
            self.center_y = player_sprite.center_y + 5
            self.angle = 180

        if player_sprite.shooting_down and player_sprite.shooting_left:
            self.center_x = player_sprite.center_x - 15
            self.center_y = player_sprite.center_y - 8
            self.angle = 315

        if player_sprite.shooting_down and player_sprite.shooting_right:
            self.center_x = player_sprite.center_x + 12
            self.center_y = player_sprite.center_y - 10
            self.angle = 45

        if player_sprite.shooting_up and player_sprite.shooting_left:
            self.center_x = player_sprite.center_x - 13
            self.center_y = player_sprite.center_y + 4
            self.angle = 225

        if player_sprite.shooting_up and player_sprite.shooting_right:
            self.center_x = player_sprite.center_x + 15
            self.center_y = player_sprite.center_y + 3
            self.angle = 135

        if player_sprite.go_right:
            self.center_x += player_sprite.speed * delta_time
        if player_sprite.go_left:
            self.center_x -= player_sprite.speed * delta_time
        if player_sprite.go_up:
            self.center_y += player_sprite.speed * delta_time
        if player_sprite.go_down:
            self.center_y -= player_sprite.speed * delta_time
