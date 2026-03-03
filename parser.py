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
        self.eat('LPARN')
        value = self.parse_expr()
        self.eat('RPARN')
        return PrintNode(value)

    def parse_expr(self):
        token = self.current_token()
        if token.type == "NUMBER":
            self.eat('NUMBER')
            return NumberNode(token.value)
        elif token.type == "IDENTIFIER":
            self.eat('IDENTIFIER')
            return VarAssignNode(token.value)
        else:
            raise Exception(f"Unexpected token {token}")
