import ttkbootstrap as tb
from ttkbootstrap.constants import *
from components.elements import *
from components.popups import *


class ModelTreeview:
    def __init__(self, app, root):
        self.app = app
        self.root = root
        self.tree = tb.ttk.Treeview(self.app.left_panel_frame)
        self.tree.pack(fill="x")
        self.update_treeview()
        self.context_menu = tb.Menu(self.root, tearoff=0)
        self.tree.bind("<Button-3>", self.show_context_menu)

        self.parent_context_menu = tb.Menu(root, tearoff=0)
        self.parent_context_menu.add_command(label="New", command=self.tv_new_item)
        self.child_context_menu = tb.Menu(root, tearoff=0)
        self.child_context_menu.add_command(label="Edit", command=self.tv_edit_item)
        self.child_context_menu.add_command(label="Delete", command=self.tv_delete_item)
    
    def update_treeview(self):
        """
        Function to update model treeview.
        """
        open_list = [self.tree.item(item, "open") for item in self.tree.get_children()]
        self.tree.delete(*self.tree.get_children())
        self.tree.heading('#0', text='Model', anchor=tb.W)
        names, moves = self.app.model.as_treeview()
        open_list += [0]*(len(names) - len(open_list))
        for iid, i in enumerate(names):
            self.tree.insert('', tb.END, text=i, iid=iid, open=open_list[iid])
        for i in moves:
            self.tree.move(*i)

    def show_context_menu(self, event):
        item = self.tree.identify("item", event.x, event.y)
        if item:
            if self.tree.parent(item) == "":
                self.parent_context_menu.post(event.x_root, event.y_root)
            else:
                self.child_context_menu.post(event.x_root, event.y_root)

    def tv_edit_item(self):
        """
        Treeview menu. Open edit dialog for selected element.
        """
        item = self.app.model.get_item_by_treeview(int(self.tree.selection()[0]))
        if self.app.current_element_dialog:
            self.app.current_element_dialog.destroy()
        if type(item) == Vertex:
            self.app.model_canvas.open_element_dialog(VertexDialog(self.app, item))
            return
        elif type(item) == Bar:
            self.app.model_canvas.open_element_dialog(BarDialog(self.app, item))
            return
        print(f"Edit item: {self.tree.selection()[0]}")

    def tv_new_item(self):
        """
        Treeview menu. Open create dialog for selected element type.
        """
        print(self.tree.selection())
        item_type = self.tree.selection()[0]
        if self.app.current_element_dialog:
                self.app.current_element_dialog.destroy()
        if item_type == '0':
            self.app.model_canvas.create_vertex(None)
        elif item_type == '1':
            self.app.model_canvas.create_bar(None)

    def tv_delete_item(self):
        """
        Treeview menu. Delete selected item.
        """
        item = self.app.model.get_item_by_treeview(int(self.tree.selection()[0]))
        if type(item) == Vertex or type(item) == Bar:
            self.app.model_canvas.post_delete_element(item)
            return

        print(f"Delete item: {self.tree.selection()[0]}")
    
    