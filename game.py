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


# Constants used to scale our sprites from their original size

CHARACTER_SCALING = .25

TILE_SCALING = 5
CRATE_SCALING = 0.2

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5

GRAVITY = 1
PLAYER_JUMP_SPEED = 7

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)


        # These are 'lists' that keep track of our sprites. Each sprite should

        # go into a list.

        self.scene = None

        self.physics_engine = None


        # Separate variable that holds the player sprite
        self.player_sprite = None

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)


    def setup(self):

        """Set up the game here. Call this function to restart the game."""

        # Create the Sprite lists

        self.scene = arcade.Scene()

        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)

        # Set up the player, specifically placing it at these coordinates.

        image_source = "resources/GordonFreemanCharacter.png"

        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)

        self.player_sprite.center_x = 64

        self.player_sprite.center_y = 128

        self.scene.add_sprite("Player", self.player_sprite)



        # Create the ground

        # This shows using a loop to place multiple sprites horizontally

        for x in range(0, 1250, 64):

            wall = arcade.Sprite("resources/middle_edge.png", TILE_SCALING)

            wall.center_x = x

            wall.center_y = 32

            self.scene.add_sprite("Walls", wall)




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



    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()
        self.scene.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        if key == arcade.key.UP or key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
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

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()

def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()