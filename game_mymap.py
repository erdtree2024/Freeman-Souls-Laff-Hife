"""
Platformer Game
"""
import arcade
import math
import os

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Laff-Hife: The Souls-Freeman Experience"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = .25
TILE_SCALING = 0.5
COIN_SCALING = 0.5

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 10
GRAVITY = .9
PLAYER_JUMP_SPEED = 15

SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

# Player starting position
PLAYER_START_X = 256
PLAYER_START_Y = 225

# Layer Names from our TileMap
LAYER_NAME_PLATFORMS = "Platforms"
LAYER_NAME_COINS = "Coins"
LAYER_NAME_FOREGROUND = "Foreground"
LAYER_NAME_BACKGROUND = "Background"
LAYER_NAME_DONT_TOUCH = "Don't Touch"
LAYER_NAME_MOVING_PLATFORMS = "Moving Platforms"
LAYER_NAME_LADDERS = "Ladders"
LAYER_NAME_END = "End"
LAYER_NAME_ENEMIES = "Enemies"
TEXTURE_LEFT = 0
TEXTURE_RIGHT = 1

def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]
class Entity(arcade.Sprite):
    def __init__(self, name_folder, name_file, type):
        super().__init__()

        # Default to facing right
        self.facing_direction = TEXTURE_RIGHT
        self.properties["type"] = type
        # Used for image sequences
        self.cur_texture = 0
        self.scale = CHARACTER_SCALING
        self.character_face_direction = TEXTURE_RIGHT
        if type == "zombie" or type == "robot":
            main_path = f":resources:images/animated_characters/{name_folder}/{name_file}"
        else:
            main_path = f"resources/enemies/{name_file}"
        self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")
        self.jump_texture_pair = load_texture_pair(f"{main_path}_jump.png")
        self.fall_texture_pair = load_texture_pair(f"{main_path}_fall.png")

        # Load textures for walking
        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)

        # Load textures for climbing
        self.climbing_textures = []
        texture = arcade.load_texture(f"{main_path}_climb0.png")
        self.climbing_textures.append(texture)
        texture = arcade.load_texture(f"{main_path}_climb1.png")
        self.climbing_textures.append(texture)

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used. If you want to specify
        # a different hit box, you can do it like the code below.
        # set_hit_box = [[-22, -64], [22, -64], [22, 28], [-22, 28]]
        self.hit_box = self.texture.hit_box_points


class Enemy(Entity):
    def __init__(self, name_folder, name_file, type):

        # Setup parent class
        super().__init__(name_folder, name_file, type)
        self.should_update_walk = 0

    def update_animation(self, delta_time: float = 1 / 60):

         # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.facing_direction == TEXTURE_RIGHT:
            self.facing_direction = TEXTURE_LEFT
        elif self.change_x > 0 and self.facing_direction == TEXTURE_LEFT:
            self.facing_direction = TEXTURE_RIGHT

            # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.facing_direction]
            return

            # Walking animation
        if self.should_update_walk == 3:
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.facing_direction]
            self.should_update_walk = 0
            return

        self.should_update_walk += 1

class RobotEnemy(Enemy):
    def __init__(self):

        # Set up parent class
        super().__init__("robot", "robot", "robot")
        self.scale = 1

class HeadcrabEnemy(Enemy):
    def __init__(self):

        # Set up parent class
        super().__init__("headcrab", "headcrab", "headcrab")
        self.scale = .25
class ZombieEnemy(Enemy):
    def __init__(self):
        # Set up parent class
        super().__init__("zombie", "zombie", "zombie")
        self.scale = 1

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        main_path = "resources/player/"
        self.scale = CHARACTER_SCALING
        self.idle_texture = load_texture_pair(f"{main_path}idle1.png")
        self.jump_texture = load_texture_pair(f"{main_path}jump1.png")
        self.fall_texture = load_texture_pair(f"{main_path}fall.png")
        self.ladder_texture = load_texture_pair(f"{main_path}ladder0.png")
        self.climb_texture = load_texture_pair((f"{main_path}ladder1.png"))
        # Load a left facing texture and a right facing texture.
        # flipped_horizontally=True will mirror the image we load.
        self.cur_texture = 0
        self.character_face_direction = TEXTURE_RIGHT
        # By default, face right.
        self.texture = self.idle_texture[0]
        self.is_on_ladder = False
        self.climbing = False

        # Load textures for walking
        self.walk_textures = []
        for i in range(3):
            texture = load_texture_pair(f"{main_path}walk{i}.png")
            self.walk_textures.append(texture)

    def update_animation(self, delta_time: float = 1 / 60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == TEXTURE_RIGHT:
            self.character_face_direction = TEXTURE_LEFT
        elif self.change_x > 0 and self.character_face_direction == TEXTURE_LEFT:
            self.character_face_direction = TEXTURE_RIGHT

        if self.is_on_ladder and abs(self.change_y) > 1:
            self.texture = self.climb_texture[self.character_face_direction]
            return

        if self.is_on_ladder:
            self.texture = self.ladder_texture[self.character_face_direction]
            return


        # Jump animation
        if self.change_y > 0 and not self.is_on_ladder:
            self.texture = self.jump_texture[self.character_face_direction]
            return
        elif self.change_y < 0 and not self.is_on_ladder:
            self.texture = self.fall_texture[self.character_face_direction]
            return

        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture[self.character_face_direction]
            return



        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 2:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture][
            self.character_face_direction
        ]
