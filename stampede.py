import sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from IPython.display import clear_output
import random
import math
import heapq


class Cell:
    def __init__(self, cellType="walkable"):
        self.occupied = None
        self.cellType = cellType
        self.north = None
        self.south = None
        self.east = None
        self.west = None

        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = None

    def set_neighbors(self, north=None, south=None, east=None, west=None):
        self.north, self.south, self.east, self.west = north, south, east, west

    def is_occupied(self):
        return self.occupied is not None

    def clear_if_exit(self):
        if self.cellType == "exit" and self.occupied:
            self.occupied = None


class Person:
    def __init__(self, isStrong, isRational, isRelaxed, location):
        self.isStrong = isStrong
        self.isRational = isRational
        self.isRelaxed = isRelaxed
        self.location = location
        self.vulnerable = not isStrong and not isRelaxed
        self.isFallen = False
        self.isDead = False
        self.fallenCounter = 0
        self.blockedCounter = 0
        self.trampledCounter = 0

    def color(self):
        if self.isDead:
            return "black"
        elif self.isFallen:
            return "lightgrey"
        elif self.isRelaxed:
            return "green"
        elif self.isStrong and not self.isRational and not self.isRelaxed:
            return "red"
        elif self.isStrong and self.isRational and not self.isRelaxed:
            return "orange"
        elif not self.isStrong and not self.isRational and not self.isRelaxed:
            return "blue"
        elif not self.isStrong and self.isRational and not self.isRelaxed:
            return "purple"

    def move_left(self):
        if self.location.west and not self.location.west.occupied():
            self.location.occupied = None
            self.location = self.location.west
            self.location.occupied = self

    def move_right(self):
        if self.location.east and not self.location.east.occupied():
            self.location.occupied = None
            self.location = self.location.east
            self.location.occupied = self

    def move_up(self):
        if self.location.north and not self.location.north.occupied():
            self.location.occupied = None
            self.location = self.location.north
            self.location.occupied = self

    def move_down(self):
        if self.location.south and not self.location.south.occupied():
            self.location.occupied = None
            self.location = self.location.south
            self.location.occupied = self

    def update_status(self):
        if self.isFallen:
            if self.trampledCounter >= 3:
                self.isFallen = False
                self.isDead = True

            self.fallenCounter += 1
            if self.fallenCounter >= 3:
                self.isFallen = False
                self.fallenCounter = 0

        if self.blockedCounter >= 3:
            self.isRelaxed = False
            self.blockedCounter = 0

    def fall(self):
        self.isFallen = True
        # Reset counter when they fall
        self.fallenCounter = 0

    def blocked(self):
        # This method will be used to increase the blocked counter
        self.blockedCounter += 1

    def reset_blocked(self):
        # Reset blocked counter if person moves
        self.blockedCounter = 0

    def trampled(self):
        self.trampledCounter += 1

    def reset_trampled(self):
        self.trampledCounter = 0


def create_grid(rows, cols, custom_layout=None):
    grid = [
        [
            Cell(
                "exit"
                if custom_layout and custom_layout[i][j] == "E"
                else (
                    "obstacle"
                    if custom_layout and custom_layout[i][j] == "X"
                    else "walkable"
                )
            )
            for j in range(cols)
        ]
        for i in range(rows)
    ]
    for i in range(rows):
        for j in range(cols):
            north = grid[i - 1][j] if i > 0 else None
            south = grid[i + 1][j] if i < rows - 1 else None
            east = grid[i][j + 1] if j < cols - 1 else None
            west = grid[i][j - 1] if j > 0 else None
            grid[i][j].set_neighbors(north, south, east, west)
    return grid


def setup_grid_and_draw(grid):
    fig, ax = plt.subplots(figsize=(10, 8))
    draw_grid(grid, ax)
    plt.ion()
    plt.show()
    return fig, ax


def draw_grid(grid, ax):
    ax.clear()
    colorsAndLabels = [
        ("green", "Relaxed"),
        ("lightgrey", "Fallen"),
        ("black", "Dead"),
        ("red", "Strong, Irrational"),
        ("orange", "Strong, Rational"),
        ("blue", "Weak, Irrational"),
        ("purple", "Weak, Rational"),
    ]

    legendElements = [
        patches.Patch(color=color, label=label) for color, label in colorsAndLabels
    ]

    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell.cellType == "exit":
                color = "lime"
                fontsize = 14 if len(grid) < 10 else 4
                ax.text(
                    j + 0.5,
                    -i + 0.5,
                    "Exit",
                    ha="center",
                    va="center",
                    fontsize=fontsize,
                )

            elif cell.cellType == "obstacle":
                color = "gray"
            else:
                color = "saddlebrown"
            ax.add_patch(patches.Rectangle((j, -i), 1, 1, fill=True, color=color))
            if cell.occupied:
                person_color = cell.occupied.color()
                ax.add_patch(
                    patches.Circle((j + 0.5, -(i - 0.5)), 0.4, color=person_color)
                )

    ax.set_xlim(0, len(grid[0]) + (len(grid[0]) / 3))
    ax.set_ylim(-len(grid), 1)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.legend(handles=legendElements, loc="upper right", bbox_to_anchor=(1.0, 1.0))


