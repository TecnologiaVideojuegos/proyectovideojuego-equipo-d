import arcade


class Boss(arcade.Sprite):
    def __init__(self, filename, scale, pos_x, pos_y, number_of_hearts, speed):
        super().__init__(filename, scale)
        self.center_x = pos_x
        self.center_y = pos_y
        self.speed = speed
        self.number_of_hearts = number_of_hearts
        self.derecha = True
        self.izquierda = False

    def movement(self):
        if self.derecha:
            self.center_x += self.speed
            if self.center_x > 600:
                self.izquierda = True
                self.derecha = False
        if self.izquierda:
            self.center_x -= self.speed
            if self.center_x < 40:
                self.izquierda = False
                self.derecha = True