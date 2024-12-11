
from cells import *
from simulator import Liquid

class Grid:
    def __init__(self):

        self.CellSize = CellSize
        self.PreviousCellSize = 1

        self.LineWidth = 0
        self.PreviousLineWidth = 0

        self.LineColor = Black
        self.PreviousLineColor = Black

        self.RenderDownFlowingLiquid = True

        self.RenderFloatingLiquid = False

        self.Cells = [[0 for y in range(0,Width)] for x in range(0,Height)]

        self.CreateGrid()

        self.LiquidSimulator = Liquid()
        self.LiquidSimulator.Initialize(self.Cells)
        

    def CreateGrid(self):
        # cells
        for x in range(Height):
            for y in range(Width):
                cell = Cell()
                cell.Set(x, y, self.CellSize, self.RenderDownFlowingLiquid, self.RenderFloatingLiquid)

                # Agregar borde
                if (x == 0 or y == 0 or x == Height - 1 or y == Width - 1):
                    cell.SetType (Solid)

                self.Cells[x][y] = cell
        self.UpdateNeighbors ()
      
    def UpdateNeighbors(self):
        for x in range(0,Height):
            for y in range(0,Width):
                if (x > 0):
                    self.Cells[x][y].Top = self.Cells [x - 1][y]
                if (x < Height-1):
                    self.Cells[x][y].Bottom = self.Cells [x + 1][y]
                if (y > 0):
                    self.Cells[x][y].Left = self.Cells [x][y - 1]
                if (y < Width-1):
                    self.Cells[x][y].Right = self.Cells [x][y + 1]

    def Update (self):
        # Run our liquid simulation 
        self.LiquidSimulator.Simulate(self.Cells)
