import pygame
from game_states.game_state import GameState
from utils.config import *

class MenuState(GameState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.title_font = pygame.font.Font(None, 64)
        self.subtitle_font = pygame.font.Font(None, 32)
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Transition to playing state
                self.state_manager.set_state("playing")
    
    def update(self, dt):
        pass
    
    def draw(self, screen):
        screen.fill(BLACK)
        
        # Draw title
        title_text = self.title_font.render("Concrete Kingdom", True, WHITE)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        screen.blit(title_text, title_rect)
        
        # Draw "Press SPACE to Start"
        start_text = self.subtitle_font.render("Press SPACE to Start", True, WHITE)
        start_rect = start_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100))
        screen.blit(start_text, start_rect)