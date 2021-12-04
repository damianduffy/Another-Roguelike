from __future__ import annotations
import random
from typing import TYPE_CHECKING

import arcade

from config import config

if TYPE_CHECKING:
    from arcade import Texture


class BaseEntity(arcade.Sprite):
    def __init__(
        self, 
        filename: str = None, 
        scale: float = config.SPRITE_SCALING, 
        image_x: float = 0, 
        image_y: float = 0, 
        image_width: float = 0, 
        image_height: float = 0, 
        center_x: float = 0, 
        center_y: float = 0, 
        repeat_count_x: int = 1, 
        repeat_count_y: int = 1, 
        flipped_horizontally: bool = False, 
        flipped_vertically: bool = False, 
        flipped_diagonally: bool = False, 
        hit_box_algorithm: str = "Simple", 
        hit_box_detail: float = 4.5, 
        texture: Texture = None, 
        angle: float = 0, 
        max_hp=100, 
        hp:int=100, 
    ):
        super().__init__(
            filename=filename, 
            scale=scale, 
            image_x=image_x, 
            image_y=image_y, 
            image_width=image_width, 
            image_height=image_height, 
            center_x=center_x, 
            center_y=center_y, 
            repeat_count_x=repeat_count_x, 
            repeat_count_y=repeat_count_y, 
            flipped_horizontally=flipped_horizontally, 
            flipped_vertically=flipped_vertically, 
            flipped_diagonally=flipped_diagonally, 
            hit_box_algorithm=hit_box_algorithm, 
            hit_box_detail=hit_box_detail, 
            texture=texture, 
            angle=angle
        )
        self.max_hp=max_hp
        self.hp=hp
        self.invincible_frame_counter=0
    
    @property
    def max_hp(self):
        return self._max_hp
    
    @max_hp.setter
    def max_hp(self, value):
        self._max_hp = value
    
    @property
    def hp(self):
        return self._hp
    
    @hp.setter
    def hp(self, value):
        # Keep the HP within the allowed range (0 to max)
        self._hp = max(0, min(value, self.max_hp))
    
    def on_draw(self):
        # draw the current hp above player
        arcade.draw_rectangle_outline(
            center_x=self.center_x, 
            center_y=self.center_y + 16 * self.scale, 
            width=16 * self.scale, 
            height=4 * self.scale, 
            color=(255, 255, 255), 
            border_width=1)
        
        max_hp_width = 14 * self.scale
        hp_width_percent = self.hp / self.max_hp
        hp_width = max_hp_width * hp_width_percent

        arcade.draw_rectangle_filled(
            center_x=self.center_x - ((max_hp_width - hp_width) // 2), 
            center_y=self.center_y + 16 * self.scale, 
            width=hp_width,
            height=2 * self.scale, 
            color=(0, 255, 0))
    
    def attacked(self, damage):
        if self.invincible_frame_counter <= 0 and damage > 0:
            self.hp -= damage
            self.invincible_frame_counter = 0.5   
    
    def on_update(self, delta_time):
        if self.invincible_frame_counter != 0:
            self.invincible_frame_counter -= delta_time
            if self.invincible_frame_counter < 0:
                # Reset to 0 ... ie. no longer invincible
                self.invincible_frame_counter = 0


class Player(BaseEntity):
    def __init__(self):
        super().__init__(
            center_x = random.randrange(config.GRID_WIDTH) * config.TILE_SIZE, 
            center_y = random.randrange(config.GRID_HEIGHT) * config.TILE_SIZE, 
        )
        # Animation state tracking
        self.charactor_directions = ["down", "up", "right", "left"]
        self.direction_index = 0
        self.charactor_actions = ["idle", "walk", "attack"]
        self.action_index = 0
        self.max_frames = 4
        self.cur_frame = 0
        self.updates_per_frame = 5

        # Load textures
        self.walk_textures = []
        for action in self.charactor_actions:
            action_frames = []
            for direction in self.charactor_directions:
                animation_frames = []
                for i in range(self.max_frames):
                    texture = arcade.load_texture(f"assets/gfx/player/{action}_{direction}_{i}.png")
                    animation_frames.append(texture)
                action_frames.append(animation_frames)
            self.walk_textures.append(action_frames)
        self.texture = self.walk_textures[self.action_index][self.direction_index][self.cur_frame]
        
        # Track movement keys
        self.down_pressed = False
        self.up_pressed = False
        self.right_pressed = False
        self.left_pressed = False
        self.attack_pressed = False
        # Speed limit
        self.max_speed = 3.0
        # How fast we accelerate
        self.acceleration_rate = 0.2
        # How fast to slow down after we letr off the key
        self.friction = 0.06
        
        self.power = 7
        self.defense = 2

    def update_animation(self, delta_time: float = 1 / 60):
        # Attack animation
        if self.attack_pressed:
            if self.action_index != 2:
                # Set animation to attack action animations.
                self.action_index = 2
                self.cur_frame = 0
            if self.cur_frame >= self.max_frames * self.updates_per_frame:
                # attack animation has finished, return to idle animation.
                self.cur_frame = 0
                self.action_index = 1
                self.attack_pressed = False
            # Set the current animation frame for the attack.
            frame = self.cur_frame // self.updates_per_frame
            self.texture = self.walk_textures[self.action_index][self.direction_index][frame]
            self.cur_frame += 1
            # Update the hitbox to align with the attack animation.
            self.set_hit_box(config.player_hit_box_coords[self.action_index][self.direction_index][frame])
            return

        # Idle animation
        if self.change_x == 0 and self.change_y == 0:
            self.action_index = 0
            frame = self.cur_frame // self.updates_per_frame
            # Change the hitbox to match the idle animation frame.
            self.set_hit_box(config.player_hit_box_coords[self.action_index][self.direction_index][frame])
            return

        # Walking animation
        self.cur_frame += 1
        if self.cur_frame >= self.max_frames * self.updates_per_frame:
            # Cycle animation around to first frame.
            self.cur_frame = 0
        frame = self.cur_frame // self.updates_per_frame
        self.texture = self.walk_textures[self.action_index][self.direction_index][frame]
        # Change the hitbox to match the current walking animation frame.
        self.set_hit_box(config.player_hit_box_coords[self.action_index][self.direction_index][frame])
        
    def on_update(self, delta_time):
        """ Movement and game logic """
        # Add some friction
        if self.change_x > self.friction:
            self.change_x -= self.friction
        elif self.change_x < -self.friction:
            self.change_x += self.friction
        else:
            self.change_x = 0

        if self.change_y > self.friction:
            self.change_y -= self.friction
        elif self.change_y < -self.friction:
            self.change_y += self.friction
        else:
            self.change_y = 0

        # Apply acceleration based on the keys pressed
        if self.up_pressed and not self.down_pressed:
            self.change_y += self.acceleration_rate
            self.direction_index = 1
        elif self.down_pressed and not self.up_pressed:
            self.change_y += -self.acceleration_rate
            self.direction_index = 0
        if self.left_pressed and not self.right_pressed:
            self.change_x += -self.acceleration_rate
            self.direction_index = 3
        elif self.right_pressed and not self.left_pressed:
            self.change_x += self.acceleration_rate
            self.direction_index = 2

        # Cap the player speed
        if self.change_x > self.max_speed:
            self.change_x = self.max_speed
        elif self.change_x < -self.max_speed:
            self.change_x = -self.max_speed
        if self.change_y > self.max_speed:
            self.change_y = self.max_speed
        elif self.change_y < -self.max_speed:
            self.change_y = -self.max_speed
        
        # Decrement the invincibility frame counter, if it's currently running.
        if self.invincible_frame_counter != 0:
            self.invincible_frame_counter -= delta_time
            if self.invincible_frame_counter < 0:
                # Reset to 0 ... ie. no longer invincible
                self.invincible_frame_counter = 0

    def attack(self, enemy):
        damage = self.power         # Iterate on this by subtracting "target" defense to get "damage".
        enemy.attacked(damage)
        
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
        elif key == arcade.key.SPACE:
            self.attack_pressed = True
        
    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False


class Tree(BaseEntity):
    def __init__(
        self, 
        center_x = None, 
        center_y = None, 
    ):
        coords = self.random_coords(center_x, center_y)
        super().__init__(
            filename = "assets/gfx/tile_0055.png", 
            center_x=coords[0], 
            center_y=coords[1], 
        )
        
    def random_coords(self, x, y):
        if x is None or y is None:
            return (
                random.randrange(config.GRID_WIDTH) * config.TILE_SIZE, 
                random.randrange(config.GRID_HEIGHT) * config.TILE_SIZE, 
            )
        return (x * config.TILE_SIZE, y * config.TILE_SIZE)


class Monster(BaseEntity):
    def __init__(self):
        super().__init__(
            filename = "assets/gfx/tile_0009.png", 
            center_x = random.randrange(config.GRID_WIDTH) * config.TILE_SIZE, 
            center_y = random.randrange(config.GRID_HEIGHT) * config.TILE_SIZE, 
            hp = 20, 
            scale=4, 
        )