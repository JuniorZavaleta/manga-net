a = [
    "+++++++++++++",
    "+++------++++",
    "++++-++++++++",
    "++++-----++++",
    "+++++++-+++++",
    "+++++++-+++-+",
    "+++++++-+++-+",
]

words = ['faisan', 'ana', 'amiga', 'gato', 'pe']


def get_ranges(arr):
    ranges = []
    for s in arr:
        row = []
        start = -1
        end = -1

        for i, c in enumerate(s):
            if c == '-':
                if start == -1:
                    start = i
                end = i

            if c == '+' and end != -1:
                row.append([start, end])
                start = -1
                end = -1
        ranges.append(row)
    return ranges


def show_matrix(arr):
    for s in arr:
        print(s)


# espacio disponibles
ed = get_ranges(a)

words_to_el = []
# Poner palabras en horizontal
for w in words:
    # i: row index, r: conjunto de pares por fila
    for i, r in enumerate(ed):
        # pair [inicio, fin]
        for pair in r:
            if (pair[1] - pair[0] + 1) == len(w):
                a[i] = a[i].replace('-'*len(w), w)
                words_to_el.append(w)

for w in words_to_el:
    words.remove(w)

words_to_el = []
# Poner palabras en vertical con primera letra ya puesta en matriz
for w in words:
    for i, s in enumerate(a):
        index_letra = s.find(w[0])

        # Si hay la primera letras en alguna parte
        if index_letra != -1:
            match = 0
            i_v = i

            for j in range(len(w)):
                if a[i_v][index_letra] == w[j] or a[i_v][index_letra] == '-':
                    match = match + 1
                    i_v = i_v + 1

            if match == len(w):
                i_v = i
                for j in range(len(w)):
                    if a[i_v][index_letra] == '-':
                        temp = list(a[i_v])
                        temp[index_letra] = w[j]
                        a[i_v] = ''.join(temp)
                    i_v = i_v + 1
                words_to_el.append(w)


for w in words_to_el:
    words.remove(w)

# Poner palabras en vertical que faltasen
for w in words:
    for i, s in enumerate(a):
        index_letra = s.find('-')

        match = 0
        i_v = i

        if index_letra != -1 and i_v + len(w) <= len(a):
            for j in range(len(w)):
                if a[i_v][index_letra] == w[j] or a[i_v][index_letra] == '-':
                    match = match + 1
                    i_v = i_v + 1

            if match == len(w):
                i_v = i
                for j in range(len(w)):
                    if a[i_v][index_letra] == '-':
                        temp = list(a[i_v])
                        temp[index_letra] = w[j]
                        a[i_v] = ''.join(temp)
                    i_v = i_v + 1
                words_to_el.append(w)

show_matrix(a)