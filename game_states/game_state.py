class GameState:
    def __init__(self, state_manager):
        self.state_manager = state_manager
    
    def enter(self):
        pass
        
    def exit(self):
        pass
        
    def handle_event(self, event):
        pass
        
    def update(self, dt):
        pass
        
    def draw(self, screen):
        pass