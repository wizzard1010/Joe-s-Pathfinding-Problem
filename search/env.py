from typing import List, Tuple
from functools import lru_cache
import numpy as np
import random
import pygame


def gen_maze(
        size: int,
        add_mud: bool = False,
        add_grass: bool = False) -> np.ndarray:
    """Generate a maze that has random paths to the goal.

    The maze is represented by an array of size with the following properties:
    - A wall is surrounding the maze.
    - Start position is at x = 1 and y = 1 (top-left index).
    - Goal position is at x = size-2 and y = size-2 (bottom-right index)
    - The starting orientation of the agent is random

    Symbol mapping:
    -  0: ' ', empty (passable)
    -  1: '#', wall (not passable)
    -  2x: '^', agent is facing up (north)
    -  3x: '>', agent is facing right (east)
    -  4x: 'v', agent is facing down (south)
    -  5x: '<', agent is facing left (west)
    -  6: 'G', goal
    -  7: '~', mud (passable, but cost more)
    -  8: '.', grass (passable, but cost more)
    """
    assert size > 5, '`size` must be greater than 5.'
    grid = np.ones(shape=(size, size), dtype=np.int32)
    start = (1, 1)
    goal = (size - 2, size - 2)
    success_count = 0
    while (grid==0).sum() < 0.75 * (size - 2)**2 or success_count < 1:
        gaps = set()
        gaps = gaps.union([(0, i) for i in range(size)])
        gaps = gaps.union([(size-1, i) for i in range(size)])
        gaps = gaps.union([(i, 0) for i in range(size)])
        gaps = gaps.union([(i, size-1) for i in range(size)])
        p = np.random.random()
        p = [p , 1-p]
        cur = start
        paths = []
        while cur != goal:
            gaps.add(cur)
            paths.append(cur)
            x, y = cur
            if np.random.random() < 0.1:
                neighbors = [(x-1, y), (x, y-1)]
            else:
                neighbors = [(x+1, y), (x, y+1)]
            neighbors = [n for n in neighbors if n not in gaps]
            if len(neighbors) == 0 or len(paths) > size * 4:
                break  # fail
            elif len(neighbors) == 1:
                step = [0]
            else:
                step = np.random.choice(np.arange(len(neighbors)), 1, p=p)
            cur = neighbors[step[0]]
        else:
            paths.append(cur)
            for c in paths:
                grid[c] = 0
            success_count += 1

    if add_mud:
        passables = list(zip(*np.where(grid == 0)))
        muds = np.random.choice(
            np.arange(len(passables)),
            size=len(passables) // 4,
            replace=False)
        for m in muds:
            grid[passables[m]] = 7
    if add_grass:
        passables = list(zip(*np.where(grid == 0)))
        waters = np.random.choice(
            np.arange(len(passables)),
            size=len(passables) // 2,
            replace=False)
        for m in waters:
            grid[passables[m]] = 8

    grid[start] = np.random.choice([20, 30, 40, 50])
    grid[goal] = 6
    grid.flags.writeable = False
    return grid.T


def render_maze(grid: np.ndarray, maps: List[str] = None) -> str:
    if maps is None:
        maps = [' ', '#', '^', '>', 'v', '<', 'G', '~', '.', 'x', 'X', 'o', 'O']
    s = [' '.join([maps[x] for x in row]) for row in grid]
    return '\n'.join(s)


def find_agent(grid: np.ndarray) -> Tuple[int, int]:
    """Return x, y location of the agent. If not exist, return None, None."""
    y, x = np.where((grid > 19) & (grid < 60))
    if len(x) > 0 and len(y) > 0:
        return x[0], y[0]
    else:
        return None, None


def aspect_scale(img, bx, by):
    """ Scales 'img' to fit into box bx/by. This method will retain the original image's aspect ratio """
    ix,iy = img.get_size()
    if ix > iy:
        # fit to width
        scale_factor = bx/float(ix)
        sy = scale_factor * iy
        if sy > by:
            scale_factor = by/float(iy)
            sx = scale_factor * ix
            sy = by
        else:
            sx = bx
    else:
        # fit to height
        scale_factor = by/float(iy)
        sx = scale_factor * ix
        if sx > bx:
            scale_factor = bx/float(ix)
            sx = bx
            sy = scale_factor * iy
        else:
            sy = by

    return pygame.transform.scale(img, (sx,sy))


@lru_cache(maxsize=30)
def load_img(path: str, cell_size: int):
    img = pygame.image.load(path)
    img = aspect_scale(img, cell_size, cell_size)
    return img


def render_maze_game(grid: np.ndarray, screen: pygame.Surface, cell_size: int=20):
    height, width = grid.shape
    agent_img = load_img('assets/agent.png', cell_size)
    brick_img = load_img('assets/brick.png', cell_size)
    goal_img = load_img('assets/end.png', cell_size)
    dirt_img = load_img('assets/dirt.png', cell_size)
    grass_img = load_img('assets/grass.png', cell_size)
    rock_img = load_img('assets/rock.png', cell_size)
    mud_img = load_img('assets/mud.png', cell_size)

    for row in range(height):
        for col in range(width):
            g = grid[row][col]
            a = -1
            if g > 10:
                a = g//10
                g = g % 10
            loc = (col*cell_size, row*cell_size)
            screen.blit(dirt_img, loc)
            img = brick_img
            if g == 0:
                img = dirt_img
            if row == 0 or col == 0 or row == height-1 or col == height-1:
                img = brick_img
                if col == 0 or col == width - 1:
                    img = pygame.transform.rotate(brick_img, 90)
            elif g == 1:
                img = rock_img
                img = pygame.transform.rotate(img, random.randint(0, 360))
                screen.blit(grass_img, loc)
            if a in [2, 3, 4, 5]:
                rot = 0
                img = agent_img
                if g == 2:
                    rot = 180
                elif g == 3:
                    rot = 90
                elif g == 5:
                    rot = 270
                img = pygame.transform.rotate(img, rot)
            if g == 6:
                img = goal_img
            if g == 7:
                img = mud_img
                img = pygame.transform.rotate(img, random.randint(0, 360))
            if g == 8:
                img = grass_img

            screen.blit(img, loc)
    pygame.display.flip()


def render_overlay(overlay: np.array, screen: pygame.Surface, cell_size: int=20):
    height, width = overlay.shape
    for row in range(height):
        for col in range(width):
            o = overlay[row][col]
            loc1 = (col*cell_size, row*cell_size)
            # loc2 = ((col+1)*cell_size, (row+1)*cell_size)
            if o == 0:
                continue
            if o < 100:
                color = (0, 0, 255)
            elif o > 100:
                color = (0, 255, 0)
            pygame.draw.rect(screen, color, pygame.Rect(*loc1, cell_size, cell_size), o % 100)
    pygame.display.flip()
