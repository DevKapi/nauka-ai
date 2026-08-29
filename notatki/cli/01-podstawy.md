# Moduł 1 — CLI (podstawy pracy w terminalu)

> Notatka z kursu pracy z agentami AI.
> Środowisko: Windows + WSL 2 (Ubuntu), shell: bash.

---

## Spis treści

1. [Czym jest CLI](#1-czym-jest-cli)
2. [Ścieżki — fundament wszystkiego](#2-ścieżki--fundament-wszystkiego)
3. [Poruszanie się po katalogach](#3-poruszanie-się-po-katalogach)
4. [Czytanie wyniku `ls -l`](#4-czytanie-wyniku-ls--l)
5. [Praca z plikami](#5-praca-z-plikami)
6. [Przekierowania — znak `>` dokładnie](#6-przekierowania--znak--dokładnie)
7. [Potoki](#7-potoki)
8. [Wyszukiwanie: grep i find](#8-wyszukiwanie-grep-i-find)
9. [Historia i skróty klawiszowe](#9-historia-i-skróty-klawiszowe)
10. [Typowe błędy](#10-typowe-błędy)
11. [Zastosowanie w QA i przy pracy z agentami AI](#11-zastosowanie-w-qa-i-przy-pracy-z-agentami-ai)
12. [Ściąga — wszystkie komendy](#12-ściąga--wszystkie-komendy)
13. [Pytania testowe](#13-pytania-testowe)

---

## 1. Czym jest CLI

**CLI** = Command Line Interface, czyli interfejs wiersza poleceń. Zamiast klikać w ikony, wpisuje się nazwę polecenia i wciska Enter.

Trzy pojęcia, które łatwo pomylić:

| Pojęcie | Co to jest | Przykład |
|---|---|---|
| **Terminal** | okno programu — sam "monitor i klawiatura" | Windows Terminal, okno WSL |
| **Shell (powłoka)** | program, który czyta polecenia i je wykonuje | `bash`, `zsh` |
| **Polecenie** | konkretny program uruchamiany przez shell | `ls`, `git`, `claude` |

Terminal sam z siebie nic nie rozumie. Nie wie, czym jest `cd`. Przekazuje tylko wpisane znaki do shella i wyświetla to, co shell odeśle. Cała logika (interpretacja poleceń, potoki, zmienne, historia) siedzi w bashu. Dlatego mówi się „skrypt bashowy", a nie „skrypt terminalowy".

### Anatomia promptu

```
kapi@kapikomp:~/nauka-ai$
```

| Fragment | Znaczenie |
|---|---|
| `kapi` | nazwa użytkownika |
| `@kapikomp` | nazwa maszyny |
| `~/nauka-ai` | **gdzie aktualnie stoję** (bieżący katalog) |
| `$` | koniec promptu. `$` = zwykły użytkownik, `#` = root |

Najważniejszy element to ścieżka. Terminal zawsze „stoi" w jakimś katalogu i większość poleceń działa względem tego miejsca. To źródło większości pomyłek początkujących.

---

## 2. Ścieżki — fundament wszystkiego

### Struktura katalogów w Linuksie

Linux nie ma dysków `C:` i `D:`. Ma **jedno drzewo** zaczynające się od `/` (root, korzeń).

```
/
├── home/
│   └── kapi/            ← katalog domowy, skrót: ~
│       └── nauka-ai/
├── etc/                 ← konfiguracja systemu
├── usr/                 ← zainstalowane programy
├── tmp/                 ← pliki tymczasowe
└── mnt/
    └── c/               ← dysk C: z Windowsa (most WSL ↔ Windows)
```

### Ścieżka bezwzględna vs względna

To jest **najważniejsze pojęcie całego modułu**.

**Ścieżka bezwzględna (absolutna)** zaczyna się od `/` i opisuje pełną drogę od korzenia. Działa **zawsze**, niezależnie od tego, gdzie stoisz:

```
/home/kapi/nauka-ai/notatki/cli/01-podstawy.md
```

**Ścieżka względna** nie zaczyna się od `/` i jest liczona **od miejsca, w którym stoisz**:

```
notatki/cli/01-podstawy.md
```

### Jedna zasada, która rozwiązuje 90% problemów

> **`/` na początku znaczy „licz od korzenia dysku".
> Jego brak znaczy „licz od miejsca, gdzie stoję".**

Jeden ukośnik decyduje o wszystkim.

### Symbole specjalne

| Symbol | Znaczenie |
|---|---|
| `.` | katalog bieżący („tutaj") |
| `..` | katalog nadrzędny („jeden poziom wyżej") |
| `~` | katalog domowy, czyli `/home/kapi` |
| `-` | poprzedni katalog (używane z `cd -`) |

`..` można powtarzać i używać w środku ścieżki:

```
/home/kapi/nauka-ai/notatki/cli     ← stoję tutaj
                    /notatki        ← ..
        /nauka-ai                   ← ../..
```

```bash
head -n 2 ../../README.md     # wyjdź 2 poziomy w górę i weź stamtąd plik
```

### Ten sam plik na trzy sposoby

Stojąc w `~/nauka-ai/notatki/cli`, wszystkie trzy wskazują to samo:

```bash
cat ../../README.md                         # względna, przez ..
cat ~/nauka-ai/README.md                    # przez ~
cat /home/kapi/nauka-ai/README.md           # bezwzględna
```

**Kiedy której używać:**

- **względna** — szybka, do codziennej pracy w jednym katalogu
- **bezwzględna** — do skryptów, konfiguracji, poleceń dla agentów AI. Jest odporna na to, gdzie ktoś stoi. Dlatego dokumentacja prawie zawsze podaje ścieżki bezwzględne.

### Metoda sprawdzania ścieżki przed uruchomieniem

1. Popatrz na prompt — masz tam swoją lokalizację cały czas.
2. Doklej do niej ścieżkę, którą chcesz wpisać, i przeczytaj wynik.
3. Jeśli wyszedł potworek typu `.../notatki/cli/notatki/cli/`, to widać duplikat.
4. Testuj przez `ls` — to polecenie niczego nie zmienia:

```bash
ls notatki/cli        # jeśli błąd tutaj, to cp/mv/head też zawiedzie
```

### Wielkość liter ma znaczenie

Linux rozróżnia wielkie i małe litery. `Notatki` i `notatki` to dwa różne katalogi.

Wyjątek: `/mnt/c`, bo Windows nie rozróżnia. Dlatego `cd users` działa tam, gdzie katalog nazywa się `Users`. **To pułapka** — kod działa lokalnie na Windowsie, a na serwerze Linuksowym się wysypuje, bo ktoś napisał `Config.json` zamiast `config.json`. W QA takie błędy zgłasza się regularnie.

---

## 3. Poruszanie się po katalogach

### `pwd` — gdzie jestem

*print working directory*

```bash
pwd
# /home/kapi/nauka-ai
```

**Odruch: przy każdym błędzie „No such file or directory" najpierw `pwd`.**

### `ls` — co tu jest

*list*

```bash
ls                    # zawartość bieżącego katalogu
ls -l                 # long: uprawnienia, właściciel, rozmiar, data
ls -a                 # all: także pliki ukryte (zaczynające się od kropki)
ls -la                # połączone flagi
ls -lh                # human-readable: 4.2K zamiast 4300
ls -lt                # sortuj po dacie modyfikacji (najnowsze u góry)
ls -ltr               # to samo, ale odwrócone — najnowsze na dole
ls -A                 # ukryte, ale bez wpisów . i ..
ls ~/nauka-ai         # zawartość innego katalogu, BEZ wchodzenia do niego
ls /etc               # to samo, ścieżka bezwzględna
```

**`ls` nigdy nie zmienia twojego położenia.** Możesz podać dowolną ścieżkę i po wykonaniu nadal stoisz tam, gdzie stałeś. To główna różnica względem `cd`.

Warianty sortowania po czasie:

| Flaga | Sortuje wg |
|---|---|
| `-t` | czas modyfikacji zawartości (mtime) — zwykle o to chodzi |
| `-c` | czas zmiany metadanych, np. uprawnień (ctime) |
| `-u` | czas ostatniego odczytu (atime) |
| `-r` | odwraca kolejność |

`ls -ltr` to jedno z najczęściej używanych poleceń przy grzebaniu w logach — najświeższe pliki lądują tuż nad promptem.

### `cd` — zmień katalog

*change directory*

```bash
cd nauka-ai                     # wejdź do podkatalogu (ścieżka względna)
cd ..                           # poziom wyżej
cd ../..                        # dwa poziomy wyżej
cd ~                            # do katalogu domowego
cd                              # to samo, bez argumentu
cd /home/kapi/nauka-ai          # ścieżka bezwzględna
cd -                            # wróć do poprzedniego katalogu
```

**`cd` działa tylko na katalogach.** Do pliku nie da się „wejść" — można go tylko otworzyć (`cat`, `less`, `nano`). Próba `cd plik.md` daje `Not a directory`.

### `tree` — struktura jako drzewo

```bash
tree                     # całe drzewo od bieżącego katalogu
tree -L 2                # tylko 2 poziomy w głąb
tree -a                  # z ukrytymi
tree -a -L 2             # oba naraz
tree ~/nauka-ai          # drzewo innego katalogu
```

Instalacja, jeśli brakuje: `sudo apt install tree`

**Uwaga na flagi z argumentem.** `-L` wymaga liczby, więc musi stać na końcu sklejonej grupy albo osobno:

```bash
tree -a -L 2      # najczytelniej
tree -aL 2        # też poprawnie
tree -La 2        # ryzykowne — -L może połknąć literę "a" jako argument
```

`tree` liczy też katalog startowy, więc `4 directories` przy trzech widocznych podkatalogach to nie błąd.

### Jak sobie radzić, gdy nie wiesz

```bash
ls --help         # szybka lista opcji
man ls            # pełna dokumentacja. Wyjście: q
which git         # gdzie na dysku leży dany program
type cd           # czy to program, czy wbudowane polecenie shella
```

W `man`: strzałki przewijają, `/tekst` szuka, `q` wychodzi.

**Uwaga na składnię `man`.** To program wyświetlający instrukcję *innego* programu, więc nazwa idzie jako argument, nie jako flaga:

```bash
man ls        # DOBRZE: pokaż instrukcję programu ls
man -ls       # ŹLE: przekaż manowi flagi -l i -s
```

---

## 4. Czytanie wyniku `ls -l`

```
drwxr-xr-x  8 kapi kapi  4096 Aug 28 22:18 .claude
│└─┬┘└┬┘└┬┘  │   │    │     │        │        │
│  │  │  │   │   │    │     │        │        └─ nazwa
│  │  │  │   │   │    │     │        └────────── data modyfikacji
│  │  │  │   │   │    │     └─────────────────── rozmiar w bajtach
│  │  │  │   │   │    └───────────────────────── grupa
│  │  │  │   │   └────────────────────────────── właściciel
│  │  │  │   └────────────────────────────────── liczba dowiązań
│  │  │  └────────────────────────────────────── prawa: inni
│  │  └───────────────────────────────────────── prawa: grupa
│  └──────────────────────────────────────────── prawa: właściciel
└─────────────────────────────────────────────── typ
```

**Pierwszy znak — typ obiektu:**

| Znak | Co to |
|---|---|
| `-` | zwykły plik |
| `d` | katalog |
| `l` | dowiązanie symboliczne (skrót) |

**Dziewięć kolejnych znaków — uprawnienia** w trzech grupach po trzy (właściciel / grupa / pozostali):

| Litera | Dla pliku | Dla katalogu |
|---|---|---|
| `r` (read) | można odczytać zawartość | można wypisać zawartość przez `ls` |
| `w` (write) | można zmodyfikować | można tworzyć i kasować pliki w środku |
| `x` (execute) | można uruchomić jako program | można **wejść** przez `cd` |

`x` przy katalogu myli — katalog nie jest programem, `x` oznacza tam prawo wejścia.

Przykłady:

```
-rw-------  .bash_history    właściciel czyta i pisze, reszta nic
-rw-r--r--  .bashrc          właściciel czyta i pisze, reszta tylko czyta
drwxr-xr-x  nauka-ai         katalog: właściciel pełne prawa, reszta wchodzi i czyta
```

**Rozmiar przy katalogu (4096) to nie waga zawartości**, tylko rozmiar wpisu w systemie plików. Do faktycznego rozmiaru: `du -sh nazwa_katalogu`.

**Znaki zapytania** (`-?????????`) oznaczają, że `ls` nie mógł odczytać nawet metadanych — zwykle brak uprawnień, np. przy plikach systemowych Windowsa (`pagefile.sys`, `hiberfil.sys`).

---

## 5. Praca z plikami

Wszystko, co robi agent AI w projekcie, sprowadza się do czterech operacji: **czyta, tworzy, modyfikuje, kasuje pliki**. To są dokładnie te polecenia.

### Tworzenie

```bash
mkdir notatki                    # jeden katalog
mkdir cli git skills             # kilka naraz
mkdir -p projekt/src/utils       # -p tworzy całą ścieżkę, także brakujące poziomy
```

Bez `-p` polecenie zawiedzie, gdy katalog nadrzędny nie istnieje. `-p` (*parents*) dodatkowo nie protestuje, gdy katalog już jest.

```bash
touch notatka.md                     # pusty plik
touch plik1.md plik2.md plik3.md     # kilka naraz
```

`touch` na **istniejącym** pliku niczego nie kasuje — tylko aktualizuje datę modyfikacji. To jego pierwotne zastosowanie.

### Podgląd zawartości

`ls` mówi, że plik istnieje i jakie ma właściwości. Te polecenia pokazują, **co jest w środku**.

```bash
cat README.md              # cała zawartość na ekran
cat -n README.md           # z numerami linii
cat plik1.md plik2.md      # skleja kilka plików (stąd nazwa: concatenate)
```

`cat` przy pliku na 2000 linii zaleje terminal. Do dużych plików:

```bash
less README.md             # przeglądarka z przewijaniem
```

Sterowanie w `less`: strzałki i `PgUp`/`PgDn` przewijają, `/fraza` szuka, `n` następne trafienie, **`q` wychodzi**.

```bash
head README.md             # pierwsze 10 linii
head -n 3 README.md        # pierwsze 3
tail -n 20 log.txt         # ostatnie 20
tail -f log.txt            # -f = follow, śledzi dopisywane linie na żywo
```

**`tail -f` to podstawowe narzędzie testera.** Odpalasz na logu, wykonujesz akcję w aplikacji i widzisz błędy w czasie rzeczywistym. Wyjście: `Ctrl+C`.

```bash
wc -l README.md            # ile linii
wc -w README.md            # ile słów
wc -c README.md            # ile znaków
wc README.md               # wszystko naraz: linie, słowa, znaki
```

### Kopiowanie i przenoszenie

```bash
cp plik.md kopia.md              # kopia w tym samym katalogu
cp plik.md notatki/              # kopiuj do katalogu, nazwa bez zmian
cp plik.md ~/backup/plik.md      # ścieżka bezwzględna
cp -r notatki/ backup/           # -r = recursive, WYMAGANE dla katalogów
cp -i plik.md kopia.md           # -i = pytaj przed nadpisaniem
```

Bez `-r` kopiowanie katalogu zawiedzie, bo `cp` domyślnie obsługuje pojedyncze pliki, a katalog to struktura z zawartością.

**`cp` domyślnie nadpisuje bez pytania.**

```bash
mv stara.md nowa.md              # zmiana nazwy
mv plik.md notatki/              # przeniesienie
mv notatki/ archiwum/            # katalog, bez -r
mv ~/nauka-ai/plik.txt ~/        # przeniesienie do katalogu domowego
```

`mv` robi jedno i drugie, bo z punktu widzenia systemu zmiana nazwy i przeniesienie to ta sama operacja: zmiana wpisu w katalogu.

**Różnica `cp` vs `mv`:** `cp` zostawia oryginał (powstaje drugi plik), `mv` go usuwa z poprzedniego miejsca (plik nadal jeden).

### Kasowanie

```bash
rm plik.md            # skasuj plik
rm -r katalog/        # skasuj katalog z zawartością
rm -i plik.md         # pytaj przed skasowaniem
rm *.tmp              # wszystkie pliki .tmp
```

Trzy rzeczy do zapamiętania:

1. **Nie ma kosza.** `rm` kasuje nieodwracalnie, nie ma `Ctrl+Z`.
2. **Nie pyta o potwierdzenie**, chyba że dodasz `-i`.
3. **`-f` (force) wyłącza wszystkie zabezpieczenia.** `rm -rf` kasuje wszystko bez ostrzeżeń. `rm -rf /` niszczy system.

**Bezpieczna procedura kasowania po wzorcu:**

```bash
ls *.log        # KROK 1: zobacz dokładnie, co pasuje
rm *.log        # KROK 2: dopiero teraz kasuj
```

`ls` z tym samym wzorcem to podgląd operacji przed jej wykonaniem.

**Zasada: kasuj dokładnie tyle, ile trzeba, ani pliku więcej.** Jeśli w katalogu jest 200 plików, a chcesz usunąć 20 plików `.log`, kasujesz `rm *.log`, a nie cały katalog.

`rmdir` kasuje wyłącznie **pusty** katalog i zawiedzie, gdy coś w nim jest — dlatego bywa bezpieczniejszy niż `rm -r`.

### Edycja

```bash
nano notatka.md
```

Skróty widoczne na dole ekranu, gdzie `^` oznacza `Ctrl`:

| Skrót | Działanie |
|---|---|
| `Ctrl+O` | zapisz (potem Enter) |
| `Ctrl+X` | wyjdź |
| `Ctrl+K` | wytnij linię |
| `Ctrl+W` | szukaj |

Jeśli kiedyś przypadkiem trafisz do `vim`, wyjście to `:q!` i Enter.

Pliki WSL można też edytować z Windowsa pod ścieżką:
`\\wsl$\Ubuntu\home\kapi\nauka-ai\`

---

## 6. Przekierowania — znak `>` dokładnie

To najważniejsza część notatki. Bez tego nie da się zrozumieć potoków ani logów.

### Punkt wyjścia: skąd bierze się tekst na ekranie

Każde polecenie coś produkuje. `ls` produkuje listę plików. `tree` produkuje drzewo. `date` produkuje datę.

Domyślnie ten wynik trafia **na ekran**. Wyobraź sobie, że każde polecenie ma rurę wyjściową, która domyślnie jest skierowana na monitor:

```
[ tree ]  ──rura──►  EKRAN
```

### Co robi `>`

Znak `>` **przestawia tę rurę z ekranu na plik**.

```
[ tree ]  ──rura──►  PLIK
```

```bash
tree > struktura.txt
```

Polecenie działa dokładnie tak samo jak wcześniej. Jedyna zmiana to miejsce, gdzie ląduje wynik.

### Trzy konsekwencje, które mylą początkujących

**1. Na ekranie nie pojawia się nic — i to jest poprawne.**

```bash
kapi@kapikomp:~/nauka-ai$ tree > struktura.txt
kapi@kapikomp:~/nauka-ai$
```

Pusto, bo wynik poszedł do pliku. To nie znaczy, że polecenie nie zadziałało. Weryfikacja:

```bash
ls -l struktura.txt        # czy plik istnieje i ma rozmiar > 0
cat struktura.txt          # co jest w środku
```

Rozmiar `0` oznacza, że polecenie nic nie wypisało — najczęściej dlatego, że wskazano nieistniejący katalog.

**2. Plik powstaje sam.** Nie trzeba go wcześniej tworzyć przez `touch`.

**3. Jeśli plik już istnieje, jego zawartość zostaje SKASOWANA.**

`>` nie dopisuje. Czyści plik do zera i zapisuje od nowa. Bez ostrzeżenia, bez potwierdzenia, bez możliwości cofnięcia.

```bash
echo "linia 1" > plik.txt     # plik.txt zawiera: linia 1
echo "linia 2" > plik.txt     # plik.txt zawiera: linia 2  ← linia 1 PRZEPADŁA
```

### `>>` — dopisywanie

Podwójny znak dopisuje na końcu, zachowując to, co było:

```bash
echo "linia 1" >> plik.txt    # plik.txt: linia 1
echo "linia 2" >> plik.txt    # plik.txt: linia 1 / linia 2
```

| | Plik nie istnieje | Plik istnieje |
|---|---|---|
| `>` | tworzy nowy | **kasuje zawartość** i zapisuje od nowa |
| `>>` | tworzy nowy | dopisuje na końcu |

**To najczęstszy sposób, w jaki początkujący traci dane w terminalu.** Jeden brakujący znak `>` i notatka pisana godzinę znika.

Zasada praktyczna: **jeśli plik ma jakąkolwiek wartość, używaj `>>`.** `>` tylko wtedy, gdy świadomie chcesz zacząć od zera.

### Ścieżka po `>` to zwykła ścieżka

Obowiązują te same zasady, co przy odczycie. To częsty błąd:

```bash
# stojąc w ~/nauka-ai:
tree > struktura.txt          # plik powstanie w ~/nauka-ai/struktura.txt
tree > ~/struktura.txt        # plik powstanie w /home/kapi/struktura.txt
```

Brak `~` lub `/` na początku = plik ląduje w katalogu, w którym stoisz. Nie tam, gdzie się go potem szuka.

### Kolejność wykonania (ciekawostka z konsekwencjami)

Bash **najpierw** tworzy (lub czyści) plik docelowy, a **dopiero potem** uruchamia polecenie. Dlatego:

```bash
tree > struktura.txt
cat struktura.txt
# w wyniku widać... struktura.txt
```

Plik wymienia sam siebie, bo w momencie skanowania katalogu przez `tree` już istniał.

Ta kolejność ma groźniejszą konsekwencję. **To nie działa:**

```bash
cat plik.txt > plik.txt       # ŹLE: plik zostaje wyczyszczony ZANIM cat go przeczyta
```

Wynik: pusty plik. Nigdy nie przekierowuj do tego samego pliku, który polecenie czyta.

### Dwa kanały wyjścia: stdout i stderr

Każde polecenie ma trzy kanały:

| Kanał | Numer | Co to |
|---|---|---|
| stdin | 0 | wejście — skąd polecenie bierze dane |
| stdout | 1 | wyjście — normalny wynik |
| stderr | 2 | wyjście błędów |

Domyślnie stdout i stderr **oba** trafiają na ekran, przez co wyglądają identycznie. Ale to dwa osobne kanały i można je rozdzielić.

Przykład z `ls /mnt/c`:

```
ls: cannot access '/mnt/c/pagefile.sys': Permission denied     ← stderr (2)
'$Recycle.Bin'  AMD  Windows  Users  ...                       ← stdout (1)
```

Rozdzielenie:

```bash
ls /mnt/c 2> /dev/null        # błędy wyrzucone, lista zostaje na ekranie
ls /mnt/c > /dev/null         # lista wyrzucona, zostają same błędy
ls /mnt/c 2> bledy.txt        # błędy do pliku, lista na ekran
ls /mnt/c > lista.txt 2> bledy.txt   # każdy kanał do osobnego pliku
ls /mnt/c &> wszystko.txt     # oba kanały do jednego pliku
```

Cyfra przed `>` mówi, który kanał przekierowujesz. Samo `>` to skrót od `1>`.

### `/dev/null` — kosz systemowy

`/dev/null` to specjalne urządzenie, które przyjmuje wszystko i natychmiast kasuje. **To nie jest kosz w sensie windowsowym** — z kosza da się odzyskać, stąd nie.

Używa się go, gdy komunikaty zaśmiecają wynik, a nie są istotne. Typowe zastosowanie: `ls /mnt/c 2> /dev/null` w WSL, gdzie pliki systemowe Windowsa zawsze produkują `Permission denied`.

### `echo` — najprostszy sposób dopisania linii

```bash
echo "tekst" >> plik.md
```

**Tekst zawsze w cudzysłowie.** Bez niego znaki specjalne zostaną zinterpretowane przez basha:

```bash
echo ## Nagłówek >> plik.md      # ŹLE: # to komentarz, dopisze pustą linię
echo "## Nagłówek" >> plik.md    # DOBRZE
```

Ta sama zasada dotyczy nazw plików ze spacjami — dlatego `ls` pokazuje `'Program Files'` w apostrofach.

### `<` — przekierowanie wejścia

Rzadziej używane, ale warto wiedzieć, że istnieje. `<` podaje zawartość pliku na **wejście** polecenia:

```bash
wc -l < plik.txt        # policz linie, dane z pliku
```

### Praktyczne zastosowania przekierowań

```bash
tree > ~/struktura.txt                    # zrzut struktury projektu do pliku
history > ~/historia.txt                  # zapis historii poleceń
date >> ~/log-pracy.txt                   # dopisanie znacznika czasu
npm test > wynik-testow.txt 2>&1          # cały output testów do jednego pliku
grep "ERROR" log.txt > bledy-do-analizy.txt   # wyciąg błędów do osobnego pliku
echo "## Notatki z dnia" >> notatka.md    # szybkie dopisanie nagłówka
```

`2>&1` znaczy „skieruj kanał 2 tam, gdzie idzie kanał 1". Używa się tego, żeby złapać błędy razem z normalnym wyjściem — przydatne przy zapisywaniu logów z testów.

---

## 7. Potoki

Znak `|` (pionowa kreska, `AltGr` + `\`) przekazuje wyjście jednego polecenia jako **wejście** następnego.

```
[ cat log.txt ] ──► [ grep ERROR ] ──► [ wc -l ] ──► EKRAN
```

**Różnica względem `>`:** `>` wysyła wynik do **pliku**, `|` wysyła do **następnego polecenia**.

```bash
ls -la | wc -l                  # policz pozycje w katalogu
cat log.txt | grep "ERROR"      # pokaż tylko linie z ERROR
history | grep "cd"             # które polecenia z cd wpisywałem
history | grep "cd" | wc -l     # ile ich było
```

Łańcuch może mieć wiele ogniw. Czyta się go od lewej:

```bash
cat log.txt | grep "ERROR" | tail -n 20 | wc -l
```

1. `cat log.txt` — czyta plik i wysyła treść dalej
2. `grep "ERROR"` — przepuszcza tylko linie z ERROR, resztę odrzuca
3. `tail -n 20` — z nich bierze ostatnie 20
4. `wc -l` — liczy, ile linii dostał

Na ekranie pojawia się **tylko jedna liczba**. Wyniki pośrednie nigdzie się nie wyświetlają — każde ogniwo przekazuje dane do następnego.

To jest filozofia Uniksa: małe narzędzia robiące jedną rzecz dobrze, łączone w łańcuchy. Zamiast jednego wielkiego programu składasz rozwiązanie z klocków.

### Pułapka przy liczeniu

```bash
ls -la ~ | wc -l
# 17
```

To **nie** znaczy 17 plików. `ls -la` dokłada trzy linie, które plikami nie są: nagłówek `total`, wpis `.` i wpis `..`. Faktycznych pozycji jest 14.

Poprawnie:

```bash
ls -A ~ | wc -l        # -A pokazuje ukryte, ale pomija . i ..
```

**Zawsze sprawdzaj, czy polecenie nie dokłada linii, których nie chcesz liczyć.**

---

## 8. Wyszukiwanie: grep i find

| Narzędzie | Szuka |
|---|---|
| `grep` | **treści wewnątrz** plików |
| `find` | **plików** po nazwie i właściwościach |

### `grep` — szukanie w treści

```bash
grep "ERROR" log.txt              # linie zawierające ERROR
grep -i "error" log.txt           # -i = ignoruj wielkość liter
grep -n "ERROR" log.txt           # -n = pokaż numery linii
grep -r "TODO" .                  # -r = rekurencyjnie, całe drzewo od bieżącego katalogu
grep -c "ERROR" log.txt           # -c = policz trafienia zamiast wypisywać
grep -v "DEBUG" log.txt           # -v = odwróć, pokaż linie BEZ dopasowania
grep -A 3 "ERROR" log.txt         # -A 3 = pokaż też 3 linie PO trafieniu
grep -B 3 "ERROR" log.txt         # -B 3 = 3 linie PRZED
grep -l "TODO" *.md               # -l = tylko nazwy plików z trafieniem
```

`grep -r` to sposób na przeszukanie całego projektu. „Gdzie w kodzie wywoływana jest ta funkcja" to jedno polecenie.

`grep -A 3` jest bardzo przydatne przy logach — sam komunikat błędu często nic nie mówi, dopiero kolejne linie ze stack trace pokazują przyczynę.

### `find` — szukanie plików

Sztywna kolejność: **`find [gdzie] [kryteria]`**

```bash
find . -name "*.md"                    # pliki .md od bieżącego katalogu w dół
find ~/nauka-ai -type d                # tylko katalogi (d = directory)
find ~/nauka-ai -type f                # tylko pliki (f = file)
find . -type f -name "01*"             # pliki zaczynające się od 01
find . -mtime -1                       # zmodyfikowane w ciągu ostatniej doby
find . -size +1M                       # większe niż 1 MB
find . -name "*.log" -delete           # znajdź i skasuj (OSTROŻNIE)
```

Cudzysłowy przy `"*.md"` są istotne. Bez nich bash rozwinie gwiazdkę **przed** uruchomieniem `find`, więc `find` dostanie już podstawioną nazwę zamiast wzorca.

### Znaki wieloznaczne

| Znak | Znaczy | Przykład |
|---|---|---|
| `*` | dowolny ciąg znaków | `ls *.md` |
| `?` | dokładnie jeden znak | `ls plik?.md` |
| `{a,b}` | jedno z wymienionych | `ls {README,LICENSE}.md` |

**Znaki wieloznaczne nie schodzą rekurencyjnie w głąb drzewa.**

```bash
ls notatki/*/*.md      # TYLKO jeden poziom w głąb notatki/
find . -name "*.md"    # całe drzewo, wszystkie poziomy
```

To ważna różnica w praktyce: w projekcie z 50 katalogami wzorzec z gwiazdką przegapi większość plików, a można być przekonanym, że ich nie ma.

---

## 9. Historia i skróty klawiszowe

```bash
history                    # lista wszystkich wpisanych poleceń
history | grep "git"       # tylko te z git
history > ~/historia.txt   # zapis do pliku
!!                         # powtórz ostatnie polecenie
sudo !!                    # powtórz ostatnie z uprawnieniami roota
```

Historia zapisuje się w pliku `~/.bash_history`. Dlatego ma uprawnienia `-rw-------` — może zawierać wrażliwe dane.

### Skróty

| Skrót | Działanie |
|---|---|
| `Tab` | autouzupełnianie nazw. Podwójny Tab = lista opcji |
| `↑` / `↓` | przewijanie historii |
| `Ctrl+R` | **wyszukiwanie w historii** — pisz fragment, Enter uruchamia |
| `Ctrl+C` | przerwij działające polecenie |
| `Ctrl+L` | wyczyść ekran (= `clear`) |
| `Ctrl+A` / `Ctrl+E` | początek / koniec linii |
| `Ctrl+U` | wyczyść całą linię |
| `Ctrl+D` | zamknij sesję (= `exit`) |

**`Tab` używać zawsze.** Eliminuje literówki i od razu pokazuje, czy plik w ogóle istnieje — jeśli nie uzupełnia, to znaczy, że w tym miejscu takiego pliku nie ma.

**`Ctrl+R` jest najbardziej niedoceniany.** Zamiast przewijać strzałką przez 50 poleceń, wciskasz `Ctrl+R`, piszesz `tree` i masz ostatnie pasujące polecenie. `Esc` pozwala je najpierw poprawić przed uruchomieniem.

---

## 10. Typowe błędy

### Trzy rodzaje komunikatów — nauczyć się rozróżniać

| Komunikat | Co znaczy | Gdzie szukać przyczyny |
|---|---|---|
| `command not found` | bash nie zna **programu** o tej nazwie | literówka w nazwie polecenia albo program niezainstalowany |
| `No such file or directory` | program działa, ale **ścieżka nie istnieje** | zła ścieżka albo złe miejsce, w którym stoisz |
| `Not a directory` | ścieżka istnieje, ale **to nie jest katalog** | złe polecenie do zadania (np. `cd` na plik) |

Pierwszy mówi „nie wiem, co mam zrobić". Drugi „wiem co, ale nie znajduję na czym". Trzeci „znalazłem, ale to nie to".

To rozróżnienie wróci przy agentach. `command not found: pytest` = brakuje narzędzia. `No such file or directory` = agent stanął w złym katalogu. Inna diagnoza, inna naprawa.

### Konkretne pomyłki z tego modułu

**Ścieżka bezwzględna zamiast względnej:**
```bash
cd /nauka-ai
# -bash: cd: /nauka-ai: No such file or directory
```
Wiodący `/` = szukaj w korzeniu dysku. `nauka-ai` leży w `/home/kapi`, nie w `/`.

**Ścieżka względna zamiast bezwzględnej:**
```bash
cd home/kapi/nauka-ai/notatki
# -bash: cd: home/kapi/nauka-ai/notatki: No such file or directory
```
Wygląda jak pełna ścieżka, ale bez wiodącego `/` bash doliczył ją do bieżącego katalogu. Powstało `/home/kapi/nauka-ai/home/kapi/nauka-ai/notatki`.

**Podwojona ścieżka przy `cp`:**
```bash
# stojąc w ~/nauka-ai/notatki/cli:
cp 01-podstawy.md notatki/cli/kopia.md
# cp: cannot create regular file 'notatki/cli/kopia.md': No such file or directory
```
Cel doliczony do bieżącego katalogu dał `.../notatki/cli/notatki/cli/`. Poprawnie: `cp 01-podstawy.md kopia.md`.

Uwaga: komunikat `cannot create regular file ... No such file or directory` brzmi, jakby brakowało pliku źródłowego, ale chodzi o **katalog docelowy**.

**Plik szukany w złym katalogu:**
```bash
# stojąc w ~/nauka-ai/notatki/cli:
head -n 2 README.md
# head: cannot open 'README.md' for reading: No such file or directory
```
`README.md` leży dwa poziomy wyżej. Poprawnie: `head -n 2 ../../README.md`.

**Zapis pliku w nieoczekiwanym miejscu:**
```bash
# stojąc w ~/nauka-ai:
tree > struktura.txt          # plik powstał w ~/nauka-ai/, nie w ~/
ls -l ~/struktura.txt
# ls: cannot access '/home/kapi/struktura.txt': No such file or directory
```

**`cd` na plik:**
```bash
cd 01-podstawy.md
# -bash: cd: 01-podstawy.md: Not a directory
```
Do pliku się nie wchodzi. `cat`, `less` albo `nano`.

**Literówka w nazwie polecenia:**
```bash
łs ~/nauka-ai        # łs: command not found
list -l              # Command 'list' not found
```
Podpowiedź Ubuntu „but there are 22 similar ones" bywa pomocna, ale często sugeruje niezwiązane programy. Nie traktować jak wyroczni.

### Lista kontrolna

- [ ] Przy `No such file or directory` → najpierw `pwd`
- [ ] Ścieżkę testować przez `ls` przed użyciem w `cp`, `mv`, `rm`
- [ ] Przed `rm` ze wzorcem → to samo z `ls`
- [ ] Do dopisywania `>>`, nie `>`
- [ ] Tekst przy `echo` w cudzysłowie
- [ ] Katalogi przy `cp` wymagają `-r`
- [ ] `cd` tylko na katalogi
- [ ] Używać `Tab` zamiast przepisywać nazwy ręcznie

---

## 11. Zastosowanie w QA i przy pracy z agentami AI

### Dlaczego tester potrzebuje terminala

- **Agenci AI żyją w terminalu.** Claude Code nie ma GUI. Gdy „uruchamia testy" albo „modyfikuje plik", wykonuje dokładnie te polecenia, które są w tej notatce. Bez ich znajomości nie da się zweryfikować, czy zrobił to, co deklaruje — pozostaje wiara na słowo.
- **Serwery i CI nie mają eksploratora plików.** Logi z pipeline'a, środowisko testowe, kontener — dostęp wyłącznie przez shell.
- **Powtarzalność.** Kliknięcia nie da się wkleić do zgłoszenia błędu. Polecenia tak — kolega odtworzy je co do znaku.
- **Automatyzacja.** To, co da się wpisać, da się zapisać jako skrypt i uruchamiać cyklicznie.

### Konkretne zastosowania w pracy testera

```bash
tail -f logs/app.log                        # obserwacja logów na żywo podczas testu
grep -i "error" logs/app.log | wc -l        # ile błędów w logu
grep -A 5 "Exception" logs/app.log          # błąd wraz z kontekstem
find . -name "*.log" -mtime -1              # logi z ostatniej doby
npm test > wynik.txt 2>&1                   # zapis pełnego outputu testów do pliku
grep "FAIL" wynik.txt                       # wyciąg samych niepowodzeń
ls -ltr logs/                               # najświeższe logi na dole listy
```

### Weryfikacja pracy agenta

Kiedy agent raportuje wykonaną pracę, sprawdzenie sprowadza się do tych samych poleceń:

```bash
ls -la                    # czy pliki, o których mówi, faktycznie powstały
cat plik.md               # czy treść jest taka, jak deklaruje
tree                      # czy struktura się zgadza
grep -r "szukana_fraza"   # czy zmiana trafiła wszędzie, gdzie miała
```

**Kluczowa umiejętność: świadome zatwierdzanie operacji destrukcyjnych.** Claude Code prosi o zgodę przed `rm`, nadpisaniem plików czy `git push`. Jeśli agent zaproponuje `rm -rf logs/`, a chodziło o `rm logs/*.log`, kliknięcie „tak" kasuje cały katalog. Czytanie tych propozycji ze zrozumieniem to część roli QA.

### Potoki a agenci

Znajomość potoków przekłada się na trzy rzeczy:

1. **Rozumienie działań agenta** — gdy w logu widać `grep -r "TODO" . | wc -l`, od razu wiadomo, co zrobił.
2. **Precyzyjniejsze polecenia** — zamiast „sprawdź logi" można powiedzieć „przefiltruj log po ERROR i policz wystąpienia".
3. **Samodzielna weryfikacja** — ten sam potok można uruchomić ręcznie i porównać wynik.

---

## 12. Ściąga — wszystkie komendy

### Nawigacja
| Komenda | Działanie |
|---|---|
| `pwd` | gdzie jestem |
| `ls` / `ls -la` / `ls -ltr` | lista plików |
| `cd katalog` / `cd ..` / `cd ~` / `cd -` | zmiana katalogu |
| `tree -a -L 2` | struktura jako drzewo |

### Pliki
| Komenda | Działanie |
|---|---|
| `mkdir -p sciezka` | utwórz katalog(i) |
| `touch plik` | utwórz pusty plik |
| `cat plik` | pokaż całą zawartość |
| `less plik` | przeglądaj z przewijaniem (`q` wyjście) |
| `head -n 5 plik` / `tail -n 5 plik` | początek / koniec |
| `tail -f plik` | śledź na żywo |
| `wc -l plik` | policz linie |
| `cp -r zrodlo cel` | kopiuj |
| `mv zrodlo cel` | przenieś / zmień nazwę |
| `rm -r cel` | usuń |
| `nano plik` | edytuj |

### Przekierowania i potoki
| Zapis | Działanie |
|---|---|
| `>` | wynik do pliku, **nadpisuje** |
| `>>` | wynik do pliku, dopisuje |
| `2>` | tylko błędy do pliku |
| `&>` | wszystko do jednego pliku |
| `2>&1` | błędy tam, gdzie normalne wyjście |
| `/dev/null` | kosz systemowy |
| `\|` | wyjście → wejście następnego polecenia |
| `<` | zawartość pliku na wejście |

### Wyszukiwanie
| Komenda | Działanie |
|---|---|
| `grep -rin "fraza" .` | szukaj w treści, rekurencyjnie, bez rozróżniania wielkości liter, z numerami linii |
| `grep -v "fraza" plik` | linie BEZ frazy |
| `grep -A 3 "fraza" plik` | z kontekstem |
| `find . -name "*.md"` | szukaj plików po nazwie |
| `find . -type d` | tylko katalogi |

### Pomoc i system
| Komenda | Działanie |
|---|---|
| `polecenie --help` | szybka pomoc |
| `man polecenie` | pełna dokumentacja (`q` wyjście) |
| `which program` | gdzie leży program |
| `history` | historia poleceń |
| `du -sh katalog` | rzeczywisty rozmiar katalogu |
| `clear` | wyczyść ekran |

---

## 13. Pytania testowe

**Teoria**

1. Czym różni się terminal od shella?
2. Czym różni się ścieżka bezwzględna od względnej? Po czym je rozpoznać?
3. Co oznaczają `.`, `..`, `~` i `-` w ścieżkach?
4. Wymień trzy rodzaje komunikatów o błędach i wyjaśnij, co każdy znaczy.
5. Co oznacza `x` w uprawnieniach katalogu?
6. Czym się różnią stdout i stderr?
7. Czym różni się `>` od `>>` i dlaczego pomyłka jest groźna?
8. Czym różni się `grep` od `find`?
9. Czym różni się `|` od `>`?
10. Czym różni się `cp` od `mv`?

**„Jak to działa?"**

11. Stoisz w `/home/kapi/projekty/api`. Wpisujesz `cd ../../nauka-ai`. Gdzie wylądujesz?
12. Dlaczego `ls notatki` może zwrócić błąd, mimo że katalog `notatki` na pewno istnieje?
13. Uruchamiasz `tree > plik.txt` i na ekranie nic się nie pojawia. Czy to błąd?
14. Dlaczego `cp katalog/ backup/` zawiedzie bez dodatkowej flagi?
15. Co robi `touch` na istniejącym pliku?
16. Wyjaśnij krok po kroku, co robi `cat log.txt | grep "ERROR" | wc -l` i co pojawi się na ekranie.
17. Dlaczego `cat plik.txt > plik.txt` daje pusty plik?
18. `ls -la | wc -l` zwraca 17. Czy w katalogu jest 17 plików?
19. Dlaczego `ls notatki/*/*.md` może nie znaleźć wszystkich plików `.md` w projekcie?
20. Co robi `2> /dev/null` i kiedy się tego używa?

**Scenariusze**

21. Masz log na 50 000 linii i chcesz zobaczyć ostatnie błędy. Czego użyjesz i dlaczego nie `cat`?
22. W katalogu jest 200 plików, chcesz usunąć wszystkie `.log`. Jak zrobić to bezpiecznie?
23. Chcesz zapisać wynik testów razem z błędami do jednego pliku. Jakie polecenie?
24. Testujesz aplikację i chcesz widzieć błędy pojawiające się w logu w czasie rzeczywistym. Co uruchomisz?
25. Agent AI zaproponował `rm -rf logs/`. Co sprawdzisz przed zatwierdzeniem?
26. Chcesz znaleźć wszystkie miejsca w projekcie, gdzie występuje słowo `TODO`, wraz z numerami linii. Jakie polecenie?
27. Dlaczego znajomość potoków jest istotna przy pracy z agentami AI?
28. Dlaczego nie warto trzymać projektów w `/mnt/c/`?
29. Kod działa lokalnie na Windowsie, ale na serwerze Linuksowym plik „nie istnieje". Jaka może być przyczyna?
30. Po co komuś w QA umiejętność pracy w terminalu, skoro istnieje eksplorator plików?

---

*Moduł 1 — zakończony. Następny: Git i GitHub.*

