# Moduł 3 — Claude Code

Data: 2026-09-01
Wersja narzędzia użyta do weryfikacji: Claude Code 2.1.252
Środowisko: Windows + WSL 2 (Ubuntu)

Cel modułu: praca z agentem AI z poziomu terminala — uruchamianie, uprawnienia,
kontekst i sesje, komendy slash, konfiguracja projektu przez `CLAUDE.md`.

---

## 1. Czym jest Claude Code

Claude Code to agent AI działający w terminalu. Dostaje zadanie napisane po ludzku,
a następnie **sam** czyta pliki, uruchamia komendy, edytuje kod i sprawdza wynik —
w pętli, aż osiągnie cel.

To nie jest ani czat w przeglądarce, ani podpowiadacz kodu w edytorze.

### Chat kontra agent

| | Chat w przeglądarce | Claude Code (CLI) |
|---|---|---|
| Widzi moje pliki | nie (chyba że wkleję) | tak, czyta je sam |
| Może zmienić plik | nie | tak |
| Może uruchomić komendę | nie | tak (`npm test`, `git status`…) |
| Widzi wynik swojej pracy | nie | tak — czyta output i poprawia się |
| Gdzie działa | strona www | mój terminal, w moim katalogu |

### Pętla agenta

```
1. Czyta moje polecenie
2. Zastanawia się, czego mu brakuje
3. Używa NARZĘDZIA (czyta plik, uruchamia komendę)
4. Czyta WYNIK tego narzędzia
5. Jeśli to nie koniec → wraca do punktu 2
6. Odpowiada
```

Przykład: „napraw failujący test". Agent uruchamia testy, czyta błąd, otwiera plik
testu, otwiera plik z kodem, wprowadza poprawkę, uruchamia testy ponownie, widzi
zielone — i dopiero wtedy odpowiada. Sześć kroków, których nie musiałem rozpisywać.

### Narzędzia agenta

| Narzędzie | Co robi | Odpowiednik z Modułu 1/2 |
|---|---|---|
| **Read** | czyta zawartość pliku | `cat plik.txt` |
| **Edit** | zmienia fragment istniejącego pliku | edycja w nano |
| **Write** | tworzy nowy plik / nadpisuje | `echo "..." > plik` |
| **Bash** | uruchamia dowolną komendę powłoki | wszystko, co wpisuję w terminalu |
| **Grep / Glob** | szuka tekstu / plików w projekcie | `grep`, `find` |
| **WebFetch / WebSearch** | pobiera stronę / szuka w sieci | — |
| **MCP** | narzędzia z zewnętrznych serwerów | — |

Każde użycie narzędzia jest widoczne w transkrypcie sesji. To mój **ślad audytowy**:
jeśli nie widzę wywołania narzędzia, odpowiedź agenta jest niezweryfikowana.

### Kiedy używać, a kiedy nie

Używać: refaktor, zmiana rozłożona na wiele plików, debugowanie, pisanie testów,
rozeznanie w nieznanym repo, operacje gitowe, generowanie dokumentacji.

Nie używać: gdy sam nie potrafię opisać celu ani ocenić, czy wynik jest poprawny.
Agent przyspiesza pracę, którą rozumiem — nie zastępuje zrozumienia.

Wymaga konta płatnego (Pro / Max / Team / Enterprise) albo rozliczenia przez Console API.

---

## 2. Uruchamianie agenta z terminala

### Zasada podstawowa: katalog ma znaczenie

```bash
cd ~/projekty/moja-apka
pwd
claude
```

Agent startuje **w katalogu, w którym stoję**. Ten katalog jest jego obszarem
roboczym. Uruchomienie `claude` w katalogu domowym to typowy błąd — agent nie widzi
wtedy projektu.

Nawyk: **`pwd` przed `claude`.**

### Sposoby uruchomienia

