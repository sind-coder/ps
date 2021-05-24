class Three:
    def __init__(self, name, children):
        self.name = name
        self.children = children

    def children_str(self):
        st = []
        for child in self.children:
            st.append( str(child) )
        return "\n".join(st)

    def add_children(self, children):
        self.children = self.children + children
        return self

    def __repr__(self):
        return self.name + ":\n" + self.children_str().replace("\n", "\n   ")
