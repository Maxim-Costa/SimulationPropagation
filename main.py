import pygame
import os
import rules
from random import *
from pygame.locals import *


pygame.init()
pygame.key.set_repeat(1, 60)
try:
    pygame.ftfont.init()
except:
    pygame.font.init()

pygame.OPENGL
pygame.DOUBLEBUF
pygame.HWSURFACE
os.environ['SDL_VIDEO_CENTERED'] = '1'


def afficherPygameMulti(maps, cell, fenetre=None):
    White = (255, 255, 255)
    Black = (0, 0, 0)

    Red = (255, 0, 0)
    Green = (0, 255, 0)
    Blue = (0, 0, 255)

    Marron = (139, 69, 19)

    # On parcourt la liste du niveau
    num_ligne = 0

    for ligne in maps:
        # On parcourt les listes de lignes
        num_case = 0
        for sprite in ligne:
            # On calcule la position réelle en pixels
            x = num_case * cell
            y = num_ligne * cell

            if sprite == 20:
                pygame.draw.rect(
                    fenetre, Blue, (x, y, cell, cell))
            elif sprite == 26:
                pygame.draw.rect(
                    fenetre, White, (x, y, cell, cell))
            elif sprite == 10:  # person who as in life
                pygame.draw.rect(
                    fenetre, Green, (x, y, cell, cell))
            elif sprite >= 100 and sprite < 200:
                pygame.draw.rect(
                    fenetre, Red, (x, y, cell, cell))
            elif sprite == 0:  # d = Départ
                pygame.draw.rect(
                    fenetre, Black, (x, y, cell, cell))

            num_case += 1
        num_ligne += 1
    pygame.display.update()


def UpdateMaps(maps, Infected):

    for y, x in Infected:
        case = maps[y][x]

        l = [(y+1, x), (y+1, x+1), (y+1, x-1), (y-1, x),
             (y-1, x+1), (y-1, x-1), (y, x+1), (y, x-1), ]

        for Ny, Nx in l:
            Ncase = maps[Ny][Nx]
            if Ncase == 10:
                choix = choice([10]*(100-rules.Infect)+[100]*rules.Infect)
                if choix == 100:
                    maps[Ny][Nx] = 100
                    Infected.append((Ny, Nx))

        if case >= 100+rules.Incubation:
            maps[y][x] = choice([20]*(100-rules.Death)+[0]*rules.Death)
            Infected.remove((y, x))
        else:
            maps[y][x] += 1


def MapsCreate(w, h, StartPopulation):
    maps = [[choice(StartPopulation) for _ in range(w)]
            for _ in range(h)]
    maps = [[26]+maps[i]+[26] for i in range(len(maps))]
    maps = [[26]*len(maps[0])] + maps + [[26]*len(maps[0])]
    return maps


def Start():
    cell = 5
    h, w = 200, 200
    fenetre = pygame.display.set_mode((w*cell+2*cell, h*cell+2*cell))
    StartPopulation = [10]
    maps = MapsCreate(w, h, StartPopulation)
    Infected = []
    y = randint(1, len(maps)-1)
    x = randint(1, len(maps[0])-1)
    maps[y][x] = 100
    Infected.append((y, x))

    continuer = True
    while continuer:
        pygame.time.Clock().tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                continuer = False
                quit()
        UpdateMaps(maps, Infected)
        afficherPygameMulti(maps, cell, fenetre)
        pygame.display.update()


Start()