| Komenda | Co robi |
|---|---|
| `claude` | sesja interaktywna w bieżącym katalogu |
| `claude "wyjaśnij ten projekt"` | sesja interaktywna z zadaniem od razu |
| `claude -p "pytanie"` | tryb print — odpowiedź na stdout i wyjście, bez sesji |
| `cat log.txt \| claude -p "znajdź błąd"` | dane z pipe'a jako wejście dla agenta |
| `claude -c` | wznów **ostatnią** sesję w tym katalogu (`--continue`) |
| `claude -r` | pokaż **listę** sesji do wznowienia (`--resume`) |
| `claude -r "nazwa"` | wznów konkretną sesję po nazwie lub ID |
| `claude -n "nazwa"` | wystartuj sesję z nadaną nazwą |
| `claude --permission-mode plan` | start w wybranym trybie uprawnień |
| `claude --model sonnet` | wymuś model na tę sesję (`sonnet`, `opus`, `haiku`) |
| `claude --version` / `-v` | wersja |
| `claude doctor` | diagnostyka instalacji, tylko do odczytu |
| `claude update` | aktualizacja |
| `claude mcp` | zarządzanie serwerami MCP |
| `claude plugin` | zarządzanie pluginami |

### Tryb interaktywny kontra `-p`

| | `claude` (interaktywny) | `claude -p` (print / headless) |
|---|---|---|
| Rozmowa | wieloturowa, agent pamięta poprzednie wiadomości | jedno pytanie, jedna odpowiedź |
| Sesja | zapisana, można wznowić | domyślnie nie trafia do `-c` |
| Komendy `/` | dostępne | w większości niedostępne |
| Wyjście | interfejs w terminalu | czysty tekst na stdout |
| Do czego | praca na żywo, iteracja | **skrypty, pipe'y, automatyzacja, CI** |

`-p` jest po to, żeby agenta dało się wpiąć w łańcuch komend — dokładnie tak, jak
uczyłem się potoków w Module 1:

```bash
claude -p "streść ten projekt" > streszczenie.txt
cat bledy.log | claude -p "co spowodowało ten crash?"
git diff | claude -p "oceń ryzyko tych zmian z perspektywy QA"
```

Wyjście z sesji interaktywnej: `/exit`, `/quit` albo `Ctrl+D`.
Przerwanie agenta w trakcie pracy: `Esc`.

---

## 3. Uprawnienia i tryby zatwierdzania

### Dlaczego to istnieje

Agent ma narzędzie Bash, czyli pełen dostęp do systemu z moimi uprawnieniami.
Agent, który źle zrozumiał polecenie, może nadpisać plik, zrobić `git reset --hard`
na niezacommitowanych zmianach, wypchnąć coś na `main` albo usunąć katalog.

Moim zadaniem nie jest ufać agentowi, tylko **świadomie decydować, ile mu wolno**.

### Warstwa 1 — monit o zgodę

```
Claude wants to run: rm stary_plik.txt
❯ 1. Yes
  2. Yes, and don't ask again for rm commands
  3. No, and tell Claude what to do differently
```

| Opcja | Znaczenie |
|---|---|
| **1. Yes** | zgoda jednorazowa — bezpieczna, domyślna |
| **2. Yes, and don't ask again** | dopisuje regułę do allowlisty, zostaje na przyszłość |
| **3. No, and tell Claude…** | odmowa + przekierowanie agenta |

Opcja 3 jest niedoceniana i **różni się od `Ctrl+C`**:

| | `Ctrl+C` | Opcja 3 |
|---|---|---|
| Agent | przerywa całą pracę | zatrzymuje tylko tę jedną akcję |
| Kontekst | zostaje, ale agent nie wie, czemu go zatrzymałem | zachowany + moje wyjaśnienie |
| Co dalej | muszę zacząć polecenie od nowa | agent sam próbuje inaczej |

Przykład: agent chce `git push origin main`. Wybieram 3 i piszę „nie pushuj na main,
utwórz branch `fix/logowanie` i wypchnij tam". Agent czyta to jako instrukcję
i wykonuje poprawioną wersję.

### Warstwa 2 — tryby uprawnień

Monit dotyczy pojedynczej akcji. Tryb dotyczy **całej sesji** i ustawia domyślną politykę.

| Tryb | Zachowanie | Kiedy używać |
|---|---|---|
| `default` (w UI: *Manual*) | pyta przed każdą zmianą pliku i każdą komendą | domyślny, bezpieczny |
| `acceptEdits` | edycje plików bez pytania, komendy nadal pytają | dużo drobnych zmian, którym ufam |
| `plan` | **niczego nie zmienia** — czyta, analizuje, kończy planem do akceptacji | nieznane repo, audyt, duża zmiana |
| `auto` | klasyfikator sam przepuszcza operacje bezpieczne, blokuje ryzykowne | codzienna praca po nabraniu wprawy |
| `dontAsk` | nie pyta, ale zachowuje blokady | rzadko, dla powtarzalnych zadań |
| `bypassPermissions` | nie pyta o nic | **tylko środowisko izolowane** (kontener, VM) |

