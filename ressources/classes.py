import json
import pygame, random, math

from ressources.functions import play_sound

try:
    from functions import crop, convert_PIL_to_pygame, apply_color, get_screen_size, play_music, stop_music
    from colors import couleur_jeu, couleur_joueurs
except ModuleNotFoundError:
    from .functions import crop, convert_PIL_to_pygame, apply_color, get_screen_size, play_music, stop_music
    from .colors import couleur_jeu, couleur_joueurs


class ImageButton:
    def __init__(self, image, size, color):
        self.image = pygame.transform.scale(image, (size[0] / 2, size[1] / 2))
        self.surface = pygame.Surface(size)
        self.rect = self.surface.get_rect()
        self.color = color
        self.background = couleur_jeu["background"]
        self.imagerect = self.image.get_rect(center = self.rect.center)
        self.collision_rect = pygame.Rect(0, 0, size[0], size[1])

    def check_click(self, pos):
        if self.collision_rect.collidepoint(pos):
            return True
        return False

    def get_collision_rect(self):
        return self.collision_rect

    def draw(self, screen, position):
        self.surface.fill(self.background)
        self.surface.blit(self.image, self.imagerect)
        pygame.draw.rect(self.surface, self.color, self.rect, 3)
        self.collision_rect.x, self.collision_rect.y = position[0], position[1]
        screen.blit(self.surface, position)

    def change_color(self, color):
        self.color = color

    def change_background(self, color):
        self.background = color

class Box:
    def __init__(self, rect, color):
        self.rect = rect
        self.color = color
        self.surface = pygame.Surface(self.rect)

    def draw(self, screen, position):
        self.surface.fill(couleur_jeu["background"])
        pygame.draw.rect(self.surface, self.color, (0, 0, self.rect[0], self.rect[1]), 5)
        screen.blit(self.surface, position)

    def get_surface(self):
        return pygame.Surface(self.rect, pygame.SRCALPHA)


