import pygame
import matplotlib.pyplot as plt
from config import dc
import th
import utils
from analizador import analizar_letra

def analisis1(surface, threshold):
    print ("iniciando analisis 1")
    array = pygame.PixelArray(surface)

    ar = []
    for y in range(surface.get_size()[0]):
        ar.append(list(array[y]))

    ret = th.threshold(ar, len(ar), surface.get_size()[0], surface.get_size()[1] , threshold, dc["margin"])

    for y in range(surface.get_size()[0]):
        array[y] = ret[y]

def analisis2(surface):
    print ("iniciando analisis 2")
    array = pygame.PixelArray(surface)

    ar = []
    for y in range(surface.get_size()[0]):
        ar.append(list(array[y]))

    ret = th.get_letters(ar, len(ar), surface.get_size()[0], surface.get_size()[1])
    for x in range(len(ret)):
        for y in range(len(ret[x])):
            array[ret[x][y][0]][ret[x][y][1]] = utils.rgb2num((255,0,0))
    return ret

def main():
    img_name = "input6.png"
    img = pygame.image.load(img_name)
    screen = pygame.display.set_mode(img.get_size(),pygame.RESIZABLE)
    pygame.display.set_caption("ProyectoX")
    screen.fill((255,255,255))
    screen.blit(img, (0,0))
    pygame.display.flip()
    analisis1(screen, dc["th"])
    cube = pygame.Surface((5,5))
    cube.fill((255,0,0))
    screen.blit(cube,(454,381))
    pygame.display.flip()
    letras = analisis2(screen)
    pygame.display.flip()
    for l in letras:
        analizar_letra(l)
    while True:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.image.save(screen , "data/output.bmp")
                return

if __name__ == "__main__":
    main()