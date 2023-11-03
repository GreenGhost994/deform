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

@dataclass
class Model:
    vertices: list = field(default_factory=lambda: [])
    lines: list = field(default_factory=lambda: [])

    def as_treeview(self):
        names = ['Vertices', 'Lines']
        moves = []
        counter = len(names)
        for i, x in enumerate(self.vertices):
            names.append(f'{x.id}: {x.x},{x.y}')
            moves.append((counter, 0, i))
            counter += 1
        for i, x in enumerate(self.lines):
            names.append(f'{x.id}: ')
            moves.append((counter, 0, i))
            counter += 1
        return names, moves
    
    def get_item_by_treeview(self, id):
        counter = 1
        for i in self.__dict__.values():
            for j in i:
                counter += 1
                if id == counter:
                    return j
