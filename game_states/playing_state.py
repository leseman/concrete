import pygame
from entities.player import Player

class PlayingState:
    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.player = Player(400, 300)  # Start player in middle of screen
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        
        # Debug font for showing stats
        self.font = pygame.font.Font(None, 36)
        
    def enter(self):
        # Called when entering this state
        pass
        
    def exit(self):
        # Called when exiting this state
        pass
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state_manager.set_state("menu")
                
    def update(self, dt):
        self.all_sprites.update(dt)
        
    def draw(self, screen):
        screen.fill((50, 50, 50))  # Dark gray background
        self.all_sprites.draw(screen)
        
        # Draw score/stats
        score_text = self.font.render(f'Score: {self.player.score}', True, (255, 255, 255))
        health_text = self.font.render(f'Health: {self.player.health}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(health_text, (10, 50))