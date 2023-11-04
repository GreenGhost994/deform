from dataclasses import dataclass, field

@dataclass
class Vertex:
    id: int
    x: float
    y: float
    comment: str = ""

@dataclass
class Line:
    id: int
    start: Vertex
    end: Vertex
    comment: str = ""

    @property
    def length(self) -> float:
        dx = self.end.x - self.start.x
        dy = self.end.y - self.start.y
        return (dx ** 2 + dy ** 2) ** 0.5

@dataclass
class Model:
    vertices: list = field(default_factory=lambda: [])
    lines: list = field(default_factory=lambda: [])

    def as_treeview(self):
        names = ['Vertices', 'Lines']
        moves = []
        counter = len(names)
        for i, x in enumerate(self.vertices):
            names.append(f'{x.id}: {x.x:.2f}, {x.y:.2f}')
            moves.append((counter, 0, i))
            counter += 1
        for i, x in enumerate(self.lines):
            names.append(f'{x.id}: {x.start.id}, {x.end.id} L={x.length:.2f}')
            moves.append((counter, 1, i))
            counter += 1
        return names, moves
    
    def get_item_by_treeview(self, id):
        counter = 1
        for i in self.__dict__.values():
            for j in i:
                counter += 1
                if id == counter:
                    return j

    def add(self, element: Vertex | Line) -> Vertex | Line:
        """
        Add element to model.
        """

        def new_id(element_list):
            if not element_list:
                return 0
            return max(element_list, key=lambda ele: ele.id).id + 1

        if type(element) == Vertex:
            if (existing := [x for x in self.vertices if x.x == element.x and x.y == element.y]):
                return existing[0]
            if not element.id:
                element.id = new_id(self.vertices)
            self.vertices.append(element)
        elif type(element) == Line:
            if not element.id:
                element.id = new_id(self.lines)
            self.lines.append(element)
        return element

    def delete(self, element):
        """
        Delete element and subelements from model.
        """
        if type(element) == Vertex:
            self.vertices.remove(element)
            self.lines = [line for line in self.lines if line.start != element and line.end != element]
        elif type(element) == Line:
            self.lines.remove(element)

    def edit(self, element):
        """
        Edit element properites.
        """
        if type(element) == Vertex:
            vertex_to_edit = next((vertex for vertex in self.vertices if vertex.id == element.id), None)
            if vertex_to_edit is not None:
                vertex_to_edit = element
        elif type(element) == Line:
            line_to_edit = next((line for line in self.vertices if line.id == element.id), None)
            if line_to_edit is not None:
                line_to_edit = element
