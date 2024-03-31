"""
An attempt at making a Snake game

Jada Potter
1/18/24
"""
import os
import sys
from typing import Optional
import random

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import pygame.gfxdraw


class TailQueue:
    """
    Class for the queue of squares that are occupied by the snake's tail
    """
    __queue: list[tuple[int, int]]

    def __init__(self) -> None:
        """
        Constructor - no parameters. Creates an empty queue of squares occupied
        by the snake's tail
        """
        self.__queue = []

    def add(self, coords: tuple[int, int]) -> None:
        """
        Adds a coordinate point to the queue
        """
        self.__queue.insert(0, coords)

    def remove(self) -> None:
        """
        Removes the last coordinate point from the queue
        """
        self.__queue.pop()

    @property
    def squares(self) -> list[tuple[int, int]]:
        """
        Property that gets the list of squares in the queue
        """
        return self.__queue

    def __contains__(self, coords: tuple[int, int]) -> bool:
        """
        Returns True if a coordinate point is in the queue, otherwise False
        """
        return coords in self.__queue

    def __len__(self) -> int:
        """
        Dunder method to return the queue length
        """
        return len(self.__queue)


class Snake:
    """
    Class for the Snake game
    """
    border: int
    board_dims: Optional[dict[str, int]]
    score_location: Optional[tuple[int, int]]

    snake_pos: tuple[int, int]
    snake_dir: Optional[str]
    tail_queue: "TailQueue"
    food_pos: Optional[tuple[int, int]]

    game_title: bool
    game_paused: bool
    game_lost: bool

    menu_button: Optional[pygame.Rect]

    surface: pygame.surface.Surface
    clock: pygame.time.Clock

    big_font: Optional[pygame.font.Font]
    med_font: Optional[pygame.font.Font]
    small_font: Optional[pygame.font.Font]

    font_color: tuple[int, int, int]
    board_color: tuple[int, int, int]
    snake_color: tuple[int, int, int]
    food_color: tuple[int, int, int]

    def __init__(self, width: int = 1280, height: int = 800,
                 border: int = 64) -> None:
        """
        Constructor

        Parameters:
            width : int : width of window
            height : int : height of window
        """
        self.border = border
        self.board_dims = None
        self.score_location = None

        self.snake_pos = (12, 12)
        self.snake_dir = None
        self.tail_queue = TailQueue()
        self.food_pos = None

        self.game_title = True
        self.game_paused = False
        self.game_lost = False

        self.menu_button = None

        # Initialize Pygame
        pygame.init()
        pygame.display.set_caption("Snake")

        self.surface = pygame.display.set_mode((width, height),
                                               pygame.RESIZABLE)
        
        self.clock = pygame.time.Clock()
        
        self.big_font = None
        self.med_font = None
        self.small_font = None
        self.font_color = (220, 220, 220)
        self.board_color = (25, 25, 25)
        self.snake_color = (255, 255, 255)
        self.food_color = (255, 0, 0)

        self.update_board_dims()
        self.add_food()

        self.event_loop()

    def restart_game(self) -> None:
        """
        Sets all game values back to default (only after clicking "restart" on
        lose menu)
        """
        self.snake_pos = (12, 12)
        self.snake_dir = None
        self.tail_queue = TailQueue()
        self.add_food()
        
    def update_snake_pos(self, direction: str) -> None:
        """
        Updates the position of the snake based on the inputted direction
        "w" means up
        "a" means left
        "s" means down
        "d" means right
        """
        self.tail_queue.add(self.snake_pos)

        x, y = self.snake_pos

        if direction == "w":
            if y > 0:
                self.snake_pos = (x, y - 1)
            else:
                self.game_lost = True
        elif direction == "a":
            if x > 0:
                self.snake_pos = (x - 1, y)
            else:
                self.game_lost = True
        elif direction == "s":
            if y < 24:
                self.snake_pos = (x, y + 1)
            else:
                self.game_lost = True
        elif direction == "d":
            if x < 24:
                self.snake_pos = (x + 1, y)
            else:
                self.game_lost = True

        # Check for tail
        if self.snake_pos in self.tail_queue:
            self.game_lost = True

        # Check for for food
        if self.snake_pos == self.food_pos:
            self.add_food()
        else:
            # Remove last tail segment only if food wasn't found
            self.tail_queue.remove()

    def add_food(self):
        """
        Adds food in a random viable location
        """
        found = False
        while not found:
            try_coord = random.randint(0,24), random.randint(0,24)
            if try_coord != self.snake_pos:
                if try_coord not in self.tail_queue:
                    self.food_pos = try_coord
                    found = True


    ### Rendering ###

    def update_board_dims(self) -> None:
        """
        Recalculates the dimensions of the board (run when application is opened
        and when window is resized)
        """
        surface_width = self.surface.get_width()
        surface_height = self.surface.get_height()

        if surface_height < surface_width:
            board_size = surface_height - 2 * self.border
            board_left = surface_width // 2 - board_size // 2
            board_top = self.border
        else:
            board_size = surface_width - 2 * self.border
            board_left = self.border
            board_top = surface_height // 2 - board_size // 2

        self.board_dims = {"left": board_left, "top": board_top,
                           "size": board_size, "cell_size": board_size // 25}

        self.big_font = pygame.font.Font(None, board_size // 12)
        self.med_font = pygame.font.Font(None, board_size // 16)
        self.small_font = pygame.font.Font(None, board_size // 24)

        self.score_location = (board_left, board_top - board_size // 16)


    def draw_cell(self, coords: tuple[int, int],
                  col: tuple[int, int, int]) -> None:
        """
        Fills a given cell with a given color
        """
        x, y = coords

        cell_size = self.board_dims["cell_size"]
        cell_left = self.board_dims["left"] + cell_size * x
        cell_top = self.board_dims["top"] + cell_size * y

        pygame.draw.rect(self.surface, col, pygame.Rect(cell_left, cell_top,
                                                        cell_size, cell_size))

    def draw_window(self) -> None:
        """
        Draws the contents of the window
        """
        self.surface.fill(self.board_color)

        # Draw the board
        board_size = self.board_dims["size"]
        board_left = self.board_dims["left"]
        board_top = self.board_dims["top"]

        pygame.draw.rect(self.surface, (0, 0, 0),
                         pygame.Rect(board_left, board_top, board_size,
                                     board_size))

        # Draw snake head
        self.draw_cell(self.snake_pos, self.snake_color)

        # Draw snake tail
        for square in self.tail_queue.squares:
            self.draw_cell(square, (123,0,123))

        # Draw food
        self.draw_cell(self.food_pos, self.food_color)

        # Draw score
        img = self.med_font.render(f"Score: {len(self.tail_queue) + 1}", True,
                                   self.font_color)
        self.surface.blit(img, self.score_location)

    ### Menu methods ###

    def draw_menu(self) -> None:
        """
        Draws the menu when the game is either on title, paused, or lost
        """
        self.surface.fill(self.board_color)

        # Draw the menu outline
        menu_size = self.board_dims["size"] // 2
        menu_left = self.board_dims["left"] + menu_size // 2
        menu_top = self.board_dims["top"] + menu_size // 2

        pygame.draw.rect(self.surface, (0, 0, 0),
                         pygame.Rect(menu_left, menu_top, menu_size,
                                     menu_size))

        # Draw menu button
        button_width = menu_size // 2
        button_height = menu_size // 4
        button_left = menu_left + menu_size // 4
        button_top = menu_top + menu_size // 2

        self.menu_button = pygame.Rect(button_left, button_top, button_width,
                                       button_height)

        pygame.draw.rect(self.surface, self.font_color, self.menu_button,
                         width=2)

        # Draw menu text
        center = menu_left + menu_size // 2
        in_title = (center, menu_top + menu_size // 4)
        in_subtitle = (center, menu_top + 3 * menu_size // 8)
        in_button = (center, menu_top + 5 * menu_size // 8)


        if self.game_title:
            self.draw_text("SNAKE", self.big_font, in_title)
            self.draw_text("By Jada Potter", self.small_font, in_subtitle)
            self.draw_text("PLAY", self.med_font, in_button)
        elif self.game_paused:
            self.draw_text("GAME PAUSED", self.big_font, in_title)
            self.draw_text("RESUME", self.med_font, in_button)
        elif self.game_lost:
            self.draw_text("GAME OVER", self.big_font, in_title)
            self.draw_text("RETRY", self.med_font, in_button)

    def draw_text(self, text: str, font: pygame.font.Font,
                  location: tuple[int, int]) -> None:
        """
        A function that draws text
        """
        img = font.render(text, True, self.font_color)
        img_rect = img.get_rect()
        img_rect.center = location
        self.surface.blit(img, img_rect)

    def click_in_button(self, pos: tuple[int, int]) -> bool:
        """
        Determines whether a mouse click was within the button onscreen
        """
        x, y = pos

        if self.menu_button is not None:
            if self.menu_button.left <= x <= self.menu_button.right:
                if self.menu_button.top <= y <= self.menu_button.bottom:
                    return True

        return False


    def event_loop(self) -> None:
        """
        Handles user interactions

        Parameters: none beyond self

        Returns: nothing
        """
        while True:
            # Process Pygame events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.WINDOWRESIZED:
                    self.update_board_dims()

                if self.game_title or self.game_paused or self.game_lost:
                    if event.type == pygame.MOUSEBUTTONUP:
                        if self.click_in_button(event.pos):
                            if self.game_title or self.game_paused:
                                self.game_title = False
                                self.game_paused = False
                            elif self.game_lost:
                                self.restart_game()
                                self.game_lost = False

                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_w:
                            if self.snake_dir != "s" or len(self.tail_queue) == 0:
                                self.snake_dir = "w"
                        if event.key == pygame.K_a:
                            if self.snake_dir != "d" or len(self.tail_queue) == 0:
                                self.snake_dir = "a"
                        if event.key == pygame.K_s:
                            if self.snake_dir != "w" or len(self.tail_queue) == 0:
                                self.snake_dir = "s"
                        if event.key == pygame.K_d:
                            if self.snake_dir != "a" or len(self.tail_queue) == 0:
                                self.snake_dir = "d"
                        if event.key == pygame.K_ESCAPE:
                            self.game_paused = True

            # If in title, paused, or lost, draw menu
            if self.game_title or self.game_paused or self.game_lost:
                self.draw_menu()
            # If game is playing
            else:
                # Change location of snake if moving
                if self.snake_dir is not None:
                    self.update_snake_pos(self.snake_dir)

                self.draw_window()

            pygame.display.update()
            self.clock.tick(12)


if __name__ == "__main__":
    Snake()
