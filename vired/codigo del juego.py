import arcade
from random import *
import os.path
import pymunk

screen_width = 640
screen_height = 640
screen_title = "Journey of the Prairie King"
sprite_scaling = 1

absolute = os.path.abspath(__file__)
path1 = os.path.dirname(absolute)
path2 = os.path.dirname(path1)
print(path2)

sprites_folder = path2 + os.path.sep + "resources" + os.path.sep + "sprites" + os.path.sep + "personajes"
bullet_folder =path2 + os.path.sep + "resources" + os.path.sep + "sprites"
maps_folder = path2 + os.path.sep + "resources" + os.path.sep + "maps"
layer_folder = path2 + os.path.sep + "resources" + os.path.sep + "maps" + os.path.sep + "layers"


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
        self.go_right = False
        self.go_left = False
        self.go_up = False
        self.go_down = False
        self.shooting_right = None
        self.shooting_left = None
        self.shooting_up = None
        self.shooting_down = None
        self.shooting_right_up = False
        self.shooting_right_down = False
        self.shooting_left_up = False
        self.shooting_left_up = False

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
        pass


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

        # lists
        self.player_list = None
        self.bullet_list = None
        self.enemy_list = None
        self.powerUpList = None

        # main character and bullet sprites
        self.player_sprite = None
        self.bullet_sprite = None

        # max number of enemies
        self.max_enemies = None

        # map sprites
        self.paredes = None
        self.suelo = None
        self.cosas = None
        self.obstaculos = None
        self.obstaculos_2 = None
        self.perfeccionar = None
        self.cuerpos = None
        self.sangre = None
        self.physics_paredes = None

        # number of the room the player is
        self.current_room = 0

        self.cd = None
        self.score = None
        self.spawn_cd = None

    def setup(self):
        """
        Set up the game and initialize the variables. Call this function to restart the game
        """

        # Set up the lists
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.powerUpList = arcade.SpriteList()
        self.physics_paredes = arcade.SpriteList()

        # Set up the player
        self.player_sprite = MainCharacter(sprites_folder + os.path.sep + "protagonista.png", sprite_scaling,
            3, 200)
        self.player_list.append(self.player_sprite)

        # The entrances is the first room
        self.entrance()

        # Set up the max number of enemies
        self.max_enemies = 10

        self.cd = 0
        self.score = 0
        # tiempo de reaparicion de enemigos
        self.spawn_cd = 0

    # Rooms created
    def entrance(self):
        my_map = arcade.tilemap.read_tmx(maps_folder + os.path.sep + "entrada.tmx")

        self.paredes = arcade.tilemap.process_layer(my_map,"paredes", 1)
        self.suelo = arcade.tilemap.process_layer(my_map,"suelo ", 1)
        self.cosas = arcade.tilemap.process_layer(my_map,"cosas", 1)
        self.obstaculos = arcade.tilemap.process_layer(my_map,"obstaculos", 1)

        self.physics_paredes = arcade.PhysicsEngineSimple(self.player_sprite, self.paredes)

    def room_1(self):

        my_map = arcade.tilemap.read_tmx(maps_folder + os.path.sep + "planta1.tmx")

        self.paredes = arcade.tilemap.process_layer(my_map, "paredes", 1)
        self.suelo = arcade.tilemap.process_layer(my_map, "suelo ", 1)
        self.obstaculos_2 = arcade.tilemap.process_layer(my_map, "obstaculos 2", 1)
        self.obstaculos = arcade.tilemap.process_layer(my_map, "obstaculos", 1)
        self.perfeccionar = arcade.tilemap.process_layer(my_map, "perfeccionar", 1)

        self.physics_paredes = arcade.PhysicsEngineSimple(self.player_sprite, self.paredes)

    def room_2(self):
        my_map = arcade.tilemap.read_tmx(maps_folder + os.path.sep + "planta2.tmx")

        self.paredes = arcade.tilemap.process_layer(my_map, "paredes", 1)
        self.suelo = arcade.tilemap.process_layer(my_map, "suelo", 1)
        self.obstaculos_2 = arcade.tilemap.process_layer(my_map, "obstaculos2", 1)
        self.obstaculos = arcade.tilemap.process_layer(my_map, "obstaculos", 1)
        self.perfeccionar = arcade.tilemap.process_layer(my_map, "perfeccionar", 1)
        self.cuerpos = arcade.tilemap.process_layer(my_map, "cuerpos", 1)
        self.sangre = arcade.tilemap.process_layer(my_map, "sangre", 1)

        self.physics_paredes = arcade.PhysicsEngineSimple(self.player_sprite, self.paredes)

    def room_3(self):
        my_map = arcade.tilemap.read_tmx(maps_folder + os.path.sep + "planta3.tmx")

        self.paredes = arcade.tilemap.process_layer(my_map, "paredes", 1)
        self.suelo = arcade.tilemap.process_layer(my_map, "suelo", 1)
        self.sangre = arcade.tilemap.process_layer(my_map, "sangre", 1)
        self.obstaculos = arcade.tilemap.process_layer(my_map, "obstaculos", 1)
        self.cuerpos = arcade.tilemap.process_layer(my_map, "cuerpos", 1)

        self.physics_paredes = arcade.PhysicsEngineSimple(self.player_sprite, self.paredes)

    def create_enemies(self, max_number):

        if len(self.enemy_list) < max_number:
            random_number = randint(1, 3)
            for enemy in range(random_number):
                pos_x = 0
                pos_y = 0
                place_choice = randint(0, 3)
                foe_choice = randint(0, 2)

                if place_choice == 0:
                    pos_x = randint(240, 340)
                    pos_y = randint(20, 21)
                elif place_choice == 1:
                    pos_x = randint(240, 340)
                    pos_y = randint(600, screen_height - 20)
                elif place_choice == 2:
                    pos_x = randint(20, 21)
                    pos_y = randint(240, 340)
                elif place_choice == 3:
                    pos_x = randint(600, screen_width - 20)
                    pos_y = randint(240, 340)

                if foe_choice == 0:
                    enemy = Enemy(sprites_folder + os.path.sep + "enemigo1.png",
                              1.5, pos_x, pos_y, 1, 3)
                elif foe_choice == 1:
                    enemy = Enemy(sprites_folder + os.path.sep + "enemigo2.png",
                              1.5, pos_x, pos_y, 2, 2)
                elif foe_choice == 2:
                    enemy = Enemy(sprites_folder + os.path.sep + "enemigo3.png",
                              1.5, pos_x, pos_y, 3, 1)

                self.enemy_list.append(enemy)
                self.physics_enemy = arcade.PhysicsEngineSimple(enemy, self.enemy_list)

    def on_update(self, delta_time):
        """ Movement and game logic """  # collisions go here

        self.cd += 2
        self.spawn_cd += 1

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

        if self.player_sprite.center_y > 650 and 389 < self.player_sprite.center_x < 438 and self.current_room == 1:
            self.current_room = 0
            self.entrance()
            self.player_sprite.center_y = 620
            self.player_sprite.center_x = 352

        # main character movement
        if self.player_sprite.go_right:
            self.player_sprite.center_x += self.player_sprite.speed * delta_time
        if self.player_sprite.go_left:
            self.player_sprite.center_x -= self.player_sprite.speed * delta_time
        if self.player_sprite.go_up:
            self.player_sprite.center_y += self.player_sprite.speed * delta_time
        if self.player_sprite.go_down:
            self.player_sprite.center_y -= self.player_sprite.speed * delta_time

        # Nos puede servir para hacer que el personaje no pase hasta que se haya acabado la ronda
        """# collisions with screen borders
        if self.player_sprite.center_x + 20 >= screen_width:
            self.player_sprite.center_x = screen_width - 20
        if self.player_sprite.center_x - 20 <= 0:
            self.player_sprite.center_x = 20
        if self.player_sprite.center_y + 32 >= screen_height:
            self.player_sprite.center_y = screen_height - 32
        if self.player_sprite.center_y - 30 <= 0:
            self.player_sprite.center_y = 30"""

        # shooting
        if self.cd % 30 == 0:

            if self.player_sprite.shooting_right and self.player_sprite.shooting_up:
                self.shoot("right_up")
            elif self.player_sprite.shooting_left and self.player_sprite.shooting_up:
                self.shoot("left_up")
            elif self.player_sprite.shooting_right and self.player_sprite.shooting_down:
                self.shoot("right_down")
            elif self.player_sprite.shooting_left and self.player_sprite.shooting_down:
                self.shoot("left_down")
            elif self.player_sprite.shooting_right:
                self.shoot("right")
            elif self.player_sprite.shooting_up:
                self.shoot("up")
            elif self.player_sprite.shooting_left:
                self.shoot("left")
            elif self.player_sprite.shooting_down:
                self.shoot("down")

        # collisions bullet - enemy
        for bullet in self.bullet_list:
            collision_bullet_enemy = arcade.check_for_collision_with_list(bullet, self.enemy_list)
            # enemy actualization of hearts
            for enemy in collision_bullet_enemy:
                bullet.remove_from_sprite_lists()
                if enemy.number_of_hearts > 0:
                    enemy.number_of_hearts -= 1
                if enemy.number_of_hearts == 0:
                    enemy.remove_from_sprite_lists()
                    self.score += 1

        if self.spawn_cd % 150 == 0:
            self.create_enemies(self.max_enemies)
        for enemy in self.enemy_list:
            self.movimiento(enemy, self.player_sprite)
            self.physics_enemy = arcade.check_for_collision_with_list(enemy, self.enemy_list)
            for enemy in self.physics_enemy:
                if len(self.physics_enemy) == 2:
                    enemy.change_y =0

        # update everything
        self.player_list.update()
        self.bullet_list.update()
        self.enemy_list.update()
        self.physics_paredes.update()
        
    def shoot(self, direction):

        # create bullet sprite
        bullet = Bullet(bullet_folder + os.path.sep + "bullet2.png", sprite_scaling/2)
        bullet.center_x = self.player_sprite.center_x
        bullet.center_y = self.player_sprite.center_y
        self.bullet_list.append(bullet)

        if direction == "right":
            bullet.change_x = bullet.speed
        if direction == "left":
            bullet.change_x = -bullet.speed
        if direction == "up":
            bullet.change_y = bullet.speed
        if direction == "down":
            bullet.change_y = -bullet.speed
        if direction == "right_up":
            bullet.change_x = bullet.speed
            bullet.change_y = bullet.speed
        if direction == "right_down":
            bullet.change_x = bullet.speed
            bullet.change_y = -bullet.speed
        if direction == "left_up":
            bullet.change_x = -bullet.speed
            bullet.change_y = bullet.speed
        if direction == "left_down":
            bullet.change_x = -bullet.speed
            bullet.change_y = -bullet.speed

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

        arcade.draw_text(f"Score: {self.score}", 550, 600, arcade.color.WHITE, 15)

        # draw all sprites
        self.player_list.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()

    def on_key_press(self, key, modifiers):

        # move character
        if key == arcade.key.W:
            self.player_sprite.go_up = True
        if key == arcade.key.A:
            self.player_sprite.go_left = True
        if key == arcade.key.S:
            self.player_sprite.go_down = True
        if key == arcade.key.D:
            self.player_sprite.go_right = True

        # player shooting
        if key == arcade.key.RIGHT:
            if not self.player_sprite.shooting_left and (not self.player_sprite.shooting_up
                                                         and not self.player_sprite.shooting_down):
                self.shoot("right")
            self.player_sprite.shooting_right = True
            self.cd = 0
        if key == arcade.key.LEFT:
            if not self.player_sprite.shooting_right and (not self.player_sprite.shooting_up
                                                          and not self.player_sprite.shooting_down):
                self.shoot("left")
            self.player_sprite.shooting_left = True
            self.cd = 0
        if key == arcade.key.UP:
            if not self.player_sprite.shooting_left and (not self.player_sprite.shooting_right
                                                         and not self.player_sprite.shooting_down):
                self.shoot("up")
            self.player_sprite.shooting_up = True
            self.cd = 0
        if key == arcade.key.DOWN:
            if not self.player_sprite.shooting_left and (not self.player_sprite.shooting_up
                                                         and not self.player_sprite.shooting_right):
                self.shoot("down")
            self.player_sprite.shooting_down = True
            self.cd = 0

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.player_sprite.go_up = False
        if key == arcade.key.A:
            self.player_sprite.go_left = False
        if key == arcade.key.S:
            self.player_sprite.go_down = False
        if key == arcade.key.D:
            self.player_sprite.go_right = False

        if key == arcade.key.RIGHT:
            self.player_sprite.shooting_right = False
        if key == arcade.key.LEFT:
            self.player_sprite.shooting_left = False
        if key == arcade.key.UP:
            self.player_sprite.shooting_up = False
        if key == arcade.key.DOWN:
            self.player_sprite.shooting_down = False


def main():
    game = Game()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
