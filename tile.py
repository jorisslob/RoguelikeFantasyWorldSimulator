class Tile:
    # A tile of the map and its properties
    def __init__(self, blocked, block_sight=None):
        """
        Create a tile

        When block_sight is not defined it is the same as blocked
        >>> tile1 = Tile(True)
        >>> tile1.block_sight
        True
        >>> tile2 = Tile(False)
        >>> tile2.block_sight
        False
        >>> tile3 = Tile(True, False)
        >>> tile3.block_sight
        False
        """
        self.blocked = blocked

        # all tiles start unexplored
        self.explored = False

        # by default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked
        self.block_sight = block_sight


if __name__ == "__main__":
    import doctest
    doctest.testmod()
