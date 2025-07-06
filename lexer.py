
import re

class TokenType:
    EOF = 'EOF'
    # Keywords
    FOSSIL = 'FOSSIL'   
    ROAR = 'ROAR'       
    GROW = 'GROW'       
    SHRINK = 'SHRINK'  
    HATCH = 'HATCH'     
    SPLIT = 'SPLIT'    
    HERD = 'HERD'       

    # Literals
    IDENTIFIER = 'IDENTIFIER'
    INTEGER = 'INTEGER'
    STRING = 'STRING'

    # Operators
    ASSIGN = 'ASSIGN'  
    LPAREN = 'LPAREN'  
    RPAREN = 'RPAREN'   
    SEMICOLON = 'SEMICOLON' 

class Token:
    def __init__(self, type, value, line=None, column=None):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __str__(self):
        return f'Token({self.type}, {repr(self.value)}, Line: {self.line}, Col: {self.column})'

    def __repr__(self):
        return self.__str__()

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if len(self.text) > 0 else None
        self.line = 1
        self.column = 1

        self.keywords = {
            'FOSSIL': TokenType.FOSSIL,
            'ROAR': TokenType.ROAR,
            'GROW': TokenType.GROW,
            'SHRINK': TokenType.SHRINK,
            'HATCH': TokenType.HATCH,
            'SPLIT': TokenType.SPLIT,
            'HERD': TokenType.HERD,
        }

    def _advance(self):
        if self.current_char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def _skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self._advance()

    def _skip_comment(self):
        while self.current_char is not None and self.current_char != '\n':
            self._advance()
        if self.current_char == '\n':
            self._advance()

    def _integer(self):
        result = ''
        start_column = self.column
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self._advance()
        return Token(TokenType.INTEGER, int(result), self.line, start_column)

    def _string(self):
        start_column = self.column
        self._advance() # Consume the opening quote
        result = ''
        while self.current_char is not None and self.current_char != '"':
            if self.current_char == '\\': 
                self._advance()
                if self.current_char == 'n':
                    result += '\n'
                elif self.current_char == 't':
                    result += '\t'
                elif self.current_char == '"':
                    result += '"'
                elif self.current_char == '\\':
                    result += '\\'
                else:
                    result += '\\' + self.current_char
            else:
                result += self.current_char
            self._advance()

        if self.current_char != '"':
            raise Exception(f"Lexer Error: Unterminated string literal at Line {self.line}, Col {start_column}")

        self._advance() # Consume the closing quote
        return Token(TokenType.STRING, result, self.line, start_column)

    def _identifier(self):
        result = ''
        start_column = self.column
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self._advance()
        token_type = self.keywords.get(result.upper(), TokenType.IDENTIFIER)
        return Token(token_type, result, self.line, start_column)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self._skip_whitespace()
                continue

            if self.current_char == '#': # Handle comments
                self._skip_comment()
                continue

            if self.current_char.isdigit():
                return self._integer()

            if self.current_char == '"':
                return self._string()

            if self.current_char.isalpha() or self.current_char == '_':
                return self._identifier()

            if self.current_char == '=':
                token = Token(TokenType.ASSIGN, self.current_char, self.line, self.column)
                self._advance()
                return token

            if self.current_char == '(':
                token = Token(TokenType.LPAREN, self.current_char, self.line, self.column)
                self._advance()
                return token

            if self.current_char == ')':
                token = Token(TokenType.RPAREN, self.current_char, self.line, self.column)
                self._advance()
                return token

            if self.current_char == ';':
                token = Token(TokenType.SEMICOLON, self.current_char, self.line, self.column)
                self._advance()
                return token

            raise Exception(f'Lexer Error: Unexpected character {self.current_char} at Line {self.line}, Col {self.column}')

        return Token(TokenType.EOF, None, self.line, self.column)




