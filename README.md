# Joe-s-Pathfinding-Problem
This is an AI project for Joe's Path finding problem using DPS, BFS, UCS and A* search strategies
This project visualizes various pathfinding algorithms on a grid-based maze using Python and Pygame. The algorithms implemented include:

Depth-First Search (DFS)
Breadth-First Search (BFS)
Uniform-Cost Search (UCS)
Greedy Search (GS)
A Search*
You can observe how each algorithm explores the maze, calculates costs, and finds the path to the goal.

How it works
Grid Maze: The program generates a random grid maze with obstacles, mud (higher cost), and grass (moderate cost).
Visualization:
Explored nodes are displayed on the grid.
The final path is visualized after the algorithm finds the solution.
Strategies: The program runs all five strategies and prints results, including:
The number of nodes explored (E).
The total cost of the path (C).
Whether the generated plan is valid.

Requirements
Make sure you have the following installed:
Python 3.x
Pygame library
Numpy library
anyway you can install requirements from requirements.txt

Notes
GRID_SIZE: You can modify the grid size in the script (GRID_SIZE variable). Larger grids may take longer to compute.
Visualization Speed: Adjust the delay using time.sleep() in the script to speed up or slow down the animations.
Maze Customization: The maze includes mud and grass, which add variability to the path costs.
