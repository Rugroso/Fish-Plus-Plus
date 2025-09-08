# Fish++

Fish++ is a custom programming language project (based on Fish Project). This repository contains the source code for a tokenizer, helper modules, and testing files to process and analyze Fish++ code.

## Project Structure

```
Fish++/
├── main.py                # Main entry point for the program
├── Helpers/               # Helper modules for tokenizing and processing
│   ├── cleaner.py
│   ├── reader.py
│   ├── symbolsTable.py
│   ├── tokenizerHelpers.py
│   ├── transitions.py
│   └── __pycache__/
├── Tokens/                # Tokenizer implementation
│   ├── tokenizer.py
│   └── __pycache__/
├── Testing/               # Test files and examples
│   └── just_testing.txt
```

## How to Run

1. Make sure you have Python 3.12 or higher installed.
2. Run the main program:

```bash
python3 main.py
```

## Main Components

- **main.py**: Entry point for running the Fish++ tokenizer and related logic.
- **Helpers/**: Contains utility modules for cleaning input, reading files, managing symbol tables, and handling tokenizer logic.
- **Tokens/tokenizer.py**: Implements the tokenizer for Fish++ code.
- **Testing/**: Contains sample input files for testing the tokenizer.

## Contributing

Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is open source and available under the MIT License.
