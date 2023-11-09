import ttkbootstrap as tb
from ttkbootstrap.constants import *
from components.elements import Vertex, Model, Bar
from components.materials import *

class VertexDialog(tb.Toplevel):
    def __init__(self, app, selected_vertex, mode=1):
        super().__init__(app)
        self.app = app
        self.model_canvas = app.model_canvas
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
        self.model_canvas.post_edit_element(self.selected_vertex)

    def apply_changes(self):
        self.selected_vertex.x = float(self.v_x_entry.get())
        self.selected_vertex.y = float(self.v_y_entry.get())
        self.selected_vertex.comment = self.comment_entry.get()

        self.model_canvas.post_edit_element(self.selected_vertex)
        self.destroy()

    def delete_vertex(self):
        self.model_canvas.post_delete_element(self.selected_vertex)
        self.destroy()

    def on_close(self, event=None):
        if self.mode:
            self.destroy()
        else:
            self.model_canvas.create_vertex(None)
        

class BarDialog(tb.Toplevel):
    def __init__(self, app, selected_bar, mode=1):
        super().__init__(app)
        self.app = app
        self.model_canvas = app.model_canvas
        self.mode = mode
        self.selected_bar = selected_bar
        self.attributes("-topmost", True)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.bind("<Escape>", self.on_close)
        self.focus_force()
        self.title(f"Edit Bar: {selected_bar.id}")
        if self.mode == 0:
            self.title("Add Bar")
        self.geometry("200x300")
        self.wm_attributes('-toolwindow', 'True')

        coordinate_frame = tb.Frame(self)
        coordinate_frame.pack(fill="x", expand=True, padx=15)

        x1_label = tb.LabelFrame(coordinate_frame, text="X")
        x1_label.pack(side="left", fill="x", expand=True)
        self.x1_entry = tb.Entry(x1_label, width=5, bootstyle="danger")
        self.x1_entry.insert(0, self.selected_bar.start.x)
        self.x1_entry.pack(fill="x", expand=True)

        y1_label = tb.LabelFrame(coordinate_frame, text="Y")
        y1_label.pack(side="left", fill="x", expand=True)
        self.y1_entry = tb.Entry(y1_label, width=5, bootstyle="success")
        self.y1_entry.insert(0, self.selected_bar.start.y)
        self.y1_entry.pack(fill="x", expand=True)

        coordinate_frame = tb.Frame(self)
        coordinate_frame.pack(fill="x", expand=True, padx=15)

        x2_label = tb.LabelFrame(coordinate_frame, text="X")
        x2_label.pack(side="left", fill="x", expand=True)
        self.x2_entry = tb.Entry(x2_label, width=5, bootstyle="danger")
        self.x2_entry.insert(0, self.selected_bar.end.x)
        self.x2_entry.pack(fill="x", expand=True)

        y2_label = tb.LabelFrame(coordinate_frame, text="Y")
        y2_label.pack(side="left", fill="x", expand=True)
        self.y2_entry = tb.Entry(y2_label, width=5, bootstyle="success")
        self.y2_entry.insert(0, self.selected_bar.end.y)
        self.y2_entry.pack(fill="x", expand=True)

        comment_label = tb.LabelFrame(self, text="Comment")
        comment_label.pack(fill="x", expand=True, padx=15)
        self.comment_entry = tb.Entry(comment_label)
        self.comment_entry.insert(0, self.selected_bar.comment)
        self.comment_entry.pack(fill="x", expand=True)

        button_frame = tb.Frame(self)
        button_frame.pack(fill="x", expand=True, padx=15)

        if self.mode == 0:
            self.add_button = tb.Button(button_frame, text="Add", command=self.add_bar, bootstyle="light")
            self.add_button.pack(side="left", fill="x", expand=True)
        else:
            self.apply_button = tb.Button(button_frame, text="Apply", command=self.apply_changes, bootstyle="light")
            self.apply_button.pack(side="left", fill="x", expand=True)

            self.delete_button = tb.Button(button_frame, text="Delete", command=self.delete_bar, bootstyle="danger")
            self.delete_button.pack(side="left")


    def add_bar(self):
        vertex1 = self.model_canvas.model.add(Vertex(None, float(self.x1_entry.get()), float(self.y1_entry.get())))
        vertex2 = self.model_canvas.model.add(Vertex(None, float(self.x2_entry.get()), float(self.y2_entry.get())))
        self.model_canvas.post_edit_element(Bar(None, vertex1, vertex2, self.comment_entry.get()))
        self.x1_entry.delete(0, tb.END)
        self.y1_entry.delete(0, tb.END)
        self.x2_entry.delete(0, tb.END)
        self.y2_entry.delete(0, tb.END)
        self.x1_entry.insert(0, vertex2.x)
        self.y1_entry.insert(0, vertex2.y)
        self.x2_entry.insert(0, "0")
        self.y2_entry.insert(0, "0")

    def apply_changes(self):
        self.selected_bar.start.x = float(self.x1_entry.get())
        self.selected_bar.start.y = float(self.y1_entry.get())
        self.selected_bar.end.x = float(self.x2_entry.get())
        self.selected_bar.end.y = float(self.y2_entry.get())
        self.selected_bar.comment = self.comment_entry.get()
        self.model_canvas.post_edit_element(self.selected_bar)
        self.destroy()

    def delete_bar(self):
        self.model_canvas.post_delete_element(self.selected_bar)
        self.destroy()

    def on_close(self, event=None):
        if self.mode:
            self.destroy()
        else:
            self.model_canvas.create_bar(None)


