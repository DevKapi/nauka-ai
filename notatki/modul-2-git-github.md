# Moduł 2 — Git i GitHub

> Notatka referencyjna. Napisana przez Claude na podstawie sesji praktycznych.
>
> **Zasada z modułu 1 obowiązuje nadal:** nie ufaj tej notatce na słowo.
> Każdą komendę sprawdź empirycznie w terminalu. Notatki bywają pisane
> z innego katalogu roboczego niż twój i wtedy przykłady nie działają.

---

## 1. Po co w ogóle Git

Git zapisuje **migawki stanu twoich plików w czasie**. Taka migawka to **commit**.

Trzy rzeczy, które ci to daje:

1. **Historia** — możesz cofnąć się do dowolnego wcześniejszego stanu projektu.
2. **Widoczność zmian** — dokładnie widzisz, które linie się zmieniły i kiedy.
3. **Bezpieczne eksperymenty** — możesz zepsuć wszystko na boku, a główna wersja pozostanie nietknięta.

**Dlaczego to kluczowe przy pracy z agentem AI:** kiedy agent modyfikuje pliki
w twoim projekcie, `git diff` jest jedynym narzędziem, które pokaże ci, co
naprawdę zrobił. A `git restore` albo usunięcie brancha cofa wszystko jednym
poleceniem. Bez Gita praca z agentem to praca bez siatki bezpieczeństwa.

Git **nie zapisuje niczego automatycznie**. Ty decydujesz, co i kiedy trafia
do historii. Dlatego istnieją trzy osobne obszary.

---

## 2. Trzy obszary + czwarty (zdalny)

To najważniejszy model mentalny w całym Gicie.

```
  Katalog roboczy          twoje pliki na dysku, tu edytujesz
         |
         |  git add
         v
  Poczekalnia (staging)    lista tego, co wejdzie do następnego commita
         |
         |  git commit
         v
  Repozytorium lokalne     folder .git, cała historia, działa offline
         |
         |  git push
         v
  Repozytorium zdalne      GitHub, kopia dla ciebie i zespołu
```

W drugą stronę: `git clone` (pierwsze pobranie) i `git pull` (kolejne).

### Po co poczekalnia

Analogia z pakowaniem paczki:

- **Katalog roboczy** — biurko z porozrzucanymi rzeczami
- **Poczekalnia** — karton, do którego wkładasz tylko wybrane przedmioty
- **Commit** — zaklejenie kartonu i odesłanie go do magazynu

Sens: zmieniłeś 5 plików, ale tylko 3 dotyczą jednej logicznej zmiany.
Chcesz zrobić dwa osobne, czytelne commity — nie jeden bałagan.

---

## 3. Komendy podstawowe

### `git init`

Tworzy folder `.git` w **bieżącym** katalogu. Od tej chwili Git obserwuje ten katalog.

```bash
mkdir moj-projekt
cd moj-projekt
git init
ls -la          # zobaczysz folder .git
```

**Uwaga:** działa tam, gdzie aktualnie jesteś. Zawsze sprawdź `pwd` przed `git init`.

---

### `git status`

Najważniejsza komenda Gita. Wpisuj ją po każdej innej komendzie.

Pokazuje: branch, zawartość poczekalni, zmiany poza poczekalnią, pliki nieznane Gitowi.

**Cztery możliwe stany pliku:**

| Stan pliku | Gdzie widoczny w `git status` |
|---|---|
| Git go nie zna | `Untracked files` |
| Zna, zmieniony, nie w poczekalni | `Changes not staged for commit` |
| Zna, zmiany w poczekalni | `Changes to be committed` |
| Zna, brak zmian | nigdzie — cisza |

Ostatni wiersz jest ważny: `git status` pokazuje **tylko to, co odbiega od
ostatniego commita**. Pliki zgodne z historią są niewidoczne.

**Czytaj podpowiedzi w nawiasach.** Git dosłownie mówi, jaką komendę uruchomić:

```
(use "git add <file>..." to include in what will be committed)
(use "git restore --staged <file>..." to unstage)
```

