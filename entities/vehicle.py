import pygame

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, vehicle_type):
        super().__init__()
        self.type = vehicle_type
        self.occupied = False
        # Vehicle specific properties and methods