import pygame
import random
from entities.player import Player
from entities.npc import NPC
from game_states.game_state import GameState
from game_states.game_over_state import GameOverState
from utils.config import *
from utils.collision import *

class PlayingState(GameState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.all_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.player = Player(400, 300, self.bullets)
        self.npcs = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.bullets)
        self.spawn_npcs(5)  # Start with 5 NPCs
        
    def spawn_npcs(self, count):
        for _ in range(count):
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            npc = NPC(x, y)
            self.npcs.add(npc)
            self.all_sprites.add(npc)
    
    def handle_event(self, event):
        self.player.handle_event(event)

    def update(self, dt):
        self.player.update(dt)
        mouse_pos = pygame.mouse.get_pos()
        self.player.rotate_to_mouse(mouse_pos)

        # Update bullets and check collisions
        for bullet in self.bullets:
            bullet.update(dt)
            hits = pygame.sprite.spritecollide(bullet, self.npcs, False)
            for npc in hits:
                if npc.take_damage(34):  # 3 shots to kill
                    npc.kill()
                    self.player.score += 100
                bullet.kill()
                break
        
        # Update NPCs and check NPC collisions
        for npc in self.npcs:
            npc.update(dt, self.player.position)
            
            # Check NPC collision with player
            if check_collision(npc, self.player):
                self.player.take_damage(10)
                
            # Check NPC collision with other NPCs
            for other_npc in self.npcs:
                if npc != other_npc and check_collision(npc, other_npc):
                    npc.reverse_direction()
                    other_npc.reverse_direction()

        if self.player.health <= 0:
            self.state_manager.add_state("game_over", GameOverState(self.state_manager, self.player.score))
            self.state_manager.set_state("game_over")
            return

    def draw(self, screen):
        screen.fill(BLACK)
        self.all_sprites.draw(screen)