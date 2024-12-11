from values import *

class Cell:

    # El método __init__ es llamado al crear el objeto
    def __init__(self):
        # Atributos de instancia
        self.X = 0
        self.Y = 0
        self.Size = 0
        self._Settled = False
        self.Liquid = 0
        self.SettleCount = 0
        self.Type = Blank
        self.Top = None
        self.Left = None
        self.Right = None
        self.Bottom = None
        self.Bitmask = 0
        self.FlowDirections = [False for _ in range(4)]
        self.RenderDownFlowingLiquid = False
        self.RenderFloatingLiquid = False
        self.BackgroundColor = White

    def Settled(self):
        return self._Settled
    
    def Settled(self,value):
        self._Settled = value
        if not self._Settled:
            self.SettleCount = 0

    def Set(self,x,y,CellSize, RenderDownFlowingLiquid, RenderFloatingLiquid):
        self.X = x
        self.Y = y
        self.Size = CellSize
        self.RenderDownFlowingLiquid = RenderDownFlowingLiquid
        self.RenderFloatingLiquid = RenderFloatingLiquid

    def SetType(self,Type):
        self.Type = Type
        if (Type == Solid):   
            self.Liquid = 0
        self.UnsettleNeighbors()

    # Agrega liquido a la celda
    def AddLiquid(self,amount):
        self.Liquid += amount
        self._Settled = False

    def ResetFlowDirections(self):
        self.FlowDirections[0] = False
        self.FlowDirections[1] = False
        self.FlowDirections[2] = False
        self.FlowDirections[3] = False

    # Fuerza a los vecinos a iterar
    def UnsettleNeighbors(self):
        if not (self.Top == None):
            self.Top.Settled = False
        if not (self.Bottom == None):
            self.Bottom.Settled = False
        if not (self.Left == None):
            self.Left.Settled = False
        if not (self.Right == None):
            self.Right.Settled = False

    def Update(self):
        # Cambia el color del fondo según el tipo
        if (self.Type == Solid):
            self.BackgroundColor = Black
        else:
            self.BackgroundColor = White

        # Actualiza el bitmask según el flujo de la celda
        self.Bitmask = 0
        if (self.FlowDirections[Top]):
            self.Bitmask += 1
        if (self.FlowDirections[Right]):
            self.Bitmask += 2
        if (self.FlowDirections[Bottom]):
            self.Bitmask += 4
        if (self.FlowDirections[Left]):
            self.Bitmask += 8

        # Ajusta el tamaño del Liquid según la capacidad de la celda
        self.scale = (1, min(1, self.Liquid))	

        # Alertas opcionales
        if not (self.RenderFloatingLiquid):
            # Remueve liquidos flotantes
            if not self.Bottom == None and not self.Bottom.Type == Solid and self.Bottom.Liquid < 1:
                self.scale = (0, 0)	
                self.Settled = False

        if (self.RenderDownFlowingLiquid):
            # Llena la celda si arriba hay liquido
            if (self.Type == Blank and not self.Top == None and (self.Top.Liquid > 0.05 or self.Top.Bitmask == 4)):
                self.scale = (1, 1)
