from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import sys
from tetris import Tetris

pygame.init()
pygame.font.init()

BG = (0, 0, 0)
GRID = (12, 12, 12)
COLOR = (127, 143, 166)
SHADOW = (178, 190, 195)

size = (500, 800)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Tetris')

game = True
clock = pygame.time.Clock()
tetris = Tetris()

fps = 30
cnt = 0
speed = 25

left_key_down = False
right_key_down = False
down_key_down = False

font = pygame.font.SysFont('Comic Sans MS', 16)
next_block_text = font.render('Next Block', False, (255,255,255))
score_text = font.render('Score', False, (255,255,255))
held_block_text = font.render('Hold', False, (255,255,255))

quit_button = pygame.Rect(430,400,50,50)
quit_text = font.render('Quit',False,(255,255,255))

held = False

while game: 
    if tetris.block == None:
        tetris.create_block()
        if tetris.intersect():
            tetris = Tetris()
            continue
    cnt += 1 
    if cnt == 1000000:      
        cnt = 0
    if cnt % speed == 0: 
        tetris.go()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                tetris.down()
                tetris.stop()
            elif event.key == pygame.K_LEFT:    
                left_key_down = True
            elif event.key == pygame.K_RIGHT:
                right_key_down = True
            elif event.key == pygame.K_UP:
                tetris.block.rotate()
                tetris.shadow_block.rotate()
                for i in range(4):
                    for j in range(4):
                        if i * 4 + j in tetris.block.current_block():   
                             while j + tetris.block.x < 0:
                                tetris.move(1)
                             while j + tetris.block.x >= tetris.width:
                                tetris.move(-1)
                for i in range(4):
                    for j in range(4):
                        if i * 4 + j in tetris.shadow_block.current_block():   
                             while j + tetris.shadow_block.x < 0:
                                tetris.move(1)
                             while j + tetris.shadow_block.x >= tetris.width:
                                tetris.move(-1)
            elif event.key == pygame.K_DOWN:
                down_key_down = True
            elif event.key == pygame.K_c and not held:
                tetris.hold()
                held = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left_key_down = False
            elif event.key == pygame.K_RIGHT:
                right_key_down = False
            elif event.key == pygame.K_DOWN:
                down_key_down = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if quit_button.collidepoint(mouse_pos):
                game = False
    if left_key_down:
        tetris.move(-1) 
        if tetris.intersect(): 
            tetris.move(1)  
    if right_key_down:
        tetris.move(1)
        if tetris.intersect():
            tetris.move(-1)
    if down_key_down:
        speed = 2
    else:
        speed = 25
    screen.fill(BG)
    for i in range(tetris.height):  
        for j in range(tetris.width):
            pygame.draw.rect(screen,GRID,pygame.Rect(j*40,i*40,40,40),1) 
            if tetris.board[i][j] > 0:
                pygame.draw.rect(screen,tetris.block.colors[tetris.board[i][j]-1],pygame.Rect(j*40,i*40,40,40))
                pygame.draw.rect(screen,SHADOW,pygame.Rect(j*40,i*40,40,40),1)
    if tetris.block != None:
        for i in range(4):
            for j in range(4):
                if i * 4 + j in tetris.block.current_block():
                    pygame.draw.rect(screen,tetris.block.colors[tetris.block.type],pygame.Rect((j+tetris.block.x)*40,(i+tetris.block.y)*40,40,40))
    score = font.render(str(tetris.score),False,(255,255,255))
    screen.blit(next_block_text,(410,20))
    screen.blit(held_block_text,(435,180))
    pygame.draw.rect(screen,COLOR,pygame.Rect(410,50,80,80),1)
    pygame.draw.rect(screen,COLOR,pygame.Rect(410,210,80,80),1)
    screen.blit(score_text,(430,300))
    screen.blit(score,(435,320))
    screen.blit(quit_text,(438,415))
    pygame.draw.rect(screen,COLOR,pygame.Rect(430,400,50,50),1)
    for i in range(4):
        for j in range(4):  
            if i * 4 + j in tetris.next_block.current_block():  
              pygame.draw.rect(screen,tetris.next_block.colors[tetris.next_block.type],pygame.Rect(410+i*20,50+j*20,20,20)) 
    if tetris.held_block != None:
        for i in range(4):  
            for j in range(4):
                if i * 4 + j in tetris.held_block.current_block():
                    pygame.draw.rect(screen,tetris.held_block.colors[tetris.held_block.type],pygame.Rect(410+i*20,210+j*20,20,20))
    tetris.shadow_down()
    for i in range(4):
        for j in range(4):
            if i * 4 + j in tetris.shadow_block.current_block():
                pygame.draw.rect(screen,SHADOW,pygame.Rect((j+tetris.shadow_block.x)*40,(i+tetris.shadow_block.y)*40,40,40),1)
    if tetris.intersect():
        tetris.block = None
        tetris.break_lines()
        held = False

    pygame.display.flip()
    clock.tick(fps)      
    
pygame.quit()
sys.exit()
