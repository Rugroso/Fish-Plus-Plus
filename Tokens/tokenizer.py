from Helpers.tokenizerHelpers import RESERVED_FINAL_STATES, RESERVED_PREFIX_STATES, ID_STATE, STRING_BODY_STATE, classify_state, is_alpha, is_digit
from Helpers.transitions import STRING_BODY_STATE
from Helpers.cleaner import clean_input

def process_tokens(self, input_text: str) -> list:
        
        input_text = clean_input(input_text)

        tokens = []
        state = self.start_state
        buffer = ""
        i = 0
        n = len(input_text)

        reserved_initials = {'f', 'i', 'e', 't', 'c', 'w', 's', 'a', 'd'}

        while i < n:
            c = input_text[i]
            # Categoría
            if state == STRING_BODY_STATE:
                category = '"' if c == '"' else 'str'
            elif c == '"':
                category = '"'
            elif is_alpha(c):
                if state == 0 and c in reserved_initials:
                    category = c
                elif state in RESERVED_PREFIX_STATES:
                    category = c
                elif state >= 10:
                    category = c
                else:
                    category = 'char'
            elif is_digit(c):
                category = 'num'
            elif c == '.':
                category = '.'
            elif c in "+-*/=(){},[]<%>!D~":
                category = c
            else:
                i += 1
                continue

            # Transición
            if category in self.states[state]:
                print (f"Transición: {state} --{category}--> {self.states[state][category]}")
                state = self.states[state][category]
                buffer += c
                print (state)
                i += 1
            else:
                # Si rompemos un prefijo reservado (no final), convertirse en id sin consumir c
                # De esta forma simplificamos la lógica y evitamos una cantidad excesiva de transiciones
                # Se puede consultar como se diseñaron estas transiciones en el DFA y NDFA
                if (state in RESERVED_PREFIX_STATES and state not in RESERVED_FINAL_STATES
                        and (is_alpha(c) or is_digit(c))):
                    state = ID_STATE
                    continue
                # Volcar token si hay uno aceptado
                if buffer and state in self.accept_states:
                    tokens.append((buffer, classify_state(state)))
                elif buffer:
                    tokens.append((buffer, 'NO RECONOCIDO'))
                # Reset y reintentar con el mismo carácter
                buffer = ""
                state = self.start_state
                continue

        if buffer and state in self.accept_states:
            tokens.append((buffer, classify_state(state)))
        elif buffer:
            tokens.append((buffer, 'NO RECONOCIDO'))
        return tokens