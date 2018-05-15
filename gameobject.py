class GameObject:
    # This is a generic object: the player, a monster, an item, the stairs...
    # It's always represented by a character on screen
    def __init__(self, x, y, char, name, color, blocks=False):
        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.color = color
        self.blocks = blocks

    def move(self, dx, dy, the_map, objects):
        # move by the given amount
        if not is_blocked(self.x + dx, self.y + dy, the_map, objects):
            self.x += dx
            self.y += dy

    def draw(self, visible_tiles, console):
        # only show if it's visible to the player
        if (self.x, self.y) in visible_tiles:
            # draw the character that represents this object at its position
            console.draw_char(self.x, self.y, self.char, self.color, bg=None)

    def clear(self, console):
        # erase the character that represents this object
        console.draw_char(self.x, self.y, ' ', self.color, bg=None)


def is_blocked(x, y, the_map, objects):
    # first test the map tile
    if the_map[x][y].blocked:
        return True

    # now check for any blocking objects
    for obj in objects:
        if obj.blocks and obj.x == x and obj.y == y:
            return True

    return False
