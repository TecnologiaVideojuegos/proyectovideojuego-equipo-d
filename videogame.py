import random
import arcade


class Persona:

    # Constructor
    def __init__(self, pos_x, pos_y):
        # , arma, muerto, num_vidas, velocidad, vida):
        # self.arma =
        # self.muerto =
        # self.num_vidas =
        self.pos_x = pos_x
        self.pos_y = pos_y
        # self.velocidad =
        # self.vida =

    def atacar(self, key):
        # Cada vez que el protagonista toque una tecla para poder atacar o cuando el enemigo toque al jugador
        # Personaje
        if key == arcade.key.SPACE:
            # Que salga una bala en direccion en la que haya disparado
            # La velocidad de la bala que puede aumentar
            pass

    def get_vida(self):
        # que coja la vida que tenga la persona

        pass

    def recibir_daño(self):
        # cada vez que haga atacar y toque a alguien que le vaya quitando vida
        pass

    def set_vida(self):
        # y se la ponga
        pass


class Protagonista(Persona):

    # Constructor
    def __init__(self, pos_x, pos_y):
        # , arma, muerto, num_vidas, velocidad, vida, dinero):
        super().__init__(pos_x, pos_y)
        # , arma, muerto, num_vidas, velocidad, vida)
        # self.dinero = 0

    # Metodos
    def get_dinero(self):
        # Coge el dinero
        pass

    def get_num_vidas(self):
        # Coge el numero de vidas
        pass

    def get_velocidad(self):
        # Coge a la velocidad que va
        pass

    def set_num_vidas(self):
        # Pone el numero de vidas, si la vida es 0 o inferior, baja una vida
        pass

    def set_velocidad(self):
        # Si el personaje tiene una mejora de velocidad, la sube
        pass


class Enemigo(Persona):

    # Constructor
    def __init__(self, pos_x, pos_y):
        # , muerto, velocidad, vida, drop_list):
        super().__init__(pos_x, pos_y)
        # , muerto,  velocidad, vida)
        self.drop_list = []

    def drop(self):
        # El drop que el enemigo suelta
        pass


class Juego(arcade.Window):

    # Constructor
    def __init__(self):
        super().__init__(800, 600, "Nombre del videojuego")

        # Listas
        self.lista_persona = None
        self.lista_enemigos = None

        # Sprites
        self.sprite_persona = None
        self.sprite_enemigos = None

        # Coordenadas
        self.coor_protagonista = None
        self.lista_enemigos_coor_x = []
        self.lista_enemigos_coor_y = []
        self.coor_enemigos = None

    def setup(self):

        # Creacion de las listas
        self.lista_persona = arcade.SpriteList()
        self.lista_enemigos = arcade.SpriteList()

        # Creacion del personaje
        self.sprite_persona = arcade.Sprite("persona.png", 0.5)
        self.lista_persona.append(self.sprite_persona)

        # Creacion del enemigo
        for i in range(0, 10):
            self.sprite_enemigos = arcade.Sprite("persona.png", 0.25)
            self.sprite_enemigos.center_y = 600
            self.sprite_enemigos.center_x = random.randrange(0, 800)
            self.lista_enemigos.append(self.sprite_enemigos)
            self.lista_enemigos_coor_x.append(self.sprite_enemigos.center_x)
            self.lista_enemigos_coor_y.append(self.sprite_enemigos.center_y)

        # Coordenadas enviadas a las clases
        self.coor_protagonista = Protagonista(self.sprite_persona.center_y, self.sprite_persona.center_x)
        self.coor_enemigos = Enemigo(self.lista_enemigos_coor_x, self.lista_enemigos_coor_y)

        # Color de fondo
        arcade.set_background_color(arcade.color.AIR_SUPERIORITY_BLUE)

    def on_draw(self):

        # Renderiza
        arcade.start_render()

        # Dibuja
        self.lista_persona.draw()
        self.lista_enemigos.draw()

    def on_key_press(self, tecla, modifiers):

        # Movimiento del protagonista dependiendo de la tecla que pulse
        if tecla == arcade.key.LEFT:
            self.sprite_persona.change_x = -5
        elif tecla == arcade.key.RIGHT:
            self.sprite_persona.change_x = 5
        elif tecla == arcade.key.UP:
            self.sprite_persona.change_y = 5
        elif tecla == arcade.key.DOWN:
            self.sprite_persona.change_y = -5

    def on_key_release(self, tecla, modifiers):

        # Se para cuando se suelta una tecla
        if tecla == arcade.key.LEFT or tecla == arcade.key.RIGHT:
            self.sprite_persona.change_x = 0
        elif tecla == arcade.key.UP or tecla == arcade.key.DOWN:
            self.sprite_persona.change_y = 0

    def on_update(self, delta_time):

        # Actualiza las posiciones de todos los personajes
        self.lista_persona.update()
        self.lista_enemigos.update()


def main():

    # Metodo main
    window = Juego()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
