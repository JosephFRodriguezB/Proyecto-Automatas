from cells import *
from values import *

class Liquid:

    def __init__(self):
        return

    def Initialize(self, cells):
        # Malla temporal para realizar cambios
        self.Diffs = [[0 for y in range(0,Width)] for x in range(0,Height)]

    # Calcula cuanto liquido debe fluir verticalmente
    def CalculateVerticalFlowValue(self,remainingLiquid,destination):
        sum = remainingLiquid + destination.Liquid
        value = 0

        if (sum <= self.MaxValue):
            value = self.MaxValue
        elif (sum < 2 * self.MaxValue + self.MaxCompression):
            value = (self.MaxValue * self.MaxValue + sum * self.MaxCompression) / (self.MaxValue + self.MaxCompression)
        else:
            value = (sum + self.MaxCompression) / 2

        return value

    # Realiza una iteración en la simulación
    def Simulate(self,cells):

        global flow
        flow = 0

        # Reinicia la malla temporal
        for x in range(0,Height):
            for y in range(0,Width):
                self.Diffs [x][y] = 0

        # Ciclo principal
        for x in range(Height):
            for y in range(Width):
                # Obtiene la referencia de la celda y reinicia su flujo
                cell = cells [x][y]
                cell.ResetFlowDirections()

                # Valida la celda
                if (cell.Type == Solid):
                    cell.Liquid = 0
                    continue

                if (cell.Liquid == 0):
                    continue

                if (cell.Settled):
                    continue
                if (cell.Liquid < self.MinValue):
                    cell.Liquid = 0
                    continue

                # Sigue el valor inicial y el actual de liquido
                startValue = cell.Liquid
                remainingValue = cell.Liquid
                flow = 0

                # Flujo hacia abajo
                if cell.Bottom != None and cell.Bottom.Type == Blank:

                    # Calcula el flujo
                    flow = self.CalculateVerticalFlowValue(cell.Liquid, cell.Bottom) - cell.Bottom.Liquid
                    if cell.Bottom.Liquid > 0 and flow > self.MinFlow:
                        flow *= self.FlowSpeed 

                    # Delimita flujo
                    flow = max (flow, 0)
                    if (flow > min(self.MaxFlow, cell.Liquid)):
                        flow = min(self.MaxFlow, cell.Liquid)

                    # Actualiza malla temporal
                    if (flow != 0):
                        remainingValue -= flow
                        self.Diffs [x][y] -= flow
                        self.Diffs [x+1][y] += flow
                        cell.FlowDirections[Bottom] = True
                        cell.Bottom.Settled = False

                # Se asegura de tener liquido
                if (remainingValue < self.MinValue):
                    self.Diffs [x][y] -= remainingValue
                    continue

                # Flujo a la izquierda
                if cell.Left != None and cell.Left.Type == Blank:

                    # Calcula el flujo
                    flow = (remainingValue - cell.Left.Liquid) / 4
                    if (flow > self.MinFlow):
                        flow *= self.FlowSpeed

                    # Delimita el flujo
                    flow = max (flow, 0)
                    if (flow > min(self.MaxFlow, remainingValue)):
                        flow = min(self.MaxFlow, remainingValue)

                    # Ajusta la malla temporal
                    if (flow != 0):
                        remainingValue -= flow
                        self.Diffs [x][y] -= flow
                        self.Diffs [x][y-1] += flow
                        cell.FlowDirections[Left] = True
                        cell.Left.Settled = False

                # Se asegura de tener liquido
                if (remainingValue < self.MinValue):
                    self.Diffs [x][y] -= remainingValue
                    continue
                
                # Flujo a la derecha
                if cell.Right != None and cell.Right.Type == Blank:

                    # Calcula el flujo
                    flow = (remainingValue - cell.Right.Liquid) / 3								
                    if (flow > self.MinFlow):
                        flow *= self.FlowSpeed 

                    # Delimita el flujo
                    flow = max (flow, 0)
                    if (flow > min(self.MaxFlow, remainingValue)):
                        flow = min(self.MaxFlow, remainingValue)
                    
                    # Ajusta la diferencia
                    if (flow != 0):
                        remainingValue -= flow
                        self.Diffs [x][y] -= flow
                        self.Diffs [x][y + 1] += flow
                        cell.FlowDirections[Right] = True
                        cell.Right.Settled = False

                # Se asegura de tener liquido
                if (remainingValue < self.MinValue):
                    self.Diffs [x][y] -= remainingValue
                    continue
                
                # Flujo de la celda
                if (cell.Top != None and cell.Top.Type == Blank):

                    flow = remainingValue - self.CalculateVerticalFlowValue (remainingValue, cell.Top) 
                    if (flow > self.MinFlow):
                        flow *= self.FlowSpeed

                    # Delimita el flujo
                    flow = max (flow, 0)
                    if (flow > min(self.MaxFlow, remainingValue)):
                        flow = min(self.MaxFlow, remainingValue)

                   # Ajusta la diferencia
                    if (flow != 0):
                        remainingValue -= flow
                        self.Diffs [x][y] -= flow
                        self.Diffs [x - 1][y] += flow
                        cell.FlowDirections[Top] = True
                        cell.Top.Settled = False

                # Se asegura de tener liquido
                if (remainingValue < self.MinValue):
                    self.Diffs [x][y] -= remainingValue
                    continue

                # Revisa si esta estancada
                if (startValue == remainingValue):
                    cell.SettleCount += 1
                    if (cell.SettleCount >= 10):
                        cell.ResetFlowDirections ()
                        cell.Settled = False
                else :
                    cell.UnsettleNeighbors ()

            
        # Actualiza el valor de las celdas
        for x in range(Height):
            for y in range(Width):
                cells[x][y].Liquid += self.Diffs [x][y]
                if (cells[x][y].Liquid < self.MinValue):
                    cells[x][y].Liquid = 0
                    # Define las celdas vacias como estancadas
                    cells[x][y].Settled = False
                cells[x][y].Update()

