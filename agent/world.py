matrix = [["." for _ in range(10)] for _ in range(10)]
agent_location = None


"""
Functions to set up the world with different configurations of walls and coins.
"""


def setBorder(matrix):
    """Places walls along the outer border of the world.

    This function mutates the given 10x10 matrix in place by setting all edge
    cells to "#". Interior cells are left unchanged.

    Args:
        matrix (list[list[str]]): A 10x10 world grid.

    Returns:
        None
    """
    for i in range(10):
        for j in range(10):
            if i == 0 or i == 9 or j == 0 or j == 9:
                matrix[i][j] = "#"


def plantCoinsInGivenLocations(matrix, locations):
    """Places coins at the specified coordinates if the cells are empty.

    A coin is only planted when the target cell contains ".". Existing walls,
    shops, agents, or coins are not overwritten.

    Args:
        matrix (list[list[str]]): A 10x10 world grid.
        locations (list[tuple[int, int]]): Cell coordinates where coins should
            be placed.

    Returns:
        None
    """
    for location in locations:
        i, j = location
        if matrix[i][j] == ".":
            matrix[i][j] = "C"


def plantCoinsInRandomLocation(matrix):
    """Attempts to place coins in random cells.

    This function performs 10 random placement attempts. A coin is only planted
    when the chosen cell is empty, so fewer than 10 coins may be added.

    Args:
        matrix (list[list[str]]): A 10x10 world grid.

    Returns:
        None
    """
    import random

    for _ in range(10):
        i = random.randint(0, 9)
        j = random.randint(0, 9)
        if matrix[i][j] == ".":
            matrix[i][j] = "C"


def plantWallsInRandomLocation(matrix):
    """Attempts to place walls in random cells.

    This function performs 10 random placement attempts. A wall is only planted
    when the chosen cell is empty, so fewer than 10 walls may be added.

    Args:
        matrix (list[list[str]]): A 10x10 world grid.

    Returns:
        None
    """
    import random

    for _ in range(10):
        i = random.randint(0, 9)
        j = random.randint(0, 9)
        if matrix[i][j] == ".":
            matrix[i][j] = "#"


def plantMazeWalls(matrix):
    """Places walls in a fixed maze-like pattern.

    This function mutates the matrix in place using a predefined layout rather
    than a randomly generated maze.

    Args:
        matrix (list[list[str]]): A 10x10 world grid.

    Returns:
        None
    """
    for i in range(10):
        for j in range(10):
            if (
                (i == 1 and j in [1, 2, 3])
                or (i == 2 and j in [3, 4, 5])
                or (i == 3 and j in [5, 6, 7])
                or (i == 4 and j in [7, 8, 9])
                or (i == 5 and j in [1, 2, 3])
                or (i == 6 and j in [3, 4, 5])
                or (i == 7 and j in [5, 6, 7])
                or (i == 8 and j in [7, 8, 9])
            ):
                matrix[i][j] = "#"


def plantRandomMazeWalls(matrix):
    """Attempts to place random walls for a loose maze-like layout.

    This function performs 20 random placement attempts. A wall is only planted
    when the selected cell is empty.

    Args:
        matrix (list[list[str]]): A 10x10 world grid.

    Returns:
        None
    """
    import random

    for _ in range(20):
        i = random.randint(0, 9)
        j = random.randint(0, 9)
        if matrix[i][j] == ".":
            matrix[i][j] = "#"


def plantRandomSophisticatedMazeWalls(matrix):
    """Attempts to place a denser random wall layout.

    This function performs 40 random placement attempts in total across two
    loops. A wall is only planted when the selected cell is empty.

    Args:
        matrix (list[list[str]]): A 10x10 world grid.

    Returns:
        None
    """
    import random

    for _ in range(20):
        i = random.randint(0, 9)
        j = random.randint(0, 9)
        if matrix[i][j] == ".":
            matrix[i][j] = "#"
    for _ in range(20):
        i = random.randint(0, 9)
        j = random.randint(0, 9)
        if matrix[i][j] == ".":
            matrix[i][j] = "#"


