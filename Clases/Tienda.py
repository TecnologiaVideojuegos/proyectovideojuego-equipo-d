
from Clases.Item import *


class Tienda:
    objetos_planta_baja = [] # bisturi && botas
    objetos_planta1 = [] # jeringa2 && botas && bisturi
    objetos_planta2 = [] # jergina3 && botas
    objetos_planta3 = [] # escalpelo electrico && corazon

    def __init__(self):
        self.tendero = arcade.Sprite(sprites_folder + os.path.sep + "tendero.png", sprite_scaling,
                                     center_x=screen_width / 2, center_y=450)

        # planta baja
        self.botas = Item(powerups_folder + os.path.sep + "Botas.png", 300, 400, 8)
        # add bisturi
        self.objetos_planta_baja.append(self.botas)

        # planta 1
        self.jeringa2 = Item(bullet_folder + os.path.sep + "jeringa2.png", 250, 400, 10)

        self.objetos_planta1.append(self.jeringa2)
        self.objetos_planta1.append(self.botas)

        # planta 2
        self.jeringa3 = Item(bullet_folder + os.path.sep + "jeringa3.png", 250, 400, 12)

        self.objetos_planta2.append(self.jeringa3)
        self.objetos_planta2.append(self.botas)

        # planta 3
        self.corazon = Item(powerups_folder + os.path.sep + "corazon obj.png", 300, 400, 15)

        self.objetos_planta3.append(self.corazon)

    def draw_tendero(self):
        self.tendero.draw()

    def draw_obj_planta_baja(self):
        for item in self.objetos_planta_baja:  # poner una variable para dejar espacios entre prints
            if not item.recogido:
                # dibujo sprite objeto
                item.draw()
                # dibujo precio
                arcade.Sprite(powerups_folder + os.path.sep + "moneda1.png", sprite_scaling / 1.5,
                              center_x=item.center_x,
                              center_y=item.center_y - 30).draw()
                arcade.draw_text(str(item.precio), item.center_x - 20, item.center_y - 37, arcade.color.BLACK, 10)

    def draw_obj_planta1(self):
        for item in self.objetos_planta1:  # poner una variable para dejar espacios entre prints
            if not item.recogido:
                # dibujo sprite objeto
                item.draw()
                # dibujo precio
                arcade.Sprite(powerups_folder + os.path.sep + "moneda1.png", sprite_scaling / 1.5,
                              center_x=item.center_x,
                              center_y=item.center_y - 30).draw()
                arcade.draw_text(str(item.precio), item.center_x - 20, item.center_y - 37, arcade.color.BLACK, 10)

    def draw_obj_planta2(self):
        for item in self.objetos_planta2:  # poner una variable para dejar espacios entre prints
            if not item.recogido:
                # dibujo sprite objeto
                item.draw()
                # dibujo precio
                arcade.Sprite(powerups_folder + os.path.sep + "moneda1.png", sprite_scaling / 1.5,
                              center_x=item.center_x,
                              center_y=item.center_y - 30).draw()
                arcade.draw_text(str(item.precio), item.center_x - 20, item.center_y - 37, arcade.color.BLACK, 10)

    def draw_obj_planta3(self):
        for item in self.objetos_planta3:  # poner una variable para dejar espacios entre prints
            if not item.recogido:
                # dibujo sprite objeto
                item.draw()
                # dibujo precio
                arcade.Sprite(powerups_folder + os.path.sep + "moneda1.png", sprite_scaling / 1.5,
                              center_x=item.center_x,
                              center_y=item.center_y - 30).draw()
                arcade.draw_text(str(item.precio), item.center_x - 20, item.center_y - 37, arcade.color.BLACK, 10)