import math

import arcade
from random import *
import os.path

screen_width = 640
screen_height = 640
screen_title = "VIR-ED"
sprite_scaling = 1

absolute = os.path.abspath(__file__)
path1 = os.path.dirname(absolute)
path2 = os.path.dirname(path1)

sprites_folder = path2 + os.path.sep + "resources" + os.path.sep + "sprites" + os.path.sep + "personajes"
bullet_folder = path2 + os.path.sep + "resources" + os.path.sep + "sprites" + os.path.sep + "armas"
powerups_folder = path2 + os.path.sep + "resources" + os.path.sep + "sprites" + os.path.sep + "powerups"
resources_folder = path2 + os.path.sep + "resources" + os.path.sep + "sprites"
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

        # cargar texturas

        self.current_texture = 0
        self.left_facing = arcade.load_texture(sprites_folder + os.path.sep + "prota izq.png")
        self.right_facing = arcade.load_texture(sprites_folder + os.path.sep + "protagonista.png")
        self.up_facing = arcade.load_texture(sprites_folder + os.path.sep + "prota esp.png")
        self.walk_right_textures = []
        self.walk_left_textures = []
        self.walk_up_textures = []
        self.walk_down_textures = []
        self.walk_right_textures.append(arcade.load_texture(sprites_folder + os.path.sep + "prota dcha anda.png"))
        self.walk_right_textures.append(arcade.load_texture(sprites_folder + os.path.sep + "prota dcha anda2.png"))
        self.walk_left_textures.append(arcade.load_texture(sprites_folder + os.path.sep + "prota izq anda.png"))
        self.walk_left_textures.append(arcade.load_texture(sprites_folder + os.path.sep + "prota izq anda2 .png"))
        self.walk_up_textures.append(arcade.load_texture(sprites_folder + os.path.sep + "prota esp anda.png"))
        self.walk_up_textures.append(arcade.load_texture(sprites_folder + os.path.sep + "prota esp anda2.png"))

    def update_animation(self, delta_time: float = 1 / 60):

        # si el jugador esta parado
        if not self.go_up and not self.go_down and not self.go_right and not self.go_left:
            self.texture = self.right_facing

        # animaciones caminar
        else:
            texture_list = []
            if self.go_up:
                texture_list = self.walk_up_textures
            elif self.go_down:
                pass
            elif self.go_right:
                texture_list = self.walk_right_textures
            elif self.go_left:
                texture_list = self.walk_left_textures

            self.current_texture += 1

            if len(texture_list) > 0:
                if self.current_texture >= len(texture_list):
                    self.current_texture = 0

                self.texture = texture_list[self.current_texture]

        # apuntar
        if self.shooting_left:
            self.texture = self.left_facing
        elif self.shooting_right:
            self.texture = self.right_facing
        elif self.shooting_up:
            self.texture = self.up_facing
        elif self.shooting_down:
            pass

    def respawn(self):

        self.center_x = screen_width // 2
        self.center_y = screen_height // 2

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
        self.speed = 6

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y


