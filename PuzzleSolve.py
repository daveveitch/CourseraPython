"""
DAVID VEITCH 3/22/2016
http://www.codeskulptor.org/#user41_bY4IIG54yf_44.py
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        # Tests if tiles positioned in row i+1 positioned correctly for condition1
        # and then tests if tiles to right in row of target tile are correct for condition2
        # and then tests if the 0 tile is positioned at (target_row, target_col)
        # both conditions must be correct to pass test
        condition1 = False
        condition2 = False
        condition3 = False
        
        # CONDITION 1
        # Checks tiles row i+1 and below, if positioned correctly, condition1 = True
        # if we are at bottom row than condition1 is true
        if target_row == (self._height - 1):
            condition1 = True
        else:
            condition1 = True
            # checks if each value in the row below is correct, if any are incorrect set condition1 to False
            for row in range(target_row + 1, self._height):
                for col in range(self._width):
                    if self.get_number(row, col) != (row * self._width + col):
                        condition1 = False
                    else:
                        pass
                
        # CONDITION 2
        # checks tiles in same row but columns to right to see if they are positioned correctly
        # if we are in rightmost column condition2 is true
        if target_col == (self._width - 1):
            condition2 = True
        else:
            condition2 = True
            for tile in range(target_col + 1, self._width):
                if self.get_number(target_row, tile) != ((target_row) * self._width + tile):
                    condition2 = False
                else:
                    pass
        
        # CONDITION 3
        if self.get_number(target_row, target_col) == 0:
            condition3 = True

        return (condition1 and condition2 and condition3)
    
    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        assert target_row > 1, "solve_interior_tile, i not greater than 1"
        assert target_col > 0, "solve_interior_tile, j not greater than 0"
        assert self.lower_row_invariant(target_row, target_col), "lower row invariant input"
        
        move_string = ""
        
        # moves 0 up and across to the target tile
        up_moves = (target_row - self.current_position(target_row, target_col)[0])
        across_moves = (target_col - self.current_position(target_row, target_col)[1])
        print up_moves, across_moves
        
        # adds up moves and across moves to the move_string
        for dummy_move in range(up_moves):
            move_string += "u"
        
        if across_moves > 0:
            for dummy_move in range(across_moves):
                    move_string += "l"
            if up_moves != 0:
                for dummy_move in range(across_moves - 1):
                    move_string += "drrul"
                move_string += "dru"
                for dummy_move in range(up_moves-1):
                    move_string += "lddru"
                move_string += "ld"    
            else:
                for dummy_move in range(across_moves-1):
                    move_string += "urrdl"
            
        elif across_moves < 0:
            for dummy_move in range(across_moves * -1):
                move_string += "r"
            if up_moves > 1: 
                for dummy_move in range(across_moves * -1):
                    move_string += "dllur"
                ### ADDED WHEN TESTING
                move_string += "dlu"               
                for dummy_move in range(up_moves-1):
                    move_string += "rddlu"
                move_string += "rdl"
            else:
                # ADDED WHEN TESTING ... THE MULTIPLY BY -1
                for dummy_move in range((across_moves * -1) - 1):
                    move_string += "ulldr"
                move_string += "ullddruld"
                     
        elif across_moves == 0:
            for dummy_move in range(up_moves-1):
                move_string += "lddru"
            move_string += "ld"
        
        # updates the puzzle
        self.update_puzzle(move_string)
        assert self.lower_row_invariant(target_row, target_col-1), "lower row invariant input"
        
        return move_string

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        #assert self.lower_row_invariant(target_row, 0), "lower row invariant input"
        assert target_row > 1
        
        move_string = ""
        
        # checks for case where target is immediately above 0
        if self.current_position(target_row, 0) == (target_row - 1, 0):
            move_string += "u"
            for dummy_move in range(self._width-1):
                move_string += "r"
        
        # case where target is to the right of the i-1 row
        elif self.current_position(target_row,0)[0] == (target_row-1):
            move_string += "u"
            if self.current_position(target_row,0)[1] == 1:
                move_string += "ruldrdlurdluurddlur"
                # moves 0 to far right of board
                for dummy_move in range(self._width - 2):
                    move_string += "r"

            else:
                for dummy_move in range(self.current_position(target_row,0)[1]):
                    move_string += "r"
                if self.current_position(target_row,0)[1] == 2:
                    move_string += "ulld"
                else:
                    for dummy_move in range(self.current_position(target_row,0)[1]-2):
                        move_string += "ulldr"
                    move_string += "ulld"    
                move_string += "ruldrdlurdluurddlur"
                # moves 0 to far right of board
                for dummy_move in range(self._width - 2):
                    move_string += "r"
                
        # case where it is in row above and you use solve interior tile on a cloned board
        # similar to solve interior tile
        else:
            move_string += "ur"
            
            # moves 0 up and across to the target tile
            # starts from one row above and one column right of target
            up_moves = ((target_row - 1) - self.current_position(target_row, 0)[0])
            across_moves = (1 - self.current_position(target_row, 0)[1])
            
            print up_moves, across_moves
            
            # adds up moves and across moves to the move_string
            for dummy_move in range(up_moves):
                move_string += "u"
        
            if across_moves > 0:
                    for dummy_move in range(across_moves):
                        move_string += "l"
                    move_string += "dru"
                    
                    for dummy_move in range(up_moves-1):
                        move_string += "lddru"
                    
                    move_string += "ld"

            elif across_moves < 0:
                for dummy_move in range(across_moves * -1):
                    move_string += "r"
                for dummy_move in range((across_moves * -1) - 1):
                    move_string += "dllur"
                move_string += "dlu"   
                                
                for dummy_move in range(up_moves-1):
                    move_string += "lddru"
                move_string += "ld"
    
            elif across_moves == 0:
                for dummy_move in range(up_moves-1):
                    move_string += "lddru"
                move_string += "ld"
            
            # solves 3x2 puzzle that is left
            move_string += "ruldrdlurdluurddlur"
            
            # moves 0 to far right of board
            for dummy_move in range(self._width - 2):
                move_string += "r"
        
        # updates the puzzle
        self.update_puzzle(move_string)
        assert self.lower_row_invariant(target_row - 1, self._width - 1), "lower row invariant input"
                
        return move_string

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        checks if puzzle invariant in cells at row 0
        """
        
        # Condition1 tests if 0 is in (0, target_col)
        # condition 2 checks if the number in (1, target_col) is correct
        # condition 3 checks if 0 is moved to (1, target_col) the puzzle
        # passes lower_row_invariant (checks if it is solved)
        condition1 = False
        condition2 = False
        condition3 = False
        
        # CONDITION 1
        if self.get_number(0, target_col) == 0:
            condition1 = True
            
            # CONDITION2
            # checks if number in (1,target_col) is correct
            if self.get_number(1, target_col) == (1 * self._width + target_col):
                condition2 = True
            
            # CONDITION 3
            # creates a cloned board, moves 0 one space down, and then checks
            # if this cloned board passes lower_row_invariant
            cloned_board = self.clone()
            cloned_board.update_puzzle("d")
            condition3 = cloned_board.lower_row_invariant(1, target_col)
        
        return (condition1 and condition2 and condition3)

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # condition 1 checks if 0 tile is at square 
        # condition 2 checks if all positions to right or below are solved
        condition1 = False
        condition2 = False
        
        if self.get_number(1, target_col) == 0:
            condition1 = True
        
        condition2 = self.lower_row_invariant(1, target_col)
        
        return (condition1 and condition2)

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row0_invariant(target_col)
        
        down_moves = self.current_position(0, target_col)[0]
        across_moves = (target_col - self.current_position(0, target_col)[1])
        move_string = ""
        
        # initially checks case where target tile right next to
        # 0
        if down_moves == 0:
            move_string += "ld"
            
            # case where target right next to 0
            if across_moves == 1:
                pass
            else:
                for dummy_move in range(across_moves - 1):
                    move_string += "l"
                
                move_string += "urdl"
                
                for dummy_move in range(across_moves - 2):
                    move_string += "urrdl"
                
                move_string += "urdlurrdluldrruld"
                
        else:       
            move_string += "ld"
            
            if across_moves == 1:
                move_string += "uld"
            else:
                for dummy_move in range(across_moves - 1):
                    move_string += "l"
            
                for dummy_move in range(across_moves - 2):
                        move_string += "urrdl"
                
            move_string += "urdlurrdluldrruld"
                
        self.update_puzzle(move_string)
        assert self.row1_invariant(target_col - 1)
                        
        return move_string

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row1_invariant(target_col)
        
        up_moves = (1 - self.current_position(1, target_col)[0])
        across_moves = (target_col - self.current_position(1, target_col)[1])
        move_string = ""
        
        # CASE where target immediately above
        if across_moves == 0:
            move_string += "u"
        elif across_moves > 0:
            if up_moves == 1:
                move_string += "u"
                for dummy_move in range(across_moves):
                    move_string += "l"
                for dummy_move in range(across_moves-1):
                    move_string += "drrul"
                move_string += "dru"
            
            elif up_moves ==0:
                for dummy_move in range(across_moves):
                    move_string += "l"
                for dummy_move in range(across_moves-1):
                    move_string += "urrdl"
                move_string += "ur"
                
        self.update_puzzle(move_string)
        assert self.row0_invariant(target_col)
        
        return move_string

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        assert self.row1_invariant(1)
        
        # moves 0 to top left corner
        move_string = "ul"
        self.update_puzzle(move_string)
        
        # checks if puzzle solved by doing this
        if self.row0_invariant(0):
            return move_string  
        else:
            # applies move RDLU until puzzle is solved
            for dummy_iteration in range(3):
                move_string += "rdlu"
                self.update_puzzle("rdlu")
                if self.row0_invariant(0):
                    break
         
        assert self.row0_invariant(0)
        return move_string

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        move_string = ""
        
        # Moves 0 to bottom right of puzzle
        across_moves = (self._width - 1) - self.current_position(0,0)[1]
        down_moves = (self._height - 1) - self.current_position(0,0)[0]
        
        for dummy_move in range(across_moves):
            move_string += "r"
        for dummy_move in range(down_moves):
            move_string += "d"
            
        self.update_puzzle(move_string) 
        
        while self.current_position(0,0) != (0,0):
            current_row = self.current_position(0,0)[0]
            current_col = self.current_position(0,0)[1]
            
            # if 0 in position 1,1, -> puzzle is a 2x2 solvable
            if (current_row, current_col) == (1,1):
                move_string += self.solve_2x2()
            
            # checks if 0 is in 0th row
            elif current_row == 0:
                self.row0_invariant(current_col)
                move_string += self.solve_row0_tile(current_col)
                
            elif current_row == 1:
                self.row1_invariant(current_col)
                move_string += self.solve_row1_tile(current_col)
            
            elif current_col == 0:
                print "passed to solve col0 tile \n", self
                self.lower_row_invariant(current_row, current_col)
                move_string += self.solve_col0_tile(current_row)
                print "came out of solve col0 tile \n", self
                
            else:
                self.lower_row_invariant(current_row, current_col)
                print "passed to solve interior tile \n", self
                move_string += self.solve_interior_tile(current_row, current_col)
                print "came out of solve interior tile \n", self                    
        
        return move_string

# Start interactive simulation
a = Puzzle(3,3,[[0,1,2],[3,4,5],[6,7,8]])
poc_fifteen_gui.FifteenGUI(a)
