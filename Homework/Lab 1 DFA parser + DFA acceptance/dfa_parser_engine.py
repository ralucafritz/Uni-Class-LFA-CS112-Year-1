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
for line in states:
    s_count = s_count + line.count('s')
    f_count = f_count + line.count('f')
if s_count > 1 or f_count == 0:
    ok_final = False

states_final = []                   # Convertim lista States, a.i sa retinem din fiecare
for line in states:                 # linie doar primul caracter, adica starile
    states_final.append(line[0])


if ok_final == True :               # Vom verifica sectiunea Transitions, astfel incat tranzitiile sa nu contina
    ok = True                       # stari care nu exista sau litere inexistente in alfabet
    for line in transitions:
        line = line.split(',')
        if line[0] not in states_final or line[1] not in sigma or line[2] not in states_final:
            ok_final = False
    if ok_final == False:
        print("Input invalid!   ~~linie cod 64~~~")
    else:
        print("Inputul valid!")

else:
    print("Input invalid!   ~~linie cod 69~~")






