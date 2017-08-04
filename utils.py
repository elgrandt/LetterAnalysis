from random import randrange as RR


### pintar un pixel de un color en una imagen
def drawPixel(img, ancho , alto , x , y, color):
	for xp in range(x - 1 , x + 2):
		if xp < 0 or xp >= ancho:
			continue
		for yp in range(y - 1, y + 2):
			if yp < 0 or yp >= alto:
				continue
			img[xp , yp] = rgb2num(color)

def randcolor():
	return RR(256),RR(256),RR(256)

# funciones para trabajar de numeros de codigo de color a rgb
def num2rgb(num):
	return num & 255 , (num >> 8) & 255 , (num >> 16) & 255
def rgb2num(color):
	r,g,b = color
	return (b + (g << 8) + (r << 16))
def black(color):
	r,g,b = num2rgb(color)
	if (r == 0 and g == 0 and b == 0):
		return True
	return False
# retornar si es blanco
def white(color):
	r,g,b = num2rgb(color)
	if (r == 255 and g == 255 and b == 255):
		return True
	return False
# el valor de x maximo de la informacion, y minimo, etc
def xMax(data):
	xmax = -1
	for x in range(len(data)):
		xmax = max(xmax , data[x][0] )
	return xmax
def yMin(data):
	ymin = 10000
	for x in range(len(data)):
		ymin = min(ymin , data[x][1])

	return ymin
def yMax(data):
	ymax = 0
	for x in range(len(data)):
		ymax = max(ymax,data[x][1])
	return ymax 