class Player:
    def __init__(self, player):
        self.player_name = player
        self.gravity = "bottom"
        self.direction = pygame.math.Vector2(433, 568)
        self.hitbox = pygame.Rect(self.direction.x, self.direction.y, 30, 62)
        self.speed = 12
        self.directions = {"left": False, "right": True,  "up": False, "down": True}
        self.player_sprites_dict = []
        self.platforms = []
        self.emotion = "happy"
        self.walk_animation_counter = 0
        self.walk_animation_type = "normal"
        self.player_sprites_indexes = {
            "happy_down_left": 0,
            "happy_down_right": 1,
            "happy_up_left": 2,
            "happy_up_right": 3,
            "sad_down_left": 4,
            "sad_down_right": 5,
            "sad_up_left": 6,
            "sad_up_right": 7,
        }
        self.player_sprites_moving_indexes = {
            "happy_down_left": 0,
            "happy_down_right": 1,
            "happy_up_left": 2,
            "happy_up_right": 3,
            "sad_down_left": 4,
            "sad_down_right": 5,
            "sad_up_left": 6,
            "sad_up_right": 7,
        }
        player_sprites = crop("./ressources/sprites/player.png", 63, 30)
        player_sprite_moving = crop("./ressources/sprites/player_moving.png", 63, 36, (38, 65))
        for index in range(len(player_sprites)):
            self.player_sprites_dict.append([
                player_sprites[index],
                player_sprite_moving[index]
            ])

    def walk_animation(self, var):
        if var["left"]:
            self.walk_animation_counter += 2
            if self.walk_animation_type == "normal" and self.walk_animation_counter == 20:
                self.walk_animation_type = "moving"
                self.walk_animation_counter = 0
            elif self.walk_animation_type == "moving" and self.walk_animation_counter == 20:
                self.walk_animation_type = "normal"
                self.walk_animation_counter = 0
        elif var["right"]:
            self.walk_animation_counter += 2
            if self.walk_animation_type == "normal" and self.walk_animation_counter == 20:
                self.walk_animation_type = "moving"
                self.walk_animation_counter = 0
            elif self.walk_animation_type == "moving" and self.walk_animation_counter == 20:
                self.walk_animation_type = "normal"
                self.walk_animation_counter = 0
        else:
            self.walk_animation_counter = 0
            self.walk_animation_type = "normal"

    def get_index(self):
        if self.emotion == "happy":
            if self.directions["up"]:
                if self.directions["left"]:
                    return self.player_sprites_indexes["happy_up_right"]
                return self.player_sprites_indexes["happy_up_left"]
            if self.directions["left"]:
                return self.player_sprites_indexes["happy_down_right"]
            return self.player_sprites_indexes["happy_down_left"]
        if self.directions["up"]:
            if self.directions["left"]:
                return self.player_sprites_indexes["sad_up_right"]
            return self.player_sprites_indexes["sad_up_left"]
        if self.directions["left"]:
            return self.player_sprites_indexes["sad_down_right"]
        return self.player_sprites_indexes["sad_down_left"]

    def get_specific_sprite(self):
        index = self.get_index()
        object = colored_players[self.player_name][self.walk_animation_type][index]
        return convert_PIL_to_pygame(object)

    def get_sprites(self):
        return self.player_sprites_dict

    def update_platforms(self, platforms):
        self.platforms = platforms

    def change_gravity(self):
        for platform in self.platforms:
            if self.hitbox.colliderect(platform.x, platform.y - 12, platform.width, platform.height):
                if self.gravity == "bottom":
                    play_sound("jump.wav")
                    self.gravity_enabled = True
                    self.directions["up"] = True
                    self.directions["down"] = False
                    self.gravity = "top"
                    self.direction.y -= self.speed
                    self.hitbox.y -= self.speed
                    break
            elif self.hitbox.colliderect(platform.x, platform.y + 12, platform.width, platform.height):
                if self.gravity == "top":
                    play_sound("jump2.wav")
                    self.gravity_enabled = True
                    self.gravity = "bottom"
                    self.directions["up"] = False
                    self.directions["down"] = True
                    self.direction.y += self.speed
                    self.hitbox.y += self.speed
                    break

    def apply_gravity(self):
        if self.gravity == "bottom":
            self.direction.y += self.speed
            self.hitbox.y += self.speed
        if self.gravity == "top":
            self.direction.y -= self.speed
            self.hitbox.y -= self.speed

    def move(self, direction):
        if direction == "left":
            self.direction.x -= (self.speed - 5)
            self.hitbox.x -= (self.speed - 5)
            self.directions["left"] = True
            self.directions["right"] = False
        if direction == "right":
            self.direction.x += (self.speed - 5)
            self.hitbox.x += (self.speed - 5)
            self.directions["left"] = False
            self.directions["right"] = True

    def update(self, var):
        self.walk_animation(var)
        if var["left"]:
            self.move("left")
        if var["right"]:
            self.move("right")
        for platform in self.platforms:
            if self.hitbox.colliderect(platform):
                if var["right"]:
                    self.hitbox.right = platform.left
                    self.direction.x = self.hitbox.x
                    break
                elif var["left"]:
                    self.hitbox.left = platform.right
                    self.direction.x = self.hitbox.x
                    break
        for platform in self.platforms:
            if self.hitbox.colliderect(platform.x, platform.y - 12, platform.width, platform.height):
                if self.gravity == "bottom":
                    self.hitbox.bottom = platform.top - 12
                    self.direction.y = self.hitbox.y
            elif self.hitbox.colliderect(platform.x, platform.y + 12, platform.width, platform.height):
                if self.gravity == "top":
                    self.hitbox.top = platform.bottom + 12
                    self.direction.y = self.hitbox.y
        self.apply_gravity()
        if self.hitbox.topleft[0] < -self.hitbox.width + 10:
            self.direction.x = get_screen_size()[0] - self.hitbox.width
            self.hitbox.x = get_screen_size()[0] - self.hitbox.width
            var["coordinates"][0] -= 1
            var["room"].change_room(var["coordinates"], var)
        elif self.hitbox.topright[0] > get_screen_size()[0] + self.hitbox.width - 10:
            self.direction.x = 1
            self.hitbox.x = 1
            var["coordinates"][0] += 1
            var["room"].change_room(var["coordinates"], var)
        elif self.hitbox.bottom > 720 + self.hitbox.height - 10:
            self.direction.y = -self.hitbox.height
            self.hitbox.y = -self.hitbox.height
            var["coordinates"][1] -= 1
            var["room"].change_room(var["coordinates"], var)
        elif self.hitbox.top < -self.hitbox.height + 10:
            self.direction.y = 720 - self.hitbox.height
            self.hitbox.y = 720 - self.hitbox.height
            var["coordinates"][1] += 1
            var["room"].change_room(var["coordinates"], var)


    def draw(self, screen, var):
        if var["collisions_show"]:
            pygame.draw.rect(screen, couleur_jeu["red"], self.hitbox)
        screen.blit(self.get_specific_sprite(), self.direction)


