from __future__ import annotations

from typing import TYPE_CHECKING, Tuple
import random
import math

import arcade

from entities import BaseEntity, Tree


class Room:
    """ A room """
    def __init__(self, r, c, h, w):
        self.row = r
        self.col = c
        self.height = h
        self.width = w


class RLDungeonGenerator:
    """ Generate the dungeon """
    def __init__(self, config):
        """ Create the board """
        self.MAX = 15  # Cutoff for when we want to stop dividing sections
        self.width = config.GRID_WIDTH
        self.height = config.GRID_HEIGHT
        self.leaves = []
        self.dungeon = []
        self.rooms = []
        self.WALL_SPRITE_SCALING = config.WALL_SPRITE_SCALING
        self.WALL_SPRITE_SIZE = config.WALL_SPRITE_SIZE
        self.AREA_WIDTH = config.AREA_WIDTH
        self.AREA_HEIGHT = config.AREA_HEIGHT

        for h in range(self.height):
            row = []
            for w in range(self.width):
                row.append('#')

            self.dungeon.append(row)

    def random_split(self, min_row, min_col, max_row, max_col):
        # We want to keep splitting until the sections get down to the threshold
        seg_height = max_row - min_row
        seg_width = max_col - min_col

        if seg_height < self.MAX and seg_width < self.MAX:
            self.leaves.append((min_row, min_col, max_row, max_col))
        elif seg_height < self.MAX <= seg_width:
            self.split_on_vertical(min_row, min_col, max_row, max_col)
        elif seg_height >= self.MAX > seg_width:
            self.split_on_horizontal(min_row, min_col, max_row, max_col)
        else:
            if random.random() < 0.5:
                self.split_on_horizontal(min_row, min_col, max_row, max_col)
            else:
                self.split_on_vertical(min_row, min_col, max_row, max_col)

    def split_on_horizontal(self, min_row, min_col, max_row, max_col):
        split = (min_row + max_row) // 2 + random.choice((-2, -1, 0, 1, 2))
        self.random_split(min_row, min_col, split, max_col)
        self.random_split(split + 1, min_col, max_row, max_col)

    def split_on_vertical(self, min_row, min_col, max_row, max_col):
        split = (min_col + max_col) // 2 + random.choice((-2, -1, 0, 1, 2))
        self.random_split(min_row, min_col, max_row, split)
        self.random_split(min_row, split + 1, max_row, max_col)

    def carve_rooms(self):
        for leaf in self.leaves:
            # We don't want to fill in every possible room or the
            # dungeon looks too uniform
            if random.random() > 0.80:
                continue
            section_width = leaf[3] - leaf[1]
            section_height = leaf[2] - leaf[0]

            # The actual room's height and width will be 60-100% of the
            # available section.
            room_width = round(random.randrange(60, 100) / 100 * section_width)
            room_height = round(random.randrange(60, 100) / 100 * section_height)

            # If the room doesn't occupy the entire section we are carving it from,
            # 'jiggle' it a bit in the square
            if section_height > room_height:
                room_start_row = leaf[0] + random.randrange(section_height - room_height)
            else:
                room_start_row = leaf[0]

            if section_width > room_width:
                room_start_col = leaf[1] + random.randrange(section_width - room_width)
            else:
                room_start_col = leaf[1]

            self.rooms.append(Room(room_start_row, room_start_col, room_height, room_width))
            for r in range(room_start_row, room_start_row + room_height):
                for c in range(room_start_col, room_start_col + room_width):
                    # Select the correct wall or floor for different parts of the room.
                    if r == room_start_row:
                        if c == room_start_col:
                            self.dungeon[r][c] = 'sw'
                        elif c == room_start_col + room_width - 1:
                            self.dungeon[r][c] = 'se'
                        else:
                            self.dungeon[r][c] = 'hr'
                    elif r == room_start_row + room_height - 1:
                        if c == room_start_col:
                            self.dungeon[r][c] = 'nw'
                        elif c == room_start_col + room_width - 1:
                            self.dungeon[r][c] = 'ne'
                        else:
                            self.dungeon[r][c] = 'hr'
                    else:
                        if c == room_start_col or c == room_start_col + room_width - 1:
                            self.dungeon[r][c] = 'vr'
                        else:
                            self.dungeon[r][c] = '.'

    @staticmethod
    def are_rooms_adjacent(room1, room2):
        """ See if two rooms are next to each other. """
        adj_rows = []
        adj_cols = []
        for r in range(room1.row, room1.row + room1.height):
            if room2.row <= r < room2.row + room2.height:
                adj_rows.append(r)

        for c in range(room1.col, room1.col + room1.width):
            if room2.col <= c < room2.col + room2.width:
                adj_cols.append(c)

        return adj_rows, adj_cols

    @staticmethod
    def distance_between_rooms(room1, room2):
        """ Get the distance between two rooms """
        centre1 = (room1.row + room1.height // 2, room1.col + room1.width // 2)
        centre2 = (room2.row + room2.height // 2, room2.col + room2.width // 2)

        return math.sqrt((centre1[0] - centre2[0]) ** 2 + (centre1[1] - centre2[1]) ** 2)

    def carve_corridor_between_rooms(self, room1, room2):
        """ Make a corridor between rooms """
        if room2[2] == 'rows':
            row = random.choice(room2[1])
            # Figure out which room is to the left of the other
            if room1.col + room1.width < room2[0].col:
                start_col = room1.col + room1.width
                end_col = room2[0].col
            else:
                start_col = room2[0].col + room2[0].width
                end_col = room1.col
            for c in range(start_col, end_col):
                self.dungeon[row][c] = '.'

            if end_col - start_col >= 4:
                self.dungeon[row][start_col] = '+'
                self.dungeon[row][end_col - 1] = '+'
            elif start_col == end_col - 1:
                self.dungeon[row][start_col] = '+'
        else:
            col = random.choice(room2[1])
            # Figure out which room is above the other
            if room1.row + room1.height < room2[0].row:
                start_row = room1.row + room1.height
                end_row = room2[0].row
            else:
                start_row = room2[0].row + room2[0].height
                end_row = room1.row

            for r in range(start_row, end_row):
                self.dungeon[r][col] = '.'

            if end_row - start_row >= 4:
                self.dungeon[start_row][col] = '+'
                self.dungeon[end_row - 1][col] = '+'
            elif start_row == end_row - 1:
                self.dungeon[start_row][col] = '+'

    def find_closest_unconnect_groups(self, groups, room_dict):
        """
        Find two nearby rooms that are in difference groups, draw
        a corridor between them and merge the groups
        """

        shortest_distance = 99999
        start = None
        start_group = None
        nearest = None

        for group in groups:
            for room in group:
                key = (room.row, room.col)
                for other in room_dict[key]:
                    if not other[0] in group and other[3] < shortest_distance:
                        shortest_distance = other[3]
                        start = room
                        nearest = other
                        start_group = group

        self.carve_corridor_between_rooms(start, nearest)

        # Merge the groups
        other_group = None
        for group in groups:
            if nearest[0] in group:
                other_group = group
                break

        start_group += other_group
        groups.remove(other_group)

    def connect_rooms(self):
        """
        Build a dictionary containing an entry for each room. Each bucket will
        hold a list of the adjacent rooms, weather they are adjacent along rows or
        columns and the distance between them.

        Also build the initial groups (which start of as a list of individual rooms)
        """
        groups = []
        room_dict = {}
        for room in self.rooms:
            key = (room.row, room.col)
            room_dict[key] = []
            for other in self.rooms:
                other_key = (other.row, other.col)
                if key == other_key:
                    continue
                adj = self.are_rooms_adjacent(room, other)
                if len(adj[0]) > 0:
                    room_dict[key].append((other, adj[0], 'rows', self.distance_between_rooms(room, other)))
                elif len(adj[1]) > 0:
                    room_dict[key].append((other, adj[1], 'cols', self.distance_between_rooms(room, other)))

            groups.append([room])

        while len(groups) > 1:
            self.find_closest_unconnect_groups(groups, room_dict)

    def generate_map(self):
        """ Make the map """
        self.random_split(1, 1, self.height - 1, self.width - 1)
        self.carve_rooms()
        self.connect_rooms()

    def build_map(self):
        """ Add wall, door, etc. sprites to the generated map """
        wall_list = arcade.SpriteList(use_spatial_hash=True)
        for row in range(self.height):
            for column in range(self.width):
                value = self.dungeon[row][column]
                if value == '#':
                    wall = arcade.Sprite("assets/gfx/tile_0011.png", self.WALL_SPRITE_SCALING)
                    wall.center_x = column * self.WALL_SPRITE_SIZE + self.WALL_SPRITE_SIZE / 2
                    wall.center_y = row * self.WALL_SPRITE_SIZE + self.WALL_SPRITE_SIZE / 2
                    wall_list.append(wall)
                elif value == 'nw':
                    wall = arcade.Sprite("assets/gfx/tile_0090.png", self.WALL_SPRITE_SCALING)
                    wall.center_x = column * self.WALL_SPRITE_SIZE + self.WALL_SPRITE_SIZE / 2
                    wall.center_y = row * self.WALL_SPRITE_SIZE + self.WALL_SPRITE_SIZE / 2
                    wall_list.append(wall)
                elif value == 'ne':
                    wall = arcade.Sprite("assets/gfx/tile_0093.png", self.WALL_SPRITE_SCALING)
                    wall.center_x = column * self.WALL_SPRITE_SIZE + self.WALL_SPRITE_SIZE / 2
                    wall.center_y = row * self.WALL_SPRITE_SIZE + self.WALL_SPRITE_SIZE / 2
                    wall_list.append(wall)
                elif value == 'sw':
                    wall = arcade.Sprite("assets/gfx/tile_0096.png", self.WALL_SPRITE_SCALING)
                    wall.center_x = column * self.WALL_SPRITE_SIZE + self.WALL_SPRITE_SIZE / 2
                    wall.center_y = row * self.WALL_SPRITE_SIZE + self.WALL_SPRITE_SIZE / 2
                    wall_list.append(wall)
                elif value == 'se':
                    wall = arcade.Sprite("assets/gfx/tile_0099.png", self.WALL_SPRITE_SCALING)
                    wall.center_x = column * self.WALL_SPRITE_SIZE + self.WALL_SPRITE_SIZE / 2
                    wall.center_y = row * self.WALL_SPRITE_SIZE + self.WALL_SPRITE_SIZE / 2
                    wall_list.append(wall)
                elif value == 'hr':
                    wall = arcade.Sprite("assets/gfx/tile_0091.png", self.WALL_SPRITE_SCALING)
                    wall.center_x = column * self.WALL_SPRITE_SIZE + self.WALL_SPRITE_SIZE / 2
                    wall.center_y = row * self.WALL_SPRITE_SIZE + self.WALL_SPRITE_SIZE / 2
                    wall_list.append(wall)
                elif value == 'vr':
                    wall = arcade.Sprite("assets/gfx/tile_0094.png", self.WALL_SPRITE_SCALING)
                    wall.center_x = column * self.WALL_SPRITE_SIZE + self.WALL_SPRITE_SIZE / 2
                    wall.center_y = row * self.WALL_SPRITE_SIZE + self.WALL_SPRITE_SIZE / 2
                    wall_list.append(wall)
        
        return wall_list

    def place_player(self, player, wall_list, config):
        # Randomly place the player. If we are in a wall, repeat until we aren't.
        placed = False
        while not placed:
            
            # Get a position in line with the map grid
            x = random.randrange(config.GRID_WIDTH) * config.WALL_SPRITE_SIZE
            y = random.randrange(config.GRID_HEIGHT) * config.WALL_SPRITE_SIZE
            
            # Randomly position
            player.center_x = x
            player.center_y = y

            # Are we in a wall?
            walls_hit = arcade.check_for_collision_with_list(player, wall_list)
            if len(walls_hit) == 0:
                # Not in a wall! Success!
                placed = True


"""
Open world stuff
"""

class World:
    def __init__(self):
        self.tree_count:int = 20
        self.tree_list:list = []
    
    @property
    def tree_list(self):
        return self._tree_list
    
    @tree_list.setter
    def tree_list(self, new_list):
        self._tree_list = new_list
    
    def place_random_trees(self) -> list:
        for count in range(self.tree_count):
            self.tree_list.append(
                Tree()
            )
        return self.tree_list
    
    '''
    Generates a 'forest'.
    '''
    def generate_forest(self, start_coords: Tuple, radius: int=4):
        # start_coords is the position on the world_map where the top left of 
        # the forest starts. Radius is how many tiles the 'radius' of the forest is.
        # Get the center coordinates.
        center = (radius, radius)
        forest_density = 1.3    # from 1 upwards. 1 is zero probability of trees.
        # furthest_distance is used to work out probability of a tree
        furthest_distance = arcade.get_distance(center[0], center[1], 0, 0)
        for x in range((radius * 2) + 1):
            for y in range((radius * 2) + 1):
                # get the distance of each tile to the center of the forest.
                distance_to_center = arcade.get_distance(center[0], center[1], x, y)
                # closer to the center will have higher probability of a tree being placed.
                chance_of_tree = furthest_distance - distance_to_center
                dice_roll = random.randint(0, int(chance_of_tree))
                # Closer to 1 is less dense. Larger the number, denser the forest.
                if dice_roll > chance_of_tree // forest_density:
                    # Create Tree object and place it in correct coords for world.
                    tree = Tree(center_x=start_coords[0] + x, center_y=start_coords[1] + y)
                    self.tree_list.append(tree)