Przełączanie w sesji: **`Shift+Tab`** — cyklicznie przez tryby.
Aktualny tryb widać **pod polem wpisywania**. To jest wskaźnik, na który patrzę
przed każdym większym poleceniem.

Start w wybranym trybie:

```bash
claude --permission-mode plan
claude --permission-mode acceptEdits
```

W sesji: `/plan` albo `/plan napraw błąd logowania`.

### Plan mode — najważniejszy tryb w pracy QA

Agent czyta, analizuje i **proponuje**, ale nie dotyka niczego. Dopiero po akceptacji
planu przechodzi do wykonania.

Zasada: **im mniej rozumiem projekt, tym bardziej zaczynam w plan mode.**

### `--dangerously-skip-permissions`

```bash
claude --dangerously-skip-permissions
```

Wyłącza wszystkie pytania. Równoważne `--permission-mode bypassPermissions`.
Nazwa nie jest przypadkowa.

Legalne zastosowanie: kontener CI, jednorazowa maszyna wirtualna — miejsce, gdzie
nie ma czego zepsuć i nikt nie patrzy na monity.

**Nie na maszynie roboczej z realnym kodem klienta, kluczami SSH i dostępem do
zdalnego repo.** Odpowiedź na pytanie „kiedy wolno": tylko w izolowanym,
jednorazowym środowisku bez dostępu do ważnych danych.

### Warstwa 3 — reguły trwałe

W sesji: `/permissions` — panel z kategoriami **allow / ask / deny**.

Reguły zapisują się w plikach ustawień:

| Plik | Zasięg |
|---|---|
| `~/.claude/settings.json` | globalny, wszystkie moje projekty |
| `.claude/settings.json` | projekt, commitowany do repo (obowiązuje zespół) |
| `.claude/settings.local.json` | projekt, prywatny — poza repo |

```json
{
  "permissions": {
    "allow": ["Read", "Bash(git status)", "Bash(git diff *)"],
    "deny": ["Bash(rm -rf *)", "Bash(git push *)", "Read(./.env)"]
  }
}
```

To samo przy starcie:

```bash
claude --allowedTools "Read" "Bash(git status)" "Bash(git diff *)"
```

Wzorzec przydatny w QA: agent „tylko do odczytu + komendy diagnostyczne" — może
wszystko przeczytać i uruchomić `git status`, ale nic nie zmieni.

### Zasada przewodnia

> Nadaję agentowi **najmniejsze uprawnienia wystarczające do zadania**.

To ta sama zasada co *least privilege* w bezpieczeństwie systemów.

---

## 4. Sesje i kontekst

### Okno kontekstowe

Agent nie ma pamięci w ludzkim sensie. Przy **każdej** mojej wiadomości dostaje na
wejście całą dotychczasową rozmowę: moje polecenia, swoje odpowiedzi, treść
przeczytanych plików, wyniki uruchomionych komend.

Ten pakiet ma limit rozmiaru — to jest **okno kontekstowe**, mierzone w tokenach
(token ≈ kawałek słowa; w polskim mniej więcej 2–3 tokeny na słowo).

Wniosek praktyczny: okno zapełnia się **nie od moich wiadomości**, tylko od danych,
które agent sam wciągnął — dużych plików i długich outputów.

### Auto-kompaktowanie

Gdy okno się zapełnia, Claude Code streszcza starszą część rozmowy i podmienia ją na
to streszczenie.

Zysk: sesja działa dalej. Koszt: **szczegóły ze streszczonej części znikają**.
To dlatego agent potrafi „zapomnieć", co ustaliliśmy godzinę wcześniej.

### Narzędzia do zarządzania kontekstem

| Komenda | Co robi | Kiedy |
|---|---|---|
| `/context` | pokazuje, **co** zajmuje okno i ile zostało | przed dużym zadaniem |
| `/clear` | **nowa, pusta rozmowa** — kasuje cały kontekst | zmiana zadania na niezwiązane |
| `/compact [wskazówka]` | streszcza ręcznie, **zachowuje ciągłość** | to samo zadanie, kontekst puchnie |
| `/rewind` | cofa rozmowę **i opcjonalnie zmiany w kodzie** | agent poszedł w złą stronę |

