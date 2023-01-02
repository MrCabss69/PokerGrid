# REFACTOR grid.py

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


# Ventana-> Objeto printeado
class Window:

    def __init__(self) -> None:
        # pygame inits
        self.shape = (N*lado, N*lado+75) # espacio vertical extra para el botón
        self.main()
    
    # marco -> define SURFACE
    def marco(self, ventana):
        # dibujamos la matriz
        for i in range(N):
            for j in range(N):
                pygame.draw.rect(ventana, color[int(self.vals[i][j])], self.grid[i][j])
        
        # dibujamos las líneas de la matriz
        for i in range(1, N + 1):
            pygame.draw.line(ventana, BL, [i*lado, 0], [i*lado, N*lado]) # verticales
            pygame.draw.line(ventana, BL, [0, i*lado], [N*lado, i*lado]) # horizontales

        # font and size
        self.add_labels(ventana)




    # click -> toggle ON/OFF cell
    def click(self, ventana):
        raton = pygame.mouse.get_pos()
        for i in range(1, N):
            for j in range(1, N):
                if self.grid[i][j].collidepoint(raton):
                    self.vals[i][j] = abs(1 - self.vals[i][j])




    # write -> label rows and columns
    def write(self, text, x, y, color="Coral",):
        font   = pygame.font.SysFont("arial", 20)
        text   = font.render(text, 1, pygame.Color(color))
        cent   = ( x + (lado//2)  ,  y + (lado//2) )
        text_rect = text.get_rect(center=cent)
        return text, text_rect




    # add_labels -> label rows and columns 
    def add_labels(self, ventana):

        for i in range(13):

            # añadimos el texto para cada letra, desde la primera fila
            text, text_r   = self.write(elems[i], (i+1)*lado, 0)

            # añadimos el texto para cada letra desde la primera columna
            text1, text_r1 = self.write(elems[i], 0, (i+1)*lado)

            # fijamos el texto en la Surface
            ventana.blit(text, text_r)
            ventana.blit(text1, text_r1)



    # pos_to_ran -> return Range object based on the GUI matrix selection
    def pos_to_ran(self, pos):
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
    def rango_df(self, positions):

        # añadimos las posiciones toggled al rango
        rango       = self.pos_to_ran(positions)
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
    def show_results(self):
        pos = set()
        # añadimos posiciones toggled
        for i in range(N-1, 0, -1):
            for j in range(N-1, 0, -1): 
                if self.vals[i][j] != 0:
                    pos.add((i-1,j-1))  
                    
        # almacenamos en un dataframe los valores de all-in para el rango de la situación
        df_strategy = self.rango_df(pos) 
        print(df_strategy)
        pass

        
        


    def main(self): 

        # pygame inits
        pygame.init()
        pygame.font.init()
        # inicialización y creación de la matriz NxN - cada celda contiene un rectángulo pygame
        self.grid = [ [ pygame.Rect( j*lado, i*lado, lado, lado ) for j in range(N) ] for i in range(N) ]


        # inicialización de estados iniciales:
        self.vals = np.zeros((N,N))

        # surface to draw on 
        ventana = pygame.display.set_mode(self.shape) # espacio extra vertical para botón
        
        # window caption
        pygame.display.set_caption("MiniFlopzilla")

        # pygame_widgets button
        button = Button(
                ventana, ((N*lado)/2)-50, (N*lado)+15, 100, 50, text='Set p1 Range',
                fontSize=20, margin=10, inactiveColour=(255, 0, 0),
                pressedColour=(0, 255, 0), radius=10, onClick=lambda: self.show_results()
        )

        # infinite loop to check events
        while True:

            #  surface instantation
            self.marco(ventana)

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
                        self.marco(ventana) 

                    #  click on matrix
                    else:
                        #  click function
                        self.click(ventana)

                        #  set the new draw
                        self.marco(ventana) 

                    #  print the new draw
                    pygame.display.update()

w = Window()