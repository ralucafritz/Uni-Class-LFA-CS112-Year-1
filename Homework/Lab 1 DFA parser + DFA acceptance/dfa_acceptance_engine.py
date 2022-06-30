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


f = open("dfa_config_file.txt")

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


if ok_final == True :               # Vom verifica sectiunea Transitions, astfel incat tranzitiile sa nu contina
    ok = True                       # stari care nu exista sau litere inexistente in alfabet
    for line in transitions:
        line = line.split(',')
        if line[0] not in list_states or line[1] not in sigma or line[2] not in list_states:
            ok_final = False
    if ok_final == False:
        print("Input invalid!   ~~linie cod 64~~~")
    else:
        print("Input valid!")

else:
    print("Input invalid!   ~~linie cod 69~~")

list_states_f = []
for index in indexFinal:            # Introducem starile finale intr-o lista pentru a avea o lista cu starile finale
    list_states_f.append(list_states[index])

word_to_test = input("Introduceti un cuvant: ")

state_now = list_states[indexStart]

checkWord = True
for letter in word_to_test:
    checkFind = False
    for trans in transitions:
        if (state_now == trans[0]) and (letter == trans[2]):
            state_now = trans[4]
            checkFind = True
            break
    if not checkFind:
        checkWord = False
        break

if state_now in list_states_f and checkWord:
    print("Cuvantul a fost acceptat")
else:
    print("Cuvantul nu a fost acceptat")


#### ab, aaa, acba, merg
#### abc, abcaca nu merg