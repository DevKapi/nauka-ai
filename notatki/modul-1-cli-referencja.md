---
modul: 1
tytul: CLI — podstawy pracy w terminalu
status: notatka referencyjna (wersja 2)
autor_notatki: Claude
uzytkownik: Kacper Kowalski (DevKapi)
srodowisko: WSL 2 / Ubuntu
---

# Moduł 1 — CLI. Notatka referencyjna

> **Wersja 2.** Pierwsza wersja notatki była niepełna: zawierała polecenia bez opisu
> wszystkich flag i nie tłumaczyła strumieni danych. Ta wersja to naprawia.
>
> **Zasada nadrzędna:** nie ufaj tej notatce na słowo. Każdy przykład
> uruchom u siebie i sprawdź, czy robi to, co jest napisane. W poprzednim module
> notatka zawierała błąd (przykład `cp` napisany z niewłaściwego katalogu
> roboczego), który kosztował sporo czasu. Notatka to punkt startu, nie wyrocznia.

---

## Spis treści

1. [Jak w ogóle działa terminal](#1-jak-w-ogóle-działa-terminal)
2. [Ścieżki — fundament wszystkiego](#2-ścieżki--fundament-wszystkiego)
3. [Nawigacja: `pwd`, `cd`, `ls`](#3-nawigacja-pwd-cd-ls)
4. [Katalogi: `mkdir`, `rmdir`](#4-katalogi-mkdir-rmdir)
5. [Pliki: `touch`, `cp`, `mv`, `rm`](#5-pliki-touch-cp-mv-rm)
6. [Podgląd zawartości: `cat`, `head`, `tail`, `less`](#6-podgląd-zawartości-cat-head-tail-less)
7. [`echo` — wypisywanie tekstu](#7-echo--wypisywanie-tekstu)
8. [**Strumienie: `>`, `>>`, `|`, `<`**](#8-strumienie--najważniejsza-sekcja-w-tej-notatce)
9. [Liczenie i sortowanie: `wc`, `sort`, `uniq`](#9-liczenie-i-sortowanie-wc-sort-uniq)
10. [Szukanie tekstu: `grep`](#10-szukanie-tekstu-grep)
11. [Szukanie plików: `find`](#11-szukanie-plików-find)
12. [Wildcards (globbing): `*`, `?`, `[]`](#12-wildcards-globbing)
13. [Typowe błędy — Twoje własne](#13-typowe-błędy--twoje-własne)
14. [Ściąga](#14-ściąga)
15. [Pytania testowe](#15-pytania-testowe)

---

## 1. Jak w ogóle działa terminal

### Trzy pojęcia, które się mylą

| Pojęcie | Co to jest |
|---|---|
| **Terminal** | Okno. Sam w sobie nic nie robi — tylko wyświetla tekst i przyjmuje klawisze. |
| **Powłoka (shell)** | Program działający w tym oknie, który czyta Twoje polecenia i je wykonuje. U Ciebie to **bash**. |
| **CLI** | *Command Line Interface* — sposób sterowania komputerem przez wpisywanie poleceń zamiast klikania. |

Powłoka to pośrednik. Ty piszesz tekst, ona rozumie, co znaczy, i uruchamia odpowiedni program.

### Znak zachęty (prompt)

```
kapi@kapikomp:~/cwiczenia-cli$
│      │           │        └── znak końca promptu ($ = zwykły użytkownik)
│      │           └── gdzie aktualnie jesteś (~ = katalog domowy)
│      └── nazwa komputera
└── nazwa użytkownika
```

Prompt sam z siebie mówi Ci, gdzie stoisz. To Twoje pierwsze źródło informacji, zanim jeszcze wpiszesz `pwd`.

### Anatomia polecenia

```bash
ls -l -a /home/kapi
│  │  │  └── argument (na czym działamy)
│  └──┴── flagi / opcje (jak ma działać)
└── nazwa programu (co uruchamiamy)
```

**Spacja jest separatorem.** To brzmi banalnie, ale to źródło większości błędów początkujących. Każda spacja kończy jeden element i zaczyna następny. Powłoka nie „domyśla się", że dwie rzeczy obok siebie są ze sobą powiązane.

Flagi można zwykle łączyć: `ls -l -a` = `ls -la`.

### Dwa rodzaje flag

```bash
ls -a              # krótka flaga: jeden myślnik, jedna litera
ls --all           # długa flaga: dwa myślniki, całe słowo
```

Zwykle znaczą to samo. Krótkie są szybsze do wpisania, długie czytelniejsze w skryptach.

### Skróty, które ratują życie

| Skrót | Działanie |
|---|---|
| `Tab` | Uzupełnia nazwę pliku/katalogu. **Używaj zawsze** — eliminuje literówki w ścieżkach. |
| `Tab` `Tab` | Pokazuje wszystkie pasujące możliwości. |
| `↑` / `↓` | Przewija historię wcześniejszych poleceń. |
| `Ctrl+C` | Przerywa działający program. |
| `Ctrl+D` | Sygnalizuje „koniec danych wejściowych". Wychodzi z `cat` bez argumentu. |
| `Ctrl+L` | Czyści ekran (to samo co `clear`). |
| `Ctrl+A` / `Ctrl+E` | Skok na początek / koniec linii. |

> **Tab to nie wygoda, to narzędzie diagnostyczne.** Jeśli `Tab` nie uzupełnia nazwy,
> to znaczy, że tego pliku tu nie ma — dowiadujesz się o błędzie ścieżki
> *zanim* wciśniesz Enter.

### Skąd wiedzieć, co robi polecenie

```bash
man ls          # pełna dokumentacja (wyjście: q)
ls --help       # krótka pomoc, mieści się na ekranie
```

`man` = *manual*. Poruszanie się: strzałki, `q` żeby wyjść, `/tekst` żeby szukać.

---

## 2. Ścieżki — fundament wszystkiego

To jest sekcja, do której warto wracać. Prawie każdy Twój dotychczasowy błąd
w Module 1 miał źródło tutaj.

### Drzewo katalogów

Linux ma **jeden korzeń** — `/`. Wszystko wyrasta z niego:

```
/
├── home/
│   └── kapi/                    ← Twój katalog domowy (~)
│       ├── nauka-ai/
│       └── cwiczenia-cli/
│           └── raport-testow/
│               ├── logi/
│               └── raporty/
├── etc/
└── usr/
```

W Windows jest wiele korzeni (`C:\`, `D:\`). W Linuksie jeden — `/`.

### Ścieżka bezwzględna (absolutna)

**Zaczyna się od `/`.** Opisuje drogę od korzenia. Działa zawsze, niezależnie od tego, gdzie stoisz.

```bash
/home/kapi/cwiczenia-cli/raport-testow/logi/testy-2026-08-28.log
```

Analogia: pełny adres pocztowy. Zadziała wysłany z dowolnego miejsca na świecie.

### Ścieżka względna

**Nie zaczyna się od `/`.** Opisuje drogę **od katalogu, w którym aktualnie stoisz**.

```bash
logi/testy-2026-08-28.log
```

Analogia: „drugie drzwi na prawo". Ma sens tylko wtedy, gdy wiadomo, skąd idziesz.

> ### 🔑 Zasada, którą trzeba znać na pamięć
>
> **Ścieżka względna zawsze startuje od tego, co pokazuje `pwd`.**
>
> Nie od poprzedniego polecenia. Nie od poprzedniego argumentu w tym samym
> poleceniu. Nie od tego, gdzie byłeś minutę temu. Od `pwd`. Zawsze.

### Symbole specjalne

| Symbol | Znaczenie | Przykład |
|---|---|---|
| `/` | korzeń systemu (na początku ścieżki) | `/home/kapi` |
| `.` | katalog bieżący — „tutaj" | `cp plik.txt .` |
| `..` | katalog nadrzędny — „piętro wyżej" | `cd ..` |
| `~` | Twój katalog domowy (`/home/kapi`) | `cd ~/nauka-ai` |
| `-` | poprzedni katalog (tylko z `cd`) | `cd -` |

### Składanie ścieżek — czytanie krok po kroku

Stoisz w `/home/kapi/cwiczenia-cli/raport-testow/raporty`.
Chcesz dostać się do `logi/testy-2026-08-28.log`.

```
../logi/testy-2026-08-28.log
```

Rozkład na kroki:

| Fragment | Gdzie jesteś po tym kroku |
|---|---|
| *(start)* | `.../raport-testow/raporty` |
| `..` | `.../raport-testow` — wyszedłeś piętro wyżej |
| `logi` | `.../raport-testow/logi` — zszedłeś do sąsiedniego katalogu |
| `testy-2026-08-28.log` | plik docelowy |

Wzór jest zawsze ten sam: **`..` tyle razy, ile pięter musisz wyjść w górę,
potem nazwy katalogów w dół.**

`..` można łączyć:

```bash
../../README.md      # dwa piętra w górę, potem plik
../../../etc/hosts   # trzy piętra w górę, potem w dół do etc/
```

### Ta sama rzecz, dwie ścieżki

Stojąc w `raporty/`, oba te polecenia robią dokładnie to samo:

```bash
cat ../logi/testy-2026-08-28.log                                    # względna
cat /home/kapi/cwiczenia-cli/raport-testow/logi/testy-2026-08-28.log  # bezwzględna
```

**Kiedy której używać:**

| | Względna | Bezwzględna |
|---|---|---|
| Zaleta | krótka, przenośna między maszynami | działa niezależnie od `pwd` |
| Wada | zależy od tego, gdzie stoisz | długa, zawiera Twoją nazwę użytkownika |
| Typowe zastosowanie | praca wewnątrz projektu | skrypty, cron, konfiguracje |

---

## 3. Nawigacja: `pwd`, `cd`, `ls`

### `pwd` — gdzie jestem

*print working directory*

```bash
pwd
```

Wypisuje ścieżkę bezwzględną katalogu bieżącego. Nie ma sensownych flag. Nie modyfikuje niczego.

**Zastosowania:**

```bash
# 1. Sprawdzenie przed operacją niebezpieczną (rm, >)
pwd

# 2. Skopiowanie ścieżki bezwzględnej do dalszego użycia
pwd
# /home/kapi/cwiczenia-cli/raport-testow/raporty

# 3. Debugowanie: "dlaczego ta ścieżka względna nie działa"
pwd     # ← prawie zawsze tutaj jest odpowiedź
```

> **Nawyk do wyrobienia:** `pwd` przed każdym `rm` i przed każdym `>`.
> To dwa polecenia, które niszczą dane bez pytania.

### `cd` — zmiana katalogu

*change directory*

```bash
cd ŚCIEŻKA
```

**Wszystkie zastosowania:**

```bash
cd /home/kapi/nauka-ai      # ścieżka bezwzględna
cd nauka-ai                 # względna — wejście do podkatalogu
cd ..                       # piętro wyżej
cd ../..                    # dwa piętra wyżej
cd ../logi                  # w górę i w bok
cd ~                        # do katalogu domowego
cd                          # ← to samo: bez argumentu = do domu
cd ~/nauka-ai/notatki       # od domu w dół
cd -                        # powrót do poprzedniego katalogu
cd /                        # do korzenia systemu
```

`cd -` jest bardzo praktyczne — działa jak przycisk „wstecz". Przeskakujesz
tam i z powrotem między dwoma katalogami.

**Typowe błędy:**

```bash
cd home/kapi        # ❌ brak / na początku → szuka podkatalogu "home" TUTAJ
cd /home/kapi       # ✅

# Stoisz już w ~/cwiczenia-cli:
cd cwiczenia-cli/raport-testow    # ❌ szuka cwiczenia-cli WEWNĄTRZ cwiczenia-cli
cd raport-testow                  # ✅
```

Drugi błąd to **podwojenie segmentu ścieżki** — Twój powracający problem.
Bierze się z myślenia „ścieżka od domu" zamiast „ścieżka od miejsca, gdzie stoję".

### `ls` — co tu jest

*list*

```bash
ls [flagi] [ścieżka]
```

Bez argumentu pokazuje zawartość katalogu bieżącego.

**Flagi:**

| Flaga | Działanie |
|---|---|
| `-l` | długi format: uprawnienia, właściciel, rozmiar, data |
| `-a` | pokazuje pliki ukryte (zaczynające się od `.`) |
| `-h` | rozmiary czytelne dla człowieka (`4.0K` zamiast `4096`) |
| `-t` | sortuje po dacie modyfikacji, najnowsze na górze |
| `-r` | odwraca kolejność sortowania |
| `-R` | rekurencyjnie — pokazuje też zawartość podkatalogów |
| `-1` | jeden plik na linię |

**Zastosowania:**

```bash
ls                          # szybki rzut oka
ls -l                       # szczegóły
ls -la                      # szczegóły + pliki ukryte (np. .git, .bashrc)
ls -lh                      # z czytelnymi rozmiarami
ls -lt                      # co ostatnio zmieniane — świetne do debugowania
ls -ltr                     # najnowsze na dole (wygodne przy długich listach)
ls -R                       # całe drzewo pod spodem
ls /home/kapi/nauka-ai      # zawartość innego katalogu, bez wchodzenia tam
ls ../logi                  # zawartość katalogu obok
ls *.log                    # tylko pliki .log
ls -l ../logi/*.log         # szczegóły plików .log w katalogu obok
```

**Czytanie `ls -l`:**

```
drwxr-xr-x 3 kapi kapi 4096 Aug 30 15:03 cwiczenia-cli
-rw-r--r-- 1 kapi kapi 6194 Aug 29 21:00 historia-modul1.txt
│└────┬──┘   │    │     │        │            └── nazwa
│     │      │    │     │        └── data modyfikacji
│     │      │    │     └── rozmiar w bajtach
│     │      │    └── grupa
│     │      └── właściciel
│     └── uprawnienia (r=czytanie, w=zapis, x=wykonanie)
└── typ: d = katalog (directory), - = zwykły plik, l = link
```

**Pierwszy znak jest najważniejszy** — od razu widzisz, czy to plik, czy katalog.

---

## 4. Katalogi: `mkdir`, `rmdir`

### `mkdir` — tworzenie katalogu

*make directory*

```bash
mkdir [flagi] ŚCIEŻKA...
```

**Flagi:**

| Flaga | Działanie |
|---|---|
| `-p` | tworzy brakujące katalogi pośrednie; nie zgłasza błędu, jeśli katalog już istnieje |
| `-v` | wypisuje, co zostało utworzone |

**Zastosowania:**

```bash
mkdir raporty                       # jeden katalog tutaj
mkdir raporty archiwum logi         # trzy katalogi obok siebie
mkdir -p projekt/src/tests          # cała ścieżka naraz, choć nic nie istnieje
mkdir -p ~/projekt/dokumentacja     # od katalogu domowego
mkdir -pv a/b/c                     # z pokazaniem, co powstało
```

**Bez `-p`:**

```bash
mkdir projekt/src/tests
# mkdir: cannot create directory 'projekt/src/tests': No such file or directory
```

`mkdir` bez `-p` tworzy **tylko ostatni element ścieżki** i wymaga, żeby cała
reszta już istniała.

> ### ⚠️ Pułapka, w którą wpadłeś
>
> ```bash
> mkdir -p cwiczenia-cli/raport-testow/logi raporty
> ```
>
> To są **dwa osobne argumenty**, rozdzielone spacją. `mkdir` traktuje każdy
> niezależnie i każdy liczy **od `pwd`**, a nie od poprzedniego argumentu.
>
> Powstało:
> - `./cwiczenia-cli/raport-testow/logi` ✅
> - `./raporty` ❌ ← w katalogu domowym, nie tam gdzie miało być
>
> Poprawnie — każdy argument to pełna ścieżka od miejsca, gdzie stoisz:
>
> ```bash
> mkdir -p cwiczenia-cli/raport-testow/logi cwiczenia-cli/raport-testow/raporty
> ```
>
> Albo, co czytelniejsze, z użyciem klamer (rozwijanych przez powłokę):
>
> ```bash
> mkdir -p cwiczenia-cli/raport-testow/{logi,raporty}
> ```
>
> Powłoka zamienia to na dwie pełne ścieżki, zanim `mkdir` w ogóle wystartuje.
> **Uwaga: bez spacji po przecinku wewnątrz klamer.**

### `rmdir` — usuwanie pustego katalogu

*remove directory*

```bash
rmdir ŚCIEŻKA
```

Usuwa **wyłącznie pusty** katalog. Jeśli coś w nim jest — odmawia:

```bash
rmdir logi
# rmdir: failed to remove 'logi': Directory not empty
```

**To jest zaleta, nie ograniczenie.** `rmdir` jest bezpieczne z definicji: jeśli
pomylisz ścieżkę i trafisz w katalog z zawartością, dostaniesz błąd zamiast
cichej utraty danych.

```bash
rmdir /home/kapi/raporty        # usuń pomyłkowo utworzony pusty katalog
rmdir -p a/b/c                  # usuń c, potem b, potem a (jeśli puste)
```

> ### 🔐 Zasada bezpieczeństwa
>
> **Wybieraj narzędzie o najmniejszej mocy rażenia, która wystarcza do zadania.**
>
> Do usunięcia pustego katalogu użyj `rmdir`, nie `rm -r`. Jeśli się pomylisz,
> `rmdir` Cię zatrzyma, a `rm -r` posłusznie wykona rozkaz.
>
> To ta sama zasada, która wróci przy zatwierdzaniu operacji agenta AI:
> zanim klikniesz „approve", zadaj sobie pytanie, co się stanie, jeśli agent
> źle zrozumiał zakres.

---

## 5. Pliki: `touch`, `cp`, `mv`, `rm`

### `touch` — utworzenie pustego pliku

```bash
touch plik.txt              # tworzy pusty plik
touch a.txt b.txt c.txt     # trzy pliki naraz
touch ../logi/nowy.log      # w innym katalogu
touch istniejacy.txt        # ← nie kasuje! aktualizuje tylko datę modyfikacji
```

Podstawowe zadanie `touch` to aktualizacja znacznika czasu. Tworzenie pliku
to efekt uboczny — ale w praktyce używa się go głównie do tego.

**Kluczowa różnica wobec `>`:**

```bash
touch dane.txt     # jeśli plik istnieje → nie rusza zawartości
> dane.txt         # jeśli plik istnieje → CZYŚCI go
```

### `cp` — kopiowanie

*copy*

```bash
cp [flagi] ŹRÓDŁO CEL
```

**Flagi:**

| Flaga | Działanie |
|---|---|
| `-r` | rekurencyjnie — wymagane do kopiowania katalogów |
| `-i` | pyta przed nadpisaniem istniejącego pliku |
| `-v` | pokazuje, co jest kopiowane |
| `-n` | nigdy nie nadpisuje |

**Zastosowania:**

```bash
cp raport.md raport-kopia.md         # kopia obok, pod inną nazwą
cp raport.md ../archiwum/            # do innego katalogu, ta sama nazwa
cp raport.md ../archiwum/stary.md    # do innego katalogu + zmiana nazwy
cp ../logi/testy.log .               # przynieś plik TUTAJ (kropka = tutaj)
cp *.log ../archiwum/                # wszystkie .log naraz
cp -r logi/ ../kopia-logow/          # cały katalog z zawartością
cp -i raport.md ../archiwum/         # z pytaniem przed nadpisaniem
```

> **`cp` nadpisuje bez ostrzeżenia.** Jeśli w celu istnieje plik o tej samej
> nazwie, zostanie zastąpiony po cichu. Dlatego `-i` przy ważnych plikach.

**Pułapka:** kropka jako cel oznacza „katalog bieżący", nie „plik o nazwie kropka":

```bash
cp ../logi/testy.log .        # ✅ kopiuje do katalogu, w którym stoisz
```

### `mv` — przenoszenie i zmiana nazwy

*move*

```bash
mv [flagi] ŹRÓDŁO CEL
```

`mv` robi dwie rzeczy naraz — przenosi **i** zmienia nazwę. To zależy tylko
od tego, czy cel jest katalogiem, czy nazwą pliku.

```bash
mv stary.txt nowy.txt                # zmiana nazwy (cel to nazwa pliku)
mv raport.md ../archiwum/            # przeniesienie (cel to katalog)
mv raport.md ../archiwum/stary.md    # przeniesienie + zmiana nazwy
mv *.log archiwum/                   # przeniesienie wielu plików
mv logi/ dane-testowe/               # zmiana nazwy katalogu (bez -r!)
mv -i raport.md ../archiwum/         # z pytaniem przed nadpisaniem
```

`mv` **nie potrzebuje `-r`** do katalogów — w przeciwieństwie do `cp` i `rm`.
Nie kopiuje zawartości, tylko zmienia wpis w systemie plików.

### `rm` — usuwanie

*remove*

```bash
rm [flagi] ŚCIEŻKA...
```

**Flagi:**

| Flaga | Działanie |
|---|---|
| `-r` | rekurencyjnie — wymagane dla katalogów |
| `-i` | pyta przed każdym usunięciem |
| `-f` | *force* — nie pyta, ignoruje błędy |
| `-v` | pokazuje, co usuwa |

```bash
rm plik.txt                 # usuń plik
rm a.txt b.txt              # usuń kilka
rm *.tmp                    # usuń wszystkie .tmp
rm -i *.log                 # z pytaniem przy każdym
rm -r katalog/              # usuń katalog z całą zawartością
rm -rv katalog/             # to samo, z pokazaniem co leci
```

> ### ☠️ `rm` nie ma kosza
>
> Usunięte = usunięte. Nie ma `Ctrl+Z`, nie ma kosza, nie ma odzyskiwania.
>
> **Nawyki:**
> 1. `pwd` przed każdym `rm`
> 2. Przy `rm` z gwiazdką — najpierw `ls` z tym samym wzorcem:
>    ```bash
>    ls *.log        # ← zobacz, co dokładnie zostanie usunięte
>    rm *.log        # ← dopiero teraz
>    ```
> 3. `rm -rf` traktuj jak ostry nóż. Kombinacja „usuń rekurencyjnie i nie pytaj"
>    nie zostawia żadnej siatki bezpieczeństwa.
> 4. Do pustego katalogu — `rmdir`, nie `rm -r`.

---

## 6. Podgląd zawartości: `cat`, `head`, `tail`, `less`

### `cat` — wypisanie całego pliku

*concatenate* (sklejać)

Nazwa mówi o prawdziwym przeznaczeniu: `cat` **skleja** pliki i wypisuje wynik.
Wyświetlanie jednego pliku to szczególny przypadek sklejania jednego elementu.

```bash
cat plik.txt                    # wypisz zawartość
cat a.txt b.txt                 # wypisz oba, jeden po drugim (SKLEJONE)
cat *.log                       # wszystkie pliki .log jeden po drugim
cat -n plik.txt                 # z numerami linii
cat ../logi/testy.log           # plik z innego katalogu
```

**Flagi:**

| Flaga | Działanie |
|---|---|
| `-n` | numeruje wszystkie linie |
| `-b` | numeruje tylko niepuste linie |
| `-A` | pokazuje znaki niewidoczne (końce linii, tabulatory) |

**Zastosowania w połączeniu z przekierowaniami** (o tym szerzej w sekcji 8):

```bash
cat a.txt b.txt > polaczone.txt      # sklej dwa pliki w nowy
cat fragment.txt >> raport.md        # dołóż zawartość na koniec innego pliku
cat plik.txt | grep "FAIL"           # przekaż zawartość dalej do przetworzenia
```

> **`cat` bez argumentu zawiesza terminal.** Nie ma pliku do czytania,
> więc czeka na tekst z klawiatury. Wyjście: `Ctrl+D` (koniec danych)
> albo `Ctrl+C` (przerwij).
>
> To był jeden z Twoich błędów: `cat | wc -l plik.log` — gdyby nie literówka
> w fladze, terminal by się zablokował.

### `head` i `tail` — początek i koniec

```bash
head plik.log               # pierwsze 10 linii
head -n 3 plik.log          # pierwsze 3 linie
head -5 plik.log            # skrócony zapis: pierwsze 5

tail plik.log               # ostatnie 10 linii
tail -n 20 plik.log         # ostatnie 20
tail -f plik.log            # ŚLEDZENIE — pokazuje nowe linie na żywo
```

**`tail -f` to podstawowe narzędzie QA.** Uruchamiasz testy w jednym oknie,
w drugim `tail -f` na pliku logu i widzisz, co się dzieje w czasie rzeczywistym.
Wyjście: `Ctrl+C`.

```bash
head -20 wielki.log         # podejrzyj strukturę, nie zalewając ekranu
tail -50 testy.log          # zobacz, czym się skończyło
tail -f logs/app.log        # obserwuj na żywo
```

### `less` — przeglądanie długich plików

```bash
less wielki.log
```

Otwiera przeglądarkę zamiast wysypywać wszystko na ekran.

| Klawisz | Działanie |
|---|---|
| `↑` `↓` | linia w górę/dół |
| `Spacja` | strona w dół |
| `g` / `G` | początek / koniec pliku |
| `/tekst` | szukaj w przód |
| `n` / `N` | następne / poprzednie trafienie |
| `q` | wyjście |

**Kiedy czego używać:**

| Sytuacja | Narzędzie |
|---|---|
| Plik krótki, chcesz go całego | `cat` |
| Plik długi, chcesz przejrzeć | `less` |
| Chcesz sprawdzić strukturę | `head` |
| Chcesz zobaczyć wynik/koniec | `tail` |
| Chcesz obserwować na żywo | `tail -f` |

---

## 7. `echo` — wypisywanie tekstu

```bash
echo "tekst"
```

Wypisuje tekst na ekran. Samo w sobie wydaje się bezużyteczne — ale w połączeniu
z `>` i `>>` staje się głównym sposobem tworzenia plików bez edytora.

```bash
echo "Hello"                       # wypisz na ekran
echo Hello                         # to samo (cudzysłów opcjonalny, ale patrz niżej)
echo ""                            # wypisz pustą linię
echo "linia1" > plik.txt           # zapisz do pliku
echo "linia2" >> plik.txt          # dopisz do pliku
echo -n "bez znaku nowej linii"    # nie dodaje entera na końcu
echo -e "linia1\nlinia2"           # -e włącza interpretację \n jako nowej linii
```

**Kiedy cudzysłów jest konieczny:**

```bash
echo Ala ma kota            # zadziała, ale...
echo "Ala  ma  kota"        # ← zachowa podwójne spacje
echo "wynik: 5 > 3"         # ← bez cudzysłowu > zostałoby przekierowaniem!
echo "test (nowy)"          # ← nawiasy mają znaczenie w bashu
```

> **Zasada:** jeśli tekst zawiera spacje, `>`, `<`, `|`, `*`, `(`, `)`, `&`,
> `;` albo cokolwiek nieoczywistego — daj cudzysłów. To kosztuje dwa znaki
> i eliminuje całą kategorię błędów.

**Cudzysłów podwójny vs pojedynczy:**

```bash
echo "$HOME"       # /home/kapi     ← podstawia wartość zmiennej
echo '$HOME'       # $HOME          ← bierze dosłownie
```

Podwójny cudzysłów pozwala na podstawienia, pojedynczy blokuje wszystko.
Na start: używaj podwójnego.

---

## 8. Strumienie — najważniejsza sekcja w tej notatce

Tu jest sedno. Jeśli zrozumiesz ten model, `>`, `>>`, `|` i `<` przestają być
zestawem znaczków do zapamiętania, a stają się jedną spójną ideą.

### Model mentalny: każdy program ma trzy rury

Wyobraź sobie, że każde uruchomione polecenie to maszyna z trzema podłączonymi rurami:

```
                    ┌─────────────────┐
   stdin (0) ──────▶│                 │──────▶ stdout (1)   ← normalny wynik
   wejście          │     PROGRAM     │
                    │                 │──────▶ stderr (2)   ← komunikaty błędów
                    └─────────────────┘
```

| Rura | Nazwa | Domyślnie podłączona do |
|---|---|---|
| **stdin** | standard input | klawiatura |
| **stdout** | standard output | ekran |
| **stderr** | standard error | ekran |

**Domyślnie:** dane wchodzą z klawiatury, wynik i błędy lecą na ekran.
Dlatego `cat plik.txt` pokazuje tekst — nie dlatego, że `cat` „umie wyświetlać",
tylko dlatego, że jego stdout jest podpięty do ekranu.

**Operatory przekierowań to nic innego jak przepinanie tych rur.**

| Operator | Co robi |
|---|---|
| `>` | przepina **stdout** z ekranu na **plik** (nadpisując) |
| `>>` | przepina **stdout** z ekranu na **plik** (dopisując) |
| `<` | przepina **stdin** z klawiatury na **plik** |
| `\|` | przepina **stdout** jednego programu na **stdin** drugiego |
| `2>` | przepina **stderr** na plik |

To wszystko. Jedna idea, pięć zapisów.

---

### `>` — nadpisanie (redirect, truncate)

```bash
polecenie > plik
```

**Co dokładnie się dzieje, w kolejności:**

1. Powłoka **otwiera plik do zapisu**
2. Jeśli plik nie istnieje → **tworzy go**
3. Jeśli plik istnieje → **kasuje całą jego zawartość** (technicznie: skraca go do zera bajtów)
4. Dopiero **teraz** uruchamia polecenie
5. Wszystko, co program wypisałby na ekran, ląduje w pliku

**Punkt 3 i 4 to najważniejszy szczegół w tej notatce.**

Plik jest czyszczony **zanim polecenie w ogóle wystartuje**. Nie „po",
nie „w trakcie". Przed.

Konsekwencja, która niszczy dane:

```bash
grep "FAIL" raport.txt > raport.txt
```

Wygląda niewinnie: „przefiltruj raport i zapisz wynik z powrotem".
W rzeczywistości:

1. Powłoka czyści `raport.txt` → **plik jest teraz pusty**
2. Startuje `grep`, który ma czytać `raport.txt`
3. `grep` czyta pusty plik, nic nie znajduje
4. Zostaje pusty plik

**Dane bezpowrotnie utracone.** Nigdy nie kieruj wyniku do tego samego pliku,
z którego czytasz. Użyj pliku tymczasowego:

```bash
grep "FAIL" raport.txt > tymczasowy.txt
mv tymczasowy.txt raport.txt
```

### Zastosowania `>`

```bash
# 1. Utworzenie pliku z tekstem (bez edytora!)
echo "# Raport z testow" > raport.md

# 2. Zapisanie wyniku polecenia do pliku
ls -l > lista-plikow.txt
pwd > gdzie-jestem.txt
grep "FAIL" *.log > bledy.txt

# 3. Zapisanie wyniku potoku
grep "FAIL" *.log | wc -l > liczba-bledow.txt

# 4. Wyczyszczenie pliku bez usuwania go
> plik.log
# ← bez polecenia z lewej! Powłoka czyści plik i nie ma czego uruchomić.
#   Plik zostaje, ale jest pusty. Częste przy resetowaniu logów.

# 5. Zapisanie do pliku w innym katalogu
grep "FAIL" ../logi/*.log > ../raporty/bledy.txt

# 6. Nadpisanie istniejącego pliku nową zawartością (świadome)
echo "nowa zawartosc" > stary-plik.txt
```

---

### `>>` — dopisanie (append)

```bash
polecenie >> plik
```

**Co się dzieje:**

1. Powłoka otwiera plik **w trybie dopisywania**
2. Jeśli plik nie istnieje → tworzy go
3. Jeśli plik istnieje → **nie rusza zawartości**, ustawia się na końcu
4. Uruchamia polecenie
5. Wynik jest **doklejany na końcu** istniejącej treści

### `>` vs `>>` — porównanie na żywym przykładzie

Test, który warto wykonać u siebie:

```bash
echo "pierwsza" > test.txt
cat test.txt
# pierwsza

echo "druga" > test.txt        # znowu >
cat test.txt
# druga                        ← "pierwsza" ZNIKŁA
```

A teraz z `>>`:

```bash
echo "pierwsza" > test.txt     # > tworzy plik od zera
echo "druga" >> test.txt       # >> dokłada
echo "trzecia" >> test.txt     # >> dokłada
cat test.txt
# pierwsza
# druga
# trzecia
```

| | `>` | `>>` |
|---|---|---|
| Plik nie istnieje | tworzy | tworzy |
| Plik istnieje | **kasuje zawartość** | zachowuje zawartość |
| Gdzie pisze | od początku | na końcu |
| Analogia | nowa kartka | dopisanie linijki na dole |
| Ryzyko | **utrata danych** | brak |

> ### 🔑 Wzorzec budowania pliku linia po linii
>
> **Pierwsza linia przez `>`, wszystkie kolejne przez `>>`.**
>
> ```bash
> echo "linia 1" >  plik.txt      # start — czyści ewentualne stare śmieci
> echo "linia 2" >> plik.txt      # dokładanie
> echo "linia 3" >> plik.txt      # dokładanie
> ```
>
> **Dlaczego pierwsza przez `>`, a nie od razu `>>`?**
>
> Bo `>` gwarantuje czysty start. Gdybyś uruchomił ten sam skrypt drugi raz
> z samymi `>>`, dokleiłbyś kolejne trzy linie do poprzednich sześciu.
> `>` na początku daje **idempotencję** — ten sam wynik niezależnie od tego,
> ile razy uruchomisz.
>
> **Co się stanie, jeśli wszystkie linie dasz przez `>`?**
>
> Zostanie tylko ostatnia. Każde `>` zaczyna od wyczyszczenia pliku.

### Zastosowania `>>`

```bash
# 1. Budowanie pliku krok po kroku
echo "# Raport" > raport.md
echo "" >> raport.md
echo "## Wyniki" >> raport.md

# 2. Dołożenie zawartości innego pliku
cat bledy.txt >> raport.md

# 3. Dopisanie wyniku polecenia do istniejącego pliku
date >> raport.md
grep "FAIL" *.log >> wszystkie-bledy.txt

# 4. Prowadzenie dziennika / logu
echo "$(date): uruchomiono testy" >> historia.log

# 5. Zbieranie wyników z wielu źródeł do jednego pliku
grep "FAIL" dzien1.log >> zbiorczy.txt
grep "FAIL" dzien2.log >> zbiorczy.txt
grep "FAIL" dzien3.log >> zbiorczy.txt
```

### Pusta linia w pliku

```bash
echo "" >> plik.md
```

`echo ""` wypisuje pusty tekst plus znak nowej linii — czyli efektywnie
pustą linię. W Markdownie to bardzo ważne, bo puste linie oddzielają akapity.

---

### `|` — potok (pipe)

```bash
polecenie1 | polecenie2
```

Bierze **stdout** pierwszego polecenia i podłącza go jako **stdin** drugiego.
Dane nie pojawiają się po drodze na ekranie ani nie lądują w żadnym pliku —
płyną prosto z jednego programu do drugiego.

### `>` vs `|` — kluczowa różnica

| | `>` | `\|` |
|---|---|---|
| Dokąd kieruje dane | do **pliku** | do **programu** |
| Po prawej stronie stoi | nazwa pliku | polecenie |
| Wynik | zapisany na dysku | przetwarzany dalej |

```bash
grep "FAIL" *.log > bledy.txt     # dane → PLIK
grep "FAIL" *.log | wc -l         # dane → PROGRAM
```

### Zastosowania `|`

```bash
# 1. Policz wyniki wyszukiwania
grep "FAIL" *.log | wc -l

# 2. Przejrzyj długi wynik strona po stronie
ls -la /usr/bin | less

# 3. Zobacz tylko początek długiego wyniku
ls -la | head -20

# 4. Filtruj wynik innego polecenia
ls -la | grep "log"
history | grep "mkdir"

# 5. Łańcuch wieloelementowy — dane płyną przez kolejne etapy
cat *.log | grep "FAIL" | sort | uniq | wc -l
#   │        │            │      │       └── policz
#   │        │            │      └── usuń duplikaty
#   │        │            └── posortuj
#   │        └── zostaw tylko FAIL
#   └── wypisz wszystkie logi

# 6. Potok + przekierowanie na końcu (bardzo częsty wzorzec)
grep "FAIL" *.log | wc -l > liczba-bledow.txt
#                            └── ostatni etap trafia do pliku
```

### Ważny szczegół: `wc -l plik` vs `cat plik | wc -l`

```bash
wc -l testy.log
# 5 testy.log        ← wc otworzył plik sam, więc zna jego nazwę

cat testy.log | wc -l
# 5                  ← wc dostał goły strumień, nie wie skąd pochodzi
```

To **nie jest kosmetyka**. Jeśli zapisujesz wynik do pliku i chcesz tam mieć
samą liczbę, musisz użyć potoku:

```bash
wc -l bledy.txt > liczba.txt          # w pliku: "3 bledy.txt"
cat bledy.txt | wc -l > liczba.txt    # w pliku: "3"   ← to chcesz
```

> **Uwaga na `grep -c` przy wielu plikach.** Kusi, żeby napisać
> `grep -c "FAIL" *.log`, ale to **nie da sumy** — da osobny licznik
> dla każdego pliku:
>
> ```
> ../logi/d1.log:2
> ../logi/d2.log:2
> ```
>
> Żeby dostać jedną liczbę zbiorczą, musisz przepuścić trafienia przez potok:
>
> ```bash
> grep -i "fail" ../logi/*.log | wc -l      # → 4
> ```
>
> `grep -c` jest użyteczne tylko przy **jednym** pliku.

---

### `<` — przekierowanie wejścia

```bash
polecenie < plik
```

Zamiast czekać na tekst z klawiatury, program czyta z pliku.

```bash
wc -l < plik.txt        # 5      ← bez nazwy pliku, bo wc go nie otwierał
sort < nazwy.txt        # posortuj zawartość pliku
```

Używa się rzadziej — większość poleceń i tak przyjmuje nazwę pliku jako argument.
Warto znać, żeby rozumieć cudze skrypty.

---

### `2>` — przekierowanie błędów

Programy wypisują komunikaty błędów na **stderr**, nie stdout. Dlatego `>`
ich nie łapie:

```bash
ls nieistniejacy > wynik.txt
# ls: cannot access 'nieistniejacy': No such file or directory
# ← błąd nadal na ekranie! Bo poleciał przez stderr, a > łapie tylko stdout
```

```bash
ls nieistniejacy 2> bledy.txt      # błędy → plik
ls nieistniejacy 2> /dev/null      # błędy → wyrzuć do kosza systemowego
ls * > wynik.txt 2> bledy.txt      # wynik i błędy do osobnych plików
ls * > wszystko.txt 2>&1           # oba strumienie do jednego pliku
ls * &> wszystko.txt               # skrócony zapis tego samego
```

`/dev/null` to „czarna dziura" systemu — wszystko, co tam trafi, znika.

**Zastosowanie w QA:** rozdzielenie wyników testów od komunikatów o błędach:

```bash
./uruchom-testy.sh > wyniki.txt 2> bledy.txt
```

---

### Kolejność operatorów — częsta pomyłka

```bash
grep "FAIL" *.log | wc -l > liczba.txt    # ✅
grep "FAIL" *.log > liczba.txt | wc -l    # ❌
```

W drugim przypadku cały wynik `grep` idzie do pliku, więc do `wc` nie dociera nic.

**Zasada:** `>` zawsze na samym końcu łańcucha.

---

### Podsumowanie sekcji

```
polecenie              →  ekran
polecenie > plik       →  plik (nadpisany)
polecenie >> plik      →  plik (dopisany na końcu)
polecenie | inne       →  wejście innego programu
polecenie < plik       →  plik jako wejście
polecenie 2> plik      →  błędy do pliku
```

---

## 9. Liczenie i sortowanie: `wc`, `sort`, `uniq`

### `wc` — word count

```bash
wc plik.txt
#   5  20 203 plik.txt
#   │   │   │
#   │   │   └── bajty
#   │   └── słowa
#   └── linie
```

| Flaga | Liczy |
|---|---|
| `-l` | linie (*lines*) — **mała litera L, nie cyfra 1** |
| `-w` | słowa (*words*) |
| `-c` | bajty (*characters*) |
| `-m` | znaki (różni się od `-c` przy polskich znakach) |

```bash
wc -l plik.log                  # ile linii
wc -l *.log                     # ile linii w każdym pliku + suma
cat plik.log | wc -l            # ile linii (sama liczba)
grep "FAIL" *.log | wc -l       # ile trafień
ls | wc -l                      # ile plików w katalogu
```

> **Twój błąd:** `wc -1` (cyfra jeden) zamiast `wc -l` (litera L).
> Komunikat `invalid option -- '1'` mówi dokładnie to: „nie znam opcji 1".
> Gdy widzisz `invalid option`, sprawdź najpierw znak po myślniku.

### `sort` — sortowanie linii

```bash
sort plik.txt              # alfabetycznie
sort -r plik.txt           # odwrotnie
sort -n liczby.txt         # numerycznie (2 przed 10, nie odwrotnie!)
sort -u plik.txt           # posortuj i usuń duplikaty
cat *.log | sort           # posortuj zawartość wielu plików
```

Różnica `sort` vs `sort -n`:

```
sort:     1, 10, 2, 20, 3      ← alfabetycznie, "10" < "2" bo "1" < "2"
sort -n:  1, 2, 3, 10, 20      ← numerycznie
```

### `uniq` — usuwanie duplikatów

```bash
uniq plik.txt              # usuń SĄSIADUJĄCE duplikaty
uniq -c plik.txt           # policz wystąpienia
uniq -d plik.txt           # pokaż tylko te, które się powtarzają
```

> **`uniq` usuwa tylko sąsiadujące duplikaty.** Dlatego prawie zawsze
> występuje po `sort`:
>
> ```bash
> sort plik.txt | uniq         # ✅ najpierw posortuj, potem odduplikuj
> uniq plik.txt                # ❌ przepuści duplikaty rozrzucone po pliku
> ```

**Klasyczny wzorzec — ranking:**

```bash
cat *.log | grep "FAIL" | sort | uniq -c | sort -rn
#                                  │        └── posortuj po liczbie, malejąco
#                                  └── policz wystąpienia
```

To pokazuje, które testy failują najczęściej. Bezpośrednio użyteczne w QA.

---

## 10. Szukanie tekstu: `grep`

*global regular expression print*

```bash
grep [flagi] "WZORZEC" PLIK...
```

`grep` przegląda plik linia po linii i wypisuje te, które pasują do wzorca.

### Flagi

| Flaga | Działanie |
|---|---|
| `-i` | ignoruje wielkość liter (*ignore case*) |
| `-v` | odwraca — pokazuje linie **niepasujące** (*invert*) |
| `-c` | zwraca tylko **liczbę** pasujących linii (*count*) |
| `-n` | pokazuje numery linii |
| `-r` | przeszukuje katalog rekurencyjnie |
| `-l` | pokazuje tylko **nazwy plików**, w których jest trafienie |
| `-h` | **ukrywa** nazwy plików przed trafieniami (*hide*) |
| `-w` | dopasowuje całe słowa |
| `-E` | rozszerzone wyrażenia regularne (pozwala na `|` jako „lub") |
| `-A 3` | pokaż 3 linie **po** trafieniu (*after*) |
| `-B 3` | pokaż 3 linie **przed** trafieniem (*before*) |

### Zastosowania

```bash
# 1. Podstawowe szukanie
grep "FAIL" testy.log

# 2. W wielu plikach naraz (grep dokleja nazwę pliku)
grep "FAIL" testy1.log testy2.log
grep "FAIL" *.log
grep "FAIL" ../logi/*.log

# 3. Bez względu na wielkość liter ← ROZWIĄZUJE PROBLEM Z "failed"
grep -i "fail" *.log

# 4. Policz trafienia bez wypisywania ich
grep -c "FAIL" testy.log

# 5. Znajdź linie NIEpasujące
grep -v "PASS" testy.log          # wszystko oprócz udanych testów

# 6. Z numerami linii (przydatne przy debugowaniu)
grep -n "Exception" app.log

# 7. Rekurencyjnie w całym drzewie katalogów
grep -r "TODO" ~/nauka-ai/

# 8. Tylko nazwy plików zawierających wzorzec
grep -rl "FAIL" ~/projekt/

# 9. Kilka wzorców naraz (alternatywa: | znaczy "lub")
grep -E "FAIL|ERROR|Exception" app.log

# 10. Kontekst wokół trafienia — kluczowe przy analizie błędów
grep -A 5 "Exception" app.log     # 5 linii po
grep -B 2 "Exception" app.log     # 2 linie przed
grep -n -A 3 -B 1 "ERROR" app.log # numery + kontekst z obu stron

# 11. Łączenie flag
grep -in "fail" *.log             # ignoruj wielkość liter + numery linii
grep -ic "fail" *.log             # ignoruj wielkość liter + policz

# 12. Grep na wyjściu innego polecenia (przez potok)
ls -la | grep "log"
history | grep "grep"
cat *.log | grep "FAIL"
```

### Pułapka wielkości liter

```
2026-08-29 10:11 failed koszyk_usuniecie_produktu
```

```bash
grep "FAIL" *.log        # ❌ NIE złapie "failed" — inna wielkość liter
grep -i "fail" *.log     # ✅ złapie "FAIL", "failed", "Fail", "FAILED"
```

To była pułapka w Twoim zadaniu praktycznym. **W realnych logach formaty są
niespójne** — różne biblioteki, różne wersje, różni programiści. `grep -i`
to domyślny wybór przy analizie logów, chyba że masz powód, żeby rozróżniać.

### Prefiks nazwy pliku przy wielu plikach

Gdy `grep` przeszukuje **więcej niż jeden plik**, dokleja nazwę pliku
przed każdym trafieniem:

```bash
grep -i "fail" ../logi/*.log
# ../logi/d1.log:2026-08-28 09:13 FAIL a
# ../logi/d2.log:2026-08-29 10:06 FAIL c
#  └─────┬─────┘
#        └── prefiks dodany przez grep
```

Przy jednym pliku prefiksu nie ma — `grep` uznaje, że i tak wiadomo, skąd
pochodzą linie.

**To bywa pomocne** (widzisz, w którym dniu wystąpił błąd) **i bywa
przeszkadzające** (gdy budujesz czysty raport). Wyłącza się flagą `-h`:

```bash
grep -hi "fail" ../logi/*.log
# 2026-08-28 09:13 FAIL a
# 2026-08-29 10:06 FAIL c
```

### Cudzysłów przy wzorcu

```bash
grep "test failed" plik.log      # ✅ spacja wewnątrz wzorca
grep test failed plik.log        # ❌ "failed" zostanie uznane za nazwę pliku
```

Zawsze cudzysłów wokół wzorca. Zawsze.

---

## 11. Szukanie plików: `find`

```bash
find GDZIE_SZUKAĆ [kryteria]
```

### `grep` vs `find` — nie mylić

| | `grep` | `find` |
|---|---|---|
| Szuka | **tekstu wewnątrz** plików | **plików** po nazwie/właściwościach |
| Pytanie | „w którym pliku jest słowo FAIL?" | „gdzie są pliki .log?" |

### Zastosowania

```bash
# 1. Wszystkie pliki .log w drzewie
find ~/cwiczenia-cli -name "*.log"

# 2. Szukanie od katalogu bieżącego
find . -name "*.md"

# 3. Bez względu na wielkość liter
find . -iname "*.LOG"

# 4. Tylko pliki (nie katalogi)
find . -type f

# 5. Tylko katalogi
find . -type d
find . -type d -name "logi"

# 6. Po fragmencie nazwy
find . -name "*raport*"

# 7. Modyfikowane w ostatnich 24h — świetne do debugowania
find . -mtime -1

# 8. Większe niż 1 MB
find . -size +1M

# 9. Ograniczenie głębokości przeszukiwania
find . -maxdepth 2 -name "*.log"

# 10. find + potok
find . -name "*.log" | wc -l                  # ile plików .log
find . -name "*.log" > lista-logow.txt        # zapisz listę
```

### Dlaczego cudzysłów jest obowiązkowy

```bash
find . -name "*.log"      # ✅ find dostaje wzorzec *.log
find . -name *.log        # ❌ powłoka rozwija * ZANIM find wystartuje
```

Bez cudzysłowu powłoka podstawia nazwy plików z katalogu bieżącego,
a `find` dostaje coś zupełnie innego, niż zamierzałeś.

---

## 12. Wildcards (globbing)

`*`, `?` i `[]` **nie są częścią poleceń**. To powłoka rozwija je na listę
nazw plików, zanim polecenie w ogóle wystartuje.

```bash
ls *.log
```

Powłoka najpierw zamienia to na:

```bash
ls testy-2026-08-28.log testy-2026-08-29.log
```

i dopiero to uruchamia. `ls` nigdy nie widzi gwiazdki.

### Wzorce

| Wzorzec | Znaczenie |
|---|---|
| `*` | dowolny ciąg znaków, także pusty |
| `?` | dokładnie jeden dowolny znak |
| `[abc]` | jeden znak z listy |
| `[0-9]` | jeden znak z zakresu |
| `{a,b}` | rozwinięcie na warianty (bez spacji po przecinku!) |

```bash
ls *.log                    # wszystkie z rozszerzeniem .log
ls testy-*                  # wszystkie zaczynające się od "testy-"
ls *2026*                   # wszystkie zawierające "2026"
ls testy-?.log              # testy-1.log, testy-a.log (jeden znak)
ls testy-[12].log           # tylko testy-1.log i testy-2.log
ls *.{log,txt}              # pliki .log ORAZ .txt
mkdir -p projekt/{src,tests,docs}    # trzy katalogi jednym poleceniem
```

> ### 🛡️ Zasada bezpieczeństwa przy gwiazdce
>
> **Zanim użyjesz `*` z poleceniem niszczącym, sprawdź wzorzec przez `ls`.**
>
> ```bash
> ls *.log        # ← co dokładnie pasuje?
> rm *.log        # ← dopiero teraz
> ```
>
> `rm *` i `rm -rf *` to najczęstsze przyczyny katastrof w terminalu.
> Jedna spacja za dużo (`rm * .log` zamiast `rm *.log`) zmienia znaczenie
> polecenia całkowicie.

---

## 13. Typowe błędy — Twoje własne

Zbiór z Modułów 0 i 1. Warto do niego wracać.

### Błąd 1 — brak `/` na początku ścieżki bezwzględnej

```bash
cd home/kapi        # ❌ szuka podkatalogu "home" w katalogu bieżącym
cd /home/kapi       # ✅
```

**Mechanizm:** brak `/` = ścieżka względna = liczona od `pwd`.

### Błąd 2 — podwojenie segmentu ścieżki

```bash
# Stoisz w ~/cwiczenia-cli:
cd cwiczenia-cli/raport-testow   # ❌ szuka cwiczenia-cli WEWNĄTRZ cwiczenia-cli
cd raport-testow                 # ✅
```

**Mechanizm:** liczysz ścieżkę od domu zamiast od `pwd`.
**Lekarstwo:** `pwd` przed zbudowaniem ścieżki. Za każdym razem.

### Błąd 3 — spacja rozdzielająca argumenty

```bash
mkdir -p cwiczenia-cli/raport-testow/logi raporty
#                                        └── to osobny argument, liczony od pwd!
```

**Mechanizm:** spacja kończy ścieżkę. Każdy argument startuje od `pwd`.
**Lekarstwo:** klamry `{logi,raporty}` albo pełna ścieżka w każdym argumencie.

### Błąd 4 — cyfra zamiast litery we fladze

```bash
wc -1 plik.log      # ❌ invalid option -- '1'
wc -l plik.log      # ✅ mała litera L, od "lines"
```

**Mechanizm:** `1` i `l` wyglądają podobnie w wielu czcionkach.
**Lekarstwo:** komunikat `invalid option` → sprawdź znak po myślniku.

### Błąd 5 — `cat` bez argumentu zawiesza terminal

```bash
cat | wc -l plik.log     # ❌ cat czeka na tekst z klawiatury
```

**Lekarstwo:** `Ctrl+D` (koniec danych) lub `Ctrl+C` (przerwij).

### Błąd 6 — `grep` gubi trafienia przez wielkość liter

```bash
grep "FAIL" *.log        # ❌ nie złapie "failed"
grep -i "fail" *.log     # ✅
```

### Błąd 7 — użycie edytora zamiast przekierowań

W zadaniu praktycznym chodziło o ćwiczenie `>` i `>>`. `nano` obchodzi
dokładnie tę umiejętność.

**Kiedy edytor jest w porządku:** przy realnej pracy nad dużym plikiem.
**Kiedy nie:** gdy ćwiczysz przekierowania albo piszesz skrypt, który ma
działać bez człowieka przy klawiaturze.

### Błąd 8 — nadpisanie pliku, z którego się czyta

```bash
grep "FAIL" raport.txt > raport.txt     # ❌ raport.txt zostanie pusty
```

**Mechanizm:** `>` czyści plik **przed** uruchomieniem `grep`.

### Błąd 9 — `grep -c` przy wielu plikach nie daje sumy

```bash
grep -c "FAIL" *.log        # ❌ osobny licznik dla każdego pliku
grep "FAIL" *.log | wc -l   # ✅ jedna liczba zbiorcza
```

**Ten błąd znalazłem w pierwszej wersji tej notatki podczas jej weryfikacji.**
Napisałem, że `grep -c` „też działa" do policzenia wszystkich błędów — nie działa.
Wykryłem to dopiero, gdy uruchomiłem przykład na prawdziwych plikach.

To jest praktyczna ilustracja zasady z nagłówka: **notatka, dokumentacja
i wygenerowany kod mogą zawierać błędy, które widać dopiero przy uruchomieniu.**

### Błąd z poprzedniego modułu (mój, nie Twój)

W notatce 1.2 przykład `cp` był napisany z założeniem innego katalogu roboczego,
niż wynikało z kontekstu. Stąd zasada z nagłówka tej notatki: **weryfikuj
przykłady empirycznie**. To dotyczy każdej dokumentacji, nie tylko mojej —
a szczególnie tego, co wygeneruje agent AI.

---

## 14. Ściąga

### Nawigacja
```bash
pwd                     # gdzie jestem
cd KATALOG              # wejdź
cd ..                   # piętro wyżej
cd ~                    # do domu
cd -                    # do poprzedniego katalogu
ls                      # co tu jest
ls -la                  # szczegóły + ukryte
ls -lt                  # posortowane po dacie
```

### Katalogi i pliki
```bash
mkdir KATALOG           # utwórz katalog
mkdir -p a/b/c          # utwórz całą ścieżkę
mkdir -p x/{a,b}        # dwa katalogi w x
rmdir KATALOG           # usuń PUSTY katalog (bezpieczne)
touch PLIK              # utwórz pusty plik
cp A B                  # kopiuj
cp -r KAT1 KAT2         # kopiuj katalog
mv A B                  # przenieś / zmień nazwę
rm PLIK                 # usuń plik
rm -r KATALOG           # usuń katalog z zawartością (uwaga!)
```

### Podgląd
```bash
cat PLIK                # cała zawartość
cat -n PLIK             # z numerami linii
head -20 PLIK           # pierwsze 20 linii
tail -20 PLIK           # ostatnie 20 linii
tail -f PLIK            # śledź na żywo
less PLIK               # przeglądaj (q = wyjście)
```

### Strumienie
```bash
POLECENIE > PLIK        # zapisz (NADPISUJE)
POLECENIE >> PLIK       # dopisz na końcu
POLECENIE | INNE        # przekaż do innego programu
POLECENIE < PLIK        # plik jako wejście
POLECENIE 2> PLIK       # błędy do pliku
> PLIK                  # wyczyść plik
```

### Wyszukiwanie
```bash
grep "WZORZEC" PLIK     # szukaj tekstu
grep -i "wzorzec" PLIK  # ignoruj wielkość liter
grep -c "WZORZEC" PLIK  # policz trafienia
grep -v "WZORZEC" PLIK  # linie NIEpasujące
grep -n "WZORZEC" PLIK  # z numerami linii
grep -r "WZORZEC" KAT/  # rekurencyjnie
find . -name "*.log"    # znajdź pliki
```

### Przetwarzanie
```bash
wc -l PLIK              # policz linie
sort PLIK               # posortuj
sort -n PLIK            # posortuj numerycznie
uniq PLIK               # usuń sąsiadujące duplikaty
sort PLIK | uniq -c     # policz wystąpienia
```

### Wzorce QA — gotowce do wykorzystania
```bash
# Wszystkie błędy z logów do jednego pliku
grep -i "fail" ../logi/*.log > bledy.txt

# Ile błędów łącznie (sama liczba)
grep -i "fail" ../logi/*.log | wc -l
# UWAGA: grep -c przy wielu plikach da licznik per plik, nie sumę!

# Ranking najczęściej failujących testów
cat *.log | grep -i "fail" | sort | uniq -c | sort -rn

# Kontekst wokół wyjątku
grep -n -A 5 -B 2 "Exception" app.log

# Obserwacja testów na żywo
tail -f wyniki-testow.log

# Rozdzielenie wyników od błędów
./uruchom-testy.sh > wyniki.txt 2> bledy.txt
```

---

## 15. Pytania testowe

Odpowiadaj bez zaglądania do notatki.

### Ścieżki
1. Czym różni się ścieżka bezwzględna od względnej? Po czym rozpoznasz, która jest która?
2. Od czego zawsze startuje ścieżka względna?
3. Co oznaczają `.`, `..`, `~`?
4. Stoisz w `/home/kapi/projekt/testy/wyniki`. Napisz ścieżkę względną do `/home/kapi/projekt/README.md`.
5. Dlaczego `cd home/kapi` nie działa, gdy stoisz w `/home/kapi`?

### Przekierowania
6. Czym różni się `>` od `>>`? Opisz oba przypadki: gdy plik istnieje i gdy nie istnieje.
7. Co się stanie, jeśli zbudujesz plik pięciolinijkowy używając samego `>`? Dlaczego?
8. Dlaczego przy budowaniu pliku pierwszą linię daje się przez `>`, a nie od razu `>>`?
9. Co robi `> plik.log` bez polecenia po lewej stronie?
10. Dlaczego `grep "FAIL" raport.txt > raport.txt` niszczy dane? Opisz kolejność zdarzeń.
11. Czym różni się `>` od `|`?
12. Dlaczego `ls nieistniejacy > wynik.txt` nadal pokazuje błąd na ekranie?

### Polecenia
13. Do czego służy flaga `-p` w `mkdir`? Co się stanie bez niej przy `mkdir a/b/c`?
14. Dlaczego `mkdir -p x/y/z w` nie tworzy `w` wewnątrz `x/y/z`?
15. Kiedy użyć `rmdir` zamiast `rm -r`? Dlaczego to jest bezpieczniejsze?
16. `cp` wymaga `-r` do katalogów, `mv` nie. Dlaczego?
17. Co zrobi `cat` uruchomiony bez argumentu? Jak się z tego wydostać?
18. Czym różni się `wc -l plik` od `cat plik | wc -l`? Kiedy ta różnica ma znaczenie?
19. Dlaczego `uniq` prawie zawsze występuje po `sort`?

### grep i find
20. Czym różni się `grep` od `find`?
21. Log zawiera `FAIL`, `failed` i `Failed`. Jak złapać wszystkie trzy?
22. Co robi `grep -v`? Podaj praktyczne zastosowanie w QA.
23. Do czego służą `-A` i `-B` w `grep`? Dlaczego to ważne przy analizie błędów?
24. Dlaczego `find . -name "*.log"` musi mieć cudzysłów?

### Scenariusze praktyczne
25. Stoisz w `~/projekt/raporty`. W `~/projekt/logi` są pliki `.log`. Napisz jedno polecenie, które zapisze wszystkie linie z błędami (dowolna wielkość liter) do `bledy.txt` w katalogu, w którym stoisz. Bez `cd`.
26. Napisz polecenie, które zapisze do pliku **samą liczbę** błędów, bez nazwy pliku źródłowego.
27. Masz plik `raport.md` z nagłówkiem. Chcesz dołożyć na koniec zawartość `bledy.txt`. Jakie polecenie?
28. Napisz łańcuch, który pokaże, które testy failują najczęściej, posortowane malejąco.
29. Testy działają i zapisują do `wyniki.log`. Chcesz obserwować je na żywo. Co robisz?
30. Chcesz usunąć wszystkie pliki `.tmp` w katalogu. Opisz bezpieczną procedurę krok po kroku.

---

## Miejsce na Twoje notatki

> Sekcja do uzupełnienia własnymi słowami. Nie przepisuj powyższego —
> napisz to tak, jak sam byś to wytłumaczył koledze z zespołu.

### `>` i `>>` własnymi słowami

*(do uzupełnienia)*

### Ścieżki względne — jak sobie to wyobrażam

*(do uzupełnienia)*

### Czego się nauczyłem na własnych błędach

*(do uzupełnienia)*

### Jak wykorzystam to w pracy QA

*(do uzupełnienia)*
