import re

TOKEN_SPEC = [
    ('NUMBER', r'\d+'),
    ('LET', r'let'),
    ('PRINT', r'print'),
    ('IDENT', r'[A-Za-z_][A-Za-z0-9_]*'),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('MUL', r'\*'),
    ('DIV', r'/'),
    ('EQUALS', r'='),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('COMMA', r','),
    ('COLON', r':'),
    ('SKIP', r'[ \t\n]+'),  # ← add \n here
    ('MISMATCH', r'.'),
]


class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"{self.type}({self.value})"


def lex(code):
    tokens = []
    code = code + "\n"
    pos = 0
    while pos < len(code):
        match = None
        for token_type, token_regex in TOKEN_SPEC:
            pattern = re.compile(token_regex)
            match = pattern.match(code, pos)
            if match:
                text = match.group(0)
                if token_type == 'SKIP':
                    # just skip, do nothing
                    pos = match.end(0)
                    break
                elif token_type == 'NUMBER':
                    tokens.append(Token('NUMBER', int(text)))
                elif token_type == 'IDENT':
                    tokens.append(Token("IDENTIFIER", text))
                elif token_type in ['LET', 'PRINT', 'PLUS', 'MINUS', 'MUL', 'DIV',
                                    'EQUALS', 'LPAREN', 'RPAREN', 'COMMA', 'COLON']:
                    tokens.append(Token(token_type, text))
                # no MISMATCH handling yet – add later if needed
                pos = match.end(0)
                break
        if not match:
            raise SyntaxError(f'Illegal character {code[pos]!r} at position {pos}')
    return tokens


if __name__ == '__main__':
    code = """
let x = 10
print(x)
"""
    tokens = lex(code)
    print(tokens)
