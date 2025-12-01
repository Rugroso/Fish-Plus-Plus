from typing import Dict, List, Optional
from Parser.ast import ASTNode


class SemanticError(Exception):
    pass


class Symbol:
    def __init__(self, name: str, typ: str, node: Optional[ASTNode] = None):
        self.name = name
        self.type = typ
        self.node = node


class SemanticAnalyzer:
    def __init__(self):
        self.scopes: List[Dict[str, Symbol]] = []
        self.functions: Dict[str, Symbol] = {}
        self.errors: List[str] = []
        self.current_function: Optional[Symbol] = None

    def push_scope(self) -> None:
        # print("Current scopes:", self.scopes)
        self.scopes.append({})

    def pop_scope(self) -> None:
        if self.scopes:
            self.scopes.pop()

    def declare_var(self, name: str, typ: str, node: ASTNode) -> None:
        if not self.scopes:
            self.push_scope()
        scope = self.scopes[-1]
        if name in scope:
            # print("Current scopes at error:", self.scopes)W
            self.errors.append(f"[Línea {node.line}] Variable '{name}' ya declarada en este ámbito")
        scope[name] = Symbol(name, typ, node)

    def lookup_var(self, name: str) -> Optional[Symbol]:
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

    def declare_function(self, name: str, return_type: str, params: List[Symbol], node: ASTNode) -> None:
        if name in self.functions:
            self.errors.append(f"[Línea {node.line}] Función '{name}' ya declarada")
            return
        sym = Symbol(name, return_type, node)
        # attach signature
        sym.params = params
        self.functions[name] = sym

    def lookup_function(self, name: str) -> Optional[Symbol]:
        return self.functions.get(name)

    def analyze(self, root: ASTNode) -> List[str]:
        self.visit(root)
        return self.errors

    # ----------------------- visitors -----------------------
    def visit(self, node: ASTNode) -> Optional[str]:
        print(f"Visiting node: {node.kind} (line {node.line})")
        method = getattr(self, f"visit_{node.kind}", self.generic_visit)
        return method(node)

    def generic_visit(self, node: ASTNode) -> Optional[str]:
        for c in node.children:
            self.visit(c)
        return None

    def visit_Program(self, node: ASTNode) -> None:
        self.push_scope()
        # program -> Block
        for c in node.children:
            self.visit(c)
        self.pop_scope()

    def visit_Block(self, node: ASTNode) -> None:
        self.push_scope()
        for c in node.children:
            self.visit(c)
        self.pop_scope()

    def visit_Params(self, node: ASTNode) -> List[Symbol]:
        params: List[Symbol] = []
        for p in node.children:
            sym = self.visit(p)
            if isinstance(sym, Symbol):
                params.append(sym)
        return params

    def visit_Param(self, node: ASTNode) -> Symbol:
        # Param children: [Type]
        typ = node.children[0].value if node.children else None
        name = node.value
        return Symbol(name, typ, node)

    def visit_FunctionDef(self, node: ASTNode) -> None:
        name = node.value
        params_node = node.children[0]
        ret_type_node = node.children[1]
        body = node.children[2]
        params = self.visit_Params(params_node)
        ret_type = ret_type_node.value if ret_type_node else None
        # declare function
        self.declare_function(name, ret_type, params, node)
        # new function scope
        prev_func = self.current_function
        self.current_function = self.functions.get(name)
        self.push_scope()
        # declare parameters in scope
        for p in params:
            self.declare_var(p.name, p.type, node)
        self.visit(body)
        self.pop_scope()
        self.current_function = prev_func

    def visit_Declaration(self, node: ASTNode) -> None:
        # node.value = name, children = [Type, maybe Initializer or expr]
        name = node.value
        tnode = node.children[0]
        typ = tnode.value
        self.declare_var(name, typ, node)
        if len(node.children) > 1:
            init = node.children[1]
            init_type = self.visit(init.children[0]) if init.children else None
            # simple check: init type matches declared type
            if init_type and not self.type_compatible(typ, init_type):
                self.errors.append(f"[Línea {node.line}] Inicializador de '{name}' no es compatible con el tipo {typ}")

    def visit_Assign(self, node: ASTNode) -> None:
        # node.value = name, children = [expr]
        name = node.value
        sym = self.lookup_var(name)
        if not sym:
            self.errors.append(f"[Línea {node.line}] Variable '{name}' no declarada")
            return
        expr_type = self.visit(node.children[0])
        if expr_type and not self.type_compatible(sym.type, expr_type):
            self.errors.append(f"[Línea {node.line}] Asignación a '{name}' ({sym.type}) con tipo incompatible {expr_type}")

    def visit_CallStmt(self, node: ASTNode) -> None:
        # call as statement
        return self.visit_Call(node)

    def visit_Call(self, node: ASTNode) -> Optional[str]:
        name = node.value
        func = self.lookup_function(name)
        if not func:
            self.errors.append(f"[Línea {node.line}] Llamada a función no declarada '{name}'")
            return None
        args_node = node.children[0] if node.children else None
        arg_types = []
        if args_node:
            for a in args_node.children:
                t = self.visit(a)
                arg_types.append(t)
        expected = getattr(func, 'params', [])
        if len(arg_types) != len(expected):
            self.errors.append(f"[Línea {node.line}] Llamada a '{name}' con {len(arg_types)} args, esperaba {len(expected)}")
        else:
            for i, (at, p) in enumerate(zip(arg_types, expected)):
                if at and not self.type_compatible(p.type, at):
                    self.errors.append(f"[Línea {node.line}] Arg {i+1} en llamada a '{name}' incompatible: esperaba {p.type}, tiene {at}")
        return func.type

    def visit_Return(self, node: ASTNode) -> None:
        if not self.current_function:
            self.errors.append(f"[Línea {node.line}] 'return' fuera de función")
            return
        expr_type = self.visit(node.children[0]) if node.children else None
        if expr_type and not self.type_compatible(self.current_function.type, expr_type):
            self.errors.append(f"[Línea {node.line}] Tipo de retorno incompatible en función '{self.current_function.name}': esperaba {self.current_function.type}, obtuvo {expr_type}")

    def visit_Print(self, node: ASTNode) -> None:
        # print accepts any type for now
        for c in node.children:
            self.visit(c)

    def visit_If(self, node: ASTNode) -> None:
        cond_type = self.visit(node.children[0])
        # simple check: condition should be comparable
        if cond_type is None:
            pass
        self.visit(node.children[1])
        self.visit(node.children[2])

    def visit_While(self, node: ASTNode) -> None:
        self.visit(node.children[0])
        self.visit(node.children[1])

    def visit_For(self, node: ASTNode) -> None:
        init = node.children[0]
        cond = node.children[1]
        step = node.children[2]
        body = node.children[3]
        if init and init.kind != 'Empty':
            self.visit(init)
        if cond and cond.kind != 'Empty':
            self.visit(cond)
        if step and step.kind != 'Empty':
            self.visit(step)
        self.visit(body)

    def visit_ForStep(self, node: ASTNode) -> None:
        if node.children:
            self.visit(node.children[0])

    def visit_Postfix(self, node: ASTNode) -> Optional[str]:
        # used in for-step
        return None

    def visit_PostfixOp(self, node: ASTNode) -> Optional[str]:
        # return type of operand
        return self.visit(node.children[0])

    def visit_UnaryOp(self, node: ASTNode) -> Optional[str]:
        return self.visit(node.children[0])

    def visit_BinaryOp(self, node: ASTNode) -> Optional[str]:
        left = self.visit(node.children[0])
        right = self.visit(node.children[1])
        if left is None or right is None:
            return None
        if not self.type_compatible(left, right):
            self.errors.append(f"[Línea {node.line}] Operación binaria '{node.value}' entre tipos incompatibles: {left} y {right}")
            return None
        return left

    def visit_Var(self, node: ASTNode) -> Optional[str]:
        sym = self.lookup_var(node.value)
        if not sym:
            self.errors.append(f"[Línea {node.line}] Variable '{node.value}' no declarada")
            return None
        return sym.type

    # ----------------------- helpers -----------------------
    def type_compatible(self, expected: Optional[str], given: Optional[str]) -> bool:
        if expected is None or given is None:
            return True
        return expected == given
