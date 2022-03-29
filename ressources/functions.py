import pygame, json, os
from PIL import Image, ImageOps

def charger_ressource(path):
    """
    Permet de lire les ressources du jeu.

    >>> charger_ressource("/sprites/info.png")
    """
    ressource = pygame.image.load(f"./ressources{path}")
    return ressource


def convert_PIL_to_pygame(image):
    """
    Convertit une image PIL en image pygame.
    """
    mode = image.mode
    size = image.size
    data = image.tobytes()

    py_image = pygame.image.fromstring(data, size, mode)
    return py_image


def stop_music(fadeout=False):
    if fadeout:
        pygame.mixer.music.fadeout(1000)
    else:
        pygame.mixer.music.stop()


def play_sound(path):
    """
    Joue un son.
    """
    sound = pygame.mixer.Sound(f"./ressources/sounds/{path}")
    sound.set_volume(0.5)
    sound.play()


def play_music(path):
    """
    Joue une musique en boucle.
    """
    pygame.mixer.music.load(f"./ressources/musics/{path}")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)


def check_already_started():
    """
    Vérifie si le jeu a déjà été lancé.
    """
    with open("./ressources/data/data-histoire.vvvvvv", "r") as f:
        data = json.load(f)
    f.close()
    if data["started"] == 1:
        return True
    else:
        return False


def crop(input, height, width, scale_size=None):
    im = Image.open(input)
    imgwidth, imgheight = im.size
    images = []
    for i in range(0,imgheight,height):
        for j in range(0,imgwidth,width):
            box = (j, i, j+width, i+height)
            a = im.crop(box)
            a = a.convert("RGBA")
            if scale_size:
                a = a.resize(scale_size)
            images.append(a)
    return images


def create_map(name_map):
    checked = True
    count = 2
    while checked:
        if not os.path.isdir(name_map):
            os.mkdir(f"./ressources/maps/{name_map}")
            checked = False
        else:
            name_map = f"{name_map} ({count})"
            count += 1


def check_room_exist(name_map, coordinates):
    if os.path.exists(f"./ressources/maps/{name_map}/{coordinates}.vvvvvv"):
        return True
    return False


def check_map_exist(name_map):
    if os.path.isdir(f"./ressources/maps/{name_map}"):
        return True
    return False


def create_data_room(name_map, coordinates):
    room_strings = {"map_data":[[{}]*32]*24, "music":"presenting_vvvvvv"}
    with open(f"./ressources/maps/{name_map}/{coordinates}.vvvvvv", "w") as f:
        json.dump(room_strings, f)
    f.close()


def read_room_data(name_map, coordinates):
    with open(f"./ressources/maps/{name_map}/{coordinates}.vvvvvv", "r") as f:
        data = json.load(f)
    f.close()
    return data


def map_editor_process(name_map, coordinates):
    if check_map_exist(name_map):
        if check_room_exist(name_map, coordinates):
            return True
        else:
            create_data_room(name_map, coordinates)
            return True
    else:
        return None


def apply_color(image, color):
    alpha = image.split()[3]  # [r, g, b, a][3] -> a

    colored = ImageOps.colorize(
        image.convert("L"), black=(0, 0, 0), white=(255,255,255), mid=color
    )
    colored.putalpha(alpha)

    return colored


def get_screen_size():
    return pygame.display.get_surface().get_size()