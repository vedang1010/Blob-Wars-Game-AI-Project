import pygame
from copy import deepcopy
from .blob import *
from .constants import *

class Board:
    def __init__(self) -> None:
        self.board = []
        self.blob_nums = {'1': 0, '2': 0}
        self.reset()

    def reset(self):
        self.board = [[None for col in range(COLS)] for row in range(ROWS)]
        self.board[0][0] = Blob(0, 0, 2)
        self.board[0][COLS-1] = Blob(0, COLS-1, 2)
        self.board[ROWS-1][0] = Blob(ROWS-1, 0, 1)
        self.board[ROWS-1][COLS-1] = Blob(ROWS-1, COLS-1, 1)
        self.blob_nums = {1: 2, 2: 2}

    def get_blob(self, row, col):
        return self.board[row][col]

    def evaluate(self):
        return self.blob_nums[1] - self.blob_nums[2]

    def get_all_children(self, player):
        chidren = []

        blobs = []
        for row in self.board:
            for blob in row:
                if blob is not None and blob.player == player:
                    blobs.append(blob)

        for blob in blobs:
            available_moves = self.get_available_moves(blob)
            for move in available_moves:
                board_copy = deepcopy(self)
                board_copy.move_blob(blob, move[0], move[1])
                if board_copy not in chidren:
                    chidren.append(board_copy)
        return chidren
    
    def get_available_moves(self, blob):
        available_moves = []
        for col in range(blob.col-2,blob.col+3):
            for row in range(blob.row-2,blob.row+3):
                within_range = row > -1 and row < ROWS and col > -1 and col < COLS
                if within_range:
                    cell = self.get_blob(row,col)
                    if cell is None:
                        available_moves.append((row,col))
        return available_moves

    def fill(self, player):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] is None:
                    self.board[row][col] = Blob(row, col, player)
                    self.blob_nums[player] += 1

    def move_blob(self, blob, row, col):
        self.board[row][col] = Blob(row, col, blob.player)
        self.blob_nums[blob.player] +=1
        if abs(blob.row - row) > 1 or abs(blob.col - col) > 1:
            self.board[blob.row][blob.col] = None
            self.blob_nums[blob.player] -=1
            
        for j in range(col-1,col+2):
            for i in range(row-1,row+2):
                within_range = i > -1 and i < ROWS and j > -1 and j < COLS
                if within_range:
                    cell = self.get_blob(i, j)
                    if cell is not None and cell.player != blob.player:
                        self.board[i][j] = Blob(i, j, blob.player)
                        self.blob_nums[blob.player] +=1
                        self.blob_nums[cell.player] -=1

    def draw_banner(self, win):
        font = pygame.font.SysFont('Comic Sans MS', 30)
        player1_number_text = font.render(f'x{self.blob_nums[1]}',False,pygame.Color('darkblue'))
        player2_number_text = font.render(f'x{self.blob_nums[2]}',False,pygame.Color('darkmagenta'))
        pygame.draw.rect(win, pygame.Color('darkgrey'), (MARGIN,HEIGHT,SQUARE_SIZE*2+MARGIN, SQUARE_SIZE))
        pygame.draw.rect(win, pygame.Color('darkgrey'), (WIDTH - SQUARE_SIZE*2 - MARGIN*2,HEIGHT,SQUARE_SIZE*2+MARGIN, SQUARE_SIZE))
        outline_color = pygame.Color('darkblue')
        color = COLORS['blue']
        pygame.draw.circle(win, outline_color, (MARGIN+ SQUARE_SIZE//2,HEIGHT + SQUARE_SIZE//2), SQUARE_SIZE//2 -8)
        pygame.draw.circle(win, color, (MARGIN+ SQUARE_SIZE//2,HEIGHT + SQUARE_SIZE//2), SQUARE_SIZE//2 -10)
        outline_color = pygame.Color('darkmagenta')
        color =  COLORS['purple']
        pygame.draw.circle(win, outline_color, (WIDTH - SQUARE_SIZE*2 + SQUARE_SIZE//2 - MARGIN*2,HEIGHT + SQUARE_SIZE//2), SQUARE_SIZE//2 -8)
        pygame.draw.circle(win, color, (WIDTH - SQUARE_SIZE*2 + SQUARE_SIZE//2 - MARGIN*2,HEIGHT + SQUARE_SIZE//2), SQUARE_SIZE//2 -10)
        win.blit(player1_number_text,(MARGIN+ SQUARE_SIZE,HEIGHT +MARGIN ))
        win.blit(player2_number_text,(WIDTH - SQUARE_SIZE*2 + SQUARE_SIZE - MARGIN*2,HEIGHT +MARGIN))
    
                        
    def draw(self, win):
        win.fill(pygame.Color('darkgreen'))
        for row in range(ROWS):
            for col in range(COLS):
                pygame.draw.rect(win, COLORS['green'], (row*(SQUARE_SIZE+MARGIN) + MARGIN, col*(SQUARE_SIZE+MARGIN)+ MARGIN, SQUARE_SIZE, SQUARE_SIZE))
    
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] is not None:
                    self.board[row][col].draw(win)

        self.draw_banner(win)
        
    def __str__(self) -> str:
        string = '\n'
        for row in range(ROWS):
            string += '\n'
            for col in range(COLS):
                string += '  '
                blob = self.board[row][col] 
                if blob is not None:
                    if blob.player == 1:
                        string += '#'
                    else:
                        string += '@'
        return string     