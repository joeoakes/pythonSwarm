import random
import tkinter as tk
from tkinter import Canvas


# Class implementing the Particle Swarm Optimization (PSO) algorithm
class ParticleSwarmOptimization:
    def __init__(self, num_robots, num_charms, max_iterations, inertia=0.5, cognitive=1.5, social=1.5):
        self.num_robots = num_robots  # Number of robots in the simulation
        self.num_charms = num_charms  # Number of charms to be searched for
        self.max_iterations = max_iterations  # Number of iterations for optimization
        self.inertia = inertia  # Inertia weight (controls momentum of particles)
        self.cognitive = cognitive  # Personal best influence factor
        self.social = social  # Global best influence factor
        self.charms = self.generate_charms()  # Generate charm positions
        self.robots = self.generate_robots()  # Generate initial robot positions
        self.velocities = [(random.uniform(-2, 2), random.uniform(-2, 2)) for _ in range(self.num_robots)]  # Initial velocities
        self.best_positions = self.robots.copy()  # Best known positions for each robot
        self.global_best = min(self.robots, key=self.evaluate_fitness)  # Best known position among all robots

    # Generate random positions for charms within a 500x500 grid
    def generate_charms(self):
        return [(random.uniform(50, 450), random.uniform(50, 450)) for _ in range(self.num_charms)]

    # Generate random positions for robots within a 500x500 grid
    def generate_robots(self):
        return [(random.uniform(50, 450), random.uniform(50, 450)) for _ in range(self.num_robots)]

    # Calculate the fitness of a position (closer to a charm is better)
    def evaluate_fitness(self, position):
        return min((position[0] - charm[0]) ** 2 + (position[1] - charm[1]) ** 2 for charm in self.charms)

    # Update positions and velocities of robots using PSO formula
    def update_particles(self):
        for i in range(self.num_robots):
            r1, r2 = random.random(), random.random()  # Random values for stochastic behavior

            # Compute new velocity based on inertia, cognitive, and social influence
            # Velocity update formula:
            # new_velocity = inertia * current_velocity
            #                + cognitive * (personal_best - current_position)
            #                + social * (global_best - current_position)
            new_velocity = (
                self.inertia * self.velocities[i][0] +
                self.cognitive * r1 * (self.best_positions[i][0] - self.robots[i][0]) +
                self.social * r2 * (self.global_best[0] - self.robots[i][0]),

                self.inertia * self.velocities[i][1] +
                self.cognitive * r1 * (self.best_positions[i][1] - self.robots[i][1]) +
                self.social * r2 * (self.global_best[1] - self.robots[i][1])
            )

            self.velocities[i] = new_velocity  # Update velocity
            # Position update formula: new_position = current_position + new_velocity
            self.robots[i] = (self.robots[i][0] + new_velocity[0], self.robots[i][1] + new_velocity[1])

            # Update personal best if the new position is better
            if self.evaluate_fitness(self.robots[i]) < self.evaluate_fitness(self.best_positions[i]):
                self.best_positions[i] = self.robots[i]

        # Update global best position among all robots
        self.global_best = min(self.best_positions, key=self.evaluate_fitness)

    # Main algorithm loop to optimize robot movement
    def run(self):
        for _ in range(self.max_iterations):
            self.update_particles()  # Update robots each iteration
        return self.robots, self.charms


# Update simulation frame (remove collected charms and redraw elements)
def update_simulation():
    global robots, charms
    canvas.delete("all")  # Clear the canvas

    if not charms:
        return  # End simulation when all charms are found

    for i in range(len(robots)):
        if charms:
            # Find the closest charm for the current robot
            closest_charm = min(charms, key=lambda c: (robots[i][0] - c[0]) ** 2 + (robots[i][1] - c[1]) ** 2)
            # Check if the robot reaches the charm (considered "collected")
            if abs(robots[i][0] - closest_charm[0]) < 5 and abs(robots[i][1] - closest_charm[1]) < 5:
                charms.remove(closest_charm)  # Remove collected charm

    # Draw remaining charms
    for charm in charms:
        canvas.create_oval(charm[0] - 5, charm[1] - 5, charm[0] + 5, charm[1] + 5, fill="gold")
    # Draw robots
    for robot in robots:
        canvas.create_rectangle(robot[0] - 10, robot[1] - 10, robot[0] + 10, robot[1] + 10, fill="blue")

    root.after(100, update_simulation)  # Schedule next frame update


# Start the simulation
def run_simulation():
    global robots, charms
    pso = ParticleSwarmOptimization(num_robots=3, num_charms=5, max_iterations=100)
    robots, charms = pso.run()
    update_simulation()


# Create GUI window and simulation canvas
root = tk.Tk()
root.title("Swarm Robots Searching for Charms - PSO")
canvas = Canvas(root, width=500, height=500, bg="white")
canvas.pack()
button = tk.Button(root, text="Start Simulation", command=run_simulation)
button.pack()
root.mainloop()
