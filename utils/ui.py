import pygame
from utils.config import *

def draw_ui(screen, player):
    # Render health
    font = pygame.font.Font(None, 36)
    health_text = font.render(f"Health: {player.health}", True, (RED))
    screen.blit(health_text, (10, 10))
    
    # Render score
    score_text = font.render(f"Score: {player.score}", True, (WHITE))
    screen.blit(score_text, (10, 50))