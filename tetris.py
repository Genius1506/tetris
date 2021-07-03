from block import Block
from copy import deepcopy

class Tetris:
    width = 10 
    height = 20
    score = 0 
    board = []
    block = None
    next_block = None
    held_block = None
    shadow_block = None

    def __init__(self):
        self.board = []
        self.score = 0
        for i in range(self.height):
            line = []
            for j in range(self.width):
                line.append(0)
            self.board.append(line)
            
    def create_block(self):
        if self.next_block == None:
            self.next_block = Block(4,0)
        self.block = self.next_block
        self.shadow_block = deepcopy(self.block)
        self.next_block = Block(4,0)
            
    def hold(self):
        temp = self.held_block
        self.held_block = self.block
        self.block = temp
        if self.block == None:
            self.create_block()
        self.block.y = 0
        self.shadow_block = deepcopy(self.block)

    def go(self):
        self.block.y += 1
        if self.intersect():
            self.block.y -= 1
            self.stop()

    def down(self):
        while not self.intersect():
            self.block.y += 1 
        self.block.y -= 1
    
    def shadow_down(self):
        while not self.shadow_intersect():
            self.shadow_block.y += 1 
        self.shadow_block.y -= 1

    def move(self,d):
        self.block.x += d
        self.shadow_block = deepcopy(self.block)

    def stop(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.block.current_block():
                    self.board[i + self.block.y][j + self.block.x] = self.block.type+1

    def in_bounds(self,x,y):
        if x < self.width and y < self.height and x >= 0 and y >= 0:
            return True
        return False

    def intersect(self):
        is_intersecting = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.block.current_block():
                    if not self.in_bounds(j+self.block.x,i+self.block.y) or self.board[i+self.block.y][j+self.block.x] > 0:
                        is_intersecting = True 
        return is_intersecting
    
    def shadow_intersect(self):
        is_intersecting = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.shadow_block.current_block():
                    if not self.in_bounds(j+self.shadow_block.x,i+self.shadow_block.y) or self.board[i+self.shadow_block.y][j+self.shadow_block.x] > 0:
                        is_intersecting = True 
        return is_intersecting
    
    def break_lines(self):
        lines = 0
        for i in range(1,self.height):
            complete_line = True
            for j in range(self.width):
                if self.board[i][j] == 0:
                    complete_line = False
            if complete_line:
                for x in range(i,1,-1):
                    for y in range(self.width):
                        self.board[x][y] = self.board[x-1][y]
                lines+=1
        self.score += (lines * 100)   