To nie ozdoba — to rozwiązanie połowy problemów bez szukania w internecie.

---

### `git add`

Wkłada plik do poczekalni.

```bash
git add notatki.txt      # jeden plik
git add .                # wszystko z bieżącego katalogu w dół
git add notatki/         # cały podkatalog
```

Kropka w `git add .` to ścieżka względna — to samo pojęcie co w module 1.

---

### `git commit`

Tworzy migawkę z tego, co jest w poczekalni.

```bash
git commit -m "Dodaj notatke z modulu 2"
```

`-m` to wiadomość (*message*).

**Jak czytać output — wersja udana:**

```
[main (root-commit) a201caa] Pierwszy commit w git-lab
 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 notatki.txt
```

| Fragment | Znaczenie |
|---|---|
| `[main` | branch, na którym powstał commit |
| `(root-commit)` | pierwszy commit w historii, pojawia się raz w życiu repo |
| `a201caa]` | skrócony hash — unikalny identyfikator migawki |
| `1 file changed, 0 insertions` | **licznik kontrolny** — zero wstawionych linii to sygnał ostrzegawczy |
| `create mode 100644` | nowy plik; `100644` = zwykły plik, `100755` = wykonywalny |

**Wersja nieudana:**

```
On branch main
Untracked files:
...
nothing added to commit but untracked files present
```

**Rozpoznanie: brak nawiasu kwadratowego z hashem = commit się nie odbył.**
Git nie krzyczy „BŁĄD" — pokazuje status i zostawia cię z tym. Musisz czytać.

#### Dobre wiadomości commitów

Wiadomość odpowiada na pytanie **„co ta zmiana robi w projekcie"**, a nie
„jakiego pliku dotyczy" (to widać w diffie).

```
ŹLE:  test-brancha.md
ŹLE:  kolejny commit
ŹLE:  poprawki
DOBRZE: Dodaj plik testowy do sprawdzenia workflow PR
DOBRZE: Usun plik o blednej nazwie .gitingore
```

#### PUŁAPKA: nigdy nie podawaj ścieżki po `git commit`

```bash
git commit notatki.txt -m "opis"     # ŹLE
git commit -m "opis"                 # DOBRZE
```

`git commit <ścieżka>` to **partial commit** — Git commituje wyłącznie ten plik
i **ignoruje całą resztę poczekalni**.

Realne konsekwencje z sesji:
- `git mv` wrzucił do poczekalni dwie operacje (usunięcie starej nazwy + dodanie nowej).
  `git commit .gitignore -m "..."` zapisał tylko dodanie. Usunięcie wisiało w poczekalni
  i trzeba było commitować je osobno. Historia nie odzwierciedlała rzeczywistości.
- Przy kończeniu merge Git odmawia twardo: `fatal: cannot do a partial commit during a merge`.

**Zasada: to, co ma wejść do commita, wybierasz przez `git add`. `git commit` tylko zamyka paczkę.**

#### Bez `-m` otwiera się edytor

Jeśli napiszesz `git commit` bez `-m`, otworzy się edytor tekstu.

- **nano** (na dole widać `^O Write Out`, `^X Exit`): `Ctrl+O`, Enter, `Ctrl+X`
- **vim** (brak podpowiedzi na dole): `Esc`, potem `:wq`, Enter
- **wyjście bez zapisu w vim:** `Esc`, potem `:q!`, Enter

Pusta wiadomość anuluje commit.

---

### `git log`

Historia commitów.

```bash
git log                      # pełna
git log --oneline            # jedna linia na commit
git log --oneline --all      # wszystkie branche, nie tylko bieżący
git log --oneline --graph --all   # + rysunek struktury gałęzi
```

Wyjście z przeglądarki `less`, jeśli log jest długi: klawisz `q`.

**Pełny output:**

```
commit a201caad40e4599c3edd37b651090b2a6372ae5a (HEAD -> main)
Author: Kacper Kowalski <kowalskikacper1029@gmail.com>
Date:   Sun Aug 30 21:35:09 2026 +0200

    Pierwszy commit w git-lab
```

