class GameObject:
    # This is a generic object: the player, a monster, an item, the stairs...
    # It's always represented by a character on screen
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx, dy, the_map):
        # move by the given amount
        if not the_map[self.x + dx][self.y + dy].blocked:
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
