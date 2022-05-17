import pygame

try:
    from constant import couleur, stars, screen_size
    from colors import couleur_jeu
    from functions import charger_ressource, play_sound, play_music, stop_music, check_already_started, map_editor_process, create_map
except ModuleNotFoundError:
    from .constant import couleur, stars, screen_size
    from .colors import couleur_jeu
    from .functions import charger_ressource, play_sound, play_music, stop_music, check_already_started, map_editor_process, create_map


def update_fps(clock):
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
    coordinates_show = var["fonts"]["verylittle_generalfont"].render(str(var["coordinates"]), True, couleur["white"])
    var["editor"].show_cursor(screen)
    var["selectobjectmenu"].draw(screen, var)
    screen.blit(coordinates_show, (screen.get_width() - 155, 10))
    rect = pygame.Rect(0, 720, screen.get_width(), screen.get_height() - 720)
    text = var["fonts"]["little_generalfont"].render(var["editor"].get_roomname(), True, couleur_jeu["cyan"])
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
    text = var["fonts"]["little_generalfont"].render(var["editor"].get_roomname(), True, couleur_jeu["cyan"])
    text_rect = text.get_rect(center=(rect.width // 2, rect.y + 15))
    screen.blit(text, text_rect)
    coordinates_show = var["fonts"]["verylittle_generalfont"].render(str(var["coordinates"]), True, couleur["white"])
    screen.blit(coordinates_show, (screen.get_width() - 155, 10))
    var["selectobjectmenu"].draw(screen, var)
    return var


def affichage_editeur_menu(screen, var):
    """
    Affiche le menu de l'éditeur.
    """
    var["editor"].draw(screen, var)
    coordinates_show = var["fonts"]["verylittle_generalfont"].render(str(var["coordinates"]), True, couleur["white"])
    screen.blit(coordinates_show, (screen.get_width() - 155, 10))
    var["boxes"]["editeurmenu"].draw(screen, (170, 130))
    var["menus"]["editeurmenu"].draw((200, 250), 40)
    rect = pygame.Rect(0, 720, screen.get_width(), screen.get_height() - 720)
    text = var["fonts"]["little_generalfont"].render(var["editor"].get_roomname(), True, couleur_jeu["cyan"])
    text_rect = text.get_rect(center=(rect.width // 2, rect.y + 15))
    screen.blit(text, text_rect)
    return var


def affichage_editeur_room_name(screen, var):
    """
    Affiche le menu pour changer le nom d'une salle.
    """
    screen.fill(couleur["black"])
    var["editor"].draw(screen, var)
    coordinates_show = var["fonts"]["verylittle_generalfont"].render(str(var["coordinates"]), True, couleur["white"])
    screen.blit(coordinates_show, (screen.get_width() - 155, 10))
    rect = pygame.Rect(0, 720, screen.get_width(), screen.get_height() - 720)
    text = var["fonts"]["little_generalfont"].render(var["editor"].get_roomname(), True, couleur_jeu["cyan"])
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


def affichage_menu_histoire(screen, var):
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
    screen.fill(couleur["black"])
    stars.draw(screen)
    var = var["room"].draw(screen, var)
    var["room"].conveyors_animations(screen, var)
    var["room"].draw_checkpoint(screen, var)
    var["players"]["viridian"].update_platforms(var["room"].get_rects())
    var["players"]["viridian"].draw(screen, var)
    var["players"]["viridian"].update(var)
    var["room"].draw_roomname(screen, var)
    if var["collisions_show"]:
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
    return var


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
    if var["menuSelect"] == "principal":
        var = affichage_menu_principal(screen, var)
    elif var["menuSelect"] == "credits":
        var = affichage_menu_credits(screen, var)
    elif var["menuSelect"] == "histoire":
        var = affichage_menu_histoire(screen, var)
    elif var["menuSelect"] == "jeu":
        var = affichage_jeu(screen, var)
    elif var["menuSelect"] == "debug":
        var = affichage_menu_debug(screen, var)
    elif var["menuSelect"] == "editeur":
        var = affichage_editeur(screen, var)
    elif var["menuSelect"] == "selectobject":
        var = affichage_selectobject(screen, var)
    elif var["menuSelect"] == "editeurmenu":
        var = affichage_editeur_menu(screen, var)
    elif var["menuSelect"] == "editeurroomname":
        var = affichage_editeur_room_name(screen, var)
    elif var["menuSelect"] == "menujeu":
        var = affichage_menu_jeu(screen, var)

    if var["debug"]:
        font = pygame.font.SysFont("Arial", 18)
        screen.blit(update_fps(clock), (10,0))
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
                    var["room"].play_music(var)
                    var["room"].change_room(var["coordinates"], var)
                    var["players"]["viridian"].update_positions([433, 568])
            if var["menus"]["principal"].menuselection[0] == "en ligne":
                var["menuSelect"] = "online mode"
            if var["menus"]["principal"].menuselection[0] == "debug":
                var["menuSelect"] = "debug"
            if var["menus"]["principal"].menuselection[0] == "crédits":
                var["menuSelect"] = "credits"
            if var["menus"]["principal"].menuselection[0] == "quitter":
                var["jeu_en_cours"] = False
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
        if event.key == pygame.K_ESCAPE:
            play_sound("menu.wav")
            var["menuSelect"] = "menujeu"
        elif event.key == pygame.K_SPACE:
            if var["dead"] is False:
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
                var["menuSelect"] = "jeu"
            elif var["menus"]["menujeu"].menuselection[0] == "retour menu":
                play_sound("menu.wav")
                var["checkpoint_position"] = ((433, 568), False)
                var["checkpoint_coordinates"] = [4, 9]
                var["menuSelect"] = "principal"
                var["current_music"] = "menu.ogg"
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
                data = map_editor_process(var["currentMap"], var["coordinates"])
                var["editor"].change_room(var["coordinates"], var)
            elif var["coordinates"][0] == -25:
                var["coordinates"][0] += 1
                data = map_editor_process(var["currentMap"], var["coordinates"])
                var["editor"].change_room(var["coordinates"], var)
        elif event.key == pygame.K_LEFT:
            if var["coordinates"][0] > -25 and var["coordinates"][0] < 25:
                var["coordinates"][0] -= 1
                data = map_editor_process(var["currentMap"], var["coordinates"])
                var["editor"].change_room(var["coordinates"], var)
            elif var["coordinates"][0] == 25:
                var["coordinates"][0] -= 1
                data = map_editor_process(var["currentMap"], var["coordinates"])
                var["editor"].change_room(var["coordinates"], var)
        elif event.key == pygame.K_UP:
            if var["coordinates"][1] < 25 and var["coordinates"][1] > -25:
                var["coordinates"][1] += 1
                data = map_editor_process(var["currentMap"], var["coordinates"])
                var["editor"].change_room(var["coordinates"], var)
            elif var["coordinates"][1] == -25:
                var["coordinates"][1] += 1
                data = map_editor_process(var["currentMap"], var["coordinates"])
                var["editor"].change_room(var["coordinates"], var)
        elif event.key == pygame.K_DOWN:
            if var["coordinates"][1] > -25 and var["coordinates"][1] < 25:
                var["coordinates"][1] -= 1
                data = map_editor_process(var["currentMap"], var["coordinates"])
                var["editor"].change_room(var["coordinates"], var)
            elif var["coordinates"][1] == 25:
                var["coordinates"][1] -= 1
                data = map_editor_process(var["currentMap"], var["coordinates"])
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

            for counter in range(var["selectobjectmenu"].get_page_infos()[0], var["selectobjectmenu"].get_page_infos()[1]):
                menu = var["editor"].get_type_object()
                try:
                    if var["selectobjectmenu"].get_platform_buttons()[counter][0].check_click(event.pos) and menu == "platform":
                        if var["selectobjectmenu"].get_platform_buttons()[counter][1] == "platform":
                            var["editor"].change_current_object(counter, "platform")
                            var["selectobjectmenu"].change_select_object(counter)
                            break
                    elif var["selectobjectmenu"].get_background_buttons()[counter][0].check_click(event.pos) and menu == "background":
                        if var["selectobjectmenu"].get_background_buttons()[counter][1] == "background":
                            var["editor"].change_current_object(counter, "background")
                            var["selectobjectmenu"].change_select_object(counter)
                            break
                    elif var["selectobjectmenu"].get_object_buttons()[counter][0].check_click(event.pos) and menu == "object":
                        if var["selectobjectmenu"].get_object_buttons()[counter][1] == "object":
                            var["editor"].change_current_object(counter, "object")
                            var["selectobjectmenu"].change_select_object(counter)
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
                var["menuSelect"] = "principal"
                var["current_music"] = "menu"
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

        elif var["menuSelect"] == "principal":
            var = controles_principal(var, event)
        elif var["menuSelect"] == "histoire":
            var = controles_histoire(var, event)
        elif var["menuSelect"] == "jeu":
            var = controles_jeu(var, event)
        elif var["menuSelect"] == "credits":
            var = controles_credits(var, event)
        elif var["menuSelect"] == "debug":
            var = controles_debug(var, event)
        elif var["menuSelect"] == "editeur":
            var = controles_editeur(var, event)
        elif var["menuSelect"] == "selectobject":
            var = controles_selectobject(var, event)
        elif var["menuSelect"] == "editeurmenu":
            var = controles_editeur_menu(var, event)
        elif var["menuSelect"] == "editeurroomname":
            var = controles_editeur_room_name(var, event)
        elif var["menuSelect"] == "menujeu":
            var = controles_menu_jeu(var, event)
    return var