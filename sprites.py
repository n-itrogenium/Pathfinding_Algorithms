import pygame
import os
import config


class BaseSprite(pygame.sprite.Sprite):
    images = dict()

    def __init__(self, row, col, file_name, transparent_color=None):
        pygame.sprite.Sprite.__init__(self)
        if file_name in BaseSprite.images:
            self.image = BaseSprite.images[file_name]
        else:
            self.image = pygame.image.load(os.path.join(config.IMG_FOLDER, file_name)).convert()
            self.image = pygame.transform.scale(self.image, (config.TILE_SIZE, config.TILE_SIZE))
            BaseSprite.images[file_name] = self.image
        # making the image transparent (if needed)
        if transparent_color:
            self.image.set_colorkey(transparent_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (col * config.TILE_SIZE, row * config.TILE_SIZE)
        self.row = row
        self.col = col


class Agent(BaseSprite):
    def __init__(self, row, col, file_name):
        super(Agent, self).__init__(row, col, file_name, config.DARK_GREEN)

    def move_towards(self, row, col):
        row = row - self.row
        col = col - self.col
        self.rect.x += col
        self.rect.y += row

    def place_to(self, row, col):
        self.row = row
        self.col = col
        self.rect.x = col * config.TILE_SIZE
        self.rect.y = row * config.TILE_SIZE

    # game_map - list of lists of elements of type Tile
    # goal - (row, col)
    # return value - list of elements of type Tile
    def get_agent_path(self, game_map, goal):
        pass


class ExampleAgent(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        path = [game_map[self.row][self.col]]

        row = self.row
        col = self.col
        while True:
            if row != goal[0]:
                row = row + 1 if row < goal[0] else row - 1
            elif col != goal[1]:
                col = col + 1 if col < goal[1] else col - 1
            else:
                break
            path.append(game_map[row][col])
        return path


# Depth First Search
class Aki(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        path = []
        stack = [game_map[self.row][self.col]]

        while True:
            tile = stack.pop()
            row = tile.row
            col = tile.col
            tiles = []

            # West
            if col > 0 and game_map[row][col - 1] not in path:
                tiles.append(game_map[row][col - 1])  

            # South
            if row < len(game_map) - 1 and game_map[row + 1][col] not in path:
                tiles.append(game_map[row + 1][col])

            # East
            if col < len(game_map[0]) - 1 and game_map[row][col + 1] not in path:
                 tiles.append(game_map[row][col + 1])

            # North
            if row > 0 and game_map[row - 1][col] not in path:
                tiles.append(game_map[row - 1][col])

            tiles.sort(key = lambda x: x.cost(), reverse=True)
            stack += tiles
            path.append(game_map[row][col])
            if row == goal[0] and col == goal[1]:
                break

        return path


# Breadth First Search
class Jocke(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        queue = [[game_map[self.row][self.col], 0]]
        while True:
            tile = queue.pop(0)
            row = tile[0].row
            col = tile[0].col
            tiles = []
            current = tile
            path = []
            while True:
                path.append(current[0])
                if current[1] == 0:
                    break
                current = current[1]
            path.reverse()
            # North
            if row > 0 and game_map[row - 1][col] not in path:
                north = i = 0
                if col > 0:
                    north += game_map[row - 1][col - 1].cost()
                    i += 1
                if col < len(game_map[0]) - 1:
                    north += game_map[row - 1][col + 1].cost()
                    i += 1
                if row > 1:
                    north += game_map[row - 2][col].cost()
                    i += 1
                north /= i
                tiles.append([north, game_map[row - 1][col]])
            
            # East
            if col < len(game_map[0]) - 1 and game_map[row][col + 1] not in path:
                east = i = 0
                if row > 0:
                    east += game_map[row - 1][col + 1].cost()
                    i += 1
                if row < len(game_map) - 1:
                    east += game_map[row + 1][col + 1].cost()
                    i += 1
                if col < len(game_map[0]) - 2:
                    east += game_map[row][col + 2].cost()
                    i += 1
                east /= i
                tiles.append([east, game_map[row][col + 1]])

            # South
            if row < len(game_map) - 1 and game_map[row + 1][col] not in path:
                south = i = 0
                if col > 0:
                    south += game_map[row + 1][col - 1].cost()
                    i += 1
                if col < len(game_map[0]) - 1:
                    south += game_map[row + 1][col + 1].cost()
                    i += 1
                if row < len(game_map) - 2:
                    south += game_map[row + 2][col].cost()
                    i += 1
                south /= i
                tiles.append([south, game_map[row + 1][col]])

            # West
            if col > 0 and game_map[row][col - 1] not in path:
                west = i = 0
                if row > 0:
                    west += game_map[row - 1][col - 1].cost()
                    i += 1
                if row < len(game_map) - 1:
                    west += game_map[row + 1][col - 1].cost()
                    i += 1
                if col > 1:
                    west += game_map[row][col - 2].cost()
                    i += 1
                west /= i
                tiles.append([west, game_map[row][col - 1]])

            tiles.sort(key = lambda x: x[0])

            while tiles: 
                queue.append([tiles.pop(0)[1], tile])
            if row == goal[0] and col == goal[1]:
                break
        return path


class Draza(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        path = [game_map[self.row][self.col]]
        return path

class Bole(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        path = [game_map[self.row][self.col]]
        return path

class Tile(BaseSprite):
    def __init__(self, row, col, file_name):
        super(Tile, self).__init__(row, col, file_name)

    def position(self):
        return self.row, self.col

    def cost(self):
        pass

    def kind(self):
        pass


class Stone(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'stone.png')

    def cost(self):
        return 1000

    def kind(self):
        return 's'


class Water(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'water.png')

    def cost(self):
        return 500

    def kind(self):
        return 'w'


class Road(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'road.png')

    def cost(self):
        return 2

    def kind(self):
        return 'r'


class Grass(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'grass.png')

    def cost(self):
        return 3

    def kind(self):
        return 'g'


class Mud(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'mud.png')

    def cost(self):
        return 5

    def kind(self):
        return 'm'


class Dune(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'dune.png')

    def cost(self):
        return 7

    def kind(self):
        return 's'


class Goal(BaseSprite):
    def __init__(self, row, col):
        super().__init__(row, col, 'x.png', config.DARK_GREEN)


class Trail(BaseSprite):
    def __init__(self, row, col, num):
        super().__init__(row, col, 'trail.png', config.DARK_GREEN)
        self.num = num

    def draw(self, screen):
        text = config.GAME_FONT.render(f'{self.num}', True, config.WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
