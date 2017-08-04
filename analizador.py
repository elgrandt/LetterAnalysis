import pygame,utils,output

surface = pygame.display.set_mode((800,600))
surface.fill((255,255,255))
global array
array = pygame.PixelArray(surface)

def estandarizar(letra, minx, miny):
    mx = letra[minx][0]
    my = letra[miny][1]
    for n in range(len(letra)):
        letra[n][0] -= mx
        letra[n][1] -= my
        array[letra[n][0]+500][letra[n][1]] = utils.rgb2num((0,0,0))

def emprolijar(letra, maxx, maxy):
    act = []
    act2 = []
    letra.sort(key = lambda point: point[1])
    for n in range(len(letra)-1):
        if letra[n+1][0] - letra[n][0] < letra[maxx][0]/10 and letra[n][1] == letra[n+1][1]:
            for x in range(letra[n][0],letra[n+1][0]+1,1):
                act.append([x,letra[n][1]])
        else:
            letra.extend(act)
            for q in act:
                array[q[0]+600][q[1]] = utils.rgb2num((255,0,0))
            act = []
    letra.sort(key = lambda point: point[0])
    for n in range(len(letra)-1):
        if letra[n+1][1] - letra[n][1] < letra[maxy][1]/10 and letra[n][0] == letra[n+1][0]:
            for y in range(letra[n][1],letra[n+1][1]+1,1):
                act2.append([letra[n][0],y])
        else:
            letra.extend(act2)
            for q in act2:
                array[q[0]+700][q[1]] = utils.rgb2num((0,0,255))
            #print(act2)
            act2 = []

def black(let,x,y):
    if utils.num2rgb(let[x][y]) == (0,0,0):
        return True
    return False

class grupo:
    def __init__(self, elementos):
        self.column = elementos[0][0]
        self.start = elementos[0][1]
        self.end = elementos[len(elementos)-1][1]
        self.connected = []

def agregar_referencias(grupos, conectados):
    gr = []
    for x in conectados:
        for y in range(len(grupos)):
            if x[0] == grupos[y].column and x[1] > grupos[y].start and x[1] < grupos[y].end:
                gr.append(grupos[y])
    for x in range(len(gr)):
        for y in range(len(gr)):
            if x != y:
                gr[x].connected.append(gr[y])
    a = 1

def generar_grafo(letra):
    maxx = 0
    maxy = 0
    for x in range(len(letra)):
        if letra[x][0] > maxx:
            maxx = letra[x][0]
        if letra[x][1] > maxy:
            maxy = letra[x][1]
    maxx += 1
    maxy += 1
    let = pygame.Surface((maxx,maxy))
    let.fill((255,255,255))
    letar = pygame.PixelArray(let)
    for x in range(len(letra)):
        letar[letra[x][0]][letra[x][1]] = utils.rgb2num((0,0,0))
    grupos = []
    for x in range(maxx):
        grupo_act = []
        for y in range(maxy):
            if black(letar,x,y):
                grupo_act.append([x,y])
                if y == maxy-1:
                    gr = grupo(grupo_act)
                    grupos.append(gr)
                    grupo_act = []
            else:
                if grupo_act != []:
                    gr = grupo(grupo_act)
                    grupos.append(gr)
                    grupo_act = []
    for y in range(maxy):
        grupo_act = []
        for x in range(maxx):
            if black(letar,x,y):
                grupo_act.append([x,y])
                if y == maxy-1:
                    agregar_referencias(grupos,grupo_act)
                    grupo_act = []
            else:
                if grupo_act != []:
                    agregar_referencias(grupos,grupo_act)
                    grupo_act = []
    a = 1

def analizar_letra(letra):
    minx,miny = 0,0
    maxx,maxy = 0,0
    for n in range(len(letra)):
        if letra[n][0] < letra[minx][0]:
            minx = n
        if letra[n][1] < letra[miny][1]:
            miny = n
        if letra[n][0] > letra[maxx][0]:
            maxx = n
        if letra[n][1] > letra[maxy][1]:
            maxy = n
    estandarizar(letra, minx, miny)
    emprolijar(letra, maxx, maxy)
    print(letra)
    generar_grafo(letra)
    for n in range(len(letra)):
        array[letra[n][0]*10][letra[n][1]*10] = utils.rgb2num((0,0,0))

if __name__ == "__main__":
    test = output.test[15]
    analizar_letra(test)
    q = False
    while not q:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                q = True
