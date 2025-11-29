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
     # 2) Normalizar saltos de línea y conservarlos para conteo de líneas en el parser
     #    Dejamos espacios/tabs intactos (el tokenizer los ignorará). Sustituimos CRLF por LF.
     text = text.replace('\r\n', '\n').replace('\r', '\n')
     return text
