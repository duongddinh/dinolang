
from lexer import TokenType, Token

class AST:
    pass

class Program(AST):
    def __init__(self, statements):
        self.statements = statements

class VariableDeclaration(AST):
    def __init__(self, identifier, expression):
        self.identifier = identifier 
        self.expression = expression 

class BinaryOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op 
        self.right = right

class Number(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class String(AST):
    def __init__(self, token):
        self.token = token 
        self.value = token.value

class Identifier(AST):
    def __init__(self, token):
        self.token = token 
        self.name = token.value

class PrintStatement(AST):
    def __init__(self, expression):
        self.expression = expression # AST node for the value to print

class InputStatement(AST):
    def __init__(self, identifier):
        self.identifier = identifier

# Parser class
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def _error(self, message="Invalid syntax"):
        raise Exception(f'Parser Error: {message} at Line {self.current_token.line}, Col {self.current_token.column}. Current token: {self.current_token}')

    def _eat(self, token_type):

        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self._error(f"Expected token type {token_type}, got {self.current_token.type}")

    def _factor(self):

        token = self.current_token
        if token.type == TokenType.INTEGER:
            self._eat(TokenType.INTEGER)
            return Number(token)
        elif token.type == TokenType.STRING:
            self._eat(TokenType.STRING)
            return String(token)
        elif token.type == TokenType.IDENTIFIER:
            self._eat(TokenType.IDENTIFIER)
            return Identifier(token)
        elif token.type == TokenType.LPAREN:
            self._eat(TokenType.LPAREN)
            node = self._expr()
            self._eat(TokenType.RPAREN)
            return node
        else:
            self._error("Expected an integer, string, identifier, or '('")

    def _expr(self):

        token = self.current_token
        if token.type in (TokenType.GROW, TokenType.SHRINK, TokenType.HATCH, TokenType.SPLIT):
            op_token = token
            self._eat(op_token.type) # Consume the operator keyword
            left_operand = self._expr()
            right_operand = self._expr()
            return BinaryOp(left=left_operand, op=op_token, right=right_operand)
        else:
            return self._factor()

    def _variable_declaration_statement(self):

        self._eat(TokenType.FOSSIL)
        identifier_token = self.current_token
        self._eat(TokenType.IDENTIFIER)
        self._eat(TokenType.ASSIGN)
        expression_node = self._expr()
        self._eat(TokenType.SEMICOLON)
        return VariableDeclaration(identifier_token, expression_node)

    def _print_statement(self):

        self._eat(TokenType.ROAR)
        expression_node = self._expr()
        self._eat(TokenType.SEMICOLON)
        return PrintStatement(expression_node)

    def _input_statement(self):

        self._eat(TokenType.HERD)
        identifier_token = self.current_token
        self._eat(TokenType.IDENTIFIER)
        self._eat(TokenType.SEMICOLON)
        return InputStatement(identifier_token)

    def _statement(self):

        if self.current_token.type == TokenType.FOSSIL:
            return self._variable_declaration_statement()
        elif self.current_token.type == TokenType.ROAR:
            return self._print_statement()
        elif self.current_token.type == TokenType.HERD:
            return self._input_statement()
        else:
            self._error("Expected a variable declaration (FOSSIL), print statement (ROAR), or input statement (HERD)")

    def parse(self):

        statements = []
        while self.current_token.type != TokenType.EOF:
            statements.append(self._statement())
        return Program(statements)



