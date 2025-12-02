from dataclasses import dataclass
from typing import List, Optional
from Parser.ast import ASTNode


@dataclass
class Token:
    type: str     # tipo de token, ej: 'fish', 'ident', '<+', 'NUM', '<D', '{', '}', '(', ')', ','
    lexeme: str   # texto original
    line: int     # número de línea (para errores)


class ParseError(Exception):
    pass


class Parser:
    def __init__(self, tokens: List):
        # Convertir tuplas a objetos Token
        token_objects = []
        for i, token in enumerate(tokens):
            if isinstance(token, tuple):
                # token puede venir como (lexeme, type) o (lexeme, type, line)
                if len(token) == 3:
                    lexeme, token_type, line = token
                else:
                    lexeme, token_type = token
                    line = i + 1
                token_objects.append(Token(type=token_type, lexeme=lexeme, line=line))
            else:
                token_objects.append(token)

        # Agregamos token de fin de entrada $
        self.tokens = token_objects + [Token(type='$', lexeme='$', line=-1)]
        self.pos = 0

    # ---------------------------------------------
    # Utilidades básicas
    # ---------------------------------------------
    @property
    def current(self) -> Token:
        return self.tokens[self.pos]

    def advance(self) -> None:
        if self.pos < len(self.tokens) - 1:
            self.pos += 1

    def match(self, expected_type: str) -> None:
        if self.current.type == expected_type:
            self.advance()
        else:
            raise ParseError(
                f"[Línea {self.current.line}] "
                f"Se esperaba '{expected_type}' pero llegó '{self.current.type}'"
            )

    def check(self, *types: str) -> bool:
        return self.current.type in types

    # ---------------------------------------------
    # Entrada principal
    # ---------------------------------------------
    def parse(self) -> ASTNode:
        ast = self.program()
        if self.current.type != '$':
            raise ParseError(
                f"[Línea {self.current.line}] "
                f"Tokens extra después de finalizar PROGRAM: '{self.current.type}'"
            )
        return ast

    # ---------------------------------------------
    # PROGRAM → fish BLOCK
    # ---------------------------------------------
    def program(self) -> ASTNode:
        if self.current.type == 'fish':
            self.match('fish')
            block_node = self.block()
            return ASTNode('Program', children=[block_node], line=self.current.line)
        else:
            raise ParseError(
                f"[Línea {self.current.line}] "
                "PROGRAM debe iniciar con 'fish'"
            )

    # ---------------------------------------------
    # BLOCK → { DECLS_AND_STMTS }
    # ---------------------------------------------
    def block(self) -> ASTNode:
        if self.current.type == '{':
            self.match('{')
            items = self.decls_and_stmts()
            if self.current.type == '}':
                self.match('}')
                node = ASTNode('Block', children=items, line=self.current.line)
                return node
            else:
                raise ParseError(
                    f"[Línea {self.current.line}] "
                    "Falta '}' al cerrar BLOCK"
                )
        else:
            raise ParseError(
                f"[Línea {self.current.line}] "
                "Se esperaba '{' al iniciar un BLOCK"
            )

    # ---------------------------------------------
    # DECLS_AND_STMTS → ITEM DECLS_AND_STMTS | ε
    # ---------------------------------------------
    def decls_and_stmts(self) -> List[ASTNode]:
        items: List[ASTNode] = []
        while self.check('<int', '<string', '<charal', '<bubble', '<hook',
                         'fishtion', 'if', 'whale', 'fork', 'try',
                         'splash', 'emerge', '{', 'ident'):
            node = self.item()
            items.append(node)
        return items

    # ---------------------------------------------
    # ITEM → DECLARATION | FUNCTION_DEF | STATEMENT
    # ---------------------------------------------
    def item(self) -> ASTNode:
        if self.check('<int', '<string', '<charal', '<bubble', '<hook'):
            return self.declaration()
        elif self.current.type == 'fishtion':
            return self.function_def()
        elif self.check('if', 'whale', 'fork', 'try', 'splash', 'emerge',
                        '{', 'ident'):
            return self.statement()
        else:
            raise ParseError(
                f"[Línea {self.current.line}] "
                "Token inesperado al iniciar ITEM"
            )

    # ---------------------------------------------
    # DECLARATION → TYPE ident DECLARATION_TAIL
    # ---------------------------------------------
    def declaration(self) -> ASTNode:
        type_node = self.type_()
        if self.current.type == 'ident':
            name = self.current.lexeme
            self.match('ident')
            init = self.declaration_tail()
            node = ASTNode('Declaration', value=name, children=[type_node], line=self.current.line)
            if init:
                node.add(init)
            return node
        else:
            raise ParseError(
                f"[Línea {self.current.line}] "
                "Se esperaba 'ident' en DECLARATION"
            )

    # ---------------------------------------------
    # DECLARATION_TAIL → <= EXPR <D
    # ---------------------------------------------
    def declaration_tail(self) -> ASTNode:
        if self.current.type == '<=':
            self.match('<=')
            expr_node = self.expr()
            if self.current.type == '<D':
                self.match('<D')
                return ASTNode('Initializer', children=[expr_node], line=self.current.line)
            else:
                raise ParseError(
                    f"[Línea {self.current.line}] "
                    "Se esperaba '<D' al final de DECLARATION"
                )
        else:
            raise ParseError(
                f"[Línea {self.current.line}] "
                "Se esperaba '<=' en DECLARATION_TAIL"
            )

    # ---------------------------------------------
    # TYPE → <int | <string | <charal | <bubble | <hook
    # ---------------------------------------------
    def type_(self) -> ASTNode:
        if self.check('<int', '<string', '<charal', '<bubble', '<hook'):
            t = self.current.type
            self.advance()
            return ASTNode('Type', value=t, line=self.current.line)
        else:
            raise ParseError(
                f"[Línea {self.current.line}] "
                "Tipo inválido en TYPE"
            )

    # ---------------------------------------------
    # FUNCTION_DEF → fishtion ident ( PARAMS ) TYPE BLOCK
    # ---------------------------------------------
    def function_def(self) -> ASTNode:
        self.match('fishtion')
        if self.current.type != 'ident':
            raise ParseError(f"[Línea {self.current.line}] Se esperaba nombre de funcion")
        name = self.current.lexeme
        self.match('ident')
        self.match('(')
        params_node = self.params()
        self.match(')')
        ret_type = self.type_()
        block_node = self.block()
        node = ASTNode('FunctionDef', value=name, children=[params_node, ret_type, block_node], line=self.current.line)
        return node

    # ---------------------------------------------
    # PARAMS → PARAM PARAMS' | ε
    # ---------------------------------------------
    def params(self) -> ASTNode:
        params = []
        if self.check('<int', '<string', '<charal', '<bubble', '<hook'):
            params.append(self.param())
            params.extend(self.params_p())
        elif self.current.type == ')':
            pass
        else:
            raise ParseError(
                f"[Línea {self.current.line}] "
                "Token inesperado en PARAMS"
            )
        return ASTNode('Params', children=params, line=self.current.line)

    # ---------------------------------------------
    # PARAMS' → , PARAM PARAMS' | ε
    # ---------------------------------------------
    def params_p(self) -> List[ASTNode]:
        params = []
        while self.current.type == ',':
            self.match(',')
            params.append(self.param())
        return params

    # ---------------------------------------------
    # PARAM → TYPE ident
    # ---------------------------------------------
    def param(self) -> ASTNode:
        t = self.type_()
        if self.current.type != 'ident':
            raise ParseError(f"[Línea {self.current.line}] Se esperaba identificador en PARAM")
        name = self.current.lexeme
        self.match('ident')
        return ASTNode('Param', value=name, children=[t], line=self.current.line)

    # ---------------------------------------------
    # STATEMENT → IF_ELSE | WHILE_LOOP | FOR_LOOP
    #           | TRY_CATCH | PRINT_STMT | RETURN_STMT
    #           | BLOCK | IDENT_STMT
    # ---------------------------------------------
    def statement(self) -> ASTNode:
        if self.current.type == 'if':
            return self.if_else()
        elif self.current.type == 'whale':
            return self.while_loop()
        elif self.current.type == 'fork':
            return self.for_loop()
        elif self.current.type == 'try':
            return self.try_catch()
        elif self.current.type == 'splash':
            return self.print_stmt()
        elif self.current.type == 'emerge':
            return self.return_stmt()
        elif self.current.type == '{':
            return self.block()
        elif self.current.type == 'ident':
            return self.ident_stmt()
        else:
            raise ParseError(
                f"[Línea {self.current.line}] "
                "Token inesperado al iniciar STATEMENT"
            )

    # ---------------------------------------------
    # IDENT_STMT → ident IDENT_TAIL
    # ---------------------------------------------
    def ident_stmt(self) -> ASTNode:
        name = self.current.lexeme
        self.match('ident')
        # Distinguish call vs assign vs inc/dec
        if self.current.type == '(':
            self.match('(')
            args = self.args()
            self.match(')')
            self.match('<D')
            return ASTNode('CallStmt', value=name, children=[args], line=self.current.line)
        elif self.current.type == '<=':
            self.match('<=')
            expr = self.expr()
            self.match('<D')
            return ASTNode('Assign', value=name, children=[expr], line=self.current.line)
        elif self.current.type == '<++':
            self.match('<++')
            self.match('<D')
            return ASTNode('Inc', value=name, line=self.current.line)
        elif self.current.type == '<--':
            self.match('<--')
            self.match('<D')
            return ASTNode('Dec', value=name, line=self.current.line)
        else:
            raise ParseError(f"[Línea {self.current.line}] Forma inválida de IDENT_STMT")

    def ident_tail(self) -> None:
        # Left for compatibility; not used now because ident_stmt handles cases
        return None

    # ---------------------------------------------
    # ARGS → EXPR ARGS' | ε
    # ---------------------------------------------
    def args(self) -> ASTNode:
        args = []
        if self.check('<+', '<-', 'ident', 'NUM',
                      'STRING_LITERAL', 'CHAR_LITERAL', '('):
            args.append(self.expr())
            args.extend(self.args_p())
        elif self.current.type == ')':
            pass
        else:
            raise ParseError(
                f"[Línea {self.current.line}] "
                "Token inesperado en ARGS"
            )
        return ASTNode('Args', children=args, line=self.current.line)

    # ---------------------------------------------
    # ARGS' → , EXPR ARGS' | ε
    # ---------------------------------------------
    def args_p(self) -> List[ASTNode]:
        args = []
        while self.current.type == ',':
            self.match(',')
            args.append(self.expr())
        return args

    # ---------------------------------------------
    # IF_ELSE → if ( EXPR ) BLOCK ELSE_PART
    # ELSE_PART → else BLOCK | ε
    # ---------------------------------------------
    def if_else(self) -> ASTNode:
        self.match('if')
        self.match('(')
        cond = self.expr()
        self.match(')')
        then_block = self.block()
        else_block = self.else_part()
        
        if else_block:
            return ASTNode('If', children=[cond, then_block, else_block], line=self.current.line)
        else:
            return ASTNode('If', children=[cond, then_block], line=self.current.line)
    
    # ---------------------------------------------
    # ELSE_PART → else BLOCK | ε
    # ---------------------------------------------
    def else_part(self) -> Optional[ASTNode]:
        if self.current.type == 'else':
            self.match('else')
            return self.block()
        else:
            return None

    # ---------------------------------------------
    # WHILE_LOOP → whale ( EXPR ) BLOCK
    # ---------------------------------------------
    def while_loop(self) -> ASTNode:
        self.match('whale')
        self.match('(')
        cond = self.expr()
        self.match(')')
        block = self.block()
        return ASTNode('While', children=[cond, block], line=self.current.line)

    # ---------------------------------------------
    # FOR_LOOP → fork ( FOR_INIT <D FOR_COND <D FOR_STEP ) BLOCK
    # ---------------------------------------------
    def for_loop(self) -> ASTNode:
        self.match('fork')
        self.match('(')
        init = self.for_init()
        self.match('<D')
        cond = self.for_cond()
        self.match('<D')
        step = self.for_step()
        self.match(')')
        block = self.block()
        return ASTNode('For', children=[init or ASTNode('Empty'), cond or ASTNode('Empty'), step or ASTNode('Empty'), block], line=self.current.line)

    # ---------------------------------------------
    # FOR_INIT → DECL_NO_DELIM | ASSIGN_NO_DELIM | ε
    # ---------------------------------------------
    def for_init(self) -> Optional[ASTNode]:
        if self.check('<int', '<string', '<charal', '<bubble', '<hook'):
            return self.decl_no_delim()
        elif self.current.type == 'ident':
            return self.assign_no_delim()
        elif self.current.type == '<D':
            return None
        else:
            raise ParseError(
                f"[Línea {self.current.line}] "
                "Token inesperado en FOR_INIT"
            )

    # ---------------------------------------------
    # FOR_COND → EXPR | ε
    # ---------------------------------------------
    def for_cond(self) -> Optional[ASTNode]:
        if self.check('<+', '<-', 'ident', 'NUM',
                      'STRING_LITERAL', 'CHAR_LITERAL', '('):
            return self.expr()
        elif self.current.type == '<D':
            return None
        else:
            raise ParseError(
                f"[Línea {self.current.line}] "
                "Token inesperado en FOR_COND"
            )

    # ---------------------------------------------
    # FOR_STEP → ident FOR_STEP_TAIL | ε
    # ---------------------------------------------
    def for_step(self) -> Optional[ASTNode]:
        if self.current.type == 'ident':
            name = self.current.lexeme
            self.match('ident')
            tail = self.for_step_tail()
            node = ASTNode('ForStep', value=name, children=[tail] if tail else [], line=self.current.line)
            return node
        elif self.current.type == ')':
            return None
        else:
            raise ParseError(
                f"[Línea {self.current.line}] "
                "Token inesperado en FOR_STEP"
            )

    # ---------------------------------------------
    # FOR_STEP_TAIL → <++ | <-- | <= EXPR
    # ---------------------------------------------
    def for_step_tail(self) -> ASTNode:
        if self.current.type == '<++':
            self.match('<++')
            return ASTNode('Postfix', value='<++', line=self.current.line)
        elif self.current.type == '<--':
            self.match('<--')
            return ASTNode('Postfix', value='<--', line=self.current.line)
        elif self.current.type == '<=':
            self.match('<=')
            expr = self.expr()
            return ASTNode('AssignTo', children=[expr], line=self.current.line)
        else:
            raise ParseError(
                f"[Línea {self.current.line}] "
                "Token inválido en FOR_STEP_TAIL"
            )

    # ---------------------------------------------
    # DECL_NO_DELIM → TYPE ident <= EXPR
    # ---------------------------------------------
    def decl_no_delim(self) -> ASTNode:
        t = self.type_()
        if self.current.type != 'ident':
            raise ParseError(f"[Línea {self.current.line}] Se esperaba ident en DECL_NO_DELIM")
        name = self.current.lexeme
        self.match('ident')
        self.match('<=')
        expr = self.expr()
        return ASTNode('Declaration', value=name, children=[t, expr], line=self.current.line)

    # ---------------------------------------------
    # ASSIGN_NO_DELIM → ident <= EXPR
    #                  | ident <--
    # ---------------------------------------------
    def assign_no_delim(self) -> ASTNode:
        name = self.current.lexeme
        self.match('ident')
        if self.current.type == '<=':
            self.match('<=')
            expr = self.expr()
            return ASTNode('Assign', value=name, children=[expr], line=self.current.line)
        elif self.current.type == '<--':
            self.match('<--')
            return ASTNode('Dec', value=name, line=self.current.line)
        else:
            raise ParseError(
                f"[Línea {self.current.line}] "
                "ASSIGN_NO_DELIM espera '<=' o '<--' después de ident"
            )

    # ---------------------------------------------
    # TRY_CATCH → try BLOCK catch BLOCK TRY_CATCH_TAIL
    # ---------------------------------------------
    def try_catch(self) -> ASTNode:
        self.match('try')
        try_block = self.block()
        self.match('catch')
        catch_block = self.block()
        tail = self.try_catch_tail()
        node = ASTNode('TryCatch', children=[try_block, catch_block], line=self.current.line)
        if tail:
            node.add(tail)
        return node

    # ---------------------------------------------
    # TRY_CATCH_TAIL → finally BLOCK | ε
    # ---------------------------------------------
    def try_catch_tail(self) -> Optional[ASTNode]:
        if self.current.type == 'finally':
            self.match('finally')
            finally_block = self.block()
            return ASTNode('Finally', children=[finally_block], line=self.current.line)
        else:
            return None

    # ---------------------------------------------
    # PRINT_STMT → splash ( EXPR ) <D
    # ---------------------------------------------
    def print_stmt(self) -> ASTNode:
        self.match('splash')
        self.match('(')
        expr = self.expr()
        self.match(')')
        self.match('<D')
        return ASTNode('Print', children=[expr], line=self.current.line)

    # ---------------------------------------------
    # RETURN_STMT → emerge EXPR <D
    # ---------------------------------------------
    def return_stmt(self) -> ASTNode:
        self.match('emerge')
        expr = self.expr()
        self.match('<D')
        return ASTNode('Return', children=[expr], line=self.current.line)

    # ---------------------------------------------
    # EXPR → EQUALITY
    # ---------------------------------------------
    def expr(self) -> ASTNode:
        return self.equality()

    # ---------------------------------------------
    # EQUALITY → RELATIONAL ( (<==|<!=) RELATIONAL )*
    # ---------------------------------------------
    def equality(self) -> ASTNode:
        node = self.relational()
        while self.current.type in ('<==', '<!='):
            op = self.current.type
            self.advance()
            right = self.relational()
            node = ASTNode('BinaryOp', value=op, children=[node, right], line=self.current.line)
        return node

    # ---------------------------------------------
    # RELATIONAL → ADD ( << | <<> | <<= | <<>= )*
    # ---------------------------------------------
    def relational(self) -> ASTNode:
        node = self.add()
        while self.current.type in ('<<', '<<>', '<<=', '<<>='):
            op = self.current.type
            self.advance()
            right = self.add()
            node = ASTNode('BinaryOp', value=op, children=[node, right], line=self.current.line)
        return node

    # ---------------------------------------------
    # ADD → MUL ( (<+|<-) MUL )*
    # ---------------------------------------------
    def add(self) -> ASTNode:
        node = self.mul()
        while self.current.type in ('<+', '<-'):
            op = self.current.type
            self.advance()
            right = self.mul()
            node = ASTNode('BinaryOp', value=op, children=[node, right], line=self.current.line)
        return node

    # ---------------------------------------------
    # MUL → UNARY ( (<*|</|<%) UNARY )*
    # ---------------------------------------------
    def mul(self) -> ASTNode:
        node = self.unary()
        while self.current.type in ('<*', '</', '<%'):
            op = self.current.type
            self.advance()
            right = self.unary()
            node = ASTNode('BinaryOp', value=op, children=[node, right], line=self.current.line)
        return node

    # ---------------------------------------------
    # UNARY → <+ UNARY | <- UNARY | POSTFIX
    # ---------------------------------------------
    def unary(self) -> ASTNode:
        if self.current.type == '<+':
            op = self.current.type
            self.match('<+')
            operand = self.unary()
            return ASTNode('UnaryOp', value=op, children=[operand], line=self.current.line)
        elif self.current.type == '<-':
            op = self.current.type
            self.match('<-')
            operand = self.unary()
            return ASTNode('UnaryOp', value=op, children=[operand], line=self.current.line)
        elif self.check('ident', 'NUM', 'STRING_LITERAL', 'CHAR_LITERAL', '('):
            return self.postfix()
        else:
            raise ParseError(
                f"[Línea {self.current.line}] "
                f"Token inesperado en UNARY: '{self.current.type}' (lexema: '{self.current.lexeme}')"
            )

    # ---------------------------------------------
    # POSTFIX → PRIMARY ( <++ | <-- )*
    # ---------------------------------------------
    def postfix(self) -> ASTNode:
        node = self.primary()
        while self.current.type in ('<++', '<--'):
            op = self.current.type
            self.advance()
            node = ASTNode('PostfixOp', value=op, children=[node], line=self.current.line)
        return node

    # ---------------------------------------------
    # PRIMARY → ident (ARGS)? | NUM | STRING_LITERAL | CHAR_LITERAL | ( EXPR )
    # ---------------------------------------------
    def primary(self) -> ASTNode:
        if self.current.type == 'ident':
            name = self.current.lexeme
            self.match('ident')
            if self.current.type == '(':
                self.match('(')
                args = self.args()
                self.match(')')
                return ASTNode('Call', value=name, children=[args], line=self.current.line)
            else:
                return ASTNode('Var', value=name, line=self.current.line)
        elif self.current.type == 'NUM':
            val = self.current.lexeme
            self.match('NUM')
            return ASTNode('Num', value=val, line=self.current.line)
        elif self.current.type == 'STRING_LITERAL':
            val = self.current.lexeme
            self.match('STRING_LITERAL')
            return ASTNode('String', value=val, line=self.current.line)
        elif self.current.type == 'CHAR_LITERAL':
            val = self.current.lexeme
            self.match('CHAR_LITERAL')
            return ASTNode('Char', value=val, line=self.current.line)
        elif self.current.type == '(':
            self.match('(')
            node = self.expr()
            self.match(')')
            return node
        else:
            raise ParseError(
                f"[Línea {self.current.line}] "
                "Token inesperado en PRIMARY"
            )

    def primary_id(self) -> None:
        # deprecated; handled in primary
        return None
