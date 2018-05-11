from rect import Rect
from tile import Tile

import config

from random import randint


def make_map(player):
    # fill map with "blocked" tiles
    the_map = [[Tile(True) for y in range(config.MAP_HEIGHT)]
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
            create_room(new_room, the_map)

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
                    create_h_tunnel(prev_x, new_x, prev_y, the_map)
                    create_v_tunnel(prev_y, new_y, new_x, the_map)
                else:
                    # first move vertically, then horizontally
                    create_v_tunnel(prev_y, new_y, prev_x, the_map)
                    create_h_tunnel(prev_x, new_x, new_y, the_map)

            # finally, append the new room to the list
            rooms.append(new_room)
            num_rooms += 1
    return the_map


def create_room(room, the_map):
    # go through the tiles in the rectangle and make them passable
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            the_map[x][y].blocked = False
            the_map[x][y].block_sight = False


def create_h_tunnel(x1, x2, y, the_map):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        the_map[x][y].blocked = False
        the_map[x][y].block_sight = False


def create_v_tunnel(y1, y2, x, the_map):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        the_map[x][y].blocked = False
        the_map[x][y].block_sight = False
