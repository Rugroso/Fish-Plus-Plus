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


        CHAR_BODY_STATE = 200
        CHAR_END_STATE = 201

        while i < n:
            c = input_text[i]
            # Categoría
            if state == STRING_BODY_STATE:
                category = '"' if c == '"' else 'str'
            elif state == CHAR_BODY_STATE:
                category = "'" if c == "'" else 'char_body'
            elif c == '"':
                category = '"'
            elif c == "'":
                category = "'"
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

            # Transición para char literal
            if state == 0 and c == "'":
                state = CHAR_BODY_STATE
                buffer += c
                i += 1
                continue
            elif state == CHAR_BODY_STATE:
                # Solo se permite un caracter entre comillas simples
                if c != "'" and c != '\\':
                    buffer += c
                    i += 1
                    continue
                elif c == '\\':
                    # Soporte para escape de caracter
                    if i + 1 < n:
                        buffer += c + input_text[i+1]
                        i += 2
                        continue
                elif c == "'":
                    buffer += c
                    state = CHAR_END_STATE
                    i += 1
                    continue
            elif state == CHAR_END_STATE:
                tokens.append((buffer, 'CHAR'))
                buffer = ""
                state = self.start_state
                continue

            # Lógica especial: si estamos en estado de número y el siguiente carácter es letra, marcar como NO VALIDO
            if state == 6 and is_alpha(input_text[i]):
                buffer += input_text[i]
                i += 1
                while i < n and (is_alpha(input_text[i]) or is_digit(input_text[i])):
                    buffer += input_text[i]
                    i += 1
                tokens.append((buffer, 'NO VALIDO'))
                buffer = ""
                state = self.start_state
                continue
            if category in self.states[state]:
                #print (f"Transición: {state} --{category}--> {self.states[state][category]}")
                state = self.states[state][category]
                buffer += c
                #print (state)
                i += 1
            else:
                # Si rompemos un prefijo reservado (no final), convertirse en id sin consumir c
                if (state in RESERVED_PREFIX_STATES and state not in RESERVED_FINAL_STATES
                        and (is_alpha(c) or is_digit(c))):
                    state = ID_STATE
                    continue
                # Volcar token si hay uno aceptado
                if buffer and state in self.accept_states:
                    tokens.append((buffer, classify_state(state)))
                elif buffer:
                    tokens.append((buffer, 'NO RECONOCIDO'))
                buffer = ""
                state = self.start_state
                continue

        if buffer and state in self.accept_states:
            tokens.append((buffer, classify_state(state)))
        elif buffer:
            tokens.append((buffer, 'NO RECONOCIDO'))
        return tokens