class Object:
    def __init__(self):
        self.alltiles = []
        self.objects = []
        self.tiles1 = crop("./ressources/sprites/tiles_backup.png", 32, 32, (30, 30))
        self.background = crop("./ressources/sprites/backgrounds.png", 32, 32, (30, 30))
        self.spikes = crop("./ressources/sprites/spikes.png", 32, 32, (30, 30))
        for i in self.tiles1:
            self.alltiles.append(i)
        for i in self.background:
            self.alltiles.append(i)
        for i in self.spikes:
            self.alltiles.append(i)
            self.objects.append(i)

    def draw_specific_grayscale_tile(self, surface, position, color, type, tile):
        object = convert_PIL_to_pygame(colored_textures[color][type][tile])
        surface.blit(object, position)
    
    def get_tiles(self):
        return self.alltiles

    def get_all_objects(self):
        return self.objects

    def get_all_spikes(self):
        return self.spikes

    def get_all_platforms(self):
        return self.tiles1

    def get_all_backgrounds(self):
        return self.background

    def get_specific_tiles(self, tiles):
        return self.alltiles[tiles]


class ColoredTextures:
    def __init__(self, object):
        self.texture_colored = {}
        platforms = object.get_all_platforms()
        backgrounds = object.get_all_backgrounds()
        objects = object.get_all_objects()
        for couleur in couleur_jeu:
            self.texture_colored[couleur] = {}
            self.texture_colored[couleur]["platform"] = {}
            self.texture_colored[couleur]["background"] = {}
            self.texture_colored[couleur]["object"] = {}
            for count in range(len(platforms)):
                self.texture_colored[couleur]["platform"][count] = apply_color(platforms[count], couleur_jeu[couleur])
            for count in range(len(backgrounds)):
                self.texture_colored[couleur]["background"][count] = apply_color(backgrounds[count], couleur_jeu[couleur])
            for count in range(len(objects)):
                self.texture_colored[couleur]["object"][count] = apply_color(objects[count], couleur_jeu[couleur])

    def get_colored_textures(self):
        return self.texture_colored


class ColoredPlayers:
    def __init__(self, object):
        self.players_colored = {}
        for player in couleur_joueurs.keys():
            self.players_colored[player] = {}
            self.players_colored[player]["normal"] = []
            self.players_colored[player]["moving"] = []
            for sprites in object:
                self.players_colored[player]["normal"].append(apply_color(sprites[0], couleur_joueurs[player]))
                self.players_colored[player]["moving"].append(apply_color(sprites[1], couleur_joueurs[player]))
    
    def get_colored_players(self):
        return self.players_colored


