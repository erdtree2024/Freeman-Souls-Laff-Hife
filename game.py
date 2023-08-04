"""
Platformer Game

CONTROLS:
Spacebar = Jump
A, D = Left, Right
"""

import timeit

import arcade
import time

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "bean-former"
COIN_SCALING = 0.15

# Constants used to scale our sprites from their original size

CHARACTER_SCALING = .25

TILE_SCALING = 5
CRATE_SCALING = 0.2

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5

GRAVITY = .3
PLAYER_JUMP_SPEED = 7

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # A Camera that can be used for scrolling the screen
        self.camera = None
        # These are 'lists' that keep track of our sprites. Each sprite should
        # A Camera that can be used to draw GUI elements
        self.gui_camera = None

        # Keep track of the score
        self.score = 0
        # go into a list.

        self.scene = None

        self.physics_engine = None

        # Separate variable that holds the player sprite
        self.player_sprite = None
        # Load sounds
        self.collect_coin_sound = arcade.load_sound("resources/bruh-sound-effect-2.mp3")
        self.jump_sound = arcade.load_sound("resources/Punch.wav")
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)


    def setup(self):
        # Set up the Camera
        self.camera = arcade.Camera(self.width, self.height)

        """Set up the game here. Call this function to restart the game."""

        # Create the Sprite lists
        # Set up the GUI Camera
        self.gui_camera = arcade.Camera(self.width, self.height)

        # Keep track of the score
        self.score = 0
        self.scene = arcade.Scene()

        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)

        # Set up the player, specifically placing it at these coordinates.

        image_source = "resources/GordonFreemanCharacter.png"

        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)

        self.player_sprite.center_x = 64

        self.player_sprite.center_y = 128

        self.scene.add_sprite("Player", self.player_sprite)
        # Use a loop to place some coins for our character to pick up
        for x in range(128, 1250, 256):
            coin = arcade.Sprite("resources/ELIJAHFATHER.png", COIN_SCALING)
            coin.center_x = x
            coin.center_y = 96
            self.scene.add_sprite("Coins", coin)


        # Create the ground

        # This shows using a loop to place multiple sprites horizontally

        for x in range(0, 1600, 64):

            wall = arcade.Sprite("resources/middle_edge.png", TILE_SCALING)
            wall2 = arcade.Sprite("resources/middle_edge.png", TILE_SCALING)

            wall.center_x = x

            wall.center_y = 32

            wall2.center_x = x+1900

            wall2.center_y = 100

            self.scene.add_sprite("Walls", wall)
            self.scene.add_sprite ("Walls", wall2)




        # Put some crates on the ground

        # This shows using a coordinate list to place sprites

        coordinate_list = [[512, 96], [256, 96], [768, 96]]



        for coordinate in coordinate_list:

            # Add a crate on the ground

            wall = arcade.Sprite(

                "resources/Crate_Transparent.png", CRATE_SCALING

            )

            wall.position = coordinate

            self.scene.add_sprite("Walls", wall)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["Walls"]
        )
        self.physics_engine.enable_multi_jump(2)



    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Activate the game camera
        self.camera.use()

        # Draw our Scene
        self.scene.draw()


        # Activate the GUI camera before drawing GUI elements

        self.gui_camera.use()



        # Draw our score on the screen, scrolling it with the viewport

        score_text = f"Score: {self.score}"

        arcade.draw_text(

            score_text,

            530,

            660,

            arcade.csscolor.WHITE,

            40,

            font_name="Kenney Blocks"

        )
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        if key == arcade.key.UP or key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
                self.physics_engine.increment_jump_counter()
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED


    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def center_camera_to_player(self):

        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)

        screen_center_y = self.player_sprite.center_y - (

            self.camera.viewport_height / 2

        )



        # Don't let camera travel past 0

        if screen_center_x < 0:

            screen_center_x = 0

        if screen_center_y < 0:

            screen_center_y = 0

        player_centered = screen_center_x, screen_center_y



        self.camera.move_to(player_centered)


    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()


        # Position the camera

        self.center_camera_to_player()
        # See if we hit any coins
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Coins"]
        )

        # Loop through each coin we hit (if any) and remove it
        for coin in coin_hit_list:
            # Remove the coin
            coin.remove_from_sprite_lists()
            # Play a sound
            arcade.play_sound(self.collect_coin_sound)
            self.score += 1

def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()