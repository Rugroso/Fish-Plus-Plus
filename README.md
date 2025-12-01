# Fish++

Fish++ is a custom programming-language project (inspired by the Fish Project). This repository implements a tokenizer (lexical analyzer), a parser (syntax analyzer) and basic semantic components for the Fish++ language.

## Project Structure

```
Fish++_Parser/
├── main.py                # Main entry point for the program
├── README.md              # This file
├── Helpers/               # Helper modules for tokenizing and processing
│   ├── cleaner.py         # Input cleaning and comment removal
│   ├── reader.py          # File reading utilities
│   ├── symbolsTable.py    # Symbol table management (semantic help)
│   ├── tokenizerHelpers.py# Token classification and state utilities
│   ├── transitions.py     # Automaton transitions and accept states
│   └── __pycache__/
├── Parser/                # Parser and semantic analysis
│   ├── ast.py             # AST node definitions
│   ├── parser.py          # Recursive descent parser
│   ├── semantic.py        # Semantic checks and symbol resolution
│   └── __pycache__/
├── Tokens/                # Tokenizer implementation
│   ├── tokenizer.py       # Lexical analyzer (finite automaton)
│   └── __pycache__/
├── Testing/               # Test files and examples
│   └── just_testing.txt   # Sample Fish++ code
```

## Features

- Lexical analysis with a finite-state tokenizer supporting:
    - Keywords: `fish`, `fishtion`, `if`, `else`, `whale`, `fork`, `try`, `catch`, `finally`, `splash`, `emerge`
    - Data types: `<int`, `<string`, `<charal`, `<bubble`, `<hook`
    - Operators and punctuators used by the language
    - Literals: numbers, strings, characters

- Syntax analysis (recursive-descent parser) supporting:
    - Function declarations and calls
    - Variable declarations and assignments
    - Control structures (if/else, loops)
    - Exception-handling constructs (try/catch/finally)
    - Expressions with operator precedence

- Basic semantic analysis: AST construction and symbol-table checks

## Requirements

- Python 3.8+ (the code runs fine on modern 3.x interpreters). Use `python3 --version` to verify.

## Quickstart — Run locally

1. (Optional) Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Run the main program (it uses the sample in `Testing/just_testing.txt` by default):

```bash
python3 main.py
```

Expected behaviour:
- The program reads `Testing/just_testing.txt`, cleans the input, tokenizes it, parses the token stream and performs basic semantic checks.
- If parsing succeeds, you should see a success message or no fatal errors printed to stdout.

## Running a different file

Open `main.py` to see the input selection logic, or modify it to load another test file. You can also import the tokenizer or parser from `Tokens/tokenizer.py` and `Parser/parser.py` for programmatic use.

## Example Fish++ snippet

```fish
fish {
        fishtion sumar(<int a, <int b) <int {
                emerge a <+ b<D
        }

        <int contador <= 0<D
        whale (contador << 5) {
                splash("Iteración: ")<D
                contador <++<D
        }
}
```

## Main components reference

- `main.py`: program entry point — orchestration for cleaning, tokenizing and parsing
- `Parser/ast.py`: AST node definitions used by the parser and semantic analyzer
- `Parser/parser.py`: recursive-descent parser implementation
- `Parser/semantic.py`: semantic checks and symbol-table interactions
- `Tokens/tokenizer.py`: finite-automaton based lexical analyzer
- `Helpers/`: helper modules (cleaner, reader, tokenizer helpers, transitions, symbol table)

## Contributing

Contributions are welcome. Please open an issue to discuss larger changes before submitting a pull request.

## License

This project is licensed under the MIT License.
