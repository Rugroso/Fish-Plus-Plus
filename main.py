from Tokens.tokenizer import process_tokens
from Helpers.cleaner import clean_input
from Helpers.transitions import transitions, accept_states
from Helpers.reader import reader
from Parser.parser import Parser
from Parser.ast import pretty_print
from Parser.semantic import SemanticAnalyzer

class Automaton:
    def __init__(self, transitions: list, accept_states: set):
        self.transitions = transitions
        self.accept_states = accept_states
        max_state = max(max(frm, to) for frm, to, _ in transitions)
        self.states = {i: {} for i in range(max_state + 1)}
        self.start_state = 0
        self._build_transitions(transitions)

    def _build_transitions(self, transitions):
        for from_state, to_state, symbol in transitions:
            self.states[from_state][symbol] = to_state

automaton = Automaton(transitions, accept_states)

for i in range(3):
    if i == 0:
        # Un test rapido mostrando un buen funcionamiento general
        print("Test General (Funciona bien)...")
        raw = reader('Testing/just_testing.txt')
    elif i == 1:
        # Un test rapido mostrando funcionamiento de un error semántico
        print("Aqui se debe presentar un error semántico (error en asignacion, tipos distintos)...")
        raw = reader('Testing/Small/test_invalid_type_mismatch.txt')
    else:
        # Un test rapido mostrando funcionamiento de un error sintáctico
        print("Aqui se debe presentar un error sintáctico (falta el main, es decir fish)...")
        raw = reader('Testing/Small/test_invalid_no_fish.txt')
    text = clean_input(raw)
    tokens = process_tokens(automaton, text)
    if not tokens:
        pass
    for token in tokens:
        print("Token:", token)
        
    parser = Parser(tokens)
    ast = parser.parse()
    print("Parsed Output:")
    pretty_print(ast)

    # Analizador semántico
    analyzer = SemanticAnalyzer()
    errors = analyzer.analyze(ast)
    # print ("scopes", analyzer.scopes)
    # print ("Functions", analyzer.functions)

    if errors:
        print('\nSemantic Errors:')
        for e in errors:
            print('-', e)
    else:
        print('\nSemantic: OK')
        