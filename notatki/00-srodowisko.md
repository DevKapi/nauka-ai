# 00 — Przygotowanie środowiska

Data: 2026-08-28
Moduł: 0
Cel: działające stanowisko do pracy z agentami AI z poziomu terminala

## 1. Konfiguracja stanowiska

System: Windows + WSL 2 (Ubuntu)

| Narzędzie | Wersja | Jak sprawdzić |
|---|---|---|
| Git | 2.43.0 | `git --version` |
| GitHub CLI | 2.45.0 | `gh --version` |
| Claude Code | 2.1.251 | `claude --version` |
| WSL | 2 | `wsl -l -v` (z PowerShella) |

Claude Code wymaga płatnego konta: Pro, Max, Team, Enterprise albo Console.
Darmowy plan Claude.ai nie daje do niego dostępu.

## 2. Budowa komendy

Schemat: `program flagi argumenty`

- **program** — co uruchamiam (`apt`, `git`, `claude`)
- **flagi/opcje** — JAK ma się zachować (`-y`, `--global`). Zaczynają się od myślnika.
  Krótkie można sklejać: `-fsSL` = `-f -s -S -L`
- **argumenty** — NA CZYM ma zadziałać (nazwy pakietów, plików, wartości)

Przykład: `sudo apt install -y git curl`
program `apt` → podkomenda `install` → flaga `-y` → argumenty `git curl`

Spacje oddzielają elementy, dlatego wartości ze spacjami trzeba brać w cudzysłów:
`git config --global user.name "Kacper Kowalski"`

## 3. WSL

WSL (Windows Subsystem for Linux) to podsystem Windowsa, który pozwala uruchomić
dystrybucję Linuksa bez maszyny wirtualnej i bez dual boota.

Różnica wersji:
- **WSL 1** — warstwa tłumacząca wywołania systemowe Linuksa na windowsowe.
  Szybszy dostęp do plików Windowsa, ale niepełna kompatybilność.
- **WSL 2** — prawdziwe jądro Linuksa w lekkiej maszynie wirtualnej.
  Pełna kompatybilność, obsługa Dockera i sandboxingu. To jest domyślne i wybrane.

WSL 2 NIE jest emulatorem. Emulacją była wersja 1, która tłumaczyła wywołania
systemowe. Wersja 2 uruchamia prawdziwe jądro Linuksa.

Dlaczego WSL, a nie PowerShell:
1. Cały ekosystem AI (kursy, dokumentacja, skille, pluginy, przykłady na GitHubie)
   zakłada bash. Komendy typu `ls`, `grep`, `chmod` to składnia uniksowa.
   W PowerShellu nauczyłbym się innego zestawu, nierozpoznawalnego w tutorialach.
2. Sandboxing, czyli izolowane wykonywanie komend przez agenta, działa
   tylko na WSL 2.
3. Bash jest przenośny: serwery, CI/CD, kontenery, praca w innej firmie.
   PowerShell zostaje na Windowsie.

CZEGO WSL NIE ROBI: nie jest potrzebny do Gita. Git działa natywnie na Windowsie,
macOS i Linuksie. Commity i pushe robiłbym tak samo w PowerShellu.

Sprawdzenie stanu: `wsl -l -v` (z PowerShella) — dystrybucje, ich stan i wersja WSL.

## 4. Zarządzanie pakietami (apt)

`sudo apt update && sudo apt upgrade -y`

- `sudo` — wykonanie z uprawnieniami administratora. Pyta o MOJE hasło, nie roota.
  Potrzebne, bo pakiety instalują się poza katalogiem domowym, w plikach systemowych.
- `apt` — menedżer pakietów Ubuntu. Pobiera z oficjalnych repozytoriów,
  weryfikuje podpisy, dociąga zależności.
- `apt update` — NIE aktualizuje programów i NIE aktualizuje samego apt.
  Odświeża lokalną listę tego, co jest dostępne w repozytoriach i w jakich wersjach.
  To jak pobranie aktualnego cennika ze sklepu.
- `apt upgrade -y` — dopiero to porównuje listę z tym, co mam zainstalowane,
  i instaluje nowsze wersje. `-y` odpowiada twierdząco na pytania y/n.

Co się stanie bez `update`: `upgrade` zadziała, ale na PRZESTARZAŁEJ liście.
System uzna, że wszystko jest aktualne, choć wyszły poprawki bezpieczeństwa.
W gorszym wariancie lista wskazuje na pliki, których już nie ma na serwerze,
i dostaję błąd 404.

