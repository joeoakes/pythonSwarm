import random
import tkinter as tk
from tkinter import Canvas


# Class implementing the Particle Swarm Optimization (PSO) algorithm
class ParticleSwarmOptimization:
    def __init__(self, num_particles, max_iterations, num_robots, num_charms):
        self.num_particles = num_particles  # Number of particles (potential solutions)
        self.max_iterations = max_iterations  # Number of iterations for optimization
        self.num_robots = num_robots  # Number of robots in the simulation
        self.num_charms = num_charms  # Number of charms to be searched for
        self.charms = self.generate_charms()
        self.robots = self.generate_robots()
        self.particles = [self.generate_possible_solution() for _ in range(self.num_particles)]
        self.velocities = [[(random.uniform(-5, 5), random.uniform(-5, 5)) for _ in range(self.num_charms)] for _ in
                           range(self.num_particles)]
        self.best_positions = list(self.particles)
        self.global_best = max(self.particles, key=self.evaluate_fitness)

    # Generate random positions for charms within a 500x500 grid, ensuring they are not overlapping
    def generate_charms(self):
        charms = []
        min_distance = 50  # Minimum distance between charms
        while len(charms) < self.num_charms:
            new_charm = (random.uniform(50, 450), random.uniform(50, 450))
            if not any(((new_charm[0] - c[0]) ** 2 + (new_charm[1] - c[1]) ** 2) ** 0.5 < min_distance for c in charms):
                charms.append(new_charm)
        return charms

    # Generate random positions for robots within a 500x500 grid
    def generate_robots(self):
        return [(random.uniform(50, 450), random.uniform(50, 450)) for _ in range(self.num_robots)]

    # Generate a possible solution (random sequence of visiting charms)
    def generate_possible_solution(self):
        return random.sample(self.charms, len(self.charms))

    # Calculate the fitness of a path (shorter total distance is better)
    def evaluate_fitness(self, path):
        return -sum(
            ((path[i][0] - path[i - 1][0]) ** 2 + (path[i][1] - path[i - 1][1]) ** 2) ** 0.5 for i in
            range(1, len(path)))

    # Update particle positions and velocities
    def update_particles(self):
        w = 0.5  # Inertia weight
        c1, c2 = 1.5, 1.5  # Acceleration coefficients

        for i in range(self.num_particles):
            for j in range(len(self.charms)):
                # Velocity update
                inertia = tuple(w * v for v in self.velocities[i][j])
                cognitive = tuple(
                    c1 * random.random() * (self.best_positions[i][j][k] - self.particles[i][j][k]) for k in range(2))
                social = tuple(
                    c2 * random.random() * (self.global_best[j][k] - self.particles[i][j][k]) for k in range(2))

                self.velocities[i][j] = tuple(inertia[k] + cognitive[k] + social[k] for k in range(2))

                # Position update
                self.particles[i][j] = tuple(self.particles[i][j][k] + self.velocities[i][j][k] for k in range(2))

            # Evaluate new fitness
            if self.evaluate_fitness(self.particles[i]) > self.evaluate_fitness(self.best_positions[i]):
                self.best_positions[i] = list(self.particles[i])

        # Update global best
        self.global_best = max(self.best_positions, key=self.evaluate_fitness)

    # Run the PSO optimization
    def run(self):
        for _ in range(self.max_iterations):
            self.update_particles()
        return self.robots, self.charms


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
    pso = ParticleSwarmOptimization(num_particles=50, max_iterations=100, num_robots=3, num_charms=5)
    robots, charms = pso.run()
    update_simulation()


root = tk.Tk()
root.title("Swarm Robots Searching for Charms using PSO")
canvas = Canvas(root, width=500, height=500, bg="white")
canvas.pack()
button = tk.Button(root, text="Start Simulation", command=run_simulation)
button.pack()
root.mainloop()
