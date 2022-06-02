#!/usr/bin/python3.4
# Setup Python ----------------------------------------------- #
import pygame, sys

# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('rampy boi')
screen = pygame.display.set_mode((500, 500), 0, 32)

tile_size = 50

class tile():
    def __init__(self, pos, tile_type, ramp=0): # 0 = none, 1 = right, 2 = left
        self.pos = pos
        self.type = tile_type
        self.ramp = ramp

def collision_test(object_1,object_list):
    collision_list = []
    for obj in object_list:
        if obj.colliderect(object_1):
            collision_list.append(obj)
    return collision_list

def tile_rect(t):
    return pygame.Rect(t.pos[0] * tile_size, t.pos[1] * tile_size, tile_size, tile_size)

class player():
    def __init__(self, pos):
        self.pos = pos
        self.color = (0, 0, 255)
        self.rect = pygame.Rect(pos[0], pos[1], 25, 50)
        self.vertical_momentum = 0

    def move(self, movement, tiles):
        normal_tiles = [tile_rect(t) for t in tiles if not t.ramp] # make list of all normal tile rects
        ramps = [t for t in tiles if t.ramp] # make list of all ramps

        # handle standard collisions
        collision_types = {'top':False,'bottom':False,'right':False,'left':False}
        self.pos[0] += movement[0]
        self.rect.x = int(self.pos[0])
        tile_hit_list = collision_test(self.rect, normal_tiles)
        for t in tile_hit_list:
            if movement[0] > 0:
                self.rect.right = t.left
                collision_types['right'] = True
            elif movement[0] < 0:
                self.rect.left = t.right
                collision_types['left'] = True
            self.pos[0] = self.rect.x
        self.pos[1] += movement[1]
        self.rect.y = int(self.pos[1])
        tile_hit_list = collision_test(self.rect, normal_tiles)
        for t in tile_hit_list:
            if movement[1] > 0:
                self.rect.bottom = t.top
                collision_types['bottom'] = True
            elif movement[1] < 0:
                self.rect.top = t.bottom
                collision_types['top'] = True
            self.pos[1] = self.rect.y

        # handle ramps
        for ramp in ramps:
            hitbox = tile_rect(ramp)
            if self.rect.colliderect(hitbox): # check if player collided with the bounding box for the ramp
                # get player's position relative to the ramp on the x axis
                rel_x = self.rect.x - hitbox.x

                # get height at player's position based on type of ramp
                if ramp.ramp == 1:
                    pos_height = rel_x + self.rect.width # go by player right edge on right ramps
                elif ramp.ramp == 2:
                    pos_height = tile_size - rel_x # is already left edge by default

                # add constraints
                pos_height = min(pos_height, tile_size)
                pos_height = max(pos_height, 0)

                target_y = hitbox.y + tile_size - pos_height

                if self.rect.bottom > target_y: # check if the player collided with the actual ramp
                    # adjust player height
                    self.rect.bottom = target_y
                    self.pos[1] = self.rect.y

                    collision_types['bottom'] = True

        # return collisions
        return collision_types

# generate test map
tiles = [tile([3, 8], 'red', 1), tile([5, 8], 'red', 1), tile([6, 8], 'red'), tile([4, 6], 'red'), tile([4, 5], 'red', 2), tile([3, 5], 'red')]
for i in range(10):
    tiles.append(tile([i, 9], 'red'))

p = player([100, 300])

right = False
left = False

# Loop ------------------------------------------------------- #
while True:
    
    # Background --------------------------------------------- #
    screen.fill((0, 0, 0))

    # Player ------------------------------------------------- #
    p.vertical_momentum += 1
    p.vertical_momentum = min(p.vertical_momentum, 15)
    player_movement = [0, p.vertical_momentum]

    if right:
        player_movement[0] += 5
    if left:
        player_movement[0] -= 5

    collisions = p.move(player_movement, tiles)
    if (collisions['bottom']) or (collisions['top']):
        p.vertical_momentum = 0

    pygame.draw.rect(screen, p.color, p.rect)

    # Tiles -------------------------------------------------- #
    for t in tiles:
        color = (0, 0, 0)
        if t.type == 'red':
            color = (255, 0, 0)
        if t.ramp == 0:
            pygame.draw.rect(screen, color, tile_rect(t))
        elif t.ramp == 1:
            pygame.draw.polygon(screen, color, [[t.pos[0] * tile_size, (t.pos[1] + 1) * tile_size - 1], [(t.pos[0] + 1) * tile_size - 1, (t.pos[1] + 1) * tile_size - 1], [(t.pos[0] + 1) * tile_size - 1, t.pos[1] * tile_size]])
        elif t.ramp == 2:
            pygame.draw.polygon(screen, color, [[t.pos[0] * tile_size, (t.pos[1] + 1) * tile_size - 1], [(t.pos[0] + 1) * tile_size - 1, (t.pos[1] + 1) * tile_size - 1], [t.pos[0] * tile_size, t.pos[1] * tile_size]])
    
    # Buttons ------------------------------------------------ #
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_RIGHT:
                right = True
            if event.key == K_LEFT:
                left = True
            if event.key == K_UP:
                p.vertical_momentum = -16
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                right = False
            if event.key == K_LEFT:
                left = False
                
    # Update ------------------------------------------------- #
    pygame.display.update()
    mainClock.tick(60)