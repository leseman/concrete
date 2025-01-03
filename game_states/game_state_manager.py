class GameStateManager:
    def __init__(self):
        self.states = {}
        self.current_state = None

    def get_current_state(self):
        return self.current_state
    
    def add_state(self, name, state):
        self.states[name] = state
    
    def set_state(self, name):
        if self.current_state:
            self.current_state.exit()
        self.current_state = self.states[name]
        self.current_state.enter()
    
    def handle_event(self, event):
        if self.current_state:
            self.current_state.handle_event(event)
    
    def update(self, dt):
        if self.current_state:
            self.current_state.update(dt)
    
    def draw(self, screen):
        if self.current_state:
            self.current_state.draw(screen)

    def restart_game(self):
        from game_states.playing_state import PlayingState
        new_playing_state = PlayingState(self)
        self.states["playing"] = new_playing_state
        self.set_state("playing")