colored_textures = ColoredTextures(Object()).get_colored_textures()
colored_players = ColoredPlayers(Player(None).get_sprites()).get_colored_players()


class DownParallax:
    """
    Permet de créer un parallax en bas.
    """
    def __init__(self, screen, image, speed):
        self.screen = screen
        self.image = image
        self.speed = speed
        self.rect = self.image.get_rect()

    def draw(self):
        self.rect.y -= self.speed
        if self.rect.y < (-self.rect.height + self.screen.get_height()):
            self.rect.y = 0
        self.screen.blit(self.image, self.rect)


class UpParallax:
    """
    Permet de créer un parallax en haut.
    """
    def __init__(self, screen, image, speed):
        self.screen = screen
        self.image = image
        self.speed = speed
        self.rect = self.image.get_rect()

    def draw(self):
        self.rect.y += self.speed
        if self.rect.y > 0:
            self.rect.y = -self.rect.height + self.screen.get_height()
        self.screen.blit(self.image, self.rect)


class MenuSelector:
    def __init__(self, screen, menulist):
        # [["start", couleur["cyan"], font["little_generalfont"]], ["quit", couleur["cyan"], font["little_generalfont"]]]
        self.screen = screen
        self.menulist = []
        for i in menulist:
            if i is not None:
                self.menulist.append(i)
        self.menuselection = [i[0] for i in self.menulist]

    def draw(self, position, space):
        const_y = 0
        for i in self.menulist:
            if i[0] == self.menuselection[0]:
                text = i[2].render(
                    "[ "+i[0].upper()+" ]",
                    True,
                    i[1]
                )
                self.screen.blit(text, (position[0], position[1] + const_y))
            else:
                text = i[2].render(
                    i[0],
                    True,
                    i[1]
                )
                self.screen.blit(text, (position[0], position[1] + const_y))
            const_y += space

    def selection_bas(self):
        """
        Permet de changer sélection de gauche à droite.
        """
        test = self.menuselection.copy()
        test.append(test.pop(0))
        self.menuselection = test

    def selection_haut(self):
        """
        Permet de changer sélection de droite à gauche.
        """
        test = self.menuselection.copy()
        value = test.pop(-1)
        test.insert(0, value)
        self.menuselection = test


