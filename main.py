from lexer import lex
from parser import Parser
from interpreter import Interpreter

code = """
let x = 10
let y = 5
print(x)
print(y)
print(x + y)
"""

tokens = lex(code)
parser = Parser(tokens)
ast = parser.parse()

interpreter = Interpreter()
for node in ast:
    interpreter.visit(node)
