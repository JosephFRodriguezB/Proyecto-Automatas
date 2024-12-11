# Configurar screen
Map_Width = 810
Map_Height = 600

# Definir tamaño de cell
CellSize = 15

# height y anchura de la cells
Width = (int) (Map_Width/CellSize)
Height = (int) (Map_Height/CellSize)

# Types validos para cada cell
Blank = 0
Solid = 1
    
# Direcciones de flujo
Top = 0
Right = 1
Bottom = 2
Left = 3

from pygame import Color
# Colores básicos
Black = Color(0,0,0)
Cyan = Color(122,122,255)
Gray = Color(125,125,125)
White = Color(255,255,255)
Yellow = Color(255,150,0)

# Valores máximos y minimos para las celdas
MaxValue = 1.0
MinValue = 0.005

# Liquido extra que puede almacenar
MaxCompression = 0.25

# Minima y máxima capacidad de flujo por iteracion
MinFlow = 0.005
MaxFlow = 4

# Adjusts flow speed (0.0f - 1.0f)
FlowSpeed = 1