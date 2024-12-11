from values import *
from grid import Grid
import pygame

# Inicializar Pygame
pygame.init()

screen = pygame.display.set_mode((Map_Width, Map_Height))

# fount para el texto
fount = pygame.font.SysFont("Arial", 12)  # Usamos Arial de tamaño 12

# Configurar titulo
pygame.display.set_caption("Fluid Simulator")

# Configurar icon
icon = pygame.image.load("Sprites\\waterdrop.png")
pygame.display.set_icon(icon)

time = pygame.time.Clock()

# Booleano para detectar clics sostenidos
holding_click = False

# Type inicial que se cambio
Last_Type = 0

checked = [[False for n in range(0,Width)] for m in range(0,Height)]

grid = Grid()
grid.CreateGrid

def draw_grid():
    screen.fill(Black)
    cells = grid.Cells

    for y in range(Width):  # Cambiamos x -> y para recorrer columnas primero
        for x in range(Height):  # Cambiamos y -> x para recorrer filas
            cell = cells[x][y]

            # Dibujar Type de la cell
            bgcolor = cell.BackgroundColor
            pygame.draw.rect(
                screen, bgcolor,
                (y * CellSize, x * CellSize, CellSize, CellSize),  # Intercambiamos x y y
            )

            scale = cell.scale
            extra = 0 if scale[1]==1 else 1.09-scale[1]
            
            pygame.draw.rect(
                screen, Cyan,
                (y * CellSize, (x+extra)*CellSize, scale[0]*CellSize, scale[1]*CellSize),  # Intercambiamos ejes
            )

            # Si quisieras renderizar texto, ajusta también las coordenadas:
            # texto = fount.render(str(cells[x][y].Liquid), True, Black)
            # screen.blit(texto, (5 + y * CellSize, x * CellSize))
    
ejecutando = True
while ejecutando:

    cells = grid.Cells
    # Obtener posición del mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()
    botones_mouse = pygame.mouse.get_pressed()
    
    # Calcular la cell donde está el mouse
    cell_x = (mouse_x // CellSize)
    cell_y = (mouse_y // CellSize)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        
        # Detectar clic breve (presionar y soltar)
        if evento.type == pygame.MOUSEBUTTONDOWN:
            Last_Type = cells[cell_y][cell_x].Type
            holding_click = True  # Marcar que el mouse está presionado

        if evento.type == pygame.MOUSEBUTTONUP:
            checked = [[False for n in range(0,Width)] for m in range(0,Height)]
            holding_click = False  # Desmarcar clic sostenido
        
        # Detectar si se presionó la tecla "R" para reiniciar
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_r:  # Tecla "R"
                grid.CreateGrid()

    # Mover el agua en cada ciclo
    grid.Update()

    # Cambiar el Type de la cell mientras el botón está presionado
    if holding_click:  # Si el clic está sostenido
        if botones_mouse[0]:
            if 0 < cell_x < Width-1 and 0 < cell_y < Height-1:  # Verificación correcta
                if not checked[cell_y][cell_x]:
                    if Last_Type == Solid:
                            cells[cell_y][cell_x].SetType(Blank)
                            cells[cell_y][cell_x].Liquid = 0
                    else:
                        cells[cell_y][cell_x].SetType(Solid)
                    checked[cell_y][cell_x] = True
        elif botones_mouse[2]:
            if 0 < cell_x < Width-1 and 0 < cell_y < Height-1:  # Verificación correcta
                cells[cell_y][cell_x].AddLiquid(10)

    draw_grid()

    pygame.display.flip()

    # Controla los fps
    time.tick(600)

# Salir de Pygame
pygame.quit()
