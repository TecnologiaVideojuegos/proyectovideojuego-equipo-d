import arcade


class Bullet(arcade.Sprite):

    def __init__(self, filename, sprite_scale):
        super().__init__(filename, sprite_scale)
        self.speed = 6

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

    def update_boss(self):
        self.center_y -= self.change_y
