import arcade

# Constantes
screen_width = 1000
screen_heigth = 500
screen_title = "Mario Proyecto"

# Constantes para escalar los sprites
character_scaling = 0.17
ground_scaling = 0.20
cylinder_scaling = 0.20

# Velocidad del jugador
player_movement_speed = 5
gravity = 1
player_jump_speed = 20

# How many pixels to keep as a minimum margin between the character and the edge of the screen.
left_viewport_margin = 250
right_viewport_margin = 250
bottom_viewport_margin = 50
top_viewport_margin = 100


class Mygame(arcade.Window):
    
    def __init__(self):
        super().__init__(screen_width, screen_heigth, screen_title)

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE) 

        # Listas que contendrán los sprites
        self.coin_list = None
        self.wall_list = None
        self.player_list = None

        # Variable sprite jugador
        self.player_sprite = None

        # Variable para seguir el Scrolling
        self.view_bottom = 0
        self.view_left = 0

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        # creación jugador
        image_source = "mario.png"
        self.player_sprite = arcade.Sprite(image_source, character_scaling)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 93
        self.player_list.append(self.player_sprite)

        # Creación del piso
        for x in range(0, 1250, 64):
            wall = arcade.Sprite("ground.png", ground_scaling)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        # Creación cilindros con una lista
        coordinate_list = [[512, 110], [256, 110], [768, 110]]

        for coordinate in coordinate_list:
            # Agrega un cráter en el suelo
            wall = arcade.Sprite("cylinder.png", cylinder_scaling)
            wall.position = coordinate
            self.wall_list.append(wall)
        
        # Motor de Física
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, gravity)


    def on_draw(self):
        arcade.start_render()

        self.player_list.draw()
        self.wall_list.draw()

    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = player_jump_speed
        
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -player_movement_speed

        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = player_movement_speed

    def on_key_release(self, key, modifiers):
        
        if key == arcade.key.LEFT:
            self.player_sprite.change_x = 0

        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        # Movimiento y lógica del juego
        self.physics_engine.update()


        # --- Manage Scrolling ---

        # Track if we need to change the viewport

        changed = False

        # Scroll left
        left_boundary = self.view_left + left_viewport_margin
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True
        
        # Scroll right		
        right_boundary = self.view_left + screen_width - right_viewport_margin
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + screen_heigth - top_viewport_margin
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + bottom_viewport_margin
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True
        
        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left, screen_width + self.view_left, self.view_bottom, screen_heigth + self.view_bottom)

def main():
    window = Mygame()
    window.setup()
    arcade.run()

if __name__ == '__main__':
    main()   