class MaterialDialog(tb.Toplevel):
    def __init__(self, app):
        super().__init__(app)
        self.app = app
        self.title("Select Material")
        self.geometry("500x500") 

        main_frame = tb.ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=5)

        self.notebook = tb.ttk.Notebook(main_frame, width=150)
        self.notebook.pack(fill="y", side="left", expand=False)

        steel_tab = tb.ttk.Frame(self.notebook)
        concrete_tab = tb.ttk.Frame(self.notebook)
        wood_tab = tb.ttk.Frame(self.notebook)

        self.notebook.add(steel_tab, text="Steel")
        self.notebook.add(concrete_tab, text="Concrete")
        self.notebook.add(wood_tab, text="Wood")

        steel_treeview = tb.ttk.Treeview(steel_tab, show="tree")
        concrete_treeview = tb.ttk.Treeview(concrete_tab, show="tree")
        wood_treeview = tb.ttk.Treeview(wood_tab, show="tree")

        self.treeviews = {
            "Steel": steel_treeview,
            "Concrete": concrete_treeview,
            "Wood": wood_treeview
        }

        steel_treeview.pack(fill="both", expand=True)
        concrete_treeview.pack(fill="both", expand=True)
        wood_treeview.pack(fill="both", expand=True)

        for steel_material in steel_dict.keys():
            steel_treeview.insert("", "end", text=steel_material, values=(steel_material))
        for concrete_material in concrete_dict.keys():
            concrete_treeview.insert("", "end", text=concrete_material, values=(concrete_material))
        for wood_material in wood_dict.keys():
            wood_treeview.insert("", "end", text=wood_material, values=(wood_material))

        properties_frame = tb.ttk.Frame(main_frame)
        properties_frame.pack(fill="both", side="left", expand=True)

        self.properties_treeview = tb.ttk.Treeview(properties_frame, columns=("Parameter", "Value"), show="headings")
        self.properties_treeview.pack(fill="both", expand=True)

        self.properties_treeview.heading("Parameter", text="Parameter")
        self.properties_treeview.heading("Value", text="Value")

        select_button = tb.Button(properties_frame, text="Select", command=self.select_material)
        select_button.pack()

        steel_treeview.bind("<<TreeviewSelect>>", self.select_material)
        concrete_treeview.bind("<<TreeviewSelect>>", self.select_material)
        wood_treeview.bind("<<TreeviewSelect>>", self.select_material)

    def select_material(self, event=None):
        if event and event.widget:
            selected_treeview = event.widget
            selected_tab = self.notebook.tab(self.notebook.select(), "text")
            material_name = selected_treeview.item(selected_treeview.selection(), "text")

            selected_dict = None
            if selected_tab == "Steel":
                selected_dict = steel_dict
            elif selected_tab == "Concrete":
                selected_dict = concrete_dict
            elif selected_tab == "Wood":
                selected_dict = wood_dict

            if selected_dict:
                material_properties = selected_dict.get(material_name)
                if material_properties:
                    print(f"Selected Material: {material_name}")
                    print("Material Properties:", material_properties)
                    ...

                    self.properties_treeview.delete(*self.properties_treeview.get_children())
                    for parameter, value in material_properties.items():
                        self.properties_treeview.insert("", "end", values=(parameter, value))
                else:
                    print(f"No properties found for {material_name} in {selected_tab}.")
                    ...
            else:
                print(f"Unknown tab: {selected_tab}")
                ...
        else:
            print("Material selection via 'Select' button")
            ...

        if not event:
            self.destroy()