Zainstalowane narzędzia:

| Pakiet | Do czego |
|---|---|
| `git` | system kontroli wersji |
| `curl` | pobiera dane z adresu URL |
| `wget` | to samo, inne podejście |
| `tree` | rysuje strukturę katalogów jako drzewo |
| `unzip` | rozpakowuje archiwa .zip |
| `gh` | GitHub CLI |

## 5. Łączenie i przekierowywanie komend

### Trzy standardowe strumienie

Każdy program w Linuksie ma trzy kanały:

| Kanał | Numer | Do czego |
|---|---|---|
| stdin | 0 | wejście, skąd program czyta dane |
| stdout | 1 | wyjście, gdzie wypisuje normalne wyniki |
| stderr | 2 | osobny kanał na komunikaty błędów |

Domyślnie stdout i stderr lecą na ekran, dlatego wyglądają tak samo.
Ale to są DWA różne kanały i można je rozdzielić.

### Operatory sekwencyjne

- `&&` — operator AND. Prawa komenda wykona się TYLKO jeśli lewa zakończyła się
  sukcesem (kod wyjścia 0).
- `;` — łączy komendy, ale druga wykona się niezależnie od wyniku pierwszej.
- `||` — operator OR. Prawa wykona się TYLKO jeśli lewa zawiodła.
  Przykład: `komenda || echo "nie udało się"`
