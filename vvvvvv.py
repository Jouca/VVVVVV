import pygame

from src.constant import screen_size, DEBUG, couleur
from src.inits import init_screen, init_fonts, init_menu_selectors, init_texts, init_boxes
from src.inits import init_buttons
from src.classes import UpParallax, SelectObjectMenu, Editor, Room, Player, Flash, Clock
from src.functions import charger_ressource, play_music, check_appdata_folder
from src.menus import affichage_menu, controles

pygame.mixer.pre_init(frequency=44100, size=-16, channels=1, buffer=512)
pygame.mixer.init()
pygame.mixer.music.set_volume(0.3)
clock = pygame.time.Clock()


def main():
    """
    Fonction principale du lancement du jeu.
    """
    screen = init_screen()
    fonts = init_fonts()
    menus = init_menu_selectors(fonts, screen)
    var = {
        "debug": DEBUG,
        "screen": screen,
        "appdata": check_appdata_folder(),
        "screen_size": screen_size,
        "width": screen_size[0],
        "heigth": screen_size[1],
        "jeu_en_cours": True,
        "fonts": fonts,

        "texts": init_texts(fonts),
        "menus": menus,
        "boxes": init_boxes(),
        "buttons": init_buttons(),
        "menuSelect": "principal",
        "menuBG": UpParallax(
            screen,
            charger_ressource("/sprites/menuBG.png"),
            6
        ),
        "deaths": 0,
        "flips": 0,
        "timeAnimation": 0,
        "currentMap": "history",
        "levelname": "",
        "coordinates": [4, 9],
        "clicked": False,
        "left_click": False,
        "right_click": False,
        "selectobjectmenu": SelectObjectMenu(),
        "editor": Editor(screen_size, "history", [4, 9]),
        "room": Room("history", [4, 9]),
        "current_music": "menu",
        "players": {
            "viridian": Player("viridian"),
            "violet": Player("violet"),
            "victoria": Player("victoria"),
            "vermilion": Player("vermilion"),
            "vitellary": Player("vitellary"),
            "verdigris": Player("verdigris"),
        },
        "left": False,
        "right": False,
        "collisions_show": False,
        "dead": False,
        "victory": False,
        "dead_animation": 0,
        "victory_animation": 0,
        "teleporter_activated": False,
        "checkpoint_position": ((433, 568), False),
        "checkpoint_coordinates": [4, 9],
        "flash": Flash(screen_size, couleur["white"], 10),
        "clock": Clock()
    }

    frame_per_second = 60
    play_music(f"{var['current_music']}.ogg")
    while var["jeu_en_cours"]:
        clock.tick(frame_per_second)
        pressed_key = pygame.key.get_pressed()
        var["clock"].tick()

        var["left"] = pressed_key[pygame.K_LEFT]
        var["right"] = pressed_key[pygame.K_RIGHT]

        var = affichage_menu(var, screen, clock)
        var = controles(var)
    exit()


# START GAME
if __name__ == "__main__":
    main()
