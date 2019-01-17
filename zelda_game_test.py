import sys, pygame
from pygame.locals import *
from enum import Enum, auto


tile_size = 16
board_height = 16
board_width = 16
max_supply_count = 3


class Dir(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    CENTER = auto()


class Pos:
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y

    def get_img_x(self):
        return self.grid_x * tile_size

    def get_img_y(self):
        return self.grid_y * tile_size

    def move(self, direction):
        if direction == Dir.UP:
            self.grid_x = self.grid_x - 1
        elif direction == Dir.DOWN:
            self.grid_x = self.grid_x + 1
        elif direction == Dir.LEFT:
            self.grid_y = self.grid_y - 1
        elif direction == Dir.LEFT:
            self.grid_y = self.grid_y + 1

    def __eq__(self, other):
        if self.grid_x == other.grid_x and self.grid_y == other.grid_y:
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def copy(self):
        return Pos(self.grid_x, self.grid_y)


class PosContainer:
    def __init__(self, data=None):
        if data:
            self.data = data
        else:
            self.data = []

    def contains(self, other):
        if type(other) == Pos:
            for pos in self.data:
                if pos == other:
                    return True
        elif issubclass(other, PosContainer):
            for x in other.data:
                if self.contains(x):
                    return True
        return False

    def copy_contents(self):
        copy = []
        for pos in self.data:
            copy.append(pos.copy())
        return copy


class PosSet(PosContainer):
    def __init__(self, data=None):
        self.data = []
        if data:
            self.add(data)


    def add(self, other):
        if type(other) == Pos and not self.contains(other):
            self.data.append(other)
        elif type(other) == PosSet:
            self.add(other)

    def subtract(self, other):
        if type(other) == Pos and self.contains(other):
            self.data.remove(other)
        elif type(other) == PosSet:
            self.subtract(other)

    def adjacent(self, pos):
        ps = PosSet()
        for direction in [Dir.UP, Dir.DOWN, Dir.LEFT, Dir.Left]:
            new_pos = pos.copy().move(direction)
            if self.contains(new_pos):
                ps.add(new_pos)
        return ps

    def copy(self):
        return PosSet(self.copy_contents())

    def get_path(self, start, end):
        possible_paths = [Path([start])]
        while possible_paths:
            path = possible_paths.pop(0)
            for adj in self.adjacent(path.get_pos(-1)).data:
                if not path.contains(adj):
                    new_path = path.copy()
                    new_path.add(adj)
                    if adj == end:
                        return new_path
                    possible_paths.append(new_path)





class Path(PosContainer):
    def add(self, pos):
        self.data.append(pos)

    def get_pos(self, index):
        return self.data[index]

    def __len__(self):
        return len(self.data)

    def copy(self):
        return Path(self.copy_contents())


class Supplies(Enum):
    ROPE = auto()
    BOMB = auto()
    POISON_BOMB = auto()
    OIL_JAR = auto()
    BALLOON = auto()
    BASKET = auto()
    WOOD_SCRAP = auto()


class Action:
    def __init__(self):
        pass

    def act(self, manager):  # Makes changes to other units/game/the board
        pass

    def is_legal(self, manager):  # Returns bool
        pass

    def diagram(self):  # Returns image to be blited onto board
        pass


class GameObj:
    def __init__(self, pos):
        self.pos = pos
        self.direction = Dir.CENTER
        self.fill_pos = False
        self.stun = -1  # -1 is permenate, 0 is no stun, any positive int is remaining turns of stun
        self.action = None

    def set_action(self):
        pass

    def get_action(self):
        if self.action.is_legal():
            return self.action

    def set_pos(self, pos):
        self.pos = pos

    def get_pos(self):
        return self.pos.copy()


class Character(GameObj):
    def __init__(self, pos):
        super().__init__(pos)
        self.items = []


class Player(Character):
    def __init__(self, pos):
        super().__init__(pos)


class Board:
    def __init__(self):
        self.action_delay = 1
        self.board = None
        self.valid_spaces = []
        self.gravity_curr = 0
        self.gravity_pattern = [Dir.CENTER]

    def spawn_objs(self):
        pass

    def get_gravity(self):
        return self.gravity_pattern[self.gravity_curr]

    def update(self):
        # Advance gravity curr
        if self.gravity_curr + 1 < len(self.gravity_pattern):
            self.gravity_curr += 1
        else:
            self.gravity_curr = 0


class Manager:
    def __init__(self):
        self.action_timer = 0
        self.player_obj = []
        self.obj = []
        self.selected_obj = None
        self.supplies = {}
        for x in Supplies:
            self.supplies[x] = 0
        self.board = Board()

    def timer(self, screen):
        if self.action_timer < self.board.action_delay:
            self.action_timer += 1
        else:
            self.action_timer = 0
            self.turn()
        self.display(screen)

    def turn(self):
        pass

    def user_input(self, key):
        if 48 <= key <= 57:


    def display(self, screen):
        screen.fill([0, 0, 0])
        pygame.display.flip()

    def get_pos_set(self, include, exclude):  # Include and exclude are sets of GameObj classes
        ps = PosSet()
        for obj in self.player_obj + self.obj:
            if type(obj) in include and not type(obj) in exclude:
                ps.add(obj.get_pos())


if __name__ == "__main__":
    pygame.init()
    manager = Manager()

    size = width, height = 320, 240
    screen = pygame.display.set_mode(size)
    pygame.time.set_timer(USEREVENT+1, 333)

    while True:
        for event in pygame.event.get():
            if event.type == USEREVENT + 1:
                manager.timer(screen)
            if event.type  == pygame.KEYDOWN:
                manager.user_input(event.key)
            if event.type == pygame.QUIT:
                sys.exit()
        manager.display(screen)
