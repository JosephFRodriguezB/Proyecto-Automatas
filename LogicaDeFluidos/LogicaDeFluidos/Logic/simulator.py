from cells import *
from values import *

class Liquid:

    def __init__(self):
        return

    def Initialize(self, cells):
        # Mantiene una guía de las diferencias entre los líquidos
        self.Diffs = [[0 for y in range(Width)] for x in range(Height)]

    # Calcula cuánto líquido debe fluir con la presión
    def CalculateVerticalFlowValue(self, remainingLiquid, destination, type="water"):
        sum = remainingLiquid + destination.Liquid
        value = 0

        if sum <= MaxValue:
            value = MaxValue
        elif sum < 2 * MaxValue + MaxCompression:
            value = (MaxValue * MaxValue + sum * MaxCompression) / (MaxValue + MaxCompression)
        else:
            value = (sum + MaxCompression) / 2

        return value

    def Simulate(self, cells):
        self.Simulate_Liquid(cells, "Water")
        self.Simulate_Liquid(cells, "Oil")

    def Simulate_Liquid(self, cells, liquidType):
        global flow
        flow = 0

        # Reinicia las diferencias
        for x in range(Height):
            for y in range(Width):
                self.Diffs[x][y] = 0

        # Ciclo principal
        for x in range(Height):
            for y in range(Width):
                # Obtiene referencia de la celda y reinicia las direcciones de flujo
                cell = cells[x][y]
                cell.ResetFlowDirections()

                # Valida la celda
                if cell.Type == Solid:
                    cell.Water = 0
                    cell.Oil = 0
                    cell.Liquid = 0
                    continue

                if cell.Liquid == 0:
                    continue

                if cell.Settled:
                    continue

                if cell.Liquid < MinValue:
                    cell.Water = 0
                    cell.Oil = 0
                    cell.Liquid = 0
                    continue

                # Define el líquido actual (Water o Oil)
                currentLiquid = getattr(cell, liquidType)

                if currentLiquid <= MinValue:
                    setattr(cell, liquidType, 0)
                    continue

                # Mantiene un índice de cuánto líquido hay y cuánto queda
                startValue = currentLiquid
                remainingValue = currentLiquid

                # Fluye a la casilla del fondo
                if cell.Bottom and cell.Bottom.Type == Blank:
                    bottomLiquidType = "Oil" if liquidType == "Water" else "Water"
                    bottomLiquid = getattr(cell.Bottom, bottomLiquidType)

                    # Permitir flujo de agua hacia abajo si hay aceite en la casilla inferior
                    if liquidType == "Water" and bottomLiquid > MinValue:
                        flow = self.CalculateVerticalFlowValue(currentLiquid, cell.Bottom) - getattr(cell.Bottom, liquidType)
                    else:
                        flow = self.CalculateVerticalFlowValue(currentLiquid, cell.Bottom) - getattr(cell.Bottom, liquidType)

                    if getattr(cell.Bottom, liquidType) > 0 and flow > MinFlow:
                        flow *= FlowSpeed

                    flow = max(flow, 0)
                    if flow > min(MaxFlow, currentLiquid):
                        flow = min(MaxFlow, currentLiquid)

                    if flow != 0:
                        remainingValue -= flow
                        self.Diffs[x][y] -= flow
                        self.Diffs[x + 1][y] += flow
                        cell.FlowDirections[Bottom] = True
                        cell.Bottom.Settled = False

                if remainingValue < MinValue:
                    self.Diffs[x][y] -= remainingValue
                    continue

                # Fluye a la izquierda
                if cell.Left and cell.Left.Type == Blank:
                    flow = (remainingValue - getattr(cell.Left, liquidType)) / 4
                    if flow > MinFlow:
                        flow *= FlowSpeed

                    flow = max(flow, 0)
                    if flow > min(MaxFlow, remainingValue):
                        flow = min(MaxFlow, remainingValue)

                    if flow != 0:
                        remainingValue -= flow
                        self.Diffs[x][y] -= flow
                        self.Diffs[x][y - 1] += flow
                        cell.FlowDirections[Left] = True
                        cell.Left.Settled = False

                if remainingValue < MinValue:
                    self.Diffs[x][y] -= remainingValue
                    continue

                # Fluye a la derecha
                if cell.Right and cell.Right.Type == Blank:
                    flow = (remainingValue - getattr(cell.Right, liquidType)) / 3
                    if flow > MinFlow:
                        flow *= FlowSpeed

                    flow = max(flow, 0)
                    if flow > min(MaxFlow, remainingValue):
                        flow = min(MaxFlow, remainingValue)

                    if flow != 0:
                        remainingValue -= flow
                        self.Diffs[x][y] -= flow
                        self.Diffs[x][y + 1] += flow
                        cell.FlowDirections[Right] = True
                        cell.Right.Settled = False

                if remainingValue < MinValue:
                    self.Diffs[x][y] -= remainingValue
                    continue

                # Fluye a la celda de arriba
                if cell.Top and cell.Top.Type == Blank:
                    topLiquidType = "Water" if liquidType == "Oil" else "Oil"
                    topLiquid = getattr(cell.Top, topLiquidType)

                    # Permitir flujo de aceite hacia arriba si hay agua en la celda superior
                    if liquidType == "Oil" and topLiquid > MinValue:
                        flow = self.CalculateVerticalFlowValue(remainingValue, cell.Top) - getattr(cell.Top, liquidType)
                    else:
                        flow = remainingValue - self.CalculateVerticalFlowValue(remainingValue, cell.Top)

                    if flow > MinFlow:
                        flow *= FlowSpeed

                    flow = max(flow, 0)
                    if flow > min(MaxFlow, remainingValue):
                        flow = min(MaxFlow, remainingValue)

                    if flow != 0:
                        remainingValue -= flow
                        self.Diffs[x][y] -= flow
                        self.Diffs[x - 1][y] += flow
                        cell.FlowDirections[Top] = True
                        cell.Top.Settled = False

                if remainingValue < MinValue:
                    self.Diffs[x][y] -= remainingValue
                    continue

                # Evita la mezcla uniforme de líquidos
                if liquidType == "Water":
                    cell.Oil = 0
                elif liquidType == "Oil":
                    cell.Water = 0

                # Revisa si la celda está asentada
                if startValue == remainingValue:
                    cell.SettleCount += 1
                    if cell.SettleCount >= 10:
                        cell.ResetFlowDirections()
                        cell.Settled = True
                else:
                    cell.UnsettleNeighbors()

        # Actualiza los valores de la celda
        for x in range(Height):
            for y in range(Width):
                updatedValue = self.Diffs[x][y]
                currentLiquid = getattr(cells[x][y], liquidType)
                setattr(cells[x][y], liquidType, currentLiquid + updatedValue)
                cells[x][y].Liquid += updatedValue
                if cells[x][y].Liquid < MinValue:
                    cells[x][y].Water = 0
                    cells[x][y].Oil = 0
                    cells[x][y].Liquid = 0
                    cells[x][y].Settled = False
                cells[x][y].Update()
