import pygame

try:
    from constant import couleur, screen_size, VERSION, DEBUG
    from colors import couleur_jeu
    from classes import MenuSelector, Box, ImageButton, Object
    from functions import charger_ressource, convert_PIL_to_pygame
except ModuleNotFoundError:
    from .constant import couleur, screen_size, VERSION, DEBUG
    from .colors import couleur_jeu
    from .classes import MenuSelector, Box, ImageButton, Object
    from .functions import charger_ressource, convert_PIL_to_pygame

all_platforms = Object().get_all_platforms()
all_backgrounds = Object().get_all_backgrounds()
all_objects = Object().get_all_objects()

def init_screen():
    """
    Initialise les paramètres de pygame.
    """
    pygame.init()
    pygame.mixer.pre_init(44100, -16, 2, 1024)
    pygame.mixer.music.set_volume(0.7)
    pygame.display.set_caption("VVVVVV")
    pygame.display.set_icon(charger_ressource("/sprites/icon.png"))
    screen = pygame.display.set_mode(screen_size)
    return screen


def init_fonts():
    """
    Initialise les polices d'écritures.
    """
    fonts = {
        "big_generalfont": pygame.font.Font(
            "./ressources/fonts/PetMe64.ttf",
            45
        ),
        "normal_generalfont": pygame.font.Font(
            "./ressources/fonts/PetMe64.ttf",
            40
        ),
        "small_generalfont": pygame.font.Font(
            "./ressources/fonts/PetMe64.ttf",
            35
        ),
        "little_generalfont": pygame.font.Font(
            "./ressources/fonts/PetMe64.ttf",
            25
        ),
        "verylittle_generalfont": pygame.font.Font(
            "./ressources/fonts/PetMe64.ttf",
            20
        ),
    }
    return fonts


def init_texts(fonts):
    """
    Initialise les textes du jeu.
    """
    texts = {
        "subtitle": fonts["little_generalfont"].render(
            "Pygame & Online Edition",
            True,
            couleur["cyan"]
        ),
        "version": fonts["little_generalfont"].render(
            VERSION,
            True,
            couleur["cyan_transparent"]
        ),
        "jouca_creator": fonts["small_generalfont"].render(
            "Crée par Jouca / Diego",
            True,
            couleur["cyan"]
        ),
        "terry": fonts["verylittle_generalfont"].render(
            "(Recréation de VVVVVV par Terry Cavanagh)",
            True,
            couleur["cyan_transparent"]
        ),
        "color": fonts["verylittle_generalfont"].render(
            "Couleur :",
            True,
            couleur["cyan"]
        ),
    }
    return texts


def init_menu_selectors(font, screen):
    """
    Initialise les sélecteurs de menus.
    """
    menu_selectors = {
        "principal": MenuSelector(
            screen,
            [
                ["jouer", couleur["cyan"], font["little_generalfont"]],
                ["en ligne", couleur["cyan"], font["little_generalfont"]],
                ["debug", couleur["cyan"], font["little_generalfont"]] if DEBUG is True else None,
                ["crédits", couleur["cyan"], font["little_generalfont"]],
                ["quitter", couleur["cyan"], font["little_generalfont"]],
            ]
        ),
        "debug": MenuSelector(
            screen,
            [
                ["éditeur histoire", couleur["cyan"], font["little_generalfont"]],
            ]
        ),
    }
    return menu_selectors

def init_boxes():
    """
    Initialise les boîtes.
    """
    boxes = {
        "selector": Box((screen_size[0] - 40, 300), couleur_jeu["blurple"]),
    }
    return boxes


def init_buttons():
    """
    Initialise les boutons.
    """
    buttons = {
        "platform": ImageButton(
            convert_PIL_to_pygame(all_platforms[0]),
            (60, 60),
            couleur_jeu["blurple"]
        ),
        "background": ImageButton(
            convert_PIL_to_pygame(all_backgrounds[0]),
            (60, 60),
            couleur_jeu["blurple"]
        ),
        "object": ImageButton(
            convert_PIL_to_pygame(all_objects[0]),
            (60, 60),
            couleur_jeu["blurple"]
        ),
        "page_left": ImageButton(
            charger_ressource("/sprites/left_arrow.png"),
            (40, 40),
            couleur_jeu["blurple"]
        ),
        "page_right": ImageButton(
            charger_ressource("/sprites/right_arrow.png"),
            (40, 40),
            couleur_jeu["blurple"]
        ),
        "color_left": ImageButton(
            charger_ressource("/sprites/left_arrow.png"),
            (40, 40),
            couleur_jeu["blurple"]
        ),
        "color_right": ImageButton(
            charger_ressource("/sprites/right_arrow.png"),
            (40, 40),
            couleur_jeu["blurple"]
        ),
    }
    return buttons