- `\` na końcu linii — znak kontynuacji. Komenda ciągnie się do następnej linii.
  Po `\` nie może być spacji.

Dlaczego w checkliście `&&`, a nie `;`:
chcę, żeby łańcuch przerwał się w miejscu pierwszego błędu i od razu było widać,
które narzędzie nie działa. Przy `;` wykonałyby się wszystkie komendy i dostałbym
kaskadę błędów, w której trudniej znaleźć źródło.

### Potok `|`

Bierze stdout lewej komendy i podaje jako stdin prawej. Zamiast wypisać na ekran,
przekazuje dalej.

`git config --list | grep user`

Krok po kroku:
1. `git config --list` wypisuje na stdout wszystkie ustawienia Gita
2. `|` przechwytuje ten strumień, nie pozwala mu trafić na ekran
3. `grep user` dostaje go na stdin i przepuszcza tylko linie zawierające „user"
4. To, co zostało, ląduje na ekranie

KLUCZOWE: `grep` nie wie nic o Gicie ani o „userach" jako pojęciu. Dostaje strumień
tekstu i filtruje linie. Ta sama komenda działa na czymkolwiek:

```bash
ls -l | grep ".md"              # tylko pliki markdown
cat log.txt | grep "ERROR"      # tylko linie z błędem
history | grep "git"            # co ostatnio robiłem z Gitem
```

Potoki można łączyć w łańcuchy:

```bash
cat log.txt | grep "ERROR" | wc -l    # policz linie z błędem
```

To jest filozofia uniksowa: małe programy robiące jedną rzecz dobrze,
łączone w łańcuchy. `grep` filtruje, `wc` liczy, `sort` sortuje.
Żaden z nich nie musi wiedzieć o istnieniu pozostałych.

RÓŻNICA `&&` vs `|` (typowe pytanie testowe):
- `&&` przekazuje INFORMACJĘ O SUKCESIE. Steruje tym, CZY druga komenda się wykona.
- `|` przekazuje DANE. Druga komenda wykona się zawsze, dostaje tylko materiał do pracy.

### Przekierowania do plików

- `>` — zapisz stdout do pliku, NADPISUJĄC jego zawartość
- `>>` — dopisz stdout na końcu pliku
- `<` — czytaj stdin z pliku
- `2>` — przekieruj stderr (kanał 2)
- `2>&1` — przekieruj stderr tam, gdzie już idzie stdout (scal oba kanały)

```bash
ls -l > lista.txt              # zapisz listę do pliku
echo "nowa linia" >> lista.txt # dopisz na końcu
komenda > wynik.txt 2>&1       # zapisz wszystko, wyniki i błędy razem
komenda 2> bledy.txt           # tylko błędy do pliku, wyniki na ekran
```

UWAGA: `>` kasuje zawartość pliku bez ostrzeżenia. `ls > notatka.md` na istniejącej
notatce oznacza jej utratę.

## 6. Konfiguracja Gita

`git config` czyta i zapisuje ustawienia Gita.

Trzy poziomy, od najogólniejszego do najbardziej szczegółowego:

| Poziom | Flaga | Plik | Zasięg |
|---|---|---|---|
| systemowy | `--system` | `/etc/gitconfig` | wszyscy użytkownicy |
| użytkownika | `--global` | `~/.gitconfig` | ja, wszystkie projekty |
| repozytorium | `--local` | `.git/config` | tylko ten projekt |

Bardziej szczegółowy nadpisuje ogólniejszy: `--local` wygrywa z `--global`,
`--global` wygrywa z `--system`.

Ustawione:

```bash
git config --global user.name "Kacper Kowalski"
git config --global user.email "kowalskikacper1029@gmail.com"
git config --global init.defaultBranch main
```

Dlaczego email musi się zgadzać z GitHubem: email trafia do KAŻDEGO commita jako
podpis autora. GitHub po nim rozpoznaje, że commit jest mój, i przypisuje go do
profilu. Jeśli się nie zgadza, commity pojawiają się jako anonimowe, bez awatara
i bez wkładu w statystyki.

`init.defaultBranch main` ustawia nazwę pierwszej gałęzi w nowym repozytorium.
Historycznie było `master`, dziś standardem jest `main`.

### Jak zmienić ustawienie dla jednego projektu

Sytuacja: mam prywatny email w `--global`, ale w projekcie służbowym commity
muszą być podpisane firmowym.

Nie ruszam konfiguracji globalnej. Zamiast tego wchodzę do repozytorium
i ustawiam nadpisanie lokalne:

```bash
cd ~/projekty/projekt-sluzbowy
git config --local user.email "kacper.kowalski@firma.pl"
```

Zapisuje się to w `.git/config` TEGO repozytorium. Ponieważ `--local` ma wyższy
priorytet niż `--global`, w tym projekcie działa firmowy email, a we wszystkich
pozostałych dalej prywatny.

WAŻNE: `--local` działa tylko wewnątrz repozytorium. W katalogu bez `.git`
komenda zwróci błąd.

### Sprawdzanie, która wartość obowiązuje

```bash
git config user.email
```

Bez flagi Git pokazuje WYNIK ROZSTRZYGNIĘCIA hierarchii, czyli wartość faktycznie
obowiązującą w bieżącym katalogu. Wygodne, ale nie mówi, skąd pochodzi.

```bash
git config --show-origin user.email
```

Wypisuje ścieżkę pliku, z którego wartość została wzięta. To jest komenda
do diagnozowania „dlaczego mój commit ma zły email".

```bash
git config --local --list     # tylko ustawienia tego repozytorium
git config --global --list    # tylko moje ustawienia użytkownika
git config --list | grep user # filtr po słowie "user"
```

### Usuwanie ustawienia

```bash
git config --local --unset user.email
```

Po tym w projekcie znów zadziała wartość z `--global`.

## 7. Uwierzytelnienie GitHub

`gh` to oficjalny klient GitHuba dla terminala. Pozwala robić z CLI to, co
normalnie w przeglądarce: tworzyć repozytoria, otwierać Pull Requesty,
przeglądać issues.

`gh auth login` uruchamia kreator uwierzytelnienia. Wybrane opcje:
- **GitHub.com** — nie GitHub Enterprise (firmowa instalacja na własnych serwerach)
- **HTTPS** — protokół komunikacji. Alternatywa to SSH z parą kluczy.
- **Yes, authenticate Git** — kluczowe. Sprawia, że `gh` staje się magazynem
  poświadczeń dla Gita, więc `git push` przestaje pytać o hasło.
- **Login with a web browser** — kod z terminala wklejam na stronie GitHuba,
  która potwierdza tożsamość i odsyła token zapisywany lokalnie.

Sprawdzenie: `gh auth status` — konto, protokół, uprawnienia tokenu. Nic nie zmienia.

## 8. Instalacja Claude Code

`curl -fsSL https://claude.ai/install.sh | bash`

`curl` pobiera zawartość spod adresu URL, domyślnie wypisując ją na ekran.

Flagi sklejone w `-fsSL`:

