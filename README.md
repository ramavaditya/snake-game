# Snake – Python Edition
A tiny but fully‑functional “Snake” game written in pure Python + Pygame.

### Author: RamaVAditya

Date: 2025‑10‑17

## 📦 What’s this?
This repository contains a single, self‑contained script (snake.py) that implements the classic Snake game.

It uses only the standard library and the popular Pygame package – no external frameworks or assets are required.

## Why Pygame?

Pygame gives you an easy way to create windows, draw shapes, handle keyboard input and keep a consistent frame‑rate. The code is written in modern Python (≥ 3.8) so it’s readable and easily tweakable.

## 📥 How to run
1. Install the only dependency
```bash
pip install pygame
```
2. Run the game
```bash
python snake.py
```
You’ll see a black window with a green “snake” that you can control with the arrow keys.

The game runs at 15 FPS by default – change FPS in the script if you want it faster or slower.

## 🛠️ Features

Feature	Description
Snake movement	Arrow keys change direction; snake grows when eating food.
Food spawning	Random empty cell each time the snake eats.
Drawing	Snake is drawn in green, food in red.
Frame‑rate control	pygame.time.Clock() keeps a steady FPS.
Pause	Press P to pause/resume the game; while paused the game state is frozen and a message appears.
Scoring & Highscore	Eating food increases the score by 1; the current score is shown at the top-center and the best (Top) score and username at the top-right. After a game over you can enter your name — the top score is saved to `highscore.json`.

## 📁 File structure
```bash
snake.py          ←  main game script
 README.md        ←  this file
Tip:
If you want to add more features (score counter, wrap‑around logic, etc.) just edit the corresponding sections in snake.py. The code is heavily commented so you can follow along.
```

## 📚 Quick‑look at the key parts
Section	What it does
SnakeGame.__init__	Sets up window, clock and initial snake/food.
spawn_food	Picks a random empty cell for food.
draw	Renders every frame (snake + food).
run	Main loop that handles input, updates, draws & refreshes.

## 🎯 What to tweak next
- Speed – change the constant FPS or CELL_SIZE.
- Snake length – change the initial snake size or behavior on collisions.
- UI – change fonts, colors, or add sound effects on eating/game over.

## 🤝 Contributing
Feel free to fork, open issues or pull requests.

If you’d like to contribute, just add your changes to snake.py and submit a PR – I’ll review them promptly.