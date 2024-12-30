import pygame

class MissionState:
    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.font = pygame.font.Font(None, 48)
        self.title = self.font.render('Current Mission', True, (255, 255, 255))
        self.mission_text = self.font.render('Deliver the package to Downtown', True, (255, 255, 255))
        self.instruction = self.font.render('Press ESC to return to game', True, (255, 200, 200))
        
    def enter(self):
        pass
        
    def exit(self):
        pass
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state_manager.set_state("playing")
                
    def update(self, dt):
        pass
        
    def draw(self, screen):
        screen.fill((20, 20, 40))  # Dark blue-ish background
        
        # Draw mission information
        title_rect = self.title.get_rect(center=(screen.get_width() // 2, 100))
        mission_rect = self.mission_text.get_rect(center=(screen.get_width() // 2, 250))
        instruction_rect = self.instruction.get_rect(center=(screen.get_width() // 2, 500))
        
        screen.blit(self.title, title_rect)
        screen.blit(self.mission_text, mission_rect)
        screen.blit(self.instruction, instruction_rect)