import arcade
from random import *

screen_width = 640
screen_height = 640
screen_title = "Journey of the Prairie King"
sprite_scaling = 1


class Character(arcade.Sprite):
    def __init__(self, filename, scale, number_of_hearts, speed):

        super().__init__(filename, scale)

        self.speed = speed
        self.number_of_hearts = number_of_hearts
        self.dead = False

    def get_number_of_hearts(self):
        """
        Devuelve el numero de corazones o "vidas" del personaje
        None -> int
        """
        return self.number_of_hearts

    def sub_heart(self):  # los hits que aguantan los enemigos son como sus "vidas"
        """
        Quita un corazon del total de corazones
        Int -> None
        """
        self.number_of_hearts -= 1
        if self.number_of_hearts <= 0:
            self.dead = True



class MainCharacter(Character):
    def __init__(self, filename, scale, number_of_hearts, speed):  # muere de un golpe

        super().__init__(filename, scale, number_of_hearts, speed)

        self.center_x = screen_width / 2
        self.center_y = screen_height / 2
        self.money = 0
        self.weapon = Weapon  # not sure how to do this
        self.go_right = False
        self.go_left = False
        self.go_up = False
        self.go_down = False
        self.shooting_right = None
        self.shooting_left = None
        self.shooting_up = None
        self.shooting_down = None

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

    def add_heart(self):
        """
        Suma un corazon al total de corazones
        Int -> None
        """
        self.number_of_hearts += 1


class Enemy(Character):
    def __init__(self, filename, scale, pos_x, pos_y, number_of_hearts, speed):

        super().__init__(filename, scale, number_of_hearts, speed)
        self.center_x = pos_x
        self.center_y = pos_y
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

    def __init__(self, filename, sprite_scale):

        super().__init__(filename, sprite_scale)
        self.speed = 5

    def update(self):

        self.center_x += self.change_x
        self.center_y += self.change_y


class Game(arcade.Window):
    def __init__(self):
        super().__init__(screen_width, screen_height, screen_title)

            def __init__(self):
        super().__init__(screen_width, screen_height, screen_title)

        # lists
        self.player_list = None
        self.bullet_list = None
        self.enemy_list = None

        # main character and bullet sprites
        self.player_sprite = None
        self.bullet_sprite = None

        # max number of enemies
        self.max_enemies = None

        # background
        self.background_image = None

        self.cd = None
        self.score = None

        # map sprites
        self.suelo_paredes = None
        self.cosas = None
        self.obstaculos = None
        self.obstaculos_2 = None
        self.perfeccionar = None
        self.cuerpos = None
        self.sangre = None

        # number of the room the player is
        self.current_room = 0

    def setup(self):
        """
        Set up the game and initialize the variables. Call this function to restart the game
        """
        # Set up the lists
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        # The entrances is the first room
        self.entrance()

        # Enemies
        # Enemy 1
        self.enemy = Enemy(randint(50, 750), 200, 3, 200)
        self.enemy_sprite = arcade.Sprite("mapas/personajes/enemigo 1.png", 1, center_x=self.enemy.pos_x,
                                            center_y=self.enemy.pos_y)
        self.enemy_list.append(self.enemy_sprite)

        # Enemy 2
        self.enemy = Enemy(randint(50, 750), 350, 3, 200)
        self.enemy_sprite = arcade.Sprite("mapas/personajes/enemigo 2.png", 1, center_x=self.enemy.pos_x,
                                            center_y=self.enemy.pos_y)
        self.enemy_list.append(self.enemy_sprite)

        # Enemy 3
        self.enemy = Enemy(randint(50, 750), 500, 3, 200)
        self.enemy_sprite = arcade.Sprite("mapas/personajes/enemigo 3.png", 1, center_x=self.enemy.pos_x,
                                            center_y=self.enemy.pos_y)
        self.enemy_list.append(self.enemy_sprite)

        # Set up the player
        self.player_sprite = MainCharacter("protagonista.png", sprite_scaling,
            3, 200)
        self.player_list.append(self.player_sprite)
        
        self.max_enemies = 10
        self.cd = 0
        self.score = 0

