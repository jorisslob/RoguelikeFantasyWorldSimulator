from tile import Tile
from rect import Rect
from gameobject import GameObject
import config

from random import randint

import tdl

color_dark_wall = (0, 0, 100)
color_light_wall = (130, 110, 50)
color_dark_ground = (50, 50, 150)
color_light_ground = (200, 180, 50)


def create_room(room):
    global my_map
    # go through the tiles in the rectangle and make them passable
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            my_map[x][y].blocked = False
            my_map[x][y].block_sight = False


def create_h_tunnel(x1, x2, y):
    global my_map
    for x in range(min(x1, x2), max(x1, x2) + 1):
        my_map[x][y].blocked = False
        my_map[x][y].block_sight = False


def create_v_tunnel(y1, y2, x):
    global my_map
    for y in range(min(y1, y2), max(y1, y2) + 1):
        my_map[x][y].blocked = False
        my_map[x][y].block_sight = False


def is_visible_tile(x, y):
    global my_map

    if x >= config.MAP_WIDTH or x < 0:
        return False
    elif y >= config.MAP_HEIGHT or y < 0:
        return False
    elif my_map[x][y].blocked == True:
        return False
    elif my_map[x][y].block_sight == True:
        return False
    else:
        return True


def make_map():
    global my_map

    # fill map with "blocked" tiles
    my_map = [[Tile(True) for y in range(config.MAP_HEIGHT)]
              for x in range(config.MAP_WIDTH)]

    rooms = []
    num_rooms = 0

    for _ in range(config.MAX_ROOMS):
        # random width and height
        w = randint(config.ROOM_MIN_SIZE, config.ROOM_MAX_SIZE)
        h = randint(config.ROOM_MIN_SIZE, config.ROOM_MAX_SIZE)
        # random position without going out of the boundaries of the map
        x = randint(0, config.MAP_WIDTH - w - 1)
        y = randint(0, config.MAP_HEIGHT - h - 1)

        # Rect class makes rectangles easier to work with
        new_room = Rect(x, y, w, h)

        # run through the other rooms and see if they intersect with this one
        failed = False
        for other_room in rooms:
            if new_room.intersect(other_room):
                failed = True
                break

        if not failed:
            # this means there are no intersections, so this room is valid

            # paint it to the map's tiles
            create_room(new_room)

            # center coordinates of new room, will be useful later
            (new_x, new_y) = new_room.center()

            if num_rooms == 0:
                # this is the first room, where the player starts at
                player.x = new_x
                player.y = new_y

            else:
                # all rooms after the first:
                # connect it to the previous room with a tunnel

                # center coordinates of previous room
                (prev_x, prev_y) = rooms[num_rooms - 1].center()

                # draw a coin (random number that is either 0 or 1)
                if randint(0, 1):
                    # first move horizontally, then vertically
                    create_h_tunnel(prev_x, new_x, prev_y)
                    create_v_tunnel(prev_y, new_y, new_x)
                else:
                    # first move vertically, then horizontally
                    create_v_tunnel(prev_y, new_y, prev_x)
                    create_h_tunnel(prev_x, new_x, new_y)

            # finally, append the new room to the list
            rooms.append(new_room)
            num_rooms += 1


def render_all(fov_recompute):
    global visible_tiles

    if fov_recompute:
        fov_recompute = False
        visible_tiles = tdl.map.quickFOV(player.x, player.y,
                                         is_visible_tile,
                                         fov=config.FOV_ALGO,
                                         radius=config.TORCH_RADIUS,
                                         lightWalls=config.FOV_LIGHT_WALLS)

        # go through all tiles, and set their background color according to the FOV
        for y in range(config.MAP_HEIGHT):
            for x in range(config.MAP_WIDTH):
                visible = (x, y) in visible_tiles
                wall = my_map[x][y].block_sight
                if not visible:
                    # it's not visible right now, the player can only see it if it's explored
                    if my_map[x][y].explored:
                        if wall:
                            con.draw_char(x, y, None, fg=None,
                                          bg=color_dark_wall)
                        else:
                            con.draw_char(x, y, None, fg=None,
                                          bg=color_dark_ground)
                else:
                    # it's visible
                    if wall:
                        con.draw_char(x, y, None, fg=None, bg=color_light_wall)
                    else:
                        con.draw_char(x, y, None, fg=None,
                                      bg=color_light_ground)
                    # since it's visible, explore it
                    my_map[x][y].explored = True

    # draw all objects in the list
    for obj in objects:
        obj.draw(visible_tiles, con)

    # blit the contents of "con" to the root console and present it
    root.blit(con, 0, 0, config.SCREEN_WIDTH, config.SCREEN_HEIGHT, 0, 0)


def handle_keys():
    global fov_recompute

    # realtime
    keypress = False
    for event in tdl.event.get():
        if event.type == 'KEYDOWN':
            user_input = event
            keypress = True

    if not keypress:
        return

    if user_input.key == 'ENTER' and user_input.alt:
        # Alt+Enter: toggle fullscreen
        tdl.set_fullscreen(not tdl.get_fullscreen())

    elif user_input.key == 'ESCAPE':
        return True  # exit game

    # movement keys
    if user_input.key == 'UP':
        player.move(0, -1, my_map)
        fov_recompute = True

    elif user_input.key == 'DOWN':
        player.move(0, 1, my_map)
        fov_recompute = True

    elif user_input.key == 'LEFT':
        player.move(-1, 0, my_map)
        fov_recompute = True

    elif user_input.key == 'RIGHT':
        player.move(1, 0, my_map)
        fov_recompute = True

##############################
# Initialization & Main Loop #
##############################


tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)
root = tdl.init(config.SCREEN_WIDTH, config.SCREEN_HEIGHT,
                title="Roguelike Fantasy World Simulator", fullscreen=False)
tdl.setFPS(config.LIMIT_FPS)
con = tdl.init(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)

# create object representing the player
player = GameObject(config.SCREEN_WIDTH//2,
                    config.SCREEN_HEIGHT//2, '@', (255, 255, 255))

# create an NPC
npc = GameObject(config.SCREEN_WIDTH//2 - 5,
                 config.SCREEN_HEIGHT//2, '@', (255, 255, 0))

# the list of objects with those two
objects = [npc, player]

# generate map (at this point it's not drawn to the screen)
make_map()

fov_recompute = True

while not tdl.event.is_window_closed():

    # draw all objects in the list
    render_all(fov_recompute)

    tdl.flush()

    # erase all objects at their old locations, before they move
    for obj in objects:
        obj.clear(con)

    # handle keys and exit game if needed
    exit_game = handle_keys()
    if exit_game:
        break
