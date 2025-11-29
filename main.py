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

raw = reader('Testing/just_testing.txt')

text = clean_input(raw)
tokens = process_tokens(automaton, text)
if not tokens:
    pass
# for token in tokens:
#     print("Token:", token)
    
parser = Parser(tokens)
ast = parser.parse()
print("Parsed Output:")
pretty_print(ast)

# Analizador semántico
analyzer = SemanticAnalyzer()
errors = analyzer.analyze(ast)
if errors:
    print('\nSemantic Errors:')
    for e in errors:
        print('-', e)
else:
    print('\nSemantic: OK')