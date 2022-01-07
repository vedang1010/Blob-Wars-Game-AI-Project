import pygame

from blobwars.constants import COLORS, FONT, HEIGHT, MARGIN, SQUARE_SIZE, WIDTH

from .board import Board

class Game:
    def __init__(self, win):
        self.reset()
        pygame.font.init()

        self.win = win
        self.font = pygame.font.SysFont(FONT, WIDTH//10)

    def reset(self):
        self.board = Board()
        self.state = 'Running'
        self.turn = 1
        self.available_moves = {}
        self.selected_blob = None

    def update(self):
        self.board.draw(self.win)
        self.draw_available_moves()
        if self.state != 'Running':
            self.print(self.state)        
        pygame.display.update()

    def pass_turn(self, player):
        other_player = 2 if player == 1 else 1
        self.board.fill(other_player)

    def toggle_pause(self):
        if self.state == 'Running':
            self.state = 'Paused'
        elif self.state == 'Paused':
            self.state = 'Running'

    def check_game_state(self):
        if self.board.blob_nums[1] == 0 or len(self.board.get_all_children(1)) == 0:
            self.state = 'GAME OVER'
            self.pass_turn(1)
        elif self.board.blob_nums[2] == 0 or len(self.board.get_all_children(2)) == 0:
            self.state = 'YOU WIN'
            self.pass_turn(2)

    def select(self, row, col):
        if self.selected_blob:
            result = self._move(row, col)
            if not result:
                self.selected_blob = None
                self.select(row, col)
        blob = self.board.get_blob(row, col)
        if blob is not None and blob.player == self.turn:
            self.selected_blob = blob
            self.available_moves = self.board.get_available_moves(blob)
            return True

        return False
        
    def _move(self, row, col):
        cell = self.board.get_blob(row, col)
        if cell is None and (row, col) in self.available_moves:
            self.board.move_blob(self.selected_blob, row, col)
            self.change_turn()
            self.available_moves = []
            return True
        else:
            return False


    def change_turn(self):
        self.turn = 2 if self.turn == 1 else 1

    def draw_available_moves(self):
        for move in self.available_moves:
            row, col = move
            x = col *(SQUARE_SIZE+MARGIN)+MARGIN + SQUARE_SIZE//2
            y = row *(SQUARE_SIZE+MARGIN)+MARGIN + SQUARE_SIZE//2
            jump = abs(self.selected_blob.row - row) > 1 or abs(self.selected_blob.col - col) > 1
            color = COLORS['white'] if jump else pygame.Color('dimgray')
            pygame.draw.circle(self.win, color, (x, y), 7)

    def print(self, text):
        textsurface = self.font.render(text, False, (255, 0, 0))
        x = (WIDTH - textsurface.get_width()) // 2 
        y = (HEIGHT - textsurface.get_height()) // 2 - 50
        bg = pygame.Surface((textsurface.get_width()+ 50, textsurface.get_height()+ 20))
        bg.set_alpha(128)
        bg.fill(pygame.Color(255, 255, 255, 128))
        self.win.blit(bg,(x-25, y-10))
        self.win.blit(textsurface, (x, y))

    def ai_move(self, board):
        self.board = board
        self.change_turn()