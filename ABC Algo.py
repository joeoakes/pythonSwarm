import random
import networkx as nx
import tkinter as tk
from tkinter import Canvas


# Class implementing the Artificial Bee Colony (ABC) optimization algorithm
class ArtificialBeeColony:
    def __init__(self, num_bees, max_iterations, num_robots, num_charms):
        self.num_bees = num_bees  # Number of bees (potential solutions)
        self.max_iterations = max_iterations  # Number of iterations for optimization
        self.num_robots = num_robots  # Number of robots in the simulation
        self.num_charms = num_charms  # Number of charms to be searched for
        self.charms = self.generate_charms()
        self.robots = self.generate_robots()
        self.current_population = [self.generate_possible_solution() for _ in range(self.num_bees)] # Initial solutions

    # Generate random positions for charms within a 500x500 grid
    def generate_charms(self):
        return [(random.uniform(50, 450), random.uniform(50, 450)) for _ in range(self.num_charms)]

    # Generate random positions for robots within a 500x500 grid
    def generate_robots(self):
        return [(random.uniform(50, 450), random.uniform(50, 450)) for _ in range(self.num_robots)]

    # Generate a possible solution (random sequence of visiting charms)
    def generate_possible_solution(self):
        return random.sample(self.charms, len(self.charms))

    # Calculate the fitness of a path (shorter total distance is better)
    def evaluate_fitness(self, path):
        return -sum(
            (path[i][0] - path[i - 1][0]) ** 2 + (path[i][1] - path[i - 1][1]) ** 2 for i in range(1, len(path)))

    # Modify a path slightly by swapping two random charms (exploring new solutions)
    def apply_random_neighborhood_structure(self, path):
        new_path = path.copy()
        idx1, idx2 = random.sample(range(len(path)), 2) # Pick two random indices
        new_path[idx1], new_path[idx2] = new_path[idx2], new_path[idx1] # Swap them
        return new_path

    # Main algorithm loop to find the best path
    def run(self):
        for _ in range(self.max_iterations):
            for i in range(self.num_bees):
                new_solution = self.apply_random_neighborhood_structure(self.current_population[i])   # Try a new path
                # Replace current path if new one is better
                if self.evaluate_fitness(new_solution) > self.evaluate_fitness(self.current_population[i]):
                    self.current_population[i] = new_solution
        best_solution = max(self.current_population, key=self.evaluate_fitness)  # Find the best path
        return self.robots, best_solution


# Move a robot step-by-step towards a target (charm location)
def move_robot_towards_target(robot, target, step=5):
    x1, y1 = robot
    x2, y2 = target
    dx = step if x2 > x1 else -step if x2 < x1 else 0  # Adjust x direction
    dy = step if y2 > y1 else -step if y2 < y1 else 0  # Adjust y direction
    return x1 + dx, y1 + dy


# Update simulation frame (move robots and check charm collection)
def update_simulation():
    global robots, charms
    canvas.delete("all")

    if not charms:
        return  # End simulation when all charms are found

    for i in range(len(robots)):
        if charms:
            # Find the closest charm for the current robot
            closest_charm = min(charms, key=lambda c: (robots[i][0] - c[0]) ** 2 + (robots[i][1] - c[1]) ** 2)
            robots[i] = move_robot_towards_target(robots[i], closest_charm)  # Move towards it
            # Check if the robot reaches the charm (considered "collected")
            if abs(robots[i][0] - closest_charm[0]) < 5 and abs(robots[i][1] - closest_charm[1]) < 5:
                charms.remove(closest_charm)  # Remove collected charm
        else:
            # If no charms left, robots move randomly
            robots[i] = (robots[i][0] + random.choice([-5, 5]), robots[i][1] + random.choice([-5, 5]))

    # Draw remaining charms
    for charm in charms:
        canvas.create_oval(charm[0] - 5, charm[1] - 5, charm[0] + 5, charm[1] + 5, fill="gold")
    # Draw robots
    for robot in robots:
        canvas.create_rectangle(robot[0] - 10, robot[1] - 10, robot[0] + 10, robot[1] + 10, fill="blue")

    root.after(100, update_simulation)


# Start the simulation
def run_simulation():
    global robots, charms
    abc = ArtificialBeeColony(num_bees=50, max_iterations=100, num_robots=3, num_charms=5)
    robots, charms = abc.run()
    update_simulation()


root = tk.Tk()
root.title("Swarm Robots Searching for Charms")
canvas = Canvas(root, width=500, height=500, bg="white")
canvas.pack()
button = tk.Button(root, text="Start Simulation", command=run_simulation)
button.pack()
root.mainloop()