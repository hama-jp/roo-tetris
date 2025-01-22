import pygame
import random
from tetromino import Tetromino, TetrominoType

class Game:
    def __init__(self):
        # SDL音声ドライバー設定（WSL用）
        import os
        os.environ['SDL_AUDIODRIVER'] = 'pulseaudio'  # dspからpulseaudioに変更
        
        pygame.init()
        try:
            # ミキサー初期化パラメータ追加
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
        except pygame.error as e:
            print(f"Sound initialization failed: {e}")
            self.sound_enabled = False
        else:
            self.sound_enabled = True
            
        self.screen = pygame.display.set_mode((500, 600))
        self.base_font = pygame.font.Font(None, 36)
        self.high_score = 0
        
        # サウンドエフェクトの安全な読み込み
        self.sounds = {}
        if self.sound_enabled:
            try:
                self.sounds = {
                    'rotate': pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'sound_rotate.wav')),
                    'line_clear': pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'sound_clear.wav')),
                    'gameover': pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'sound_gameover.wav'))
                }
            except FileNotFoundError as e:
                print(f"Sound file not found: {e}")
                self.sound_enabled = False
        
        # カラー設定
        self.bg_color = (30, 30, 30)
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
                        board_y < 0 or board_y >= self.height or
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
            # 難易度調整（スコアに応じて速度アップ）
            level = min(self.score // 1000 + 1, 15)
            self.clock.tick(5 + level)
            
            # キーリピート設定
            pygame.key.set_repeat(200, 50)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                
                # 改良された入力処理
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

            # 接着遅延処理
            # 自然落下処理（接着遅延対応版）
            current_time = pygame.time.get_ticks()
            
            if not self._check_collision(offset_y=1):
                self.current_piece.y += 1
                self.lock_timer = 0  # リセット
            else:
                # 操作による移動があった場合はタイマーリセット
                if any(pygame.key.get_pressed()[k] for k in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN)):
                    self.lock_timer = current_time
                
                if self.lock_timer == 0:
                    self.lock_timer = current_time
                elif current_time - self.lock_timer > 500:  # 500ms経過
                    self._merge_piece()
                    self._spawn_new_piece()
                    self.lock_timer = 0
                    if self._check_collision():
                        self.game_over = True

            self.screen.fill((0, 0, 0))
            
            # ボードの描画（背景と枠線追加）
            # ボード背景
            pygame.draw.rect(self.screen, (30, 30, 60),
                           (0, 0, self.width*self.grid_size, self.height*self.grid_size))
            
            # セル描画
            for y, row in enumerate(self.board):
                for x, val in enumerate(row):
                    if val:
                        pygame.draw.rect(self.screen, self._get_color(val),
                            (x*self.grid_size, y*self.grid_size, self.grid_size-1, self.grid_size-1))
            
            # ボード枠線（青色）
            pygame.draw.rect(self.screen, (0, 120, 255),
                           (0, 0, self.width*self.grid_size, self.height*self.grid_size), 2)
            
            # 現在のテトリミノの描画
            for y, row in enumerate(self.current_piece.matrix):
                for x, val in enumerate(row):
                    if val:
                        px = (self.current_piece.x + x) * self.grid_size
                        py = (self.current_piece.y + y) * self.grid_size
                        pygame.draw.rect(self.screen, self.current_piece.color,
                            (px, py, self.grid_size-1, self.grid_size-1))
            
            # スコア表示の改善
            score_text = self.base_font.render(f'SCORE: {self.score}', True, (255, 255, 255))
            hi_score_text = self.base_font.render(f'HIGH: {self.high_score}', True, (200, 200, 200))
            
            # テキスト背景
            pygame.draw.rect(self.screen, self.bg_color, (5, 5, 200, 70))
            self.screen.blit(score_text, (10, 10))
            self.screen.blit(hi_score_text, (10, 40))
            
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

        # ゲームオーバー処理の改善
        self.high_score = max(self.score, self.high_score)
        overlay = pygame.Surface((500, 600), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        
        game_over_text = self.base_font.render('GAME OVER', True, (255, 50, 50))
        restart_text = self.base_font.render('Press R to Restart', True, (255, 255, 255))
        final_score_text = self.base_font.render(f'Final Score: {self.score}', True, (255, 255, 255))
        
        self.screen.blit(overlay, (0, 0))
        self.screen.blit(game_over_text, (250 - game_over_text.get_width()//2, 200))
        self.screen.blit(final_score_text, (250 - final_score_text.get_width()//2, 250))
        self.screen.blit(restart_text, (250 - restart_text.get_width()//2, 300))
        pygame.display.update()
        
        # リスタート待機ループ
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__init__()
                        self.run()
                        waiting = False
                    if event.key == pygame.K_q:
                        waiting = False
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
