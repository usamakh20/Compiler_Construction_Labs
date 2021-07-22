import string
import re
import sys

from Token import *


class Lexer:

    def __init__(self):
        self.LETTER = tuple(string.ascii_letters)
        self.DIGIT = tuple(string.digits)
        self.Identifiers = ["break", "case", "char", "const", "continue",
                            "default", "double", "else", "enum", "extern",
                            "float", "for", "goto", "if", "int", "long",
                            "return", "short", "static", "struct", "switch",
                            "void", "while"]

        self.acceptance_states = self.flatten_dictionary({
            (1, 2, 3): "Arithmetic OP",
            4: "  Identifier /   Keyword   ",
            (5, 8): "Relational OP",
            (7, 9): "  Punctuator ",
            (10, 11): "    Number   "
        })
        self.transition_function = self.flatten_dictionary({
            0:
                {
                    ('*', '/', '%'): 1,
                    '+': 2,
                    '-': 3,
                    self.LETTER: 4,
                    ('>', '<'): 5,
                    '!': 6,
                    '=': 7,
                    ('{', '}',
                     '(', ')',
                     '[', ']',
                     ',', '.',
                     ';', ':',
                     "\"", "&"): 9,
                    self.DIGIT: 10
                },
            1:
                {},
            2:
                {'+': 1},
            3:
                {'-': 1},
            4:
                {
                    self.LETTER + self.DIGIT: 4
                },
            (5, 6, 7):
                {'=': 8},
            8:
                {},
            9:
                {},
            10:
                {self.DIGIT: 10, '.': 11},
            11:
                {},
            '0':
                {}
        })

    def is_acceptance_state(self, state):
        return self.acceptance_states.keys().__contains__(state)

    def dfa(self, input_string, state=0, character_index=0):

        if character_index == len(input_string) or type(state) is str:
            state = int(state)
            if self.is_acceptance_state(state):
                token_name = self.acceptance_states[state]
                token_value = input_string[:character_index]
                if state == 4:
                    token_name = token_name.split('/')[1 if self.Identifiers.__contains__(token_value) else 0]
                return Token(token_name, token_value), input_string[character_index:]
            else:
                print("Syntax Error!!!! near " + input_string)
                exit(1)

        else:
            new_state = self.transition_function.get(state).get(input_string[character_index], '0')

            if new_state == '0' and self.is_acceptance_state(state):
                new_state = str(state)
                character_index -= 1

            return self.dfa(input_string, new_state, character_index + 1)

    def lex(self, source_code):

        # removing comments whitespaces, carriage line feeds and other unneeded strings
        code_text_list = re.sub(r'#.*', '', re.sub(r'//.*', '', re.sub(r'/\*(.|[\r\n])*?\*/', '', source_code))).split()

        print(
            '|\t\t' + ' Token Name ' + '\t\t|' + '|\t\t' + '  Token Value  ' + '\t\t\t|' + '|\t\t\t\t\t' + 'Hash Value' + '\t\t\t\t|')

        for text in code_text_list:
            token, remaining_string = self.dfa(text)
            token.print()
            while remaining_string != '':
                token, remaining_string = self.dfa(remaining_string)
                token.print()

    def flatten_dictionary(self, dictionary):
        new_dictionary = {}

        for k, value in dictionary.items():
            if type(value) is dict:
                new_value = self.flatten_dictionary(value)

            else:
                new_value = value

            if type(k) is tuple:
                for key in k:
                    new_dictionary[key] = new_value
            else:
                new_dictionary[k] = new_value

        return new_dictionary


if __name__ == "__main__":
    source_code = open(sys.argv[1], 'r').read()
    Lexer().lex(source_code)
