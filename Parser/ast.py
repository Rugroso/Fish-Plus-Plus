from dataclasses import dataclass, field
from typing import Any, List


@dataclass
class ASTNode:
    kind: str
    value: Any = None
    children: List['ASTNode'] = field(default_factory=list)
    line: int = -1

    def add(self, node: 'ASTNode') -> None:
        if node is not None:
            self.children.append(node)


def pretty_print(node: ASTNode, indent: int = 0) -> None:
    pad = '  ' * indent
    if node is None:
        print(pad + '<empty>')
        return
    val = f": {node.value}" if node.value is not None else ''
    print(f"{pad}{node.kind}{val}")
    for c in node.children:
        pretty_print(c, indent + 1)
