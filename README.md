# Algoritmi pretrage
Ovaj projekat predstavlja grafičku simulaciju osnovnih algoritama pretraživanja napisanu na
programskom jeziku _Python_. Glavni prozor aplikacije prikazuje dvodimezionalnu mapu
polja različite vrste po kojoj se kreće agent koristeći unapred definisanu pretragu.
Vrsta polja na mapi različito utiče na konačnu cenu putanje. Cilj je dovesti agenta od
startnog do završnog polja putanjom koju izabrani algoritam generiše.  
Pre pokretanja potrebno je instalirati paket _pygame_ (verzija 2.0.2) u okviru _Python_ interpretera.

## Pokretanje projekta iz terminala
Pokretanje projekta se vrši zadavanjem sledeće komande:
```
python main.py <map> <agent>
```
Argument `map` predstavlja relativnu putanju do tekstualne datoteke sa konfiguracijom mape (podrazumevano `maps/map0.txt`).  
Argument `agent` predstavlja naziv klase agenta koji se koristi (podrazumevano `ExampleAgent`).  
  
U okviru prozora prikazana je mapa polja po kojoj se agent kreće, ispod koje se nalazi sekcija sa informacijom o trenutnoj ceni putanje. Pritiskom na dugme _SPACE_ moguće je
pokrenuti i privremeno zaustaviti kretanje agenta. Pritiskom na dugme _ENTER_ moguće je prikazati konačnu putanju do ciljnog polja. Pritiskom na dugme _ESC_ moguće je prekinuti
rad aplikacije i zatvoriti njen glavni prozor. Agent se može kretati samo u
jednom od četiri smera (gore, desno, dole, levo) i u jednom koraku preći tačno jedno polje.  

## Mapa
Mapa je tekstualna datoteka sledećeg formata:  
Prva linija datoteke sadrži zarezom odvojene startne koordinate vrste i kolone polja na kom se nalazi agent.
Druga linija sadrži zarezom odvojene ciljne koordinate vrste i kolone polja na koje agent treba da stigne.
Vrste i kolone su indeksirane počevši od 0. Nakon toga se u proizvoljnom broju redova nalaze oznake polja koja čine mapu.
Na mapi se mogu naći polja data u tabeli.
|Naziv|Oznaka|Cena|
|:---:|:---:|:---:|
|Put  |r     |2   |
|Trava|g     |3   |
|Blato|m     |5   |
|Pesak|d     |7   |
|Voda |w     |500 |
|Stena|s     |1000|

## Agenti sistema
### Aki - _Depth First Search_
Agent koristi strategiju pretrage po dubini (_Depth First Search_), pri čemu prednost daje
prohodnijim poljima (sa manjom cenom), a u slučaju dva ili više takvih
polja bira polje po strani sveta (sever, istok, jug, zapad).

### Jocke - _Breadth First Search_
Agent koristi strategiju pretrage po širini (_Breadth First Search_), pri čemu prednost daje
poljima čiji su susedi kolektivno prohodniji (sa manjom prosečnom
cenom), a u slučaju dva ili više takvih polja bira polje po strani sveta
(sever, istok, jug, zapad).

### Draza - _Branch and Bound Search_
Agent koristi strategiju grananja i ograničavanja (_Branch and Bound Search_), a u slučaju dve
ili više parcijalnih putanja istih cena bira onu sa manje čvorova na
putanji, odnosno proizvoljnu putanju u slučaju dve ili više takvih
parcijalnih putanja.

### Bole - _A* Search_
Agent koristi A* strategiju pretraživanja, pri čemu heuristika predstavlja odabir najprohodnijeg polja koje je najbliže cilju.



