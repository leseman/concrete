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
        self.direction = pygame.math.Vector2(0, 0)  # Add this line
        self.rect.center = self.position
        self.speed = 100
        self.health = 100
        
    def update(self, dt, player_pos):
        # Simple AI: Move towards player
        self.direction = pygame.math.Vector2(player_pos) - self.position  # Store direction
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()
            self.position += self.direction * self.speed * dt
            self.rect.center = self.position

    def take_damage(self, amount):
        self.health -= amount
        return self.health <= 0
    
    def reverse_direction(self):
        if self.direction.length() > 0:  # Add check to prevent zero vector multiplication
            self.direction *= -1  # Reverse the direction vector