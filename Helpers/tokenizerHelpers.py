def is_alpha(char):
    # Verifica si el carácter es una letra (mayúscula/minúscula) o '_'
    return (
        (char >= 'a' and char <= 'z') or
        (char >= 'A' and char <= 'Z') or
        char == '_'
    )

def is_digit(char):
    # Verifica si el carácter es un dígito explícitamente
    return char >= '0' and char <= '9'

# Conjunto de estados de prefijos de reservadas
RESERVED_PREFIX_STATES = {
    53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 67, 68, 69, 70, 71, 120, 121, 65,
    72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90,
    91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101,
    102, 103, 104, 105, 106,
    107, 108, 109, 110,
}


# Finales de palabras reservadas
RESERVED_FINAL_STATES = {
    56, 60, 64, 65, 71, 73, 77, 82, 85, 90, 95, 101, 106, 110,
}
ID_STATE = 5
NUM_STATE = 6
STRING_BODY_STATE = 122
STRING_END_STATE = 123
CHAR_END_STATE = 201

def classify_state(state: int) -> str:
    # Identificadores y números
    if state == ID_STATE:
        return 'ident'
    if state == NUM_STATE or state == 127:  # Números enteros y decimales
        return 'NUM'
    if state == CHAR_END_STATE:
        return 'CHAR_LITERAL'
    # Prefijo de reservada inconcluso
    if state in RESERVED_PREFIX_STATES and state not in RESERVED_FINAL_STATES:
        return 'ident'
    mapping = {
        # Tipos de datos
        30: '<int', 
        36: '<string', 
        42: '<charal', 
        48: '<bubble', 
        52: '<hook',
        # Operadores
        11: '<=',      # Asignación
        12: '<+',      # Suma
        13: '<-',      # Resta
        14: '<*',      # Multiplicación
        15: '</',      # División
        16: '<%',      # Módulo
        17: '<<',      # Menor que
        21: '<<>',     # Mayor que
        22: '<<=',     # Menor o igual
        23: '<!=',     # Diferente
        24: '<==',     # Igual
        25: '<++',     # Incremento
        26: '<--',     # Decremento
        27: '<<>=',    # Mayor o igual
        19: '<D',      # Delimitador
        20: 'COMENTARIO_BLOQUE_INICIO',
        # Palabras reservadas
        56: 'fish',       # Main
        60: 'IMPORT', 
        64: 'fishtion',   # Function
        65: 'fork',       # For
        71: 'finally', 
        73: 'if',
        77: 'else', 
        82: 'emerge',     # Return
        85: 'try', 
        90: 'catch', 
        95: 'whale',      # While
        101: 'splash',    # Print
        106: 'ARRAY', 
        110: 'DICT',
        # Símbolos
        111: 'CORCHETE_IZQ', 
        112: 'CORCHETE_DER', 
        113: '{', 
        114: '}',
        115: ',', 
        116: 'PUNTO', 
        118: 'COMENTARIO_LINEA', 
        119: 'COMENTARIO_BLOQUE_FIN',
        2: '(', 
        3: ')',
        # Operadores simples
        1: 'OP', 
        7: 'OP', 
        8: 'OP', 
        9: 'OP',
        # Literales de string
        123: 'STRING_LITERAL',
    }
    return mapping.get(state, 'NO RECONOCIDO')