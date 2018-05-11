from gameobject import GameObject
from themap import make_map
import config

import tdl

color_dark_wall = (0, 0, 100)
color_light_wall = (130, 110, 50)
color_dark_ground = (50, 50, 150)
color_light_ground = (200, 180, 50)


def is_visible_tile(x, y, the_map):
    if x >= config.MAP_WIDTH or x < 0:
        return False
    elif y >= config.MAP_HEIGHT or y < 0:
        return False
    elif the_map[x][y].blocked == True:
        return False
    elif the_map[x][y].block_sight == True:
        return False
    else:
        return True


def render_all(fov_recompute, visible_tiles):
    def visibility(x, y):
        return is_visible_tile(x, y, my_map)

    if fov_recompute:
        fov_recompute = False
        visible_tiles = tdl.map.quickFOV(player.x, player.y,
                                         visibility,
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


def handle_keys(fov_recompute):
    # realtime
    keypress = False
    for event in tdl.event.get():
        if event.type == 'KEYDOWN':
            user_input = event
            keypress = True

    if not keypress:
        return (False, fov_recompute)

    if user_input.key == 'ENTER' and user_input.alt:
        # Alt+Enter: toggle fullscreen
        tdl.set_fullscreen(not tdl.get_fullscreen())

    elif user_input.key == 'ESCAPE':
        return (True, False)  # exit game

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

    return (False, fov_recompute)

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
my_map = make_map(player)
visible_tiles = None

fov_recompute = True

while not tdl.event.is_window_closed():

    # draw all objects in the list
    render_all(fov_recompute, visible_tiles)

    tdl.flush()

    # erase all objects at their old locations, before they move
    for obj in objects:
        obj.clear(con)

    # handle keys and exit game if needed
    (exit_game, fov_recompute) = handle_keys(fov_recompute)
    if exit_game:
        break
