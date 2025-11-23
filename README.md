# Fish++

Fish++ is a custom programming language project (based on Fish Project). This repository contains the complete implementation of a lexical analyzer (tokenizer) and syntax analyzer (parser) for the Fish++ programming language.

## Project Structure

```
Fish++_Parser/
├── main.py                # Main entry point for the program
├── README.md              # This file
├── Helpers/               # Helper modules for tokenizing and processing
│   ├── cleaner.py         # Input cleaning utilities
│   ├── reader.py          # File reading utilities
│   ├── symbolsTable.py    # Symbol table management
│   ├── tokenizerHelpers.py # Token classification and state management
│   ├── transitions.py     # Automaton transitions and accept states
│   └── __pycache__/
├── Parser/                # Parser implementation
│   ├── parser.py          # Recursive descent parser
│   └── __pycache__/
├── Tokens/                # Tokenizer implementation
│   ├── tokenizer.py       # Lexical analyzer
│   └── __pycache__/
├── Testing/               # Test files and examples
│   └── just_testing.txt   # Sample Fish++ code
```

## Features

- **Lexical Analysis**: Complete tokenizer with support for:
  - Keywords: `fish`, `fishtion`, `if`, `else`, `whale`, `fork`, `try`, `catch`, `finally`, `splash`, `emerge`
  - Data types: `<int`, `<string`, `<charal`, `<bubble`, `<hook`
  - Operators: `<+`, `<-`, `<*`, `</`, `<%`, `<=`, `<==`, `<!=`, `<<`, `<<>`, `<<=`, `<<>=`, `<++`, `<--`
  - Literals: numbers, strings, characters
  - Symbols: `{`, `}`, `(`, `)`, `,`, `<D`

- **Syntax Analysis**: Recursive descent parser supporting:
  - Function declarations
  - Variable declarations and assignments
  - Control structures (if-else, while, for loops)
  - Exception handling (try-catch-finally)
  - Expressions with operator precedence
  - Print and return statements

## How to Run

1. Make sure you have Python 3.12 or higher installed.
2. Run the main program:

```bash
python3 main.py
```

The program will:
1. Read the test file from `Testing/just_testing.txt`
2. Clean and tokenize the input
3. Parse the token stream
4. Display "Parsing completed successfully" if the code is syntactically correct

## Language Syntax Example

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

    if (contador <<> 5) {
        splash("Mayor que 5")<D
    } else {
        splash("No mayor que 5")<D
    }
}
```

## Main Components

- **main.py**: Entry point that orchestrates tokenization and parsing
- **Parser/parser.py**: Implements recursive descent parser with error reporting
- **Tokens/tokenizer.py**: Finite automaton-based lexical analyzer
- **Helpers/tokenizerHelpers.py**: Token classification and state mapping
- **Helpers/transitions.py**: Automaton transition table and accept states
- **Helpers/cleaner.py**: Input preprocessing and comment removal
- **Testing/**: Sample Fish++ programs for testing

## Contributing

Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is open source and available under the MIT License.