- Hash ma 40 znaków, ale w praktyce wystarczy pierwsze 7
- `(HEAD -> main)` — HEAD wskazuje na branch `main`, `main` wskazuje na ten commit
- `Author` pochodzi z konfiguracji Gita ustawionej w module 0

**Uwaga na flagi:** `-all` to błąd, `--all` to poprawna forma.
Skrót = jedna kreska + jedna litera. Pełna nazwa = dwie kreski + słowo.

---

### `git diff`

Pokazuje różnice. Dwie odmiany, których nie wolno mylić:

```bash
git diff              # katalog roboczy  <->  poczekalnia
git diff --staged     # poczekalnia      <->  ostatni commit
git diff -w           # ignoruje różnice w białych znakach
```

**Kluczowa obserwacja:** zmiana jest w danym momencie **w jednym miejscu naraz**.

- Przed `git add` — zmiana siedzi w katalogu roboczym.
  `git diff` ją pokazuje, `git diff --staged` milczy.
- Po `git add` — zmiana przeskoczyła do poczekalni.
  `git diff` milknie, `git diff --staged` ją pokazuje.

#### Jak czytać diff

```
diff --git a/notatki.txt b/notatki.txt
index 819f54d..799cc9c 100644
--- a/notatki.txt
+++ b/notatki.txt
@@ -1 +1,2 @@
 pierwsza linia
+druga linia
```

| Element | Znaczenie |
|---|---|
| `a/plik` | wersja **stara** |
| `b/plik` | wersja **nowa** |
| `@@ -1 +1,2 @@` | stara: od linii 1, długość 1. Nowa: od linii 1, długość 2 |
| linia z `-` | usunięta |
| linia z `+` | dodana |
| linia ze **spacją** na początku | kontekst — nie zmieniła się |

**Git nie ma pojęcia „linia zmodyfikowana".** Modyfikacja to zawsze usunięcie
starej i dodanie nowej — zobaczysz `-` i `+` obok siebie.

Praktyczna konsekwencja: jeśli agent AI przepisze plik z tą samą treścią, ale
innym formatowaniem, dostaniesz diff ze 100 usuniętymi i 100 dodanymi liniami.
Wtedy przydaje się `git diff -w`.

**To jest format, w którym przeglądasz pracę agenta AI i robisz code review.**

---

### `git restore`

```bash
git restore notatki.txt            # cofa zmiany w katalogu roboczym
git restore --staged notatki.txt   # wyjmuje plik z poczekalni (nie kasuje zmian)
```

Skąd Git bierze treść? **Z ostatniego commita, czyli z folderu `.git`.**
Kasując coś na dysku, nie tykasz historii.

**NIEBEZPIECZNE:** `git restore` kasuje bezpowrotnie wszystko, czego nie
zdążyłeś zacommitować. Nie ma cofnięcia.

---

### `.gitignore`

Plik tekstowy z listą wzorców. Git ignoruje pasujące pliki i nie proponuje ich do commita.

```bash
echo 'haslo.txt' > .gitignore
cat .gitignore          # zawsze weryfikuj
git add .gitignore
git commit -m "Dodaj .gitignore z regula dla haslo.txt"
```

Typowa zawartość:

```
*.log
node_modules/
.env
haslo.txt
```

**Sprawdzenie, czy działa:** plik znika z `git status`. Git nadal widzi go na
dysku, ale świadomie pomija.

**Dwie rzeczy do zapamiętania:**
- `.gitignore` **zawsze commitujesz** — to plik zespołowy, wszyscy mają te same reguły
- Literówka w nazwie (`.gitingore`) = mechanizm w ogóle się nie uruchamia,
  a Git tego nie zgłosi. Będzie traktował plik jak zwykły plik tekstowy.

---

### `git mv`

Zmienia nazwę pliku **i od razu wpisuje tę zmianę do poczekalni**.

