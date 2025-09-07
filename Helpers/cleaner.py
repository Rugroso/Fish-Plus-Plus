import re

def _remove_comments(input_text: str) -> str:
     # Eliminar comentarios de bloque <~ ... ~> (no codiciosa, a través de líneas). Si no hay cierre, elimina hasta EOF
     text = re.sub(r"<~.*?(~>|$)", "", input_text, flags=re.S)
     # Eliminar comentarios de línea ~~ hasta el fin de línea
     text = re.sub(r"~~[^\n]*", "", text)
     return text

def clean_input(input_text: str) -> str:
     # 1) Quitar comentarios primero
     text = _remove_comments(input_text)
     # 2) Luego eliminar todos los espacios en blanco
     text = ''.join(ch for ch in text if not ch.isspace())
     return text
