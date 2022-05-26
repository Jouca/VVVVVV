import pygame
import os
try:
    from constant import couleur, stars
    from colors import couleur_jeu
    from functions import charger_ressource, play_sound, play_music, convert_PIL_to_pygame
    from functions import check_already_started, map_editor_process, create_map, crop
    from classes import MenuSelector, Room
except ModuleNotFoundError:
    from .constant import couleur, stars
    from .colors import couleur_jeu
    from .functions import charger_ressource, play_sound, play_music, convert_PIL_to_pygame
    from .functions import check_already_started, map_editor_process, create_map, crop
    from .classes import MenuSelector, Room


def update_fps(clock):
    """
    Met à jour le nombre de FPS.
    """
    font = pygame.font.SysFont("Arial", 18)
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color(255, 255, 255))
    return fps_text


def affichage_editeur(screen, var):
    """
    Affiche l'éditeur.
    """
    screen.fill(couleur["black"])
    var["editor"].draw(screen, var)
    coordinates_show = var["fonts"]["verylittle_generalfont"].render(
        str(var["coordinates"]),
        True,
        couleur["white"]
    )
    var["editor"].show_cursor(screen)
    var["selectobjectmenu"].draw(screen, var)
    screen.blit(coordinates_show, (screen.get_width() - 155, 10))
    rect = pygame.Rect(0, 720, screen.get_width(), screen.get_height() - 720)
    text = var["fonts"]["little_generalfont"].render(
        var["editor"].get_roomname(),
        True,
        couleur_jeu["cyan"]
    )
    text_rect = text.get_rect(center=(rect.width // 2, rect.y + 15))
    screen.blit(text, text_rect)
    return var


def affichage_selectobject(screen, var):
    """
    Affiche le menu de sélection des objets.
    """
    screen.fill(couleur["black"])
    var["editor"].draw(screen, var)
    rect = pygame.Rect(0, 720, screen.get_width(), screen.get_height() - 720)
    text = var["fonts"]["little_generalfont"].render(
        var["editor"].get_roomname(),
        True,
        couleur_jeu["cyan"]
    )
    text_rect = text.get_rect(center=(rect.width // 2, rect.y + 15))
    screen.blit(text, text_rect)
    coordinates_show = var["fonts"]["verylittle_generalfont"].render(
        str(var["coordinates"]),
        True,
        couleur["white"]
    )
    screen.blit(coordinates_show, (screen.get_width() - 155, 10))
    var["selectobjectmenu"].draw(screen, var)
    return var


def affichage_editeur_menu(screen, var):
    """
    Affiche le menu de l'éditeur.
    """
    var["editor"].draw(screen, var)
    coordinates_show = var["fonts"]["verylittle_generalfont"].render(
        str(var["coordinates"]),
        True,
        couleur["white"]
    )
    screen.blit(coordinates_show, (screen.get_width() - 155, 10))
    var["boxes"]["editeurmenu"].draw(screen, (170, 130))
    var["menus"]["editeurmenu"].draw((200, 250), 40)
    rect = pygame.Rect(0, 720, screen.get_width(), screen.get_height() - 720)
    text = var["fonts"]["little_generalfont"].render(
        var["editor"].get_roomname(),
        True,
        couleur_jeu["cyan"]
    )
    text_rect = text.get_rect(center=(rect.width // 2, rect.y + 15))
    screen.blit(text, text_rect)
    return var


def affichage_editeur_room_name(screen, var):
    """
    Affiche le menu pour changer le nom d'une salle.
    """
    screen.fill(couleur["black"])
    var["editor"].draw(screen, var)
    coords_show = var["fonts"]["verylittle_generalfont"].render(
        str(var["coordinates"]),
        True,
        couleur["white"]
    )
    screen.blit(coords_show, (screen.get_width() - 155, 10))
    rect = pygame.Rect(0, 720, screen.get_width(), screen.get_height() - 720)
    text = var["fonts"]["little_generalfont"].render(
        var["editor"].get_roomname(),
        True,
        couleur_jeu["cyan"]
    )
    text_rect = text.get_rect(center=(rect.width // 2, rect.y + 15))
    screen.blit(text, text_rect)
    return var


def affichage_menu_principal(screen, var):
    """
    Affiche le menu principal.
    """
    var["menuBG"].draw()
    screen.blit(charger_ressource("/sprites/logo.png"), (200, 60))
    screen.blit(var["texts"]["subtitle"], (190, 150))
    screen.blit(var["texts"]["version"], (730, 750))
    var["menus"]["principal"].draw((350, 300), 40)
    return var


def affichage_menu_en_ligne(screen, var):
    """
    Affiche le menu en ligne.
    """
    var["menuBG"].draw()
    var["menus"]["enligne"].draw((350, 300), 40)
    return var


def affichage_menu_niveaux_editeur(screen, var):
    """
    Affiche le menu des niveaux pouvant être ouvert dans l'éditeur.
    """
    var["menuBG"].draw()
    var["menus"]["editeurniveau"].draw((350, 300), 40)
    return var


def affichage_create_level(screen, var):
    """
    Affiche le menu de création de niveau.
    """
    var["menuBG"].draw()
    screen.blit(var["texts"]["typelevelname"], (200, 150))
    screen.blit(var["texts"]["pressenter"], (70, 550))
    rect = pygame.Rect(70, 260, 800, 50)
    text = var["fonts"]["small_generalfont"].render(var["levelname"], True, couleur_jeu["white"])
    text_rect = text.get_rect(center=rect.center)
    screen.blit(text, text_rect)
    return var


def affichage_jouer_niveau(screen, var):
    """
    Affiche le menu de jouer un niveau.
    """
    var["menuBG"].draw()
    var["menus"]["jouerniveau"].draw((350, 300), 40)
    return var


def affichage_menu_histoire(screen, var):
    """
    Affiche le menu de l'histoire.
    """
    screen.fill(couleur["black"])
    if var["timeAnimation"] == 50:
        play_music("pause.ogg")
    if var["timeAnimation"] >= 50:
        stars.draw(screen)
        var["room"].draw(screen)
        var["players"]["viridian"].update_platforms(var["room"].get_rects())
        var["players"]["viridian"].draw(screen, var)
        var["players"]["viridian"].update(var)
        var["room"].draw_roomname(screen, var)
        if var["collisions_show"]:
            for i in var["room"].get_rects():
                pygame.draw.rect(screen, couleur["blue"], i, 1)
    var["timeAnimation"] += 1
    return var


def affichage_jeu(screen, var):
    """
    Affiche le jeu.
    """
    screen.fill(couleur["black"])
    stars.draw(screen)
    var = var["room"].draw(screen, var)
    var["room"].conveyors_animations(screen, var)
    var["room"].draw_checkpoint(screen, var)
    var["players"]["viridian"].update_platforms(var["room"].get_rects())
    if var["victory_animation"] < 260:
        var["players"]["viridian"].draw(screen, var)
    if var["teleporter_activated"]:
        var["room"].teleporter_animations(screen, var)
    else:
        var["room"].reset_teleporter()
    var["players"]["viridian"].update(var)
    var["room"].draw_roomname(screen, var)
    if var["collisions_show"]:
        show_collisions(screen, var)
    return var


def show_collisions(screen, var):
    """
    Affiche les collisions.
    """
    for i in var["room"].get_rects():
        if i[1] == "platform":
            pygame.draw.rect(screen, couleur["blue"], i[0], 1)
        elif i[1] == "enemy":
            pygame.draw.rect(screen, couleur["red"], i[0], 1)
        elif i[1] == "conveyor_left" or i[1] == "conveyor_right":
            pygame.draw.rect(screen, couleur["yellow"], i[0], 1)
        elif i[1] == "laser_v" or i[1] == "laser_h":
            pygame.draw.rect(screen, couleur["yellow"], i[0], 1)
        elif i[1] == "checkpoint_up" or i[1] == "checkpoint_down":
            pygame.draw.rect(screen, couleur["green"], i[0], 1)
        elif i[1] == "teleporter":
            pygame.draw.rect(screen, couleur["green"], i[0], 1)


def affichage_menu_jeu(screen, var):
    """
    Affiche le menu de jeu.
    """
    var = affichage_jeu(screen, var)
    var["boxes"]["menujeu"].draw(screen, (170, 130))
    var["menus"]["menujeu"].draw((300, 250), 40)
    screen.blit(var["texts"]["menu"], (380, 150))
    screen.blit(var["texts"]["warnmenujeu1"], (230, 430))
    screen.blit(var["texts"]["warnmenujeu2"], (190, 458))
    return var


def affichage_victory(screen, var):
    """
    Affiche la victoire.
    """
    var["victory_animation"] += 1
    screen.fill(couleur["black"])
    stars.draw(screen)
    var = var["room"].draw(screen, var)
    var["room"].conveyors_animations(screen, var)
    var["room"].draw_checkpoint(screen, var)
    var["room"].draw_roomname(screen, var)
    var["boxes"]["victory"].draw(screen, (130, 160))
    rect = pygame.Rect(130, 160, 700, 400)
    screen.blit(
        convert_PIL_to_pygame(
            crop(
                "./ressources/sprites/levelcomplete.png",
                48,
                320,
                (640, 96)
            )[0]
        ),
        (rect.x + 20, rect.y)
    )
    death = var["fonts"]["small_generalfont"].render(
        f"Morts : {var['deaths']}",
        True,
        couleur_jeu["cyan"]
    )
    death_rect = death.get_rect(center=rect.center)
    flip = var["fonts"]["small_generalfont"].render(
        f"Flips : {var['flips']}",
        True,
        couleur_jeu["cyan"]
    )
    flip_rect = flip.get_rect(center=rect.center)
    clock = var['clock'].convert_time()
    timer = var["fonts"]["small_generalfont"].render(
        f"Temps : {clock}",
        True,
        couleur_jeu["cyan"]
    )
    timer_rect = timer.get_rect(center=rect.center)
    if var["victory_animation"] >= 600:
        screen.blit(death, (death_rect.x, 290))
    if var["victory_animation"] >= 630:
        screen.blit(flip, (flip_rect.x, 340))
    if var["victory_animation"] >= 660:
        screen.blit(timer, (timer_rect.x, 390))
    if var["victory_animation"] >= 830:
        press = var["fonts"]["absolutelittle_generalfont"].render(
            "(Appuyer sur une touche pour continuer)",
            True,
            couleur_jeu["white"]
        )
        screen.blit(press, (150, 510))
    return var


def affichage_menu_credits(screen, var):
    """
    Affiche le menu des crédits.
    """
    var["menuBG"].draw()
    screen.blit(var["texts"]["jouca_creator"], (110, 150))
    screen.blit(var["texts"]["terry"], (75, 250))
    return var


def affichage_menu_debug(screen, var):
    """
    Affiche le menu debug.
    """
    var["menuBG"].draw()
    var["menus"]["debug"].draw((240, 300), 40)
    return var


def affichage_menu(var, screen, clock):
    """
    Permet de gérer l'affichage des menus.
    """
    var = menus_affichage[var["menuSelect"]](screen, var)

    if var["debug"]:
        font = pygame.font.SysFont("Arial", 18)
        screen.blit(update_fps(clock), (10, 0))
        screen.blit(font.render(str(var["coordinates"]), 1, pygame.Color(255, 255, 255)), (10, 20))
    pygame.display.flip()
    return var


def controles_principal(var, event):
    """
    Occupation des contrôles du menu principal.
    """
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            play_sound("menu.wav")
            var["menus"]["principal"].selection_haut()
        if event.key == pygame.K_DOWN:
            play_sound("menu.wav")
            var["menus"]["principal"].selection_bas()
        if event.key == pygame.K_RETURN:
            play_sound("menu.wav")
            if var["menus"]["principal"].menuselection[0] == "jouer":
                if check_already_started():
                    var["menuSelect"] = "play"
                else:
                    var["menuSelect"] = "jeu"
                    var["coordinates"] = [4, 9]
                    var["room"] = Room("history", [4, 9])
                    var["clock"].reset()
                    var["clock"].start_clock()
                    var["room"].play_music(var)
                    var["room"].change_room(var["coordinates"], var)
                    var["players"]["viridian"].update_positions([433, 568])
            if var["menus"]["principal"].menuselection[0] == "en ligne":
                var["menuSelect"] = "online"
            if var["menus"]["principal"].menuselection[0] == "debug":
                var["menuSelect"] = "debug"
            if var["menus"]["principal"].menuselection[0] == "crédits":
                var["menuSelect"] = "credits"
            if var["menus"]["principal"].menuselection[0] == "quitter":
                var["jeu_en_cours"] = False
    return var


def controles_en_ligne(var, event):
    """
    Occupation des contrôles du menu en ligne.
    """
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            play_sound("menu.wav")
            var["menus"]["enligne"].selection_haut()
        if event.key == pygame.K_DOWN:
            play_sound("menu.wav")
            var["menus"]["enligne"].selection_bas()
        if event.key == pygame.K_ESCAPE:
            play_sound("menu.wav")
            var["menuSelect"] = "principal"
        if event.key == pygame.K_RETURN:
            play_sound("menu.wav")
            if var["menus"]["enligne"].menuselection[0] == "retour":
                var["menuSelect"] = "principal"
            elif var["menus"]["enligne"].menuselection[0] == "éditeur niveau":
                levelmenu = [["crée niveau", couleur["white"], var["fonts"]["little_generalfont"]]]
                for level in os.listdir('./ressources/maps'):
                    if level != "history":
                        levelmenu.append(
                            [level, couleur["cyan"], var["fonts"]["little_generalfont"]]
                        )
                levelmenu.append(["retour", couleur["white"], var["fonts"]["little_generalfont"]])
                var["menus"]["editeurniveau"] = MenuSelector(
                    var["screen"],
                    levelmenu,
                )
                var["menuSelect"] = "niveauxediteur"
            elif var["menus"]["enligne"].menuselection[0] == "jouer niveau":
                levelmenu = []
                for level in os.listdir('./ressources/maps'):
                    if level != "history":
                        levelmenu.append(
                            [level, couleur["cyan"], var["fonts"]["little_generalfont"]]
                        )
                levelmenu.append(["retour", couleur["white"], var["fonts"]["little_generalfont"]])
                var["menus"]["jouerniveau"] = MenuSelector(
                    var["screen"],
                    levelmenu,
                )
                var["menuSelect"] = "niveauxjouer"
    return var


def controles_niveaux_editeur(var, event):
    """
    Occupation des contrôles du menu éditeur de niveaux.
    """
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            play_sound("menu.wav")
            var["menus"]["editeurniveau"].selection_haut()
        if event.key == pygame.K_DOWN:
            play_sound("menu.wav")
            var["menus"]["editeurniveau"].selection_bas()
        if event.key == pygame.K_ESCAPE:
            play_sound("menu.wav")
            var["menuSelect"] = "online"
        if event.key == pygame.K_RETURN:
            play_sound("menu.wav")
            if var["menus"]["editeurniveau"].menuselection[0] == "retour":
                var["menuSelect"] = "online"
            elif var["menus"]["editeurniveau"].menuselection[0] == "crée niveau":
                var["menuSelect"] = "createlevel"
            else:
                for button in var["menus"]["editeurniveau"].get_menus():
                    if button[0] == var["menus"]["editeurniveau"].menuselection[0]:
                        var["currentMap"] = button[0]
                        var["coordinates"] = [4, 9]
                        var["menuSelect"] = "editeur"
                        data = map_editor_process(var["currentMap"], var["coordinates"])
                        if data is None:
                            create_map(var["currentMap"])
                            data = map_editor_process(var["currentMap"], var["coordinates"])
                        var["editor"].update_mapdata(var["currentMap"], var["coordinates"])
                        var["editor"].change_room(var["coordinates"], var)
    return var


def controles_niveaux_jouer(var, event):
    """
    Occupation des contrôles du menu jouer de niveaux.
    """
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            play_sound("menu.wav")
            var["menus"]["jouerniveau"].selection_haut()
        if event.key == pygame.K_DOWN:
            play_sound("menu.wav")
            var["menus"]["jouerniveau"].selection_bas()
        if event.key == pygame.K_ESCAPE:
            play_sound("menu.wav")
            var["menuSelect"] = "online"
        if event.key == pygame.K_RETURN:
            play_sound("menu.wav")
            if var["menus"]["jouerniveau"].menuselection[0] == "retour":
                var["menuSelect"] = "online"
            else:
                for button in var["menus"]["jouerniveau"].get_menus():
                    if button[0] == var["menus"]["jouerniveau"].menuselection[0]:
                        var["menuSelect"] = "jeu"
                        var["coordinates"] = [4, 9]
                        var["clock"].reset()
                        var["clock"].start_clock()
                        var["room"] = Room(button[0], [4, 9])
                        var["room"].play_music(var)
                        var["room"].change_room(var["coordinates"], var)
                        var["players"]["viridian"].update_positions([433, 568])

    return var


def controles_createlevel(var, event):
    """
    Occupation des contrôles du menu création de niveaux.
    """
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            var["menuSelect"] = "editeurniveau"
            var["levelname"] = ""
        elif event.key == pygame.K_BACKSPACE:
            var["levelname"] = var["levelname"][:-1]
        elif event.key == pygame.K_RETURN:
            if var["levelname"] != "":
                var["currentMap"] = var["levelname"]
            else:
                var["currentMap"] = "unknown"
            var["levelname"] = ""
            var["coordinates"] = [4, 9]
            var["menuSelect"] = "editeur"
            data = map_editor_process(var["currentMap"], var["coordinates"])
            if data is None:
                create_map(var["currentMap"])
                data = map_editor_process(var["currentMap"], var["coordinates"])
            var["editor"].update_mapdata(var["currentMap"], var["coordinates"])
            var["editor"].change_room(var["coordinates"], var)
        else:
            var["levelname"] += event.unicode
    return var


def controles_histoire(var, event):
    """
    Occupation des contrôles du menu histoire.
    """
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            play_sound("menu.wav")
            var["menuSelect"] = "principal"
            play_music("menu.ogg")
        elif event.key == pygame.K_SPACE:
            var["players"]["viridian"].change_gravity()
        if var["debug"]:
            if event.key == pygame.K_c:
                if var["collisions_show"]:
                    var["collisions_show"] = False
                else:
                    var["collisions_show"] = True
    return var


def controles_jeu(var, event):
    """
    Occupation des contrôles du menu jeu.
    """
    if event.type == pygame.KEYDOWN:
        if var["dead"] is False and var["victory"] is False:
            if event.key == pygame.K_ESCAPE:
                play_sound("menu.wav")
                var["clock"].stop_clock()
                var["menuSelect"] = "menujeu"
            elif event.key == pygame.K_SPACE:
                var["flips"] += 1
                var["players"]["viridian"].change_gravity()
        if var["debug"]:
            if event.key == pygame.K_c:
                if var["collisions_show"]:
                    var["collisions_show"] = False
                else:
                    var["collisions_show"] = True
    if pygame.mixer.music.get_endevent() == 0:
        pygame.mixer.music.set_endevent(1)
        pygame.mixer.music.play(-1)
    return var


def controles_victory(var, event):
    """
    Occupation des contrôles du menu victoire.
    """
    if event.type == pygame.KEYDOWN and var["victory_animation"] >= 840:
        play_sound("menu.wav")
        var["checkpoint_position"] = ((433, 568), False)
        var["checkpoint_coordinates"] = [4, 9]
        var["menuSelect"] = "principal"
        var["current_music"] = "menu.ogg"
        var["victory_animation"] = 0
        var["victory"] = False
        var["deaths"] = 0
        var["flips"] = 0
        var["players"]["viridian"].reset_gravity()
        play_music("menu.ogg")
    return var


def controles_menu_jeu(var, event):
    """
    Occupation des contrôles du menu jeu.
    """
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            var["menuSelect"] = "jeu"
        if event.key == pygame.K_UP:
            play_sound("menu.wav")
            var["menus"]["menujeu"].selection_haut()
        if event.key == pygame.K_DOWN:
            play_sound("menu.wav")
            var["menus"]["menujeu"].selection_bas()
        if event.key == pygame.K_RETURN:
            play_sound("menu.wav")
            if var["menus"]["menujeu"].menuselection[0] == "continuer":
                var["clock"].start_clock()
                var["menuSelect"] = "jeu"
            elif var["menus"]["menujeu"].menuselection[0] == "retour menu":
                play_sound("menu.wav")
                var["checkpoint_position"] = ((433, 568), False)
                var["checkpoint_coordinates"] = [4, 9]
                var["menuSelect"] = "principal"
                var["current_music"] = "menu.ogg"
                var["victory_animation"] = 0
                var["victory"] = False
                var["deaths"] = 0
                var["flips"] = 0
                var["players"]["viridian"].reset_gravity()
                play_music("menu.ogg")
    return var


def controles_credits(var, event):
    """
    Occupation des contrôles du menu des crédits.
    """
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            var["menuSelect"] = "principal"
    return var


def controles_debug(var, event):
    """
    Occupation des contrôles du menu debug.
    """
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            var["menuSelect"] = "principal"
        if event.key == pygame.K_RETURN:
            play_sound("menu.wav")
            if var["menus"]["debug"].menuselection[0] == "éditeur histoire":
                var["currentMap"] = "history"
                var["coordinates"] = [4, 9]
                var["menuSelect"] = "editeur"
                data = map_editor_process(var["currentMap"], var["coordinates"])
                if data is None:
                    create_map(var["currentMap"])
                    data = map_editor_process(var["currentMap"], var["coordinates"])
                var["editor"].update_mapdata(var["currentMap"], var["coordinates"])
                var["editor"].change_room(var["coordinates"], var)
    return var


def controles_editeur(var, event):
    """
    Occupation des contrôles de l'éditeur.
    """
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            var["menuSelect"] = "editeurmenu"
        elif event.key == pygame.K_TAB:
            var["menuSelect"] = "selectobject"
            var["selectobjectmenu"].change_anim_mode()
        elif event.key == pygame.K_s:
            var["editor"].save_data(var["coordinates"])
            play_sound("gamesaved.wav")
        elif event.key == pygame.K_RIGHT:
            if var["coordinates"][0] < 25 and var["coordinates"][0] > -25:
                var["coordinates"][0] += 1
                map_editor_process(var["currentMap"], var["coordinates"])
                var["editor"].change_room(var["coordinates"], var)
            elif var["coordinates"][0] == -25:
                var["coordinates"][0] += 1
                map_editor_process(var["currentMap"], var["coordinates"])
                var["editor"].change_room(var["coordinates"], var)
        elif event.key == pygame.K_LEFT:
            if var["coordinates"][0] > -25 and var["coordinates"][0] < 25:
                var["coordinates"][0] -= 1
                map_editor_process(var["currentMap"], var["coordinates"])
                var["editor"].change_room(var["coordinates"], var)
            elif var["coordinates"][0] == 25:
                var["coordinates"][0] -= 1
                map_editor_process(var["currentMap"], var["coordinates"])
                var["editor"].change_room(var["coordinates"], var)
        elif event.key == pygame.K_UP:
            if var["coordinates"][1] < 25 and var["coordinates"][1] > -25:
                var["coordinates"][1] += 1
                map_editor_process(var["currentMap"], var["coordinates"])
                var["editor"].change_room(var["coordinates"], var)
            elif var["coordinates"][1] == -25:
                var["coordinates"][1] += 1
                map_editor_process(var["currentMap"], var["coordinates"])
                var["editor"].change_room(var["coordinates"], var)
        elif event.key == pygame.K_DOWN:
            if var["coordinates"][1] > -25 and var["coordinates"][1] < 25:
                var["coordinates"][1] -= 1
                map_editor_process(var["currentMap"], var["coordinates"])
                var["editor"].change_room(var["coordinates"], var)
            elif var["coordinates"][1] == 25:
                var["coordinates"][1] -= 1
                map_editor_process(var["currentMap"], var["coordinates"])
                var["editor"].change_room(var["coordinates"], var)
    elif event.type == pygame.MOUSEBUTTONDOWN:
        var["clicked"] = True
        if event.button == 3:
            var["editor"].remove_object()
            var["right_click"] = True
        elif event.button == 1:
            var["editor"].place_object()
            var["left_click"] = True
    elif event.type == pygame.MOUSEBUTTONUP:
        var["clicked"] = False
        var["left_click"], var["right_click"] = False, False
    elif var["clicked"]:
        if var["right_click"]:
            var["editor"].remove_object()
        elif var["left_click"]:
            var["editor"].place_object()
    var["editor"].cursor_position(pygame.mouse.get_pos())
    return var


def controles_selectobject(var, event):
    """
    Occupation des contrôles du menu pour sélectionner les objets.
    """
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_TAB:
            var["menuSelect"] = "editeur"
            var["selectobjectmenu"].change_anim_mode()
    elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            if var["buttons"]["platform"].check_click(event.pos):
                var["selectobjectmenu"].change_select_object_menu("platform")
                var["selectobjectmenu"].reset_page()
                var["editor"].change_type_object("platform")
            elif var["buttons"]["background"].check_click(event.pos):
                var["selectobjectmenu"].change_select_object_menu("background")
                var["selectobjectmenu"].reset_page()
                var["editor"].change_type_object("background")
            elif var["buttons"]["object"].check_click(event.pos):
                var["selectobjectmenu"].change_select_object_menu("object")
                var["selectobjectmenu"].reset_page()
                var["editor"].change_type_object("object")
            elif var["buttons"]["page_left"].check_click(event.pos):
                var["selectobjectmenu"].change_page("left")
            elif var["buttons"]["page_right"].check_click(event.pos):
                var["selectobjectmenu"].change_page("right")
            elif var["buttons"]["color_left"].check_click(event.pos):
                var["editor"].change_color("left")
            elif var["buttons"]["color_right"].check_click(event.pos):
                var["editor"].change_color("right")

            for nb in range(
                var["selectobjectmenu"].get_page_infos()[0],
                var["selectobjectmenu"].get_page_infos()[1]
            ):
                menu = var["editor"].get_type_object()
                try:
                    if var["selectobjectmenu"].get_platform_buttons()[nb][0].check_click(
                        event.pos
                    ) and menu == "platform":
                        if var["selectobjectmenu"].get_platform_buttons()[nb][1] == "platform":
                            var["editor"].change_current_object(nb, "platform")
                            var["selectobjectmenu"].change_select_object(nb)
                            break
                    elif var["selectobjectmenu"].get_background_buttons()[nb][0].check_click(
                        event.pos
                    ) and menu == "background":
                        if var["selectobjectmenu"].get_background_buttons()[nb][1] == "background":
                            var["editor"].change_current_object(nb, "background")
                            var["selectobjectmenu"].change_select_object(nb)
                            break
                    elif var["selectobjectmenu"].get_object_buttons()[nb][0].check_click(
                        event.pos
                    ) and menu == "object":
                        if var["selectobjectmenu"].get_object_buttons()[nb][1] == "object":
                            var["editor"].change_current_object(nb, "object")
                            var["selectobjectmenu"].change_select_object(nb)
                            break
                except IndexError:
                    pass
    return var


def controles_editeur_menu(var, event):
    """
    Occupation des contrôles du menu de l'éditeur.
    """
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            var["menuSelect"] = "editeur"
        if event.key == pygame.K_UP:
            play_sound("menu.wav")
            var["menus"]["editeurmenu"].selection_haut()
        if event.key == pygame.K_DOWN:
            play_sound("menu.wav")
            var["menus"]["editeurmenu"].selection_bas()
        if event.key == pygame.K_RETURN:
            play_sound("menu.wav")
            if var["menus"]["editeurmenu"].menuselection[0] == "continuer":
                var["menuSelect"] = "editeur"
            elif var["menus"]["editeurmenu"].menuselection[0] == "sauvegarder":
                var["editor"].save_data(var["coordinates"])
                var["menuSelect"] = "editeur"
                play_sound("gamesaved.wav")
            elif var["menus"]["editeurmenu"].menuselection[0] == "changer nom salle":
                var["menuSelect"] = "editeurroomname"
            elif var["menus"]["editeurmenu"].menuselection[0] == "retour menu":
                var["checkpoint_position"] = ((433, 568), False)
                var["checkpoint_coordinates"] = [4, 9]
                var["menuSelect"] = "principal"
                var["current_music"] = "menu.ogg"
                var["victory_animation"] = 0
                var["victory"] = False
                var["deaths"] = 0
                var["flips"] = 0
                var["players"]["viridian"].reset_gravity()
                play_music("menu.ogg")
    return var


def controles_editeur_room_name(var, event):
    """
    Occupation des contrôles du menu pour changer le nom de la salle.
    """
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            var["menuSelect"] = "editeur"
        elif event.key == pygame.K_BACKSPACE:
            var["editor"].write_roomname(event.unicode, "backspace")
        else:
            var["editor"].write_roomname(event.unicode, "write")
    return var


def controles(var):
    """
    Occupation de la gestion des contrôles par rapport à leur menu.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            var["jeu_en_cours"] = False

        var = menus_controles[var["menuSelect"]](var, event)
    return var


menus_affichage = {
    "principal": affichage_menu_principal,
    "online": affichage_menu_en_ligne,
    "niveauxediteur": affichage_menu_niveaux_editeur,
    "niveauxjouer": affichage_jouer_niveau,
    "createlevel": affichage_create_level,
    "credits": affichage_menu_credits,
    "histoire": affichage_menu_histoire,
    "jeu": affichage_jeu,
    "victory": affichage_victory,
    "debug": affichage_menu_debug,
    "editeur": affichage_editeur,
    "selectobject": affichage_selectobject,
    "editeurmenu": affichage_editeur_menu,
    "editeurroomname": affichage_editeur_room_name,
    "menujeu": affichage_menu_jeu
}
menus_controles = {
    "principal": controles_principal,
    "online": controles_en_ligne,
    "niveauxediteur": controles_niveaux_editeur,
    "niveauxjouer": controles_niveaux_jouer,
    "createlevel": controles_createlevel,
    "credits": controles_credits,
    "histoire": controles_histoire,
    "jeu": controles_jeu,
    "victory": controles_victory,
    "debug": controles_debug,
    "editeur": controles_editeur,
    "selectobject": controles_selectobject,
    "editeurmenu": controles_editeur_menu,
    "editeurroomname": controles_editeur_room_name,
    "menujeu": controles_menu_jeu
}
