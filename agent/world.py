matrix = [["." for _ in range(10)] for _ in range(10)]
agent_location = None

"""
Functions to set up the world with different configurations of walls and coins.
"""


def setBorder(matrix):
    """
    Border world will have walls sorrounding it, but will have no walls and no coins planted inside the world.
    Agent will have to navigate through the world to reach the shop while avoiding fall from the edge.
    """
    for i in range(10):
        for j in range(10):
            if i == 0 or i == 9 or j == 0 or j == 9:
                matrix[i][j] = "#"


def plantCoinsInGivenLocations(matrix, locations):
    """
    Plant coins in the given locations. Locations should be a list of tuples, where each tuple represents the (i, j) coordinates of the cell where the coin should be planted.
    """

    for location in locations:
        i, j = location
        if matrix[i][j] == ".":
            matrix[i][j] = "C"


def plantCoinsInRandomLocation(matrix):
    """
    Plant coins in random locations within the world.
    """
    import random

    for _ in range(10):
        i = random.randint(0, 9)
        j = random.randint(0, 9)
        if matrix[i][j] == ".":
            matrix[i][j] = "C"


def plantWallsInRandomLocation(matrix):
    """
    Plant walls in random locations within the world.
    """
    import random

    for _ in range(10):
        i = random.randint(0, 9)
        j = random.randint(0, 9)
        if matrix[i][j] == ".":
            matrix[i][j] = "#"


def plantMazeWalls(matrix):
    """
    Plant walls in a maze-like pattern within the world.
    Agent will have to navigate through the maze to reach the shop while avoiding walls and fall from the edge.
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
    """
    Plant walls in random locations within the world, but in a maze-like pattern.
    Agent will have to navigate through the maze to reach the shop while avoiding walls and fall from the edge.
    """
    import random

    for _ in range(20):
        i = random.randint(0, 9)
        j = random.randint(0, 9)
        if matrix[i][j] == ".":
            matrix[i][j] = "#"


def plantRandomSophisticatedMazeWalls(matrix):
    """
    Plant walls in random locations within the world, but in a more sophisticated maze-like pattern.
    Agent will have to navigate through the maze to reach the shop while avoiding walls and fall from the edge.
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
    """
    Plant a shop in a random location within the world.
    Agent will have to navigate through the world to reach the shop while avoiding walls and fall from the edge.
    """
    import random

    while True:
        i = random.randint(0, 9)
        j = random.randint(0, 9)
        if matrix[i][j] == ".":
            matrix[i][j] = "S"
            break


def plantAgentInRandomLocation(matrix):
    """
    Plant the agent in a random location within the world.
    Agent will have to navigate through the world to collect coins and reach the shop while avoiding walls and fall from the edge.
    """
    import random

    while True:
        i = random.randint(0, 9)
        j = random.randint(0, 9)
        if matrix[i][j] == ".":
            matrix[i][j] = "A"
            break


"""
Functions to get the location of the agent, coins and shop in the world."""


def getAgentLocation(matrix):
    """
    Get the location of the agent in the world.
    Returns a tuple (i, j) representing the coordinates of the agent in the world.
    """
    for i in range(10):
        for j in range(10):
            if matrix[i][j] == "A":
                return (i, j)
    return None


def getCoinsLocations(matrix):
    """
    Get the locations of the coins in the world.
    Returns a list of tuples, where each tuple represents the coordinates of a coin in the world.
    """
    coins = []
    for i in range(10):
        for j in range(10):
            if matrix[i][j] == "C":
                coins.append((i, j))
    return coins


def getShopLocation(matrix):
    """
    Get the location of the shop in the world.
    Returns a tuple (i, j) representing the coordinates of the shop in the world.
    """
    for i in range(10):
        for j in range(10):
            if matrix[i][j] == "S":
                return (i, j)
    return None


"""
Agent can move in four directions: up, down, left, right. 
Agent cannot move through walls or fall from the edge of the world. Agent can only move to an empty cell or a cell with a coin or a shop.
"""


def moveAgent(matrix, direction):
    """
    Move the agent in the given direction if possible.
    Direction can be 'up', 'down', 'left' or 'right'.
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
    """
    Move the agent in the given direction until it hits a wall or the edge of the world, without falling from the edge.
    Direction can be 'up', 'down', 'left' or 'right'.
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
    """
    Empty world will have no walls and no coins, but will have a shop planted in the world. Agent will have to navigate through the world to reach the shop while avoiding fall from the edge.
    """
    plantAShopInRandomLocation(matrix)


def setOpenWorld():
    """
    Open world will have no walls sorrounding it, but will have some walls and coins planted inside the world. Agent will have to navigate through the world to collect coins while avoiding walls and fall from the edge.
    """
    plantRandomSophisticatedMazeWalls(matrix)
    plantCoinsInRandomLocation(matrix)


def setBorderWorld():
    """
    Border world will have walls sorrounding it, but will have some walls and coins planted inside the world. Agent will have to navigate through the world to collect coins while avoiding walls and fall from the edge.
    """
    setBorder(matrix)
    plantRandomSophisticatedMazeWalls(matrix)
    plantCoinsInRandomLocation(matrix)
    plantAShopInRandomLocation(matrix)


def printWorld(matrix):
    """
    Print the world in a readable format.
    """
    for i in range(10):
        for j in range(10):
            print(matrix[i][j], end="  ")
        print()


"""
Set up the world with different configurations of walls and coins.
"""
def reset_world():
    global matrix, agent_location
    matrix = [["." for _ in range(10)] for _ in range(10)]
    agent_location = None

def initialise_world():
    global agent_location
    # reset_world()
    setOpenWorld()
    plantAgentInRandomLocation(matrix)
    agent_location = getAgentLocation(matrix)


TOOLS_REGISTRY = {
    "getAgentLocation": lambda: getAgentLocation(matrix),
    "moveAgent": lambda direction: moveAgent(matrix, direction),
    "moveUntilEdgeOrWallWithoutFallingFromEdge": lambda direction: moveUntilEdgeOrWallWithoutFallingFromEdge(
        matrix, direction
    ),
}


# setOpenWorld()


# print("Agent position: ", getAgentLocation(matrix))
# print("Coins positions: ", getCoinsLocations(matrix))
# print("Shop position: ", getShopLocation(matrix))
# print("World:")
# printWorld(matrix)

# for _ in range(5):
#     moveUntilEdgeOrWallWithoutFallingFromEdge(matrix, "up")

# for _ in range(5):
#     moveUntilEdgeOrWallWithoutFallingFromEdge(matrix, "down")

# for _ in range(2):
#     moveUntilEdgeOrWallWithoutFallingFromEdge(matrix, "left")

# print("Agent position after moving up: ", getAgentLocation(matrix))
# print("World after moving up:")
# printWorld(matrix)
