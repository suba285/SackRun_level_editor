import pygame
from image_loader import img_loader
from map import *

pygame.init()

# 10 - gem
# 11 - dirt
# 12 - stone
# 13 - free tile
# 14 - free tile
# 15 - free tile
# 16 - free tile
# 17 - free tile
# 18 - wheat
# 19 - fake bee hive
# 20 - portal
# 21 - dirt tile rocks
# 22 - greenhouse
# 23 - bear trap
# 24 - platform
# 25 - wobbly mushrooms
# 26 - hot lava start
# 27 - hot lava stop
# 28 - real bee hive
# 29 - shockwave mushroom
# 30 - set lava
# 31 - set lava left
# 32 - set lava right
# 33 - short grass
# 34 - short grass left
# 35 - short grass right
# 36 - bush
# 37 - spitting plant left
# 38 - spitting plant right
# 39 - spitting plant up
# 40 - log
# 41 - birch tree
# 42 - tree
# 43 - flowers
# 44 - leek patch
# 45 - carrot patch
# 46 - lettuce patch
# 47 - background tile
# 48 - dark background tile

tile_key = {
    1: 10,
    2: 11,
    3: 12,
    4: 18,
    5: 19,
    6: 20,
    7: 21,
    8: 22,
    9: 23,
    10: 24,
    11: 25,
    12: 26,
    13: 27,
    14: 28,
    15: 29,
    16: 30,
    17: 31,
    18: 32,
    19: 33,
    20: 34,
    21: 35,
    22: 36,
    23: 37,
    24: 38,
    25: 39,
    26: 40,
    27: 41,
    28: 42,
    29: 43,
    30: 44,
    31: 45,
    32: 46,
    33: 47,
    34: 48
}

inverted_tile_key = {v: k for k, v in tile_key.items()}

big_tiles = {
    19: (32, 48),
    22: (96, 64),
    28: (32, 48),
    36: (64, 64),
    40: (64, 32),
    41: (32, 96),
    42: (64, 64)
}

map = level7
run = True
tile_size = 30
width = 1200
canvas_width = 1020
height = 900

start_line_x = 0
start_line_y = 0

tile_counter = 1

screen = pygame.display.set_mode((width, height))

pygame.display.set_caption('level editor')

tile_list = []
rects = []

row_count = 0
for column in range(int(canvas_width / tile_size)):
    col_count = 0
    for tile in range(int(height / tile_size)):
        y = row_count * tile_size
        x = col_count * tile_size
        rects.append(pygame.Rect(x, y, tile_size, tile_size))
        col_count += 1
    row_count += 1


# loading images -------------------------------------------------------------------------------------------------------
background = pygame.transform.scale(pygame.image.load('menu_background.png'), (canvas_width, height))

tile_images = {
    10: img_loader('data/images/gem.PNG', tile_size / 2, tile_size / 2),
    11: img_loader(f'data/images/tile_dirt.PNG', tile_size, tile_size),
    12: img_loader(f'data/images/tile_stone.PNG', tile_size, tile_size),
    18: img_loader('data/images/light_wheat_plant.PNG', 3, tile_size),
    19: img_loader('data/images/bee_hive.PNG', tile_size, 1.5 * tile_size),
    20: img_loader('data/images/portal.PNG', tile_size, tile_size),
    21: img_loader(f'data/images/tile_dirt_rocks.PNG', tile_size, tile_size),
    22: img_loader('data/images/greenhouse.PNG', tile_size * 3, tile_size * 2),
    23: img_loader('data/images/bear_trap_shut.PNG', tile_size, tile_size / 2),
    24: img_loader('data/images/platform.PNG', tile_size, tile_size),
    25: img_loader('data/images/green_mushroom.PNG', tile_size / 2, tile_size / 2),
    26: img_loader('data/images/hot_lava_start.PNG', tile_size, tile_size),
    27: img_loader('data/images/hot_lava_end.PNG', tile_size, tile_size),
    28: img_loader('data/images/bee_hive.PNG', tile_size, 1.5 * tile_size),
    29: img_loader('data/images/shockwave_mushroom.PNG', tile_size, tile_size / 2),
    30: img_loader('data/images/lava.PNG', tile_size, 5),
    31: img_loader('data/images/lava_edge.PNG', tile_size, 5),
    32: pygame.transform.flip(img_loader('data/images/lava_edge.PNG', tile_size, 5), True, False),
    33: img_loader('data/images/short_grass.PNG', tile_size, tile_size),
    34: img_loader('data/images/short_grass_left.PNG', tile_size, tile_size),
    35: img_loader('data/images/short_grass_right.PNG', tile_size, tile_size),
    36: img_loader('data/images/bush1.PNG', 2 * tile_size, 2 * tile_size),
    37: img_loader('data/images/spitting_plant0.PNG', tile_size, tile_size),
    38: pygame.transform.flip(img_loader('data/images/spitting_plant0.PNG', tile_size, tile_size), True, False),
    39: img_loader('data/images/spitting_plant_up0.PNG', tile_size, tile_size),
    40: img_loader('data/images/log0.PNG', 2 * tile_size, tile_size),
    41: img_loader('data/images/tree_birch.PNG', tile_size, tile_size * 3),
    42: img_loader('data/images/tree.PNG', 2 * tile_size, 2 * tile_size),
    43: img_loader('data/images/short_flowers_together.PNG', tile_size, tile_size),
    44: img_loader('data/images/leek_patch.PNG', tile_size, tile_size),
    45: img_loader('data/images/carrot_patch.PNG', tile_size, tile_size),
    46: img_loader('data/images/lettuce_patch.PNG', tile_size, tile_size),
    47: img_loader('data/images/tile_bg.PNG', tile_size, tile_size),
    48: img_loader('data/images/tile_bg_dark.PNG', tile_size, tile_size)
}


