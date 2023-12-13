import pygame
from .constants import *

class Blob:
    def __init__(self, row, col, player):
        self.row = row
        self.col = col
        self.player = player
        self.color = COLORS['blue'] if player == 1 else COLORS['purple']
        self.x = 0
        self.y = 0
        self.get_position()

    def get_position(self):
        self.x = self.col *(SQUARE_SIZE+MARGIN)+MARGIN + SQUARE_SIZE//2
        self.y = self.row *(SQUARE_SIZE+MARGIN)+MARGIN + SQUARE_SIZE//2

    def draw(self, win):
        outline_color = pygame.Color('darkblue') if self.player == 1 else pygame.Color('darkmagenta')
        pygame.draw.circle(win, outline_color, (self.x, self.y), SQUARE_SIZE//2 -8)
        pygame.draw.circle(win, self.color, (self.x, self.y), SQUARE_SIZE//2 -10)

    def __repr__(self) -> str:
        return str(self.player)
