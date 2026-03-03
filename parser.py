from node import *


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def eat(self, token_type):
        if self.current_token() and self.current_token().type == token_type:
            self.pos += 1
        else:
            raise Exception(f"Expected {token_type} but got {self.current_token()}")

    def parse(self):
        statements = []
        while self.current_token() is not None:
            if self.current_token().type == "LET":
                statements.append(self.parse_var_assign())
            elif self.current_token().type == "PRINT":
                statements.append(self.parse_print())
            else:
                raise Exception(f"Unexpected token {self.current_token()}")
        return statements

    def parse_var_assign(self):
        self.eat('LET')
        var_name = self.current_token().value
        self.eat('IDENTIFIER')
        self.eat('EQUALS')
        value = self.parse_expr()
        return VarAssignNode(var_name, value)

    def parse_print(self):
        self.eat('PRINT')
        self.eat('LPAREN')

        values = []

        # Must have at least one argument
        if self.current_token() is None or self.current_token().type == 'RPAREN':
            raise Exception("print() requires at least one argument")

        # Parse first expression
        values.append(self.parse_expr())

        # Then: zero or more   COMMA expression
        while self.current_token() and self.current_token().type == 'COMMA':
            self.eat('COMMA')
            values.append(self.parse_expr())

        # Must end with )
        if self.current_token() is None or self.current_token().type != 'RPAREN':
            raise Exception(f"Expected ) but got {self.current_token()}")

        self.eat('RPAREN')

        return PrintNode(values)

    def parse_expr(self):
        left = None
        token = self.current_token()

        # First term: number or variable
        if token.type == 'NUMBER':
            self.eat('NUMBER')
            left = NumberNode(token.value)
        elif token.type == 'IDENTIFIER':
            self.eat('IDENTIFIER')
            left = VarAccessNode(token.value)
        else:
            raise Exception(f"Unexpected token in expression: {token}")

        # Check for operator
        while self.current_token() and self.current_token().type in ('PLUS', 'MINUS', 'MUL', 'DIV'):
            op_token = self.current_token()
            self.eat(op_token.type)
            right = self.parse_expr()  # recursive call for right-hand side
            left = BinOpNode(left, op_token.type, right)

        return left
