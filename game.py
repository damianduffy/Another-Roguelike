#!/usr/bin/env python3

"""
This example procedurally develops a random cave based on
Binary Space Partitioning (BSP)

For more information, see:
https://roguebasin.roguelikedevelopment.org/index.php?title=Basic_BSP_Dungeon_generation
https://github.com/DanaL/RLDungeonGenerator

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.procedural_caves_bsp
"""

import os

import arcade

from config import config
from entities import Monster, Player
import views
from procgen import World
from performance import FPSCounter      # Used if performance stats option is enabled.


class Game(arcade.View):
    """
    Main application class.
    """

    def __init__(self):
        super().__init__()

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.grid = None
        self.world_map = None
        self.enemy_list = None
        #self.world_objects = None
        self.player_list = None
        self.player_sprite = None
        self.view_bottom = 0
        self.view_left = 0
        self.physics_engine = None

        # FPS performance monitor
        self.fps = FPSCounter()
    
    def on_show(self):
        arcade.set_background_color(config.BACKGROUND_COLOR)

    def setup(self):
        """ Set up the game """
        self.world_map = arcade.SpriteList(use_spatial_hash=True)
        self.enemy_list = arcade.SpriteList(use_spatial_hash=False)
        #self.world_objects = arcade.SpriteList(use_spatial_hash=True)
        self.player_list = arcade.SpriteList()

        world = World()
        # Generate trees at random in world
        world.place_random_trees()
        #self.world_objects.extend(world.place_trees())
        #self.world_map.extend(world.place_random_trees())
        # Generate world forest(s).
        '''
        world.generate_forest((10, 10), 8)
        world.generate_forest((20, 20), 6)
        '''
        # Add the tree(s) and forest(s) to the world.
        self.world_map.extend(world.tree_list)

        # Create cave system using a 2D grid
        #dg = RLDungeonGenerator(config=config)
        '''
        dg.generate_map()

        # This is the simple-to-understand method. Each grid location
        # is a sprite.
        self.world_map = dg.build_map()
        '''
        # Set up the player
        self.player_sprite = Player()
        self.player_list.append(self.player_sprite)
        self.enemy_list.append(Monster())

        # Place the player randomly in the map
        #dg.place_player(self.player_sprite, self.world_map, config)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                         self.world_map)
        
    def on_draw(self):
        """ Render the screen. """

        # Start timing how long this takes for FPS performance stats
        self.fps.set_draw_start_time()

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Draw the sprites
        self.world_map.draw(pixelated=True)
        #self.world_objects.draw()
        self.enemy_list.draw(pixelated=True)
        self.player_list.draw(pixelated=True)
        # draw healthbar above enemy
        for entity in self.enemy_list:
            entity.on_draw()
        # draw healthbar above player
        self.player_sprite.on_draw()

        if config.SHOW_PERFORMANCE:
            # Draw hit boxes.
            self.player_sprite.draw_hit_box(arcade.color.RED, 3)
            # update timings for FPS performance stats
            self.fps.set_draw_time()
            self.fps.tick()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        self.player_sprite.on_key_press(key, modifiers)
        # Handle mid-game pause, menu, exit, etc.
        if key == arcade.key.ESCAPE:
            # pass self, the current view, to preserve this view's state
            quit_game = views.QuitView(self)
            self.window.show_view(quit_game)
        elif key == arcade.key.P:
            # pass self, the current view, to preserve this view's state
            pause = views.PauseView(self)
            self.window.show_view(pause)

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        self.player_sprite.on_key_release(key, modifiers)

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Start update timer
        self.fps.set_start_time()

        # Move the player
        #self.player_list.update()
        self.physics_engine.update()

        # update player animations
        self.player_sprite.on_update(delta_time)
        self.player_sprite.update_animation(delta_time)

        # update enemy sprites
        self.enemy_list.update()
        self.enemy_list.on_update(delta_time)

        player_collision_list = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)
        if len(player_collision_list) > 0:
            for enemy in player_collision_list:
                self.player_sprite.attack(enemy)

        # --- Manage Scrolling ---

        # Track if we need to change the viewport
        changed = False

        # Scroll left
        left_bndry = self.view_left + config.VIEWPORT_MARGIN
        if self.player_sprite.center_x < left_bndry:
            self.view_left -= left_bndry - self.player_sprite.center_x
            changed = True

        # Scroll right
        right_bndry = self.view_left + config.WINDOW_WIDTH - config.VIEWPORT_MARGIN
        if self.player_sprite.center_x > right_bndry:
            self.view_left += self.player_sprite.center_x - right_bndry
            changed = True

        # Scroll up
        top_bndry = self.view_bottom + config.WINDOW_HEIGHT - config.VIEWPORT_MARGIN
        if self.player_sprite.center_y > top_bndry:
            self.view_bottom += self.player_sprite.center_y - top_bndry
            changed = True

        # Scroll down
        bottom_bndry = self.view_bottom + config.VIEWPORT_MARGIN
        if self.player_sprite.center_y < bottom_bndry:
            self.view_bottom -= bottom_bndry - self.player_sprite.center_y
            changed = True

        if changed:
            arcade.set_viewport(self.view_left,
                                config.WINDOW_WIDTH + self.view_left,
                                self.view_bottom,
                                config.WINDOW_HEIGHT + self.view_bottom)

        # Performance stats
        if config.SHOW_PERFORMANCE:
            # Save the time it took to do this.
            self.fps.set_processing_time()
            # Total time program has been running.
            self.fps.set_total_program_time()
            # Get current FPS.
            if self.fps.time_since_last_reading():
                self.fps.set_last_reading()
                # It takes the program a while to "warm up", so the first
                # few seconds our readings will be off. So wait some time
                # before taking readings
                if self.fps.get_total_program_time() > 5 and \
                    self.fps.get_total_program_time() % 2 == 1:
                        # Get timings. Optionally can print to file.
                        self.fps.get_timings()
                        self.fps.update()


def main():
    """ Main function, start up window and run """
    window = arcade.Window(config.WINDOW_WIDTH, config.WINDOW_HEIGHT, config.WINDOW_TITLE, fullscreen=config.FULLSCREEN)
    # Start menu view
    menu_view = views.MenuView()
    window.show_view(menu_view)
    # Display everything
    arcade.run()


if __name__ == "__main__":
    main()