# entities/player.py
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Create a simple rectangle for the player sprite
        self.image = pygame.Surface((32, 32))
        self.image.fill((0, 255, 0))  # Green color for now
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Player attributes
        self.speed = 300  # pixels per second
        self.health = 100
        self.score = 0
        self.position = pygame.math.Vector2(x, y)
        
    def update(self, dt):
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