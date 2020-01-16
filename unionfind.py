class Node:
    def __init__(self, id):
        self.id = id
        self.parent = None
    
    def __repr__(self):
        if self.parent == None:
            added = " Root"
        else:
            added = " " + str(self.parent.id)
        return str(self.id) + added

    def find(self) -> 'Node':
        if self.parent == None:
            return self
        else:
            return self.parent.find()

    def unite(self, other: 'Node'):
        p1, p2 = self.find(), other.find()
        if not p1 == p2:
            p2.parent = p1