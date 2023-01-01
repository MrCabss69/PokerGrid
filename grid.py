
"""
CREANDO GRID INTERACTIVO CON BACKEND USANDO PYGAME
"""


# IMPORTS
import pygame
import numpy as np
import pandas as pd
import pygame_widgets as pw
from poker import Range, Hand
from pygame.locals import *
from pygame_widgets.button import Button

# CONSTANTES
N    = 14   # tamaño fila
lado = 35   # tamaño de célula

# COLORES
BL      = (250, 250, 250)
VRD_CLR = (0, 255, 153)
VRD_OSC = (23, 63, 53)
color   = [VRD_OSC, VRD_CLR] 

# POKER CARD RANKING - DESCENDING
elems = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

# PYGAME OBJECTS:
#   Rect(left, top, width, height) -> Rect
#   line(surface, color, start_pos, end_pos) -> Rect

# inicialización y creación de la matriz NxN - cada celda contiene un rectángulo pygame
grid = [ [ pygame.Rect( j*lado, i*lado, lado, lado ) for j in range(N) ] for i in range(N) ]


# inicialización de estados iniciales:
vals = np.zeros((N,N))


# marco -> define SURFACE
def marco(ventana):
    # dibujamos la matriz
    for i in range(N):
        for j in range(N):
            pygame.draw.rect(ventana, color[int(vals[i][j])], grid[i][j])
    
    # dibujamos las líneas de la matriz
    for i in range(1, N + 1):
        pygame.draw.line(ventana, BL, [i*lado, 0], [i*lado, N*lado]) # verticales
        pygame.draw.line(ventana, BL, [0, i*lado], [N*lado, i*lado]) # horizontales

    # font and size
    add_labels(ventana)




# click -> toggle ON/OFF cell
def click(ventana):
    raton = pygame.mouse.get_pos()
    for i in range(1, N):
        for j in range(1, N):
            if grid[i][j].collidepoint(raton):
                vals[i][j] = abs(1 - vals[i][j])




# write -> label rows and columns
def write(text, x, y, color="Coral",):
    font   = pygame.font.SysFont("arial", 20)
    text   = font.render(text, 1, pygame.Color(color))
    cent   = ( x + (lado//2)  ,  y + (lado//2) )
    text_rect = text.get_rect(center=cent)
    return text, text_rect




# add_labels -> label rows and columns 
def add_labels(ventana):

    for i in range(13):

        # añadimos el texto para cada letra, desde la primera fila
        text, text_r   = write(elems[i], (i+1)*lado, 0)

        # añadimos el texto para cada letra desde la primera columna
        text1, text_r1 = write(elems[i], 0, (i+1)*lado)

        # fijamos el texto en la Surface
        ventana.blit(text, text_r)
        ventana.blit(text1, text_r1)



# pos_to_ran -> return Range object based on the GUI matrix selection
def pos_to_ran(pos):
    rango = ''
    for p in pos:
        if p[0] == p[1]:
            rango += elems[p[0]] + elems[p[1]] + ' '
        elif p[0] < p[1]:
            rango +=  elems[p[0]] + elems[p[1]] + 's' + ' '
        elif p[0] > p[1]:
            rango +=  elems[p[1]] + elems[p[0]] + 'o' + ' '
    return Range(rango)




# rango_df -> dataframe de estrategia
def rango_df(positions):

    # añadimos las posiciones toggled al rango
    rango       = pos_to_ran(positions)
    """
    print('\n', 'El rango seleccionado es: ', '\n', rango.to_ascii())
    """
    
    # convertimos el rango a una lista de manos 
    manos = list(rango.hands)

    # creamos el diccionario de estrategia: 1 o 0 a la probabilidad de ir all-in
    d = {str(h): [0.] if h not in manos else [1.] for h in list(Hand)}

    # get_input -> devuelve string de la situación actual
    def get_input():
        try:
            res = input('Selecciona posición: SB/xx o BB/xxr: \n').lower()
            if res in ['sb','bb']:
                res = 'xx' if res == 'sb' else 'xxr'
            return res
        except:
            get_input()
    
    # get situación actual por input de teclado
    situacion = get_input()
    
    # devolvemos un DataFrame
    return pd.DataFrame.from_dict(d,orient="index",columns=[situacion])




# show_results -> print toggled data in the matrix as poker range
def show_results():
    global vals
    pos = set()
    # añadimos posiciones toggled
    for i in range(N-1, 0, -1):
        for j in range(N-1, 0, -1): 
            if vals[i][j] != 0:
                pos.add((i-1,j-1))  
                
    # almacenamos en un dataframe los valores de all-in para el rango de la situación
    df_strategy = rango_df(pos) 
    print(df_strategy)
    pass

    
    


def main(): 

    # pygame inits
    pygame.init()
    pygame.font.init()

    # surface to draw on 
    ventana = pygame.display.set_mode((N*lado, N*lado+75)) # espacio extra vertical para botón
    
    # window caption
    pygame.display.set_caption("MiniFlopzilla")

    # pygame_widgets button
    button = Button(
            ventana, ((N*lado)/2)-50, (N*lado)+15, 100, 50, text='Set p1 Range',
            fontSize=20, margin=10, inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=10, onClick=lambda: show_results()
    )

    # infinite loop to check events
    while True:

        #  surface instantation
        marco(ventana)

        #  draw
        button.draw()
        
        #  print the draw on the screen
        pygame.display.update()

        for event in pygame.event.get():

            #   update button events
            pw.update(event)

            #   event: exit()
            if event.type == pygame.QUIT:
                pygame.display.update()
                pygame.quit()

            #   event: click()
            elif event.type == MOUSEBUTTONDOWN:

                #  check if click on button -- pos y >> matriz
                if pygame.mouse.get_pos()[1] > N*lado:

                    #  update event on button
                    pw.update(event)
                    
                    #  show results and set the new draw
                    marco(ventana) 

                #  click on matrix
                else:
                    #  click function
                    click(ventana)

                    #  set the new draw
                    marco(ventana) 

                #  print the new draw
                pygame.display.update()

main()