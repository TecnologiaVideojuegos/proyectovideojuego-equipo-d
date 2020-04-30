import arcade
from random import *

screen_width = 640
screen_height = 640
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

        self.drop_list = ["","",""]  # items, todavía por definir, lista de objetos (clase)

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
        self.enemy_list = None

        # main character, bullet and enemy
        self.player = None
        self.bullet_shoot = None
        self.enemy = None

        # character, bullet and enemy sprites
        self.player_sprite = None
        self.bullet_sprite = None
        self.enemy_sprite = None

        # map sprites
        self.paredes = None
        self.suelo = None
        self.cosas = None
        self.obstaculos = None
        self.obstaculos_2 = None
        self.perfeccionar = None
        self.cuerpos = None
        self.sangre = None

        # number of the room the player is
        self.current_room = 0

        # physics between enemies
        self.physics_engine_enemy = None
        self.physics_engine_enemy1 = None
        self.physics_engine_enemy2 = None

        # collision bullet - enemy
        self.collision_bullet_enemy = None

    def setup(self):
        """
        Set up the game and initialize the variables. Call this function to restart the game
        """
        # Set up the lists
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.physics_engine_enemy = arcade.SpriteList()
        self.physics_engine_enemy1 = arcade.SpriteList()
        self.physics_engine_enemy2 = arcade.SpriteList()

        # The entrances is the first room
        self.entrance()

        # Set up the player
        self.player = MainCharacter(screen_width / 2, 305, 3, 360)
        self.player_sprite = arcade.Sprite(
            "mapas/personajes/protagonista.png",
            sprite_scaling, center_x=self.player.pos_x, center_y=self.player.pos_y)

        self.player_list.append(self.player_sprite)

    # Rooms created
    def entrance(self):
        my_map = arcade.tilemap.read_tmx("mapas/archivos tsx/entrada.tmx")

        self.paredes = arcade.tilemap.process_layer(my_map, "paredes", 1)
        self.suelo = arcade.tilemap.process_layer(my_map, "suelo ", 1)
        self.cosas = arcade.tilemap.process_layer(my_map, "cosas", 1)
        self.obstaculos = arcade.tilemap.process_layer(my_map, "obstaculos", 1)

        # Enemies
        # Enemies 2
        self.enemy = Enemy(640, 305, 2, 3)
        self.enemy_sprite = arcade.Sprite("mapas/personajes/enemigo 2.png", 1, center_x=self.enemy.pos_x, center_y=self.enemy.pos_y)
        self.enemy_sprite.speed = self.enemy.speed
        self.enemy_sprite.number_of_hearts = self.enemy.number_of_hearts
        self.enemy_list.append(self.enemy_sprite)
        self.physics_engine_enemy=(arcade.PhysicsEngineSimple(self.enemy_sprite, self.enemy_list))

        # Enemies 3
        self.enemy = Enemy(0, 500, 4, 1)
        self.enemy_sprite = arcade.Sprite("mapas/personajes/enemigo 3.png", 1, center_x=self.enemy.pos_x, center_y=self.enemy.pos_y)
        self.enemy_sprite.speed = self.enemy.speed
        self.enemy_sprite.number_of_hearts = self.enemy.number_of_hearts
        self.enemy_list.append(self.enemy_sprite)
        self.physics_engine_enemy1 =(arcade.PhysicsEngineSimple(self.enemy_sprite, self.enemy_list))

        # Enemies 1
        self.enemy = Enemy(0, 305, 2, 2)
        self.enemy_sprite = arcade.Sprite("mapas/personajes/enemigo 1.png", 1, center_x=self.enemy.pos_x, center_y=self.enemy.pos_y)
        self.enemy_sprite.speed = self.enemy.speed
        self.enemy_sprite.number_of_hearts = self.enemy.number_of_hearts
        self.enemy_list.append(self.enemy_sprite)
        self.physics_engine_enemy2 = (arcade.PhysicsEngineSimple(self.enemy_sprite, self.enemy_list))

    def room_1(self):

        my_map = arcade.tilemap.read_tmx("mapas/archivos tsx/planta 1.tmx")

        self.paredes = arcade.tilemap.process_layer(my_map, "paredes", 1)
        self.suelo = arcade.tilemap.process_layer(my_map, "suelo ", 1)
        self.obstaculos_2 = arcade.tilemap.process_layer(my_map, "obstaculos 2", 1)
        self.obstaculos = arcade.tilemap.process_layer(my_map, "obstaculos", 1)
        self.perfeccionar = arcade.tilemap.process_layer(my_map, "perfeccionar", 1)

    def room_2(self):
        my_map = arcade.tilemap.read_tmx("mapas/archivos tsx/planta 2.tmx")

        self.paredes = arcade.tilemap.process_layer(my_map, "paredes", 1)
        self.suelo = arcade.tilemap.process_layer(my_map, "suelo ", 1)
        self.obstaculos_2 = arcade.tilemap.process_layer(my_map, "obstaculos2", 1)
        self.obstaculos = arcade.tilemap.process_layer(my_map, "obstaculos", 1)
        self.perfeccionar = arcade.tilemap.process_layer(my_map, "perfeccionar", 1)
        self.cuerpos = arcade.tilemap.process_layer(my_map, "cuerpos", 1)
        self.sangre = arcade.tilemap.process_layer(my_map, "sangre", 1)

    def room_3(self):
        my_map = arcade.tilemap.read_tmx("mapas/archivos tsx/planta 3.tmx")

        self.paredes = arcade.tilemap.process_layer(my_map, "paredes", 1)
        self.suelo = arcade.tilemap.process_layer(my_map, "suelo ", 1)
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
            self.player_sprite.center_y = 620
            self.player_sprite.center_x = 416

        if self.player_sprite.center_y > 635 and 298 < self.player_sprite.center_x < 343 and self.current_room == 1:
            self.current_room = 2
            self.room_2()
            self.player_sprite.center_y = 30
            self.player_sprite.center_x = 288

        if self.player_sprite.center_y > 635 and 256 < self.player_sprite.center_x < 320 and self.current_room == 2:
            self.current_room = 3
            self.room_3()
            self.player_sprite.center_y = 30
            self.player_sprite.center_x = 256

        # Going down stairs
        if self.player_sprite.center_y < 10 and 224 < self.player_sprite.center_x < 288 and self.current_room == 3:
            self.current_room = 2
            self.room_2()
            self.player_sprite.center_y = 620
            self.player_sprite.center_x = 288

        if self.player_sprite.center_y < 10 and 256 < self.player_sprite.center_x < 320 and self.current_room == 2:
            self.current_room = 1
            self.room_1()
            self.player_sprite.center_y = 620
            self.player_sprite.center_x = 320

        if self.player_sprite.center_y > 635 and 389 < self.player_sprite.center_x < 438 and self.current_room == 1:
            self.current_room = 0
            self.entrance()
            self.player_sprite.center_y = 620
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

        # collision of the bullet with enemy
        for self.bullet_sprite in self.bullet_list:
            collision_bullet_enemy = arcade.check_for_collision_with_list(self.bullet_sprite, self.enemy_list)
            if len(collision_bullet_enemy) > 0:
                self.bullet_sprite.remove_from_sprite_lists()

            # enemy actualization of hearts
            for self.enemy_sprite in collision_bullet_enemy:
                if self.enemy_sprite.number_of_hearts > 0:
                    self.enemy_sprite.number_of_hearts -= 1
                if self.enemy_sprite.number_of_hearts == 0:
                    self.enemy_sprite.remove_from_sprite_lists()

        # List to make the enemy goes to the coordenates of the player
        for self.enemy_sprite in self.enemy_list:
            self.movimiento(self.enemy_sprite, self.player_sprite)

        # update player position
        self.physics_engine_enemy.update()
        self.physics_engine_enemy1.update()
        self.physics_engine_enemy2.update()
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
            bullet.change_x = -bullet.speed / 2
            bullet.change_y = -bullet.speed / 2
            bullet.angle = 225
        if self.player.down and self.player.right:
            bullet.change_x = bullet.speed / 2
            bullet.change_y = -bullet.speed / 2
            bullet.angle = 315
        if self.player.up and self.player.left:
            bullet.change_x = -bullet.speed / 2
            bullet.change_y = bullet.speed / 2
            bullet.angle = 135
        if self.player.up and self.player.right:
            bullet.change_x = bullet.speed / 2
            bullet.change_y = bullet.speed / 2
            bullet.angle = 45
        if not self.player.up and not self.player.down and not self.player.right and not self.player.left:
            bullet.change_x = 0
            bullet.change_y = bullet.speed
            bullet.angle = 90

    def movimiento(self, enemy, player):

        # Movement
        if enemy.center_x < player.center_x:
            enemy.center_x += enemy.speed
        if enemy.center_x > player.center_x:
            enemy.center_x -= enemy.speed
        if enemy.center_y < player.center_y:
            enemy.center_y += enemy.speed
        if enemy.center_y > player.center_y:
            enemy.center_y -= enemy.speed

    def on_draw(self):
        """
        Render the screen
        """
        arcade.start_render()

        # draw background
        # arcade.draw_lrwh_rectangle_textured(0, 0, screen_width, screen_height, self.background_image)

        # draw of the map
        # Room entrance
        if self.current_room == 0:
            self.paredes.draw()
            self.suelo.draw()
            self.cosas.draw()
            self.obstaculos.draw()

        # Room 1
        if self.current_room == 1:
            self.paredes.draw()
            self.suelo.draw()
            self.obstaculos.draw()
            self.obstaculos_2.draw()
            self.perfeccionar.draw()

        # Room 2
        if self.current_room == 2:
            self.paredes.draw()
            self.suelo.draw()
            self.obstaculos.draw()
            self.obstaculos_2.draw()
            self.perfeccionar.draw()
            self.sangre.draw()
            self.cuerpos.draw()

        # Room 3
        if self.current_room == 3:
            self.paredes.draw()
            self.suelo.draw()
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