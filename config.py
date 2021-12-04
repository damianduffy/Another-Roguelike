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

        # Player hitbox coords during different actions
        self.player_hit_box_coords = [
            # idle
            [
                # down
                [
                    ((-6.0, -4.0), (-3.0, -7.0), (3.0, -7.0), (5.0, -5.0), (5.0, 5.0), (0.0, 10.0), (-5.0, 10.0), (-6.0, 9.0)),     # frame 0
                    ((-6.0, -4.0), (-3.0, -7.0), (3.0, -7.0), (5.0, -5.0), (5.0, 5.0), (1.0, 9.0), (-5.0, 9.0), (-6.0, 8.0)),       # frame 1
                    ((-6.0, -4.0), (-3.0, -7.0), (3.0, -7.0), (5.0, -5.0), (5.0, 6.0), (2.0, 9.0), (-5.0, 9.0), (-6.0, 8.0)),       # frame 2
                    ((-6.0, -4.0), (-3.0, -7.0), (3.0, -7.0), (5.0, -5.0), (5.0, 6.0), (1.0, 10.0), (-5.0, 10.0), (-6.0, 9.0)),     # frame 3
                ], 
                # up
                [
                    ((-5.0, -5.0), (-3.0, -7.0), (3.0, -7.0), (6.0, -4.0), (6.0, 8.0), (4.0, 10.0), (0.0, 10.0), (-5.0, 5.0)),      # frame 0
                    ((-5.0, -5.0), (-3.0, -7.0), (3.0, -7.0), (6.0, -4.0), (6.0, 7.0), (4.0, 9.0), (-1.0, 9.0), (-5.0, 5.0)),       # frame 1
                    ((-5.0, -5.0), (-3.0, -7.0), (3.0, -7.0), (6.0, -4.0), (6.0, 7.0), (4.0, 9.0), (-2.0, 9.0), (-5.0, 6.0)),       # frame 2
                    ((-5.0, -5.0), (-3.0, -7.0), (3.0, -7.0), (6.0, -4.0), (6.0, 8.0), (4.0, 10.0), (-1.0, 10.0), (-5.0, 6.0)),     # frame 3
                ], 
                # right
                [
                    ((-5.0, -5.0), (-3.0, -7.0), (3.0, -7.0), (4.0, -6.0), (4.0, 6.0), (0.0, 10.0), (-2.0, 10.0), (-5.0, 7.0)),     # frame 0
                    ((-5.0, -5.0), (-3.0, -7.0), (3.0, -7.0), (4.0, -6.0), (4.0, 6.0), (1.0, 9.0), (-2.0, 9.0), (-5.0, 6.0)),       # frame 1
                    ((-5.0, -5.0), (-3.0, -7.0), (3.0, -7.0), (4.0, -6.0), (4.0, 7.0), (2.0, 9.0), (-2.0, 9.0), (-5.0, 6.0)),       # frame 2
                    ((-5.0, -5.0), (-3.0, -7.0), (3.0, -7.0), (4.0, -6.0), (4.0, 7.0), (1.0, 10.0), (-2.0, 10.0), (-5.0, 7.0)),     # frame 3
                ], 
                # left 
                [
                    ((-4.0, -6.0), (-3.0, -7.0), (3.0, -7.0), (5.0, -5.0), (5.0, 7.0), (2.0, 10.0), (0.0, 10.0), (-4.0, 6.0)),      # frame 0
                    ((-4.0, -6.0), (-3.0, -7.0), (3.0, -7.0), (5.0, -5.0), (5.0, 6.0), (2.0, 9.0), (-1.0, 9.0), (-4.0, 6.0)),       # frame 1
                    ((-4.0, -6.0), (-3.0, -7.0), (3.0, -7.0), (5.0, -5.0), (5.0, 6.0), (2.0, 9.0), (-2.0, 9.0), (-4.0, 7.0)),       # frame 2
                    ((-4.0, -6.0), (-3.0, -7.0), (3.0, -7.0), (5.0, -5.0), (5.0, 7.0), (2.0, 10.0), (-1.0, 10.0), (-4.0, 7.0)),     # frame 3
                ], 
            ], 
            # walk 
            [
                # down
                [
                    ((-6.0, -4.0), (-3.0, -7.0), (3.0, -7.0), (4.0, -6.0), (4.0, 7.0), (1.0, 10.0), (-5.0, 10.0), (-6.0, 9.0)),     # frame 0
                    ((-6.0, -4.0), (-3.0, -7.0), (3.0, -7.0), (5.0, -5.0), (5.0, 5.0), (0.0, 10.0), (-5.0, 10.0), (-6.0, 9.0)),     # frame 1
                    ((-6.0, -4.0), (-3.0, -7.0), (3.0, -7.0), (4.0, -6.0), (4.0, 7.0), (1.0, 10.0), (-5.0, 10.0), (-6.0, 9.0)),     # frame 2
                    ((-6.0, -4.0), (-3.0, -7.0), (3.0, -7.0), (5.0, -5.0), (5.0, 5.0), (0.0, 10.0), (-5.0, 10.0), (-6.0, 9.0)),     # frame 3
                ],
                # up
                [
                    ((-4.0, -6.0), (-3.0, -7.0), (3.0, -7.0), (6.0, -4.0), (6.0, 8.0), (4.0, 10.0), (-1.0, 10.0), (-4.0, 7.0)),     # frame 0
                    ((-4.0, -6.0), (-3.0, -7.0), (3.0, -7.0), (6.0, -4.0), (6.0, 8.0), (4.0, 10.0), (0.0, 10.0), (-4.0, 6.0)),      # frame 1
                    ((-4.0, -6.0), (-3.0, -7.0), (3.0, -7.0), (6.0, -4.0), (6.0, 8.0), (4.0, 10.0), (-1.0, 10.0), (-4.0, 7.0)),     # frame 2
                    ((-4.0, -6.0), (-3.0, -7.0), (3.0, -7.0), (6.0, -4.0), (6.0, 8.0), (4.0, 10.0), (0.0, 10.0), (-4.0, 6.0)),      # frame 3
                ],
                # right
                [
                    ((-5.0, -5.0), (-3.0, -7.0), (3.0, -7.0), (5.0, -5.0), (5.0, 6.0), (1.0, 10.0), (-3.0, 10.0), (-5.0, 8.0)),     # frame 0
                    ((-5.0, -5.0), (-3.0, -7.0), (3.0, -7.0), (4.0, -6.0), (4.0, 6.0), (0.0, 10.0), (-2.0, 10.0), (-5.0, 7.0)),     # frame 1
                    ((-5.0, -5.0), (-3.0, -7.0), (3.0, -7.0), (4.0, -6.0), (4.0, 7.0), (1.0, 10.0), (-1.0, 10.0), (-5.0, 6.0)),     # frame 2
                    ((-5.0, -5.0), (-3.0, -7.0), (3.0, -7.0), (4.0, -6.0), (4.0, 6.0), (0.0, 10.0), (-2.0, 10.0), (-5.0, 7.0)),     # frame 3
                ],
                # left 
                [
                    ((-5.0, -5.0), (-3.0, -7.0), (3.0, -7.0), (5.0, -5.0), (5.0, 8.0), (3.0, 10.0), (-1.0, 10.0), (-5.0, 6.0)),     # frame 0
                    ((-4.0, -6.0), (-3.0, -7.0), (3.0, -7.0), (5.0, -5.0), (5.0, 7.0), (2.0, 10.0), (0.0, 10.0), (-4.0, 6.0)),      # frame 1
                    ((-4.0, -6.0), (-3.0, -7.0), (3.0, -7.0), (5.0, -5.0), (5.0, 6.0), (1.0, 10.0), (-1.0, 10.0), (-4.0, 7.0)),     # frame 2
                    ((-4.0, -6.0), (-3.0, -7.0), (3.0, -7.0), (5.0, -5.0), (5.0, 7.0), (2.0, 10.0), (0.0, 10.0), (-4.0, 6.0)),      # frame 3
                ],
            ], 
            # attack
            [
                # down
                [
                    ((-10.0, -12.0), (-8.0, -14.0), (5.0, -14.0), (13.0, -6.0), (13.0, -1.0), (5.0, 7.0), (-3.0, 7.0), (-10.0, 0.0)),   # frame 0
                    ((-15.0, -7.0), (-8.0, -14.0), (4.0, -14.0), (8.0, -10.0), (8.0, 2.0), (3.0, 7.0), (-4.0, 7.0), (-15.0, -4.0)),     # frame 1
                    ((-16.0, -6.0), (-10.0, -12.0), (-2.0, -12.0), (5.0, -5.0), (5.0, 5.0), (3.0, 7.0), (-9.0, 7.0), (-16.0, 0.0)),     # frame 2
                    ((-16.0, -1.0), (-10.0, -7.0), (3.0, -7.0), (5.0, -5.0), (5.0, 5.0), (3.0, 7.0), (-13.0, 7.0), (-16.0, 4.0)),       # frame 3
                ], 
                # up
                [
                    ((-13.0, 1.0), (-5.0, -7.0), (3.0, -7.0), (10.0, 0.0), (10.0, 12.0), (8.0, 14.0), (-5.0, 14.0), (-13.0, 6.0)),      # frame 0
                    ((-8.0, -2.0), (-3.0, -7.0), (4.0, -7.0), (15.0, 4.0), (15.0, 7.0), (8.0, 14.0), (-4.0, 14.0), (-8.0, 10.0)),       # frame 1
                    ((-4.0, -6.0), (-3.0, -7.0), (9.0, -7.0), (16.0, 0.0), (16.0, 6.0), (10.0, 12.0), (1.0, 12.0), (-4.0, 7.0)),        # frame 2
                    ((-4.0, -6.0), (-3.0, -7.0), (13.0, -7.0), (16.0, -4.0), (16.0, 1.0), (9.0, 8.0), (-3.0, 8.0), (-4.0, 7.0)),        # frame 3
                ], 
                # right 
                [
                    ((-8.0, -2.0), (4.0, -14.0), (11.0, -14.0), (15.0, -10.0), (15.0, 0.0), (8.0, 7.0), (-6.0, 7.0), (-8.0, 5.0)),      # frame 0
                    ((-4.0, -11.0), (0.0, -15.0), (11.0, -15.0), (15.0, -11.0), (15.0, -2.0), (6.0, 7.0), (-2.0, 7.0), (-4.0, 5.0)),    # frame 1
                    ((-9.0, -12.0), (-7.0, -14.0), (0.0, -14.0), (5.0, -9.0), (5.0, 6.0), (4.0, 7.0), (-2.0, 7.0), (-9.0, 0.0)),        # frame 2
                    ((-9.0, -9.0), (-8.0, -10.0), (0.0, -10.0), (5.0, -5.0), (5.0, 6.0), (4.0, 7.0), (-2.0, 7.0), (-9.0, 0.0)),         # frame 3
                ], 
                # left 
                [
                    ((-15.0, -10.0), (-11.0, -14.0), (-4.0, -14.0), (8.0, -2.0), (8.0, 5.0), (6.0, 7.0), (-8.0, 7.0), (-15.0, 0.0)),    # frame 0
                    ((-15.0, -10.0), (-10.0, -15.0), (0.0, -15.0), (4.0, -11.0), (4.0, 5.0), (2.0, 7.0), (-6.0, 7.0), (-15.0, -2.0)),   # frame 1
                    ((-5.0, -9.0), (0.0, -14.0), (7.0, -14.0), (9.0, -12.0), (9.0, 0.0), (2.0, 7.0), (-4.0, 7.0), (-5.0, 6.0)),         # frame 2
                    ((-5.0, -5.0), (0.0, -10.0), (8.0, -10.0), (9.0, -9.0), (9.0, 0.0), (2.0, 7.0), (-4.0, 7.0), (-5.0, 6.0)),          # frame 3
                ], 
            ], 
        ]



config = Config()