| Flaga | Znaczenie |
|---|---|
| `-f` | fail — przy błędzie HTTP zwróć błąd zamiast wypisywać stronę błędu |
| `-s` | silent — bez paska postępu |
| `-S` | show-error — ale komunikaty błędów jednak pokazuj |
| `-L` | location — podążaj za przekierowaniami |

`| bash` — pobrany skrypt nie trafia na ekran, tylko przez potok do interpretera
bash, który go WYKONUJE. To ten sam mechanizm potoku co w sekcji 5:
stdout `curl` staje się stdin `bash`.

Czyli: pobierz skrypt z internetu i natychmiast uruchom.

RYZYKO: wykonuję kod, którego nie widziałem. Jeśli adres jest podstawiony albo
serwer przejęty, uruchamiam cudzy kod na swoim koncie. Tutaj bezpieczne, bo to
oficjalna domena Anthropic. Ale przy losowym blogu bezpieczniej:

```bash
curl -fsSL https://adres/install.sh -o install.sh   # -o zapisuje do pliku
less install.sh                                      # najpierw przeczytaj
bash install.sh                                      # dopiero potem uruchom
```

Instalacja w WSL używa instalatora linuksowego. Instalacje natywne aktualizują się
automatycznie w tle.

`claude` bez argumentów uruchamia interaktywną sesję agenta W BIEŻĄCYM KATALOGU.
Katalog ma znaczenie: agent widzi projekt, w którym go uruchomiłem.
`/exit` kończy sesję. Komendy z `/` to komendy slash Claude Code, nie shella.

## 9. Narzędzia diagnostyczne

`claude doctor` — sprawdza stan instalacji, poprawność plików ustawień, wypisuje
ostrzeżenia i sugerowane poprawki. Nie uruchamia sesji agenta.

Jest TYLKO DO ODCZYTU: niczego nie zmienia, nie naprawia, nie nadpisuje. Dlatego
można ją uruchamiać dowolnie często przy diagnozowaniu, bez ryzyka pogorszenia
sytuacji. Dla kontrastu `claude update` faktycznie zmienia stan systemu.

ZASADA OGÓLNA: przy każdym nowym narzędziu warto od razu znaleźć komendę, która
pokazuje stan, niczego nie zmieniając. Rodzina, którą już znam:
`git status`, `gh auth status`, `git config --list`, `claude doctor`.
To są komendy, od których zaczynam, gdy coś nie działa.

## 10. Typowe błędy

| Objaw | Przyczyna | Rozwiązanie |
|---|---|---|
| `claude: command not found` zaraz po instalacji | otwarta sesja terminala ma stary `PATH` sprzed instalacji | zamknij i otwórz terminal ponownie |
| `wsl --install` nie działa | wyłączona wirtualizacja w BIOS | włącz Intel VT-x / AMD-V |
| Hasło przy `sudo` „nie działa" | znaki nie są wyświetlane, brak gwiazdek | wpisuj na ślepo, potem Enter |
| Git prosi o hasło przy każdym `push` | brak skonfigurowanych poświadczeń | `gh auth login` z opcją uwierzytelnienia Gita |
| Wklejanie `Ctrl+V` nie działa w terminalu | terminal ma inne znaczenie tego skrótu | `Ctrl+Shift+V` albo prawy przycisk myszy |
| Plik nagle pusty po `>` | `>` nadpisuje bez ostrzeżenia | używać `>>` gdy chcę dopisać |
| Commit ma zły email | konfiguracja lokalna nadpisuje globalną | `git config --show-origin user.email` |

## 11. Pytania testowe

1. Czym różni się `apt update` od `apt upgrade`? Dlaczego kolejność ma znaczenie?
2. Kiedy użyć `&&`, a kiedy `;` do połączenia dwóch komend? Podaj przykład
   sytuacji, w której wybór ma realne konsekwencje.
3. Na czym polega ryzyko wzorca `curl ... | bash` i jak wykonać instalację
   bezpieczniej?
4. Czym różni się terminal od shella? Gdzie w tym podziale mieści się `bash`?
5. Które ustawienie wygra: `user.email` przez `--global` czy przez `--local`?
   Dlaczego taka hierarchia ma sens?
6. Czym różni się `komenda1 && komenda2` od `komenda1 | komenda2`?
   Co przekazuje każdy z tych operatorów?
7. Mam prywatny email w konfiguracji globalnej. Jak ustawić inny dla jednego
   projektu i jak sprawdzić, który faktycznie obowiązuje?