```bash
git mv stara-nazwa.md nowa-nazwa.md
git status              # zobaczysz: deleted + new file, albo renamed
```

W poczekalni lądują **dwie operacje**: usunięcie starej nazwy i dodanie nowej.
Dlatego trzeba je zacommitować razem (`git commit -m`, bez ścieżki).

---

## 4. Branche

### Czym branch NIE jest

Branch nie jest pudełkiem, do którego wpadają commity. To najczęstszy błąd myślowy.

### Czym branch jest

**Commity leżą we wspólnej puli. Branch to karteczka z nazwą, przyklejona do
jednego commita.**

Technicznie: plik tekstowy w `.git`, w którym zapisany jest jeden hash.
Dlatego tworzenie brancha jest natychmiastowe — Git nie kopiuje plików.

Analogia: sznur z koralikami. Koraliki to commity, branch to spinacz zaczepiony
na jednym koraliku. Możesz mieć dwa spinacze na tym samym koraliku.

### Jak commity są ze sobą połączone

Każdy commit zapisuje **hash swojego rodzica**. To jedyne połączenie, jakie istnieje.

Dlatego historię czyta się od końca do początku: `git log` bierze commit
wskazywany przez HEAD, pyta „kto był przede mną", przechodzi tam, i tak
aż do pierwszego commita.

**Commit nie wie, na jakim jest branchu.** Taka informacja nie jest nigdzie zapisana.

### HEAD

Wskaźnik mówiący, **na którym branchu aktualnie jesteś**.

```
d2e5d82 (HEAD -> main) kolejny commit
```

Czytaj: HEAD → `main` → commit `d2e5d82`.

`git switch` przesuwa HEAD **i fizycznie podmienia pliki w katalogu roboczym**,
żeby odpowiadały nowemu branchowi. Pliki znikają i pojawiają się — to normalne.
Nie giną, leżą w `.git` przypisane do commitów na drugiej gałęzi.

### Co robi każda komenda ze wskaźnikami

| Komenda | Co się dzieje |
|---|---|
| `git commit` | powstaje commit; **branch, na którym stoisz, przesuwa się** na niego |
| `git branch nazwa` | nowa karteczka w miejscu HEAD; **NIE przełącza** |
| `git switch nazwa` | HEAD przeskakuje + pliki na dysku się podmieniają |
| `git switch -c nazwa` | tworzy karteczkę i od razu przełącza |
| `git merge nazwa` | wciąga commity z tamtej karteczki tutaj |
| `git branch -d nazwa` | zdejmuje karteczkę; **commity zostają** |

**PUŁAPKA:** `git branch test` tworzy branch, ale zostawia cię tam, gdzie byłeś.
Jeśli potem zrobisz commit, przesunie się **stary** branch, nie nowy.
Dlatego prawie zawsze używa się `git switch -c`.

### Komendy

```bash
git branch                  # lista; gwiazdka przy bieżącym
git switch -c nowa-galaz    # utwórz i przełącz  (najczęstsza forma)
git switch main             # przełącz na istniejący
git merge nazwa             # wciągnij zmiany TUTAJ
git branch -d nazwa         # usuń bezpiecznie
git branch -D nazwa         # usuń siłą (niebezpieczne)
```

> Stare poradniki używają `git checkout`. Robi to samo i jeszcze pięć innych
> rzeczy, przez co jest mylące. Git 2.23 wprowadził `git switch`, żeby to
> rozdzielić. Używaj `switch`.

### Kierunek merge

**Najpierw przełączasz się tam, gdzie zmiany mają trafić, potem mergujesz.**

```bash
git switch main             # stoję tam, gdzie chcę mieć zmiany
git merge wersja-a          # wciągam zmiany stamtąd
```

---

## 5. Dwa rodzaje merge

Git decyduje sam, patrząc na jedną rzecz: **czy istnieje prosta ścieżka od
miejsca, gdzie stoję, do commita, który wciągam.**

### Fast-forward

Warunek: **na `main` nie pojawił się żaden nowy commit** od czasu odgałęzienia.

