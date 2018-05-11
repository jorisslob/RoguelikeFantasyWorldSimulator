class Rect:
    """
    A rectangle on the map, used to characterize a room

    >>> r = Rect(10, 10, 6, 6)
    >>> r.center()
    (13, 13)
    >>> r2 = Rect(14, 14, 7, 7)
    >>> r.intersect(r2)
    True
    """

    def __init__(self, x, y, w, h):
        """
        Create a rectangle, not too fancy

        >>> r1 = Rect(0, 0, 0, 0)
        >>> (r1.x1, r1.y1, r1.x2, r1.y2)
        (0, 0, 0, 0)
        """
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return (center_x, center_y)

    def intersect(self, other):
        # returns true if this rectangle intersects with another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