def plantAShopInRandomLocation(matrix):
    """Places a shop in a random empty cell.

    The function keeps sampling random coordinates until it finds an empty cell,
    then places "S" there.

    Args:
        matrix (list[list[str]]): A 10x10 world grid.

    Returns:
        None
    """
    import random

    while True:
        i = random.randint(0, 9)
        j = random.randint(0, 9)
        if matrix[i][j] == ".":
            matrix[i][j] = "S"
            break


def plantAgentInRandomLocation(matrix):
    """Places the agent in a random empty cell.

    The function keeps sampling random coordinates until it finds an empty cell,
    then places "A" there.

    Args:
        matrix (list[list[str]]): A 10x10 world grid.

    Returns:
        None
    """
    import random

    while True:
        i = random.randint(0, 9)
        j = random.randint(0, 9)
        if matrix[i][j] == ".":
            matrix[i][j] = "A"
            break


"""
Functions to get the location of the agent, coins and shop in the world.
"""


def getAgentLocation(matrix):
    """Returns the coordinates of the agent.

    The matrix is scanned row by row until a cell containing "A" is found.

    Args:
        matrix (list[list[str]]): A 10x10 world grid.

    Returns:
        tuple[int, int] | None: The `(row, column)` position of the agent, or
        None if no agent exists in the grid.
    """
    for i in range(10):
        for j in range(10):
            if matrix[i][j] == "A":
                return (i, j)
    return None


def getCoinsLocations(matrix):
    """Returns the coordinates of all coins in the world.

    Args:
        matrix (list[list[str]]): A 10x10 world grid.

    Returns:
        list[tuple[int, int]]: A list of `(row, column)` positions containing
        coins.
    """
    coins = []
    for i in range(10):
        for j in range(10):
            if matrix[i][j] == "C":
                coins.append((i, j))
    return coins


def getShopLocation(matrix):
    """Returns the coordinates of the shop.

    The matrix is scanned row by row until a cell containing "S" is found.

    Args:
        matrix (list[list[str]]): A 10x10 world grid.

    Returns:
        tuple[int, int] | None: The `(row, column)` position of the shop, or
        None if no shop exists in the grid.
    """
    for i in range(10):
        for j in range(10):
            if matrix[i][j] == "S":
                return (i, j)
    return None


"""
Agent can move in four directions: up, down, left, right.
Agent cannot move through walls or fall from the edge of the world. Agent can
only move to an empty cell or a cell with a coin or a shop.
"""


def moveAgent(matrix, direction):
    """Moves the agent one step in the given direction when possible.

    The function updates the global `agent_location` cache if needed. Movement
    is blocked when the destination is out of bounds or contains a wall.

    Args:
        matrix (list[list[str]]): A 10x10 world grid.
        direction (str): The movement direction. Expected values are `"up"`,
            `"down"`, `"left"`, or `"right"`.

    Returns:
        bool: True if the agent moved successfully, otherwise False.
    """
    global agent_location

    if agent_location is None:
        agent_location = getAgentLocation(matrix)

    i, j = agent_location
    if direction == "up" and i > 0 and matrix[i - 1][j] != "#":
        matrix[i][j] = "."
        matrix[i - 1][j] = "A"
        agent_location = (i - 1, j)
        return True
    elif direction == "down" and i < 9 and matrix[i + 1][j] != "#":
        matrix[i][j] = "."
        matrix[i + 1][j] = "A"
        agent_location = (i + 1, j)
        return True
    elif direction == "left" and j > 0 and matrix[i][j - 1] != "#":
        matrix[i][j] = "."
        matrix[i][j - 1] = "A"
        agent_location = (i, j - 1)
        return True
    elif direction == "right" and j < 9 and matrix[i][j + 1] != "#":
        matrix[i][j] = "."
        matrix[i][j + 1] = "A"
        agent_location = (i, j + 1)
        return True
    return False


