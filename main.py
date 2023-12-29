import pygame
from constants import *
from game import Game
from alphaBeta import *
import time
FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT + SQUARE_SIZE + MARGIN))
pygame.display.set_caption('BLOB WARS')
Icon = pygame.image.load('blob_wars.jpg')
pygame.display.set_icon(Icon)
# user=1
# ai=2
def get_row_col_from_mouse(pos):
    x, y = pos
    col = x // (SQUARE_SIZE + MARGIN)
    row = y // (SQUARE_SIZE + MARGIN)
    return row, col

def main():
    running = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    
    # value, best_move = max_func(game.board, 0, 64)
    # print(value, best_move)

    while running:
        clock.tick(FPS)
        

        if game.turn == 2 and game.state == 'Running':
            best_move = min_func(game.board, 0, -64)[1]
            # time.sleep(5)
            game.ai_move(best_move)
            # best_move = min_func(game.board, 0, -64)[1]
            # game.ai_move(best_move)
            game.change_turn()
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
            if event.type == pygame.MOUSEBUTTONDOWN and game.state == 'Running':
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)
                
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                   game.toggle_pause()                       

                elif event.key == pygame.K_r and game.state == 'GAME OVER' or game.state == 'YOU WIN':
                    game.reset()

                elif event.key == pygame.K_p:
                    
                    game.pass_turn(1)

                    
                    game.pass_turn(1)
        if game.state != 'GAME OVER' and game.state != 'YOU WIN':
            game.check_game_state()
        game.update()


    pygame.quit()

if __name__ == '__main__':
    main()
