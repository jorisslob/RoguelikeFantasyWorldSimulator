import tdl

# actual size of the window
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

# 20 frames-per-second maximum
LIMIT_FPS = 20

# size of the map
MAP_WIDTH = 80
MAP_HEIGHT = 45

color_dark_wall = (0, 0, 100)
color_dark_ground = (50, 50, 150)


class Tile:
    # A tile of the map and its properties
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked

        # by default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked
        self.block_sight = block_sight


class Rect:
    # A rectangle on the map, used to characterize a room
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h


class GameObject:
    # This is a generic object: the player, a monster, an item, the stairs...
    # It's always represented by a character on screen
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx, dy):
        # move by the given amount
        if not my_map[self.x + dx][self.y + dy].blocked:
            self.x += dx
            self.y += dy

    def draw(self):
        # draw the character that represents this object at its position
        con.draw_char(self.x, self.y, self.char, self.color)

    def clear(self):
        # erase the character that represents this object
        con.draw_char(self.x, self.y, ' ', self.color, bg=None)


def make_map():
    global my_map

    # fill map with "blocked" tiles
    my_map = [[Tile(True) for y in range(MAP_HEIGHT)]
              for x in range(MAP_WIDTH)]

    # create two rooms
    room1 = Rect(20, 15, 10, 15)
    room2 = Rect(50, 15, 10, 15)
    create_room(room1)
    create_room(room2)
    create_h_tunnel(25, 55, 23)


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


def render_all():
    # go through all tiles, and set their background color
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            wall = my_map[x][y].block_sight
            if wall:
                con.draw_char(x, y, None, fg=None, bg=color_dark_wall)
            else:
                con.draw_char(x, y, None, fg=None, bg=color_dark_ground)

    # draw all objects in the list
    for obj in objects:
        obj.draw()

    # blit the contents of "con" to the root console and present it
    root.blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)


def handle_keys():
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
        player.move(0, -1)

    elif user_input.key == 'DOWN':
        player.move(0, 1)

    elif user_input.key == 'LEFT':
        player.move(-1, 0)

    elif user_input.key == 'RIGHT':
        player.move(1, 0)

##############################
# Initialization & Main Loop #
##############################


tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)
root = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT,
                title="Roguelike Fantasy World Simulator", fullscreen=False)
tdl.setFPS(LIMIT_FPS)
con = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT)

# create object representing the player
player = GameObject(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, '@', (255, 255, 255))

# create an NPC
npc = GameObject(SCREEN_WIDTH//2 - 5, SCREEN_HEIGHT//2, '@', (255, 255, 0))

# the list of objects with those two
objects = [npc, player]

# generate map (at this point it's not drawn to the screen)
make_map()
player.x = 25
player.y = 23

while not tdl.event.is_window_closed():

    # draw all objects in the list
    render_all()

    tdl.flush()

    # erase all objects at their old locations, before they move
    for obj in objects:
        obj.clear()

    # handle keys and exit game if needed
    exit_game = handle_keys()
    if exit_game:
        break
