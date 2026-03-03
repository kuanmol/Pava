from node import NumberNode, VarAssignNode, VarAccessNode, PrintNode


class Interpreter:
    def __init__(self):
        self.variables = {}

    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        raise Exception(f"No visit_{type(node).__name__} method define")

    def visit_NumberNode(self, node):
        return node.value

    def visit_VarAssignNode(self, node):
        value = self.visit(node.value)
        self.variables[node.name] = value
        return value

    def visit_VarAccessNode(self, node):
        if node.name not in self.variables:
            raise Exception(f"Variable {node.name} does not exist")
        return self.variables[node.name]

    def visit_PrintNode(self, node):
        value = self.visit(node.value)
        print(value)
        return value

    def visit_BinOpNode(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        if node.op == 'PLUS':
            return left + right
        elif node.op == 'MINUS':
            return left - right
        elif node.op == 'MUL':
            return left * right
        elif node.op == 'DIV':
            return left / right
