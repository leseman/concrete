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
        self.velocity = pygame.math.Vector2(0, 0)
        self.direction = pygame.math.Vector2(0, 0)
        self.rect.center = self.position
        
        # Movement parameters
        self.max_speed = 100
        self.max_force = 200  # Maximum steering force
        self.approach_radius = 100  # Distance to start slowing down
        self.avoid_radius = 50  # Distance to avoid other NPCs
        
        # Health
        self.health = 100
        
    def seek(self, target_pos):
        """Calculate steering force towards target"""
        desired = pygame.math.Vector2(target_pos) - self.position
        distance = desired.length()
        
        if distance > 0:
            desired = desired.normalize()
            
            # Slow down as we approach the target
            if distance < self.approach_radius:
                desired *= self.max_speed * (distance / self.approach_radius)
            else:
                desired *= self.max_speed
                
            # Calculate steering force
            steer = desired - self.velocity
            if steer.length() > self.max_force:
                steer = steer.normalize() * self.max_force
                
            return steer
        return pygame.math.Vector2(0, 0)
    
    def avoid_others(self, npcs):
        """Calculate steering force to avoid other NPCs"""
        steering = pygame.math.Vector2(0, 0)
        nearby_count = 0
        
        for other in npcs:
            if other != self:
                distance = self.position.distance_to(other.position)
                if distance < self.avoid_radius:
                    # Calculate repulsion force
                    diff = self.position - other.position
                    if diff.length() > 0:
                        diff = diff.normalize()
                        # Scale force by distance (closer = stronger)
                        diff *= (self.avoid_radius - distance) / self.avoid_radius
                        steering += diff
                        nearby_count += 1
        
        # Average the steering force
        if nearby_count > 0:
            steering /= nearby_count
            if steering.length() > 0:
                steering = steering.normalize() * self.max_force
        
        return steering
    
    def update(self, dt, player_pos, npcs=None):
        # Calculate seek force towards player
        seek_force = self.seek(player_pos)
        
        # Calculate avoidance force
        avoid_force = pygame.math.Vector2(0, 0)
        if npcs:
            avoid_force = self.avoid_others(npcs)
        
        # Combine forces
        acceleration = seek_force + avoid_force * 1.5  # Increase avoidance weight
        
        # Update velocity
        self.velocity += acceleration * dt
        if self.velocity.length() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed
        
        # Update position
        self.position += self.velocity * dt
        self.rect.center = self.position
        
        # Update direction for collision handling
        if self.velocity.length() > 0:
            self.direction = self.velocity.normalize()

    def take_damage(self, amount):
        self.health -= amount
        return self.health <= 0
    
    def reverse_direction(self):
        if self.velocity.length() > 0:
            # Reverse velocity instead of just direction
            self.velocity *= -1
            self.direction = self.velocity.normalize()