class Menu(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("VIR-ED", screen_width // 2, screen_height // 2,
                         arcade.color.WHITE, font_size=30, anchor_x="center")
        arcade.draw_text("Click para empezar", screen_width // 2, screen_height // 3,
                         arcade.color.WHITE, font_size=30, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = Game()
        game_view.setup()
        self.window.show_view(game_view)


class GameOver(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Game Over", screen_width // 2, screen_height // 2,
                         arcade.color.WHITE, 30, anchor_x="center")
        arcade.draw_text("Esc - Menu\n\nR - Reiniciar", screen_width // 2, screen_height // 3,
                         arcade.color.WHITE, font_size=30, anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            menu_view = Menu()
            self.window.show_view(menu_view)
        if key == arcade.key.R:
            game_view = Game()
            game_view.setup()
            self.window.show_view(game_view)


class Game(arcade.View):
    def __init__(self):
        super().__init__()
        # lists
        self.player_list = None
        self.bullet_list = None
        self.enemy_list = None
        self.powerUpList = None
        self.weapon_list = None
        self.invisible_list = None
        self.bomb_list = None

        # main character and bullet sprites
        self.player_sprite = None
        self.bullet_sprite = None
        self.weapon = None
        self.invisible = None
        self.bomb = None

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
        self.escaleras = None

        # physics
        self.physics_paredes = None
        self.physics_cosas = None
        self.physics_obstaculos = None
        self.physics_paredes_enemy = None
        self.physics_obstaculos2 = None
        self.physics_perfeccionar = None
        self.physics_cuerpos = None
        self.physics_sangre = None
        self.physics_enemy_list = None

        # number of the room the player is
        self.current_room = 0

        # collision
        self.collision_enemy = None
        self.collision_main_character = None

        # movement of the enemies when main character is dead
        self.movement = False

        # counters
        self.cd = None
        self.score = None
        self.spawn_cd = None
        self.time = None
        self.time_quotient = None
        self.money = None

        self.start = False
        self.space = False

        self.finish_0 = False
        self.finish_1 = False
        self.finish_2 = False
        self.finish_3 = False
        self.enemy_death = False

        self.shop = None
        self.shop_list = None

        # PowerUps
        self.powerUpAguja = None
        self.powerUpListAguja = None
        self.powerUpTriple = None
        self.powerUpListTriple = None
        self.powerUpLejia = None
        self.powerUpListLejia = None
        self.triple = False
        self.cd_triple = None
        self.dissapear = True
        self.cd_dissapear = None
        self.legia = False

    def setup(self):
        """
        Set up the game and initialize the variables. Call this function to restart the game
        """
        # Set up the lists
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.weapon_list = arcade.SpriteList()
        self.powerUpList = arcade.SpriteList()
        self.invisible_list = arcade.SpriteList()
        self.physics_paredes_enemy = arcade.SpriteList()
        self.physics_enemy_list = arcade.SpriteList()
        self.physics_paredes = arcade.SpriteList()
        self.physics_cosas = arcade.SpriteList()
        self.physics_obstaculos = arcade.SpriteList()
        self.physics_paredes_enemy = arcade.SpriteList()
        self.physics_obstaculos2 = arcade.SpriteList()
        self.physics_perfeccionar = arcade.SpriteList()
        self.physics_cuerpos = arcade.SpriteList()
        self.physics_sangre = arcade.SpriteList()
        self.bomb_list = arcade.SpriteList()
        self.shop_list = arcade.SpriteList()

        self.powerUpListAguja = arcade.SpriteList()
        self.powerUpListTriple = arcade.SpriteList()
        self.powerUpListLejia = arcade.SpriteList()

        # Set up the player
        self.player_sprite = MainCharacter(sprites_folder + os.path.sep + "protagonista.png", sprite_scaling,
                                           3, 200)
        self.player_list.append(self.player_sprite)

        # The entrances is the first room
        self.entrance()

        # Set up the max number of enemies
        self.max_enemies = 10

        # Set up counters
        self.cd = 0
        self.score = 0
        self.time = 60
        self.spawn_cd = 0
        self.cd_dissapear = 0
        self.cd_triple = 0
        self.money = 0

    # Rooms created
    def entrance(self):
        # load map
        my_map = arcade.tilemap.read_tmx(maps_folder + os.path.sep + "entrada.tmx")

        # load layers
        self.paredes = arcade.tilemap.process_layer(my_map, "paredes", 1)
        self.suelo = arcade.tilemap.process_layer(my_map, "suelo ", 1)
        self.cosas = arcade.tilemap.process_layer(my_map, "cosas", 1)
        self.obstaculos = arcade.tilemap.process_layer(my_map, "obstaculos", 1)
        self.escaleras = arcade.tilemap.process_layer(my_map, "escalera", 1)

        # bomb
        if not self.finish_0:
            self.bomb = arcade.Sprite(resources_folder + os.path.sep + "bombaAntivirus.png", 1, center_x=320,
                                      center_y=320)
            self.bomb_list.append(self.bomb)

        if len(self.bomb_list) != 0 and self.finish_0:
            self.bomb.kill()

        # physics layers and player
        self.physics_paredes = arcade.PhysicsEngineSimple(self.player_sprite, self.paredes)
        self.physics_cosas = arcade.PhysicsEngineSimple(self.player_sprite, self.cosas)
        self.physics_obstaculos = arcade.PhysicsEngineSimple(self.player_sprite, self.obstaculos)

        # enemies
        self.create_enemies()
        self.create_weapon(bullet_folder + os.path.sep + "jeringa1.png", self.player_sprite.center_x + 15
                           , self.player_sprite.center_y - 5, 90)

    def room_1(self):
        # load map
        my_map = arcade.tilemap.read_tmx(maps_folder + os.path.sep + "planta1.tmx")

        # load layers
        self.paredes = arcade.tilemap.process_layer(my_map, "paredes", 1)
        self.suelo = arcade.tilemap.process_layer(my_map, "suelo ", 1)
        self.obstaculos_2 = arcade.tilemap.process_layer(my_map, "obstaculos 2", 1)
        self.obstaculos = arcade.tilemap.process_layer(my_map, "obstaculos", 1)
        self.perfeccionar = arcade.tilemap.process_layer(my_map, "perfeccionar", 1)
        self.escaleras = arcade.tilemap.process_layer(my_map, "escalera", 1)

        # bomb
        if not self.finish_1:
            self.bomb = arcade.Sprite(resources_folder + os.path.sep + "bombaAntivirus.png", 1, center_x=320,
                                      center_y=320)
            self.bomb_list.append(self.bomb)

        if len(self.bomb_list) != 0 and self.finish_1:
            self.bomb.kill()

        # physics layers and player
        self.physics_paredes = arcade.PhysicsEngineSimple(self.player_sprite, self.paredes)
        self.physics_obstaculos = arcade.PhysicsEngineSimple(self.player_sprite, self.obstaculos)
        self.physics_obstaculos2 = arcade.PhysicsEngineSimple(self.player_sprite, self.obstaculos_2)
        self.physics_perfeccionar = arcade.PhysicsEngineSimple(self.player_sprite, self.perfeccionar)

        # enemies
        self.create_enemies()

    def room_2(self):
        # load map
        my_map = arcade.tilemap.read_tmx(maps_folder + os.path.sep + "planta2.tmx")

        # load layers
        self.paredes = arcade.tilemap.process_layer(my_map, "paredes", 1)
        self.suelo = arcade.tilemap.process_layer(my_map, "suelo", 1)
        self.obstaculos_2 = arcade.tilemap.process_layer(my_map, "obstaculos2", 1)
        self.obstaculos = arcade.tilemap.process_layer(my_map, "obstaculos", 1)
        self.perfeccionar = arcade.tilemap.process_layer(my_map, "perfeccionar", 1)
        self.cuerpos = arcade.tilemap.process_layer(my_map, "cuerpos", 1)
        self.sangre = arcade.tilemap.process_layer(my_map, "sangre", 1)
        self.escaleras = arcade.tilemap.process_layer(my_map, "escalera", 1)

        # bomb
        if not self.finish_2:
            self.bomb = arcade.Sprite(resources_folder + os.path.sep + "bombaAntivirus.png", 1, center_x=320,
                                      center_y=320)
            self.bomb_list.append(self.bomb)
        if len(self.bomb_list) != 0 and self.finish_2:
            self.bomb.kill()

        # physics layers and player
        self.physics_paredes = arcade.PhysicsEngineSimple(self.player_sprite, self.paredes)
        self.physics_obstaculos = arcade.PhysicsEngineSimple(self.player_sprite, self.obstaculos)
        self.physics_obstaculos2 = arcade.PhysicsEngineSimple(self.player_sprite, self.obstaculos_2)
        self.physics_perfeccionar = arcade.PhysicsEngineSimple(self.player_sprite, self.perfeccionar)
        self.physics_cuerpos = arcade.PhysicsEngineSimple(self.player_sprite, self.cuerpos)
        self.physics_sangre = arcade.PhysicsEngineSimple(self.player_sprite, self.sangre)

        # enemies
        self.create_enemies()

    def room_3(self):
        # load map
        my_map = arcade.tilemap.read_tmx(maps_folder + os.path.sep + "planta3.tmx")

        # load layers
        self.paredes = arcade.tilemap.process_layer(my_map, "paredes", 1)
        self.suelo = arcade.tilemap.process_layer(my_map, "suelo", 1)
        self.sangre = arcade.tilemap.process_layer(my_map, "sangre", 1)
        self.obstaculos = arcade.tilemap.process_layer(my_map, "obstaculos", 1)
        self.cuerpos = arcade.tilemap.process_layer(my_map, "cuerpos", 1)
        self.escaleras = arcade.tilemap.process_layer(my_map, "escalera", 1)

        # bomb
        if not self.finish_3:
            self.bomb = arcade.Sprite(resources_folder + os.path.sep + "bombaAntivirus.png", 1, center_x=350,
                                      center_y=320)
            self.bomb_list.append(self.bomb)

        if len(self.bomb_list) != 0 and self.finish_3:
            self.bomb.kill()

        # physics layers and player
        self.physics_paredes = arcade.PhysicsEngineSimple(self.player_sprite, self.paredes)
        self.physics_obstaculos = arcade.PhysicsEngineSimple(self.player_sprite, self.obstaculos)
        self.physics_cuerpos = arcade.PhysicsEngineSimple(self.player_sprite, self.cuerpos)
        self.physics_sangre = arcade.PhysicsEngineSimple(self.player_sprite, self.sangre)

        # enemies
        self.create_enemies()

    def room_draw(self):
        # drawing layers
        # Entrance
        if self.current_room == 0:
            self.paredes.draw()
            self.suelo.draw()
            self.cosas.draw()
            self.obstaculos.draw()
            self.escaleras.draw()

        # Room 1
        if self.current_room == 1:
            self.paredes.draw()
            self.suelo.draw()
            self.obstaculos.draw()
            self.obstaculos_2.draw()
            self.perfeccionar.draw()
            self.escaleras.draw()

        # Room 2
        if self.current_room == 2:
            self.paredes.draw()
            self.suelo.draw()
            self.obstaculos.draw()
            self.obstaculos_2.draw()
            self.perfeccionar.draw()
            self.sangre.draw()
            self.cuerpos.draw()
            self.escaleras.draw()

        # Room 3
        if self.current_room == 3:
            self.paredes.draw()
            self.suelo.draw()
            self.obstaculos.draw()
            self.sangre.draw()
            self.cuerpos.draw()
            self.escaleras.draw()

    def room_update(self):

        # map update
        # Entrance -> Room 1
        if self.player_sprite.center_y > 630 and 323 < self.player_sprite.center_x < 380 and self.current_room == 0:
            if self.finish_0:
                self.current_room = 1
                self.room_1()
                self.player_sprite.center_y = 620
                self.player_sprite.center_x = 448
                self.shop.kill()
            if not self.finish_0:
                self.player_sprite.center_y = 630

        # Room 1 -> Room 2
        if self.player_sprite.center_y > 635 and 258 < self.player_sprite.center_x < 316 and self.current_room == 1:
            if self.finish_1:
                self.current_room = 2
                self.room_2()
                self.player_sprite.center_y = 30
                self.player_sprite.center_x = 288
                self.shop.kill()
            if not self.finish_1:
                self.player_sprite.center_y = 635

        # Room 2 -> Room 3
        if self.player_sprite.center_y > 635 and 258 < self.player_sprite.center_x < 316 and self.current_room == 2:
            if self.finish_2:
                self.current_room = 3
                self.room_3()
                self.player_sprite.center_y = 30
                self.player_sprite.center_x = 256
                self.shop.kill()
            if not self.finish_2:
                self.player_sprite.center_y = 635

        # Going down stairs
        # Room 3 -> Room 2
        if self.player_sprite.center_y < 10 and 226 < self.player_sprite.center_x < 284 and self.current_room == 3:
            self.current_room = 2
            self.room_2()
            self.player_sprite.center_y = 620
            self.player_sprite.center_x = 288

        # Room 2 -> Room 1
        if self.player_sprite.center_y < 10 and 256 < self.player_sprite.center_x < 320 and self.current_room == 2:
            self.current_room = 1
            self.room_1()
            self.player_sprite.center_y = 620
            self.player_sprite.center_x = 300

        # Room 1 -> Entrance
        if self.player_sprite.center_y > 640 and 418 < self.player_sprite.center_x < 476 and self.current_room == 1:
            self.current_room = 0
            self.entrance()
            self.player_sprite.center_y = 620
            self.player_sprite.center_x = 352

        self.room_update_2()

    def room_update_2(self):
        # update physics
        # Entrance
        if self.current_room == 0:
            self.physics_paredes.update()
            self.physics_cosas.update()
            self.physics_obstaculos.update()
            if len(self.enemy_list) == 0 and self.enemy_death:
                self.enemy_death = False
                self.finish_0 = True
                self.shop = arcade.Sprite(resources_folder + os.path.sep + "cartel tienda.png", 1, center_x=32,
                                          center_y=305)
                self.shop_list.append(self.shop)
            if len(self.enemy_list) > 0:
                self.finish_0 = False

        # Room 1
        if self.current_room == 1:
            self.physics_paredes.update()
            self.physics_obstaculos.update()
            self.physics_obstaculos2.update()
            self.physics_perfeccionar.update()
            if len(self.enemy_list) == 0 and self.enemy_death:
                self.enemy_death = False
                self.finish_1 = True
                self.shop = arcade.Sprite(resources_folder + os.path.sep + "cartel tienda.png", 1, center_x=32,
                                          center_y=305)
                self.shop_list.append(self.shop)
            if len(self.enemy_list) > 0:
                self.finish_1 = False
        # Room 2
        if self.current_room == 2:
            self.physics_paredes.update()
            self.physics_obstaculos.update()
            self.physics_obstaculos2.update()
            self.physics_perfeccionar.update()
            self.physics_sangre.update()
            self.physics_cuerpos.update()
            if len(self.enemy_list) == 0 and self.enemy_death:
                self.enemy_death = False
                self.finish_2 = True
                self.shop = arcade.Sprite(resources_folder + os.path.sep + "cartel tienda.png", 1, center_x=32,
                                          center_y=400)
                self.shop_list.append(self.shop)
            if len(self.enemy_list) > 0:
                self.finish_2 = False
        # Room 3
        if self.current_room == 3:
            self.physics_paredes.update()
            self.physics_sangre.update()
            self.physics_cuerpos.update()
            self.physics_obstaculos.update()
            if len(self.enemy_list) == 0 and self.enemy_death:
                self.enemy_death = False
                self.finish_3 = True
                self.shop = arcade.Sprite(resources_folder + os.path.sep + "cartel tienda.png", 1, center_x=32,
                                          center_y=335)
                self.shop_list.append(self.shop)
            if len(self.enemy_list) > 0:
                self.finish_3 = False

    def create_enemies(self):
        if self.start:
            max_number = 0
            random_number = 0
            if self.current_room == 0:
                max_number = 5
                random_number = randint(1, 2)
            if self.current_room == 1:
                max_number = 8
                random_number = randint(1, 3)
            if self.current_room == 2:
                max_number = 11
                random_number = randint(2, 3)
            if self.current_room == 3:
                max_number = 14
                random_number = randint(2, 4)
            if len(self.enemy_list) < max_number:
                for enemy in range(random_number):
                    pos_x = 0
                    pos_y = 0
                    place_choice = randint(0, 3)
                    foe_choice = randint(0, 2)

                    if place_choice == 0:
                        pos_x = randint(610, 640)
                        if self.current_room == 0 or self.current_room == 1:
                            pos_y = 300
                        if self.current_room == 2:
                            pos_y = 270
                        if self.current_room == 3:
                            pos_y = 330
                    if place_choice == 1:
                        pos_x = randint(0, 30)
                        if self.current_room == 0 or self.current_room == 1:
                            pos_y = 300
                        if self.current_room == 2:
                            pos_y = 390
                        if self.current_room == 3:
                            pos_y = 330
                    if place_choice == 2:
                        if self.current_room == 0:
                            pos_x = randint(0, 30)
                            pos_y = 300
                        if self.current_room == 1:
                            pos_x = randint(0, 30)
                            pos_y = 360
                        if self.current_room == 2:
                            pos_x = 390
                            pos_y = randint(610, 640)
                        if self.current_room == 3:
                            pos_x = 300
                            pos_y = randint(610, 640)
                    if place_choice == 3:
                        if self.current_room == 0:
                            pos_x = randint(610, 640)
                            pos_y = 300
                        if self.current_room == 1:
                            pos_x = 330
                            pos_y = randint(0, 30)
                        if self.current_room == 2:
                            pos_x = 390
                            pos_y = randint(610, 640)
                        if self.current_room == 3:
                            pos_x = 300
                            pos_y = randint(610, 640)

                    if foe_choice == 0:
                        enemy = Enemy(sprites_folder + os.path.sep + "enemigo1.png",
                                      1, pos_x, pos_y, 1, 1)
                    elif foe_choice == 1:
                        enemy = Enemy(sprites_folder + os.path.sep + "enemigo2.png",
                                      1, pos_x, pos_y, 2, 1)
                    elif foe_choice == 2:
                        enemy = Enemy(sprites_folder + os.path.sep + "enemigo3.png",
                                      1, pos_x, pos_y, 4, 1)

                    self.enemy_list.append(enemy)

    def movement_enemy(self, enemy, player):

        # Movement
        if enemy.center_x < player.center_x:
            enemy.center_x += enemy.speed
        if enemy.center_x > player.center_x:
            enemy.center_x -= enemy.speed
        if enemy.center_y < player.center_y:
            enemy.center_y += enemy.speed
        if enemy.center_y > player.center_y:
            enemy.center_y -= enemy.speed

    def create_weapon(self, weapon, pos_x, pos_y, angle):
        # Weapon
        self.weapon = arcade.Sprite(weapon, sprite_scaling / 1.5, center_x=pos_x, center_y=pos_y)
        self.weapon.angle = angle
        self.weapon_list.append(self.weapon)

    def update_weapon(self):
        if self.player_sprite.shooting_right or (self.player_sprite.change_x == 0 and self.player_sprite.change_y == 0):
            self.weapon.center_x = self.player_sprite.center_x + 15
            self.weapon.center_y = self.player_sprite.center_y - 5
            self.weapon.angle = 90

        if self.player_sprite.shooting_left:
            self.weapon.center_x = self.player_sprite.center_x - 13
            self.weapon.center_y = self.player_sprite.center_y - 4
            self.weapon.angle = 270

        if self.player_sprite.shooting_down:
            self.weapon.center_x = self.player_sprite.center_x + 5
            self.weapon.center_y = self.player_sprite.center_y - 12
            self.weapon.angle = 0

        if self.player_sprite.shooting_up:
            self.weapon.center_x = self.player_sprite.center_x + 8
            self.weapon.center_y = self.player_sprite.center_y + 5
            self.weapon.angle = 180

        if self.player_sprite.shooting_down and self.player_sprite.shooting_left:
            self.weapon.center_x = self.player_sprite.center_x - 15
            self.weapon.center_y = self.player_sprite.center_y - 8
            self.weapon.angle = 315

        if self.player_sprite.shooting_down and self.player_sprite.shooting_right:
            self.weapon.center_x = self.player_sprite.center_x + 12
            self.weapon.center_y = self.player_sprite.center_y - 10
            self.weapon.angle = 45

        if self.player_sprite.shooting_up and self.player_sprite.shooting_left:
            self.weapon.center_x = self.player_sprite.center_x - 13
            self.weapon.center_y = self.player_sprite.center_y + 4
            self.weapon.angle = 225

        if self.player_sprite.shooting_up and self.player_sprite.shooting_right:
            self.weapon.center_x = self.player_sprite.center_x + 15
            self.weapon.center_y = self.player_sprite.center_y + 3
            self.weapon.angle = 135

    def movement_shoot_player(self, delta_time):
        # main character and weapon movement
        if self.player_sprite.go_right:
            self.player_sprite.center_x += self.player_sprite.speed * delta_time
            self.weapon.center_x += self.player_sprite.speed * delta_time
        if self.player_sprite.go_left:
            self.player_sprite.center_x -= self.player_sprite.speed * delta_time
            self.weapon.center_x -= self.player_sprite.speed * delta_time
        if self.player_sprite.go_up:
            self.player_sprite.center_y += self.player_sprite.speed * delta_time
            self.weapon.center_y += self.player_sprite.speed * delta_time
        if self.player_sprite.go_down:
            self.player_sprite.center_y -= self.player_sprite.speed * delta_time
            self.weapon.center_y -= self.player_sprite.speed * delta_time

        # shooting
        if self.cd % 30 == 0:
            if self.player_sprite.shooting_right and self.player_sprite.shooting_up:
                self.shoot("right_up", None)
            elif self.player_sprite.shooting_left and self.player_sprite.shooting_up:
                self.shoot("left_up", None)
            elif self.player_sprite.shooting_right and self.player_sprite.shooting_down:
                self.shoot("right_down", None)
            elif self.player_sprite.shooting_left and self.player_sprite.shooting_down:
                self.shoot("left_down", None)
            elif self.player_sprite.shooting_right:
                self.shoot("right", None)
            elif self.player_sprite.shooting_up:
                self.shoot("up", None)
            elif self.player_sprite.shooting_left:
                self.shoot("left", None)
            elif self.player_sprite.shooting_down:
                self.shoot("down", None)

    def waves(self):
        if 40 <= self.time_quotient <= 59:
            if self.spawn_cd % 190 == 0:
                self.create_enemies()
        if 10 <= self.time_quotient <= 40:
            if self.spawn_cd % 160 == 0:
                self.create_enemies()
        if 10 >= self.time_quotient:
            if self.spawn_cd % 130 == 0:
                self.create_enemies()
        if self.time_quotient < 0:
            self.max_enemies = 0
            self.start = False
            self.time = 60
            self.enemy_death = True

    def shoot(self, direction, dir):

        # create bullet sprite
        """if self.current_room == 0:"""
        bullet = Bullet(bullet_folder + os.path.sep + "gota1.png", sprite_scaling / 2)
        self.bullet_list.append(bullet)

        """if self.current_room == 1:
            bullet = Bullet(bullet_folder + os.path.sep + "gota2.png", sprite_scaling / 2)
            self.bullet_list.append(bullet)"""

        if direction == "right":
            bullet.center_x = self.weapon.center_x + 10
            bullet.center_y = self.weapon.center_y + 1
            bullet.change_x = bullet.speed
            bullet.angle = 90
            if dir is None:
                dir = "right"
                if self.triple and dir == "right":
                    self.shoot("right_down", "right")
                    self.shoot("right_up", "right")
        if direction == "left":
            bullet.center_x = self.weapon.center_x - 10
            bullet.center_y = self.weapon.center_y
            bullet.change_x = -bullet.speed
            bullet.angle = 270
            if dir is None:
                dir = "left"
                if self.triple and dir == "left":
                    self.shoot("left_down", "left")
                    self.shoot("left_up", "left")
        if direction == "up":
            bullet.center_x = self.weapon.center_x
            bullet.center_y = self.weapon.center_y + 10
            bullet.change_y = bullet.speed
            bullet.angle = 180
            if dir is None:
                dir = "up"
                if self.triple and dir == "up":
                    self.shoot("left_up", "up")
                    self.shoot("right_up", "up")
        if direction == "down":
            bullet.center_x = self.weapon.center_x
            bullet.center_y = self.weapon.center_y - 10
            bullet.change_y = -bullet.speed
            bullet.angle = 0
            if dir is None:
                dir = "down"
                if self.triple and dir == "down":
                    self.shoot("right_down", "down")
                    self.shoot("left_down", "down")
        if direction == "right_up":
            bullet.center_x = self.weapon.center_x + 10
            bullet.center_y = self.weapon.center_y + 10
            bullet.change_x = bullet.speed / math.sqrt(2)
            bullet.change_y = bullet.speed / math.sqrt(2)
            bullet.angle = 135
            if dir is None:
                dir = "right_up"
                if self.triple and dir == "right_up":
                    self.shoot("right", "right_up")
                    self.shoot("up", "right_up")
        if direction == "right_down":
            bullet.center_x = self.weapon.center_x + 10
            bullet.center_y = self.weapon.center_y - 10
            bullet.change_x = bullet.speed / math.sqrt(2)
            bullet.change_y = -bullet.speed / math.sqrt(2)
            bullet.angle = 45
            if dir is None:
                dir = "right_down"
                if self.triple and dir == "right_down":
                    self.shoot("down", "right_down")
                    self.shoot("right", "right_down")
        if direction == "left_up":
            bullet.center_x = self.weapon.center_x - 10
            bullet.center_y = self.weapon.center_y + 10
            bullet.change_x = -bullet.speed / math.sqrt(2)
            bullet.change_y = bullet.speed / math.sqrt(2)
            bullet.angle = 225
            if dir is None:
                dir = "left_up"
                if self.triple and dir == "left_up":
                    self.shoot("left", "left_up")
                    self.shoot("up", "left_up")
        if direction == "left_down":
            bullet.center_x = self.weapon.center_x - 10
            bullet.center_y = self.weapon.center_y - 10
            bullet.change_x = -bullet.speed / math.sqrt(2)
            bullet.change_y = -bullet.speed / math.sqrt(2)
            bullet.angle = 315
            if dir is None:
                dir = "left_down"
                if self.triple and dir == "left_down":
                    self.shoot("down", "left_down")
                    self.shoot("left", "left_down")

    def collision(self, delta_time):
        # collision enemy-player, enemy-enemy and death
        for enemy in self.enemy_list:
            # enemy movement
            self.movement_enemy(enemy, self.player_sprite)

            # game over if player is hit
            if arcade.check_for_collision(self.player_sprite, enemy):
                self.player_sprite.respawn()
                arcade.pause(1)
                game_over = GameOver()
                self.window.show_view(game_over)

            # enemies physics
            self.collision_enemy = arcade.check_for_collision_with_list(enemy, self.enemy_list)
            for i in range(len(self.collision_enemy)):
                self.physics_enemy_list = arcade.PhysicsEngineSimple(self.collision_enemy[i], self.enemy_list)

            # bullet disappears, not creation of enemies and the stop
            if self.movement:
                enemy.speed = 0
                self.max_enemies = len(self.enemy_list)
                if self.dissapear:
                    for bullet in self.bullet_list:
                        bullet.kill()

        # collisions bullet - enemy
        for bullet in self.bullet_list:
            if arcade.check_for_collision_with_list(bullet, self.paredes):
                bullet.kill()
            collision_bullet_enemy = arcade.check_for_collision_with_list(bullet, self.enemy_list)
            # enemy actualization of hearts
            for enemy in collision_bullet_enemy:
                # dissapear
                if self.dissapear:
                    bullet.kill()
                if enemy.number_of_hearts > 0:
                    enemy.number_of_hearts -= 1
                if enemy.number_of_hearts == 0:
                    self.powerUps_drop(enemy, randint(0, 10))
                    enemy.kill()
                    self.money += randint(45, 55)
                    self.score += 1

        start_the_wave = arcade.check_for_collision_with_list(self.player_sprite, self.bomb_list)
        if start_the_wave and self.space:
            self.bomb.kill()
            self.start = True

        self.powerUps_update(delta_time)

    def powerUps_drop(self, enemy, number):
        if number == 0:
            self.powerUpAguja = arcade.Sprite(powerups_folder + os.path.sep + "powerUpAguja.png",
                                              center_x=enemy.center_x,
                                              center_y=enemy.center_y)
            self.powerUpListAguja.append(self.powerUpAguja)
        if number == 1:
            self.powerUpTriple = arcade.Sprite(powerups_folder + os.path.sep + "powerUpTriple.png",
                                               center_x=enemy.center_x,
                                               center_y=enemy.center_y)
            self.powerUpListTriple.append(self.powerUpTriple)
        if number == 2:
            self.powerUpLejia = arcade.Sprite(powerups_folder + os.path.sep + "poweUpLejia.png",
                                              center_x=enemy.center_x,
                                              center_y=enemy.center_y)
            self.powerUpListLejia.append(self.powerUpLejia)
        if 3 <= number <= 20:
            pass

    def powerUps_update(self, delta_time):

        # powerUp legia
        for self.powerUpLejia in self.powerUpListLejia:
            if arcade.check_for_collision_with_list(self.player_sprite, self.powerUpListLejia):
                self.legia = True
                self.powerUpLejia.kill()

        if self.legia:
            for enemy in self.enemy_list:
                enemy.kill()
                if len(self.enemy_list) == 0:
                    self.legia = False

        # powerUp triple disparo
        for self.powerUpTriple in self.powerUpListTriple:
            if arcade.check_for_collision_with_list(self.player_sprite, self.powerUpListTriple):
                self.triple = True
                self.powerUpTriple.kill()

        if self.triple:
            self.cd_triple += delta_time
            if self.cd_triple > 6:
                self.triple = False
                self.cd_triple = 0

        # powerUp agujas
        for self.powerUpAguja in self.powerUpListAguja:
            if arcade.check_for_collision_with_list(self.player_sprite, self.powerUpListAguja):
                self.powerUpAguja.kill()
                self.dissapear = False

        if not self.dissapear:
            self.cd_dissapear += delta_time
            if self.cd_dissapear > 6:
                self.dissapear = True
                self.cd_dissapear = 0

    def on_update(self, delta_time):
        """ Movement and game logic """  # collisions go here

        # Counters
        self.cd += 2
        self.spawn_cd += 1
        if self.start:
            self.time -= delta_time
        self.time_quotient = self.time // 1

        # Room updates
        self.room_update()

        # waves
        self.waves()

        for self.weapon in self.weapon_list:
            self.update_weapon()

        # update everything
        self.movement_shoot_player(delta_time)
        self.collision(delta_time)
        self.player_list.update()
        self.player_list.update_animation()
        self.bullet_list.update()
        self.enemy_list.update()
        self.bomb_list.update()
        self.physics_enemy_list.update()
        self.powerUpListAguja.update()
        self.powerUpListTriple.update()
        self.powerUpListLejia.update()

    def on_draw(self):
        """
        Render the screen
        """
        arcade.start_render()

        # draw of the map
        # Room entrance
        self.room_draw()

        # text
        arcade.draw_text(f"Score: {self.score}", 550, 615, arcade.color.WHITE, 15)
        # arcade.draw_text(f"Time wave: {self.time_quotient}", 400, 10, arcade.color.WHITE, 10)

        # draw all sprites
        self.bomb_list.draw()
        self.powerUpListAguja.draw()
        self.powerUpListTriple.draw()
        self.powerUpListLejia.draw()
        self.weapon_list.draw()
        self.player_list.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()
        self.shop_list.draw()

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
                self.shoot("right", None)
            self.player_sprite.shooting_right = True
            self.cd = 0
        if key == arcade.key.LEFT:
            if not self.player_sprite.shooting_right and (not self.player_sprite.shooting_up
                                                          and not self.player_sprite.shooting_down):
                self.shoot("left", None)
            self.player_sprite.shooting_left = True
            self.cd = 0
        if key == arcade.key.UP:
            if not self.player_sprite.shooting_left and (not self.player_sprite.shooting_right
                                                         and not self.player_sprite.shooting_down):
                self.shoot("up", None)
            self.player_sprite.shooting_up = True
            self.cd = 0
        if key == arcade.key.DOWN:
            if not self.player_sprite.shooting_left and (not self.player_sprite.shooting_up
                                                         and not self.player_sprite.shooting_right):
                self.shoot("down", None)
            self.player_sprite.shooting_down = True
            self.cd = 0

        if key == arcade.key.SPACE:
            self.space = True

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

        if key == arcade.key.SPACE:
            self.space = False


def main():
    window = arcade.Window(screen_width, screen_height, screen_title)
    menu = Menu()
    window.show_view(menu)
    arcade.run()


if __name__ == "__main__":
    main()
