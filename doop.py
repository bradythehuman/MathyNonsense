import math
from random import randint
import sys, pygame
from pygame.locals import *
# from enum import Enum, auto


def circle_build_pit(center):
    rot = 0
    mag = 110
    min_mag = 50
    origional_mag = mag
    expand_mod = 1
    expand_flag = True
    expand_invert_mod = 50
    pnts = []
    while rot < 360:
        pnts.append((center[0] + mag * math.cos(math.radians(rot)), center[1] + mag * math.sin(math.radians(rot))))
        if expand_mod > 0:
            mag += randint(0, expand_mod)
        elif expand_mod < 0:
            mag += randint(expand_mod, 0)
        rot += 1
        if (randint(0, expand_invert_mod) == 0) or (mag < min_mag and not expand_flag) or \
                (expand_mod > 10 and expand_flag) or (expand_mod < -10 and not expand_flag) or\
                (rot > 280 and bool(mag > origional_mag) == expand_flag):
            expand_flag = not expand_flag
        if expand_flag:
            expand_mod += 1
        else:
            expand_mod -= 1
        print(expand_mod)
    return pnts


def rand_build_pit(start):
    rand_mod = 1
    lump_max = 125000
    pit = set()
    buffer = [start]
    buffer_b = []
    while buffer:
        curr = buffer.pop(0)
        if curr not in pit and randint(0, rand_mod) <= 5000 + (rand_mod * 0.5):
            pit.add(curr)
            buffer.append(generate_adj(curr[0], curr[1], curr[2]))
            buffer.append(generate_adj(curr[1], curr[2], curr[0]))
            buffer.append(generate_adj(curr[2], curr[0], curr[1]))
            rand_mod += 1
        else:
            buffer_b.append(generate_adj(curr[0], curr[1], curr[2]))
            buffer_b.append(generate_adj(curr[1], curr[2], curr[0]))
            buffer_b.append(generate_adj(curr[2], curr[0], curr[1]))
    while buffer_b and lump_max:
        curr = buffer_b.pop(0)
        if curr not in pit:
            pit.add(curr)
            buffer_b.append(generate_adj(curr[0], curr[1], curr[2]))
            buffer_b.append(generate_adj(curr[1], curr[2], curr[0]))
            buffer_b.append(generate_adj(curr[2], curr[0], curr[1]))
            lump_max -= 1
    return pit


def add_adj(pit, curr):
    if curr not in pit and randint(0, 1) != 0:
        pit.add(curr)
        add_adj(pit, generate_adj(curr[0], curr[1], curr[2]))
        add_adj(pit, generate_adj(curr[1], curr[2], curr[0]))
        add_adj(pit, generate_adj(curr[2], curr[0], curr[1]))


def generate_adj(a, b, c):
    return a, b, (b[0] + a[0] - c[0], b[1] + a[1] - c[1])


if __name__ == "__main__":
    pygame.init()

    colors = {"BLACK": [0, 0, 0],
              "WHITE": [255, 255, 255],
              "GREEN1": [128, 229, 130],
              "GREEN2": [144, 208, 145],
              "GREEN3": [141, 196, 141],
              }

    # pit = rand_build_pit(((960, 540), (960, 542), (963, 541)))
    pit = circle_build_pit((960, 540))

    size = width, height = 1920, 1080
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    pygame.time.set_timer(USEREVENT+1, 333)

    while True:
        for event in pygame.event.get():
            if event.type == USEREVENT + 1:
                pass  # Timer event goes here
            if event.type  == pygame.KEYDOWN:
                pass  # Key press goes here
            if event.type == pygame.QUIT or pygame.key.get_pressed()[K_BACKSPACE]:
                sys.exit()
        screen.fill(colors["GREEN1"])
        # for tri in pit:
        #     pygame.draw.polygon(screen, colors["GREEN2"], tri, 0)
        pygame.draw.polygon(screen, colors["GREEN2"], pit, 0)
        pygame.display.flip()