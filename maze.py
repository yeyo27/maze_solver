import random
from tkinter import Tk, Canvas

from time import sleep


class Point:
    def __init__(self, x: int, y: int):
        self.x, self.y = x, y


class Line:
    def __init__(self, p1: Point, p2: Point):
        self.p1, self.p2 = p1, p2

    def draw(self, canvas: Canvas, fill_color: str):
        canvas.create_line(
            self.p1.x, self.p1.y,
            self.p2.x, self.p2.y,
            fill=fill_color, width=2
        )
        canvas.pack()


class Window:
    def __init__(self, width: int, height: int):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.canvas = Canvas(master=self.__root, width=width, height=height, background="white")
        self.canvas.pack()
        self.window_is_running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.window_is_running = True
        while self.window_is_running:
            self.redraw()

    def close(self):
        self.window_is_running = False

    def draw_line(self, line: Line, fill_color: str):
        line.draw(self.canvas, fill_color)


class Cell:
    def __init__(self, x1: int, y1: int, x2: int, y2: int, win: Window = None):
        # Top left corner of cell
        self._x1 = x1
        self._y1 = y1
        # Bottom right corner of cell
        self._x2 = x2
        self._y2 = y2
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
        self._win = win

    def draw(self):
        if self.has_top_wall:
            self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x2, self._y1)), "black")
        else:
            self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x2, self._y1)), "white")

        if self.has_left_wall:
            self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x1, self._y2)), "black")
        else:
            self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x1, self._y2)), "white")

        if self.has_right_wall:
            self._win.draw_line(Line(Point(self._x2, self._y1), Point(self._x2, self._y2)), "black")
        else:
            self._win.draw_line(Line(Point(self._x2, self._y1), Point(self._x2, self._y2)), "white")

        if self.has_bottom_wall:
            self._win.draw_line(Line(Point(self._x1, self._y2), Point(self._x2, self._y2)), "black")
        else:
            self._win.draw_line(Line(Point(self._x1, self._y2), Point(self._x2, self._y2)), "white")

    def draw_move(self, to_cell: "Cell", undo: bool = False):
        initial_cell_center = Point((self._x1 + self._x2) // 2, (self._y1 + self._y2) // 2)
        to_cell_center = Point((to_cell._x1 + to_cell._x2) // 2, (to_cell._y1 + to_cell._y2) // 2)
        if not undo:
            self._win.draw_line(Line(initial_cell_center, to_cell_center), "red")
        else:
            self._win.draw_line(Line(initial_cell_center, to_cell_center), "black")


class Maze:
    def __init__(self, x1: int, y1: int,
                 num_rows: int, num_cols: int,
                 cell_size_x: int, cell_size_y: int,
                 win: Window = None,
                 seed: int = None
                 ):
        if seed is not None:
            random.seed(seed)

        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        self._cells = []
        for i in range(self._num_cols):
            new_row = []
            for j in range(self._num_rows):
                new_cell = Cell(
                    self._x1 + i * self._cell_size_x,
                    self._y1 + j * self._cell_size_y,
                    self._x1 + (i + 1) * self._cell_size_x,
                    self._y1 + (j + 1) * self._cell_size_y,
                    self._win
                )

                new_row.append(new_cell)

                self._draw_cell(new_cell)

            self._cells.append(new_row)

    def _draw_cell(self, cell: Cell):
        if self._win:
            cell.draw()
            self._animate()

    def _animate(self):
        if self._win:
            self._win.redraw()
            sleep(0.05)

    def _break_entrance_and_exit(self):
        entrance_cell = self._cells[0][0]
        entrance_cell.has_top_wall = False
        self._draw_cell(entrance_cell)

        exit_cell = self._cells[self._num_cols - 1][self._num_rows - 1]
        exit_cell.has_bottom_wall = False
        self._draw_cell(exit_cell)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True

        while True:
            next_to_visit = []
            if i > 0 and not self._cells[i - 1][j].visited:
                next_to_visit.append((i - 1, j, "left"))

            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                next_to_visit.append((i + 1, j, "right"))

            if j > 0 and not self._cells[i][j - 1].visited:
                next_to_visit.append((i, j - 1, "top"))

            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                next_to_visit.append((i, j + 1, "bottom"))

            if len(next_to_visit) == 0:
                self._draw_cell(self._cells[i][j])
                return

            next_cell_indexes = random.choice(next_to_visit)
            next_cell = self._cells[next_cell_indexes[0]][next_cell_indexes[1]]
            # next_cell.visited = True

            if next_cell_indexes[2] == "left":
                next_cell.has_right_wall = False
                self._cells[i][j].has_left_wall = False

            if next_cell_indexes[2] == "right":
                next_cell.has_left_wall = False
                self._cells[i][j].has_right_wall = False

            if next_cell_indexes[2] == "bottom":
                next_cell.has_top_wall = False
                self._cells[i][j].has_bottom_wall = False

            if next_cell_indexes[2] == "top":
                next_cell.has_bottom_wall = False
                self._cells[i][j].has_top_wall = False

            self._break_walls_r(next_cell_indexes[0], next_cell_indexes[1])

    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False


def main():
    win = Window(800, 600)
    num_cols = 12
    num_rows = 10
    Maze(10, 10, num_rows, num_cols, 10, 10, win)
    win.wait_for_close()


if __name__ == "__main__":
    main()