class Room:
    def __init__(self, map_name, coordinates):
        self.x_position = 0
        self.y_position = 0
        self.map_name = map_name
        self.object = Object()
        try:
            with open(f"./ressources/maps/{map_name}/{coordinates}.vvvvvv", "r") as f:
                self.data = json.load(f)
            f.close()
        except json.decoder.JSONDecodeError:
            self.data = None
        except FileNotFoundError:
            self.data = None

    def change_room(self, coordinates, var):
        try:
            with open(f"./ressources/maps/{self.map_name}/{coordinates}.vvvvvv", "r") as f:
                self.data = json.load(f)
            f.close()
        except json.decoder.JSONDecodeError:
            self.data = None
        except FileNotFoundError:
            self.data = None
        try:
            if var["current_music"] != self.data["music"]:
                var["current_music"] = self.data["music"]
                play_music(f"{var['current_music']}.ogg")
        except TypeError:
            if var["current_music"] != "presenting_vvvvvv":
                var["current_music"] = "presenting_vvvvvv"
                play_music(f"presenting_vvvvvv.ogg")
        return var


    def get_rects(self):
        rects = []
        position_x = 0
        position_y = 0
        try:
            for y_values in self.data["map_data"]:
                for values in y_values:
                    try:
                        if values["platform"] is not None:
                            rects.append(pygame.Rect(position_x, position_y, 30, 30))
                    except KeyError:
                        pass
                    position_x += 30
                position_y += 30
                position_x = 0
        except TypeError:
            pass
        return rects

    def update_data(self, x, y, type, data=None, order=None):
        if order == "place":
            try:
                self.data["map_data"][x][y][type] = data[0]
                self.data["map_data"][x][y]["color"] = data[1]
            except IndexError:
                pass
        elif order == "remove":
            try:
                self.data["map_data"][x][y] = {}
            except KeyError:
                pass
        else:
            self.data["map_data"][x][y] = {}


    def save_data(self, coordinates):
        with open(f"./ressources/maps/{self.map_name}/{coordinates}.vvvvvv", "w") as f:
            json.dump(self.data, f)
        f.close()


    def reset_position(self):
        self.x_position = 0
        self.y_position = 0

    def draw(self, screen):
        surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        try:
            for y_values in self.data["map_data"]:
                for values in y_values:
                    try:
                        color  = values["color"]
                    except KeyError:
                        pass

                    try:
                        if values["platform"] is not None:
                            self.object.draw_specific_grayscale_tile(surface, (self.x_position * 30, self.y_position * 30), color, "platform", values["platform"])
                    except KeyError:
                        pass
                    try:
                        if values["background"] is not None:
                            self.object.draw_specific_grayscale_tile(surface, (self.x_position * 30, self.y_position * 30), color, "background", values["background"])
                    except KeyError:
                        pass
                    try:
                        if values["object"] is not None:
                            self.object.draw_specific_grayscale_tile(surface, (self.x_position * 30, self.y_position * 30), color, "object", values["object"])
                    except KeyError:
                        pass
                    self.x_position += 1
                self.y_position += 1
                self.x_position = 0
            screen.blit(surface, (0, 0))
            self.reset_position()
        except TypeError:
            pass

    def draw_roomname(self, screen, var, customtext=None):
        rect = pygame.Rect(0, 720, screen.get_width(), screen.get_height() - 720)
        pygame.draw.rect(screen, couleur_jeu["black"], rect)
        try:
            if customtext is None:
                try:
                    text = var["fonts"]["little_generalfont"].render(self.data["roomname"], True, couleur_jeu["cyan"])
                    screen.blit(text, text.get_rect(center = (rect.width // 2, rect.y + 15)))
                except KeyError:
                    pass
            else:
                text = var["fonts"]["little_generalfont"].render(customtext, True, couleur_jeu["red"])
                screen.blit(text, text.get_rect(center = (rect.width // 2, rect.y + 15)))
        except TypeError:
            text = var["fonts"]["little_generalfont"].render("This room is empty.", True, couleur_jeu["red"])
            screen.blit(text, text.get_rect(center = (rect.width // 2, rect.y + 15)))

    def play_music(self, var):
        try:
            if self.data["music"] is not None:
                if var["current_music"] != self.data["music"]:
                    var["current_music"] = self.data["music"]
                    stop_music()
                    play_music(f"{var['current_music']}.ogg")
        except TypeError:
            if var["current_music"] != "presenting_vvvvvv":
                var["current_music"] = "presenting_vvvvvv"
                stop_music()
                play_music(f"presenting_vvvvvv.ogg")


class Editor:
    def __init__(self, screen_size, map_name, coordinates):
        self.map = Room(map_name, coordinates)
        self.box_size = 30
        self.screen_size = screen_size
        self.cursor_rect_position = pygame.Rect(0, 0, 0, 0)
        self.object_selected = 0
        self.colors = [color for color in couleur_jeu.keys()]
        self.object_type = "platform"

    def update_mapdata(self, map_name, coordinates):
        self.map = Room(map_name, coordinates)

    def change_room(self, coordinates, var):
        self.map.change_room(coordinates, var)
        return var

    def draw(self, screen):
        self.map.draw(screen)
 
    def cursor_position(self, mouse_position):
        for i in range((self.screen_size[0] // self.box_size) + 1):
            for j in range((self.screen_size[1] // self.box_size) + 1):
                if mouse_position[0] >= (i*self.box_size) - self.box_size and mouse_position[0] <= i*self.box_size:
                    if mouse_position[1] >= (j*self.box_size) - self.box_size and mouse_position[1] <= j*self.box_size:
                        if (i-1)*self.box_size >= 0 and (j-1)*self.box_size >= 0:
                            self.cursor_rect_position = pygame.Rect((i-1)*self.box_size, (j-1)*self.box_size, self.box_size, self.box_size)
                            return self.cursor_rect_position

    def show_cursor(self, screen):
        pygame.draw.rect(screen, couleur_jeu["white"], self.cursor_rect_position, 2)

    def remove_object(self):
        for i in range((self.screen_size[0] // self.box_size) + 1):
            for j in range((self.screen_size[1] // self.box_size) + 1):
                if i*self.box_size == self.cursor_rect_position.x and j*self.box_size == self.cursor_rect_position.y:
                    self.map.update_data(j, i, type=self.object_type, order="remove")
            

    def place_object(self):
        for i in range((self.screen_size[0] // self.box_size) + 1):
            for j in range((self.screen_size[1] // self.box_size) + 1):
                if i*self.box_size == self.cursor_rect_position.x and j*self.box_size == self.cursor_rect_position.y:
                    self.map.update_data(j, i, self.object_type, data=[self.object_selected, self.colors[0]], order="place")

    def change_current_object(self, object_selected):
        self.object_selected = object_selected


    def change_type_object(self, object_type):
        self.object_type = object_type


    def save_data(self, coordinates):
        self.map.save_data(coordinates)


    def get_color_selected(self):
        return self.colors[0]


    def change_color(self, color_selected):
        if color_selected == "right":
            test = self.colors.copy()
            test.append(test.pop(0))
            self.colors = test
        elif color_selected == "left":
            test = self.colors.copy()
            value = test.pop(-1)
            test.insert(0, value)
            self.colors = test

class SelectObjectMenu:
    def __init__(self):
        self.object = Object()
        self.x_position = 20
        self.y_position = 100
        self.select_box_y = 0
        self.select_object_menu = "platform"
        self.select_object = 0
        self.counter_anim = 0
        self.anim_mode = None
        self.all_platform_buttons = []
        self.all_backgrounds_buttons = []
        self.all_object_buttons = []
        self.select_menus = ["platform", "background", "object"]
        self.page_platform = 0
        self.page_background = 0
        self.page_object = 0
        for platform in self.object.get_all_platforms():
            self.all_platform_buttons.append([ImageButton(convert_PIL_to_pygame(platform), (57, 57), couleur_jeu["background"]), "platform"])
        for background in self.object.get_all_backgrounds():
            self.all_backgrounds_buttons.append([ImageButton(convert_PIL_to_pygame(background), (57, 57), couleur_jeu["background"]), "background"])
        for object in self.object.get_all_objects():
            self.all_object_buttons.append([ImageButton(convert_PIL_to_pygame(object), (57, 57), couleur_jeu["background"]), "object"])

    def exponential_anim(self):
        counter = self.counter_anim * 0.1005
        if (counter < 1):
            self.select_box_y = 0.5 * math.pow(2, 10 * (counter - 1))
        else:
            self.select_box_y = 0.5 * (-math.pow(2, -10 * (counter - 1)) + 2)
        if self.anim_mode == "up":
            self.counter_anim += 1
        elif self.anim_mode == "down":
            self.counter_anim -= 1

    def draw(self, screen, var):
        self.exponential_anim()
        surface = var["boxes"]["selector"].get_surface()
        var["boxes"]["selector"].draw(screen,  (20, get_screen_size()[1] - (300 * self.select_box_y)))
        if self.select_object_menu == "platform":
            if self.page_platform > 0:
                var["buttons"]["page_left"].draw(screen, (230, get_screen_size()[1] - (130 * self.select_box_y)))
            if self.page_platform < len(self.object.get_all_platforms()) // 32:
                var["buttons"]["page_right"].draw(screen, (897, get_screen_size()[1] - (130 * self.select_box_y)))
        elif self.select_object_menu == "background":
            if self.page_background > 0:
                var["buttons"]["page_left"].draw(screen, (230, get_screen_size()[1] - (130 * self.select_box_y)))
            if self.page_background < len(self.object.get_all_backgrounds()) // 32:
                var["buttons"]["page_right"].draw(screen, (897, get_screen_size()[1] - (130 * self.select_box_y)))
        elif self.select_object_menu == "object":
            if self.page_background > 0:
                var["buttons"]["page_left"].draw(screen, (230, get_screen_size()[1] - (130 * self.select_box_y)))
            if self.page_background < len(self.object.get_all_backgrounds()) // 32:
                var["buttons"]["page_right"].draw(screen, (897, get_screen_size()[1] - (130 * self.select_box_y)))
        var["buttons"]["color_left"].draw(screen, (40, get_screen_size()[1] - (60 * self.select_box_y)))
        var["buttons"]["color_right"].draw(screen, (170, get_screen_size()[1] - (60 * self.select_box_y)))
        screen.blit(var["texts"]["color"], (40, get_screen_size()[1] - (100 * self.select_box_y)))
        pygame.draw.rect(screen, couleur_jeu[var["editor"].get_color_selected()], (100, get_screen_size()[1] - (65 * self.select_box_y), 50, 50))
        pygame.draw.line(
            screen,
            couleur_jeu["blurple"],
            (20, get_screen_size()[1] - (120 * self.select_box_y)),
            (230, get_screen_size()[1] - (120 * self.select_box_y)),
            1
        )
        pygame.draw.line(
            screen,
            couleur_jeu["blurple"],
            (230, get_screen_size()[1] - (300 * self.select_box_y)),
            (230, get_screen_size()[1]),
            1
        )
        pygame.draw.line(
            screen,
            couleur_jeu["blurple"],
            (230, get_screen_size()[1] - (210    * self.select_box_y)),
            (get_screen_size()[0] - 22, get_screen_size()[1] - (210 * self.select_box_y)),
            1
        )
        x_position = 270
        y_position = get_screen_size()[1] - (193 * self.select_box_y)
        id_platform = 0 if self.page_platform == 0 else self.page_platform * 33
        id_background = 0 if self.page_background == 0 else self.page_background * 33
        id_object = 0 if self.page_object == 0 else self.page_object * 33
        for i in self.select_menus:
            try:
                if self.select_object_menu == i:
                    var["buttons"][i].change_color(couleur_jeu["cyan"])
                    if self.select_object_menu == "platform":
                        self.page_start = self.page_platform * 33
                        self.page_end = (self.page_platform + 1) * 33
                        for counter in range(self.page_start, self.page_end):
                            if self.all_platform_buttons[counter][1] == i:
                                if x_position >= surface.get_width() - 40:
                                    x_position = 270
                                    y_position += 57
                                if self.select_object == id_platform:
                                    self.all_platform_buttons[counter][0].change_color(couleur_jeu["cyan"])
                                else:
                                    self.all_platform_buttons[counter][0].change_color(couleur_jeu["background"])
                                self.all_platform_buttons[counter][0].draw(screen, (x_position, y_position))
                                x_position += 57
                                id_platform += 1
                    elif self.select_object_menu == "background":
                        self.page_start = self.page_background * 33
                        self.page_end = (self.page_background + 1) * 33
                        for counter in range(self.page_start, self.page_end):
                            if self.all_backgrounds_buttons[counter][1] == i:
                                if x_position >= surface.get_width() - 40:
                                    x_position = 270
                                    y_position += 57
                                if self.select_object == id_background:
                                    self.all_backgrounds_buttons[counter][0].change_color(couleur_jeu["cyan"])
                                else:
                                    self.all_backgrounds_buttons[counter][0].change_color(couleur_jeu["background"])
                                self.all_backgrounds_buttons[counter][0].draw(screen, (x_position, y_position))
                                x_position += 57
                                id_background += 1
                    elif self.select_object_menu == "object":
                        self.page_start = self.page_object * 33
                        self.page_end = (self.page_object + 1) * 33
                        for counter in range(self.page_start, self.page_end):
                            if self.all_object_buttons[counter][1] == i:
                                if x_position >= surface.get_width() - 40:
                                    x_position = 270
                                    y_position += 57
                                if self.select_object == id_object:
                                    self.all_object_buttons[counter][0].change_color(couleur_jeu["cyan"])
                                else:
                                    self.all_object_buttons[counter][0].change_color(couleur_jeu["background"])
                                self.all_object_buttons[counter][0].draw(screen, (x_position, y_position))
                                x_position += 57
                                id_object += 1
                else:
                    var["buttons"][i].change_color(couleur_jeu["blurple"])
            except IndexError:
                pass

        var["buttons"]["platform"].draw(screen, (250, get_screen_size()[1] - (283 * self.select_box_y)))
        var["buttons"]["background"].draw(screen, (330, get_screen_size()[1] - (283 * self.select_box_y)))
        var["buttons"]["object"].draw(screen, (410, get_screen_size()[1] - (283 * self.select_box_y)))
        self.reset_position()
        screen.blit(surface, (20, get_screen_size()[1] - (300 * self.select_box_y)))

    def change_anim_mode(self):
        if self.anim_mode == "up":
            self.anim_mode = "down"
            self.counter_anim = 20
        else:
            self.anim_mode = "up"
            self.counter_anim = 0

    def reset_position(self):
        self.x_position = 20
        self.y_position = 100

    def reset_page(self):
        self.page_platform = 0
        self.page_background = 0
        self.page_object = 0

    def change_select_object_menu(self, select_object_menu):
        self.select_object_menu = select_object_menu

    def change_select_object(self, object_id):
        self.select_object = object_id

    def change_page(self, page):
        if page == "left":
            if self.select_object_menu == "platform":
                if self.page_platform > 0:
                    self.page_platform -= 1
            elif self.select_object_menu == "background":
                if self.page_background > 0:
                    self.page_background -= 1
            elif self.select_object_menu == "object":
                if self.page_object > 0:
                    self.page_object -= 1
        elif page == "right":
            if self.select_object_menu == "platform":
                if self.page_platform < len(self.object.get_all_platforms()) // 32:
                    self.page_platform += 1
            elif self.select_object_menu == "background":
                if self.page_background < len(self.object.get_all_backgrounds()) // 32:
                    self.page_background += 1
            elif self.select_object_menu == "object":
                if self.page_object < len(self.object.get_all_objects()) // 32:
                    self.page_object += 1

    def get_platform_buttons(self):
        return self.all_platform_buttons

    def get_background_buttons(self):
        return self.all_backgrounds_buttons

    def get_object_buttons(self):
        return self.all_object_buttons

    def get_object_menu(self):
        return self.select_object_menu

    def get_page_infos(self):
        return self.page_start, self.page_end

    def get_page_number(self):
        return self.page_platform, self.page_background


class BGStars:
    def __init__(self, starRate, starSpeed):
        self.stars = []
        self.starTime = 0
        self.starRate = starRate
        self.starSpeed = starSpeed

    def grey(self, val):
        return val, val, val

    def draw(self, screen):
        if self.starTime >= self.starRate:
            self.starTime = 0
            self.stars.append([screen.get_width() + 5, random.randint(0, screen.get_height() - 32), random.randint(0, 50)])

        for (st, s) in enumerate(self.stars):
            pygame.draw.rect(screen, self.grey(255 - (s[2] * 5)), (s[0], s[1], 5, 5), 0)
            s[0] -= self.starSpeed - round(s[2] / 5)
            if s[0] < 0:
                del self.stars[st]
        self.starTime += 1