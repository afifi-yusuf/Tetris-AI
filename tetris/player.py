from board import Direction, Rotation, Action
from random import Random
import time


class Player:
    def choose_action(self, board):
        raise NotImplementedError


class YusufPlayer(Player):
    def __init__(self, seed=None):
        self.random = Random(seed)

    def print_board(self, board):
        print("--------")
        for y in range(24):
            s = ""
            for x in range(10):
                if (x,y) in board.cells:
                    s += "#"
                else:
                    s += "."
            print(s, y)
                
    def rotate_clockwise(self, cloned_board, num_rotations):
        has_landed = False
        for _ in range(num_rotations):
            has_landed = cloned_board.rotate(Rotation.Clockwise)
            if has_landed != False:
                return has_landed
        return has_landed
    
    def x_value_of_max_height(self, cloned_board, max_height):
        for cell in cloned_board.cells:
            if cell[1] == max_height:
                return cell[0]

    def score_height(self, cloned_board):
        #the higher the better
        min = 23
        for cell in cloned_board.cells:
            if cell[1] < min:
                min = cell[1]
        return min
    
    def score_holes(self, cloned_board):
        #the lower the better
        holes = 0
        #for cell in cloned_board.cells:
         #   if (cell[0], cell[1]+1) not in cloned_board.cells and not cell[1]+1  > 23 :
          #      holes +=1
        for r in range(11):
            highest_in_col = False
            for c in range(24):
                if highest_in_col and (r,c) not in cloned_board.cells:
                    holes += 1
                if (r,c) in cloned_board.cells:
                    highest_in_col = True
        return holes
        
    
    def score_blocks(self, cloned_board):
        #the lower the better
        return len(cloned_board.cells)
    
    def score_bumpiness(self, cloned_board):
        heights = [23] * 10  # Assuming a 10-column Tetris grid
        total_bumpiness = 0

             
        # Update the heights of each column
        for cell in cloned_board.cells:
            column = cell[0]
            if cell[1] < heights[column]:
                heights[column] = cell[1] 

        # Calculate the total bumpiness
        for i in range(len(heights) - 1):
            total_bumpiness += abs(heights[i] - heights[i + 1])

        return total_bumpiness
    
    def score_aggregate_height(self, cloned_board):
        heights = [23] * 10  # Assuming a 10-column Tetris grid
             
        # Update the heights of each column
        for cell in cloned_board.cells:
            column = cell[0]
            if cell[1] < heights[column]:
                heights[column] = cell[1] 
        return(max(heights)-min(heights))
    
    def score_heights_cleared(self, cloned_board):
        heights_cleared = 0
        for r in range(11):
            count = 0
            for c in range(4):
                if (r,c) in cloned_board.cells:
                    count += 1
            if count == 10:
                heights_cleared += 1
        return heights_cleared    
            
    
    def score(self, cloned_board, heights_cleared):
        x = 1  #5
        y = -1000
        z = 0 #-35
        m = -200 #-15
        b = -0.1
        k = 0
        kW = 0
        if heights_cleared == 1:
            k = -10000
        elif heights_cleared == 2:
            k = -1000
        elif heights_cleared == 3:
            k = -500
        elif heights_cleared == 4:
            k = 10000
        #self.print_board(cloned_board)
        score = x*self.score_height(cloned_board) + y*self.score_holes(cloned_board) + z*self.score_blocks(cloned_board)  + m*self.score_bumpiness(cloned_board) + k*heights_cleared + b*self.score_aggregate_height(cloned_board) 
        return score

    def move_to_target(self, cloned_board, target_x):
        has_landed = False
        while has_landed == False and target_x < cloned_board.falling.left:
            has_landed = cloned_board.move(Direction.Left)
        while has_landed == False and target_x > cloned_board.falling.left:
            has_landed = cloned_board.move(Direction.Right)
        return has_landed
    def move_to_target_next(self, cloned_board, target_x):
        has_landed = False
        while has_landed == False and target_x < cloned_board.falling.left:
            has_landed = cloned_board.next.move(Direction.Left)
        while has_landed == False and target_x > cloned_board.falling.left:
            has_landed = cloned_board.next.move(Direction.Right)
        return has_landed
    

    def choose_action(self, board):
        try:
            #time.sleep(1)
            best_score = -float('inf')
            best_score2 = -float('inf')
            best_moves = []
    
            for rotation in range(4):
                for x in range(board.width):
                    cloned_board = board.clone()
                    prev_height = self.score_height(cloned_board)
                    prev_blocks = self.score_blocks(cloned_board)
                    for _ in range(rotation):
                        cloned_board.rotate(Rotation.Clockwise)
                    new_left = cloned_board.falling.left
                    has_landed = self.move_to_target(cloned_board, x)
                    
                    if has_landed == False:
                        cloned_board.move(Direction.Drop)
                    
                    #self.print_board(cloned_board)
                    #print("Score: ", current_score)
                    for rotation2 in range(4):
                        for x2 in range(board.width):
                            next_board = cloned_board.clone()
                            prev_blocks = self.score_blocks(cloned_board)
                            #prev_height = self.score_height(next_board)
                            for _ in range(rotation2):
                                next_board.rotate(Rotation.Clockwise)
                            new_left_2 = cloned_board.falling.left
                            has_landed = self.move_to_target(next_board, x2)
                            if has_landed == False:
                                next_board.move(Direction.Drop)
                            heights_cleared = 0
                            #print(self.score_blocks(next_board) - prev_blocks)
                            if (self.score_blocks(next_board) - prev_blocks) == -6:
                                heights_cleared = 1
                            elif (self.score_blocks(next_board) - prev_blocks) == -16:
                                heights_cleared = 2
                            elif (self.score_blocks(next_board) - prev_blocks) == -26:
                                heights_cleared = 3
                            elif (self.score_blocks(next_board) - prev_blocks) == -36:
                                heights_cleared = 4

                            current_score = self.score(next_board, heights_cleared)
                            #self.print_board(cloned_board)
                            #print("Score: ", current_score)
                            if current_score > best_score:
                                #self.print_board(cloned_board)
                                #print("Rotations: ", rotation)
                                #print(x - new_left)
                                #print(heights_cleared)
                                best_score = current_score
                                best_moves = [Rotation.Clockwise] * rotation
                                best_moves.extend([Direction.Left] * (new_left - x)) if x < new_left else best_moves.extend([Direction.Right] * (x - new_left))
                                best_moves.append(Direction.Drop)
            
                    
            
            if self.score_height(board.clone()) <= 7 and board.clone().bombs_remaining > 0:
                return [Action.Bomb]
            else:
                return best_moves
        except:
            return 

SelectedPlayer = YusufPlayer
