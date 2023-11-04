# import tkinter as tk
# import tkinter.simpledialog
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import threading
import time
import math
from components.elements import Vertex, Model, Line
from components.model_canvas import *

class VertexDialog(tb.Toplevel):
    def __init__(self, parent, selected_vertex, mode=1):
        super().__init__(parent)
        self.parent = parent
        self.mode = mode
        self.selected_vertex = selected_vertex
        self.attributes("-topmost", True)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.bind("<Escape>", self.on_close)
        self.focus_force()
        self.title(f"Edit Vertex: {selected_vertex.id}")
        if self.mode == 0:
            self.title("Add Vertex")
        self.geometry("200x200")
        self.wm_attributes('-toolwindow', 'True')

        coordinate_frame = tb.Frame(self)
        coordinate_frame.pack(fill="x", expand=True, padx=15)

        v_x_label = tb.LabelFrame(coordinate_frame, text="X")
        v_x_label.pack(side="left", fill="x", expand=True)
        self.v_x_entry = tb.Entry(v_x_label, width=5, bootstyle="danger")
        self.v_x_entry.insert(0, self.selected_vertex.x)
        self.v_x_entry.pack(fill="x", expand=True)

        v_y_label = tb.LabelFrame(coordinate_frame, text="Y")
        v_y_label.pack(side="left", fill="x", expand=True)
        self.v_y_entry = tb.Entry(v_y_label, width=5, bootstyle="success")
        self.v_y_entry.insert(0, self.selected_vertex.y)
        self.v_y_entry.pack(fill="x", expand=True)

        comment_label = tb.LabelFrame(self, text="Comment")
        comment_label.pack(fill="x", expand=True, padx=15)
        self.comment_entry = tb.Entry(comment_label)
        self.comment_entry.insert(0, self.selected_vertex.comment)
        self.comment_entry.pack(fill="x", expand=True)

        button_frame = tb.Frame(self)
        button_frame.pack(fill="x", expand=True, padx=15)

        if self.mode == 0:
            self.add_button = tb.Button(button_frame, text="Add", command=self.add_vertex, bootstyle="light")
            self.add_button.pack(side="left", fill="x", expand=True)
        else:
            self.apply_button = tb.Button(button_frame, text="Apply", command=self.apply_changes, bootstyle="light")
            self.apply_button.pack(side="left", fill="x", expand=True)

            self.delete_button = tb.Button(button_frame, text="Delete", command=self.delete_vertex, bootstyle="danger")
            self.delete_button.pack(side="left")


    def add_vertex(self):
        self.selected_vertex.x = float(self.v_x_entry.get())
        self.selected_vertex.y = float(self.v_y_entry.get())
        self.selected_vertex.comment = self.comment_entry.get()
        self.selected_vertex.id = None
        app.post_edit_element(self.selected_vertex)

    def apply_changes(self):
        self.selected_vertex.x = float(self.v_x_entry.get())
        self.selected_vertex.y = float(self.v_y_entry.get())
        self.selected_vertex.comment = self.comment_entry.get()

        app.post_edit_element(self.selected_vertex)
        self.destroy()

    def delete_vertex(self):
        app.post_delete_element(self.selected_vertex)
        self.destroy()

    def on_close(self, event=None):
        if self.mode:
            self.destroy()
        else:
            app.create_vertex(None)
        

