from tkinter import *
import numpy as np
import create_adj_m
import run_simulation

FILENAME_TAIL = '10x10_maze3'

class Cell:
    FILLED_COLOR_BG = "white" # locations that can go to
    EMPTY_COLOR_BG = "black" # walls
    FILLED_COLOR_BORDER = "black"
    EMPTY_COLOR_BORDER = "black"
    START_COLOR_BG = "green"
    END_COLOR_BG = "red"

    def __init__(self, master, x, y, size, start, end):
        """ Constructor of the object called by Cell(...) """
        self.master = master
        self.abs = x
        self.ord = y
        self.size = size
        self.fill = True
        self.start=start
        self.end=end

    def switch(self):
        """ Switch if the cell is filled or not. """
        self.fill = not self.fill

    def draw(self):
        """ order to the cell to draw its representation on the canvas """
        if self.master is not None:
            fill = Cell.FILLED_COLOR_BG
            outline = Cell.FILLED_COLOR_BORDER
            if not self.fill:
                fill = Cell.EMPTY_COLOR_BG
                outline = Cell.EMPTY_COLOR_BORDER
            if self.abs == self.start[0] and self.ord == self.start[1]:
                fill = Cell.START_COLOR_BG
                outline = Cell.FILLED_COLOR_BORDER
                self.fill = True
            elif self.abs == self.end[0] and self.ord == self.end[1]:
                fill = Cell.END_COLOR_BG
                outline = Cell.FILLED_COLOR_BORDER
                self.fill = True

            xmin = self.abs * self.size
            xmax = xmin + self.size
            ymin = self.ord * self.size
            ymax = ymin + self.size

            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill=fill,
                                         outline=outline)

        # print("xmin: " + str(xmin) + " ymin: " + str(ymin) + " xmax: " + str(xmax) + " ymax: " + str(ymax))


class CellGrid(Canvas):
    def __init__(self, master, rowNumber, columnNumber, cellSize, *args,
                 **kwargs):
        Canvas.__init__(self, master, width=cellSize * columnNumber,
                        height=cellSize * rowNumber, *args, **kwargs)

        self.cellSize = cellSize

        self.start = (0,0)
        self.end = (rowNumber - 1, columnNumber - 1)

        self.grid = []
        for row in range(rowNumber):
            line = []
            for column in range(columnNumber):
                line.append(Cell(self, column, row, cellSize, self.start, self.end))

            self.grid.append(line)

        # memorize the cells that have been modified to avoid many switching of state during mouse motion.
        self.switched = []

        # bind click action
        self.bind("<Button-1>", self.handleMouseClick)
        # bind moving while clicking
        self.bind("<B1-Motion>", self.handleMouseMotion)
        # bind release button action - clear the memory of midified cells.
        self.bind("<ButtonRelease-1>", lambda event: self.switched.clear())

        self.draw()

    def draw(self):
        for row in self.grid:
            for cell in row:
                cell.draw()

    def _eventCoords(self, event):
        row = int(event.y / self.cellSize)
        column = int(event.x / self.cellSize)
        return row, column

    def handleMouseClick(self, event):
        row, column = self._eventCoords(event)
        cell = self.grid[row][column]
        cell.switch()
        cell.draw()
        # add the cell to the list of cell switched during the click
        self.switched.append(cell)

    def handleMouseMotion(self, event):
        row, column = self._eventCoords(event)
        cell = self.grid[row][column]

        if cell not in self.switched:
            cell.switch()
            cell.draw()
            self.switched.append(cell)



app = Tk()

nx = 10
ny = 10
cell_size = 50

grid = CellGrid(app, nx, ny, cell_size)
grid.pack()

app.mainloop()

locations = []
for i in range(len(grid.grid)):
    for j in range(len(grid.grid[i])):
        if grid.grid[i][j].fill:
            locations.append([i, j])

locations = np.array(locations)
adjacency_mat = create_adj_m.create_adjacency_mat(locations)

np.save('data/location'  + FILENAME_TAIL + '.npy', locations)
np.save('data/adjacency_mat' + FILENAME_TAIL + '.npy', adjacency_mat)

# run_simulation.run_simulation(FILENAME_TAIL, plot=False)