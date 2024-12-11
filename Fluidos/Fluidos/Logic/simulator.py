from cells import *
from values import *

class Liquid:

    def __init__(self):
        # Valores máximos y minimos para las cells
        self.MaxValue = MaxValue
        self.MinValue = MinValue

        # Extra liquid a cell can store than the cell above it
        self.MaxCompression = MaxCompression

        # Lowest and highest amount of liquids allowed to flow per iteration
        self.MinFlow = MinFlow
        self.MaxFlow = MaxFlow

        # Adjusts flow speed (0.0f - 1.0f)
        self.FlowSpeed = FlowSpeed

    def Initialize(self, cells):
        # Keep track of modifications to cell liquid values
        self.Diffs = [[0 for y in range(0,Width)] for x in range(0,Height)]

    # Calculate how much liquid should flow to destination with pressure
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

    # Run one simulation step
    def Simulate(self,cells):

        global flow
        flow = 0

        # Reset the diffs array
        for x in range(0,Height):
            for y in range(0,Width):
                self.Diffs [x][y] = 0

        # Main loop
        for x in range(Height):
            for y in range(Width):
                # Get reference to Cell and reset flow
                cell = cells [x][y]
                cell.ResetFlowDirections()

                # Validate cell
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

                # Keep track of how much liquid this cell started off with
                startValue = cell.Liquid
                remainingValue = cell.Liquid
                flow = 0

                # Flow to bottom cell
                if cell.Bottom != None and cell.Bottom.Type == Blank:

                    # Determine rate of flow
                    flow = self.CalculateVerticalFlowValue(cell.Liquid, cell.Bottom) - cell.Bottom.Liquid
                    if cell.Bottom.Liquid > 0 and flow > self.MinFlow:
                        flow *= self.FlowSpeed 

                    # Constrain flow
                    flow = max (flow, 0)
                    if (flow > min(self.MaxFlow, cell.Liquid)):
                        flow = min(self.MaxFlow, cell.Liquid)

                    # Update temp values
                    if (flow != 0):
                        remainingValue -= flow
                        self.Diffs [x][y] -= flow
                        self.Diffs [x+1][y] += flow
                        cell.FlowDirections[Bottom] = True
                        cell.Bottom.Settled = False


                # Check to ensure we still have liquid in this cell
                if (remainingValue < self.MinValue):
                    self.Diffs [x][y] -= remainingValue
                    continue

                # Flow to left cell
                if cell.Left != None and cell.Left.Type == Blank:

                    # Calculate flow rate
                    flow = (remainingValue - cell.Left.Liquid) / 4
                    if (flow > self.MinFlow):
                        flow *= self.FlowSpeed

                    # constrain flow
                    flow = max (flow, 0)
                    if (flow > min(self.MaxFlow, remainingValue)):
                        flow = min(self.MaxFlow, remainingValue)

                    # Adjust temp values
                    if (flow != 0):
                        remainingValue -= flow
                        self.Diffs [x][y] -= flow
                        self.Diffs [x][y-1] += flow
                        cell.FlowDirections[Left] = True
                        cell.Left.Settled = False

                # Check to ensure we still have liquid in this cell
                if (remainingValue < self.MinValue):
                    self.Diffs [x][y] -= remainingValue
                    continue
                
                # Flow to right cell
                if cell.Right != None and cell.Right.Type == Blank:

                    # calc flow rate
                    flow = (remainingValue - cell.Right.Liquid) / 3										
                    if (flow > self.MinFlow):
                        flow *= self.FlowSpeed 

                    # constrain flow
                    flow = max (flow, 0)
                    if (flow > min(self.MaxFlow, remainingValue)):
                        flow = min(self.MaxFlow, remainingValue)
                    
                    # Adjust temp values
                    if (flow != 0):
                        remainingValue -= flow
                        self.Diffs [x][y] -= flow
                        self.Diffs [x][y + 1] += flow
                        cell.FlowDirections[Right] = True
                        cell.Right.Settled = False

                # Check to ensure we still have liquid in this cell
                if (remainingValue < self.MinValue):
                    self.Diffs [x][y] -= remainingValue
                    continue
                
                # Flow to Top cell
                if (cell.Top != None and cell.Top.Type == Blank):

                    flow = remainingValue - self.CalculateVerticalFlowValue (remainingValue, cell.Top) 
                    if (flow > self.MinFlow):
                        flow *= self.FlowSpeed

                    # constrain flow
                    flow = max (flow, 0)
                    if (flow > min(self.MaxFlow, remainingValue)):
                        flow = min(self.MaxFlow, remainingValue)

                   # Adjust values
                    if (flow != 0):
                        remainingValue -= flow
                        self.Diffs [x][y] -= flow
                        self.Diffs [x - 1][y] += flow
                        cell.FlowDirections[Top] = True
                        cell.Top.Settled = False

                # Check to ensure we still have liquid in this cell
                if (remainingValue < self.MinValue):
                    self.Diffs [x][y] -= remainingValue
                    continue

                # Check if cell is settled
                if (startValue == remainingValue):
                    cell.SettleCount += 1
                    if (cell.SettleCount >= 10):
                        cell.ResetFlowDirections ()
                        cell.Settled = False
                else :
                    cell.UnsettleNeighbors ()

            
        # Update Cell values
        for x in range(Height):
            for y in range(Width):
                cells[x][y].Liquid += self.Diffs [x][y]
                if (cells[x][y].Liquid < self.MinValue):
                    cells[x][y].Liquid = 0
                    # default empty cell to unsettled
                    cells[x][y].Settled = False
                cells[x][y].Update()

