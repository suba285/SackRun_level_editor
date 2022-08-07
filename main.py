import pygame
import os
from image_loader import img_loader
from map import *
from button import Button

pygame.init()

clock = pygame.time.Clock()

map = tile_map
run = True
tile_size = 30
width = 1200
canvas_width = 1020
height = 900

start_line_x = 0
start_line_y = 0

current_tile_num = 11

click_cooldown = 30

fps = 60

screen = pygame.display.set_mode((width, height))

pygame.display.set_caption('level editor')

images = []
tiles = []
tile_list = []
list_of_different_tiles = [40, 41, 42, 30, 23, 28, 19]

# loading images -------------------------------------------------------------------------------------------------------
background = pygame.transform.scale(pygame.image.load('menu_background.png'), (canvas_width, height))

list_of_tiles = os.listdir('/Users/johnsubocz/PycharmProjects/SackRun_level_editor/tiles')
num_tiles = len(list_of_tiles)

corner_tile = img_loader('different_size_tiles/background_tile_corner.PNG', tile_size, tile_size)

for num in range(10, num_tiles + 20):
    if num == 40:
        images.append((img_loader('different_size_tiles/tile18.PNG', 2 * tile_size, tile_size), False))
    elif num == 41 or num == 42:
        images.append((img_loader('different_size_tiles/tile30.PNG', 2 * tile_size, 2 * tile_size), False))
    elif num == 30:
        images.append((img_loader('different_size_tiles/tile5.PNG', 2 * tile_size, 2 * tile_size), False))
    elif num == 23:
        images.append((img_loader('different_size_tiles/tile29.PNG', tile_size, tile_size / 2), False))
    elif num == 28 or num == 19:
        img = img_loader(f'tiles/tile{num}.PNG', tile_size, 2 * tile_size)
        selected = False
        tile_inf = (img, selected)
        images.append(tile_inf)
    elif num == 47:
        img = img_loader('different_size_tiles/background_tile.PNG', tile_size, tile_size)
        images.append((img, False))
    elif num == 48:
        img = img_loader('different_size_tiles/background_tile_edges.PNG', tile_size, tile_size)
        images.append((img, False))
    elif num == 49:
        # corner_left
        img = corner_tile
        images.append((img, False))
    elif num == 50:
        # corner_right
        img = pygame.transform.flip(corner_tile, True, False)
        images.append((img, False))
    elif num == 51:
        # corner_left_bottom
        img = pygame.transform.flip(corner_tile, False, True)
        images.append((img, False))
    elif num == 52:
        # corner_right_bottom
        img = pygame.transform.flip(corner_tile, True, True)
        images.append((img, False))
    else:
        img = img_loader(f'tiles/tile{num}.PNG', tile_size, tile_size)
        selected = False
        tile_inf = (img, selected)
        images.append(tile_inf)

for img in images:
    rect = img[0].get_rect()
    tiles.append((img[0], img[1], rect))

default_rect = tiles[0][0].get_rect()


# buttons --------------------------------------------------------------------------------------------------------------
def button_assigner():
    col_counter = 0
    row_counter = 0
    spacer = tile_size/2
    list_of_buttons = []
    for num in range(10, num_tiles + 11):
        num_ok = True
        for i in list_of_different_tiles:
            if num == i:
                num_ok = False
        if num_ok:
            col_counter += 1
            if col_counter > 3:
                row_counter += 1
                col_counter = 0
            x = canvas_width + (spacer * col_counter) + (tile_size * (col_counter - 1))
            y = (spacer * row_counter) + tile_size * (row_counter - 1)
            btn = Button(x, y, tiles[num][0], tiles[num][0])
            list_of_buttons.append(btn)


# tile placing system --------------------------------------------------------------------------------------------------
def tile_system(tile_num, key):
    mouse_pos = pygame.mouse.get_pos()
    sys_row_count = 0
    if pygame.mouse.get_pressed()[0] == 1 or key[pygame.K_x]:
        for row in map:
            sys_column_count = 0
            for column in row:
                temp_rect = tiles[0][0].get_rect()
                temp_rect.x = sys_column_count * tile_size
                temp_rect.y = sys_row_count * tile_size
                if temp_rect.collidepoint(mouse_pos):
                    if key[pygame.K_x]:
                        map[sys_row_count][sys_column_count] = 00
                    else:
                        map[sys_row_count][sys_column_count] = tile_num
                sys_column_count += 1
            sys_row_count += 1


def menu():
    pass


def img_rect_pos(img, col_count, row_count):
    rect = img.get_rect()
    rect.x = col_count * tile_size
    rect.y = row_count * tile_size
    tile = [img, rect]
    return tile


# tile blitting system -------------------------------------------------------------------------------------------------
def blit_tiles_system():
    tile_list = []
    row_count = 0
    for row in map:
        column_count = 0
        for num in row:
            if num != 00:
                tile = img_rect_pos(tiles[num - 10][0], column_count, row_count)
                tile_list.append(tile)

            column_count += 1
        row_count += 1

    return tile_list


def blit_tiles(tile_list, screen):
    for tile in tile_list:
        screen.blit(tile[0], tile[1])


def draw_grid(start_line_x, start_line_y):
    for num in range(int((canvas_width/tile_size) + 1)):
        pygame.draw.line(screen, (90, 90, 90), (start_line_x, 0), (start_line_x, height), 2)
        start_line_x += tile_size
    for num in range(int((height/tile_size) + 1)):
        pygame.draw.line(screen, (90, 90, 90), (0, start_line_y), (canvas_width, start_line_y), 2)
        start_line_y += tile_size


# ======================================================================================================================

tile_list = blit_tiles_system()

while run:

    clock.tick(fps)

    key = pygame.key.get_pressed()

    screen.fill((0, 0, 0))

    screen.blit(background, (0, 0))

    clock.tick(60)
    events = pygame.event.get()

    tile_system(current_tile_num, key)

    draw_grid(start_line_x, start_line_y)

    real_fps = clock.get_fps()

    blit_tiles(tile_list, screen)

    screen.blit(tiles[current_tile_num - 10][0], (canvas_width + tile_size, tile_size))

    if key[pygame.K_p]:
        print(map)

    click_cooldown += 1

    if pygame.mouse.get_pressed()[0] or key[pygame.K_x]:
        tile_list = blit_tiles_system()
    if pygame.mouse.get_pressed()[2] and click_cooldown >= 5:
        click_cooldown = 0
        if key[pygame.K_z]:
            step = -1
        else:
            step = 1
        if current_tile_num == 52 and step > 0:
            current_tile_num = 10
        elif current_tile_num == 10 and step < 0:
            current_tile_num = 52
        else:
            current_tile_num += step

    # quit handling ----------------------------------------------------------------------------------------------------
    for event in events:
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            tile_list = blit_tiles_system()

    pygame.display.update()
