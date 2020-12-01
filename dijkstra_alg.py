#!/usr/local/bin/python3
# coding=utf8

# Adjazenzmatrizen
matrix = [
    [0,1,0,0,3,0],
    [1,0,4,5,0,0],
    [0,4,0,0,2,0],
    [0,5,0,0,1,3],
    [3,0,2,1,0,2],
    [0,0,0,3,2,0]
]
matrix2 = [
    [0,4,0,0],
    [4,0,2,5],
    [0,2,0,1],
    [0,5,1,0]
]

matrix3 = [
    [0,3,2,0,0,0],
    [3,0,1,0,0,0],
    [2,1,0,4,1,0],
    [0,0,4,0,0,3],
    [0,0,1,0,0,0],
    [0,0,0,3,0,0]
]

# im Code unten beschrieben
def findAll(a, n):
    index = 0
    product = []
    for i in a:
        if i == n:
            product.append([n, index])
        index += 1
    return product

# Liest Adjazenzmatrix und gibt Liste aus
def findNumInArray(a):
    index1 = 0
    index2 = 0
    pos = []
    for i in a:
        for j in i:
            if j != 0:
                if not [index2, index1, j] in pos:
                    pos.append([index1, index2, j])
            index2 += 1
        index2 = 0
        index1 += 1
    return pos

# Aktuelle Matrix
currMatrix = matrix
kanten = findNumInArray(currMatrix)
knoten = [i for i in range(len(currMatrix))]

print("weights: {}".format(kanten))
print("nodes: {}".format(knoten))
print("")

def dijkstra(knoten, kanten, start, ziel):

    # Variablen
    roteListe = [knoten[0]]
    blaueListe = []
    kennzahl = [-1] * (len(kanten)+1)
    kennzahl[0] = 0
    aktuelleStadt = start
    aktuelleKennzahl = 0
    index = 0

    while aktuelleStadt != ziel:

        # Nachbarstädte herausfinden
        nachbarStaedte = []
        for i in range(len(kanten)):
            if kanten[i][0] == knoten[knoten.index(aktuelleStadt)]:
                nachbarStaedte.append(kanten[i])
        # print("nachbarStaedte: {}".format(nachbarStaedte))

        # # Prüfen ob es Nachbarstädte hat und ob aktuelleStadt Ziel ist -> nur bei Graph 3 (matrix3)
        # if nachbarStaedte == [] and aktuelleStadt != ziel:
        #     print("*************")
        #     knoten.remove(aktuelleStadt)
        #     for i in kanten:
        #         if i[1] == aktuelleStadt:
        #             kanten.remove(i)
        #     print(dijkstra(knoten, kanten, start, ziel))

        # Prüfen der Kennzahl
        for j in range(len(nachbarStaedte)):
            summe = aktuelleKennzahl + nachbarStaedte[j][2]
            kennzahlIndex = kanten.index(nachbarStaedte[j])+1
            if kennzahlIndex > len(kennzahl)-1:
                #print("index out of range..")
                kennzahlIndex -= 1
            #print("aK: {}, nbSW: {}, summe: {}".format(aktuelleKennzahl, nachbarStaedte[j][2], summe))
            if kennzahl[kennzahlIndex] == -1:
                kennzahl[kennzahlIndex] = summe
            elif kennzahl[kennzahlIndex] > summe:
                kennzahl[kennzahlIndex] = summe

        #print("kz: {}".format(kennzahl))

        # Herausfinden, welcher Wert benötigt wird
        temporary = []
        kzIndexList = [i for i in range(len(kennzahl))]
        for k in range(len(kennzahl)-1):
            if kennzahl[k] != -1:
                if not kanten[kzIndexList[k]][1] in roteListe:
                    temporary.append(kennzahl[k])

        temporary.pop(0)
        #print("temporary: {}".format(temporary))

        # min() nimmt immer erstmögliche kleinste Zahl -> [3, 5, 6, 3] also index 0 -> mein Code findAll() kann unterscheiden
        allMinimum = findAll(kennzahl, min(temporary))
        #print(allMinimum)
        minimum = allMinimum[-1][1]
        #print("minimum: {}".format(minimum))
        aktuelleStadt = kanten[minimum-1][1]
        aktuelleKennzahl = kennzahl[minimum]
        roteListe.append(aktuelleStadt)

        # Blaue Liste dient für das Ergebnis, um zu sehen welche Knoten und Werte angenommen wurden
        if minimum == len(kanten)-1:
            blaueListe.append(kanten[minimum])
        else:
            blaueListe.append(kanten[minimum-1])
        print("\ncurrent node: {}".format(aktuelleStadt))
        #print("aK: {}".format(aktuelleKennzahl))
        print("red list: {}".format(roteListe))
        #print("blaueListe: {}".format(blaueListe))
        #print("kz: {}".format(kennzahl))

        nachbarStaedte, temporary = [], []

    # Ab hier werden Knoten und Werte, die angenommen worden sind, herausgefunden

    count = 1
    for i in range(len(blaueListe)-1):
        wert = blaueListe[i]
        for j in range(1, len(blaueListe)):
            if blaueListe[j][0] == wert[1]:
                count += 1
        if count == 1:
            if wert[1] == ziel:
                pass
            else:
                blaueListe.remove(wert)

    knotenBesucht = []
    for i in range(len(blaueListe)):
        knotenBesucht.append(blaueListe[i][0])
        if i == len(blaueListe)-1:
            knotenBesucht.append(blaueListe[i][1])

    werteAngenommen = [0]
    index1 = 0
    index2 = 1
    for i in range(len(knotenBesucht)-1):
        for j in range(len(kanten)):
            e1 = knotenBesucht[index1]
            e2 = knotenBesucht[index2]
            if kanten[j][0] == e1 and kanten[j][1] == e2:
                werteAngenommen.append(kanten[j][2])
        index1 += 1
        index2 += 1

    for i in range(1, len(werteAngenommen)):
        index99 = i - 1
        werteAngenommen[i] += werteAngenommen[index99]

    return "\nvisited nodes: {}\ncurrent weighting on the node: {}\n".format(knotenBesucht, werteAngenommen)


start = int(input("enter start node: "))
ziel = int(input("enter target node: "))
print(dijkstra(knoten, kanten, start, ziel))