```
/compact skup się na ustaleniach dotyczących struktury testów
```

`/rewind` (aliasy `/undo`, `/checkpoint`) potrafi cofnąć **także pliki**, nie tylko
rozmowę. To moje „cofnij" po tym, jak agent narobił bałaganu.

Nawyk: skończone zadanie → `/clear`. Nowe zadanie zaczyna z czystym oknem.
Najczęstszy błąd początkującego to prowadzenie całego dnia pracy w jednej sesji.

### Sesje

Każda sesja interaktywna zapisuje się na dysku. Przy wyjściu Claude Code wypisuje:

```
Resume this session with:
claude --resume 49882269-d21e-4d68-b3c1-84f366f578a4
```

| Komenda | Co robi |
|---|---|
| `claude -c` | wznawia ostatnią rozmowę w bieżącym katalogu |
| `claude -r` | lista sesji do wyboru |
| `claude -r "nazwa"` | wznawia konkretną sesję |
| `claude -n "nazwa"` | startuje sesję z nazwą |
| `/resume` | przełącza sesję **bez wychodzenia** z Claude Code |

Sesje są **przypisane do katalogu** — `claude -c` w `~/cc-test` wznowi rozmowę
z `~/cc-test`, nie z innego projektu. Kolejny powód, żeby sprawdzać `pwd`.

Sesja kontra kontekst — dwie różne rzeczy:
- **sesja** = zapisana na dysku rozmowa, można do niej wrócić
- **kontekst** = to, co agent widzi *w tej chwili* na wejściu

`/clear` czyści kontekst, ale **nie kończy sesji** — dalej jestem w tym samym
procesie i katalogu.

---

## 5. Komendy slash

Wpisywane w sesji interaktywnej. Wpisanie samego `/` pokazuje listę.

### Kontekst i sesja

| Komenda | Do czego |
|---|---|
| `/context` | zużycie okna kontekstowego |
| `/clear` | nowa rozmowa, pusty kontekst (aliasy `/new`, `/reset`) |
| `/compact` | streszczenie rozmowy z zachowaniem ciągłości |
| `/rewind` | cofnięcie rozmowy i/lub kodu (aliasy `/undo`, `/checkpoint`) |
| `/resume` | przełączenie na inną sesję |

### Sterowanie agentem

| Komenda | Do czego |
|---|---|
| `/plan [opis]` | wejście w plan mode, opcjonalnie od razu z zadaniem |
| `/permissions` | panel reguł allow / ask / deny |
| `/model` | zmiana modelu |
| `/effort` | ile „myślenia" agent wkłada w zadanie (`low` … `max`) |
| `/config` | ustawienia (motyw, model domyślny) |

### Praca z kodem i Gitem

| Komenda | Do czego |
|---|---|
| `/diff` | interaktywny podgląd niezacommitowanych zmian |
| `/code-review` | przegląd diffa pod kątem błędów (alias `/review`) |
| `/security-review` | przegląd diffa pod kątem podatności |
| `/init` | wygenerowanie `CLAUDE.md` dla repo |
| `/memory` | edycja plików `CLAUDE.md` |

### Diagnostyka

| Komenda | Do czego |
|---|---|
| `/help` | lista komend |
| `/doctor` | pełny przegląd konfiguracji, **proponuje poprawki** |
| `/status` | stan sesji |
| `/usage` | zużycie limitów (alias `/cost`) |
| `/mcp` | status serwerów MCP |
| `/exit` | wyjście (alias `/quit`) |

**Różnica warta zapamiętania:**
`claude doctor` w terminalu = diagnostyka tylko do odczytu, bez uruchamiania sesji.
`/doctor` w sesji = pełny przegląd (nieużywane skille, wolne hooki, zduplikowane
`CLAUDE.md`) i **propozycje napraw do zatwierdzenia**. Nic nie zmienia bez zgody.

### Skróty w prompcie

| Zapis | Działanie |
|---|---|
| `!komenda` | uruchamia komendę shella, output ląduje w rozmowie (`!git log --oneline -5`) |
| `@ścieżka/plik` | wstawia plik do promptu |
| `#tekst` | dopisuje tekst do `CLAUDE.md` bez otwierania pliku |
| `Esc` | przerywa agenta w trakcie |
| `Shift+Tab` | przełącza tryb uprawnień |

### Składnia

Komenda musi być **na początku wiadomości**, tekst po niej to jej argument:

