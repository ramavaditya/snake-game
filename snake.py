#!/usr/bin/env python3
"""
Snake – a tiny, fully‑functional game written in pure Python + Pygame.
Author:   ramavaditya
Date:     2025‑10‑17

The program is intentionally simple so you can read it line by line and tweak it if you wish.
"""

# --------------------------------------------------------------------------- #
# Imports & constants
# --------------------------------------------------------------------------- #
import pygame
from typing import List, Tuple
import random
import os
import json

# Window size (pixels)
WINDOW_W = 640          # width
WINDOW_H = 480          # height
CELL_SIZE = 20           # size of one snake “cell” in pixels

# Frames per second – how fast the game runs
FPS = 15

# --------------------------------------------------------------------------- #
# Helper types
# --------------------------------------------------------------------------- #
Position = Tuple[int, int]   # (row, col) – row is y, col is x

# --------------------------------------------------------------------------- #
# Game state
# --------------------------------------------------------------------------- #
class SnakeGame:
    """
    Holds all data needed for the game and drives the main loop.
    """

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        pygame.display.set_caption("Snake – Python Edition")
        self.clock = pygame.time.Clock()
        # The snake is a list of positions (row, col)
        # start somewhere near the middle
        start_r = (WINDOW_H // CELL_SIZE) // 2
        start_c = (WINDOW_W // CELL_SIZE) // 2 - 1
        self.snake: List[Position] = [(start_r, start_c), (start_r, start_c + 1), (start_r, start_c + 2)]
        self.direction: Position = (0, 1)   # moving right initially (dy, dx)
        self.food: Position | None = None

        # scoring
        self.score = 0
        # load top score (name and score)
        self.highscore_name, self.highscore_score = self.load_highscore()

        # font for score display
        self.font = pygame.font.SysFont(None, 28)

        # Timing for the food spawn
        self.spawn_food()

    # --------------------------------------------------------------------- #
    # Food spawning logic
    # --------------------------------------------------------------------- #
    def spawn_food(self):
        """Place a new piece of food at a random empty cell."""
        while True:
            r = random.randint(0, WINDOW_H // CELL_SIZE - 1)
            c = random.randint(0, WINDOW_W // CELL_SIZE - 1)
            if (r, c) not in self.snake:          # avoid collision with snake
                self.food = (r, c)
                break

    # --------------------------------------------------------------------- #
    # Main loop – runs until the user quits
    # --------------------------------------------------------------------- #
    def run(self):
        """Main game loop."""
        running = True
        while running:
            # 1. Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Arrow keys set absolute direction (prevents drifting/diagonals)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        new_dir = (-1, 0)
                    elif event.key == pygame.K_DOWN:
                        new_dir = (1, 0)
                    elif event.key == pygame.K_LEFT:
                        new_dir = (0, -1)
                    elif event.key == pygame.K_RIGHT:
                        new_dir = (0, 1)
                    else:
                        new_dir = None

                    # Prevent reversing into itself: new_dir must not be opposite of current
                    if new_dir:
                        if (new_dir[0] + self.direction[0], new_dir[1] + self.direction[1]) != (0, 0):
                            self.direction = new_dir

            # 2. Update snake position
            # Calculate new head position with wrap-around (toroidal board)
            rows = WINDOW_H // CELL_SIZE
            cols = WINDOW_W // CELL_SIZE
            new_r = (self.snake[-1][0] + self.direction[0]) % rows
            new_c = (self.snake[-1][1] + self.direction[1]) % cols
            new_head = (new_r, new_c)

            # Check collision with self (game over). For simplicity, stop the game.
            if new_head in self.snake:
                running = False
                continue

            # Add new head
            self.snake.append(new_head)

            # 3. Check if we hit the food
            if self.food and new_head == self.food:
                # eating: increase score and spawn new food (don't remove tail)
                self.score += 1
                self.spawn_food()
            else:
                # Not eating — remove tail so the snake appears to move
                self.snake.pop(0)

            # 4. Draw everything
            self.draw()

            # 5. Refresh screen & tick
            pygame.display.flip()
            self.clock.tick(FPS)

        # when the main loop ends, handle game over (username prompt & highscore)
        self.handle_game_over()

    # --------------------------------------------------------------------- #
    # Drawing routine – called every frame
    # --------------------------------------------------------------------- #
    def draw(self):
        """Draw the whole game state to the screen."""
        # Clear background
        self.screen.fill((0, 0, 0))          # black

        # Draw snake
        for r, c in self.snake:
            pygame.draw.rect(
                self.screen,
                (0, 255, 0),                     # green
                pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )

        # Draw food
        if self.food:
            pygame.draw.rect(
                self.screen,
                (255, 0, 0),                     # red
                # draw food as single cell same size as snake
                pygame.Rect(self.food[1] * CELL_SIZE, self.food[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )

        # Draw current score at top-middle
        score_surf = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        score_rect = score_surf.get_rect()
        score_rect.midtop = (WINDOW_W // 2, 6)
        self.screen.blit(score_surf, score_rect)

        # Draw top score at top-right
        top_surf = self.font.render(f"Top: {self.highscore_name} {self.highscore_score}", True, (255, 255, 0))
        top_rect = top_surf.get_rect()
        top_rect.top = 6
        top_rect.right = WINDOW_W - 8
        self.screen.blit(top_surf, top_rect)

    # --------------------------------------------------------------------- #
    # Highscore persistence & game-over handling
    # --------------------------------------------------------------------- #
    def highscore_path(self) -> str:
        return os.path.join(os.path.dirname(__file__), "highscore.json")

    def load_highscore(self) -> tuple:
        path = self.highscore_path()
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("name", "---"), int(data.get("score", 0))
        except Exception:
            return "---", 0

    def save_highscore(self, name: str, score: int) -> None:
        path = self.highscore_path()
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump({"name": name, "score": int(score)}, f)
        except Exception:
            # ignore save errors silently
            pass

    def handle_game_over(self):
        """Prompt the user for a name and save high score only if beaten."""
        pygame.event.clear()
        name = ""
        prompt = "Enter name (press Enter to confirm):"
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if name == "":
                            name = "Player"
                        # only save if beat top
                        if self.score > self.highscore_score:
                            self.save_highscore(name, self.score)
                            self.highscore_name, self.highscore_score = name, self.score
                        return
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        # ignore non-character control keys
                        if len(event.unicode) == 1 and event.unicode.isprintable():
                            name += event.unicode

            # draw prompt
            self.screen.fill((0, 0, 0))
            go_surf = self.font.render("Game Over", True, (255, 0, 0))
            go_rect = go_surf.get_rect(center=(WINDOW_W // 2, WINDOW_H // 2 - 40))
            self.screen.blit(go_surf, go_rect)

            score_surf = self.font.render(f"Your score: {self.score}", True, (255, 255, 255))
            score_rect = score_surf.get_rect(center=(WINDOW_W // 2, WINDOW_H // 2 - 10))
            self.screen.blit(score_surf, score_rect)

            prompt_surf = self.font.render(prompt, True, (200, 200, 200))
            prompt_rect = prompt_surf.get_rect(center=(WINDOW_W // 2, WINDOW_H // 2 + 20))
            self.screen.blit(prompt_surf, prompt_rect)

            name_surf = self.font.render(name + ("_" if (pygame.time.get_ticks() // 500) % 2 == 0 else ""), True, (255, 255, 255))
            name_rect = name_surf.get_rect(center=(WINDOW_W // 2, WINDOW_H // 2 + 50))
            self.screen.blit(name_surf, name_rect)

            pygame.display.flip()
            clock.tick(30)

# --------------------------------------------------------------------------- #
# Entry point – run the game
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    SnakeGame().run()