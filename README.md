# Velha das Velhas - Advanced Tic-Tac-Toe Game
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

This project is a variation of the traditional Tic-Tac-Toe game, built in Python using the tkinter library for the graphical user interface (GUI). The game features an advanced mode called "Velha das Velhas," which includes smaller Tic-Tac-Toe boards within a larger board, offering a unique twist to the classic game.

## Features
Multiple Boards: Play on a 3x3 grid of Tic-Tac-Toe boards, each representing a smaller game.
Victory Conditions: The game checks for horizontal, vertical, and diagonal victories in each smaller board, as well as for the overall board.
Graphical User Interface: The game features an intuitive GUI using tkinter, providing a smooth and interactive user experience.
Resizable Window: The game window has a minimum size and can be resized according to your preference.

## Gameplay

Players take turns clicking on the cells of the Tic-Tac-Toe boards to place their respective symbols (X and O).
Each smaller 3x3 board operates as an independent game of Tic-Tac-Toe.
The goal is to win in individual smaller boards, and the overall victory is determined based on the combined results of all the smaller boards.

## Code Overview

`criar_tabuleiro()`: Creates a 3x3 Tic-Tac-Toe board.
`criar_tabuleiros_menores()`: Initializes the game with smaller boards.
`verificar_vitoria()`: Checks if a player has won on a specific board.
`tabuleiro_cheio()`: Verifies if all cells in a board are filled.
`VelhaDasVelhas`: Main class managing the game logic and the tkinter GUI.

## Future Enhancements
Some potential improvements for future versions:
* Implement an AI opponent.
* Add multiplayer support over a network.
* Add sound effects and animations for enhanced user experience.