8. Co robi `>`, a co `>>`? Który z nich może spowodować utratę danych?
9. Czym są stdin, stdout i stderr? Dlaczego stderr jest osobnym kanałem?

## 12. Ściąga komend z modułu 0

Legenda: `[plik]` to miejsce, w które wstawiasz własną nazwę.

### Nawigacja

| Komenda | Co robi |
|---|---|
| `pwd` | pokazuje, w którym katalogu jestem (print working directory) |
| `cd [katalog]` | wchodzi do katalogu (change directory) |
| `cd ~` | wraca do katalogu domowego |
| `cd ..` | wychodzi poziom wyżej |
| `ls` | listuje zawartość katalogu |
| `ls -l` | listuje ze szczegółami: uprawnienia, rozmiar, data |
| `ls -la` | to samo, ale pokazuje też pliki ukryte (zaczynające się od kropki) |

`~` to skrót na katalog domowy. Shell zamienia go na pełną ścieżkę
przed uruchomieniem programu.

### Pliki i katalogi

| Komenda | Co robi |
|---|---|
| `mkdir [nazwa]` | tworzy katalog |
| `mkdir -p a/b/c` | tworzy całą ścieżkę, nie zgłasza błędu gdy istnieje |
| `cp [źródło] [cel]` | kopiuje plik |
| `mv [źródło] [cel]` | przenosi lub zmienia nazwę |
| `rm [plik]` | KASUJE plik. Bez kosza, bez potwierdzenia, bez odzysku |
| `touch [plik]` | tworzy pusty plik |

### Czytanie plików

| Komenda | Co robi | Wyjście |
|---|---|---|
| `cat [plik]` | wypisuje całą zawartość | kończy sam |
| `cat -n [plik]` | to samo z numerami linii | kończy sam |
| `less [plik]` | czytanie stronami, do długich plików | `q` |
| `head -20 [plik]` | pierwsze 20 linii | kończy sam |
| `tail -20 [plik]` | ostatnie 20 linii | kończy sam |
| `tail -f [plik]` | śledzi plik na żywo, dopisuje nowe linie | `Ctrl+C` |
| `wc -l [plik]` | liczy linie | kończy sam |
| `wc -w [plik]` | liczy słowa | kończy sam |

`tail -f` to główne narzędzie do obserwowania logów w trakcie działania testów.

### Wyszukiwanie

| Komenda | Co robi |
|---|---|
| `grep "wzorzec" [plik]` | wypisuje linie zawierające wzorzec |
| `grep -n "wzorzec" [plik]` | dodaje numery linii |
| `grep -i "wzorzec" [plik]` | ignoruje wielkość liter |
| `grep -A 3 "wzorzec" [plik]` | pokazuje 3 linie PO trafieniu (After) |
| `grep -B 1 "wzorzec" [plik]` | pokazuje 1 linię PRZED trafieniem (Before) |
| `grep -c "wzorzec" [plik]` | tylko liczy trafienia |
| `grep "^## " [plik]` | `^` oznacza początek linii |

### Operatory i przekierowania