class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Where is the right edge of the map?
        self.end_of_map = 0

        # Level
        self.level = 1

        # Load sounds

        # Our TileMap Object

        self.tile_map = None


        # Our Scene Object
        self.scene = None
        self.end_of_map = 0
        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our physics engine
        self.physics_engine = None

        # A Camera that can be used for scrolling the screen
        self.camera = None

        # A Camera that can be used to draw GUI elements
        self.gui_camera = None

        # Keep track of the score
        self.score = 0
        # Do we need to reset the score?
        self.reset_score = True

        # Load sounds
        self.collect_coin_sound = arcade.load_sound("resources/bruh-sound-effect-2.mp3")
        self.jump_sound = arcade.load_sound("resources/Punch.wav")
        self.game_over = arcade.load_sound("resources/you-died-sound-effect.mp3")
        self.background_music = arcade.load_sound("resources/the-final-battle.mp3")

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        # Set up the Cameras
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)


        # Name of map file to load

        # # Map name
        map_name = f"resources/WORLD{self.level}.tmx"

        # Layer Specific Options for the Tilemap
        layer_options = {
            LAYER_NAME_PLATFORMS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_COINS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_DONT_TOUCH: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_END: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_LADDERS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_MOVING_PLATFORMS: {
                "use_spatial_hash": False,
            },
            # LAYER_NAME_ENEMIES: {
            #     "use_spatial_hash": True
            # }
        }


        # Layer specific options are defined based on Layer names in a dictionary

        # Doing this will make the SpriteList for the platforms layer

        # use spatial hashing for detection.



        # Read in the tiled map

        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)



        # Initialize Scene with our TileMap, this will automatically add all layers

        # from the map as SpriteLists in the scene in the proper order.

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Keep track of the score, make sure we keep the score if the player finishes a level
        if self.reset_score:
            self.score = 0
        self.reset_score = True

        arcade.play_sound(self.background_music, volume=.25)
        # Keep track of the score
        # self.scene.add_sprite_list_after("Player", LAYER_NAME_FOREGROUND)
        # Set up the player, specifically placing it at these coordinates.

        self.player_sprite = Player()
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.scene.add_sprite("Player", self.player_sprite)

        # # Calculate the right edge of the my_map in pixels
        self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE
        # -- Enemies
        enemies_layer = self.tile_map.object_lists[LAYER_NAME_ENEMIES]

        for my_object in enemies_layer:
            # cartesian = self.tile_map.get_cartesian(
            #     my_object.center_x, my_object.center_y
            # )
            cartesian = self.tile_map.get_cartesian(
                my_object.shape[0], my_object.shape[1]
            )
            enemy_type = my_object.properties["type"]
            if enemy_type == "robot":
                enemy = RobotEnemy()
            elif enemy_type == "zombie":
                enemy = ZombieEnemy()
            elif enemy_type == "headcrab":
                enemy = HeadcrabEnemy()
            else:
                raise Exception(f"Unknown enemy type {enemy_type}.")
            enemy.center_x = math.floor(
                cartesian[0] * TILE_SCALING * self.tile_map.tile_width
            )
            enemy.center_y = math.floor(
                (cartesian[1] + 1) * (self.tile_map.tile_height * TILE_SCALING)
            )
            if "boundary_left" in my_object.properties:
                enemy.boundary_left = my_object.properties["boundary_left"]
            if "boundary_right" in my_object.properties:
                enemy.boundary_right = my_object.properties["boundary_right"]
            if "change_x" in my_object.properties:
                enemy.change_x = my_object.properties["change_x"]

            self.scene.add_sprite(LAYER_NAME_ENEMIES, enemy)


        # --- Other stuff

        # Set the background color

        if self.tile_map.background_color:

            arcade.set_background_color(self.tile_map.background_color)



        # Create the 'physics engine'

        self.physics_engine = arcade.PhysicsEnginePlatformer(

            self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["Platforms"],
            platforms=self.scene[LAYER_NAME_MOVING_PLATFORMS],
            ladders=self.scene[LAYER_NAME_LADDERS]

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
            380,
            10,
            arcade.csscolor.WHITE,
            25,
            font_name="Kenney Blocks"
        )

    # Draw hit boxes.

        self.player_sprite.draw_hit_box(arcade.color.RED, 3)
    def process_keychange(self):
        """
        Called when we change a key up/down or we move on/off a ladder.
        """
        # Process up/down
        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
            elif (
                    self.physics_engine.can_jump(y_distance=10)
                    and not self.jump_needs_reset
            ):
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                self.jump_needs_reset = True
                arcade.play_sound(self.jump_sound)
        elif self.down_pressed and not self.up_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED

        # Process up/down when on a ladder and no movement
        if self.physics_engine.is_on_ladder():
            if not self.up_pressed and not self.down_pressed:
                self.player_sprite.change_y = 0
            elif self.up_pressed and self.down_pressed:
                self.player_sprite.change_y = 0

        # Process left/right
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        if key == arcade.key.UP or key == arcade.key.SPACE or key == arcade.key.W:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
            elif self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
                self.physics_engine.increment_jump_counter()
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
            else:
                self.player_sprite.height *= 0.5
        # self.process_keychange()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = 0
            else:
                self.player_sprite.height *= 2
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0
        # self.process_keychange()


    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def on_update(self, delta_time):
        """Movement and game logic"""
        self.player_sprite.update()
        # Move the player with the physics engine
        self.physics_engine.update()

        if self.physics_engine.is_on_ladder():
            self.player_sprite.is_on_ladder = True
            # self.process_keychange()
        else:
            self.player_sprite.is_on_ladder = False
            # self.process_keychange()


        # Update walls, used with moving platforms
        self.scene.update([LAYER_NAME_MOVING_PLATFORMS, LAYER_NAME_ENEMIES])

        # Update Animations
        self.scene.update_animation(
            delta_time, [LAYER_NAME_COINS, LAYER_NAME_BACKGROUND, LAYER_NAME_ENEMIES, "Player"]
        )

        for enemy in self.scene[LAYER_NAME_ENEMIES]:
            if (
                enemy.boundary_right
                and enemy.right > enemy.boundary_right
                and enemy.change_x > 0
            ):
                enemy.change_x *= -1

            if (
                enemy.boundary_left
                and enemy.left < enemy.boundary_left
                and enemy.change_x < 0
            ):
                enemy.change_x *= -1

        # See if we hit anything
        player_collision_list = arcade.check_for_collision_with_lists(
            self.player_sprite,
            [
                self.scene[LAYER_NAME_COINS],
                self.scene[LAYER_NAME_ENEMIES],
            ],
        )
        # Loop through each coin we hit (if any) and remove it
        for collision in player_collision_list:

            if self.scene[LAYER_NAME_ENEMIES] in collision.sprite_lists:
                arcade.play_sound(self.game_over)
                self.setup()
                return
            else:

                self.score += 1
                # Figure out how many points this coin is worth
                # if "Points" not in collision.properties:
                #     print("Warning, collected a coin without a Points property.")
                # else:
                #     points = int(collision.properties["Points"])
                #     self.score += points

                # Remove the coin
                collision.remove_from_sprite_lists()
                arcade.play_sound(self.collect_coin_sound)

        # Position the camera
        self.center_camera_to_player()
        # Did the player fall off the map?
        if self.player_sprite.center_y < -100:
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y

            arcade.play_sound(self.game_over)

        # Did the player touch something they should not?
        if arcade.check_for_collision_with_list(
            self.player_sprite, self.scene[LAYER_NAME_DONT_TOUCH]
        ):
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y

            arcade.play_sound(self.game_over)
            self.setup()
        # See if the user got to the end of the level
        if self.player_sprite.center_x >= self.end_of_map:
            # Advance to the next level
            self.level += 1


            # Make sure to keep the score from this level when setting up the next level
            self.reset_score = False

            # Load the next level
            self.setup()

        if arcade.check_for_collision_with_list(
                self.player_sprite, self.scene[LAYER_NAME_END]
        ):
            self.level += 1
            self.reset_score = False
            self.setup()

def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()