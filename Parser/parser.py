from dataclasses import dataclass
from typing import List


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
                lexeme, token_type = token
                token_objects.append(Token(type=token_type, lexeme=lexeme, line=i+1))
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
    def parse(self) -> None:
        self.program()
        if self.current.type != '$':
            raise ParseError(
                f"[Línea {self.current.line}] "
                f"Tokens extra después de finalizar PROGRAM: '{self.current.type}'"
            )

    # ---------------------------------------------
    # PROGRAM → fish BLOCK
    # ---------------------------------------------
    def program(self) -> None:
        if self.current.type == 'fish':
            self.match('fish')
            self.block()
        else:
            raise ParseError(
                f"[Línea {self.current.line}] "
                "PROGRAM debe iniciar con 'fish'"
            )

    # ---------------------------------------------
    # BLOCK → { DECLS_AND_STMTS }
    # ---------------------------------------------
    def block(self) -> None:
        if self.current.type == '{':
            self.match('{')
            self.decls_and_stmts()
            if self.current.type == '}':
                self.match('}')
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
    # FIRST = { <int, <string, <charal, <bubble, <hook,
    #           fishtion, if, whale, fork, try, splash, emerge, {, ident, ε }
    # FOLLOW = { } }
    # ---------------------------------------------
    def decls_and_stmts(self) -> None:
        if self.check('<int', '<string', '<charal', '<bubble', '<hook',
                      'fishtion', 'if', 'whale', 'fork', 'try',
                      'splash', 'emerge', '{', 'ident'):
            self.item()
            self.decls_and_stmts()
        elif self.current.type == '}':
            # ε
            return
        else:
            raise ParseError(
                f"[Línea {self.current.line}] "
                "Token inesperado en DECLS_AND_STMTS"
            )

    # ---------------------------------------------
    # ITEM → DECLARATION | FUNCTION_DEF | STATEMENT
    # ---------------------------------------------
    def item(self) -> None:
        if self.check('<int', '<string', '<charal', '<bubble', '<hook'):
            self.declaration()
        elif self.current.type == 'fishtion':
            self.function_def()
        elif self.check('if', 'whale', 'fork', 'try', 'splash', 'emerge',
                        '{', 'ident'):
            self.statement()
        else:
            raise ParseError(
                f"[Línea {self.current.line}] "
                "Token inesperado al iniciar ITEM"
            )

    # ---------------------------------------------
    # DECLARATION → TYPE ident DECLARATION_TAIL
    # ---------------------------------------------
    def declaration(self) -> None:
        self.type_()
        if self.current.type == 'ident':
            self.match('ident')
            self.declaration_tail()
        else:
            raise ParseError(
                f"[Línea {self.current.line}] "
                "Se esperaba 'ident' en DECLARATION"
            )

    # ---------------------------------------------
    # DECLARATION_TAIL → <= EXPR <D
    # ---------------------------------------------
    def declaration_tail(self) -> None:
        if self.current.type == '<=':
            self.match('<=')
            self.expr()
            if self.current.type == '<D':
                self.match('<D')
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
    def type_(self) -> None:
        if self.check('<int', '<string', '<charal', '<bubble', '<hook'):
            self.advance()
        else:
            raise ParseError(
                f"[Línea {self.current.line}] "
                "Tipo inválido en TYPE"
            )

    # ---------------------------------------------
    # FUNCTION_DEF → fishtion ident ( PARAMS ) TYPE BLOCK
    # ---------------------------------------------
    def function_def(self) -> None:
        self.match('fishtion')
        self.match('ident')
        self.match('(')
        self.params()
        self.match(')')
        self.type_()
        self.block()

    # ---------------------------------------------
    # PARAMS → PARAM PARAMS' | ε
    # FIRST(PARAMS) = { <int, <string, <charal, <bubble, <hook, ε }
    # FOLLOW(PARAMS) = { ) }
    # ---------------------------------------------
    def params(self) -> None:
        if self.check('<int', '<string', '<charal', '<bubble', '<hook'):
            self.param()
            self.params_p()
        elif self.current.type == ')':
            # ε
            return
        else:
            raise ParseError(
                f"[Línea {self.current.line}] "
                "Token inesperado en PARAMS"
            )

    # ---------------------------------------------
    # PARAMS' → , PARAM PARAMS' | ε
    # ---------------------------------------------
    def params_p(self) -> None:
        if self.current.type == ',':
            self.match(',')
            self.param()
            self.params_p()
        elif self.current.type == ')':
            # ε
            return
        else:
            raise ParseError(
                f"[Línea {self.current.line}] "
                "Token inesperado en PARAMS'"
            )

    # ---------------------------------------------
    # PARAM → TYPE ident
    # ---------------------------------------------
    def param(self) -> None:
        self.type_()
        self.match('ident')

    # ---------------------------------------------
    # STATEMENT → IF_ELSE | WHILE_LOOP | FOR_LOOP
    #           | TRY_CATCH | PRINT_STMT | RETURN_STMT
    #           | BLOCK | IDENT_STMT
    # ---------------------------------------------
    def statement(self) -> None:
        if self.current.type == 'if':
            self.if_else()
        elif self.current.type == 'whale':
            self.while_loop()
        elif self.current.type == 'fork':
            self.for_loop()
        elif self.current.type == 'try':
            self.try_catch()
        elif self.current.type == 'splash':
            self.print_stmt()
        elif self.current.type == 'emerge':
            self.return_stmt()
        elif self.current.type == '{':
            self.block()
        elif self.current.type == 'ident':
            self.ident_stmt()
        else:
            raise ParseError(
                f"[Línea {self.current.line}] "
                "Token inesperado al iniciar STATEMENT"
            )

    # ---------------------------------------------
    # IDENT_STMT → ident IDENT_TAIL
    # ---------------------------------------------
    def ident_stmt(self) -> None:
        self.match('ident')
        self.ident_tail()

    # ---------------------------------------------
    # IDENT_TAIL → ( ARGS ) <D
    #            | <= EXPR <D
    #            | <++ <D
    #            | <-- <D
    # ---------------------------------------------
    def ident_tail(self) -> None:
        if self.current.type == '(':
            self.match('(')
            self.args()
            self.match(')')
            self.match('<D')
        elif self.current.type == '<=':
            self.match('<=')
            self.expr()
            self.match('<D')
        elif self.current.type == '<++':
            self.match('<++')
            self.match('<D')
        elif self.current.type == '<--':
            self.match('<--')
            self.match('<D')
        else:
            raise ParseError(
                f"[Línea {self.current.line}] "
                "Forma inválida de IDENT_TAIL"
            )

    # ---------------------------------------------
    # ARGS → EXPR ARGS' | ε
    # FIRST(ARGS) = { <+, <-, ident, NUM, STRING_LITERAL, CHAR_LITERAL, (, ε }
    # FOLLOW(ARGS) = { ) }
    # ---------------------------------------------
    def args(self) -> None:
        if self.check('<+', '<-', 'ident', 'NUM',
                      'STRING_LITERAL', 'CHAR_LITERAL', '('):
            self.expr()
            self.args_p()
        elif self.current.type == ')':
            # ε
            return
        else:
            raise ParseError(
                f"[Línea {self.current.line}] "
                "Token inesperado en ARGS"
            )

    # ---------------------------------------------
    # ARGS' → , EXPR ARGS' | ε
    # ---------------------------------------------
    def args_p(self) -> None:
        if self.current.type == ',':
            self.match(',')
            self.expr()
            self.args_p()
        elif self.current.type == ')':
            # ε
            return
        else:
            raise ParseError(
                f"[Línea {self.current.line}] "
                "Token inesperado en ARGS'"
            )

    # ---------------------------------------------
    # IF_ELSE → if ( EXPR ) BLOCK else BLOCK
    # ---------------------------------------------
    def if_else(self) -> None:
        self.match('if')
        self.match('(')
        self.expr()
        self.match(')')
        self.block()
        self.match('else')
        self.block()

    # ---------------------------------------------
    # WHILE_LOOP → whale ( EXPR ) BLOCK
    # ---------------------------------------------
    def while_loop(self) -> None:
        self.match('whale')
        self.match('(')
        self.expr()
        self.match(')')
        self.block()

    # ---------------------------------------------
    # FOR_LOOP → fork ( FOR_INIT <D FOR_COND <D FOR_STEP ) BLOCK
    # ---------------------------------------------
    def for_loop(self) -> None:
        self.match('fork')
        self.match('(')
        self.for_init()
        self.match('<D')
        self.for_cond()
        self.match('<D')
        self.for_step()
        self.match(')')
        self.block()

    # ---------------------------------------------
    # FOR_INIT → DECL_NO_DELIM | ASSIGN_NO_DELIM | ε
    # FIRST(FOR_INIT) = { <int, <string, <charal, <bubble, <hook, ident, ε }
    # FOLLOW(FOR_INIT) = { <D }
    # ---------------------------------------------
    def for_init(self) -> None:
        if self.check('<int', '<string', '<charal', '<bubble', '<hook'):
            self.decl_no_delim()
        elif self.current.type == 'ident':
            self.assign_no_delim()
        elif self.current.type == '<D':
            # ε
            return
        else:
            raise ParseError(
                f"[Línea {self.current.line}] "
                "Token inesperado en FOR_INIT"
            )

    # ---------------------------------------------
    # FOR_COND → EXPR | ε
    # FIRST(FOR_COND) = FIRST(EXPR) ∪ { ε }
    # FOLLOW(FOR_COND) = { <D }
    # ---------------------------------------------
    def for_cond(self) -> None:
        if self.check('<+', '<-', 'ident', 'NUM',
                      'STRING_LITERAL', 'CHAR_LITERAL', '('):
            self.expr()
        elif self.current.type == '<D':
            # ε
            return
        else:
            raise ParseError(
                f"[Línea {self.current.line}] "
                "Token inesperado en FOR_COND"
            )

    # ---------------------------------------------
    # FOR_STEP → ident FOR_STEP_TAIL | ε
    # FIRST(FOR_STEP) = { ident, ε }
    # FOLLOW(FOR_STEP) = { ) }
    # ---------------------------------------------
    def for_step(self) -> None:
        if self.current.type == 'ident':
            self.match('ident')
            self.for_step_tail()
        elif self.current.type == ')':
            # ε
            return
        else:
            raise ParseError(
                f"[Línea {self.current.line}] "
                "Token inesperado en FOR_STEP"
            )

    # ---------------------------------------------
    # FOR_STEP_TAIL → <++ | <-- | <= EXPR
    # FIRST(FOR_STEP_TAIL) = { <++, <--, <= }
    # ---------------------------------------------
    def for_step_tail(self) -> None:
        if self.current.type == '<++':
            self.match('<++')
        elif self.current.type == '<--':
            self.match('<--')
        elif self.current.type == '<=':
            self.match('<=')
            self.expr()
        else:
            raise ParseError(
                f"[Línea {self.current.line}] "
                "Token inválido en FOR_STEP_TAIL"
            )

    # ---------------------------------------------
    # DECL_NO_DELIM → TYPE ident <= EXPR
    # ---------------------------------------------
    def decl_no_delim(self) -> None:
        self.type_()
        self.match('ident')
        self.match('<=')
        self.expr()

    # ---------------------------------------------
    # ASSIGN_NO_DELIM → ident <= EXPR
    #                  | ident <--
    # (Versión final del PDF)
    # ---------------------------------------------
    def assign_no_delim(self) -> None:
        self.match('ident')
        if self.current.type == '<=':
            self.match('<=')
            self.expr()
        elif self.current.type == '<--':
            self.match('<--')
        else:
            raise ParseError(
                f"[Línea {self.current.line}] "
                "ASSIGN_NO_DELIM espera '<=' o '<--' después de ident"
            )

    # ---------------------------------------------
    # TRY_CATCH → try BLOCK catch BLOCK TRY_CATCH_TAIL
    # ---------------------------------------------
    def try_catch(self) -> None:
        self.match('try')
        self.block()
        self.match('catch')
        self.block()
        self.try_catch_tail()

    # ---------------------------------------------
    # TRY_CATCH_TAIL → finally BLOCK | ε
    # FIRST = { finally, ε }
    # ---------------------------------------------
    def try_catch_tail(self) -> None:
        if self.current.type == 'finally':
            self.match('finally')
            self.block()
        else:
            # ε
            return

    # ---------------------------------------------
    # PRINT_STMT → splash ( EXPR ) <D
    # ---------------------------------------------
    def print_stmt(self) -> None:
        self.match('splash')
        self.match('(')
        self.expr()
        self.match(')')
        self.match('<D')

    # ---------------------------------------------
    # RETURN_STMT → emerge EXPR <D
    # ---------------------------------------------
    def return_stmt(self) -> None:
        self.match('emerge')
        self.expr()
        self.match('<D')

    # ---------------------------------------------
    # EXPR → EQUALITY
    # ---------------------------------------------
    def expr(self) -> None:
        self.equality()

    # ---------------------------------------------
    # EQUALITY → RELATIONAL EQUALITY'
    # ---------------------------------------------
    def equality(self) -> None:
        self.relational()
        self.equality_p()

    # ---------------------------------------------
    # EQUALITY' → <== RELATIONAL EQUALITY'
    #           | <!= RELATIONAL EQUALITY'
    #           | ε
    # FOLLOW(EQUALITY') = { ), <D, , }
    # ---------------------------------------------
    def equality_p(self) -> None:
        if self.current.type == '<==':
            self.match('<==')
            self.relational()
            self.equality_p()
        elif self.current.type == '<!=':
            self.match('<!=')
            self.relational()
            self.equality_p()
        elif self.check(')', '<D', ','):
            # ε
            return
        else:
            raise ParseError(
                f"[Línea {self.current.line}] "
                "Token inesperado en EQUALITY'"
            )

    # ---------------------------------------------
    # RELATIONAL → ADD RELATIONAL'
    # ---------------------------------------------
    def relational(self) -> None:
        self.add()
        self.relational_p()

    # ---------------------------------------------
    # RELATIONAL' → << ADD RELATIONAL'
    #             | <<> ADD RELATIONAL'
    #             | <<= ADD RELATIONAL'
    #             | <<>= ADD RELATIONAL'
    #             | ε
    # FOLLOW(RELATIONAL') = { <==, <!=, ), <D, , }
    # ---------------------------------------------
    def relational_p(self) -> None:
        if self.current.type in ('<<', '<<>', '<<=', '<<>='):
            self.advance()
            self.add()
            self.relational_p()
        elif self.current.type in ('<==', '<!=', ')', '<D', ','):
            # ε
            return
        else:
            raise ParseError(
                f"[Línea {self.current.line}] "
                "Token inesperado en RELATIONAL'"
            )

    # ---------------------------------------------
    # ADD → MUL ADD'
    # ---------------------------------------------
    def add(self) -> None:
        self.mul()
        self.add_p()

    # ---------------------------------------------
    # ADD' → <+ MUL ADD' | <- MUL ADD' | ε
    # FOLLOW(ADD') = { <<, <<>, <<=, <<>=, <==, <!=, ), <D, , }
    # ---------------------------------------------
    def add_p(self) -> None:
        if self.current.type in ('<+', '<-'):
            self.advance()
            self.mul()
            self.add_p()
        elif self.current.type in ('<<', '<<>', '<<=', '<<>=',
                                   '<==', '<!=', ')', '<D', ','):
            # ε
            return
        else:
            raise ParseError(
                f"[Línea {self.current.line}] "
                "Token inesperado en ADD'"
            )

    # ---------------------------------------------
    # MUL → UNARY MUL'
    # ---------------------------------------------
    def mul(self) -> None:
        self.unary()
        self.mul_p()

    # ---------------------------------------------
    # MUL' → <* UNARY MUL' | </ UNARY MUL' | <% UNARY MUL' | ε
    # FOLLOW(MUL') = { <+, <-, <<, <<>, <<=, <<>=, <==, <!=, ), <D, , }
    # ---------------------------------------------
    def mul_p(self) -> None:
        if self.current.type in ('<*', '</', '<%'):
            self.advance()
            self.unary()
            self.mul_p()
        elif self.current.type in ('<+', '<-', '<<', '<<>', '<<=', '<<>=',
                                   '<==', '<!=', ')', '<D', ','):
            # ε
            return
        else:
            raise ParseError(
                f"[Línea {self.current.line}] "
                "Token inesperado en MUL'"
            )

    # ---------------------------------------------
    # UNARY → <+ UNARY | <- UNARY | POSTFIX
    # ---------------------------------------------
    def unary(self) -> None:
        if self.current.type == '<+':
            self.match('<+')
            self.unary()
        elif self.current.type == '<-':
            self.match('<-')
            self.unary()
        elif self.check('ident', 'NUM', 'STRING_LITERAL',
                        'CHAR_LITERAL', '('):
            self.postfix()
        else:
            raise ParseError(
                f"[Línea {self.current.line}] "
                f"Token inesperado en UNARY: '{self.current.type}' (lexema: '{self.current.lexeme}')"
            )

    # ---------------------------------------------
    # POSTFIX → PRIMARY POSTFIX'
    # ---------------------------------------------
    def postfix(self) -> None:
        self.primary()
        self.postfix_p()

    # ---------------------------------------------
    # POSTFIX' → <++ POSTFIX' | <-- POSTFIX' | ε
    # ---------------------------------------------
    def postfix_p(self) -> None:
        if self.current.type in ('<++', '<--'):
            self.advance()
            self.postfix_p()
        else:
            # ε (cuando viene algo en FOLLOW: operadores binarios, ), <D, , ...)
            return

    # ---------------------------------------------
    # PRIMARY → ident PRIMARY_ID
    #         | NUM
    #         | STRING_LITERAL
    #         | CHAR_LITERAL
    #         | ( EXPR )
    # ---------------------------------------------
    def primary(self) -> None:
        if self.current.type == 'ident':
            self.match('ident')
            self.primary_id()
        elif self.current.type == 'NUM':
            self.match('NUM')
        elif self.current.type == 'STRING_LITERAL':
            self.match('STRING_LITERAL')
        elif self.current.type == 'CHAR_LITERAL':
            self.match('CHAR_LITERAL')
        elif self.current.type == '(':
            self.match('(')
            self.expr()
            self.match(')')
        else:
            raise ParseError(
                f"[Línea {self.current.line}] "
                "Token inesperado en PRIMARY"
            )

    # ---------------------------------------------
    # PRIMARY_ID → ( ARGS ) | ε
    # ---------------------------------------------
    def primary_id(self) -> None:
        if self.current.type == '(':
            self.match('(')
            self.args()
            self.match(')')
        else:
            # ε
            return