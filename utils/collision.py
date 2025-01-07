import pygame
import math
from typing import List, Tuple

def get_triangle_points(sprite) -> List[Tuple[float, float]]:
    """
    Get the actual triangle points of the player sprite, taking rotation into account.
    """
    # Base triangle points (40x30 triangle)
    base_points = [(0, 30), (40, 15), (0, 0)]
    
    # Get the center of the sprite
    center = sprite.rect.center
    
    # Convert points to be relative to center
    centered_points = [
        (x - 20, y - 15) for x, y in base_points  # 20,15 is half of 40,30
    ]
    
    # Rotate points
    rotated_points = []
    for x, y in centered_points:
        angle_rad = math.radians(sprite.angle)
        rotated_x = x * math.cos(angle_rad) - y * math.sin(angle_rad)
        rotated_y = x * math.sin(angle_rad) + y * math.cos(angle_rad)
        rotated_points.append((
            rotated_x + center[0],
            rotated_y + center[1]
        ))
    
    return rotated_points

def point_in_triangle(px: float, py: float, triangle_points: List[Tuple[float, float]]) -> bool:
    """
    Check if a point is inside a triangle using barycentric coordinates.
    """
    def sign(p1: Tuple[float, float], p2: Tuple[float, float], p3: Tuple[float, float]) -> float:
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
    
    v1, v2, v3 = triangle_points
    d1 = sign((px, py), v1, v2)
    d2 = sign((px, py), v2, v3)
    d3 = sign((px, py), v3, v1)
    
    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    
    return not (has_neg and has_pos)

def check_collision_precise(sprite1, sprite2) -> bool:
    """
    More precise collision detection between sprites.
    For Player (triangle) vs NPC/Bullet (rectangle) collisions.
    """
    # If sprite1 is the player (has angle attribute), use triangle collision
    if hasattr(sprite1, 'angle'):
        triangle_points = get_triangle_points(sprite1)
        rect_points = [
            sprite2.rect.topleft,
            sprite2.rect.topright,
            sprite2.rect.bottomleft,
            sprite2.rect.bottomright
        ]
        for point in rect_points:
            if point_in_triangle(point[0], point[1], triangle_points):
                return True
        return False
    elif hasattr(sprite2, 'angle'):
        return check_collision_precise(sprite2, sprite1)
    else:
        return sprite1.rect.colliderect(sprite2.rect)

def resolve_collision(sprite1, sprite2):
    """
    Push overlapping sprites apart.
    """
    # Calculate center points
    center1 = pygame.math.Vector2(sprite1.rect.center)
    center2 = pygame.math.Vector2(sprite2.rect.center)
    
    # Calculate direction and distance
    direction = center1 - center2
    if direction.length() > 0:  # Avoid division by zero
        direction = direction.normalize()
    else:
        direction = pygame.math.Vector2(1, 0)  # Default push right if centers overlap
    
    # Push sprites apart
    push_distance = (sprite1.rect.width + sprite2.rect.width) * 0.55  # Slightly more than half combined width
    
    # Update positions
    sprite1.position = center2 + direction * push_distance
    sprite2.position = center1 - direction * push_distance
    
    # Update rectangles
    sprite1.rect.center = sprite1.position
    sprite2.rect.center = sprite2.position

def handle_collisions(player, npcs, bullets):
    """
    Handle all game collisions and their effects.
    """
    # Check bullet collisions with NPCs
    for bullet in bullets:
        for npc in npcs:
            if check_collision_precise(bullet, npc):
                # Damage NPC
                if npc.take_damage(25):  # Returns True if NPC dies
                    npc.kill()
                    player.score += 100
                # Remove bullet
                bullet.kill()
    
    # Check player collision with NPCs
    for npc in npcs:
        if check_collision_precise(player, npc):
            # Damage player and knock back NPC
            player.take_damage(10)
            npc.reverse_direction()
            resolve_collision(player, npc)
    
    # Check NPC collisions with other NPCs
    npc_list = list(npcs)
    for i, npc1 in enumerate(npc_list):
        for npc2 in npc_list[i+1:]:
            if check_collision_precise(npc1, npc2):
                resolve_collision(npc1, npc2)
                # Reverse both NPCs' directions
                npc1.reverse_direction()
                npc2.reverse_direction()