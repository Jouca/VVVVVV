import pygame

from ressources.constant import screen_size
from ressources.inits import init_screen, init_fonts, init_menu_selectors, init_texts, init_boxes, init_buttons
from ressources.classes import UpParallax, SelectObjectMenu, Editor, Room, Player
from ressources.functions import charger_ressource, play_music
from ressources.menus import affichage_menu, controles

pygame.mixer.pre_init(frequency=44100, size=-16, channels=1, buffer=512)
pygame.mixer.init()
clock = pygame.time.Clock()


def main():
    """
    Fonction principale du lancement du jeu.
    """
    screen = init_screen()
    fonts = init_fonts()
    menus = init_menu_selectors(fonts, screen)
    var = {
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
        "timeAnimation": 0,
        "currentMap": "history",
        "coordinates": [4, 9],
        "clicked": False,
        "left_click": False,
        "right_click": False,
        "selectobjectmenu": SelectObjectMenu(),
        "editor": Editor(screen_size, "history", [0, 0]),
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
    }

    frame_per_second = 60
    play_music(f"{var['current_music']}.ogg")
    while var["jeu_en_cours"]:
        clock.tick(frame_per_second)
        pressed_key = pygame.key.get_pressed()
        if pressed_key[pygame.K_LEFT]:
            var["left"] = True
        else:
            var["left"] = False
        if pressed_key[pygame.K_RIGHT]:
            var["right"] = True
        else:
            var["right"] = False

        var = affichage_menu(var, screen, clock)
        var = controles(var)


# START GAME
if __name__ == "__main__":
    main()
