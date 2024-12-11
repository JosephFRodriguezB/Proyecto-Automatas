# Configurar screen
Map_Width = 810
Map_Height = 600

# Definir tamaño de celdas
CellSize = 15

# Altura y anchura de las celdas
Width = (int) (Map_Width/CellSize)
Height = (int) (Map_Height/CellSize)

# Estados validos para cada celda
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

# Ajusta la velocidad del flujo (0.0 - 1.0)
FlowSpeed = 1