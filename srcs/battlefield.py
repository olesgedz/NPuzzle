class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def down(self):
        return type(self)(self.x, self.y + 1)

    def up(self):
        return type(self)(self.x, self.y - 1)

    def left(self):
        return type(self)(self.x - 1, self.y)

    def right(self):
        return type(self)(self.x + 1, self.y)

    def is_valid(self, size_of_field, exception=None):
        result = size_of_field > self.x >= 0 and size_of_field > self.y >= 0
        if exception is not None and not result:
            raise exception
        return result

    @classmethod
    def by_index(cls, index, size_of_field):
        pass

class Point:
    def __init__(self, value, coordinate, field):
        self.coordinate = coordinate
        self.field = field
        self.value = value
        self.neighbors = self.get_neighbors()

class BattleField:
    def __init__(self, size, data):
        self.size = size
        self.points = self.get_points_from_source(source)
        self.cursor

    def get_points_from_source(self, source):
        result = []
        for index, number in enumerate(source):
            point = Point(number, Coordinate.by_index(index, self.size), self)
            result.append(point)
        return result

    def check_coordinate(self, coordinate):
        coordinate.is_valid(self.size, exception=ValueError(f'Coordinate {coordinate} is not valid.'))

    def get_point(self, coordinate):
        pass

    def get_line(self, coordinate):
        index_begin
