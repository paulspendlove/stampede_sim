import matplotlib.pyplot as plt
import matplotlib.patches as patches
from IPython.display import clear_output

class Cell:
    def __init__(self, cellType='walkable'):
        self.occupied = None
        self.cellType = cellType
        self.north = None
        self.south = None
        self.east = None
        self.west = None

    def set_neighbors(self, north=None, south=None, east=None, west=None):
        self.north, self.south, self.east, self.west = north, south, east, west

    def is_occupied(self):
        return self.occupied is not None

class Person:
    def __init__(self, isStrong, isRational, isRelaxed, location):
        self.isStrong = isStrong
        self.isRational = isRational
        self.isRelaxed = isRelaxed
        self.location = location
        self.vulnerable = not isStrong and not isRelaxed
        self.isFallen = False
        self.isDead = False

    def color(self):
        if self.isDead:
            return 'black'
        elif self.isFallen:
            return 'lightgrey'
        elif self.isRelaxed:
            return 'green'
        elif self.isStrong and not self.isRational and not self.isRelaxed:
            return 'red'
        elif self.isStrong and self.isRational and not self.isRelaxed:
            return 'orange'
        elif not self.isStrong and not self.isRational and not self.isRelaxed:
            return 'blue'
        elif not self.isStrong and self.isRational and not self.isRelaxed:
            return 'purple'

    def move_left(self):
        if self.location.west and not self.location.west.is_occupied():
            self.location.occupied = None
            self.location = self.location.west
            self.location.occupied = self

    def move_right(self):
        if self.location.east and not self.location.east.is_occupied():
            self.location.occupied = None
            self.location = self.location.east
            self.location.occupied = self

    def move_up(self):
        if self.location.north and not self.location.north.is_occupied():
            self.location.occupied = None
            self.location = self.location.north
            self.location.occupied = self

    def move_down(self):
        if self.location.south and not self.location.south.is_occupied():
            self.location.occupied = None
            self.location = self.location.south
            self.location.occupied = self

def create_grid(rows, cols):
    grid = [[Cell() for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            north = grid[i-1][j] if i > 0 else None
            south = grid[i+1][j] if i < rows - 1 else None
            east = grid[i][j+1] if j < cols - 1 else None
            west = grid[i][j-1] if j > 0 else None
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
        ('green', 'Relaxed'),
        ('lightgrey', 'Fallen'),
        ('black', 'Dead'),
        ('red', 'Strong, Irrational'),
        ('orange', 'Strong, Rational'),
        ('blue', 'Weak, Irrational'),
        ('purple', 'Weak, Rational')
    ]
    
    legendElements = [patches.Patch(color=color, label=label) for color, label in colorsAndLabels]

    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            color = 'saddlebrown' if cell.cellType == 'walkable' else 'gray'
            ax.add_patch(patches.Rectangle((j, -i), 1, 1, fill=True, color=color))
            if cell.occupied:
                person_color = cell.occupied.color()
                ax.add_patch(patches.Circle((j + 0.5, -(i - 0.5)), 0.4, color=person_color))

    ax.set_xlim(0, len(grid[0])+2)
    ax.set_ylim(-len(grid), 1)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.legend(handles=legendElements, loc='upper right', bbox_to_anchor=(1.0, 1.0))

def run_simulation(grid, steps=10):
    # FILLER: Should be replaced with logic to run pathfinding algorithm in loop
    fig, ax = setup_grid_and_draw(grid)
    person = grid[0][4].occupied

    directions = ['left', 'down']
    direction_index = 0

    for _ in range(steps):
        if directions[direction_index] == 'left' and person.location.west:
            person.move_left()
        elif directions[direction_index] == 'down' and person.location.south:
            person.move_down()

        clear_output(wait=True)
        draw_grid(grid, ax)
        plt.pause(1)

        if person.location.west is None or person.location.south is None:
            direction_index = 1 - direction_index

    plt.close(fig)


# example grid 

# grid = create_grid(5, 5)
# grid[1][1].cellType = 'obstacle'
# grid[3][3].cellType = 'obstacle'
# grid[0][0].occupied = Person(True, True, False, grid[0][0])
# grid[2][2].occupied = Person(False, True, True, grid[2][2])
# grid[4][4].occupied = Person(True, False, True, grid[4][4])

grid = create_grid(5, 5)
grid[0][4].occupied = Person(True, True, False, grid[0][4])
run_simulation(grid, steps=15)

# We can generate grid's like this, using create_grid and modifying contents however necessary
# Next, we draw each grid with the above function
# Finally, after a certain timeout (or keypress?) we run the pathfinding algorithm, make moves
# between cells, and redraw the image.
