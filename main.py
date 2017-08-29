import pygame
import matplotlib.pyplot as plt
from config import dc
import th
import utils
from analizador import analizar_letra
import string,random,time
import net_training
import numpy as np

def analisis1(surface, threshold):
    #print ("iniciando analisis 1")
    array = pygame.PixelArray(surface)

    ar = []
    for y in range(surface.get_size()[0]):
        ar.append(list(array[y]))

    ret = th.threshold(ar, len(ar), surface.get_size()[0], surface.get_size()[1] , threshold, dc["margin"])

    for y in range(surface.get_size()[0]):
        array[y] = ret[y]

def analisis2(surface):
    #print ("iniciando analisis 2")
    array = pygame.PixelArray(surface)

    ar = []
    for y in range(surface.get_size()[0]):
        ar.append(list(array[y]))

    ret = th.get_letters(ar, len(ar), surface.get_size()[0], surface.get_size()[1])
    #for x in range(len(ret)):
    #    for y in range(len(ret[x])):
    #        array[ret[x][y][0]][ret[x][y][1]] = utils.rgb2num((255,0,0))
    return ret

def ordenar_letras(letras):
    lines = []
    for x in range(len(letras)):
        mxX = max(letras[x], key = lambda a: a[0])[0]
        mxY = max(letras[x], key = lambda a: a[1])[1]
        mnX = min(letras[x], key = lambda a: a[0])[0]
        mnY = min(letras[x], key = lambda a: a[1])[1]
        chosen = False
        for y in range(len(lines)):
            line = lines[y]
            if ( mnY >= line[1][0] and mnY < line[1][1] ) or ( mxY > line[1][0] and mxY <= line[1][1] ):
                lines[y][0].append(letras[x])
                chosen = True
                break
        if not chosen:
            lines.append([[letras[x]], [mnY,mxY]])
    for x in range(len(lines)):
        lines[x][0] = sorted(lines[x][0], key = lambda a: min(a, key = lambda a: a[0]))
    lines = sorted(lines, key = lambda a: a[1][0])
    lets = []
    for x in lines:
        lets += x[0]
    return lets

def main():
    img_name = "input_test.png"
    img = pygame.image.load(img_name)
    screen = pygame.display.set_mode((2*img.get_size()[0],2*img.get_size()[1]),pygame.RESIZABLE)
    pygame.display.set_caption("ProyectoX")
    screen.fill((255,255,255))
    screen.blit(pygame.transform.smoothscale(img,(2*img.get_size()[0],2*img.get_size()[1])), (0,0))
    pygame.display.flip()
    analisis1(screen, dc["th"])
    cube = pygame.Surface((5,5))
    cube.fill((255,0,0))
    screen.blit(cube,(454,381))
    pygame.display.flip()
    letras = analisis2(screen)
    pygame.display.flip()
    """grafos = []
    for l in letras:
        grafos.append(analizar_letra(l,screen))"""
    f = open("output.py","w")
    f.write("test = "+str(letras))
    while True:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.image.save(screen , "data/output.bmp")
                return

def train():
    available_letters = string.ascii_uppercase
    end = False
    pygame.init()
    screen = pygame.display.set_mode((400,400))
    screen.fill((255,255,255))
    X = []
    Y = []
    while not end:
        font = pygame.font.Font(None,random.randrange(10,30))
        size = random.randrange(100)
        surf = pygame.Surface((400,400))
        surf.fill((255,255,255))
        lines = [""]
        i = 0
        txt = ""
        for x in range(size):
            act = random.choice(available_letters)
            txt += act
            lines[i] += act + " "
            render = font.render(lines[i]+"A",True,(0,0,0))
            if render.get_size()[0] > surf.get_size()[0]-20:
                i += 1
                lines.append("")
        y = 20
        for x in range(len(lines)):
            render = font.render(lines[x],True,(0,0,0))
            surf.blit(render,(20,y))
            y += render.get_size()[1] + 4
        analisis1(surf,dc["th"])
        letters = analisis2(surf)
        letters = ordenar_letras(letters)
        if len(letters) != size:
            print("Error, no se detectaron todas las letras")
            return
        for a in range(len(letters)):
            x = letters[a]
            screen.fill((255,255,255))
            s = pygame.Surface((max(x,key=lambda a: a[0])[0] - min(x,key=lambda a: a[0])[0] + 1, max(x,key=lambda a: a[1])[1] - min(x,key=lambda a: a[1])[1] + 1))
            s.fill((255,255,255))
            array = pygame.PixelArray(s)
            for y in x:
                array[y[0] - min(x,key=lambda a: a[0])[0]][y[1] - min(x,key=lambda a: a[1])[1]] = utils.rgb2num((0,0,0))
            new_size = [0,0]
            if s.get_size()[0] > s.get_size()[1]:
                new_size[0] = 30
                new_size[1] = (30/s.get_size()[0]) * s.get_size()[1]
            else:
                new_size[1] = 30
                new_size[0] = (30/s.get_size()[1]) * s.get_size()[0]
            del array
            s = pygame.transform.scale(s,(int(new_size[0]), int(new_size[1])))
            s2 = pygame.Surface((30,30))
            s2.fill((255,255,255))
            s2.blit(s,(0,0))
            array2 = pygame.PixelArray(s2)
            arr = []
            for n in range(len(array2)):
                arr += list(array2[n])
            del array2
            X.append(arr)
            tmp_y = [0] * (ord(max(available_letters)) - ord(min(available_letters)) + 1)
            tmp_y[ord(txt[a]) - ord(min(available_letters))] = 1
            Y.append(tmp_y)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.image.save(screen , "data/output.bmp")
                end = True
    #net_training.train_neural_net(np.array(X),np.array(Y))
    file = open("example_data.py", "w+")
    file.write("X = "+str(X)+"\n")
    file.write("Y = "+str(Y))

if __name__ == "__main__":
    train()