# import tkinter as tk
# import tkinter.simpledialog
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import threading
import time
import math
from components.elements import Vertex, Model, Bar
from components.model_canvas import *
from components.model_treeview import *


class StructuralAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DEFORM")
        self.model = Model()

         # Grid setup
        self.top_panel = tb.PanedWindow(self.root, orient=VERTICAL, bootstyle="light")
        self.top_menu = tb.Frame(self.top_panel)
        self.middle_panel = tb.PanedWindow(self.top_panel, orient=HORIZONTAL, bootstyle="light")
        self.left_panel_frame = tb.Frame(self.middle_panel)
        self.bottom_panel = tb.PanedWindow(self.middle_panel, orient=VERTICAL, bootstyle="light")
        self.model_canvas = CanvasFunctions(self, self.root)
        self.create_vertex_button = tb.Button(self.top_menu, text="Add Vertex", bootstyle="light")
        self.create_vertex_button.bind("<Button-1>", self.model_canvas.create_vertex)
        self.create_bar_button = tb.Button(self.top_menu, text="Add Bar", bootstyle="light")
        self.create_bar_button.bind("<Button-1>", self.model_canvas.create_bar)
        self.coordinate_label = tb.Label(self.bottom_panel, text="(0, 0)")
        self.treeview = ModelTreeview(self, self.root)

        # Grid pack
        self.top_panel.pack(fill=BOTH, expand=1)
        self.top_panel.add(self.top_menu)
        self.create_vertex_button.pack(side="left")
        self.create_bar_button.pack(side="left")
        self.top_panel.add(self.middle_panel)
        self.middle_panel.add(self.left_panel_frame)
        self.middle_panel.add(self.bottom_panel)
        self.bottom_panel.add(self.model_canvas.canvas)
        self.bottom_panel.add(self.coordinate_label)

        self.current_element_dialog = None


        # Run coordinates preview
        self.update_coordinates_thread()


        self.init_drawing()


    def update_coordinates_thread(self):
        """
        Function to update current mouse position in model coordinates.
        """
        def update_label():
            while True:
                x, y = self.model_canvas.cursor_coordinates_in_model(*self.model_canvas.get_cursor_location())
                self.update_coordinate_label(x, y)
                self.root.update()
                time.sleep(0.1)

        thread = threading.Thread(target=update_label)
        thread.daemon = True
        thread.start()


    def update_coordinate_label(self, x, y):
        self.coordinate_label.config(text=f"({x:.2f}, {y:.2f})")

    #     self.middle_x = event.width / 2
    #     self.middle_y = event.height / 2
    #     self.redraw_canvas()
    #     # print(self.bottom_panel.sashpos(0))
    
    def init_drawing(self):
        v0 = Vertex(0, 1, 1)
        v1 = Vertex(1, 1, 2)
        self.model.add(v0)
        self.model.add(v1)
        self.model.add(Vertex(2, 2, 1))
        self.model.add(Bar(0, v0, v1))
        self.treeview.update_treeview()

if __name__ == "__main__":
    # root = tk.Tk()
    root = tb.Window(themename="darkly")
    app = StructuralAnalysisApp(root)
    root.mainloop()
