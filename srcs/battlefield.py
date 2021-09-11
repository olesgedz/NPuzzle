class Coordinate:
    def __init__(self, x, y, is_difference=False):
        self.x = x
        self.y = y
        self.is_difference = is_difference

    def __sub__(self, other):
        if not isinstance(other, type(self)):
            raise ValueError('You can only subtract coordinate objects from each other.')
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
        return coordinate.y * size_of_field + coordinate.x

class Point:
    def __init__(self, value, coordinate, field, index):
        self.coordinate = coordinate
        self.field = field
        self._value = value
        self.index = index
        self.error = self.estimate(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self.reestimate(new_value)
        self._value = new_value
        if new_value == 0:
            self.field.cursor = self

    def estimate(self, value):
        expected_index = self.field.get_expected_index_by_value(value)
        expected_coordinate = Coordinate.by_index(expected_index, self.field.size)
        return (expected_coordinate - self.coordinate).estimate()

    def reestimate(self, value):
        new_error = self.estimate(value)
        difference = new_error - self.error
        self.field.error += difference
        self.error = new_error

    def find_neighbors(self):
        maybe_neighbors_coordinates = [self.coordinate.up(), self.coordinate.down(), self.coordinate.right(), self.coordinate.left()]
        neighbors_coordinates = []
        for candidate in maybe_neighbors_coordinates:
            if candidate.is_valid(self.field.size):
                neighbors_coordinates.append(candidate)
        neighbors = []
        for coordinate in neighbors_coordinates:
            neighbors.append(self.field.get_point_by_coordinate(coordinate))
        self.neighbors = neighbors

    def exchange_values(self, other):
        self.value, other.value = other.value, self.value

    def __lt__(self, other):
        if self.value != 0:
            raise ValueError('You can only move other cells to the cell with a zero value.')
        self.exchange_values(other)

    def __gt__(self, other):
        if other.value != 0:
            raise ValueError('You can only move other cells to the cell with a zero value.')
        self.exchange_values(other)


from functools import partial


class BaseGameEvent(RuntimeError):
    pass

class GameDoneWin(BaseGameEvent):
    pass

class GameDoneLose(BaseGameEvent):
    pass

class CastDuplicate(BaseGameEvent):
    pass

class SearchFrame:
    casts = {}

    def __init__(self, field, cursor, heuristics, previous_frame):
        self.field = field
        self.cursor = cursor
        self.heuristics
        self.previous_frame = previous_frame
        self.cast_register()
        self.neighbors = self.get_sorted_neighbors()


    def cast_register(self):
        self.cast = self.generate_cast(field)
        if self.cast in self.casts:
            exception = CastDuplicate('The cast has an earlier double.')
            exception.double = self.casts[self.cast]
            raise exception
        self.casts[self.cast] = self

    def get_sorted_neighbors(self):
        neighbors = cursor.neighbors
        return sorted(neighbors, key=partial(self.heuristics, self.field))

    


class BattleField:
    def __init__(self, size, data, heuristics):
        self.size = size
        self.points = self.get_points_from_source(data)
        self.link_points()
        self.cursor = self.search_zero()
        self.error = self.estimate()
        self.heuristics = heuristics
        self.current_frame = None

    def __str__(self):
        max_len = max([len(str(x.value)) for x in self.points])
        slots = []
        for point in self.points:
            value = point.value
            post_spaces = ' ' * (max_len - len(str(point.value)) + 1)
            slot = f'{value}{post_spaces}'
            slots.append(slot)
        lines = []
        line = []
        for index, slot in enumerate(slots):
            line.append(slot)
            if (index + 1) % (self.size) == 0:
                lines.append(line)
                line = []
        ended_lines = [''.join(slots) for slots in lines]
        result = '\n'.join(ended_lines)
        return result

    def link_points(self):
        for point in self.points:
            point.find_neighbors()

    def estimate(self):
        result = 0
        for point in self.points:
            result += point.error
        return result

    def get_expected_index_by_value(self, value):
        if value == 0:
            return self.size ** 2 - 1
        return value - 1

    def get_points_from_source(self, source):
        result = []
        for index, number in enumerate(source):
            point = Point(number, Coordinate.by_index(index, self.size), self, index)
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

    def get_frame(self):
        if not self.error:
            raise GameDoneWin('Game is done, you win.')
        try:
            frame = SearchFrame(self, self.cursor, self.heuristics, self.current_frame)
        except CastDuplicate as e:
            frame = e.double
        return frame


    def fight(self):
        try:
            self.current_frame = self.get_frame()
        except


def base_heuristics(field, current_point):
    cursor = field.cursor
    current_point > cursor
    error = field.error
    current_point < cursor
    return error



battle = BattleField(3, [0, 2, 3, 4, 5, 6, 7, 8, 1], base_heuristics)
print(battle)
print(battle.estimate())
battle.points[0] < battle.points[-1]
print(battle)
print(battle.estimate())
battle.points[-1] < battle.points[1]
print(battle)
print(battle.estimate())