def find_exits(grid):
    exits = []
    for row in grid:
        for cell in row:
            if cell.cellType == "exit":
                exits.append(cell)
    return exits


def run_simulation(grid, steps=10):
    fig, ax = setup_grid_and_draw(grid)
    auto_run = False

    print("\nRunning simulation...")
    try:
        for _ in range(steps):
            for row in grid:
                for cell in row:
                    cell.clear_if_exit()
                    if cell.occupied:

                        # TODO: Perform pathfinding algorithm for each occupied cell.
                        # Pathfinding should consider fallen people as obstacles for rational, relaxed people, but as
                        # things that can be moved over for better gain for irrational, non-relaxed people.

                        # TODO: Either move person in the algorithm function OR here.  Account for game theory logic.
                        # i.e. Strong and Irrational person will attempt to push to progress.  Others may be blocked, and stand still.
                        # For any fallen or blocked people, use appropriate functions to increment their trackers.
                        # (so we know when to stand a fallen person back up, or mark as dead)

                        # TODO: Update each person's state at some point using the update_status function, after calling fallen or blocked, etc. when necessary.

                        # TODO: Finalize how pushing will work.  Since 2 people can't occupy one space, does pushing swap both?
                        # Or does pushing only occur if there's an empty space past the fallen person to be moved into?
                        # Same decision should apply to trampling.

                        # I don't think we have time to calculate inertia or any similar physics mentioned in the paper.
                        # I'm not convinced the paper did either, as its mentioned so briefly.  I think this current turn based system
                        # will be fine though.

                        pass

            clear_output(wait=True)
            draw_grid(grid, ax)

            fig.suptitle(f"Step {_ + 1} of {steps}")
            plt.pause(1)

            if auto_run:
                # time.sleep(1)
                print(f"Auto running step {_ + 1} of {steps}.")

            else:
                user_input = input(
                    "Press 'enter' to move to the next step or type 'auto' to run all remaining steps (type 'exit' to cancel): "
                )
                if user_input.lower() == "exit":
                    print("Simulation cancelled.")
                    break
                elif user_input.lower() == "auto":
                    print("Auto running remaining steps.")
                    auto_run = True
                elif user_input:
                    continue
    except KeyboardInterrupt:
        print("\nSimulation cancelled by user.")

    plt.close(fig)


def input_safe(prompt, default_func):
    user_input = input(prompt)
    if user_input == "":
        value = default_func()
        print(f"No input provided. Using random value: {value}")
        return value
    return int(user_input)


