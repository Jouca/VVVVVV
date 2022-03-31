import pygame

try:
    from classes import Object, BGStars
except ModuleNotFoundError:
    from .classes import Object, BGStars

DEBUG = True
VERSION = "V. infdev"
screen_size = (960, 780)

# Variables importantes
objects = Object()
stars = BGStars(4, 12)

# Couleurs
couleur = {
    "translucent": pygame.Color(255, 255, 255, 25),
    "black": pygame.Color(0, 0, 0),
    "white": pygame.Color(255, 255, 255),
    "red": pygame.Color(255, 0, 0),
    "green": pygame.Color(0, 255, 0),
    "blue": pygame.Color(0, 57, 255),
    "yellow": pygame.Color(255, 255, 0),
    "cyan": pygame.Color(20, 200, 220),
    "cyan_transparent": pygame.Color(177, 177, 255),
    "gold": pygame.Color(255, 200, 0)
}

# Couleurs jeu
couleur_jeu = {
    "green": pygame.Color(148, 238, 130),
    "blue": pygame.Color(131, 141, 235),
    "pink": pygame.Color(235, 139, 223),
    "red": pygame.Color(242, 126, 151),
    "yellow": pygame.Color(229, 235, 133),
    "cyan": pygame.Color(137, 235, 206),
}
