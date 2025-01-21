import pygame
import random
from tetromino import Tetromino, TetrominoType

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((500, 600))  # プレビュー領域追加のため幅を拡張
        
        # 色のマッピング
        self.colors = {
            1: (0, 255, 255),   # I
            2: (255, 255, 0),   # O
            3: (128, 0, 128),   # T
            4: (0, 255, 0),     # S
            5: (255, 0, 0),     # Z
            6: (0, 0, 255),     # J
            7: (255, 165, 0)    # L
        }
        pygame.display.set_caption("Tetris Deep Seek")
        self.clock = pygame.time.Clock()
        
        self.grid_size = 30
        self.width = 10
        self.height = 20
        self.board = [[0] * self.width for _ in range(self.height)]
        
        self.current_piece = None
        self.next_piece = self._new_piece()
        self._spawn_new_piece()
        self.score = 0
        self.game_over = False

    def _new_piece(self):
        return Tetromino.create(random.choice(list(TetrominoType)))
        
    def _spawn_new_piece(self):
        self.current_piece = self.next_piece
        self.next_piece = self._new_piece()
        self.current_piece.x = self.width // 2 - len(self.current_piece.matrix[0]) // 2
        self.current_piece.y = 0

    def _check_collision(self, offset_x=0, offset_y=0):
        for y, row in enumerate(self.current_piece.matrix):
            for x, cell in enumerate(row):
                if cell:
                    board_x = self.current_piece.x + x + offset_x
                    board_y = self.current_piece.y + y + offset_y
                    if (board_x < 0 or board_x >= self.width or
                        board_y >= self.height or
                        self.board[board_y][board_x]):
                        return True
        return False

    def _merge_piece(self):
        for y, row in enumerate(self.current_piece.matrix):
            for x, cell in enumerate(row):
                if cell:
                    self.board[y + self.current_piece.y][x + self.current_piece.x] = cell
        self._clear_lines()

    def _get_color(self, val: int) -> tuple[int, int, int]:
        return self.colors.get(val, (0, 0, 0))

    def _clear_lines(self):
        lines_cleared = 0
        new_board = []
        for row in self.board:
            if 0 not in row:
                lines_cleared += 1
            else:
                new_board.append(row)
        self.score += lines_cleared ** 2 * 100
        self.board = [[0]*self.width for _ in range(lines_cleared)] + new_board

    def run(self):
        while not self.game_over:
            self.clock.tick(5)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if not self._check_collision(offset_x=-1):
                            self.current_piece.x -= 1
                    elif event.key == pygame.K_RIGHT:
                        if not self._check_collision(offset_x=1):
                            self.current_piece.x += 1
                    elif event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                        self.current_piece.rotate()
                    elif event.key == pygame.K_DOWN:
                        if not self._check_collision(offset_y=1):
                            self.current_piece.y += 1

            if not self._check_collision(offset_y=1):
                self.current_piece.y += 1
            else:
                self._merge_piece()
                self._spawn_new_piece()
                if self._check_collision():
                    self.game_over = True

            self.screen.fill((0, 0, 0))
            
            # ボードの描画
            for y, row in enumerate(self.board):
                for x, val in enumerate(row):
                    if val:
                        pygame.draw.rect(self.screen, self._get_color(val),
                            (x*self.grid_size, y*self.grid_size, self.grid_size-1, self.grid_size-1))
            
            # 現在のテトリミノの描画
            for y, row in enumerate(self.current_piece.matrix):
                for x, val in enumerate(row):
                    if val:
                        px = (self.current_piece.x + x) * self.grid_size
                        py = (self.current_piece.y + y) * self.grid_size
                        pygame.draw.rect(self.screen, self.current_piece.color,
                            (px, py, self.grid_size-1, self.grid_size-1))
            
            # スコア表示
            font = pygame.font.SysFont('Arial', 24)
            score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))
            
            # ネクストテトリミノ表示
            preview_x = self.width * self.grid_size + 50
            preview_y = 100
            preview_size = 4 * self.grid_size
            
            # プレビュー背景
            pygame.draw.rect(self.screen, (50, 50, 50), 
                           (preview_x, preview_y, preview_size, preview_size))
            
            # ネクストテトリミノ描画
            for y, row in enumerate(self.next_piece.matrix):
                for x, cell in enumerate(row):
                    if cell:
                        px = preview_x + x * self.grid_size + (preview_size - len(self.next_piece.matrix[0]) * self.grid_size) // 2
                        py = preview_y + y * self.grid_size + (preview_size - len(self.next_piece.matrix) * self.grid_size) // 2
                        pygame.draw.rect(self.screen, self.next_piece.color,
                            (px, py, self.grid_size-1, self.grid_size-1))
            
            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
