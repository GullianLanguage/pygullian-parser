from enum import Enum
from dataclasses import dataclass

from .source import Source

class BaseKind:
    value: str

    def __hash__(self):
        return hash(self.value)
    
    def __eq__(self, value: str):
        return self.value == value

class TokenKind(BaseKind, Enum):
    LeftParenthesis=        '('
    RightParenthesis=       ')'
    LeftBrace=              '{'
    RightBrace=             '}'
    LeftBracket=            '['
    RightBracket=           ']'
    Dot=                    '.'
    Comma=                  ','
    Exclamation=            '!'
    Interrogation=          '?'
    Colon=                  ':'
    Semicolon=              ';'
    Equal=                  '='
    GreaterThan=            '>'
    LessThan=               '<'
    Plus=                   '+'
    Minus=                  '-'
    Star=                   '*'
    StarStar=               '**'
    Slash=                  '/'
    Percent=                '%'
    Ampersand=              '&'
    Caret=                  '^'
    VerticalBar=            '|'
    Left=                   '>>'
    Right=                  '<<'
    NotEqual=               '!='
    EqualEqual=             '=='
    GreaterThanEqual=       '>='
    LessThanEqual=          '<='
    PlusEqual=              '+='
    MinusEqual=             '-='
    StarEqual=              '*='
    StarStarEqual=          '**='
    SlashEqual=             '/='
    PercentEqual=           '%='
    AmpersandEqual=         '&='
    CaretEqual=             '^='
    VerticalBarEqual=       '|='
    LeftEqual=              '>>='
    RightEqual=             '<<='

TOKENKIND_SORTED = sorted(TokenKind.__members__.values(), key=lambda member: len(member.value), reverse=True)

TOKENKIND_UNARYOPERATORS = {
    TokenKind.Interrogation,
    TokenKind.Plus,
    TokenKind.Minus,
    TokenKind.Star,
    TokenKind.Ampersand,
}

TOKENKIND_BINARYOPERATORS = {
    TokenKind.GreaterThan,
    TokenKind.LessThan,
    TokenKind.Plus,
    TokenKind.Minus,
    TokenKind.Star,
    TokenKind.StarStar,
    TokenKind.Slash,
    TokenKind.Percent,
    TokenKind.Ampersand,
    TokenKind.Caret,
    TokenKind.VerticalBar,
    TokenKind.Left,  
    TokenKind.Right,
    TokenKind.NotEqual,
    TokenKind.EqualEqual,
    TokenKind.GreaterThanEqual,
    TokenKind.LessThanEqual,
}

TOKENKIND_ASSIGNMENTOPERATORS = {
    TokenKind.Equal,
    TokenKind.PlusEqual,
    TokenKind.MinusEqual,
    TokenKind.StarEqual,
    TokenKind.StarStarEqual,
    TokenKind.SlashEqual,
    TokenKind.PercentEqual,
    TokenKind.AmpersandEqual,
    TokenKind.CaretEqual,
    TokenKind.VerticalBarEqual,
    TokenKind.LeftEqual,
    TokenKind.RightEqual
}

TOKENKIND_NUMERICOPERATORS = {
    TokenKind.Plus,
    TokenKind.Minus,
    TokenKind.Star,
    TokenKind.StarStar,
    TokenKind.Slash,
    TokenKind.Percent,
    TokenKind.Ampersand,
    TokenKind.Caret,
    TokenKind.VerticalBar,
    TokenKind.Left,  
    TokenKind.Right,
}

TOKENKIND_LOGICOPERATORS = {
    TokenKind.GreaterThan,
    TokenKind.LessThan,
    TokenKind.NotEqual,
    TokenKind.EqualEqual,
    TokenKind.GreaterThanEqual,
    TokenKind.LessThanEqual,
}

@dataclass
class Token:
    kind: TokenKind
    line: int

    @property
    def format(self):
        return self.kind.value

class KeywordKind(BaseKind, Enum):
    Extern=                 'extern'
    Import=                 'import'
    Struct=                 'struct'
    Enum=                   'enum'
    Union=                  'union'
    Let=                    'let'
    Fun=                    'fun'
    Return=                 'return'
    While=                  'while'
    Break=                  'break'
    Continue=               'continue'
    If=                     'if'
    Else=                   'else'
    Elif=                   'elif'
    Comptime=               'comptime'
    Not=                    'not'
    And=                    'and'
    Or=                     'or'

KEYWORDKIND_SORTED = sorted(KeywordKind.__members__.values(), key=lambda member: len(member.value))

@dataclass
class Keyword:
    kind: TokenKind
    line: int

    @property
    def format(self):
        return self.kind.value

@dataclass
class Comment:
    value: str
    line: int

    @property
    def format(self):
        return f'#{self.value}'

@dataclass(repr=False)
class Name:
    value: str
    line: int=-1

    def __hash__(self):
        return hash(self.value)
    
    def __eq__(self, value: str):
        return self.value == value
    
    def __repr__(self):
        return self.value

    @property
    def format(self):
        return self.value

@dataclass(repr=False)
class Literal:
    value: bool | int | float | str
    line: int

    def __repr__(self):
        return repr(self.value)
    
    def __hash__(self):
        return hash(self.value)
    
    @property
    def format(self):
        return repr(self.value)

@dataclass
class Lexer:
    source: Source
    module_name: str='main'
    line: int=1

    def scan_comment(self) -> Comment:
        value = str()

        for char in self.source:
            if char == '\n':
                break
            else:
                value += char
        
        return Comment(value.strip(), self.line)
    
    def scan_numeric_literal(self, value: str):
        char = '.'

        for char in self.source:
            if char >= '0' and char <= '9':
                value += char
            else:
                self.source.release()
                break
        
        if char == '.':
            value += self.source.capture()
            
            for char in self.source:
                if char >= '0' and char <= '9':
                    value += char
                else:
                    self.source.release()
                    break
            
            return Literal(float(value), self.line)
        
        return Literal(int(value), self.line)
    
    def scan_text_literal(self, quote: str) -> Literal:
        value = str()

        for char in self.source:
            if char == '\\':
                value += self.source.capture()
                continue

            if char == quote:
                break

            value += char
        
        return Literal(value, self.line)
    
    def scan_name(self, value: str) -> Literal:
        for char in self.source:
            if char == '_' or char >= 'a' and char <= 'z' or char >= 'A' and char <= 'Z' or char >= '0' and char <= '9':
                value += char
            else:
                self.source.release()
                break
        
        return Name(value, self.line)
    
    def scan_token(self):
        self.source.release()

        for tokenkind in TOKENKIND_SORTED:
            if self.source.capture(len(tokenkind.value)) == tokenkind.value:
                return Token(tokenkind, self.line)
            
            self.source.release(len(tokenkind.value))
        
        raise SyntaxError(f"invalid token {self.source.capture()!r}. at line {self.line} in module {self.module_name}")

    def lex(self):
        for char in self.source:
            if char == '\n':
                self.line += 1
                continue
            elif char == ' ':
                continue
            
            if char == '#':
                yield self.scan_comment()
            elif char >= 'a' and char <= 'z':
                name = self.scan_name(char)

                if name.value in KEYWORDKIND_SORTED:
                    yield Keyword(KeywordKind(name.value), self.line)
                else:
                    yield name
            elif char >= 'A' and char <= 'Z' or char == '_':
                yield self.scan_name(char)
            elif char >= '0' and char <= '9':
                yield self.scan_numeric_literal(char)
            elif char == '"' or char == "'":
                yield self.scan_text_literal(char)
            else:
                yield self.scan_token()
        
        return self