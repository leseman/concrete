import pygame

class NPC(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, npc_type):
        super().__init__()
        self.type = npc_type
        self.state = "idle"
        # NPC AI and behavior methods