```
A --- B --- C --- D --- E
            ^           ^
          main        testy       →  main przesuwa się na E
```

Git nie ma czego godzić — tylko przesuwa karteczkę do przodu, jak taśmę.

```
Updating d2e5d82..ced8d21
Fast-forward
 notatki.txt | 1 +
```

Rozpoznanie: słowo `Fast-forward`. **Nie powstaje nowy commit.**

### Merge commit

Warunek: obie gałęzie mają nowe commity — historia się rozeszła.

```
A --- B --- C --- F --------- M      M ma DWÓCH rodziców: F i E
             \               /
              D --- E ------/
```

Git tworzy **jedyny rodzaj commita z dwoma rodzicami**. Otworzy edytor
z gotową wiadomością `Merge branch 'nazwa'`.

**Rozpoznanie merge commita w grafie:**

```
*   e36a616 (HEAD -> main) Merge branch 'wersja-a'
|\                                    <-- DWIE linie schodzą się w jeden punkt
| * 69befa8 (wersja-a) tekst z wersji A
* | 60461a2 tekst z main
|/                                    <-- tu historia się rozeszła
* ced8d21 wspólny przodek
```

Rozpoznajesz go po **dwóch rodzicach** (`|\`), a **nie** po `(HEAD -> main)` —
to widać przy każdym najnowszym commicie.

Drugi sygnał: brak `1 file changed` w outpucie. Merge commit sam z siebie nie
wnosi treści, tylko łączy.

---

## 6. Konflikty

### Kiedy powstają

**Ta sama linia tego samego pliku została zmieniona inaczej na obu branchach.**

Jeśli zmiany są w różnych miejscach pliku, Git łączy je automatycznie bez pytania.
Zmieniłeś linię 10, ktoś inny linię 50 — Git bierze obie.

### Konflikt to nie błąd

To **pytanie**: „mam dwie wersje tej linii, nie zgadnę której chcesz — wybierz".

### Jak wygląda

```
$ git merge wersja-a
Auto-merging notatki.txt
CONFLICT (content): Merge conflict in notatki.txt
Automatic merge failed; fix conflicts and then commit the result.
```

`git status` pokaże nową sekcję:

```
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
        both modified:   notatki.txt
```

`both modified` = jeden plik z dwiema konkurencyjnymi wersjami treści.

W pliku Git wstawia znaczniki:

```
<<<<<<< HEAD
tekst z main
=======
tekst z wersji A
>>>>>>> wersja-a
```

| Znacznik | Rola |
|---|---|
| `<<<<<<< HEAD` | początek bloku; nazwa mówi, skąd pochodzi wersja poniżej (twój bieżący branch) |
| `=======` | **separator** między wersjami — czysto techniczny, nie oznacza błędu |
| `>>>>>>> wersja-a` | koniec bloku; nazwa brancha, z którego pochodzi wersja powyżej |

### Jak rozwiązać

1. Otwórz plik i zredaguj go tak, jak ma wyglądać **docelowo**
2. **Usuń wszystkie trzy linie ze znacznikami**
3. `git add plik`
4. `git commit` — **bez `-m` i bez ścieżki**

```bash
# przez echo
echo "tekst z main" > notatki.txt
echo "tekst z wersji A" >> notatki.txt
cat notatki.txt          # weryfikacja: zero znaczników

git add notatki.txt
git status               # "All conflicts fixed but you are still merging"
git commit               # otworzy edytor z gotową wiadomością
```

**Najczęstszy błąd początkujących:** zostawienie `=======` w pliku.
Kod przestaje działać, a przyczyna jest niewidoczna, dopóki nie spojrzysz uważnie.

### Ucieczka awaryjna

```bash
git merge --abort        # anuluje merge, wraca do stanu sprzed
```

---

## 7. Usuwanie brancha

`git branch -d` sprawdza **jedną rzecz**: czy commity z tego brancha są
osiągalne z innego miejsca w historii.

- **Po mergu:** commity są przodkami merge commita, na który wskazuje `main`.
  Nic nie ginie. `-d` przechodzi.
- **Bez merga:** commity byłyby nieosiągalne z żadnej nazwy. `-d` odmawia:

```
error: the branch 'eksperyment' is not fully merged
```

`-D` (duże D) omija ten bezpiecznik. Commity zostają w `.git`, ale nikt na nie
nie wskazuje — to *dangling commit*. Po ~30 dniach Git kasuje je na dobre.

**Zasada: jeśli `-d` odmawia, zatrzymaj się i sprawdź, zamiast odruchowo
dopisywać wielką literę.**

Awaryjne odzyskiwanie: `git reflog` przechowuje historię ruchów HEAD.
Warto o tym wiedzieć, nie warto na tym polegać.

---

## 8. GitHub i praca zdalna

### Czym jest GitHub

**Repozytorium na GitHubie to zwykłe repo Gita.** Te same commity, te same branche.
Różnica: leży na cudzym serwerze i ma interfejs w przeglądarce.

GitHub nie jest częścią Gita — to firma, która hostuje repozytoria i dokłada
narzędzia do współpracy (PR, review, issues).

### Remote

**Remote to nazwany adres innego repozytorium.** Zapisany URL, nic więcej.

Domyślna nazwa `origin` to konwencja, nie słowo kluczowe.

```bash
git remote -v
```

```
origin  https://github.com/DevKapi/nauka-ai.git (fetch)
origin  https://github.com/DevKapi/nauka-ai.git (push)
```

Dwa wpisy: skąd pobierasz i dokąd wysyłasz. Zwykle ten sam adres.

### Trzy rzeczy o podobnych nazwach

| Nazwa | Co to jest |
|---|---|
| `main` | twój lokalny branch — na nim pracujesz |
| `origin/main` | **twoje zapamiętane wyobrażenie** o tym, gdzie stoi `main` na GitHubie |
| `main` na serwerze | prawdziwy stan na GitHubie |

Środkowy wiersz myli wszystkich. `origin/main` to **migawka** z ostatniej rozmowy
z serwerem. Git nie ma stałego połączenia z GitHubem.

**Konsekwencja praktyczna:**

```
Your branch is up to date with 'origin/main'.
```

To znaczy „zgodny z tym, co ostatnio widziałem", a **nie** „zgodny z serwerem".
Ten komunikat pojawia się nawet wtedy, gdy na GitHubie są już nowe commity.

### Komendy

```bash
git clone <url>       # pobiera całe repo + ustawia origin. Raz na projekt.
git fetch             # pyta serwer o nowości, aktualizuje origin/main
                      # NIE tyka twoich plików ani lokalnego main. Bezpieczne.
git pull              # fetch + merge w jednym. Może wywołać konflikt.
git push              # wysyła twoje commity na serwer
```

### Pierwszy push nowego brancha

```bash
$ git push
fatal: The current branch notatki-modul2 has no upstream branch.
To push the current branch and set the remote as upstream, use

    git push --set-upstream origin notatki-modul2
```

Git nie wie, dokąd wysłać nowy branch, bo jeszcze nie ma powiązania.
**Podaje ci gotową komendę — skopiuj ją.**

```bash
git push --set-upstream origin notatki-modul2
# skrót: git push -u origin notatki-modul2
```

`-u` (*upstream*) zapamiętuje powiązanie. Kolejne razy wystarczy samo `git push`.

---

## 9. Pull Request i code review

**PR to nie jest komenda Gita** — to funkcja GitHuba.

Pull Request to prośba: „mam gotowe zmiany na branchu X, proszę o wciągnięcie
ich do `main`". Otwiera miejsce, gdzie zespół widzi diff, komentuje konkretne
linie i zatwierdza albo prosi o poprawki.

**Code review to bezpośrednio teren QA.** Przeglądanie cudzego diffa przed
wpuszczeniem go do głównej gałęzi to ta sama umiejętność co czytanie `git diff`.

Merge PR-a robisz przyciskiem na stronie. Efekt identyczny jak `git merge`,
tylko wykonany na serwerze. GitHub tworzy commit:

```
Merge pull request #1 from DevKapi/notatki-modul2
```

Numer `#1` to identyfikator PR-a w obrębie repo — używa go cały zespół.

### Pełny workflow

```bash
git switch -c moja-zmiana          # 1. osobny branch
# ... edytujesz pliki ...
cat plik                           # 2. weryfikacja treści
git add .
git status                         # 3. sprawdź, co jest w poczekalni
git commit -m "Opisowa wiadomosc"
git push -u origin moja-zmiana     # 4. branch trafia na GitHub

# 5. na GitHubie: otwierasz PR
# 6. review: ktoś komentuje, ty poprawiasz i pushujesz ponownie
# 7. merge przyciskiem

git switch main
git pull                           # 8. ściągasz zmergowany stan
git branch -d moja-zmiana          # 9. sprzątasz lokalny branch
```

**Krok 8 jest obowiązkowy.** Po merge przez przeglądarkę twój lokalny Git nadal
ma starą historię. Dopiero `git pull` ściąga merge commit:

```
   82d749f..ae942fb  main -> origin/main
Updating 82d749f..ae942fb
Fast-forward
```

---

## 10. Zastosowanie w pracy z agentem AI

To jest powód, dla którego ćwiczysz Gita.

```bash
git switch -c ai-refactor     # osobna gałąź na pracę agenta
# uruchamiasz Claude Code
git diff                      # oglądasz, co naprawdę zrobił
```

Dwie ścieżki:

**Praca dobra:**
```bash
git add .
git commit -m "Refaktor testow przez agenta"
git switch main
git merge ai-refactor
```

**Praca zła:**
```bash
git switch main
git branch -D ai-refactor     # wszystko znika, main nietknięty
```

Ta druga ścieżka to powód, dla którego branche istnieją: **dają ci prawo do
nieudanego eksperymentu.**

Agent powie „gotowe, dodałem testy". Twoim zadaniem jest sprawdzić
`git diff --staged`, a nie uwierzyć na słowo.

---

## 11. Typowe błędy — z prawdziwej sesji

### `touch plik > "tekst"`

**Najkosztowniejszy błąd tego modułu.** Rozkład na części:

| Fragment | Co robi bash |
|---|---|
| `touch notatki.txt` | tworzy **pusty** plik |
| `>` | „to, co komenda wypisze, zapisz do pliku" |
| `"testowa linijka"` | **nazwa pliku docelowego** — cudzysłów sprawia, że spacje są częścią nazwy |

`touch` nic nie wypisuje. Efekt: dwa puste pliki, w tym jeden o nazwie
`testowa linijka`. Tekst stał się **nazwą** pliku, a nie jego treścią.

**Reguła:**

```
KOMENDA_KTÓRA_WYPISUJE_TEKST  >  NAZWA_PLIKU
              ↑ lewa               ↑ prawa
```

```bash
echo "treść" > plik.txt      # DOBRZE — nadpisuje
echo "treść" >> plik.txt     # DOBRZE — dopisuje na końcu
touch plik.txt               # DOBRZE — tworzy pusty plik
touch plik.txt > "treść"     # ŹLE — tworzy dwa puste pliki
```

`touch` **nigdy** nie łączy się z przekierowaniem.

Objawy w Gicie: `0 insertions(+)` przy commicie, pusty `git diff`,
`nothing added to commit` zamiast potwierdzenia commita.

### Nieczytanie potwierdzeń

Git wypisał status zamiast `[main a201caa]` — commit się nie odbył, ale praca
poszła dalej z założeniem sukcesu. **To nie literówka, tylko brak nawyku weryfikacji.**

### Literówka w nazwie pliku konfiguracyjnego

`.gitingore` zamiast `.gitignore`. Git nie zgłasza — po prostu traktuje to jak
zwykły plik i mechanizm ignorowania nigdy się nie uruchamia.

### Ścieżka po `git commit`

Opisane w sekcji 3. Trzy razy uszło płazem, czwarty raz zablokowało merge.

### `-all` zamiast `--all`

```
error: switch `l' expects a numerical value
```

Jedna kreska + jedna litera = skrót. Dwie kreski + słowo = pełna nazwa.

---

## 12. Trzy odruchy kontrolne

| Po czym | Sprawdź | Czego szukasz |
|---|---|---|
| utworzeniu pliku z treścią | `cat plik` | czy treść tam jest |
| `git commit` | pierwsza linia outputu | `[branch hash]` i `insertions` > 0 |
| `git add` | `git status` | plik w sekcji `Changes to be committed` |

Dodatkowo przy pustym pliku: `wc -l plik` (liczba linii) albo `ls -la`
(rozmiar `0` bajtów = plik pusty).

---

## 13. Ściąga — wszystkie komendy modułu

```bash
# Podstawy
git init                          # utwórz repozytorium w bieżącym katalogu
git status                        # stan poczekalni i katalogu roboczego
git add <plik>                    # wrzuć do poczekalni
git add .                         # wrzuć wszystko
git commit -m "opis"              # zapisz migawkę
git log --oneline                 # historia
git diff                          # roboczy <-> poczekalnia
git diff --staged                 # poczekalnia <-> ostatni commit
git restore <plik>                # cofnij zmiany (NIEBEZPIECZNE)
git restore --staged <plik>       # wyjmij z poczekalni
git mv <stara> <nowa>             # zmień nazwę + wrzuć do poczekalni

# Branche
git branch                        # lista
git switch -c <nazwa>             # utwórz i przełącz
git switch <nazwa>                # przełącz
git merge <nazwa>                 # wciągnij zmiany TUTAJ
git merge --abort                 # anuluj merge
git branch -d <nazwa>             # usuń bezpiecznie
git branch -D <nazwa>             # usuń siłą (NIEBEZPIECZNE)
git log --oneline --graph --all   # graf wszystkich gałęzi

# Zdalne
git clone <url>                   # pobierz repo
git remote -v                     # pokaż remote'y
git fetch                         # sprawdź serwer (bezpieczne)
git pull                          # fetch + merge
git push                          # wyślij commity
git push -u origin <branch>       # pierwszy push nowego brancha
```

---

## 14. Pytania, o które można zapytać na teście

1. Wymień trzy obszary Gita i powiedz, co robi każda komenda przenosząca zmiany między nimi.
2. Po co istnieje poczekalnia? Dlaczego nie wystarczy `commit` bez `add`?
3. Jaka jest różnica między `git diff` a `git diff --staged`?
4. Po czym poznasz, patrząc na output, że commit **nie** został utworzony?
5. Czym różni się `Untracked files` od `Changes not staged for commit`?
6. Czym technicznie jest branch?
7. Stoisz na `main`, robisz `git branch test`, potem `git commit`. Który branch się przesunął?
8. Kiedy merge daje fast-forward, a kiedy tworzy merge commit? Od czego to zależy?
9. Po czym rozpoznajesz merge commit w `git log --graph`?
10. Kiedy powstaje konflikt? Co oznacza `=======`?
11. Jak rozwiązać konflikt krok po kroku?
12. Kasujesz branch po udanym mergu. Czy tracisz commity? Dlaczego?
13. Dlaczego `git branch -d` czasem odmawia, a `-D` nie?
14. Czym jest `origin/main` i dlaczego różni się od `main` na serwerze?
15. Dlaczego `git status` mówi „up to date", gdy na GitHubie są nowe commity?
16. Czym różni się `git fetch` od `git pull`?
17. Czym jest Pull Request? Czy to komenda Gita?
18. Opisz pełny workflow: zmiana → commit → push → PR → review → merge.
19. Dlaczego po merge PR-a na GitHubie trzeba zrobić `git pull` lokalnie?
20. Jak Git wykorzystasz przy pracy z agentem AI? Podaj konkretny scenariusz.
