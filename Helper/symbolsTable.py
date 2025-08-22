tokens = {
    "MAIN": {
        "regex": r"fish",
        "example": "fish"
    },
    "IMPORTAR": {
        "regex": r"fishport",
        "example": "fishport"
    },
    "IF": {
        "regex": r"if",
        "example": "if"
    },
    "ELSE": {
        "regex": r"else",
        "example": "else"
    },
    "FUNCION": {
        "regex": r"fishtion",
        "example": "fishtion"
    },
    "TRY": {
        "regex": r"try",
        "example": "try"
    },
    "CATCH": {
        "regex": r"catch",
        "example": "catch"
    },
    "FINALLY": {
        "regex": r"finally",
        "example": "finally"
    },
    "RETURN": {
        "regex": r"emerge",
        "example": "emerge"
    },
    # TIPOS DE DATOS - Solo estos tienen "<"
    "ENTERO": {
        "regex": r"<int",
        "example": "<int"
    },
    "STRING": {
        "regex": r"<string",
        "example": "<string"
    },
    "CHAR": {
        "regex": r"<charal",
        "example": "<charal"
    },
    "FLOAT": {
        "regex": r"<bubble",
        "example": "<bubble"
    },
    "BOOLEANO": {
        "regex": r"<hook",
        "example": "<hook"
    },
    # FIN TIPOS DE DATOS
    "WHILE": {
        "regex": r"whale",
        "example": "whale"
    },
    "FOR": {
        "regex": r"fork",
        "example": "fork"
    },
    "PRINT": {
        "regex": r"splash",
        "example": "splash"
    },
    "ID": {
        "regex": r"[a-zA-Z_][a-zA-Z0-9_]*",
        "example": "contador"
    },
    "NUM": {
        "regex": r"[0-9]+(\.[0-9]+)?",
        "example": "42, 3.14"
    },
    "ASIGNACION": {
        "regex": r"<=",
        "example": "<="
    },
    "OP_SUMA": {
        "regex": r"<\+",
        "example": "<+"
    },
    "OP_RESTA": {
        "regex": r"<-",
        "example": "<-"
    },
    "OP_MULTIPLICACION": {
        "regex": r"<\*",
        "example": "<*"
    },
    "OP_DIVISION": {
        "regex": r"</",
        "example": "</"
    },
    "OP_MODULO": {
        "regex": r"<%",
        "example": "<%"
    },
    "OP_MENOR_QUE": {
        "regex": r"<<",
        "example": "<<"
    },
    "OP_MAYOR_QUE": {
        "regex": r"<<>",
        "example": "<<>"
    },
    "DELIMITADOR": {
        "regex": r"<D",
        "example": "<D"
    },
    "OP_IGUAL": {
        "regex": r"<==",
        "example": "<=="
    },
    "OP_DIFERENTE": {
        "regex": r"<!=",
        "example": "<!="
    },
    "OP_MENOR_IGUAL": {
        "regex": r"<<=",
        "example": "<<="
    },
    "OP_MAYOR_IGUAL": {
        "regex": r"<<>=",
        "example": "<<>="
    },
    "PARENTESIS_IZQ": {
        "regex": r"\(",
        "example": "("
    },
    "PARENTESIS_DER": {
        "regex": r"\)",
        "example": ")"
    },
    "CORCHETE_IZQ": {
        "regex": r"\[",
        "example": "["
    },
    "CORCHETE_DER": {
        "regex": r"\]",
        "example": "]"
    },
    "LLAVE_IZQ": {
        "regex": r"\{",
        "example": "{"
    },
    "LLAVE_DER": {
        "regex": r"\}",
        "example": "}"
    },
    "COMA": {
        "regex": r",",
        "example": ","
    },
    "PUNTO": {
        "regex": r"\.",
        "example": "."
    },
    "ARRAY": {
        "regex": r"array", 
        "example": "array"
    },
    "DICT": {
        "regex": r"dict", 
        "example": "dict"
    },
    "COMENTARIO_LINEA": {
        "regex": r"~~.*",
        "example": "~~ esto es un comentario"
    },
    "COMENTARIO_BLOQUE_INICIO": {
        "regex": r"<~",
        "example": "<~"
    },
    "COMENTARIO_BLOQUE_FIN": {
        "regex": r"~>",
        "example": "~>"
    },
    "INCREMENTO": {
        "regex": r"<\+\+",
        "example": "<++"
    },
    "DECREMENTO": {
        "regex": r"<--",
        "example": "<--"
    }   
}