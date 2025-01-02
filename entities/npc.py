import pygame
import random
import math
from utils.config import *

class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.position = pygame.math.Vector2(x, y)
        self.rect.center = self.position
        self.speed = 100
        self.health = 100
        
    def update(self, dt, player_pos):
        # Simple AI: Move towards player
        direction = pygame.math.Vector2(player_pos) - self.position
        if direction.length() > 0:
            direction = direction.normalize()
            self.position += direction * self.speed * dt
            self.rect.center = self.position

    def take_damage(self, amount):
        self.health -= amount
        return self.health <= 0