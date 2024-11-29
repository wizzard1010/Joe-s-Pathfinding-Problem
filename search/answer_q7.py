from typing import Literal, List, Tuple, TypeAlias, Annotated
import heapq

import numpy as np

from search.env import find_agent

State: TypeAlias = Tuple[int, int, str]

#===============================================================================
# 7.1 FORMULATION
#===============================================================================

def state_func(grid: np.ndarray) -> State:
    """Return a state based on the grid (observation).

    Number mapping:
    -  0: dirt (passable)
    -  1: wall (not passable)
    -  2x: agent is facing up (north)
    -  3x: agent is facing right (east)
    -  4x: agent is facing down (south)
    -  5x: agent is facing left (west)
    -  6: goal
    -  7: mud (passable, but cost more)
    -  8: grass (passable, but cost more)

    State is a tuple of
    - x (int)
    - y (int)
    - facing ('N', 'E', 'S', or 'W')
    """
    # TODO
    x, y = find_agent(grid)
    facing_map = {2: 'N', 3: 'E', 4: 'S', 5: 'W'}
    facing = facing_map[grid[y, x] // 10]
    return (x, y, facing)


# TODO
ACTIONS: List[str] = ['TurnLeft', 'TurnRight', 'MoveForward']

def transition(state: State, action: str, grid: np.ndarray) -> State:
    x, y, facing = state
    if action == 'TurnLeft':
        new_facing = {'N': 'W', 'W': 'S', 'S': 'E', 'E': 'N'}[facing]
        return (x, y, new_facing)
    elif action == 'TurnRight':
        new_facing = {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}[facing]
        return (x, y, new_facing)
    elif action == 'MoveForward':
        dx, dy = {'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0)}[facing]
        new_x, new_y = x + dx, y + dy
        if grid[new_y, new_x] != 1:  # Check for walls
            return (new_x, new_y, facing)
    return state


def is_goal(state: State, grid: np.ndarray) -> bool:
    """Return whether the state is a goal state."""
    # TODO
    x, y, _ = state
    return grid[y, x] == 6


def cost(state: State, action: str, grid: np.ndarray) -> float:
    """Return a cost of an action on the state."""
    # TODO
    # Place the following lines with your own implementation
    x, y, _ = state
    if action == 'MoveForward':
        cell = grid[y, x]
        if cell == 7:  # Mud
            return 3.0
        elif cell == 8:  # Grass
            return 2.0
    return 1.0


#===============================================================================
# 7.2 SEARCH
#===============================================================================


def heuristic(state: State, goal_state: State) -> float:
    """Return the heuristic value of the state."""
    # TODO
    x, y, _ = state
    gx, gy, _ = goal_state
    return abs(x - gx) + abs(y - gy)

def graph_search(
        grid: np.ndarray,
        strategy: Literal['DFS', 'BFS', 'UCS', 'GS', 'A*'] = 'A*'
        ) -> Tuple[
            Annotated[List[str], 'actions of the plan'],
            Annotated[List[State], 'states of the plan'],
            Annotated[List[State], 'explored states']]:
    """Return a plan (actions and states) and a list of explored states (in order)."""

    # TODO
    # Replace the lines below with your own implementation
    start = state_func(grid)  # Initialize the start state
    goal = (grid.shape[1] - 2, grid.shape[0] - 2, 'N')  # Assuming goal is bottom-right facing North

    # Initialize the frontier
    frontier = [(0 + heuristic(start, goal), 0, start, [])]  # (priority, path_cost, state, path)
    explored = set()
    explored_states = []

    while frontier:
        if strategy in ['DFS', 'BFS']:
            _, path_cost, current_state, path = frontier.pop(0 if strategy == 'BFS' else -1)
        else:
            _, path_cost, current_state, path = heapq.heappop(frontier)

        # Skip already-explored states
        if current_state in explored:
            continue

        explored.add(current_state)
        explored_states.append(current_state)

        # Check if we've reached the goal
        if is_goal(current_state, grid):
            # Generate the final sequence of plan states
            plan_states = [start]
            for action in path:
                next_state = transition(plan_states[-1], action, grid)
                plan_states.append(next_state)
            return path, plan_states, explored_states

        for action in ACTIONS:
            # Calculate the next state using the transition function
            next_state = transition(current_state, action, grid)
            if next_state != current_state:  # Ignore invalid transitions
                #calculate the action cost
                action_cost = cost(current_state, action, grid)
                new_cost = path_cost + action_cost
                
                #Determine priority based on the strategy
                if strategy == 'UCS':
                    priority = new_cost
                elif strategy == 'GS':
                    priority = heuristic(next_state, goal)
                else: #A*
                    priority = new_cost + heuristic(next_state, goal)
                
                #Add the next state to the frontier
                heapq.heappush(frontier, (priority, new_cost, next_state, path + [action]))

    # Return empty if no solution is found
    return [], [], explored_states