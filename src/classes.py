import json
import pygame
import random
import math

try:
    from functions import crop, convert_PIL_to_pygame, apply_color, get_screen_size, play_music
    from functions import stop_music, play_sound, read_room_data, write_room_data, empty_room
    from functions import create_data_room
    from colors import couleur_jeu, couleur_joueurs
except ModuleNotFoundError:
    from .functions import crop, convert_PIL_to_pygame, apply_color, get_screen_size, play_music
    from .functions import stop_music, play_sound, read_room_data, write_room_data, empty_room
    from .functions import create_data_room
    from .colors import couleur_jeu, couleur_joueurs


class Clock:
    """
    Classe qui gère le temps.
    """
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.time = 0
        self.delta_time = 0
        self.last_time = 0
        self.stop = False

    def tick(self):
        if self.stop is False:
            self.delta_time = self.clock.tick(self.fps)
            self.time += self.delta_time

    def get_time(self):
        self.last_time = self.time

    def stop_clock(self):
        self.stop = True

    def start_clock(self):
        self.stop = False

    def reset(self):
        self.time = 0
        self.last_time = 0
        self.delta_time = 0
        self.clock = pygame.time.Clock()

    def convert_time(self):
        """
        Convertit le temps en secondes en temps en heures, minutes, secondes et millisecondes.
        """
        milliseconds = self.time % 1000
        seconds = (self.time // 1000) % 60
        minutes = ((self.time // 1000) // 60) % 60
        hours = math.floor(minutes // 60)
        if hours > 0:
            return "{}:{}:{}.{}".format(hours, minutes, seconds, milliseconds)
        return "{}:{}.{}".format(minutes, seconds, milliseconds)


class ImageButton:
    def __init__(self, image, size, color):
        self.image = pygame.transform.scale(image, (size[0] / 2, size[1] / 2))
        self.surface = pygame.Surface(size)
        self.rect = self.surface.get_rect()
        self.color = color
        self.background = couleur_jeu["background"]
        self.imagerect = self.image.get_rect(center=self.rect.center)
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


class Flash:
    def __init__(self, rect, color, time):
        self.rect = rect
        self.time = time
        self.counter = 0
        self.surface = pygame.Surface(self.rect)
        self.surface.fill(color)

    def draw(self, screen):
        self.counter += 1
        if self.counter < self.time:
            screen.blit(self.surface, (0, 0))

    def reset(self):
        self.counter = 0


class Player:
    def __init__(self, player):
        self.player_name = player
        self.gravity = "bottom"
        self.positions = [433, 568]
        self.direction = pygame.math.Vector2(self.positions)
        self.hitbox = pygame.Rect(self.direction.x, self.direction.y, 30, 56)
        self.speed = 12
        self.directions = {"left": False, "right": True,  "up": False, "down": True}
        self.player_sprites_dict = []
        self.platforms = []
        self.authorized_platforms = [
            "platform",
            "conveyor_left",
            "conveyor_right",
        ]
        self.conveyors = [
            "conveyor_left",
            "conveyor_right",
        ]
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
        self.lock_laser_v = (False, 0)
        self.lock_laser_h = (False, 0)
        self.checkpoint_position = ((False, False), "up")
        self.checkpoint_coordinates = [0, 0]
        player_sprites = crop("./ressources/sprites/player.png", 63, 30)
        player_sprite_moving = crop("./ressources/sprites/player_moving.png", 63, 36, (38, 65))
        for index in range(len(player_sprites)):
            self.player_sprites_dict.append([
                player_sprites[index],
                player_sprite_moving[index]
            ])

    def update_positions(self, positions):
        self.positions = positions
        self.direction = pygame.math.Vector2(self.positions)
        self.hitbox = pygame.Rect(self.direction.x, self.direction.y, 30, 62)

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

    def modify_checkpoint(self, coordinates, direction, room_coords, var):
        if (
            coordinates != var["checkpoint_position"][0] or
            room_coords != var["checkpoint_coordinates"]
        ):
            self.checkpoint_position = (coordinates, direction)
            self.checkpoint_coordinates = room_coords
            var["checkpoint_position"] = self.checkpoint_position
            var["checkpoint_coordinates"] = self.checkpoint_coordinates.copy()
            play_sound("save.wav")
        return var

    def change_gravity(self):
        for platform in self.platforms:
            if self.hitbox.colliderect(
                platform[0].x,
                platform[0].y - 12,
                platform[0].width,
                platform[0].height
            ) and platform[1] in self.authorized_platforms:
                if self.gravity == "bottom":
                    play_sound("jump.wav")
                    self.gravity_enabled = True
                    self.directions["up"] = True
                    self.directions["down"] = False
                    self.gravity = "top"
                    self.direction.y -= self.speed
                    self.hitbox.y -= self.speed
                    break
            elif self.hitbox.colliderect(
                platform[0].x,
                platform[0].y + 12,
                platform[0].width,
                platform[0].height
            ) and platform[1] in self.authorized_platforms:
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

    def move_conveyor(self, direction):
        if direction == "left":
            self.direction.x -= (self.speed - 7)
            self.hitbox.x -= (self.speed - 7)
        if direction == "right":
            self.direction.x += (self.speed - 7)
            self.hitbox.x += (self.speed - 7)

    def die(self, var):
        self.emotion = "sad"
        self.walk_animation_type = "normal"
        var["dead_animation"] += 1
        if var["dead_animation"] == 1:
            var["deaths"] += 1
            self.player_name = "dead"
            play_sound("hurt.wav")
        if var["dead_animation"] == 60:
            var["dead"] = False
            var["dead_animation"] = 0
            self.player_name = "viridian"
            self.emotion = "happy"
            if var["checkpoint_position"][1] == "down":
                self.gravity = "top"
                self.directions["down"] = False
                self.directions["up"] = True
            else:
                self.gravity = "bottom"
                self.directions["down"] = True
                self.directions["up"] = False
            self.update_positions(
                [var["checkpoint_position"][0][0] + 15, var["checkpoint_position"][0][1]]
            )
            var["coordinates"] = var["checkpoint_coordinates"].copy()
            var["room"].change_room(var["coordinates"], var)

    def victory(self, var):
        var["victory_animation"] += 1
        if var["victory_animation"] == 1:
            var["teleporter_activated"] = True
            play_sound("gamesaved.wav")
        if var["victory_animation"] >= 60:
            var["flash"].draw(var["screen"])
        if var["victory_animation"] == 60:
            var["flash"].reset()
            play_sound("preteleport.wav")
        elif var["victory_animation"] == 120:
            var["flash"].reset()
            play_sound("preteleport.wav")
        elif var["victory_animation"] == 180:
            var["flash"].reset()
            play_sound("preteleport.wav")
        elif var["victory_animation"] == 210:
            var["flash"].reset()
            stop_music()
            play_sound("preteleport.wav")
        elif var["victory_animation"] == 260:
            play_sound("teleport.wav")
            var["teleporter_activated"] = False
        elif var["victory_animation"] == 340:
            play_sound("victory.ogg")
            var["menuSelect"] = "victory"
            var["victory"] = 0

    def update(self, var):
        if var["dead"]:
            self.die(var)
            return
        if var["dead"] is False:
            for platform in self.platforms:
                if self.hitbox.colliderect(platform[0]) and platform[1] == "enemy":
                    var["dead"] = True
                    self.die(var)
                    return
            if var["victory"] is False:
                self.walk_animation(var)
                if var["left"]:
                    self.move("left")
                if var["right"]:
                    self.move("right")
            for platform in self.platforms:
                if self.hitbox.colliderect(platform[0]) and platform[1] == "laser_v":
                    if self.lock_laser_v[0] is False:
                        if self.gravity == "bottom":
                            self.directions["up"] = True
                            self.directions["down"] = False
                            self.gravity = "top"
                            self.lock_laser_v = (True, self.hitbox.x)
                            play_sound("blip.wav")
                        elif self.gravity == "top":
                            self.directions["up"] = False
                            self.directions["down"] = True
                            self.gravity = "bottom"
                            self.lock_laser_v = (True, self.hitbox.x)
                            play_sound("blip.wav")
                elif self.hitbox.colliderect(
                    platform[0].x,
                    platform[0].y,
                    platform[0].width,
                    platform[0].height
                ) and platform[1] == "laser_h":
                    if self.lock_laser_h[0] is False:
                        if self.gravity == "bottom":
                            self.directions["up"] = True
                            self.directions["down"] = False
                            self.gravity = "top"
                            self.lock_laser_h = (True, self.hitbox.y)
                            play_sound("blip.wav")
                        elif self.gravity == "top":
                            self.directions["up"] = False
                            self.directions["down"] = True
                            self.gravity = "bottom"
                            self.lock_laser_h = (True, self.hitbox.y)
                            play_sound("blip.wav")
                if self.lock_laser_h[0]:
                    if abs(self.hitbox.y - abs(self.lock_laser_h[1])) > 30:
                        self.lock_laser_h = (False, 0)
                if self.lock_laser_v[0]:
                    if abs(self.hitbox.x - abs(self.lock_laser_v[1])) > 32:
                        self.lock_laser_v = (False, 0)
            for platform in self.platforms:
                if self.hitbox.colliderect(
                    platform[0].x,
                    platform[0].y - 12,
                    platform[0].width,
                    platform[0].height
                ) and platform[1] in self.conveyors:
                    if self.gravity == "bottom":
                        self.hitbox.bottom = platform[0].top - 12
                        self.direction.y = self.hitbox.y
                        if platform[1] == "conveyor_left":
                            self.move_conveyor("left")
                            var["left"] = True
                        if platform[1] == "conveyor_right":
                            self.move_conveyor("right")
                            var["right"] = True
                elif self.hitbox.colliderect(
                    platform[0].x,
                    platform[0].y + 12,
                    platform[0].width,
                    platform[0].height
                ) and platform[1] in self.conveyors:
                    if self.gravity == "top":
                        self.hitbox.top = platform[0].bottom + 12
                        self.direction.y = self.hitbox.y
                        if platform[1] == "conveyor_left":
                            self.move_conveyor("left")
                            var["left"] = True
                        if platform[1] == "conveyor_right":
                            self.move_conveyor("right")
                            var["right"] = True
            for platform in self.platforms:
                if self.hitbox.colliderect(
                    platform[0]
                ) and platform[1] in self.authorized_platforms:
                    if var["right"]:
                        self.hitbox.right = platform[0].left
                        self.direction.x = self.hitbox.x
                        break
                    elif var["left"]:
                        self.hitbox.left = platform[0].right
                        self.direction.x = self.hitbox.x
                        break
            for platform in self.platforms:
                if self.hitbox.colliderect(
                    platform[0].x,
                    platform[0].y - 12,
                    platform[0].width,
                    platform[0].height
                ) and platform[1] in self.authorized_platforms:
                    if self.gravity == "bottom":
                        self.hitbox.bottom = platform[0].top - 12
                        self.direction.y = self.hitbox.y
                elif self.hitbox.colliderect(
                    platform[0].x,
                    platform[0].y + 12,
                    platform[0].width,
                    platform[0].height
                ) and platform[1] in self.authorized_platforms:
                    if self.gravity == "top":
                        self.hitbox.top = platform[0].bottom + 12
                        self.direction.y = self.hitbox.y
            # Check if checkpoint is reached
            for platform in self.platforms:
                if self.hitbox.colliderect(platform[0]) and platform[1] == "checkpoint_up":
                    var = self.modify_checkpoint(
                        (platform[0].x, platform[0].y), "up", var["room"].get_coords(), var
                    )
                if self.hitbox.colliderect(platform[0]) and platform[1] == "checkpoint_down":
                    var = self.modify_checkpoint(
                        (platform[0].x, platform[0].y), "down", var["room"].get_coords(), var
                    )
            # Check if teleporter is reached
            for platform in self.platforms:
                if self.hitbox.colliderect(platform[0]) and platform[1] == "teleporter":
                    var["victory"] = True
                    var["clock"].stop_clock()
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
                self.direction.y = -self.hitbox.height + 3
                self.hitbox.y = -self.hitbox.height + 3
                var["coordinates"][1] -= 1
                var["room"].change_room(var["coordinates"], var)
            elif self.hitbox.top < -self.hitbox.height + 10:
                self.direction.y = 720 - self.hitbox.height
                self.hitbox.y = 720 - self.hitbox.height
                var["coordinates"][1] += 1
                var["room"].change_room(var["coordinates"], var)
        if var["victory"]:
            self.victory(var)

    def draw(self, screen, var):
        if var["collisions_show"]:
            pygame.draw.rect(screen, couleur_jeu["red"], self.hitbox)
        screen.blit(self.get_specific_sprite(), self.direction)

    def reset_gravity(self):
        self.gravity = "bottom"
        self.directions["down"] = True
        self.directions["up"] = False


class Object:
    def __init__(self):
        self.alltiles = []
        self.objects = []
        self.tiles1 = crop("./ressources/sprites/tiles_backup.png", 32, 32, (30, 30))
        self.background = crop("./ressources/sprites/backgrounds.png", 32, 32, (30, 30))
        self.spikes = crop("./ressources/sprites/spikes.png", 32, 32, (30, 30))
        self.conveyors = crop("./ressources/sprites/conveyors.png", 32, 32, (30, 30))
        self.lasers = crop("./ressources/sprites/lasers.png", 32, 32, (30, 30))
        self.checkpoints = crop("./ressources/sprites/checkpoints.png", 64, 64, (60, 60))
        self.teleporters = crop("./ressources/sprites/teleporters.png", 384, 384, (240, 240))
        for i in self.tiles1:
            self.alltiles.append(i)
        for i in self.background:
            self.alltiles.append(i)
        for i in self.spikes:
            self.alltiles.append(i)
            self.objects.append(i)
        for i in self.conveyors:
            self.alltiles.append(i)
        self.objects.append(self.conveyors[0])
        self.objects.append(self.conveyors[4])
        for i in self.lasers:
            self.objects.append(i)
            self.alltiles.append(i)
        for i in self.checkpoints:
            self.alltiles.append(i)
        self.objects.append(self.checkpoints[1])
        self.objects.append(self.checkpoints[3])
        for i in self.teleporters:
            self.alltiles.append(i)
        self.objects.append(self.teleporters[0])

    def draw_specific_grayscale_tile(self, surface, position, color, type, tile):
        object = convert_PIL_to_pygame(colored_textures[color][type][tile])
        surface.blit(object, position)

    def draw_tile(self, surface, position, tile, index):
        if tile == "teleporters":
            surface.blit(convert_PIL_to_pygame(self.teleporters[index]), position)

    def get_tiles(self):
        return self.alltiles

    def get_all_objects(self):
        return self.objects

    def get_all_spikes(self):
        return self.spikes

    def get_all_conveyors(self):
        return self.conveyors

    def get_all_lasers(self):
        return self.lasers

    def get_all_checkpoints(self):
        return self.checkpoints

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
        conveyors = object.get_all_conveyors()
        lasers = object.get_all_lasers()
        checkpoints = object.get_all_checkpoints()
        for couleur in couleur_jeu:
            self.texture_colored[couleur] = {}
            self.texture_colored[couleur]["platform"] = {}
            self.texture_colored[couleur]["background"] = {}
            self.texture_colored[couleur]["object"] = {}
            self.texture_colored[couleur]["conveyor"] = {}
            self.texture_colored[couleur]["laser"] = {}
            self.texture_colored[couleur]["checkpoint_up"] = {}
            self.texture_colored[couleur]["checkpoint_down"] = {}
            for count in range(len(platforms)):
                self.texture_colored[couleur]["platform"][count] = apply_color(
                    platforms[count], couleur_jeu[couleur]
                )
            for count in range(len(backgrounds)):
                self.texture_colored[couleur]["background"][count] = apply_color(
                    backgrounds[count], couleur_jeu[couleur]
                )
            for count in range(len(objects)):
                self.texture_colored[couleur]["object"][count] = apply_color(
                    objects[count], couleur_jeu[couleur]
                )
            for count in range(len(conveyors)):
                self.texture_colored[couleur]["conveyor"][count] = apply_color(
                    conveyors[count], couleur_jeu[couleur]
                )
            for count in range(len(lasers)):
                self.texture_colored[couleur]["laser"][count] = apply_color(
                    lasers[count], couleur_jeu[couleur]
                )
            for count in range(len(checkpoints)):
                self.texture_colored[couleur]["checkpoint_up"][count] = apply_color(
                    checkpoints[count], couleur_jeu[couleur]
                )
            for count in range(len(checkpoints)):
                self.texture_colored[couleur]["checkpoint_down"][count] = apply_color(
                    checkpoints[count], couleur_jeu[couleur]
                )

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
                self.players_colored[player]["normal"].append(
                    apply_color(sprites[0], couleur_joueurs[player])
                )
                self.players_colored[player]["moving"].append(
                    apply_color(sprites[1], couleur_joueurs[player])
                )

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
                    "[ " + i[3].upper() + " ]",
                    True,
                    i[1]
                )
                self.screen.blit(text, (position[0], position[1] + const_y))
            else:
                text = i[2].render(
                    i[3],
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

    def get_menus(self):
        return self.menulist


class Room:
    def __init__(self, map_name, coordinates):
        self.x_position = 0
        self.y_position = 0
        self.map_name = map_name
        self.object = Object()
        self.surface = None
        self.conveyors_animation = 0
        self.conveyors_timeanimation = 0
        self.teleporter_animation = 0
        self.teleporter_timeanimation = 0
        self.coordinates = coordinates
        try:
            self.data = read_room_data(self.map_name, self.coordinates)
        except json.decoder.JSONDecodeError:
            self.data = empty_room()
        except FileNotFoundError:
            self.data = empty_room()

    def refresh_room(self):
        try:
            self.data = read_room_data(self.map_name, self.coordinates)
        except json.decoder.JSONDecodeError:
            self.data = empty_room()
        except FileNotFoundError:
            self.data = empty_room()
        
        self.surface = None
        self.coordinates = self.coordinates.copy()

    def change_room(self, coordinates, var):
        try:
            self.data = read_room_data(self.map_name, coordinates)
        except json.decoder.JSONDecodeError:
            self.data = empty_room()
        except FileNotFoundError:
            self.data = empty_room()
        
        try:
            if var["current_music"] != self.data["music"]:
                var["current_music"] = self.data["music"]
                play_music(f"{var['current_music']}.ogg")
        except TypeError:
            if var["current_music"] != "presenting_vvvvvv":
                var["current_music"] = "presenting_vvvvvv"
                play_music("presenting_vvvvvv.ogg")
        self.surface = None
        self.coordinates = coordinates.copy()
        return var

    def get_coords(self):
        return self.coordinates

    def get_rects(self):
        rects = []
        position_x = 0
        position_y = 0
        try:
            for y_values in self.data["map_data"]:
                for values in y_values:
                    try:
                        if values["platform"] is not None:
                            rects.append((pygame.Rect(position_x, position_y, 30, 30), "platform"))
                    except KeyError:
                        pass
                    try:
                        if values["object"] is not None:
                            if values["object"] == 0 or values["object"] == 4:
                                # Spike bottom
                                rects.append(
                                    (pygame.Rect(position_x + 11, position_y, 4, 8), "enemy")
                                )
                                rects.append(
                                    (pygame.Rect(position_x + 7, position_y + 7, 13, 8), "enemy")
                                )
                                rects.append(
                                    (pygame.Rect(position_x + 4, position_y + 15, 20, 8), "enemy")
                                )
                                rects.append(
                                    (pygame.Rect(position_x, position_y + 22, 28, 8), "enemy")
                                )
                            elif values["object"] == 1 or values["object"] == 5:
                                # Spike top
                                rects.append(
                                    (pygame.Rect(position_x, position_y, 28, 8), "enemy")
                                )
                                rects.append(
                                    (pygame.Rect(position_x + 4, position_y + 8, 20, 8), "enemy")
                                )
                                rects.append(
                                    (pygame.Rect(position_x + 7, position_y + 15, 13, 8), "enemy")
                                )
                                rects.append(
                                    (pygame.Rect(position_x + 11, position_y + 22, 4, 8), "enemy")
                                )
                            elif values["object"] == 2 or values["object"] == 6:
                                # Spike right
                                rects.append(
                                    (pygame.Rect(position_x + 22, position_y + 3, 8, 27), "enemy")
                                )
                                rects.append(
                                    (pygame.Rect(position_x + 15, position_y + 6, 8, 20), "enemy")
                                )
                                rects.append(
                                    (pygame.Rect(position_x + 7, position_y + 10, 8, 13), "enemy")
                                )
                                rects.append(
                                    (pygame.Rect(position_x, position_y + 15, 8, 4), "enemy")
                                )
                            elif values["object"] == 3 or values["object"] == 7:
                                # Spike left
                                rects.append(
                                    (pygame.Rect(position_x, position_y + 3, 8, 27), "enemy")
                                )
                                rects.append(
                                    (pygame.Rect(position_x + 7, position_y + 6, 8, 20), "enemy")
                                )
                                rects.append(
                                    (pygame.Rect(position_x + 15, position_y + 10, 8, 13), "enemy")
                                )
                                rects.append(
                                    (pygame.Rect(position_x + 22, position_y + 15, 8, 4), "enemy")
                                )
                            elif values["object"] == 8:
                                # Conveyor left
                                rects.append(
                                    (pygame.Rect(position_x, position_y, 30, 30), "conveyor_left")
                                )
                            elif values["object"] == 9:
                                # Conveyor right
                                rects.append(
                                    (pygame.Rect(position_x, position_y, 30, 30), "conveyor_right")
                                )
                            elif values["object"] == 10:
                                # Laser horizontal
                                rects.append(
                                    (pygame.Rect(position_x, position_y + 15, 30, 1), "laser_h")
                                )
                            elif values["object"] == 11:
                                # Laser vertical
                                rects.append(
                                    (pygame.Rect(position_x + 13, position_y, 4, 30), "laser_v")
                                )
                            elif values["object"] == 12:
                                # Checkpoint up
                                rects.append(
                                    (pygame.Rect(position_x, position_y, 60, 60), "checkpoint_up")
                                )
                            elif values["object"] == 13:
                                # Checkpoint down
                                rects.append(
                                    (pygame.Rect(position_x, position_y, 60, 60), "checkpoint_down")
                                )
                            elif values["object"] == 14:
                                rects.append(
                                    (pygame.Rect(position_x, position_y, 240, 240), "teleporter")
                                )
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
                if self.data["map_data"][x][y][type] == "object" and (
                    data[0] == 10 or data[0] == 11 or data[0] == 12 or data[0] == 13
                ):
                    self.data["map_data"][x][y]["color"] = "white"
                else:
                    self.data["map_data"][x][y]["color"] = data[1]
            except IndexError:
                pass
            except TypeError:
                create_data_room(self.map_name, self.coordinates)
                self.refresh_room()
        elif order == "remove":
            try:
                self.data["map_data"][x][y] = {}
            except KeyError:
                pass
            except TypeError:
                create_data_room(self.map_name, self.coordinates)
                self.refresh_room()
        else:
            self.data["map_data"][x][y] = {}
        self.surface = None

    def save_data(self, coordinates):
        write_room_data(self.map_name, coordinates, self.data)

    def reset_position(self):
        self.x_position = 0
        self.y_position = 0

    def conveyors_animations(self, screen, var):
        self.conveyors_timeanimation += 1
        if self.conveyors_timeanimation >= 10:
            self.conveyors_timeanimation = 0
            self.conveyors_animation += 1
            if self.conveyors_animation == 4:
                self.conveyors_animation = 0
            var = self.draw_animations(screen, var)

    def teleporter_animations(self, screen, var):
        self.teleporter_timeanimation += 1
        if self.teleporter_timeanimation >= 15:
            self.teleporter_timeanimation = 0
            self.teleporter_animation += 1
            if self.teleporter_animation == 5:
                self.teleporter_animation = 1
            var = self.draw_animations(screen, var)

    def reset_teleporter(self):
        self.teleporter_animation = 0

    def draw_checkpoint(self, screen, var):
        checkpoint_position = var["checkpoint_position"]
        checkpoint_coordinates = var["checkpoint_coordinates"]
        if checkpoint_position[0] != (False, False):
            if checkpoint_coordinates == self.coordinates:
                if checkpoint_position[1] == "up":
                    self.object.draw_specific_grayscale_tile(
                        screen, checkpoint_position[0], "white", "checkpoint_up", 1
                    )
                elif checkpoint_position[1] == "down":
                    self.object.draw_specific_grayscale_tile(
                        screen, checkpoint_position[0], "white", "checkpoint_down", 3
                    )

    def draw_animations(self, screen, var):
        surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        try:
            surface.blit(self.surface, (0, 0))
            for y_values in self.data["map_data"]:
                for values in y_values:
                    try:
                        color = values["color"]
                    except KeyError:
                        pass

                    try:
                        if values["object"] is not None:
                            if values["object"] == 8:
                                self.object.draw_specific_grayscale_tile(
                                    surface,
                                    (
                                        self.x_position * 30,
                                        self.y_position * 30
                                    ),
                                    color,
                                    "conveyor",
                                    self.conveyors_animation
                                )
                            if values["object"] == 9:
                                self.object.draw_specific_grayscale_tile(
                                    surface,
                                    (
                                        self.x_position * 30,
                                        self.y_position * 30
                                    ),
                                    color,
                                    "conveyor",
                                    4 + self.conveyors_animation
                                )
                            if values["object"] == 14:
                                self.object.draw_tile(
                                    surface,
                                    (
                                        self.x_position * 30,
                                        self.y_position * 30
                                    ),
                                    "teleporters",
                                    self.teleporter_animation
                                )
                    except KeyError:
                        pass
                    self.x_position += 1
                self.y_position += 1
                self.x_position = 0
            screen.blit(surface, (0, 0))
            self.reset_position()
            self.surface = surface
            screen.blit(self.surface, (0, 0))
        except TypeError:
            pass
        return var

    def draw(self, screen, var):
        surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        if self.surface is None:
            try:
                for y_values in self.data["map_data"]:
                    for values in y_values:
                        try:
                            color = values["color"]
                        except KeyError:
                            pass

                        try:
                            if values["platform"] is not None:
                                self.object.draw_specific_grayscale_tile(
                                    surface,
                                    (
                                        self.x_position * 30,
                                        self.y_position * 30
                                    ),
                                    color,
                                    "platform",
                                    values["platform"]
                                )
                        except KeyError:
                            pass
                        try:
                            if values["background"] is not None:
                                self.object.draw_specific_grayscale_tile(
                                    surface,
                                    (
                                        self.x_position * 30,
                                        self.y_position * 30
                                    ),
                                    color,
                                    "background",
                                    values["background"]
                                )
                        except KeyError:
                            pass
                        try:
                            if values["object"] is not None:
                                if values["object"] == 12 and (
                                    self.x_position * 30,
                                    self.y_position * 30
                                ) != var["checkpoint_position"][0]:
                                    self.object.draw_specific_grayscale_tile(
                                        surface,
                                        (
                                            self.x_position * 30,
                                            self.y_position * 30
                                        ),
                                        "gray",
                                        "checkpoint_up",
                                        0
                                    )
                                elif values["object"] == 13 and (
                                    self.x_position * 30,
                                    self.y_position * 30
                                ) != var["checkpoint_position"][0]:
                                    self.object.draw_specific_grayscale_tile(
                                        surface,
                                        (
                                            self.x_position * 30,
                                            self.y_position * 30
                                        ),
                                        "gray",
                                        "checkpoint_down",
                                        2
                                    )
                                elif values["object"] == 12:
                                    self.object.draw_specific_grayscale_tile(
                                        surface,
                                        (
                                            self.x_position * 30,
                                            self.y_position * 30
                                        ),
                                        "gray",
                                        "checkpoint_up",
                                        0
                                    )
                                elif values["object"] == 13:
                                    self.object.draw_specific_grayscale_tile(
                                        surface,
                                        (
                                            self.x_position * 30,
                                            self.y_position * 30
                                        ),
                                        "gray",
                                        "checkpoint_down",
                                        2
                                    )
                                elif values["object"] == 14:
                                    self.object.draw_tile(
                                        surface,
                                        (
                                            self.x_position * 30,
                                            self.y_position * 30
                                        ),
                                        "teleporters",
                                        0
                                    )
                                else:
                                    self.object.draw_specific_grayscale_tile(
                                        surface,
                                        (
                                            self.x_position * 30,
                                            self.y_position * 30
                                        ),
                                        color,
                                        "object",
                                        values["object"]
                                    )
                        except KeyError:
                            pass
                        self.x_position += 1
                    self.y_position += 1
                    self.x_position = 0
                screen.blit(surface, (0, 0))
                self.reset_position()
                self.surface = surface
            except TypeError:
                pass
        else:
            screen.blit(self.surface, (0, 0))
        return var

    def draw_roomname(self, screen, var, customtext=None):
        rect = pygame.Rect(0, 720, screen.get_width(), screen.get_height() - 720)
        pygame.draw.rect(screen, couleur_jeu["black"], rect)
        try:
            if customtext is None:
                try:
                    text = var["fonts"]["little_generalfont"].render(
                        self.data["roomname"], True, couleur_jeu["cyan"]
                    )
                    screen.blit(text, text.get_rect(center=(rect.width // 2, rect.y + 15)))
                except KeyError:
                    pass
            else:
                text = var["fonts"]["little_generalfont"].render(
                    customtext, True, couleur_jeu["cyan"]
                )
                screen.blit(text, text.get_rect(center=(rect.width // 2, rect.y + 15)))
        except TypeError:
            text = var["fonts"]["little_generalfont"].render(
                "This room is empty.", True, couleur_jeu["red"]
            )
            screen.blit(text, text.get_rect(center=(rect.width // 2, rect.y + 15)))

    def get_roomname(self):
        try:
            return self.data["roomname"]
        except KeyError:
            self.data["roomname"] = ""
            return self.data["roomname"]
        except TypeError:
            return ""

    def write_roomname(self, key, action):
        if action == "backspace":
            self.data["roomname"] = self.data["roomname"][:-1]
        else:
            self.data["roomname"] += key

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
                play_music("presenting_vvvvvv.ogg")


class Editor:
    def __init__(self, screen_size, map_name, coordinates):
        self.map = Room(map_name, coordinates)
        self.model_box = 1
        self.box_size = 30 * self.model_box
        self.screen_size = screen_size
        self.cursor_rect_position = pygame.Rect(0, 0, 0, 0)
        self.object_selected = 0
        self.colors = [color for color in couleur_jeu.keys()]
        self.object_type = "platform"

    def update_mapdata(self, map_name, coordinates):
        self.map = Room(map_name, coordinates)

    def write_roomname(self, key, action):
        self.map.write_roomname(key, action)

    def get_roomname(self):
        return self.map.get_roomname()

    def change_room(self, coordinates, var):
        self.map.change_room(coordinates, var)
        return var

    def draw(self, screen, var):
        self.map.draw(screen, var)

    def cursor_position(self, mouse_position):
        for i in range((self.screen_size[0] // 30) + 1):
            for j in range((self.screen_size[1] // 30) + 1):
                if mouse_position[0] >= (i * 30) - 30 and mouse_position[0] <= i * 30:
                    if mouse_position[1] >= (j * 30) - 30 and mouse_position[1] <= j * 30:
                        if (i - 1) * self.box_size >= 0 and (j - 1) * self.box_size >= 0:
                            self.cursor_rect_position = pygame.Rect(
                                (i - 1) * 30, (j - 1) * 30, self.box_size, self.box_size
                            )
                            return self.cursor_rect_position

    def show_cursor(self, screen):
        pygame.draw.rect(screen, couleur_jeu["white"], self.cursor_rect_position, 2)

    def remove_object(self):
        for i in range((self.screen_size[0] // 30) + 1):
            for j in range((self.screen_size[1] // 30) + 1):
                if i * 30 == self.cursor_rect_position.x and j * 30 == self.cursor_rect_position.y:
                    self.map.update_data(j, i, type=self.object_type, order="remove")

    def place_object(self):
        for i in range((self.screen_size[0] // 30) + 1):
            for j in range((self.screen_size[1] // 30) + 1):
                if i * 30 == self.cursor_rect_position.x and j * 30 == self.cursor_rect_position.y:
                    self.map.update_data(
                        j, i, self.object_type, data=[
                            self.object_selected, self.colors[0]
                        ], order="place"
                    )

    def change_current_object(self, object_selected, type):
        self.object_selected = object_selected
        if type == "object":
            if object_selected == 12 or object_selected == 13:
                self.model_box = 2
                self.box_size = 30 * self.model_box
                return
            elif object_selected == 14:
                self.model_box = 8
                self.box_size = 30 * self.model_box
                return
        self.model_box = 1
        self.box_size = 30 * self.model_box

    def change_type_object(self, object_type):
        self.object_type = object_type

    def get_type_object(self):
        return self.object_type

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
            self.all_platform_buttons.append(
                [
                    ImageButton(
                        convert_PIL_to_pygame(platform),
                        (57, 57),
                        couleur_jeu["background"]
                    ),
                    "platform"
                ]
            )
        for background in self.object.get_all_backgrounds():
            self.all_backgrounds_buttons.append(
                [
                    ImageButton(
                        convert_PIL_to_pygame(background),
                        (57, 57),
                        couleur_jeu["background"]
                    ),
                    "background"
                ]
            )
        for object in self.object.get_all_objects():
            self.all_object_buttons.append(
                [
                    ImageButton(
                        convert_PIL_to_pygame(object),
                        (57, 57),
                        couleur_jeu["background"]
                    ),
                    "object"
                ]
            )

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
        var["boxes"]["selector"].draw(
            screen,  (20, get_screen_size()[1] - (300 * self.select_box_y))
        )
        if self.select_object_menu == "platform":
            if self.page_platform > 0:
                var["buttons"]["page_left"].draw(
                    screen, (230, get_screen_size()[1] - (130 * self.select_box_y))
                )
            if self.page_platform < len(self.object.get_all_platforms()) // 32:
                var["buttons"]["page_right"].draw(
                    screen, (897, get_screen_size()[1] - (130 * self.select_box_y))
                )
        elif self.select_object_menu == "background":
            if self.page_background > 0:
                var["buttons"]["page_left"].draw(
                    screen, (230, get_screen_size()[1] - (130 * self.select_box_y))
                )
            if self.page_background < len(self.object.get_all_backgrounds()) // 32:
                var["buttons"]["page_right"].draw(
                    screen, (897, get_screen_size()[1] - (130 * self.select_box_y))
                )
        elif self.select_object_menu == "object":
            if self.page_background > 0:
                var["buttons"]["page_left"].draw(
                    screen, (230, get_screen_size()[1] - (130 * self.select_box_y))
                )
            if self.page_background < len(self.object.get_all_backgrounds()) // 32:
                var["buttons"]["page_right"].draw(
                    screen, (897, get_screen_size()[1] - (130 * self.select_box_y))
                )
        var["buttons"]["color_left"].draw(
            screen, (40, get_screen_size()[1] - (60 * self.select_box_y))
        )
        var["buttons"]["color_right"].draw(
            screen, (170, get_screen_size()[1] - (60 * self.select_box_y))
        )
        screen.blit(var["texts"]["color"], (40, get_screen_size()[1] - (100 * self.select_box_y)))
        pygame.draw.rect(
            screen,
            couleur_jeu[var["editor"].get_color_selected()],
            (100, get_screen_size()[1] - (65 * self.select_box_y), 50, 50)
        )
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
            (230, get_screen_size()[1] - (210 * self.select_box_y)),
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
                                    self.all_platform_buttons[counter][0].change_color(
                                        couleur_jeu["cyan"]
                                    )
                                else:
                                    self.all_platform_buttons[counter][0].change_color(
                                        couleur_jeu["background"]
                                    )
                                self.all_platform_buttons[counter][0].draw(
                                    screen, (x_position, y_position)
                                )
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
                                    self.all_backgrounds_buttons[counter][0].change_color(
                                        couleur_jeu["cyan"]
                                    )
                                else:
                                    self.all_backgrounds_buttons[counter][0].change_color(
                                        couleur_jeu["background"]
                                    )
                                self.all_backgrounds_buttons[counter][0].draw(
                                    screen, (x_position, y_position)
                                )
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
                                    self.all_object_buttons[counter][0].change_color(
                                        couleur_jeu["cyan"]
                                    )
                                else:
                                    self.all_object_buttons[counter][0].change_color(
                                        couleur_jeu["background"]
                                    )
                                self.all_object_buttons[counter][0].draw(
                                    screen, (x_position, y_position)
                                )
                                x_position += 57
                                id_object += 1
                else:
                    var["buttons"][i].change_color(couleur_jeu["blurple"])
            except IndexError:
                pass

        var["buttons"]["platform"].draw(
            screen, (250, get_screen_size()[1] - (283 * self.select_box_y))
        )
        var["buttons"]["background"].draw(
            screen, (330, get_screen_size()[1] - (283 * self.select_box_y))
        )
        var["buttons"]["object"].draw(
            screen, (410, get_screen_size()[1] - (283 * self.select_box_y))
        )
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

    def get_select_object_menu(self):
        return self.select_object_menu

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
            self.stars.append(
                [
                    screen.get_width() + 5,
                    random.randint(0, screen.get_height() - 32),
                    random.randint(0, 50)
                ]
            )

        for (st, s) in enumerate(self.stars):
            pygame.draw.rect(screen, self.grey(255 - (s[2] * 5)), (s[0], s[1], 5, 5), 0)
            s[0] -= self.starSpeed - round(s[2] / 5)
            if s[0] < 0:
                del self.stars[st]
        self.starTime += 1
