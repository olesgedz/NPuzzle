class Coordinate:
    def __init__(self, x, y, is_difference=False):
        self.x = x
        self.y = y
        self.is_difference = is_difference

    def __sub__(self, other):
        x = max((self.x, other.x)) - min((self.x, other.x))
        y = max((self.y, other.y)) - min((self.y, other.y))
        return type(self)(x, y, is_difference=True)

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

    def estimate(self):
        if self.is_difference:
            return self.x + self.y
        raise ValueError('The evaluation can only be performed for the difference between the coordinates.')

    @classmethod
    def by_index(cls, index, size_of_field):
        if index < 0:
            raise ValueError('Index must be >= 0.')
        y = index // size_of_field
        x = index - (y * size_of_field)
        return cls(x, y)

    @staticmethod
    def to_index(coordinate, size_of_field):
        result = coordinate.y * size_of_field + coordinate.x

class Point:
    def __init__(self, value, coordinate, field, index):
        self.coordinate = coordinate
        self.field = field
        self.value = value
        self.neighbors = self.get_neighbors()
        self.index = index
        self.expected_value = self.get_expected_value(index)
        self.error = get_error()

    def get_expected_value(self, index):
        pass

    def get_error(self):
        pass


    def get_neighbors(self):
        maybe_neighbors_coordinates = [self.coordinate.up(), self.coordinate.down(), self.coordinate.right(), self.coordinate.left()]
        neighbors_coordinates = []
        for candidate in maybe_neighbors_coordinates:
            if candidate.is_valid(self.field.size):
                neighbors_coordinates.append(candidate)
        neighbors = []
        for coordinate in neighbors_coordinates:
            neighbors.append(self.field.get_point_by_coordinate(coordinate))
        return neighbors


class BattleField:
    def __init__(self, size, data):
        self.size = size
        self.points = self.get_points_from_source(source)
        self.cursor = self.search_zero()
        self.error = self.error_estimation()

    def error_estimation():
        pass

    def get_points_from_source(self, source):
        result = []
        for index, number in enumerate(source):
            point = Point(number, Coordinate.by_index(index, self.size), self)
            result.append(point)
        return result

    def search_zero(self):
        for point in self.points:
            if point.value == 0:
                return point

    def check_coordinate(self, coordinate):
        coordinate.is_valid(self.size, exception=ValueError(f'Coordinate {coordinate} is not valid.'))

    def get_point_by_coordinate(self, coordinate):
        index = Coordinate.to_index(coordinate, self.size)
        return self.points[index]

    def fight(self):
        pass
