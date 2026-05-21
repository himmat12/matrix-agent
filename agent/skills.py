def worldMap(matrix):
    '''
    Scan the world and return the location of the agent, coins and shop. 
    Agent will have to navigate through the world to collect coins and reach the shop while avoiding walls and fall from the edge.
    '''
    agent_location = None
    coin_locations = []
    shop_location = None
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 'A':
                agent_location = (i, j)
            elif matrix[i][j] == 'C':
                coin_locations.append((i, j))
            elif matrix[i][j] == 'S':
                shop_location = (i, j)
    return agent_location, coin_locations, shop_location


def scanAdjacentCells(matrix, agent_location):
    '''
    Scan the adjacent cells of the agent and return the locations of the coins and shop. 
    Agent will have to navigate through the world to collect coins and reach the shop while avoiding walls and fall from the edge.
    '''
    adjacent_cells = []
    i, j = agent_location
    if i > 0:
        adjacent_cells.append((i-1, j))
    if i < len(matrix) - 1:
        adjacent_cells.append((i+1, j))
    if j > 0:
        adjacent_cells.append((i, j-1))
    if j < len(matrix[i]) - 1:
        adjacent_cells.append((i, j+1))
    
    coin_locations = []
    shop_location = None
    for cell in adjacent_cells:
        x, y = cell
        if matrix[x][y] == 'C':
            coin_locations.append(cell)
        elif matrix[x][y] == 'S':
            shop_location = cell
    return coin_locations, shop_location

def breakWalls(matrix, agent_location):
    '''
    Break the walls in the adjacent cells of the agent. 
    Agent will have to navigate through the world to collect coins and reach the shop while avoiding walls and fall from the edge.
    '''
    i, j = agent_location
    if i > 0 and matrix[i-1][j] == 'W':
        matrix[i-1][j] = '.'
    if i < len(matrix) - 1 and matrix[i+1][j] == 'W':
        matrix[i+1][j] = '.'
    if j > 0 and matrix[i][j-1] == 'W':
        matrix[i][j-1] = '.'
    if j < len(matrix[i]) - 1 and matrix[i][j+1] == 'W':
        matrix[i][j+1] = '.'
        
