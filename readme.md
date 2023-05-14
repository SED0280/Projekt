# Hledání nejkratší cesty v bludišti
## Textový popis
Jedná se o projekt do předmětu Vědecké výpočty v pythonu.
Tento projekt se zabývá řešením (hledáním nejkratší cesty) a také základním generováním bludišť. Základním vstupem bude bludiště n x m, přičemž vstup do bludiště bude vždy levý horní roh a výstup bude vždy pravý dolní roh. Z jedné buňky do druhé se lze dostat pouze přes společnou hranu (nikoliv přes roh). Cílem projektu je implementovat algoritmy pro načítání, hledání nejkratší cesty a generování bludiště.

Na začátku bude implementována funkce pro načítání bludiště z CSV souboru. Tato funkce bude umět načítat bludiště o libovolném rozměru n x m a uložit ho do paměti v podobě NumPy matice s True/False hodnotami (True = buňka je neprůchozí). Poté bude implementován algoritmus pro hledání nejkratší cesty. Poslední částí bude vytvoření generátoru bludiště za použití algoritmu pro hledání nejkratší cesty.

Výstup bude formou obrázku (černá = neprostupná část, bílá = průchozí, červená = nejkratší cesta).

## Popis metod knihovny
### nactiBludiste(mazefile)
Tato metoda načte bludiště z csv souboru mazefile a vrátí pole s tímto bludištěm kde 0 je volné místo a 1 je zeď.
### IsMaze(maze)
Metoda zjistí ze vstupního pole zda toto bludiště má řešení. Pokud má řešení vrácí hodnotu True, pokud nemá řešení vrací hodnotu False.
### printMaze(maze)
Metoda vypíše pole pomocí znaků ■ a mezery, kde ■ je zeď bludiště a mezera je volné místo.
### makeIncidencniMatice(maze)
Tato metoda zjistí incidenční matici ze zadaného pole maze a vrací ji zpět společně s indexy cest v bludišti.
### DijkstraFindPath(inmat,nodes)
Tato metoda najde nejkratší cestu v bludišti zadaného pomocí incidenční matice a indexů volných míst v bludišti. Cesta se uloží do jednorozměrného pole s indexy míst v bludišti. Tohle jednorozměrné pole je poté vráceno. 
### printMazePath(maze,path)
Metoda printMazePath funguje obdobně jako printMaze, kde se bludiště vypíše pomocí znaků ■ a mezery, ale v této funkci se vypíše tečka na místech s indexy z pole path.
### generateMaze(n,m,choice = "random")
Tato metoda vygeneruje bludište o zadaných rozměrech n a m. Bludiště se generuje podle volby v promenné choice. Pokud není volby vybranná zvolí se volba random.
### volby:
* random: náhodně přidává volné místa dokud bludiště nemá řešení.
* grid: náhodně přidává volné místa do tvaru mřížky dokud bludiště nemá řešení.
* clean: vytvoří volnou plochu bez zdí.
* zigzag1-4: tyto volby generují různě otočené bludiště přibližně ve tvaru písmena S nebo Z.
* zigzagRandom: vytvoří bludiště náhodně z jedné z možností zigzag1 až zigzag4.
* snake: bludiště má jen jednu cestu která jde postupně dolů ze strany na stranu.
### mazePathToImg(maze,path,name)
Poslední metoda mazePathToImg uloží bludiště do obrázku png ve kterém jsou znázorněny zdi černou barvou, volné místa bílou barvou a nejkratší cesta červenou barvou.

Všechny metody knihovny mazelib.py jsou použity v Jupyter notebooku VVP_Project.ipynb.