def draw_grid(start_line_x, start_line_y):
    for num in range(int((canvas_width/tile_size) + 1)):
        pygame.draw.line(screen, (90, 90, 90), (start_line_x, 0), (start_line_x, height), 2)
        start_line_x += tile_size
    for num in range(int((height/tile_size) + 1)):
        pygame.draw.line(screen, (90, 90, 90), (0, start_line_y), (canvas_width, start_line_y), 2)
        start_line_y += tile_size


# variables
click = False
delete = False
a_press = False
d_press = False
switch_counter = 30

clock = pygame.time.Clock()

selected_tile_surf = pygame.Surface((tile_size * 3, tile_size * 2))

# ======================================================================================================================
while run:
    mouse_pos = pygame.mouse.get_pos()

    clock.tick(60)

    selected_tile_surf.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                tile_counter -= 1
                a_press = True
            if event.key == pygame.K_d:
                tile_counter += 1
                d_press = True
            if event.key == pygame.K_s:
                delete = True
            if event.key == pygame.K_p:
                for row in map:
                    print(f'{row},')
            if event.key == pygame.K_b:
                row_count = 0
                for row in map:
                    col_count = 0
                    for col in row:
                        if col not in [47, 48]:
                            map[row_count][col_count] = 0
                        col_count += 1
                    row_count += 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                delete = False
            if event.key == pygame.K_d:
                d_press = False
                switch_counter = 30
            if event.key == pygame.K_a:
                a_press = False
                switch_counter = 30

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            click = False

    if d_press:
        switch_counter -= 1
        if switch_counter < 0:
            tile_counter += 1
            switch_counter = 7
    if a_press:
        switch_counter -= 1
        if switch_counter < 0:
            tile_counter -= 1
            switch_counter = 7

    if tile_counter < 1:
        tile_counter = 34
    if tile_counter > 34:
        tile_counter = 1

    row_count = 0
    for row in map:
        col_count = 0
        for tile in row:
            x = col_count * tile_size
            y = row_count * tile_size
            rect = pygame.Rect(x, y, tile_size, tile_size)
            if rect.collidepoint(mouse_pos):
                if click:
                    map[row_count][col_count] = tile_key[tile_counter]
                if delete:
                    map[row_count][col_count] = 0
            if tile != 0:
                screen.blit(tile_images[tile], rect)
            col_count += 1
        row_count += 1

    img = tile_images[tile_key[tile_counter]]
    selected_tile_surf.blit(img, (tile_size * 1.5 - img.get_width() / 2, tile_size - img.get_height() / 2))

    screen.blit(pygame.transform.scale(selected_tile_surf,
                                       (tile_size * 6, tile_size * 4)), (width - tile_size * 6, tile_size * 3))

    draw_grid(start_line_x, start_line_y)

    pygame.display.update()

pygame.quit()
