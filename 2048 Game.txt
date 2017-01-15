"""
Clone of 2048 game.
IMPORT POC AND RUN GUI AT BOTTOM HAVE BEEN COMMENTED OUT
DAVID VEITCH 1/24/2016
http://www.codeskulptor.org/#user42_AZvhTjsosa_16.py
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
        
    temp_list = []
    merged_list = []
    
    # create two lists of 0s same length as inputted list
    count = 0
    while count < len(line):
        count += 1
        temp_list.append(0)
        merged_list.append(0)
    
    # creates list where non-zero elements have been shifted over 
    # but not added together
    count = 0
    for tile in line:
        if tile != 0: 
            temp_list[count] = tile
            count += 1               
    
    # if two numbers adjacent are same, they are added together in a list
    # if merged, the element that got added is set to 0
    count = 0
    while count < (len(line) - 1):
        if temp_list[count] == temp_list[count + 1]:
            temp_list[count] *= 2
            temp_list[count + 1] = 0
    
        count = count + 1
    
    # Outputs final merged list by eliminating zeros again
    count = 0
    for tile in temp_list:
        if tile != 0: 
            merged_list[count] = tile
            count += 1
    
    return merged_list

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._grid = []
        self.reset()
        
        # creates a set of initial tiles to use for the move function
        self._initial_tiles = {}
        self._initial_tiles[UP] = [[0, col] for col in range(self._grid_width)]
        self._initial_tiles[DOWN] = [[self._grid_height - 1, col] for col in range(self._grid_width)]
        self._initial_tiles[LEFT] = [[row, 0] for row in range(self._grid_height)]
        self._initial_tiles[RIGHT] = [[row, self._grid_width - 1] for row in range(self._grid_height)]

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [[0 for dummy_row in range(self._grid_width)] for dummy_col in range(self._grid_height)]

        
        # Calls new_tile method to add some starting tiles
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        string_representation = ""
        
        # outputs a grid broken up by new lines
        for row in self._grid:
            string_representation += str(row) + "\n"
            
        return string_representation

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # defines the max number of steps needed to be taken
        # based on which direction it is and width/height
        if direction == (UP): 
            num_steps = self._grid_height
        elif direction == (DOWN):
            num_steps = self._grid_height
        else: 
            num_steps = self._grid_width
        
        # iterates over each initial tile and merges the row/column associated with it
        # create_new_tile variable will only turn true if something moves at some point
        create_new_tile = False
        
        for initial_tile in self._initial_tiles[direction]:
            # creates temporary list of tiles that will get merged
            temp_list_to_merge = []
            
            for step in range(num_steps):
                # creates a variable with coordinates of tiles being iterated through in self._grid
                current_tile_coordinates = [initial_tile[0] + OFFSETS[direction][0] * step, 
                                            initial_tile[1] + OFFSETS[direction][1] * step]

                # adds value of tile to temp_list_to_merge
                temp_list_to_merge.append(self._grid[current_tile_coordinates[0]][current_tile_coordinates[1]])
            
            # takes temp_list_to_merge and performs merge function on it
            temp_list_to_merge = merge(temp_list_to_merge)

            # iterates to place values in temp_list_to_merge on coordinates in self._grid            
            for step in range(num_steps):
                current_tile_coordinates = [initial_tile[0] + OFFSETS[direction][0] * step, initial_tile[1] + OFFSETS[direction][1] * step]
                # checks if something has moved, if so, will spawn a new tile after the loop
                if self._grid[current_tile_coordinates[0]][current_tile_coordinates[1]] != temp_list_to_merge[step]:
                    create_new_tile = True
                self._grid[current_tile_coordinates[0]][current_tile_coordinates[1]] = temp_list_to_merge[step]
        
        # create a new tile after everything has been merged
        if create_new_tile:
            self.new_tile()                         

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # checks if there are any blank tiles
        # if there are blank tiles will put in a random tile
        
        for row in self._grid:
            if (0 in row):
                while True:
                    random_row = random.randrange(0, self._grid_height)
                    random_col = random.randrange(0, self._grid_width)
            
                    # checks if the random cell is 0 and if so fills it with a number
                    # 90% of time will be 2, 10% of time will be 4
                    if self._grid[random_row][random_col] == 0:
                        if random.random() >= 0.9: 
                            self._grid[random_row][random_col] = 4
                        else: 
                            self._grid[random_row][random_col] = 2
                        break
                break
            
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(4, 5))
