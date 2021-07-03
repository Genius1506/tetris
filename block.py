import random

class Block:
    blocks = [
        [[1,5,9,13], [0,1,2,3]],
        [[1,4,5,9],[1,4,5,6],[1,5,6,9],[0,1,2,5]],
        [[5,6,9,10]],
        [[0,1,2,4],[0,1,5,9],[2,4,5,6],[0,4,8,9]],
        [[0,1,2,6],[1,5,8,9],[0,4,5,6],[0,1,4,8]],
        [[1,2,4,5],[0,4,5,9]],
        [[0,1,5,6],[1,4,5,8]]
    ]
    colors = [
        (112, 161, 255),
        (255, 71, 87),
        (255, 127, 80),
        (46, 213, 115),
        (236, 204, 104),
        (55, 66, 250),
        (181, 52, 113)
    ]
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.type = random.randint(0,6)
        self.current_rotation = 0
    def rotate(self):
        self.current_rotation = (self.current_rotation + 1) % len(self.blocks[self.type])
    def current_block(self):
        return self.blocks[self.type][self.current_rotation]