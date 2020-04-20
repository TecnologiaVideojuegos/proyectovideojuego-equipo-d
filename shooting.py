
class Bullet(arcade.Sprite):

    def __init__(self, filename, sprite_scale):
        super().__init__(filename, sprite_scale)

        self.speed = 5

    def update(self):

        self.center_x += self.change_x
        self.center_y += self.change_y



# this in __init__, player
self.shooting_right = None
self.shooting_left = None
self.shooting_up = None
self.shooting_down = None

# this in __init__
self.cd = None

# this in setup
self.cd = 0

# this in on_update
self.cd += 1

if self.cd % 60 == 0:
    if self.shooting_right:
       self.shoot("right")
    if self.shooting_left:
       self.shoot("left")
    if self.shooting_up:
       self.shoot("up")
    if self.shooting_down:
       self.shoot("down")

def shoot(self, dir1):

    # create bullet sprite
    bullet = Bullet("C:/Users/Usuario/Desktop/Pitón/Sprites/bullet.png", sprite_scaling/10)
    bullet.center_x = self.player_sprite.center_x
    bullet.center_y = self.player_sprite.center_y
    self.bullet_list.append(bullet)

    if dir1 == "right":
        bullet.change_x = bullet.speed
    if dir1 == "left":
        bullet.change_x = -bullet.speed
    if dir1 == "up":
        bullet.change_y = bullet.speed
    if dir1 == "down":
        bullet.change_y = -bullet.speed

# shooting
# this on key pressed
        if key == arcade.key.RIGHT:
            self.shoot("right")
            self.shooting_right = True
            self.cd = 0
        if key == arcade.key.LEFT:
            self.shoot("left")
            self.shooting_left = True
            self.cd = 0
        if key == arcade.key.UP:
            self.shoot("up")
            self.shooting_up = True
            self.cd = 0
        if key == arcade.key.DOWN:
            self.shoot("down")
            self.shooting_down = True
            self.cd = 0


# this on key released
        if key == arcade.key.RIGHT:
            self.shooting_right = False
        if key == arcade.key.LEFT:
            self.shooting_left = False
        if key == arcade.key.UP:
            self.shooting_up = False
        if key == arcade.key.DOWN:
            self.shooting_down = False



