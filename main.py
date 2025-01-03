import pygame
import sys
from game_states.game_state_manager import GameStateManager
from game_states.menu_state import MenuState
from game_states.playing_state import PlayingState
from game_states.mission_state import MissionState
from game_states.game_over_state import GameOverState
from utils.config import *
from utils.ui import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Concrete Kingdom")
        self.clock = pygame.time.Clock()
        self.state_manager = GameStateManager()
        self.init_states()

    def init_states(self):
        self.state_manager.add_state("menu", MenuState(self.state_manager))
        self.state_manager.add_state("playing", PlayingState(self.state_manager))
        self.state_manager.add_state("mission", MissionState(self.state_manager))
        self.state_manager.set_state("menu")

    def run(self):
        while True:
            dt = self.clock.tick(60) / 1000.0
           
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.state_manager.handle_event(event)
           
            self.state_manager.update(dt)
            self.state_manager.draw(self.screen)

            current_state = self.state_manager.get_current_state()
            if isinstance(current_state, PlayingState):
                draw_ui(self.screen, current_state.player)
        
            pygame.display.flip()

if __name__ == "__main__":
   game = Game()
   game.run()