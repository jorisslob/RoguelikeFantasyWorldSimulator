import tdl

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20


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
        self.x += dx
        self.y += dy

    def draw(self):
        # draw the character that represents this object at its position
        con.draw_char(self.x, self.y, self.char, self.color)

    def clear(self):
        # erase the character that represents this object
        con.draw_char(self.x, self.y, ' ', self.color, bg=None)


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


tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)
root = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT,
                title="Roguelike Fantasy World Simulator", fullscreen=False)
con = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT)

tdl.setFPS(LIMIT_FPS)

player = GameObject(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, '@', (255, 255, 255))
npc = GameObject(SCREEN_WIDTH//2 - 5, SCREEN_HEIGHT//2, '@', (255, 255, 0))
objects = [npc, player]

while not tdl.event.is_window_closed():
    for obj in objects:
        obj.draw()

    root.blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)
    tdl.flush()

    for obj in objects:
        obj.clear()

    # handle keys and exit game if needed
    exit_game = handle_keys()
    if exit_game:
        break
