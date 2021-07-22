def dfa(input_string, transition_function, state='S'):
    if len(input_string) == 0:
        if state == 'F':
            print("String Accepted!!")
        else:
            print("String Rejected!!")
        return

    new_state = transition_function.get(state).get(input_string[0],'T')

    dfa(input_string[1:], transition_function, new_state)


if __name__ == "__main__":
    transition_dictionary = {
        'F':
            {'a': '2','b': '4'},
        '2':
            {'a': 'F','b': '3'},
        '3':
            {'a': '4', 'b': '2'},
        '4':
            {'a': '3', 'b': 'F'},
        'T':
            {'':'T'}
    }

    for i in range(5):
        dfa(input("Enter String: "), transition_dictionary,'F')