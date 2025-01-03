import pygame
import math
from utils.config import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed=500):
        super().__init__()
        self.image = pygame.Surface((8, 8))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.position = pygame.math.Vector2(x, y)
        self.direction = direction
        self.speed = speed
        self.rect.center = self.position
        
    def update(self, dt):
        self.position += self.direction * self.speed * dt
        self.rect.center = self.position

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, bullets_group):
        super().__init__()
        # Create player triangle shape
        self.original_image = pygame.Surface((40, 30), pygame.SRCALPHA)
        pygame.draw.polygon(self.original_image, (GREEN), [(0, 30), (40, 15), (0, 0)])
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Player attributes
        self.speed = 300
        self.health = 100
        self.score = 0
        self.position = pygame.math.Vector2(x, y)
        self.angle = 0

        # invincibility
        self.invincible = False
        self.invincible_timer = 0
        self.invincible_duration = 1.0
        
        # Shooting attributes
        self.shoot_cooldown = 0.2  # Seconds between shots
        self.shoot_timer = 0
        self.bullets_group = bullets_group
        
    def rotate_to_mouse(self, mouse_pos):
        # Calculate angle to mouse position
        dx = mouse_pos[0] - self.rect.centerx
        dy = mouse_pos[1] - self.rect.centery
        self.angle = math.degrees(math.atan2(-dy, dx))
        
        # Rotate image
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            self.shoot(self.bullets_group)

    def shoot(self, bullets_group):
        # Check if enough time has passed since last shot
        if self.shoot_timer <= 0:
            # Calculate bullet spawn position (at the tip of the player triangle)
            angle_rad = math.radians(self.angle)
            spawn_offset = pygame.math.Vector2(40, 0).rotate(-self.angle)
            spawn_pos = self.position + spawn_offset
            
            # Create bullet with direction based on player angle
            direction = pygame.math.Vector2(1, 0).rotate(-self.angle).normalize()
            bullet = Bullet(spawn_pos.x, spawn_pos.y, direction)
            bullets_group.add(bullet)
            self.groups()[0].add(bullet)
            
            # Reset shoot timer
            self.shoot_timer = self.shoot_cooldown
    
    def update(self, dt):
        # Update shoot timer
        if self.shoot_timer > 0:
            self.shoot_timer -= dt

        # Update invincibility
        if self.invincible:
            self.invincible_timer -= dt
            if self.invincible_timer <= 0:
                self.invincible = False
        
        # Handle movement
        keys = pygame.key.get_pressed()
        direction = pygame.math.Vector2(0, 0)
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction.x = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction.x = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            direction.y = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            direction.y = 1
            
        # Normalize diagonal movement
        if direction.length() > 0:
            direction = direction.normalize()
            
        # Update position
        self.position += direction * self.speed * dt
        self.rect.center = self.position

    def take_damage(self, amount):
        if not self.invincible:
            self.health -= amount
            self.invincible = True
            self.invincible_timer = self.invincible_duration