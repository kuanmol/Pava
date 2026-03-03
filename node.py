class NumberNode:
    def __init__(self, value):
        self.value = value


class VarAssignNode:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class VarAccessNode:
    def __init__(self, name):
        self.name = name


class PrintNode:
    def __init__(self, value):
        self.value = value
