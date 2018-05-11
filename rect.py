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

        Normal case
        >>> r1 = Rect(10, 10, 10, 10)
        >>> (r1.x1, r1.y1, r1.x2, r1.y2)
        (10, 10, 20, 20)

        Weird rectangles
        >>> r2 = Rect(0, 0, 0, 0)
        >>> (r2.x1, r2.y1, r2.x2, r2.y2)
        (0, 0, 0, 0)
        >>> r3 = Rect(10, 10, -5, -5)
        >>> (r3.x1, r3.y1, r3.x2, r3.y2)
        (10, 10, 5, 5)
        """
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        """
        Calculates the center of a rectangle

        Happy path
        >>> r1 = Rect(10, 10, 2, 2)
        >>> r1.center()
        (11, 11)

        Rounded down
        >>> r2 = Rect(20, 10, 3, 5)
        >>> r2.center()
        (21, 12)
        """
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return (center_x, center_y)

    def intersect(self, other):
        """
        returns true if this rectangle intersects with another one
        intersection also includes touching

        >>> r1 = Rect(10, 10, 10, 10)
        >>> r2 = Rect(15, 15, 10, 10)
        >>> r3 = Rect(25, 25, 10, 10)
        >>> r1.intersect(r2)
        True
        >>> r1.intersect(r3)
        False
        >>> r2.intersect(r3)
        True
        """
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
