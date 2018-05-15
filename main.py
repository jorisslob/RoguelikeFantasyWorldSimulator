from controls import handle_keys
from gameobject import GameObject
from themap import make_map
import colors
import config

import tdl


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
                                          bg=colors.dark_blue)
                        else:
                            con.draw_char(x, y, None, fg=None,
                                          bg=colors.desaturated_blue)
                else:
                    # it's visible
                    if wall:
                        con.draw_char(x, y, None, fg=None,
                                      bg=colors.desaturated_amber)
                    else:
                        con.draw_char(x, y, None, fg=None,
                                      bg=colors.brass)
                    # since it's visible, explore it
                    my_map[x][y].explored = True

    # draw all objects in the list
    for obj in objects:
        obj.draw(visible_tiles, con)

    # blit the contents of "con" to the root console and present it
    root.blit(con, 0, 0, config.SCREEN_WIDTH, config.SCREEN_HEIGHT, 0, 0)


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
                    config.SCREEN_HEIGHT//2, '@', 'player', colors.white, blocks=True)

# the list of objects, will be larger later
objects = [player]

# generate map (at this point it's not drawn to the screen), and extend the list of objects
(my_map, new_objects) = make_map(player)
objects.extend(new_objects)

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
    (exit_game, fov_recompute) = handle_keys(
        fov_recompute, player, my_map, objects)
    if exit_game:
        break