```
/compact skup się na ustaleniach o testach
   ↑ komenda    ↑ argument
```

**Ukośnik, nie myślnik** — to dwie różne warstwy:

| Gdzie | Składnia | Przykład |
|---|---|---|
| W terminalu, przed startem sesji | `--flaga` | `claude --permission-mode plan` |
| W środku sesji | `/komenda` | `/permissions` |

### Własne komendy

Format starszy: pliki `.md` w `.claude/commands/` — nadal działa.
Format zalecany obecnie: **skille**, czyli `.claude/skills/<nazwa>/SKILL.md`.
Anthropic scalił własne komendy ze skillami. Szczegóły w Module 6.

---

## 6. `CLAUDE.md` — pamięć projektu

### Problem, który rozwiązuje

Bez tego pliku w każdej nowej sesji tłumaczę agentowi to samo: jak uruchamiać testy,
czego nie ruszać, jaka jest konwencja commitów. Po `/clear` albo po auto-kompaktowaniu
— znowu od zera.

`CLAUDE.md` agent **czyta automatycznie przy każdym starcie sesji**.

### Lokalizacje i dziedziczenie

| Lokalizacja | Zasięg |
|---|---|
| `~/.claude/CLAUDE.md` | wszystkie moje projekty — osobiste preferencje |
| `./CLAUDE.md` w repo | ten projekt, cały zespół — commitowany do Gita |
| `podkatalog/CLAUDE.md` | reguły specyficzne dla podkatalogu |

**Dziedziczenie (sprawdzone praktycznie):** agent wczytuje plik z bieżącego katalogu
**oraz wszystkie nadrzędne, idąc w górę drzewa**. Reguły ogólne trzymam wyżej,
szczegółowe niżej — działają jednocześnie.

Konsekwencja: gdy agent zachowuje się nieoczekiwanie, sprawdzam, czy nie ma
`CLAUDE.md` piętro wyżej.

Plik w repo jest najważniejszy: wchodzi do Gita, obowiązuje cały zespół i przechodzi
przez code review jak każdy inny plik.

### `/init`

W sesji, w katalogu projektu:

```
/init
```

Agent przegląda strukturę, konfiguracje i testy, po czym pisze wstępny `CLAUDE.md`.
**To punkt startowy, nie produkt końcowy.** Agent zgadnie konwencje z kodu, ale nie
zgadnie zasad zespołowych ani tego, których katalogów nie wolno ruszać.

### Co pisać, a czego nie

To **nie jest README**. To instrukcja obsługi *dla agenta*.

| Pisz | Nie pisz |
|---|---|
| komendy budowania i testowania | opisu, czym jest projekt biznesowo |
| konwencje nazewnictwa | historii zmian |
| katalogi zakazane | rzeczy, które agent sam wyczyta z kodu |
| wymagania przed commitem | listy zależności z `package.json` |
| typowe pułapki projektu | długich wywodów |

Trzy reguły:

1. **Nie wpisuj rzeczy, które agent sam wie** (`ls`, `cd`, `git status`). Każda linia
   zajmuje okno kontekstowe w **każdej** sesji. Dlatego `/doctor` osobno wykrywa
   zbyt duże pliki `CLAUDE.md`.
2. **Zakazy formułuj pod to, co agent zrobiłby w dobrej wierze**, a mnie zaboli.
   „Nie usuwaj repo z GitHuba" jest bezużyteczne — agent i tak by tego nie zrobił.
   „Nie commituj na `main`" jest użyteczne.
3. **Sekcja z pułapkami to najcenniejsza część pliku** — wiedza, której nie ma
   w kodzie, przekazywana normalnie ustnie nowej osobie w zespole.

### Przykład

```markdown
# Projekt: sklep-api

## Komendy
- Testy jednostkowe: `npm run test:unit`
- Testy E2E: `npm run test:e2e` (wymaga `docker compose up -d`)
- Linter: `npm run lint` — uruchamiać zawsze przed commitem

## Konwencje
- Nazwy testów po angielsku, komentarze po polsku
- Każdy nowy endpoint wymaga testu E2E
- Commity: `typ: opis` (feat, fix, test, docs)

## Zakazy
- Nie modyfikuj `legacy/` — kod przeznaczony do usunięcia
- Nie commituj bezpośrednio na `main` — zawsze branch i PR
- Nie dodawaj nowych zależności bez uzgodnienia

## Pułapki
- Testy E2E przy pierwszym uruchomieniu potrzebują ~30 s na start bazy;
  bez niej failują z mylącym błędem timeoutu
- `config.local.json` jest w .gitignore — nie odtwarzaj go
```

