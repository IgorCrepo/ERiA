import copy as cp

# wczytywanie mapy
plik = open("grid.txt", "r+")

# wczytanie wszystkich linii pliku grid.txt do zmiennej map
mapa = []
for x in range(10): # 20 dla grida 20x20 5
    w = plik.readline()
    mapa.append(w.split())

#-----------------------------------------------

for x in range(len(mapa)):
    for y in range(len(mapa[0])):
        mapa[x][y] = int(mapa[x][y])

#-------------------------------------------------

k = len(mapa) - 1

lista_o = []  # tablica otwarta
lista_z = []  # tablica zamknięta
lista_z.append([k, 0, 0, 0, None, None])  # [Y, X, koszt pojedyńczego ruchu , koszt całkowity, Y rodzica, X rodzica]
start = [k, 0, 0, 0, None, None]
koniec = [0, k, 0, 0, None, None]

#------------------------------------------------------------------------------
def idy(y): # zamiana na poprawny indeks osi y do obliczeń
    indeks = {0 : 19, 1: 18, 2: 17, 3: 16, 4: 15, 5: 14, 6: 13, 7: 12, 8: 11,
              9: 10, 10: 9, 11: 8, 12: 7, 13: 6, 14: 5, 15: 4, 16:3, 17:2,
              18: 1, 19:0}
    return indeks.get(y)

#-------------------------------------------------------------------------------

def dodaj_do_LO(pkt):
    k = False

    for x in range(len(lista_o)):
        if pkt[0] == lista_o[x][0] and pkt[1] == lista_o[x][1]:
            k = True
            if pkt[3] < lista_o[x][3]:
                lista_o[x] = pkt

    if k == False:
        lista_o.append(pkt)

#-----------------------------------------------------------------------------------

def dodaj_do_LZ(): # funkcja dodająca punkt z listy otwartej do listy zamkniętej
    if len(lista_o) > 1:
        min = lista_o[-1] # dodawany jest punkt o najmniejszym koszcie z listy otwartej
        for z in range(len(lista_o)-1, -1, -1): # jeżeli dwa punkty mają taki sam koszt to pierwszeństwo ma ten naj
            if lista_o[z][3] < min[3]:
                min = lista_o[z]

        lista_z.append(min)
        lista_o.remove(min)

    elif len(lista_o)== 1:
        el = lista_o.pop(0)
        lista_z.append(el)

#-----------------------------------------------------------------------------------

def spr_czy_LZ(y, x): # sprawdza, czy kratka nie jest z LZ
    warunek = False
    for j in range(len(lista_z)):
        if y == lista_z[j][0] and x == lista_z[j][1]:
            warunek = True
            break

    return warunek

#-------------------------------------------------------------------------------

def utworz_pkt(y, x, pkt_rodzic):

    koszt_p = pkt_rodzic[2] + 1
    y_rodzica =  pkt_rodzic[0]
    x_rodzica =  pkt_rodzic[1]
    koszt_fin = koszt_p + (((idy(y) - idy(koniec[0]))**2 + (x - koniec[1])**2)**(1/2)) # funkcja obliczająca nasz całkowity koszt ruchu
    nowy_punkt = [y, x, koszt_p, koszt_fin, y_rodzica, x_rodzica ] # nowy punkt
    return nowy_punkt

#--------------------------------------------------------------------------------

obecny = lista_z[0]
#print(lista_z[0][0], lista_z[0][1])
i = 0
d = k + 1
warunek = True
while(warunek):

    pkt = obecny

    #pkt dolny
    p_d = pkt[0] + 1 #punkt dolny to punkt o indeksie pionowym większym o jeden od obecnego punktu
    if p_d < d: #sprawdzenie czy indeks nie wychodzi poza mapę, czy się w niej zawiera
        if mapa[p_d][pkt[1]] != 5: # jeżeli sprawdzany punkt jest w mapie to sprawdzamy czy nie jest on przeszkodą, które omijamy
            if spr_czy_LZ(p_d, pkt[1]) == False:
                #obliczamy/tworzymy punkt
                pkt_d = utworz_pkt(p_d, pkt[1], pkt)  # tworzenie nowego punktu
                dodaj_do_LO(pkt_d) # dopisanie punktu do tablicy tymczasowej

    #pkt lewy
    p_l = pkt[1] -1
    if p_l > -1:
        if mapa[pkt[0]][p_l] != 5:
            if spr_czy_LZ(pkt[0], p_l) == False:
                pkt_d = utworz_pkt(pkt[0], p_l, pkt)
                dodaj_do_LO(pkt_d) # dopisanie punktu do tablicy tymczasowej

    #pkt górny
    p_g = pkt[0] -1
    if p_g > -1:
        if mapa[p_g][pkt[1]] != 5:
            if spr_czy_LZ(p_g, pkt[1]) == False:
                pkt_d = utworz_pkt(p_g, pkt[1], pkt)
                dodaj_do_LO(pkt_d)

    #pkt prawy
    p_p = pkt[1] + 1
    if p_p < d:
        if mapa[pkt[0]][p_p] != 5:
            if spr_czy_LZ(pkt[0], p_p) == False:
                pkt_d = utworz_pkt(pkt[0], p_p, pkt)
                dodaj_do_LO(pkt_d) # dopisanie punktu do tablicy tymczasowej


    dodaj_do_LZ() # dodanie punktu z listy otwartej do listy zamkniętej

    obecny = lista_z[-1]

    # --------------------------------------------------------------------------------------------------
    if(obecny[0] == koniec[0] and obecny[1] == koniec[1]):
        warunek = False
        # porządkowanie danych do wyznaczenia ścieżki
        n = []  # tablica, do  której zapisywana jest lista zamknięta jedynie z współrzędnymi i rodzicami

        for t in lista_z:
            t = t[:2] + t[4:]
            n.append(t)

        n.reverse()

        sciezka = []
        sciezka.append(n[0])

        # znajdywanie ścieżki
        i = 0
        warunek = True
        while (i < len(n) and warunek == True):
            j = i + 1
            while (j < len(n)):
                if sciezka[i][2] == n[j][0] and sciezka[i][3] == n[j][1]:
                    sciezka.append(n[j])
                    # print(sciezka)
                    break
                j += 1
            if sciezka[-1][2] == None and sciezka[-1][3] == None:
                warunek = False
            i += 1

        sciezka.reverse()
        # print(sciezka)

        mapa2 = cp.deepcopy(mapa)

        # zaznaczenie ściezki
        for x in sciezka:
            mapa2[x[0]][x[1]] = 3

        # wyświetlenie ścieżki na mapie
        for x in mapa2:
            print(x)

    # --------------------------------------------------------------------------------
    # jeżeli lista otwarta jest pusta to brak rozwiązania (brak nowych punktów)
    if not lista_o:
        print("Brak rozwiązania")
        break