# Rooms created
    def entrance(self):
        my_map = arcade.tilemap.read_tmx("mapas/archivos tsx/entrada.tmx")

        self.suelo_paredes = arcade.tilemap.process_layer(my_map, "suelo y paredes", 1)
        self.cosas = arcade.tilemap.process_layer(my_map, "cosas", 1)
        self.obstaculos = arcade.tilemap.process_layer(my_map, "obstaculos", 1)

    def room_1(self):

        my_map = arcade.tilemap.read_tmx("mapas/archivos tsx/planta 1.tmx")

        self.suelo_paredes = arcade.tilemap.process_layer(my_map, "suelo y paredes", 1)
        self.obstaculos_2 = arcade.tilemap.process_layer(my_map, "obstaculos 2", 1)
        self.obstaculos = arcade.tilemap.process_layer(my_map, "obstaculos", 1)
        self.perfeccionar = arcade.tilemap.process_layer(my_map, "perfeccionar", 1)

    def room_2(self):
        my_map = arcade.tilemap.read_tmx("mapas/archivos tsx/planta 2.tmx")

        self.suelo_paredes = arcade.tilemap.process_layer(my_map, "suelos y paredes", 1)
        self.obstaculos_2 = arcade.tilemap.process_layer(my_map, "obstaculos2", 1)
        self.obstaculos = arcade.tilemap.process_layer(my_map, "obstaculos", 1)
        self.perfeccionar = arcade.tilemap.process_layer(my_map, "perfeccionar", 1)
        self.cuerpos = arcade.tilemap.process_layer(my_map, "cuerpos", 1)
        self.sangre = arcade.tilemap.process_layer(my_map, "sangre", 1)

    def room_3(self):
        my_map = arcade.tilemap.read_tmx("mapas/archivos tsx/planta 3.tmx")

        self.suelo_paredes = arcade.tilemap.process_layer(my_map, "suelo y paredes", 1)
        self.sangre = arcade.tilemap.process_layer(my_map, "sangre", 1)
        self.obstaculos = arcade.tilemap.process_layer(my_map, "obstaculos", 1)
        self.cuerpos = arcade.tilemap.process_layer(my_map, "cuerpos", 1)

    def on_update(self, delta_time):
        """ Movement and game logic """  # collisions go here

        # Update of the room where the player is
        # Going up stairs

        if self.player_sprite.center_y > 630 and 326 < self.player_sprite.center_x < 376 and self.current_room == 0:
            self.current_room = 1
            self.room_1()
            self.player_sprite.center_y = 630
            self.player_sprite.center_x = 416

        if self.player_sprite.center_y > 635 and 298 < self.player_sprite.center_x < 343 and self.current_room == 1:
            self.current_room = 2
            self.room_2()
            self.player_sprite.center_y = 20
            self.player_sprite.center_x = 288

        if self.player_sprite.center_y > 635 and 256 < self.player_sprite.center_x < 320 and self.current_room == 2:
            self.current_room = 3
            self.room_3()
            self.player_sprite.center_y = 20
            self.player_sprite.center_x = 256

        # Going down stairs
        if self.player_sprite.center_y < 10 and 224 < self.player_sprite.center_x < 288 and self.current_room == 3:
            self.current_room = 2
            self.room_2()
            self.player_sprite.center_y = 630
            self.player_sprite.center_x = 288

        if self.player_sprite.center_y < 10 and 256 < self.player_sprite.center_x < 320 and self.current_room == 2:
            self.current_room = 1
            self.room_1()
            self.player_sprite.center_y = 630
            self.player_sprite.center_x = 320

        if self.player_sprite.center_y > 635 and 389 < self.player_sprite.center_x < 438 and self.current_room == 1:
            self.current_room = 0
            self.entrance()
            self.player_sprite.center_y = 625
            self.player_sprite.center_x = 352

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
        if self.player_sprite.center_x + 20 >= screen_width:
            self.player_sprite.center_x = screen_width - 20
        if self.player_sprite.center_x - 20 <= 0:
            self.player_sprite.center_x = 20
        if self.player_sprite.center_y + 32 >= screen_height:
            self.player_sprite.center_y = screen_height - 32
        if self.player_sprite.center_y - 30 <= 0:
            self.player_sprite.center_y = 30

        # make the bullet shoot
        if self.bullet_shoot:
            self.shoot()

        # List to make the enemy goes to the coordenates of the player
        for self.enemy_sprite in self.enemy_list:
            self.movimiento(self.enemy_sprite, self.player_sprite)

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

    def movimiento(self, enemy, player):

        # Movement
        if enemy.center_x < player.center_x:
            enemy.center_x += 2
        if enemy.center_x > player.center_x:
            enemy.center_x -= 2
        if enemy.center_y < player.center_y:
            enemy.center_y += 2
        if enemy.center_y > player.center_y:
            enemy.center_y -= 2

    def on_draw(self):
        """
        Render the screen
        """
        arcade.start_render()

        # draw background
        # arcade.draw_lrwh_rectangle_textured(0, 0, screen_width, screen_height, self.background_image)

        # draw of the map
        # Room entrance
        if self.current_room == 0 :
            self.suelo_paredes.draw()
            self.cosas.draw()
            self.obstaculos.draw()

        # Room 1
        if self.current_room == 1:
            self.suelo_paredes.draw()
            self.obstaculos.draw()
            self.obstaculos_2.draw()
            self.perfeccionar.draw()

        # Room 2
        if self.current_room == 2:
            self.suelo_paredes.draw()
            self.obstaculos.draw()
            self.obstaculos_2.draw()
            self.perfeccionar.draw()
            self.sangre.draw()
            self.cuerpos.draw()

        # Room 3
        if self.current_room == 3:
            self.suelo_paredes.draw()
            self.obstaculos.draw()
            self.sangre.draw()
            self.cuerpos.draw()

        # draw all sprites
        self.player_list.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()

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
