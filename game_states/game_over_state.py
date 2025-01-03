from game_states.game_state import GameState
import pygame

class GameOverState(GameState):
    def __init__(self, state_manager, score):
        super().__init__(state_manager)
        self.score = score
        self.font = pygame.font.Font(None, 74)
        
    def draw(self, screen):
        screen.fill((0, 0, 0))
        game_over = self.font.render('Game Over', True, (255, 0, 0))
        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        restart_text = self.font.render('Press R to Restart', True, (255, 255, 255))
        
        screen.blit(game_over, (400 - game_over.get_width()//2, 200))
        screen.blit(score_text, (400 - score_text.get_width()//2, 300))
        screen.blit(restart_text, (400 - restart_text.get_width()//2, 400))
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.state_manager.restart_game()