import arcade
from game import Game
from config import config


class MenuView(arcade.View):
    def on_show(self):
        self.background = arcade.load_texture("assets/gfx/menu_background.png")
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                    config.WINDOW_WIDTH, 
                                    config.WINDOW_HEIGHT,
                                    self.background)
        arcade.draw_text(
            "Dungeon Adventure", 
            30, 
            config.WINDOW_HEIGHT - 100,
            arcade.color.WHITE, 
            font_size=30, 
            anchor_x="left")
        arcade.draw_text(
            "Press <SPACE> to start game", 
            30, 
            config.WINDOW_HEIGHT - 150,
            arcade.color.GRAY, 
            font_size=20, 
            anchor_x="left")
        arcade.draw_text(
            "Press <ESC> to exit", 
            30, 
            config.WINDOW_HEIGHT - 180,
            arcade.color.GRAY, 
            font_size=20, 
            anchor_x="left")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.SPACE:   
            game = Game()
            self.window.show_view(game)
            game.setup()
        elif key == arcade.key.ESCAPE:
            # Quit the game
            self.window.close()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game = Game()
        self.window.show_view(game)
        game.setup()


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.text_x = self.game_view.view_left + (config.WINDOW_WIDTH // 2)
        self.text_y = self.game_view.view_bottom + (config.WINDOW_HEIGHT // 2)

    def on_show(self):
        pass
        #arcade.set_background_color(arcade.color.ORANGE)

    def on_draw(self):
        arcade.draw_rectangle_filled(
            center_x=self.text_x,
            center_y=self.text_y + 10,
            width=300,
            height=200,
            color=arcade.color.BLACK
        )
        # View title
        arcade.draw_text("GAME PAUSED",
                        self.text_x - 200, self.text_y + 30, 
                        arcade.color.WHITE, 
                        font_size=20, 
                        width=400, 
                        align="center")
        # Show tip to return or reset
        arcade.draw_text("Press 'P' to return",
                        self.text_x - 200, self.text_y, 
                        arcade.color.WHITE, 
                        font_size=18, 
                        width=400, 
                        align="center")
        arcade.draw_text("Press Enter to reset level",
                        self.text_x - 200, self.text_y - 30, 
                        arcade.color.WHITE, 
                        font_size=18, 
                        width=400, 
                        align="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.P:   
            # resume game
            self.window.show_view(self.game_view)
        elif key == arcade.key.ENTER:  # reset game
            # stop the previous game view's music
            # TBC - should be a check here to confirm if music is None
            if self.game_view.music:
                self.game_view.music.stop(self.game_view.current_player)
            # Create new game, assign it to the window and setup
            game = Game()
            self.window.show_view(game)
            game.setup()


class QuitView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.text_x = self.game_view.view_left + (config.WINDOW_WIDTH // 2)
        self.text_y = self.game_view.view_bottom + (config.WINDOW_HEIGHT // 2)

    def on_show(self):
        arcade.set_background_color(arcade.color.RED)

    def on_draw(self):
        arcade.start_render()

        # Draw player, for effect, on pause screen.
        # The previous View (GameView) was passed in
        # and saved in self.game_view.
        player_sprite = self.game_view.player_sprite
        player_sprite.draw()

        # draw an orange filter over him
        arcade.draw_lrtb_rectangle_filled(left=player_sprite.left,
                                          right=player_sprite.right,
                                          top=player_sprite.top,
                                          bottom=player_sprite.bottom,
                                          color=arcade.color.RED + (200,))

        # View title
        arcade.draw_text("QUIT GAME?",
                        self.text_x - 200, self.text_y, 
                        arcade.color.WHITE, 
                        font_size=20, 
                        width=400, 
                        align="center")
        # Show tip for keyboard shortcuts
        arcade.draw_text("(Y/N)",
                        self.text_x - 200, self.text_y - 30, 
                        arcade.color.WHITE, 
                        font_size=18, 
                        width=400, 
                        align="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.N:   
            # resume game
            self.window.show_view(self.game_view)
        elif key == arcade.key.Y:
            # Quit the game
            self.window.close()


'''
Game-over screen displayed when player dies
'''
class GameOverView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.text_x = self.game_view.view_left + (config.WINDOW_WIDTH // 2)
        self.text_y = self.game_view.view_bottom + (config.WINDOW_HEIGHT // 2)

    def on_draw(self):
        arcade.draw_rectangle_filled(
            center_x=self.text_x,
            center_y=self.text_y,
            width=300,
            height=209,
            color=arcade.color.BLACK
        )
        # View title
        arcade.draw_text("GAME OVER",
                        self.text_x - 200, self.text_y + 30, 
                        arcade.color.WHITE, 
                        font_size=20, 
                        width=400, 
                        align="center")
        # Show player score
        arcade.draw_text(f"Score: {self.game_view.score:.0f}",
                        self.text_x - 200, self.text_y, 
                        arcade.color.WHITE, 
                        font_size=18, 
                        width=400, 
                        align="center")
        # Show tip to exit or restart
        arcade.draw_text("Press <SPACE> to restart",
                        self.text_x - 200, self.text_y - 40, 
                        arcade.color.GRAY, 
                        font_size=18, 
                        width=400, 
                        align="center")
        arcade.draw_text("Press <ESC> to quit",
                        self.text_x - 200, self.text_y - 70, 
                        arcade.color.GRAY, 
                        font_size=18, 
                        width=400, 
                        align="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:   
            # Quit the game
            self.window.close()
        elif key == arcade.key.SPACE:  # reset game
            # stop the previous game view's music
            # TBC - should be a check here to confirm if music is None
            if self.game_view.music:
                self.game_view.music.stop(self.game_view.current_player)
            # Create new game, assign it to the window and setup
            game = Game()
            self.window.show_view(game)
            game.setup()


'''
Level end screen displayed when player finishes level
'''
class LevelEndView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.text_x = self.game_view.view_left + (config.WINDOW_WIDTH // 2)
        self.text_y = self.game_view.view_bottom + (config.WINDOW_HEIGHT // 2)

    def on_draw(self):
        arcade.draw_rectangle_filled(
            center_x=self.text_x,
            center_y=self.text_y,
            width=300,
            height=190,
            color=arcade.color.BLACK
        )
        # View title
        arcade.draw_text("Level Complete!!!",
                        self.text_x - 200, self.text_y + 30, 
                        arcade.color.WHITE, 
                        font_size=20, 
                        width=400, 
                        align="center")
        # Show player score
        arcade.draw_text(f"Score: {self.game_view.score:.0f}",
                        self.text_x - 200, self.text_y, 
                        arcade.color.WHITE, 
                        font_size=18, 
                        width=400, 
                        align="center")
        # Show tip to exit or restart
        arcade.draw_text("Press <SPACE> to continue",
                        self.text_x - 200, self.text_y - 40, 
                        arcade.color.GRAY, 
                        font_size=18, 
                        width=400, 
                        align="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.SPACE:  # reset game
            # stop the previous game view's music
            # TBC - should be a check here to confirm if music is None
            if self.game_view.music:
                self.game_view.music.stop(self.game_view.current_player)
            # Create new game, assign it to the window and setup
            game = Game()
            self.window.show_view(game)
            game.setup()