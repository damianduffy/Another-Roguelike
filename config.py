from typing import List


class Config:
    def __init__(self) -> None:
        self.SPRITE_SCALING = 2
        #self.WALL_SPRITE_SCALING = 2
        #self.PLAYER_SPRITE_SCALING = 2
        self.TILE_SIZE = 8 * self.SPRITE_SCALING
        #self.WALL_SPRITE_SIZE = self.TILE_SIZE * self.WALL_SPRITE_SCALING

        # How big the grid is
        self.GRID_WIDTH = 32
        self.GRID_HEIGHT = 32

        self.AREA_WIDTH = self.GRID_WIDTH * self.TILE_SIZE
        self.AREA_HEIGHT = self.GRID_HEIGHT * self.TILE_SIZE

        # How fast the player moves
        self.MOVEMENT_SPEED = 5

        # How close the player can get to the edge before we scroll.
        self.VIEWPORT_MARGIN = 250

        self.FULLSCREEN = False

        # How big the window is
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 600
        self.WINDOW_TITLE = "Another Roguelike Dungeon Crawler!"

        self.BACKGROUND_COLOR = (0x20, 0x20, 0x20)
        # Show or hide performance stats.
        self.SHOW_PERFORMANCE = False


config = Config()