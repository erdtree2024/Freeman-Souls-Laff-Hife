"""
Platformer Game
"""
import arcade

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "bean-former"


# Constants used to scale our sprites from their original size

CHARACTER_SCALING = .25

TILE_SCALING = 5
CRATE_SCALING = 0.2



class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)


        # These are 'lists' that keep track of our sprites. Each sprite should

        # go into a list.

        self.wall_list = None

        self.player_list = None


        # Separate variable that holds the player sprite
        self.player_sprite = None

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)


    def setup(self):

        """Set up the game here. Call this function to restart the game."""

        # Create the Sprite lists

        self.player_list = arcade.SpriteList()

        self.wall_list = arcade.SpriteList(use_spatial_hash=True)



        # Set up the player, specifically placing it at these coordinates.

        image_source = "resources/GordonFreemanCharacter.png"

        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)

        self.player_sprite.center_x = 64

        self.player_sprite.center_y = 128

        self.player_list.append(self.player_sprite)



        # Create the ground

        # This shows using a loop to place multiple sprites horizontally

        for x in range(0, 1250, 64):

            wall = arcade.Sprite("resources/middle_edge.png", TILE_SCALING)

            wall.center_x = x

            wall.center_y = 32

            self.wall_list.append(wall)



        # Put some crates on the ground

        # This shows using a coordinate list to place sprites

        coordinate_list = [[512, 96], [256, 96], [768, 96]]



        for coordinate in coordinate_list:

            # Add a crate on the ground

            wall = arcade.Sprite(

                "resources/Crate_Transparent.png", CRATE_SCALING

            )

            wall.position = coordinate

            self.wall_list.append(wall)


    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()


        # Draw our sprites

        self.wall_list.draw()

        self.player_list.draw()



def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()