### Powiązanie z Front Matterem (Moduł 5) i skillami (Moduł 6)

`CLAUDE.md` to czysty Markdown, bez nagłówka metadanych. Skille natomiast zaczynają
się blokiem **Front Matter**:

```yaml
---
name: code-review
description: Sprawdza diff pod kątem błędów
---
```

Różnica koncepcyjna:
- **`CLAUDE.md`** = instrukcje ładowane **zawsze**, przy każdej sesji
- **skill** = instrukcje ładowane **na żądanie**, opisane Front Matterem

---

## 7. Zastosowania w QA

| Zadanie | Jak |
|---|---|
| Analiza logów | `cat bledy.log \| claude -p "co spowodowało crash?"` |
| Ocena ryzyka zmian | `git diff \| claude -p "oceń ryzyko z perspektywy QA"` |
| Rozeznanie w nieznanym repo | `claude --permission-mode plan` — zero ryzyka modyfikacji |
| Reprodukcja buga | agent uruchamia testy, czyta stack trace, wskazuje miejsce w kodzie |
| Pisanie testów | agent czyta istniejący kod i dopisuje przypadki zgodne z konwencją |
| Przegląd przed merge'em | `/diff` (co się zmieniło) → `/code-review` (czy bezpieczne) |
| Krok w pipeline CI | `claude -p` z `--output-format json` |

### Prompt injection — klasa podatności do zapamiętania

Tryb `auto` sprawdza akcje pod kątem ryzyka **i prompt injection**. Prompt injection
to złośliwa instrukcja schowana w danych, które agent czyta — w pliku, logu,
komentarzu w kodzie, treści strony. Agent może potraktować ją jak moje polecenie.

> **Wszystko, co agent czyta, jest potencjalnym wejściem sterującym.**

To jest realna powierzchnia ataku przy pracy agenta na cudzym repo albo na danych
z zewnątrz.

---

## 8. Typowe błędy

| Błąd | Skutek | Jak unikać |
|---|---|---|
| Uruchomienie `claude` w złym katalogu | agent nie widzi projektu | `pwd` przed startem |
| `-permissions` zamiast `/permissions` | komenda nierozpoznana | w sesji ukośnik, w terminalu `--flaga` |
| Odruchowe „Yes, and don't ask again" | allowlista, której nie pamiętam | czytać, na co się zgadzam |
| `Ctrl+C` zamiast opcji 3 | agent nie wie, co zrobił źle | przekierować, nie przerywać |
| Cały dzień w jednej sesji | zaśmiecony kontekst, spadek jakości | `/clear` między zadaniami |
| Przyjmowanie wyniku bez weryfikacji | nie wiem, czy agent wiedział czy zmyślił | sprawdzić, czy użył narzędzia |
| Traktowanie `/init` jako produktu końcowego | `CLAUDE.md` niepełny albo błędny | przeczytać i poprawić |
| Rozdmuchany `CLAUDE.md` | koszt kontekstu w każdej sesji | tylko to, czego agent nie wie |
| Błędy w ścieżkach (`notatki.`, `modul-03/claude-code.md`) | komenda nie znajduje pliku | kopiować nazwę z outputu `git status` |

### Osobna uwaga: agent może być nieaktualny

Notatkę do tego modułu wygenerował agent i **pominął dwa tryby uprawnień**
(`auto`, `dontAsk`) oraz kilka komend, mimo że sam ich używałem w wersji 2.1.252.

Powód: opisał narzędzie na podstawie wiedzy z treningu, nie sprawdzając stanu
mojej instalacji.

> Wygenerowany tekst wygląda równie pewnie niezależnie od tego, czy jest aktualny.
> Notatka od agenta to szkic do weryfikacji, nie gotowy produkt.

Ta sama zasada dotyczy `CLAUDE.md` z `/init` i każdej odpowiedzi, przy której nie
widzę wywołania narzędzia.

---

## 9. Ściąga

