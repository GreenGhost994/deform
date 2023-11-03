# import tkinter as tk
# import tkinter.simpledialog
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import threading
import time
import math
from components.elements import Vertex, Model, Line

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
        app.post_edit_vertex(self.selected_vertex)

    def apply_changes(self):
        self.selected_vertex.x = float(self.v_x_entry.get())
        self.selected_vertex.y = float(self.v_y_entry.get())
        self.selected_vertex.comment = self.comment_entry.get()

        app.post_edit_vertex(self.selected_vertex)
        self.destroy()

    def delete_vertex(self):
        app.post_delete_vertex(self.selected_vertex)
        self.destroy()

    def on_close(self, event=None):
        if self.mode:
            self.destroy()
        else:
            app.create_vertex(None)
        

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

        self.update_coordinates_thread()

        self.dragging = False  # Flag to indicate if dragging is in progress
        self.dragged_vertex = None  # Index of the vertex being dragged
        self.drag_start = None  # Initial mouse position when dragging started
        self.view_drag_start = None  # Initial mouse position for scrolling
        self.current_vertex_dialog = None

        self.canvas.bind("<Configure>", self.update_middle)
        self.canvas.bind("<Button-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)
        self.canvas.bind("<Double-Button-1>", self.edit_vertex)
        self.canvas.bind("<Button-2>", self.on_scroll_press)  # Middle mouse button
        self.canvas.bind("<B2-Motion>", self.on_scroll_drag)  # Middle mouse button
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)

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
            self.current_vertex_dialog.destroy()
            self.open_vertex_dialog(VertexDialog(self.root, item))
            return

        print(f"Edit item: {self.tree.selection()[0]}")

    def delete_item(self):
        item = self.model.get_item_by_treeview(int(self.tree.selection()[0]))
        if type(item) == Vertex:
            self.post_delete_vertex(item)
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

    def on_mouse_press(self, event):
        x, y = event.x, event.y
        if self.is_creating_vertex:
            v_x, v_y = self.model_space_location(x, y)
            vertex = Vertex(self.new_id(self.model.vertices), v_x, v_y)
            self.model.vertices.append(vertex)
            self.draw_vertex(vertex)
        else:
            for vertex in self.model.vertices:
                vertex_index, v_x, v_y = vertex.id, vertex.x, vertex.y
                screen_x, screen_y = self.screen_space_location(v_x, v_y)
                distance = math.sqrt((x - screen_x)**2 + (y - screen_y)**2)
                if distance <= 5:
                    self.select_vertex(vertex)
                    self.drag_start = (x, y)
                    self.dragging = False  # Don't start dragging until the mouse moves a certain distance
                    self.dragged_vertex = vertex_index
                    break
            else:
                self.selected_items = []
                self.redraw_canvas()

    def on_mouse_drag(self, event):
        if self.dragged_vertex is not None:
            if not self.dragging:
                x, y = event.x, event.y
                distance = math.sqrt((x - self.drag_start[0])**2 + (y - self.drag_start[1])**2)
                if distance >= 20:
                    self.dragging = True
            if self.dragging:
                x, y = event.x, event.y
                v_x, v_y = self.model_space_location(x, y)
                vertex_to_move = next((vertex for vertex in self.model.vertices if vertex.id == self.dragged_vertex), None)
                if vertex_to_move is not None:
                    vertex_to_move.x = v_x
                    vertex_to_move.y = v_y
                    self.redraw_canvas()

    def on_mouse_release(self, event):
        self.dragging = False
        self.dragged_vertex = None
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

    def edit_vertex(self, event):
        if not self.dragging:
            x, y = event.x, event.y
            for vertex in self.model.vertices:
                vertex_index, v_x, v_y = vertex.id, vertex.x, vertex.y
                screen_x, screen_y = self.screen_space_location(v_x, v_y)
                distance = math.sqrt((x - screen_x)**2 + (y - screen_y)**2)
                if distance <= 5:
                    self.selected_vertex = vertex_index
                    v_x, v_y = vertex.x, vertex.y
                    self.current_vertex_dialog.destroy()
                    self.open_vertex_dialog(VertexDialog(self.root, vertex))
                    break
    
    def open_vertex_dialog(self, vertex_dialog):
        if self.current_vertex_dialog:
            self.current_vertex_dialog.destroy()
        self.current_vertex_dialog = vertex_dialog

    def create_vertex(self, event):
        """
        Toggle is_creating_vertex.
        """
        if self.is_creating_vertex == False:
            self.is_creating_vertex = not self.is_creating_vertex
            self.create_vertex_button.config(bootstyle="success")
            self.open_vertex_dialog(VertexDialog(self.root, Vertex(None, 0, 0), mode=0))
        else:
            self.is_creating_vertex = not self.is_creating_vertex
            if self.current_vertex_dialog:
                self.current_vertex_dialog.destroy()
            self.create_vertex_button.config(bootstyle="light")

    def create_line(self, event):
        """
        Toggle is_creating_line.
        """
        if self.is_creating_line == False:
            self.is_creating_line = not self.is_creating_line
            self.create_line_button.config(bootstyle="success")
            # self.open_line_dialog(VertexDialog(self.root, Vertex(None, 0, 0), mode=0))
        else:
            self.is_creating_line = not self.is_creating_line
            # if self.current_line_dialog:
            #     self.current_line_dialog.destroy()
            self.create_line_button.config(bootstyle="light")

    def canvas_click(self, event):
        if self.is_creating_vertex:
            v_x, v_y = self.model_space_location(event.x, event.y)
            vertex = Vertex(self.new_id(self.vertices), v_x, v_y)
            self.model.vertices.append(vertex)
            self.draw_vertex(vertex)

    def post_edit_vertex(self, selected_vertex):
        if selected_vertex.id == None:
            self.model.vertices.append(Vertex(self.new_id(self.model.vertices),selected_vertex.x,selected_vertex.y,selected_vertex.comment))
        else:
            vertex_to_edit = next((vertex for vertex in self.model.vertices if vertex.id == selected_vertex.id), None)
            if vertex_to_edit is not None:
                vertex_to_edit.x = selected_vertex.x
                vertex_to_edit.y = selected_vertex.y

        self.redraw_canvas()
        self.update_treeview()

    def post_delete_vertex(self, selected_vertex):
        index_to_delete = next((index for index, vertex in enumerate(self.model.vertices) if vertex.id == selected_vertex.id), None)
        if index_to_delete is not None:
            self.model.vertices.pop(index_to_delete)
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
        self.canvas.create_text(x, y - 15, text=f"({vertex.x:.2f}, {vertex.y:.2f})", fill="gray")
        self.canvas.create_text(x, y + 15, text=f"{vertex.id}", fill="gray")

    def select_vertex(self, vertex):
        if vertex in self.selected_items:
            self.selected_items.remove(vertex)
        else:
            self.selected_items.append(vertex)
        self.redraw_canvas()
        
    def draw_line(self, line):
        x1, y1 = self.screen_space_location(line.start.x, line.start.y)
        x2, y2 = self.screen_space_location(line.end.x, line.end.y)
    
        selected_color = "Red"  # Color for selected vertices
        fill_color = selected_color if line in self.selected_items else "White"

        self.canvas.create_line(x1, y1, x2, y2, fill=fill_color, width=3)

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

    def new_id(self, element_list):
        print(element_list)
        if not element_list:
            return 0
        return max(element_list, key=lambda ele: ele.id).id + 1
    
    def init_drawing(self):
        v0 = Vertex(0, 1, 1)
        v1 = Vertex(1, 1, 2)
        self.model.vertices.append(v0)
        self.model.vertices.append(v1)
        self.model.vertices.append(Vertex(2, 2, 1))
        self.model.lines.append(Line(0, v0, v1))

if __name__ == "__main__":
    # root = tk.Tk()
    root = tb.Window(themename="darkly")
    app = StructuralAnalysisApp(root)
    root.mainloop()
