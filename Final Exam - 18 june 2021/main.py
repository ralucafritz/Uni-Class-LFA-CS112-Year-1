# Echipa formata din:
#           Capmare Alex
#           Butelca Radu
#           Fritz Raluca

def sectiuni(nume, str):
    ok = False                              ##### Parcurgem sectiunile
    sec = []
    for line in str:
        if line == nume + ":":              #### se selecteaza liniile dintre numele sectiunii
            ok = True                       #### alese si end
            continue
        if line == "end":
            ok = False
        if ok == True:                     #### si apoi se adauga la lista ce va fi returnata
            sec.append(line)
    return sec

f = open("input.in")                       ### deschidem fisierul pentru configuratie

str = []                                    ### initializam o lista goala pentru toate liniile din fisier

for line in f:
    line = line.strip().lower()
    if len(line) > 0 and line[0] != '#':    ### transformam inputul si il retinem in str daca lungimea liniei
        str.append(line)                    ### este mai mare decat 0 sau daca nu incepe cu # (-> comentarii)


                                            #####
states = sectiuni("states", str)
inp_alph= sectiuni("input alphabet", str)
tape_alph= sectiuni("tape alphabet", str)           ### pentru fiecare sectiune, retinem blocul aferent acesteia
transitions = sectiuni("transitions", str)
start_state = sectiuni("start state", str)
accept_state = sectiuni("accept state", str)
reject_state = sectiuni("reject state", str)                                                        ######

##  accept_state si reject_state se initializeaza ca liste chiar daca au doar o valoare posibila
##  conform modelului pentru celelalte sectiuni. ulterior vom folosi accept_state[0] si reject_state[0]
                                                     ##  dar fiecare are doar o valoare posibila-> se verifica


## verificam daca exista DOAR o stare de acceptare si DOAR o stare de respingere si daca
## starile de accept si reject sunt diferite
if len(accept_state) > 1 or len(reject_state) > 1 or accept_state[0] == reject_state[0]:
    print("Eroare! Input invalid Trebuie sa existe doar o stare de acceptare si/sau respingere si acestea trebuie "
          "sa fie diferite una de cealalta!")
    exit()

## verificam daca alfabetul inputul este inclus in alfabetul tape-ului
for simbol in inp_alph:
    if simbol not in tape_alph:
        print("Input invalid")
        exit()


## Verificam daca exista toate sectiunile
if len(states)*len(inp_alph)*len(tape_alph)*len(transitions)*len(start_state)*len(accept_state)* len(reject_state) == 0:
    print("Nu ati introdus toate sectiunile! Input invalid! ")
    exit()


ok = True

direction = ['l','r','n']    ### initializam o lista cu directii posibile l- left r-right n-neutral (sta pe loc)
### am aflat ca o masina turing poate avea si o pozitie neutra la : https://ai.dmi.unibas.ch/_files/teaching/fs21/theo/slides/theory-b10-handout4.pdf

### verificam ca toate caracterele din tranzitie sa apartina alfabetului tape / states si listei de directii
for line in transitions :
    line = line.split(' ')
    if line[0] not in states or line[1] not in states or line[2] not in tape_alph or line[3] not in tape_alph or line[4] not in tape_alph or line[5] not in tape_alph or line[6] not in direction or line[7] not in direction:
        ok = False

# verificat daca totul a fost ok pana acum si afisiam daca configuratia este valida sau invalida
if not ok:
    print("Input invalid!")
    exit()
else:
    print("Input valid!")

################################################################################################

_string = input("Introduceti stringul: ")     ## stringul pe care il citim

_string = [x for x in _string]                ## transformam stringul in lista pentru a-l putea modifica, acesta va tine locul tape=ului

ok = True
for x in _string :
    if x not in inp_alph :                    ## veriricam ca literele stringului sa apartina alfabetului inputului
        ok = False

if ok == False:
    print("String invalid!")
    exit()

cap1 = 0                                      ## retinem cele 2 capete la polii opusi ai inputului care este introdus in tape
                                              ##(folosim _stringul pe post de tape)
cap2 = len(_string) - 1

stare = start_state[0]                         ##initializam cu starea initiala starea de plecare

while stare != accept_state[0] and stare != reject_state[0]:     ## ruleaza cat timp starea curenta e dif. de cea acceptata sau respinsa => poate rula la infinit
    ok = False

    for trans in transitions:
        trans = trans.split(' ')

        if trans[0] == stare and trans[2] == _string[cap1] and trans[3] == _string[cap2]: ## cautam tranzitia aferenta starii curente si a valorilor capetelor
            stare = trans[1]                   ## modificam starea actuala
            ok = True                          ## marcam gasirea tranzitiei
            _string[cap1] = trans[4]
            _string[cap2] = trans[5]           ## modificam valorile de pe tape cu valorile corespunzatore tranzitiei
            if trans[6] == 'l':                ########
                cap1 = cap1 - 1
                if (cap1 < 0) :
                    cap1 = 0
            elif trans[6] == 'r':
                cap1 = cap1 + 1
                if(cap1 > len(_string) - 1):             # verificam in ce directii ne vom deplasa cu capetele
                    _string.append('_')                  # tratam cazurile in care ajungem la "marginile" tape-ului
                                                         # tape-ul are caractere infinite in dreapta, asadar marim lista tape daca e cazul
            if trans[7] == 'l':                          # val unui capat nu poate fi mai mica decat 0, asadar tratam cazul
                cap2 = cap2 - 1                          # daca directia nu este nici R nici L => este N => capatul respectiv nu isi va modifica pozitia
                if (cap2 < 0):
                    cap2 = 0
            elif trans[7] == 'r':
                cap2 = cap2 + 1
                if (cap2 > len(_string) - 1):
                    _string.append('_')                                                                                    ########

            break
    if ok == False:
        print("Nu s-a gasit tranzitie, eroare input!")
        exit()

    ### daca s-a ajuns aici inseamna ca starea actuala este fie cea de acceptare fie cea de respingere
if stare == accept_state[0]:
    print("Cuvant acceptat")
else:
    print("Cuvant respins")


## pentru exercitiul nr 2 am folosit fisierul "input.in" ca si configuratie
## pentru exercitiul nr 3 am folosit fisierul "prefix.in" ca si configuratie
## pentru exercitiul nr 4 am folosit fisierul "suma.in" ca si configuratie



## print la tape-ul final pentru suma.in (EXERCITIUL 4)

count = 0
for simbol in _string:
    if simbol != '_':
        print(simbol, end=" ")
        count = count + 1
print("")
print(count)