| Zapis | Co robi |
|---|---|
| `a && b` | wykonaj `b` TYLKO jeśli `a` się powiodło |
| `a \|\| b` | wykonaj `b` TYLKO jeśli `a` zawiodło |
| `a ; b` | wykonaj `b` niezależnie od wyniku `a` |
| `a \| b` | przekaż WYJŚCIE `a` jako WEJŚCIE `b` |
| `a > plik` | zapisz wyjście do pliku, NADPISUJĄC |
| `a >> plik` | dopisz wyjście na końcu pliku |
| `a 2> plik` | zapisz do pliku tylko błędy (stderr) |
| `a > plik 2>&1` | zapisz do pliku wszystko, wyniki i błędy |
| `\` na końcu linii | komenda ciągnie się do następnej linii |

### Pakiety

| Komenda | Co robi |
|---|---|
| `sudo apt update` | odświeża listę dostępnych pakietów |
| `sudo apt upgrade -y` | instaluje nowsze wersje zainstalowanych pakietów |
| `sudo apt install -y [pakiet]` | instaluje pakiet |
| `sudo apt remove [pakiet]` | usuwa pakiet |

### Git — konfiguracja

| Komenda | Co robi |
|---|---|
| `git --version` | wersja Gita |
| `git config --global user.name "Imię"` | ustawia nazwę autora dla wszystkich repo |
| `git config --global user.email "mail"` | ustawia email autora |
| `git config --local user.email "mail"` | nadpisuje email TYLKO w tym repozytorium |
| `git config user.email` | pokazuje wartość faktycznie obowiązującą tutaj |
| `git config --show-origin user.email` | pokazuje, z którego pliku pochodzi wartość |
| `git config --list` | wypisuje wszystkie ustawienia |
| `git config --local --unset user.email` | usuwa ustawienie lokalne |

### GitHub CLI

| Komenda | Co robi |
|---|---|
| `gh --version` | wersja gh |
| `gh auth login` | uruchamia kreator logowania |
| `gh auth status` | pokazuje konto i uprawnienia tokenu, nic nie zmienia |

### Claude Code

| Komenda | Co robi |
|---|---|
| `claude --version` | wersja Claude Code |
| `claude` | uruchamia sesję agenta W BIEŻĄCYM KATALOGU |
| `claude doctor` | diagnostyka, tylko do odczytu |
| `claude update` | ręczna aktualizacja |
| `/exit` | wychodzi z sesji agenta (komenda slash, wewnątrz sesji) |

### Pobieranie

| Komenda | Co robi |
|---|---|
| `curl -fsSL [url]` | pobiera zawartość spod URL na stdout |
| `curl -fsSL [url] -o [plik]` | pobiera i zapisuje do pliku |
| `curl -fsSL [url] \| bash` | pobiera skrypt i NATYCHMIAST uruchamia (ryzykowne) |

### Edytory

| Komenda | Co robi | Wyjście |
|---|---|---|
| `nano [plik]` | prosty edytor terminalowy | `Ctrl+X` |
| `code [plik]` | otwiera VS Code na pliku w WSL | zamknięcie okna |

Skróty nano: `Ctrl+O` zapisz, `Ctrl+X` wyjdź, `Ctrl+W` szukaj,
`Ctrl+K` wytnij linię, `Ctrl+U` wklej.
VS Code: `Ctrl+Shift+V` podgląd Markdown.

### Diagnostyka i pomoc

| Komenda | Co robi | Wyjście |
|---|---|---|
| `[program] --version` | wersja programu |
| `[program] --help` | skrócona pomoc |
| `man [program]` | pełna dokumentacja | `q` |
| `which [program]` | pokazuje, gdzie leży plik wykonywalny |
| `uname -a` | informacje o jądrze systemu |
| `history` | lista ostatnio wpisanych komend |

### Skróty klawiszowe terminala

| Skrót | Działanie |
|---|---|
| `Tab` | autouzupełnianie nazw plików i komend |
| `↑` `↓` | przewijanie historii komend |
| `Ctrl+R` | wyszukiwanie w historii |
| `Ctrl+C` | PRZERYWA działający program |
| `Ctrl+D` | kończy sesję shella (jak `exit`) |
| `Ctrl+L` | czyści ekran (jak `clear`) |
| `Ctrl+Shift+V` | WKLEJANIE (nie `Ctrl+V`) |
| `Ctrl+Shift+C` | kopiowanie |

`Tab` to najważniejszy z nich. Zaczynasz pisać nazwę, wciskasz Tab,
shell dokańcza. Chroni przed literówkami i pokazuje, czy plik istnieje.

### Jak wyjść z czegokolwiek

| Gdzie jestem | Wyjście |
|---|---|
| `less`, `man` | `q` |
| `nano` | `Ctrl+X` |
| sesja `claude` | `/exit` |
| program się nie kończy | `Ctrl+C` |
| shell / terminal | `exit` albo `Ctrl+D` |
| `vim` (trafiłem przypadkiem) | `Esc`, potem `:q!` i Enter |

### Komendy, z którymi trzeba uważać

| Komenda | Ryzyko |
|---|---|
| `rm [plik]` | kasuje bez kosza i bez potwierdzenia |
| `rm -rf [katalog]` | kasuje katalog z całą zawartością, rekurencyjnie |
| `> [plik]` | nadpisuje zawartość istniejącego pliku |
| `curl ... \| bash` | uruchamia kod, którego nie widziałem |
| `sudo [cokolwiek]` | działa z uprawnieniami administratora |

Nawyk: przed operacją na plikach sprawdź `pwd`. Większość wypadków
w terminalu bierze się z tego, że ktoś był w innym katalogu, niż myślał.