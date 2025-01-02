import pygame
from game_states.game_state import GameState
from utils.config import *

class MenuState(GameState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.font = pygame.font.Font(None, 74)
        self.title = self.font.render('Concrete Kingdom', True, (WHITE))
        self.start_text = self.font.render('Press SPACE to Start', True, (WHITE))
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.state_manager.set_state("playing")

    def draw(self, screen):
        screen.fill(BLACK)
        screen.blit(self.title, (screen.get_width()//2 - self.title.get_width()//2, 200))
        screen.blit(self.start_text, (screen.get_width()//2 - self.start_text.get_width()//2, 300))