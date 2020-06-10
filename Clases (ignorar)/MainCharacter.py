
from Clases.Character import *
from Clases.Parametros import *


class MainCharacter(Character):
    def __init__(self, filename, scale, number_of_hearts, speed):  # muere de un golpe

        super().__init__(filename, scale, number_of_hearts, speed)

        self.center_x = screen_width / 2
        self.center_y = screen_height / 2
        self.go_right = False
        self.go_left = False
        self.go_up = False
        self.go_down = False
        self.shooting_right = None
        self.shooting_left = None
        self.shooting_up = None
        self.shooting_down = None
        self.money = 40

        self.counter = 0

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

    def respawn(self):
        self.center_x = screen_width / 2
        self.center_y = screen_height / 2

    def update(self, delta_time: float = 1 / 60):

        # animacion
        # si el jugador esta parado
        if not self.go_up and not self.go_down and not self.go_right and not self.go_left:
            self.texture = self.right_facing

        # animaciones caminar
        else:
            texture_list = []
            if self.go_up:
                texture_list = self.walk_up_textures
            elif self.go_down:
                texture_list = self.walk_right_textures
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
            self.texture = self.right_facing

        if self.go_down or self.go_right or self.go_left or self.go_up:
            if self.counter % 20 == 0:
                move = arcade.load_sound(sound_folder + os.path.sep + "move.wav")
                arcade.play_sound(move)

        self.counter += 2
        # main character movement
        if self.go_right:
            self.center_x += self.speed * delta_time
        if self.go_left:
            self.center_x -= self.speed * delta_time
        if self.go_up:
            self.center_y += self.speed * delta_time
        if self.go_down:
            self.center_y -= self.speed * delta_time
