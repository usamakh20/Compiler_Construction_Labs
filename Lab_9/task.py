class Parser:

    def __init__(self):
        grammar_text = open('grammar', 'r').read()
        self.non_terminals = []
        self.terminals = ['(', ')', '+', '-', '*', '/', 'id', 'num', '$']
        self.start_symbol = 'E'
        self.grammar = self.structure_grammar(grammar_text.replace(' ', ''))
        self.first_sets = {}
        self.follow_sets = {}
        for non_terminal in self.grammar:
            self.first_sets[non_terminal] = self.get_first_set(non_terminal)
            self.follow_sets[non_terminal] = self.get_follow_set(non_terminal)

    def get_first_of_production(self, production):
        first_of_production = set()
        for symbol in production:
            if symbol in self.non_terminals:
                first = self.get_first_set(symbol)
                first_of_production = first_of_production.union(first)
                if 'ε' in first:
                    continue
                else:
                    break
            else:
                first_of_production.add(symbol)
                break

        return first_of_production

    def get_first_set(self, non_terminal):
        if non_terminal in self.first_sets:
            return self.first_sets[non_terminal]

        first_set = set()
        for production in self.grammar[non_terminal]:
            first_set = first_set.union(self.get_first_of_production(production))

        return first_set

    def get_follow_set(self, non_terminal):
        if non_terminal in self.follow_sets:
            return self.follow_sets[non_terminal]

        follow_set = {'ε'}
        if non_terminal == self.start_symbol:
            follow_set.add('$')

        for symbol, productions in self.grammar.items():
            for production in productions:
                for i in range(len(production)):
                    if production[i] == non_terminal:
                        for next_symbol in production[i + 1:]:
                            if 'ε' in follow_set:
                                follow_set.remove('ε')
                            if next_symbol in self.non_terminals:
                                follow_set = follow_set.union(self.get_first_set(next_symbol))
                                if 'ε' in follow_set:
                                    continue
                                else:
                                    break
                            else:
                                follow_set.add(next_symbol)
                                break

                        if 'ε' in follow_set:
                            follow_set.remove('ε')
                            if symbol != non_terminal:
                                follow_set = follow_set.union(self.get_follow_set(symbol))

        return follow_set

    def is_nullable(self, non_terminal):
        for productions in self.grammar[non_terminal]:
            for production in productions:
                for symbol in production:
                    if symbol == 'ε':
                        return 'Yes'
        return 'No'

    def get_parse_table(self, non_terminal):
        parse_row = ['\t    '] * len(self.terminals)
        for production in self.grammar[non_terminal]:
            first_of_production = self.get_first_of_production(production)
            if 'ε' in first_of_production:
                first_of_production.remove('ε')
                first_of_production = first_of_production.union(self.get_follow_set(non_terminal))
            indices = [self.terminals.index(terminal) for terminal in first_of_production]
            for i in indices:
                parse_row[i] = non_terminal + ' → ' + ''.join(production)
                for k in range(7 - len(parse_row[i])):
                    parse_row[i] += ' '

        return parse_row

    def structure_grammar(self, grammar_text):
        grammar = {}
        grammar_text = grammar_text.split('\n')[:-1]
        grammar_text = [line + "\n" for line in grammar_text]

        separate_grammar_text = []
        for line in grammar_text:
            separate_grammar_text.append(line.split('→'))

        self.non_terminals = [item[0] for item in separate_grammar_text]

        for non_terminal, productions in separate_grammar_text:
            accumulator = ['']
            grammar[non_terminal] = []
            for character in productions:
                if character == '|' or character == '\n':
                    grammar[non_terminal].append(accumulator[:-1])
                    accumulator = ['']
                else:
                    accumulator[-1] += character
                    if accumulator[-1] in self.terminals + self.non_terminals + ['ε']:
                        accumulator += ['']

        return grammar

    def print_tables(self):

        alt_3_2 = 2


        print('\n\nFIRST FOLLOW SETS:\n')
        print('Non-terminal|  Nullable |\t\tFIRST\t\t|\tFOLLOW')
        for non_terminal in self.grammar:
            print('------------|-----------|-------------------|----------------')
            print('\t' + non_terminal + '\t\t|\t  ' + self.is_nullable(non_terminal), end='\t|\t  ')
            print(*self.first_sets[non_terminal], sep=' ', end='')
            for i in range(alt_3_2):
                print('\t', end='')

            print('|\t', end='')
            print(*self.follow_sets[non_terminal], sep=' ')
            alt_3_2 = int(6 / alt_3_2)

        print('\n\nPARSE TABLE:\n\n\t|\t', end='')
        print(*self.terminals, sep='\t|\t', end='\n')
        for non_terminal in self.grammar:
            print('----|-------|-------|-------|-------|-------|-------|-------|-------|-------')
            print(non_terminal, end='\t|')
            print(*self.get_parse_table(non_terminal), sep='|')


if __name__ == '__main__':
    Parser().print_tables()