```bash
# Uruchamianie
pwd                                 # ZAWSZE przed startem
claude                              # sesja interaktywna
claude "zadanie"                    # sesja z promptem na start
claude -p "zadanie"                 # jednorazowa odpowiedź, bez sesji
cat log.txt | claude -p "..."       # dane przez pipe
claude -c                           # wznów ostatnią sesję
claude -r                           # wybierz sesję z listy
claude -n "nazwa-zadania"           # sesja z nazwą
claude --permission-mode plan       # start w trybie tylko-analiza
claude --model sonnet               # wybór modelu
claude doctor                       # diagnostyka z terminala
claude update                       # aktualizacja
```

```
# W sesji
/context          # ile kontekstu zużyte
/clear            # nowa rozmowa, pusty kontekst
/compact          # streść rozmowę, zachowaj ciągłość
/rewind           # cofnij rozmowę i/lub kod
/plan             # wejdź w plan mode
/permissions      # reguły uprawnień
/init             # wygeneruj CLAUDE.md
/diff             # podgląd niezacommitowanych zmian
/code-review      # przegląd diffa
/doctor           # przegląd konfiguracji + propozycje napraw
/exit             # wyjście

Shift+Tab         # przełącz tryb uprawnień
Esc               # przerwij agenta
!git status       # shell w rozmowie
@src/api.py       # wstaw plik do promptu
#zawsze po polsku # dopisz do CLAUDE.md
```

---

## 10. Pytania na test

**Podstawy**
1. Czym agent CLI różni się od czatu w przeglądarce i od autouzupełniania w edytorze?
2. Opisz pętlę działania agenta.
3. Wymień pięć narzędzi agenta i ich odpowiedniki w zwykłym terminalu.
4. Skąd Claude Code wie, co jest w pliku, którego nie wkleiłem?
5. Dlaczego trzeba uruchamiać `claude` w katalogu projektu?

**Uruchamianie**
6. Kiedy użyć `claude -p` zamiast trybu interaktywnego? Podaj konkretny przykład z QA.
7. Do czego służy `claude -c`, a do czego `claude -r`?
8. Co robi `cat plik.log | claude -p "..."` i dlaczego to przydatne w testowaniu?

**Uprawnienia**
9. Wymień sześć trybów uprawnień i po jednym scenariuszu dla każdego.
10. Czym `acceptEdits` różni się od `bypassPermissions`?
11. W jakim trybie agent niczego nie zmienia? Co zwraca na końcu?
12. Czym różni się opcja „3. No, and tell Claude what to do differently" od `Ctrl+C`?
13. Kiedy wolno użyć `--dangerously-skip-permissions`, a kiedy absolutnie nie?
14. Gdzie trzymać stałe reguły uprawnień zamiast zatwierdzać je co sesję?
15. Jaka jest kolejność plików `settings.json` od globalnego do lokalnego?
16. Jak sprawdzić, w jakim trybie jestem w danej chwili?

**Kontekst i sesje**
17. Czym różni się sesja od kontekstu?
18. Co zapełnia okno kontekstowe najszybciej i dlaczego?
19. Co się dzieje przy auto-kompaktowaniu i co się przy tym traci?
20. Co robi `/clear`, a czego nie robi — czy kończy sesję?
21. Kiedy `/compact`, a kiedy `/clear`?
22. Do czego służy `/rewind` i czym różni się od `/clear`?

**Komendy**
23. Czym różni się `claude doctor` od `/doctor`?
24. Do czego służą `!`, `@` i `#` w prompcie?
25. Dlaczego `-permissions` nie zadziała, a `/permissions` tak?
26. Która para komend służy do oceny zmian przed merge'em i czym się różnią?

**CLAUDE.md**
27. Kiedy agent wczytuje `CLAUDE.md` i skąd dokładnie?
28. Na czym polega dziedziczenie plików `CLAUDE.md`?
29. Co wpisać do `CLAUDE.md`, a czego tam nie umieszczać i dlaczego?
30. Dlaczego zbyt długi `CLAUDE.md` jest realnym problemem, a nie tylko estetycznym?
31. Co robi `/init` i dlaczego wyniku nie należy przyjmować bez sprawdzenia?
32. Czym `CLAUDE.md` różni się koncepcyjnie od skilla?

**Praktyka i bezpieczeństwo**
33. Czym jest prompt injection w kontekście agenta pracującego na repo?
34. Jak zweryfikować, czy odpowiedź agenta opiera się na faktach z projektu?
35. Opisz pełny workflow: nowe zadanie w repo → wybór trybu → praca agenta →
    weryfikacja → commit → PR → merge.
