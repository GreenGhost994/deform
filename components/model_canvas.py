import math
from components.elements import Vertex, Line

def distance_from_point_to_line(px, py, x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    if dx == dy == 0:
        return math.sqrt((px - x1)**2 + (py - y1)**2)
    t = ((px - x1) * dx + (py - y1) * dy) / (dx**2 + dy**2)
    t = max(0, min(1, t))
    nearest_x, nearest_y = x1 + t * dx, y1 + t * dy
    return math.sqrt((px - nearest_x)**2 + (py - nearest_y)**2)


class CanvasFunctions:
    def __init__(self, canvas):
        self.canvas = canvas
        self.dragged_element = None
        self.drag_start_vertex_start = None
        self.drag_start_vertex_end = None
        self.dragging = False

    def on_mouse_drag(self, event):
        if self.dragged_element is not None:
            x, y = event.x, event.y
            if not self.dragging:
                distance = math.sqrt((x - self.drag_start[0])**2 + (y - self.drag_start[1])**2)
                if distance >= 20:
                    self.dragging = True
            if self.dragging:
                v_x, v_y = self.model_space_location(x, y)
                if type(self.dragged_element) == Vertex:
                    self.dragged_element.x = v_x
                    self.dragged_element.y = v_y
                    self.redraw_canvas()
                elif type(self.dragged_element) == Line:
                    dx = x - self.drag_start[0]
                    dy = y - self.drag_start[1]
                    v_dx, v_dy = dx / self.scale, dy / self.scale
                    self.dragged_element.start.x += v_dx
                    self.dragged_element.start.y -= v_dy
                    self.dragged_element.end.x += v_dx
                    self.dragged_element.end.y -= v_dy
                    self.drag_start = self.drag_start[0] + dx, self.drag_start[1] + dy
                    self.redraw_canvas()

    def redraw_canvas(self):
        self.canvas.delete("all")
        self.draw_ucs_start()
        for line in self.model.lines:
            self.draw_line(line)
        for vertex in self.model.vertices:
            self.draw_vertex(vertex)
    
    def draw_ucs_start(self):
        if self.vector_x is not None and self.vector_y is not None:
            x, y = self.vector_x + self.middle_x, self.vector_y + self.middle_y
            self.canvas.create_line(x, y, x + 30, y, fill="red")
            self.canvas.create_line(x, y, x, y - 30, fill="green")