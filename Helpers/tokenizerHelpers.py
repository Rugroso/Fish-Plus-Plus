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

def classify_state(state: int) -> str:
    # Identificadores y números
    if state == ID_STATE:
        return 'ID'
    if state == NUM_STATE or state == 127:  # Números enteros y decimales
        return 'NUM'
    # Prefijo de reservada inconcluso
    if state in RESERVED_PREFIX_STATES and state not in RESERVED_FINAL_STATES:
        return 'ID'
    mapping = {
        # Tipos
        30: 'INT', 36: 'STRING', 42: 'CHAR', 48: 'FLOAT', 52: 'BOOLEANO',
        # Operadores <*>
        11: 'ASIGNACION', 12: 'OP_SUMA', 13: 'OP_RESTA', 14: 'OP_MULTIPLICACION',
        15: 'OP_DIVISION', 16: 'OP_MODULO', 17: 'OP_MENOR_QUE', 21: 'OP_MAYOR_QUE',
        22: 'OP_MENOR_IGUAL', 23: 'OP_DIFERENTE', 24: 'OP_IGUAL', 25: 'INCREMENTO',
        26: 'DECREMENTO', 27: 'OP_MAYOR_IGUAL', 19: 'DELIMITADOR', 20: 'COMENTARIO_BLOQUE_INICIO',
        # Palabras reservadas
        56: 'MAIN', 60: 'IMPORT', 64: 'FUNCTION', 65: 'FOR', 71: 'FINALLY', 73: 'IF',
        77: 'ELSE', 82: 'RETURN', 85: 'TRY', 90: 'CATCH', 95: 'WHILE', 101: 'PRINT',
        106: 'ARRAY', 110: 'DICT',
        # Símbolos
        111: 'CORCHETE_IZQ', 112: 'CORCHETE_DER', 113: 'LLAVE_IZQ', 114: 'LLAVE_DER',
        115: 'COMA', 116: 'PUNTO', 118: 'COMENTARIO_LINEA', 119: 'COMENTARIO_BLOQUE_FIN',
        2: 'PAREN_IZQ', 3: 'PAREN_DER',
        # Operadores simples
        1: 'OP', 7: 'OP', 8: 'OP', 9: 'OP',
    # Literales
    123: 'STRING',
    }
    return mapping.get(state, 'UNKNOWN')