def moveUntilEdgeOrWallWithoutFallingFromEdge(matrix, direction):
    """Moves the agent repeatedly until blocked by a wall or boundary.

    The agent continues moving in the requested direction until the next move
    would leave the grid or enter a wall. The matrix and global
    `agent_location` are updated in place.

    Args:
        matrix (list[list[str]]): A 10x10 world grid.
        direction (str): The movement direction. Expected values are `"up"`,
            `"down"`, `"left"`, or `"right"`.

    Returns:
        None
    """
    global agent_location

    while True:
        if agent_location is None:
            agent_location = getAgentLocation(matrix)

        i, j = agent_location
        if direction == "up" and i > 0 and matrix[i - 1][j] != "#":
            matrix[i][j] = "."
            matrix[i - 1][j] = "A"
            agent_location = (i - 1, j)
        elif direction == "down" and i < 9 and matrix[i + 1][j] != "#":
            matrix[i][j] = "."
            matrix[i + 1][j] = "A"
            agent_location = (i + 1, j)
        elif direction == "left" and j > 0 and matrix[i][j - 1] != "#":
            matrix[i][j] = "."
            matrix[i][j - 1] = "A"
            agent_location = (i, j - 1)
        elif direction == "right" and j < 9 and matrix[i][j + 1] != "#":
            matrix[i][j] = "."
            matrix[i][j + 1] = "A"
            agent_location = (i, j + 1)
        else:
            break


"""
World will be represented as a 10x10 matrix, where:
- '.' represents an empty cell
- '#' represents a wall
- 'C' represents a coin
- 'S' represents a shop
- 'A' represents the agent
"""


def setEmptyWorld():
    """Initializes an empty world with only a randomly placed shop.

    This function uses the global `matrix` and does not reset existing state
    before placing the shop.

    Args:
        None

    Returns:
        None
    """
    plantAShopInRandomLocation(matrix)


def setOpenWorld():
    """Configures the global world with random walls and coins.

    The world remains open at the border, and no shop or agent is placed by
    this function.

    Args:
        None

    Returns:
        None
    """
    plantRandomSophisticatedMazeWalls(matrix)
    plantCoinsInRandomLocation(matrix)


def setBorderWorld():
    """Configures the global world with border walls, random walls, coins, and a shop.

    This function mutates the global `matrix` by surrounding it with walls,
    adding additional random walls and coins, and placing one shop.

    Args:
        None

    Returns:
        None
    """
    setBorder(matrix)
    plantRandomSophisticatedMazeWalls(matrix)
    plantCoinsInRandomLocation(matrix)
    plantAShopInRandomLocation(matrix)


def printWorld(matrix):
    """Prints the world grid in a readable row-by-row format.

    Args:
        matrix (list[list[str]]): A 10x10 world grid.

    Returns:
        None
    """
    for i in range(10):
        for j in range(10):
            print(matrix[i][j], end="  ")
        print()


"""
Set up the world with different configurations of walls and coins.
"""


def reset_world():
    """Resets the global world state.

    This function recreates the global `matrix` as an empty 10x10 grid and
    clears the cached `agent_location`.

    Args:
        None

    Returns:
        None
    """
    global matrix, agent_location
    matrix = [["." for _ in range(10)] for _ in range(10)]
    agent_location = None


def initialise_world():
    """Initializes the world and caches the agent's location.

    This function populates the global world using `setOpenWorld()`, places the
    agent in a random empty cell, and stores the agent's location in the global
    `agent_location` variable.

    Args:
        None

    Returns:
        None
    """
    global agent_location
    # reset_world()
    setOpenWorld()
    plantAgentInRandomLocation(matrix)
    agent_location = getAgentLocation(matrix)

def main():
    initialise_world()

if __name__ == "__main__":
    main()