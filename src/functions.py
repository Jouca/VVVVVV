import pygame, json, os, gzip
from PIL import Image, ImageOps
try:
    from officiallevels import OFFICIAL_LEVELS
except ModuleNotFoundError:
    from .officiallevels import OFFICIAL_LEVELS


def empty_room():
    return {
        "map_data": [[{}]*32]*24,
        "roomname": "",
        "music": "presenting_vvvvvv"
    }


def check_appdata_folder():
    """
    Permet de crée le dossier data si il n'existe pas dans %appdata%.
    """
    data = "{}"
    dir_path = '%s\\VVVVVV_Python\\' % os.environ['APPDATA']
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        with open("%s\\levels.vvvvvv" % dir_path, "wb") as f:
            f.write(gzip.compress(data.encode("utf-8")))
    elif not os.path.exists("%s\\levels.vvvvvv" % dir_path):
        with open("%s\\levels.vvvvvv" % dir_path, "wb") as f:
            f.write(gzip.compress(data.encode("utf-8")))
    return dir_path


def read_appdata_levels():
    """
    Permet de lire le fichier des niveaux sauvegardé dans appdata.
    """
    with open("%s\\levels.vvvvvv" % check_appdata_folder(), "rb") as f:
        return json.loads(gzip.decompress(f.read()).decode("utf-8"))


def write_appdata_levels(name_map, coordinates, data):
    """
    Permet d'écrire des données sur le niveau présent dans le dossier appdata.
    """
    json_data = read_appdata_levels()
    json_data[name_map][str(coordinates)] = data
    jdata = json.dumps(json_data)
    serial = jdata.encode('utf-8')
    with open("%s\\levels.vvvvvv" % check_appdata_folder(), "wb") as f:
        f.write(gzip.compress(serial))


def read_ressources_levels(name_map):
    """
    Permet de lire les niveaux présent dans le fichier ressource.
    """
    with open(f"./ressources/maps/{name_map}.vvvvvv", "rb") as f:
        return json.loads(gzip.decompress(f.read()).decode("utf-8"))


def write_ressources_levels(name_map, coordinates, data):
    """
    Permet d'écrire des données sur le niveau présent dans le dossier ressource.
    """
    json_data = read_ressources_levels(name_map)
    json_data[str(coordinates)] = data
    jdata = json.dumps(json_data)
    serial = jdata.encode('utf-8')
    with open(f"./ressources/maps/{name_map}.vvvvvv", "wb") as f:
        f.write(gzip.compress(serial))


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
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)


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
    data = read_appdata_levels()
    data[name_map] = {}
    jdata = json.dumps(data)
    serial = jdata.encode('utf-8')
    with open("%s\\levels.vvvvvv" % check_appdata_folder(), "wb") as f:
        f.write(gzip.compress(serial))


def check_room_exist(name_map, coordinates):
    if name_map in OFFICIAL_LEVELS:
        if str(coordinates) in read_ressources_levels(name_map).keys():
            return True
    elif str(coordinates) in read_appdata_levels()[name_map].keys():
        return True
    return False


def check_map_exist(name_map):
    if name_map in OFFICIAL_LEVELS:
        if os.path.isdir(f"./ressources/maps/{name_map}.vvvvvv"):
            return True
    elif name_map in read_appdata_levels().keys():
        return True
    return False


def create_data_room(name_map, coordinates):
    if name_map in OFFICIAL_LEVELS:
        write_ressources_levels(name_map, coordinates, empty_room())
    else:
        write_appdata_levels(name_map, coordinates, empty_room())


def read_room_data(name_map, coordinates):
    try:
        if name_map in OFFICIAL_LEVELS:
            return read_ressources_levels(name_map)[str(coordinates)]
        else:
            return read_appdata_levels()[name_map][str(coordinates)]
    except KeyError:
        return None


def write_room_data(name_map, coordinates, data):
    if name_map in OFFICIAL_LEVELS:
        write_ressources_levels(name_map, coordinates, data)
    else:
        write_appdata_levels(name_map, coordinates, data)


def check_not_empty_room(name_map):
    if name_map in OFFICIAL_LEVELS:
        map = read_ressources_levels(name_map)
        map_temp = map.copy()
        for room in map.keys():
            if map[room]["map_data"] == empty_room()["map_data"]:
                del map_temp[room]
        with open (f"./ressources/maps/{name_map}.vvvvvv", "wb") as f:
            f.write(gzip.compress(json.dumps(map_temp).encode("utf-8")))
    else:
        allmap = read_appdata_levels()
        map = allmap[name_map]
        map_temp = map.copy()
        for room in map.keys():
            if map[room]["map_data"] == empty_room()["map_data"]:
                del map_temp[room]
        allmap[name_map] = map_temp.copy()
        with open("%s\\levels.vvvvvv" % check_appdata_folder(), "wb") as f:
            f.write(gzip.compress(json.dumps(allmap).encode("utf-8")))


def map_editor_process(name_map, coordinates):
    check_not_empty_room(name_map)
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