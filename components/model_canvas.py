import math
from components.elements import *
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from components.popups import *

def distance_from_point_to_bar(px: float, py: float, x1: float, y1: float, x2: float, y2: float) -> float:
    dx, dy = x2 - x1, y2 - y1
    if dx == dy == 0:
        return math.sqrt((px - x1)**2 + (py - y1)**2)
    t = ((px - x1) * dx + (py - y1) * dy) / (dx**2 + dy**2)
    t = max(0, min(1, t))
    nearest_x, nearest_y = x1 + t * dx, y1 + t * dy
    return math.sqrt((px - nearest_x)**2 + (py - nearest_y)**2)


class CanvasFunctions:
    def __init__(self, app, root):
        self.model = app.model
        self.app = app
        self.root = root
        self.vector_x = 0
        self.vector_y = 0
        self.middle_x = 0
        self.middle_y = 0
        self.scale = 100
        self.snap = 2
        self.display_settings = {
            "vertex_id": 1,
            "vertex_coords": 1,
            "bar_id": 1,
        }
        self.selected_items = []

        self.canvas = tb.Canvas(self.app.bottom_panel, width=800, height=600)

        self.is_creating_vertex = False
        self.is_creating_bar = False
        self.selected_vertex = None
        self.creating_bar = None

        self.dragging = False  # Flag to indicate if dragging is in progress
        self.dragged_element = None  # Index of the vertex being dragged
        self.drag_start = None  # Initial mouse position when dragging started
        self.view_drag_start = None  # Initial mouse position for scrolling


        # Configure binds
        self.canvas.bind("<Configure>", self.update_middle)
        self.canvas.bind("<Button-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)
        self.canvas.bind("<Double-Button-1>", self.on_double_edit_element)
        self.canvas.bind("<Button-2>", self.on_scroll_press)
        self.canvas.bind("<B2-Motion>", self.on_scroll_drag)
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        
        self.root.bind("<Escape>", self.clear_selected_items)
        self.root.bind("<Delete>", self.erase_selected_items)



    def on_mouse_wheel(self, event):
        """
        Ability to zoom in and zoom out the model space.
        """
        x, y = self.cursor_coordinates_in_model(*self.get_cursor_location())

        if event.delta < 0:
            self.scale /= 1.1
        else:
            self.scale *= 1.1

        x,y = self.screen_space_location(x, y)
        new_x, new_y = self.screen_space_location(*self.cursor_coordinates_in_model(*self.get_cursor_location()))
        self.vector_x += new_x - x
        self.vector_y += new_y - y
        self.redraw_canvas()


    def clear_selected_items(self, event):
        """
        - Clean list of selected items
        - Clean previous vertex while bar create
        after pressing ESC.
        """
        self.selected_items = []
        self.creating_bar = None
        self.redraw_canvas()

    def erase_selected_items(self, event):
        for item in self.selected_items:
            self.model.delete(item)
        self.selected_items = []
        self.redraw_canvas()
        self.app.treeview.update_treeview()

    def on_mouse_press(self, event):

        def create_vertex_element():
            v_x, v_y = self.model_space_location(x, y)
            vertex = Vertex(None, v_x, v_y)
            self.model.add(vertex)
            self.draw_vertex(vertex)
            return vertex
        
        def check_if_vertex_pressed():
            for vertex in self.model.vertices:
                screen_x, screen_y = self.screen_space_location(vertex.x, vertex.y)
                distance = math.sqrt((x - screen_x)**2 + (y - screen_y)**2)
                if distance <= 5:
                    self.select_element(vertex)
                    return vertex
            return False

        def check_if_bar_pressed():
            for bar in self.model.bars:
                x1, y1 = self.screen_space_location(bar.start.x, bar.start.y)
                x2, y2 = self.screen_space_location(bar.end.x, bar.end.y)
                distance_to_bar = distance_from_point_to_bar(x, y, x1, y1, x2, y2)
                if distance_to_bar <= 3:
                    self.select_element(bar)
                    return bar
        

        x, y = event.x, event.y

        if self.is_creating_vertex:
            if not check_if_vertex_pressed():
                create_vertex_element()

        elif self.is_creating_bar:
            if not self.selected_items:
                if not self.creating_bar:
                    if not (next_vertex := check_if_vertex_pressed()):
                        self.creating_bar = create_vertex_element()
                    else:
                        self.creating_bar = next_vertex
                else:
                    if not (next_vertex := check_if_vertex_pressed()):
                        next_vertex = create_vertex_element()
                    self.model.add(Bar(None, self.creating_bar, next_vertex))
                    self.creating_bar = next_vertex
            elif len(self.selected_items) == 1:
                if type(self.selected_items[0]) == Vertex:
                    if not (next_vertex := check_if_vertex_pressed()):
                        next_vertex = create_vertex_element()
                    if self.selected_items:
                        self.model.add(Bar(None, self.selected_items[0], next_vertex))
                        self.creating_bar = next_vertex
                        self.selected_items = []

            self.redraw_canvas()


        else:
            if vertex := check_if_vertex_pressed():
                self.drag_start = (x, y)
                self.dragging = False  # Don't start dragging until the mouse moves a certain distance
                self.dragged_element = vertex
            elif bar := check_if_bar_pressed():
                self.drag_start = (x, y)
                self.dragging = False  # Don't start dragging until the mouse moves a certain distance
                self.dragged_element = bar
            else:
                self.selected_items = []
                self.redraw_canvas()

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
                elif type(self.dragged_element) == Bar:
                    dx = x - self.drag_start[0]
                    dy = y - self.drag_start[1]
                    v_dx, v_dy = dx / self.scale, dy / self.scale
                    self.dragged_element.start.x += v_dx
                    self.dragged_element.start.y -= v_dy
                    self.dragged_element.end.x += v_dx
                    self.dragged_element.end.y -= v_dy
                    self.drag_start = self.drag_start[0] + dx, self.drag_start[1] + dy
                    self.redraw_canvas()

    def on_mouse_release(self, event):
        self.dragging = False
        self.dragged_element = None
        self.app.treeview.update_treeview()

    def on_scroll_press(self, event):
        self.view_drag_start = (event.x, event.y)

    def on_scroll_drag(self, event):
        """
        Function to move the model view.
        """
        x, y = event.x, event.y
        if self.view_drag_start is not None:
            delta_x = x - self.view_drag_start[0]
            delta_y = y - self.view_drag_start[1]
            if self.vector_x is not None and self.vector_y is not None:
                self.vector_x += delta_x
                self.vector_y += delta_y
                self.view_drag_start = (x, y)
                self.redraw_canvas()

    def on_double_edit_element(self, event):
        if not self.dragging:
            x, y = event.x, event.y
            for vertex in self.model.vertices:
                vertex_index, v_x, v_y = vertex.id, vertex.x, vertex.y
                screen_x, screen_y = self.screen_space_location(v_x, v_y)
                distance = math.sqrt((x - screen_x)**2 + (y - screen_y)**2)
                if distance <= 5:
                    self.selected_vertex = vertex_index
                    v_x, v_y = vertex.x, vertex.y
                    if self.app.current_element_dialog:
                        self.app.current_element_dialog.destroy()
                    self.open_element_dialog(VertexDialog(self.app, vertex))
                    break
    
    def open_element_dialog(self, element_dialog):
        if self.app.current_element_dialog:
            self.app.current_element_dialog.destroy()
        self.app.current_element_dialog = element_dialog    

    def create_vertex(self, event):
        """
        Toggle is_creating_vertex. Open Vertex Dialog.
        """
        if self.is_creating_vertex == False:
            self.is_creating_vertex = not self.is_creating_vertex
            self.app.create_vertex_button.config(bootstyle="success")
            self.open_element_dialog(VertexDialog(self.app, Vertex(None, 0, 0), mode=0))
        else:
            self.is_creating_vertex = not self.is_creating_vertex
            if self.app.current_element_dialog:
                self.app.current_element_dialog.destroy()
            self.app.create_vertex_button.config(bootstyle="light")

    def create_bar(self, event):
        """
        Toggle is_creating_bar. Open Bar Dialog.
        """
        if self.is_creating_bar == False:
            self.is_creating_bar = not self.is_creating_bar
            self.app.create_bar_button.config(bootstyle="success")
            self.open_element_dialog(BarDialog(self.app, Bar(None, Vertex(None, 0, 0), Vertex(None, 0, 0)), mode=0))
        else:
            self.is_creating_bar = not self.is_creating_bar
            if self.app.current_element_dialog:
                self.app.current_element_dialog.destroy()
            self.app.create_bar_button.config(bootstyle="light")
            self.creating_bar = None

    def canvas_click(self, event):
        if self.is_creating_vertex:
            v_x, v_y = self.model_space_location(event.x, event.y)
            vertex = Vertex(None, v_x, v_y)
            self.model.add(vertex)
            self.draw_vertex(vertex)

    def post_edit_element(self, element):
        if element.id == None:
            self.model.add(element)
        else:
            self.model.edit(element)

        self.redraw_canvas()
        self.app.treeview.update_treeview()

    def post_delete_element(self, element):
        self.model.delete(element)
        self.redraw_canvas()
        self.app.treeview.update_treeview()

    def redraw_canvas(self):
        self.canvas.delete("all")
        self.draw_ucs_start()
        for bar in self.model.bars:
            self.draw_bar(bar)
        for vertex in self.model.vertices:
            self.draw_vertex(vertex)

    def draw_ucs_start(self):
        if self.vector_x is not None and self.vector_y is not None:
            x, y = self.vector_x + self.middle_x, self.vector_y + self.middle_y
            self.canvas.create_line(x, y, x + 30, y, fill="red")
            self.canvas.create_line(x, y, x, y - 30, fill="green")

    def draw_vertex(self, vertex):
        v_x, v_y = vertex.x, vertex.y
        x, y = self.screen_space_location(v_x, v_y)
    
        selected_color = "Red"  # Color for selected vertices
        selected_color_outline = "DarkRed"  # Color for selected vertices
        fill_color = selected_color if vertex in self.selected_items else "DarkOliveGreen1"
        outline_color = selected_color_outline if vertex in self.selected_items else "DarkOliveGreen3"

        self.canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill=fill_color, outline=outline_color)
        if self.display_settings['vertex_coords']:
            self.canvas.create_text(x, y - 15, text=f"({vertex.x:.2f}, {vertex.y:.2f})", fill="gray")
        if self.display_settings['vertex_id']:
            self.canvas.create_text(x, y + 15, text=f"{vertex.id}", fill="gray")

    def select_element(self, element):
        if element in self.selected_items:
            self.selected_items.remove(element)
        else:
            self.selected_items.append(element)
        self.redraw_canvas()
        
    def draw_bar(self, bar):
        x1, y1 = self.screen_space_location(bar.start.x, bar.start.y)
        x2, y2 = self.screen_space_location(bar.end.x, bar.end.y)
    
        selected_color = "Light Coral"
        fill_color = selected_color if bar in self.selected_items else "White"

        self.canvas.create_line(x1, y1, x2, y2, fill=fill_color, width=3)
        if bar.length * self.scale > 50:
            self.canvas.create_line(x2, y2, (x1 + x2) / 2, (y1 + y2) / 2, fill=fill_color, width=1, arrow=tb.LAST, arrowshape=(-15,-15,4))
        if self.display_settings['bar_id']:
            angle = -math.degrees(math.atan2(y2 - y1, x2 - x1))
            x_mid = (x1 + x2) / 2
            y_mid = (y1 + y2) / 2
            self.canvas.create_text(x_mid, y_mid, angle=angle, text=f"{bar.id}", fill="gray", anchor="s")


    def get_cursor_location(self):
        """
        Function to get curren cursor location.
        """
        return self.root.winfo_pointerx() - self.root.winfo_rootx(), self.root.winfo_pointery() - self.root.winfo_rooty()

    def model_space_location(self, x: float, y: float):
        """
        Function to convert canvas location to virtual model space coordinates
        """
        x, y = x - self.middle_x - self.vector_x, self.middle_y - y + self.vector_y
        return self.snap_round(x / self.scale), self.snap_round(y / self.scale)
    
    def snap_round(self, snap_value: float):
        return round(snap_value, self.snap)

    def cursor_coordinates_in_model(self, x: float, y: float):
        """
        Function to calculate cursor positon in virtual model space
        """
        x, y = x - self.middle_x - self.app.middle_panel.sashpos(0) - 3 - self.vector_x, self.middle_y - y + self.app.top_panel.sashpos(0) + 3 + self.vector_y
        return x / self.scale, y / self.scale
        
    def screen_space_location(self, v_x: float, v_y: float):
        """
        Function to convert virtual model space coordinates to canvas location
        """
        x = v_x * self.scale + self.vector_x + self.middle_x
        y = self.middle_y + self.vector_y - v_y * self.scale 
        return x, y


    def update_middle(self, event) -> None:
        """
        Update center of model canvas position.
        """
        self.middle_x = event.width / 2
        self.middle_y = event.height / 2
        self.redraw_canvas()

    