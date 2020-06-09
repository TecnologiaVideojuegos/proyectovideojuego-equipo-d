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
music_folder = path2 + os.path.sep + "resources" + os.path.sep + "newmusic"
sound_folder = path2 + os.path.sep + "resources" + os.path.sep + "newsounds"
pantallas_folder = path2 + os.path.sep + "resources" + os.path.sep + "maps" + os.path.sep + "pantallas"
