import pygame

class MenuState:
    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.font = pygame.font.Font(None, 74)
        self.title = self.font.render('Concrete Kingdom', True, (255, 255, 255))
        self.start_text = self.font.render('Press SPACE to Start', True, (255, 255, 255))
        
    def enter(self):
        pass
        
    def exit(self):
        pass
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.state_manager.set_state("playing")
                
    def update(self, dt):
        pass
        
    def draw(self, screen):
        screen.fill((0, 0, 0))  # Black background
        
        # Center the title
        title_rect = self.title.get_rect(center=(screen.get_width() // 2, 200))
        screen.blit(self.title, title_rect)
        
        # Center the start text
        start_rect = self.start_text.get_rect(center=(screen.get_width() // 2, 400))
        screen.blit(self.start_text, start_rect)