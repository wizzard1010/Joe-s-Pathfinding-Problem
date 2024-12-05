import time

import pygame
import numpy as np

from search import env
from search import answer_q7

# During the development you can reduce this GRID_SIZE
GRID_SIZE = 40
CELL_SIZE = 40
WINDOW_SIZE = (CELL_SIZE * GRID_SIZE, CELL_SIZE * GRID_SIZE)

grid = env.gen_maze(GRID_SIZE, add_mud=True, add_grass=True)

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Pathfinding')
env.render_maze_game(grid, screen, CELL_SIZE)

#Start the search
# strategy = 'A*'
# plan_actions, plan_states, explored_states = answer_q7.graph_search(grid, strategy)

# # Visualization
# overlay = np.zeros_like(grid)
# total_cost = 0.0
# for state in explored_states:
#     x, y, f = state
#     print('Explored: ', x, y, f)
#     overlay[y, x] += 1
#     env.render_overlay(overlay, screen, CELL_SIZE)
#     time.sleep(0.1)


# overlay = np.zeros_like(grid)
# total_cost = 0.0
# for action, state in zip(plan_actions, plan_states):
#     total_cost += answer_q7.cost(state, action, grid)
#     x, y, f = state
#     overlay[y, x] += 101
#     env.render_overlay(overlay, screen, CELL_SIZE)
#     time.sleep(0.1)

# print('The plan:', ', '.join(plan_actions))
# print('The plan cost:', total_cost)
# print('Total explored states (iterations):', len(explored_states))

# E = len(explored_states)  # Number of explored nodes
# C = total_cost            # Path cost (already calculated in the overlay loop)

# print(f"\nResults for {strategy}:")
# print(f"E (Number of explored nodes): {E}")
# print(f"C (Path cost of the returned plan): {C}")

def verify_plan(grid, plan_states, plan_actions):
    """Verify if the given plan leads to the goal correctly."""
    if not plan_states or not plan_actions:
        print("Plan is empty!")
        return False

    # Start with the first state
    current_state = plan_states[0]

    for i, action in enumerate(plan_actions):
        next_state = answer_q7.transition(current_state, action, grid)
        expected_state = plan_states[i + 1] if i + 1 < len(plan_states) else None

        # Debugging log
        print(f"Action: {action}, Current: {current_state}, Next: {next_state}, Expected: {expected_state}")

        if next_state != expected_state:
            print(f"Plan is invalid! Transition mismatch at {current_state} with action {action}")
            print(f"Expected: {expected_state}, Got: {next_state}")
            return False

        current_state = next_state

    # Verify the goal state
    if not answer_q7.is_goal(current_state, grid):
        print("Plan is invalid! Final state does not match the goal.")
        return False

    print("Plan is valid!")
    return True

strategies = ['DFS', 'BFS', 'UCS', 'GS', 'A*']

# Loop through all strategies
for strategy in strategies:
    print(f"\nRunning {strategy} strategy...")
    plan_actions, plan_states, explored_states = answer_q7.graph_search(grid, strategy)

    # Visualization for explored states
    overlay = np.zeros_like(grid)
    for state in explored_states:
        x, y, f = state
        overlay[y, x] += 1
    env.render_overlay(overlay, screen, CELL_SIZE)
    time.sleep(1)  # Optional delay for visualization

    # Visualization for the plan
    overlay = np.zeros_like(grid)
    total_cost = 0.0
    for action, state in zip(plan_actions, plan_states):
        total_cost += answer_q7.cost(state, action, grid)
        x, y, f = state
        overlay[y, x] += 101
        env.render_overlay(overlay, screen, CELL_SIZE)
        time.sleep(0.1)

    # Calculate explored nodes and path cost
    E = len(explored_states)  # Number of explored nodes
    C = total_cost            # Path cost (already calculated above)

    # Print results for the current strategy
    print(f"Results for {strategy}:")
    print(f"E (Number of explored nodes): {E}")
    print(f"C (Path cost of the returned plan): {C}")

    # Verify the plan
    if verify_plan(grid, plan_states, plan_actions):
        print(f"The plan is correct for {strategy}.")
    else:
        print(f"The plan is incorrect for {strategy}.")

pygame.display.flip()
pygame.quit()

input('Hit `Enter` to end the program.')

# if verify_plan(grid, plan_states, plan_actions):
#     print("The plan is correct for this search experiment.")
# else:
#     print("The plan is incorrect!")

# pygame.display.flip()
# pygame.quit()

# input('Hit `Enter` to end the program.')