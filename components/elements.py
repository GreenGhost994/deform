from dataclasses import dataclass, field

@dataclass
class Vertex:
    id: int
    x: float
    y: float
    comment: str = ""

@dataclass
class Bar:
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
class LoadCase:
    id: int
    name: str = ""

@dataclass
class Load:
    id: int
    comment: str = ""

@dataclass
class Support:
    id: int
    comment: str = ""

@dataclass
class Section:
    id: int
    name: str = ""

@dataclass
class Material:
    id: int
    name: str = ""

@dataclass
class Model:
    vertices: list = field(default_factory=lambda: [])
    bars: list = field(default_factory=lambda: [])
    sections: list = field(default_factory=lambda: [])
    load_cases: list = field(default_factory=lambda: [])
    loads: list = field(default_factory=lambda: [])
    supports: list = field(default_factory=lambda: [])
    materials: list = field(default_factory=lambda: [])

    def as_treeview(self):
        names = ['Vertices', 'Bars', 'Sections', 'Materials']
        moves = []
        counter = len(names)
        for i, x in enumerate(self.vertices):
            names.append(f'{x.id}: {x.x:.2f}, {x.y:.2f}')
            moves.append((counter, 0, i))
            counter += 1
        for i, x in enumerate(self.bars):
            names.append(f'{x.id}: {x.start.id}, {x.end.id} L={x.length:.2f}')
            moves.append((counter, 1, i))
            counter += 1
        for i, x in enumerate(self.sections):
            names.append(f'{x.id}: {x.name}')
            moves.append((counter, 1, i))
            counter += 1
        for i, x in enumerate(self.materials):
            names.append(f'{x.id}: {x.name}')
            moves.append((counter, 1, i))
            counter += 1
        return names, moves
    
    def get_item_by_treeview(self, id):
        counter = 3
        for i in self.__dict__.values():
            for j in i:
                counter += 1
                if id == counter:
                    return j

    def add(self, element: Vertex | Bar) -> Vertex | Bar:
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
        elif type(element) == Bar:
            if not element.id:
                element.id = new_id(self.bars)
            self.bars.append(element)
        return element

    def delete(self, element):
        """
        Delete element and subelements from model.
        """
        if type(element) == Vertex:
            self.vertices.remove(element)
            self.bars = [bar for bar in self.bars if bar.start != element and bar.end != element]
        elif type(element) == Bar:
            self.bars.remove(element)

    def edit(self, element):
        """
        Edit element properites.
        """
        if type(element) == Vertex:
            vertex_to_edit = next((vertex for vertex in self.vertices if vertex.id == element.id), None)
            if vertex_to_edit is not None:
                vertex_to_edit = element
        elif type(element) == Bar:
            bar_to_edit = next((bar for bar in self.vertices if bar.id == element.id), None)
            if bar_to_edit is not None:
                bar_to_edit = element