def main():
    args = sys.argv[1:]
    # For debugging purposes, we can pass in arguments to the script to skip the input prompts.
    # Example: python stampede.py debug
    # Can remove in final version.
    if args and args[0] == "debug":
        print("Running in debug grid.")
        print("5x5 grid with two obstacles")
        grid = create_grid(5, 5)
        grid[0][4].cellType = "exit"
        grid[1][1].cellType = "obstacle"
        grid[3][3].cellType = "obstacle"
        grid[0][0].occupied = Person(True, True, False, grid[0][0])
        grid[2][2].occupied = Person(False, True, True, grid[2][2])
        grid[4][4].occupied = Person(True, False, True, grid[4][4])
        walkable_count = sum(
            1 for row in grid for cell in row if cell.cellType == "walkable"
        )
        print("Population density: 20%")
        density = 20
        print("Rational: 20%")
        rational = 20
        print("Strong: 20%")
        strong = 20
        print("Relaxed: 20%")
        relaxed = 20
        print("Seed: 1")
        seed = 1
        random.seed(int(seed))
        print("Max steps: 20")
        max_steps = 20

    else:
        print("Welcome to the Crowd Stampede Simulation Setup!")
        grid_selection = input(
            "Type '1' to use a pre-made grid, or '2' to create your own grid: "
        )
        if grid_selection.lower() == "1":
            # Add more grids for more predefined experiments?
            grids = {
                "1": "5x5 grid with two obstacles",
                "2": "8x8 grid with random obstacles",
                "3": "50x20 hallway with large obstacles and few exits",
            }
            print("Available grids:")
            for name, description in grids.items():
                print(f"{name}: {description}")
            grid_choice = input("Choose a grid: ")
            if grid_choice == "1":
                grid = create_grid(5, 5)
                grid[0][4].cellType = "exit"
                grid[1][1].cellType = "obstacle"
                grid[3][3].cellType = "obstacle"
                grid[0][0].occupied = Person(True, True, False, grid[0][0])
                grid[2][2].occupied = Person(False, True, True, grid[2][2])
                grid[4][4].occupied = Person(True, False, True, grid[4][4])
            elif grid_choice == "2":
                grid = create_grid(8, 8)
                # Add random obstacles
                for _ in range(10):
                    i, j = random.randint(0, 7), random.randint(0, 7)
                    grid[i][j].cellType = "obstacle"
                grid[0][0].cellType = "exit"
            elif grid_choice == "3":
                grid = create_grid(20, 50)
                grid[6][0].cellType = "exit"
                grid[7][0].cellType = "exit"

                grid[12][0].cellType = "exit"
                grid[13][0].cellType = "exit"

                grid[6][49].cellType = "exit"
                grid[7][49].cellType = "exit"

                grid[12][49].cellType = "exit"
                grid[13][49].cellType = "exit"

                grid[0][15].cellType = "exit"

                grid[0][35].cellType = "exit"

                grid[19][15].cellType = "exit"

                grid[19][35].cellType = "exit"

                grid[9][9].cellType = "obstacle"
                grid[9][10].cellType = "obstacle"
                grid[10][9].cellType = "obstacle"
                grid[10][10].cellType = "obstacle"

                grid[9][19].cellType = "obstacle"
                grid[9][20].cellType = "obstacle"
                grid[10][19].cellType = "obstacle"
                grid[10][20].cellType = "obstacle"

                grid[9][29].cellType = "obstacle"
                grid[9][30].cellType = "obstacle"
                grid[10][29].cellType = "obstacle"
                grid[10][30].cellType = "obstacle"

                grid[9][39].cellType = "obstacle"
                grid[9][40].cellType = "obstacle"
                grid[10][39].cellType = "obstacle"
                grid[10][40].cellType = "obstacle"

        elif grid_selection.lower() == "2":
            rows = int(input("Enter the number of rows for the grid: "))
            cols = int(input("Enter the number of columns for the grid: "))
            custom_layout = []
            print(
                "Enter your grid layout line by line (use '0' for walkable, 'X' for obstacle, 'E' for exit): "
            )
            for _ in range(rows):
                new_row = input()
                if len(new_row) == rows:
                    custom_layout.append(new_row)
                else:
                    print("Invalid length. A walkable row will be included instead.")
                    custom_layout.append("".join(["0" * rows]))
            grid = create_grid(rows, cols, custom_layout)

        walkable_count = sum(
            1 for row in grid for cell in row if cell.cellType == "walkable"
        )
        density = input_safe(
            "Enter population density as a percentage (0-100): ",
            lambda: random.randint(0, 100),
        )

        # These are technically percentage chances to be this trait, which should be fine (I think)
        rational = input_safe(
            "Enter the percentage that is rational (0-100): ",
            lambda: random.randint(0, 100),
        )
        strong = input_safe(
            "Enter the percentage that is strong (0-100): ",
            lambda: random.randint(0, 100),
        )
        relaxed = input_safe(
            "Enter the percentage that is relaxed (0-100): ",
            lambda: random.randint(0, 100),
        )

        seed = input("Enter a seed for the RNG (any integer): ")
        if not seed:
            seed = random.randint(0, 10000)
            print(f"No seed provided. Using random seed: {seed}")
        random.seed(int(seed))

        max_steps = input_safe(
            "Enter the number of simulation steps to take (any integer): ", lambda: 100
        )
    total_people = int((density / 100) * walkable_count)
    rows = len(grid)
    cols = len(grid[0])
    for _ in range(total_people):
        while True:
            i, j = random.randint(0, rows - 1), random.randint(0, cols - 1)
            if grid[i][j].cellType == "walkable" and not grid[i][j].is_occupied():
                is_rational = random.random() < (rational / 100)
                is_strong = random.random() < (strong / 100)
                is_relaxed = random.random() < (relaxed / 100)
                grid[i][j].occupied = Person(
                    is_strong, is_rational, is_relaxed, grid[i][j]
                )
                break

    run_simulation(grid, max_steps)


if __name__ == "__main__":
    main()
