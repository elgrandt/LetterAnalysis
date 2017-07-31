import pygame
import matplotlib.pyplot as plt
from config import dc
import th

def analisis1(surface, threshold):
    print ("iniciando analisis del proceso 1")
    array = pygame.PixelArray(surface)

    ar = []
    for y in range(surface.get_size()[0]):
        ar.append(list(array[y]))

    ret = th.threshold(ar, len(ar), surface.get_size()[0], surface.get_size()[1] , threshold, dc["margin"])

    for y in range(surface.get_size()[0]):
        array[y] = ret[y]

def main():
    img_name = "input.jpg"
    img = pygame.image.load(img_name)
    screen = pygame.display.set_mode(img.get_size())
    pygame.display.set_caption("ProyectoX")
    screen.blit(img, (0,0))
    pygame.display.flip()
    analisis1(screen, dc["th"])
    while True:

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

if __name__ == "__main__":
    main()