class LineDialog(tb.Toplevel):
    def __init__(self, parent, selected_line, mode=1):
        super().__init__(parent)
        self.parent = parent
        self.mode = mode
        self.selected_line = selected_line
        self.attributes("-topmost", True)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.bind("<Escape>", self.on_close)
        self.focus_force()
        self.title(f"Edit Line: {selected_line.id}")
        if self.mode == 0:
            self.title("Add Line")
        self.geometry("200x300")
        self.wm_attributes('-toolwindow', 'True')

        coordinate_frame = tb.Frame(self)
        coordinate_frame.pack(fill="x", expand=True, padx=15)

        x1_label = tb.LabelFrame(coordinate_frame, text="X")
        x1_label.pack(side="left", fill="x", expand=True)
        self.x1_entry = tb.Entry(x1_label, width=5, bootstyle="danger")
        self.x1_entry.insert(0, self.selected_line.start.x)
        self.x1_entry.pack(fill="x", expand=True)

        y1_label = tb.LabelFrame(coordinate_frame, text="Y")
        y1_label.pack(side="left", fill="x", expand=True)
        self.y1_entry = tb.Entry(y1_label, width=5, bootstyle="success")
        self.y1_entry.insert(0, self.selected_line.start.y)
        self.y1_entry.pack(fill="x", expand=True)

        coordinate_frame = tb.Frame(self)
        coordinate_frame.pack(fill="x", expand=True, padx=15)

        x2_label = tb.LabelFrame(coordinate_frame, text="X")
        x2_label.pack(side="left", fill="x", expand=True)
        self.x2_entry = tb.Entry(x2_label, width=5, bootstyle="danger")
        self.x2_entry.insert(0, self.selected_line.end.x)
        self.x2_entry.pack(fill="x", expand=True)

        y2_label = tb.LabelFrame(coordinate_frame, text="Y")
        y2_label.pack(side="left", fill="x", expand=True)
        self.y2_entry = tb.Entry(y2_label, width=5, bootstyle="success")
        self.y2_entry.insert(0, self.selected_line.end.y)
        self.y2_entry.pack(fill="x", expand=True)

        comment_label = tb.LabelFrame(self, text="Comment")
        comment_label.pack(fill="x", expand=True, padx=15)
        self.comment_entry = tb.Entry(comment_label)
        self.comment_entry.insert(0, self.selected_line.comment)
        self.comment_entry.pack(fill="x", expand=True)

        button_frame = tb.Frame(self)
        button_frame.pack(fill="x", expand=True, padx=15)

        if self.mode == 0:
            self.add_button = tb.Button(button_frame, text="Add", command=self.add_line, bootstyle="light")
            self.add_button.pack(side="left", fill="x", expand=True)
        else:
            self.apply_button = tb.Button(button_frame, text="Apply", command=self.apply_changes, bootstyle="light")
            self.apply_button.pack(side="left", fill="x", expand=True)

            self.delete_button = tb.Button(button_frame, text="Delete", command=self.delete_line, bootstyle="danger")
            self.delete_button.pack(side="left")


    def add_line(self):
        vertex1 = app.model.add(Vertex(None, float(self.x1_entry.get()), float(self.y1_entry.get())))
        vertex2 = app.model.add(Vertex(None, float(self.x2_entry.get()), float(self.y2_entry.get())))
        app.post_edit_element(Line(None, vertex1, vertex2, self.comment_entry.get()))
        self.x1_entry.delete(0, tb.END)
        self.y1_entry.delete(0, tb.END)
        self.x2_entry.delete(0, tb.END)
        self.y2_entry.delete(0, tb.END)
        self.x1_entry.insert(0, vertex2.x)
        self.y1_entry.insert(0, vertex2.y)
        self.x2_entry.insert(0, "0")
        self.y2_entry.insert(0, "0")

    def apply_changes(self):
        self.selected_line.start.x = float(self.x1_entry.get())
        self.selected_line.start.y = float(self.y1_entry.get())
        self.selected_line.end.x = float(self.x2_entry.get())
        self.selected_line.end.y = float(self.y2_entry.get())
        self.selected_line.comment = self.comment_entry.get()
        app.post_edit_element(self.selected_line)
        self.destroy()

    def delete_line(self):
        app.post_delete_element(self.selected_line)
        self.destroy()

    def on_close(self, event=None):
        if self.mode:
            self.destroy()
        else:
            app.create_line(None)


class StructuralAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DEFORM")
        self.model = Model()
        self.selected_items = []
        self.vector_x = 0
        self.vector_y = 0
        self.middle_x = 0
        self.middle_y = 0
        self.scale = 100
        self.snap = 2
        self.display_settings = {
            "vertex_id": 1,
            "vertex_coords": 1,
            "line_id": 1,
        }

         # Grid setup
        self.top_panel = tb.PanedWindow(self.root, orient=VERTICAL, bootstyle="light")
        self.top_panel.pack(fill=BOTH, expand=1)
        self.top_menu = tb.Frame(self.top_panel)
        self.top_panel.add(self.top_menu)

        self.create_vertex_button = tb.Button(self.top_menu, text="Add Vertex", bootstyle="light")
        self.create_vertex_button.pack(side="left")
        self.create_vertex_button.bind("<Button-1>", self.create_vertex)
        self.create_line_button = tb.Button(self.top_menu, text="Add Line", bootstyle="light")
        self.create_line_button.pack(side="left")
        self.create_line_button.bind("<Button-1>", self.create_line)

        self.middle_panel = tb.PanedWindow(self.top_panel, orient=HORIZONTAL, bootstyle="light")
        self.top_panel.add(self.middle_panel)

        self.left_panel_frame = tb.Frame(self.middle_panel)
        self.middle_panel.add(self.left_panel_frame)

        self.bottom_panel = tb.PanedWindow(self.middle_panel, orient=VERTICAL, bootstyle="light")
        self.middle_panel.add(self.bottom_panel)

        self.canvas = tb.Canvas(self.bottom_panel, width=800, height=600)
        self.bottom_panel.add(self.canvas)

        self.coordinate_label = tb.Label(self.bottom_panel, text="Current Coordinate: (0, 0)")
        self.bottom_panel.add(self.coordinate_label)

        self.tree = tb.ttk.Treeview(self.left_panel_frame)
        self.tree.pack(fill="x")
        self.update_treeview()
        self.context_menu = tb.Menu(root, tearoff=0)
        self.context_menu.add_command(label="Edit", command=self.edit_item)
        self.context_menu.add_command(label="Delete", command=self.delete_item)
        self.tree.bind("<Button-3>", self.show_context_menu)


        self.is_creating_vertex = False
        self.is_creating_line = False
        self.selected_vertex = None
        self.creating_line = None

        self.update_coordinates_thread()

        self.dragging = False  # Flag to indicate if dragging is in progress
        self.dragged_element = None  # Index of the vertex being dragged
        self.drag_start = None  # Initial mouse position when dragging started
        self.view_drag_start = None  # Initial mouse position for scrolling
        self.current_element_dialog = None

        self.canvas.bind("<Configure>", self.update_middle)
        self.canvas.bind("<Button-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)
        self.canvas.bind("<Double-Button-1>", self.on_double_edit_element)
        self.canvas.bind("<Button-2>", self.on_scroll_press)  # Middle mouse button
        self.canvas.bind("<B2-Motion>", self.on_scroll_drag)  # Middle mouse button
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)

        self.root.bind("<Escape>", self.clear_selected_items)
        self.root.bind("<Delete>", self.erase_selected_items)

        self.init_drawing()

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

    def edit_item(self):
        item = self.model.get_item_by_treeview(int(self.tree.selection()[0]))
        if type(item) == Vertex:
            if self.current_element_dialog:
                self.current_element_dialog.destroy()
            self.open_element_dialog(VertexDialog(self.root, item))
            return
        elif type(item) == Line:
            if self.current_element_dialog:
                self.current_element_dialog.destroy()
            self.open_element_dialog(LineDialog(self.root, item))
            return

        print(f"Edit item: {self.tree.selection()[0]}")

    def delete_item(self):
        item = self.model.get_item_by_treeview(int(self.tree.selection()[0]))
        if type(item) == Vertex or type(item) == Line:
            self.post_delete_element(item)
            return

        print(f"Delete item: {self.tree.selection()[0]}")

    def update_treeview(self):
        """
        Function to update model treeview.
        """
        open_list = [self.tree.item(item, "open") for item in self.tree.get_children()]
        self.tree.delete(*self.tree.get_children())
        self.tree.heading('#0', text='Model', anchor=tb.W)
        names, moves = self.model.as_treeview()
        open_list += [0]*(len(names) - len(open_list))
        for iid, i in enumerate(names):
            self.tree.insert('', tb.END, text=i, iid=iid, open=open_list[iid])
        for i in moves:
            self.tree.move(*i)

    def show_context_menu(self, event):
        item = self.tree.identify("item", event.x, event.y)
        if item:
            self.context_menu.post(event.x_root, event.y_root)

    def clear_selected_items(self, event):
        """
        - Clean list of selected items
        - Clean previous vertex while line create
        after pressing ESC.
        """
        self.selected_items = []
        self.creating_line = None
        self.redraw_canvas()

    def erase_selected_items(self, event):
        for item in self.selected_items:
            self.model.delete(item)
        self.selected_items = []
        self.redraw_canvas()
        self.update_treeview()

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

        def check_if_line_pressed():
            for line in self.model.lines:
                x1, y1 = self.screen_space_location(line.start.x, line.start.y)
                x2, y2 = self.screen_space_location(line.end.x, line.end.y)
                distance_to_line = distance_from_point_to_line(x, y, x1, y1, x2, y2)
                if distance_to_line <= 3:
                    self.select_element(line)
                    return line
        

        x, y = event.x, event.y

        if self.is_creating_vertex:
            if not check_if_vertex_pressed():
                create_vertex_element()

        elif self.is_creating_line:
            if not self.selected_items:
                if not self.creating_line:
                    if not (next_vertex := check_if_vertex_pressed()):
                        self.creating_line = create_vertex_element()
                    else:
                        self.creating_line = next_vertex
                else:
                    if not (next_vertex := check_if_vertex_pressed()):
                        next_vertex = create_vertex_element()
                    self.model.add(Line(None, self.creating_line, next_vertex))
                    self.creating_line = next_vertex
            elif len(self.selected_items) == 1:
                if type(self.selected_items[0]) == Vertex:
                    if not (next_vertex := check_if_vertex_pressed()):
                        next_vertex = create_vertex_element()
                    if self.selected_items:
                        self.model.add(Line(None, self.selected_items[0], next_vertex))
                        self.creating_line = next_vertex
                        self.selected_items = []

            self.redraw_canvas()


        else:
            if vertex := check_if_vertex_pressed():
                self.drag_start = (x, y)
                self.dragging = False  # Don't start dragging until the mouse moves a certain distance
                self.dragged_element = vertex
            elif line := check_if_line_pressed():
                self.drag_start = (x, y)
                self.dragging = False  # Don't start dragging until the mouse moves a certain distance
                self.dragged_element = line
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

    def on_mouse_release(self, event):
        self.dragging = False
        self.dragged_element = None
        self.update_treeview()

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
                    if self.current_element_dialog:
                        self.current_element_dialog.destroy()
                    self.open_element_dialog(VertexDialog(self.root, vertex))
                    break
    
    def open_element_dialog(self, element_dialog):
        if self.current_element_dialog:
            self.current_element_dialog.destroy()
        self.current_element_dialog = element_dialog    

    def create_vertex(self, event):
        """
        Toggle is_creating_vertex.
        """
        if self.is_creating_vertex == False:
            self.is_creating_vertex = not self.is_creating_vertex
            self.create_vertex_button.config(bootstyle="success")
            self.open_element_dialog(VertexDialog(self.root, Vertex(None, 0, 0), mode=0))
        else:
            self.is_creating_vertex = not self.is_creating_vertex
            if self.current_element_dialog:
                self.current_element_dialog.destroy()
            self.create_vertex_button.config(bootstyle="light")

    def create_line(self, event):
        """
        Toggle is_creating_line.
        """
        if self.is_creating_line == False:
            self.is_creating_line = not self.is_creating_line
            self.create_line_button.config(bootstyle="success")
            self.open_element_dialog(LineDialog(self.root, Line(None, Vertex(None, 0, 0), Vertex(None, 0, 0)), mode=0))
        else:
            self.is_creating_line = not self.is_creating_line
            if self.current_element_dialog:
                self.current_element_dialog.destroy()
            self.create_line_button.config(bootstyle="light")
            self.creating_line = None

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
        self.update_treeview()

    def post_delete_element(self, element):
        self.model.delete(element)
        self.redraw_canvas()
        self.update_treeview()

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
        
    def draw_line(self, line):
        x1, y1 = self.screen_space_location(line.start.x, line.start.y)
        x2, y2 = self.screen_space_location(line.end.x, line.end.y)
    
        selected_color = "Light Coral"
        fill_color = selected_color if line in self.selected_items else "White"

        self.canvas.create_line(x1, y1, x2, y2, fill=fill_color, width=3)
        if self.display_settings['line_id']:
            angle = -math.degrees(math.atan2(y2 - y1, x2 - x1))
            x_mid = (x1 + x2) / 2
            y_mid = (y1 + y2) / 2
            self.canvas.create_text(x_mid, y_mid, angle=angle, text=f"{line.id}", fill="gray", anchor="s")

    def update_coordinates_thread(self):
        """
        Function to update current mouse position in model coordinates.
        """
        def update_label():
            while True:
                x, y = self.cursor_coordinates_in_model(*self.get_cursor_location())
                self.update_coordinate_label(x, y)
                self.root.update()
                time.sleep(0.1)

        thread = threading.Thread(target=update_label)
        thread.daemon = True
        thread.start()

    def get_cursor_location(self):
        """
        Function to get curren cursor location.
        """
        return self.root.winfo_pointerx() - self.root.winfo_rootx(), self.root.winfo_pointery() - self.root.winfo_rooty()

    def model_space_location(self, x, y):
        """
        Function to convert canvas location to virtual model space coordinates
        """
        x, y = x - self.middle_x - self.vector_x, self.middle_y - y + self.vector_y
        # return x / self.scale, y / self.scale
        return self.snap_round(x / self.scale), self.snap_round(y / self.scale)
    
    def snap_round(self, snap_value):
        return round(snap_value, self.snap)

    def cursor_coordinates_in_model(self, x, y):
        """
        Function to calculate cursor positon in virtual model space
        """
        x, y = x - self.middle_x - self.middle_panel.sashpos(0) - 3 - self.vector_x, self.middle_y - y + self.top_panel.sashpos(0) + 3 + self.vector_y
        return x / self.scale, y / self.scale
        
    def screen_space_location(self, v_x, v_y):
        """
        Function to convert virtual model space coordinates to canvas location
        """
        x = v_x * self.scale + self.vector_x + self.middle_x
        y = self.middle_y + self.vector_y - v_y * self.scale 
        return x, y


    def update_coordinate_label(self, x, y):
        self.coordinate_label.config(text=f"Current Coordinate: ({x:.2f}, {y:.2f})")

    def update_middle(self, event):
        self.middle_x = event.width / 2
        self.middle_y = event.height / 2
        self.redraw_canvas()
        # print(self.bottom_panel.sashpos(0))
    
    def init_drawing(self):
        v0 = Vertex(0, 1, 1)
        v1 = Vertex(1, 1, 2)
        self.model.add(v0)
        self.model.add(v1)
        self.model.add(Vertex(2, 2, 1))
        self.model.add(Line(0, v0, v1))

if __name__ == "__main__":
    # root = tk.Tk()
    root = tb.Window(themename="darkly")
    app = StructuralAnalysisApp(root)
    root.mainloop()
