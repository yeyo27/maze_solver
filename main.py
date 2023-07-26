from tkinter import Tk, BOTH, Canvas


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
        self.canvas = Canvas(master=self.__root, width=width, height=height)
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
    def __init__(self, x1: int, y1: int, x2: int, y2: int, win: Window):
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
        self._win = win

    def draw(self):
        if self.has_top_wall:
            self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x2, self._y1)), "black")
        if self.has_left_wall:
            self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x1, self._y2)), "black")
        if self.has_right_wall:
            self._win.draw_line(Line(Point(self._x2, self._y1), Point(self._x2, self._y2)), "black")
        if self.has_bottom_wall:
            self._win.draw_line(Line(Point(self._x1, self._y2), Point(self._x2, self._y2)), "black")


def main():
    win = Window(800, 600)
    p1 = Point(20, 20)
    p2 = Point(40, 40)
    p3 = Point(60, 60)
    p4 = Point(80, 80)
    cell1 = Cell(p1.x, p1.y, p2.x, p2.y, win)
    cell2 = Cell(p3.x, p3.y, p4.x, p4.y, win)
    cell1.draw()
    cell2.draw()
    win.wait_for_close()


if __name__ == "__main__":
    main()
