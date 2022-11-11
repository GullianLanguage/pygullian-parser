from gullian_parser.source import Source
from gullian_parser.lexer import Lexer
from gullian_parser.parser import Parser

hello_world = Source(open('examples/hello_world.gullian').read())
tokens = tuple(Lexer(hello_world).lex())
asts = tuple(Parser(Source(tokens)).parse())

for ast in asts:
    print(ast)