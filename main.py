import pygame
import matplotlib.pyplot as plt
from config import dc
import th

def analisis1(surface, array, name):
    print ("iniciando analisis del proceso 1")
    axis = []
    points = []
    for x in range(150,185,1):
        surf = pygame.image.load(name)
        s_array = pygame.PixelArray(surf)
        ar = []
        for y in range(surf.get_size()[0]):
            ar.append(list(s_array[y]))
        print("HOLA")
        th.threshold(str(ar), surf.get_size()[0], surf.get_size()[1] , dc["th"], dc["margin"])
        print("CHAU")
        black = x
        #black = proceso1(s_array,surface.get_size()[0],surface.get_size()[1] , dc)
        axis.append(x)
        points.append(black)
        #pygame.image.save(surface,"data/output"+str(x)+".jpg")

    plt.plot(axis , points)
    #plt.show()



def main():
    img_name = "input.jpg"
    img = pygame.image.load(img_name)
    img_array = pygame.PixelArray(img)
    analisis1(img, img_array, img_name)


if __name__ == "__main__":
    main()