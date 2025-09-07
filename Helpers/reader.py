def reader(input_file: str) -> str:
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            raw = f.read()
    except FileNotFoundError:
        print(f"No se encontró el archivo de entrada: {input_file}")
        raise
    return raw
