import arcade
from random import *

screen_width = 700
screen_height = 700
screen_title = "Journey of the Prairie King"
sprite_scaling = 1


class Character:
    def __init__(self, pos_x, pos_y, number_of_hearts, speed):

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed = speed
        self.number_of_hearts = number_of_hearts
        self.dead = False

    def get_number_of_hearts(self):
        """
        Devuelve el numero de corazones o "vidas" del personaje
        None -> int
        """
        return self.number_of_hearts

    def sub_heart(self, number_of_hearts):  # los hits que aguantan los enemigos son como sus "vidas"
        """
        Quita un corazon del total de corazones
        Int -> None
        """
        self.number_of_hearts -= 1
        if self.number_of_hearts <= 0:
            self.dead = True


class MainCharacter(Character):
    def __init__(self, pos_x, pos_y, number_of_hearts, speed):  # muere de un golpe

        super().__init__(pos_x, pos_y, number_of_hearts, speed)

        self.money = 0
        self.weapon = Weapon  # not sure how to do this
        self.right = False
        self.left = False
        self.up = False
        self.down = False

    def get_money(self):
        """
        Retorna el dinero del personaje
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

    def add_heart(self, number_of_hearts):
        """
        Suma un corazon al total de corazones
        Int -> None
        """
        self.number_of_hearts += 1


class Enemy(Character):
    def __init__(self, pos_x, pos_y, number_of_hearts, speed):

        super().__init__(pos_x, pos_y, number_of_hearts, speed)

        self.drop_list = []  # items, todavía por definir, lista de objetos (clase)

    def drop(self):
        """
        Elige un item al azar del drop list y lo retorna
        None -> String
        """
        return self.drop_list[randint(0, len(self.drop_list) - 1)]  # no tengo en cuenta droprate


class Item:
    def __init__(self, price):
        self.price = price


class Weapon(Item):
    def __init__(self, name, price, dmg, weapon_type):
        super().__init__(price)
        self.dmg = dmg
        self.name = name
        self.powerUp_list = ["Caja de vacunas", "Lejía", "Aguja nueva"]
        self.weapon_type = weapon_type

    def has_power_up(self):
        """
        Checkea si un arma tiene powerUp
        String -> boolean
        """
        pass

    def apply_power_up(self, power_up):
        """
        Aplica powerUp a arma
        String -> None
        """


class Consumable(Item):
    def __init__(self, name):
        super().__init__(name)

    def apply_consumable(self, consumable):
        """
        Aplica objeto consumible
        String -> None
        """
        pass


class Bullet(arcade.Sprite):
    def update(self):
        self.center_y += self.change_y
        self.center_x += self.change_x


class Game(arcade.Window):
    def __init__(self):
        super().__init__(screen_width, screen_height, screen_title)

        # lists
        self.player_list = None
        self.bullet_list = None

        # main character
        self.player = None
        self.bullet_shoot = None

        # character and bullet sprites
        self.player_sprite = None
        self.bullet_sprite = None

        # map sprites
        self.suelo_paredes = None
        self.cosas = None
        self.obstaculos = None


    def setup(self):
        """
        Set up the game and initialize the variables. Call this function to restart the game
        """

        # Load map
        my_map = arcade.tilemap.read_tmx("mapas/archivos tsx/entrada.tmx")

        # Set up the layer of the map
        self.suelo_paredes = arcade.tilemap.process_layer(my_map, "suelo y paredes", 1)
        self.cosas = arcade.tilemap.process_layer(my_map, "cosas", 1)
        self.obstaculos = arcade.tilemap.process_layer(my_map, "obstaculos", 1)

        # Set up the lists
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        # Set up the player
        self.player = MainCharacter(screen_width / 2, screen_height / 2, 3, 200)
        self.player_sprite = arcade.Sprite(
            "mapas/personajes/protagonista.png",
            sprite_scaling, center_x=self.player.pos_x, center_y=self.player.pos_y)

        self.player_list.append(self.player_sprite)

    def on_update(self, delta_time):
        """ Movement and game logic """  # collisions go here

        # main character movement
        if self.player.right:
            self.player_sprite.center_x += self.player.speed * delta_time
        if self.player.left:
            self.player_sprite.center_x -= self.player.speed * delta_time
        if self.player.up:
            self.player_sprite.center_y += self.player.speed * delta_time
        if self.player.down:
            self.player_sprite.center_y -= self.player.speed * delta_time

        # collisions with screen borders (not finished)
        if self.player_sprite.center_x + 27 >= screen_width:
            self.player_sprite.center_x = screen_width - 27
        if self.player_sprite.center_x <= 0:
            self.player_sprite.center_x = 0
        if self.player_sprite.center_y >= screen_height:
            self.player_sprite.center_y = screen_height
        if self.player_sprite.center_y <= 0:
            self.player_sprite.center_y = 0

        # make the bullet shoot
        if self.bullet_shoot:
            self.shoot()

        # update player position
        self.player_list.update()
        self.bullet_list.update()

    def shoot(self):

        # Bullet creation
        bullet = Bullet("bullet.png", 0.5)
        bullet.center_x = self.player_sprite.center_x
        bullet.center_y = self.player_sprite.center_y
        self.bullet_list.append(bullet)
        bullet.speed = 8

        # Direction of the bullet
        if self.player.right:
            bullet.change_x = bullet.speed
            bullet.change_y = 0
            bullet.angle = 0
        if self.player.down:
            bullet.change_x = 0
            bullet.change_y = -bullet.speed
            bullet.angle = 270
        if self.player.left:
            bullet.change_x = -bullet.speed
            bullet.change_y = 0
            bullet.angle = 180
        if self.player.up:
            bullet.change_x = 0
            bullet.change_y = bullet.speed
            bullet.angle = 90
        if self.player.down and self.player.left:
            bullet.change_x = -bullet.speed/2
            bullet.change_y = -bullet.speed/2
            bullet.angle = 225
        if self.player.down and self.player.right:
            bullet.change_x = bullet.speed/2
            bullet.change_y = -bullet.speed/2
            bullet.angle = 315
        if self.player.up and self.player.left:
            bullet.change_x = -bullet.speed/2
            bullet.change_y = bullet.speed/2
            bullet.angle = 135
        if self.player.up and self.player.right:
            bullet.change_x = bullet.speed/2
            bullet.change_y = bullet.speed/2
            bullet.angle = 45
        if not self.player.up and not self.player.down and not self.player.right and not self.player.left:
            bullet.change_x = 0
            bullet.change_y = bullet.speed
            bullet.angle = 90

    def on_draw(self):
        """
        Render the screen
        """
        arcade.start_render()

        # draw background
        # arcade.draw_lrwh_rectangle_textured(0, 0, screen_width, screen_height, self.background_image)

        # draw of the map
        self.suelo_paredes.draw()
        self.cosas.draw()
        self.obstaculos.draw()

        # draw all sprites
        self.player_list.draw()
        self.bullet_list.draw()

    def on_key_press(self, key, modifiers):

        # move character
        if key == arcade.key.W:
            self.player.up = True
        if key == arcade.key.A:
            self.player.left = True
        if key == arcade.key.S:
            self.player.down = True
        if key == arcade.key.D:
            self.player.right = True

        # to shoot
        if key == arcade.key.SPACE:
            self.shoot()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.player.up = False
        if key == arcade.key.A:
            self.player.left = False
        if key == arcade.key.S:
            self.player.down = False
        if key == arcade.key.D:
            self.player.right = False


def main():
    game = Game()
    game.setup()
    arcade.run()


main()