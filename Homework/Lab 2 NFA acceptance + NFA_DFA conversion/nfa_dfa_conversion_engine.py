def sectiuni(nume, str):
    ok = False
    sec = []
    for line in str:
        if line == nume + ":":
            ok = True
            continue 
        if line == "end":
            ok = False
        if ok == True:
            sec.append(line)
    return sec


f = open("nfa_config_file.txt", 'r')

str = []

for line in f:
    line = line.strip().lower()
    if len(line) > 0 and line[0] != '#':
        str.append(line)

sigma = sectiuni("sigma", str)
states = sectiuni("states", str)
transitions = sectiuni("transitions", str)


if len(sigma)*len(states)*len(transitions) == 0:        # Verificam daca exista toate sectiunile
    print("Nu ati introdus toate sectiunile!")
    exit()

ok_final = True                                 # Vom verifica sectiunea States,astfel incat sa nu contina
ok = True                                       # 2 stari initiale, si sa contina cel putin o stare finala
s_count = 0
f_count = 0
indexFinal = []
indexStart = 0
index = 0
for line in states:
    if line.count('s') !=0:                     # Retinem indexul starii initiale
        indexStart = index
        s_count += line.count('s')
    if line.count('f') != 0:                    # Retinem indexii starilor finale
        indexFinal.append(index)
        f_count += line.count('f')
    index += 1

if s_count > 1 or f_count == 0:
    ok_final = False

list_states = []                   # Convertim lista States, a.i sa retinem din fiecare
for line in states:                 # linie doar primul caracter, adica starile
    list_states.append(line[0])


if ok_final:               # Vom verifica sectiunea Transitions, astfel incat tranzitiile sa nu contina
    ok = True                       # stari care nu exista sau litere inexistente in alfabet
    for line in transitions:
        line = line.split(',')
        if line[0] not in list_states or line[1] not in sigma or line[2] not in list_states:
            ok_final = False
    if not ok_final:
        print("Input invalid!   ~~linie cod 64~~~")
    else:
        print("Input valid!")

else:
    print("Input invalid!   ~~linie cod 69~~")

list_states_f = []
for index in indexFinal:            # Introducem starile finale intr-o lista pentru a avea o lista cu starile finale
    list_states_f.append(list_states[index])


list_NFA = []
list_DFA = []

state_DFA_start = list_states[indexStart]
sigma_DFA = sigma
states_NFA = []

for state in states:
    states_NFA.append(state[0])

now_states = []
letters = []
next_states = []

for trans in transitions:
    now_state = trans[0]
    letter = trans[2]
    next_state = trans[4]
    if now_state not in now_states:
        now_states.append(now_state)
        index_now_state = now_states.index(now_state)
        letters.append([])
        next_states.append([])
        for element in sigma:
            letters[index_now_state].append(element)
            next_states[index_now_state].append([])

        for j in range(len(letters[index_now_state])):
            if letters[index_now_state][j] == letter:
                next_states[index_now_state][j].append(next_state)
    else:
        index_now_state = now_states.index(now_state)

        for j in range(len(letters[index_now_state])):
            if letters[index_now_state][j] == letter:
                next_states[index_now_state][j].append(next_state)

list_NFA.append(now_states)
list_NFA.append(letters)
list_NFA.append(next_states)

for state in list_states:
    if state not in list_NFA[0]:
        list_NFA[0].append(state)
        index_now_state = list_NFA[0].index(state)
        list_NFA[1].append([])
        list_NFA[2].append([])
        for element in sigma:
            list_NFA[1][index_now_state].append(element)
            list_NFA[2][index_now_state].append([])

        for j in range(len(list_NFA[1][index_now_state])):
           next_states[index_now_state][j].append([])


print("\nNFA:")
print("States: ")
for state in list_states:
    print(state, end=" ")

print("")

print("Sigma: ")
for sigma_element in sigma:
    print(sigma_element, end=" ")

print("")

print("Initial state: ", "\n", list_states[indexStart])

print("Final states: ")
for state in list_states_f:
    print(state, end=" ")

print("")

print("Transitions:\n")

for state_key in list_NFA[0]:
    print("State: ", state_key)
    for letter_key in list_NFA[1][list_NFA[0].index(state_key)]:
        print("Letter: ", letter_key)
        for j in range(len(list_NFA[1][list_NFA[0].index(state_key)])):
            if list_NFA[1][list_NFA[0].index(state_key)][j] == letter_key:
                print("States ", list_NFA[2][list_NFA[0].index(state_key)][j])

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("----------------------------------------------------------------")

print("")

states_DFA = []
letters_DFA = []
next_states_DFA = []
states_DFA.append(list_NFA[0][indexStart])

for i in range(len(list_NFA[0])):
    new_state = ""
    letters_DFA.append(list_NFA[1][i])
    new_states_now = []
    next_states_DFA.append([])
    for element in sigma:
        next_states_DFA[i].append([])
    for j in range(len(list_NFA[1][i])):
        new_state = ""
        k = 0
        while k < len(list_NFA[2][i][j]):
            if list_NFA[2][i][j][k] is not []:
                for state_now in list_NFA[2][i][j][k]:
                    new_state += state_now
            else:
                new_state = ""
            k += 1
        if new_state != "":
            next_states_DFA[i][j].append(new_state)
            new_states_now.append(new_state)


    for state in new_states_now:
        if state not in states_DFA:
            states_DFA.append(state)

list_DFA.append(states_DFA)
list_DFA.append(letters_DFA)
list_DFA.append(next_states_DFA)
list_states_f_DFA = list_states_f


print("\nDFA:")
print("States: ")
for state in states_DFA:
    print(state, end=" ")

print("")

print("Sigma: ")
for sigma_element in sigma_DFA:
    print(sigma_element, end=" ")

print("")

print("Initial state: ", "\n", state_DFA_start)

print("Final states: ")
for state in list_states_f_DFA:
    print(state, end=" ")

print("")

print("Transitions:\n")

for state_key in list_DFA[0]:
    print("State: ", state_key)
    for letter_key in list_DFA[1][list_DFA[0].index(state_key)]:
        print("Letter: ", letter_key)
        for j in range(len(list_DFA[1][list_DFA[0].index(state_key)])):
            if list_DFA[1][list_DFA[0].index(state_key)][j] == letter_key:
                print("States ", list_DFA[2][list_DFA[0].index(state_key)][j])

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("----------------------------------------------------------------")

print("")