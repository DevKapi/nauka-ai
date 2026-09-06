# Moduł 6 — AI Skills (Agent Skills)

Notatka referencyjna. Kurs `nauka-ai`, projekt praktyczny: `projekt-zamowienia`.

---

## 1. Czym jest skill

**Skill to katalog na dysku z plikiem `SKILL.md` w środku.** W tym pliku jest instrukcja napisana słowami: jak wykonać konkretne, powtarzalne zadanie.

Skill nie jest programem. Nie jest wtyczką. Nie ma instalatora. To folder z plikiem tekstowym, który agent czyta.

Minimum:

```
testy/
└── SKILL.md
```

Maksimum:

```
webapp-testing/
├── SKILL.md        ← wymagany
├── examples/       ← przykłady użycia
├── scripts/        ← skrypty do uruchomienia
└── LICENSE.txt     ← licencja
```

---

## 2. Jaki problem rozwiązuje

Masz procedurę QA, którą powtarzasz: format zgłoszenia buga, sposób uruchamiania testów regresji, checklistę przed releasem. Trzy możliwości:

| Podejście | Wada |
|---|---|
| Wklejać do czatu za każdym razem | Marnujesz czas, za trzecim razem coś pominiesz |
| Wpisać do `CLAUDE.md` | `CLAUDE.md` ładuje się **w całości przy każdym starcie sesji**. Pięć procedur po 200 linii = płacisz tokenami zawsze, nawet gdy piszesz zwykły test |
| Zrobić skilla | Do kontekstu wchodzi tylko nazwa + opis. Treść dopiero przy użyciu |

**Reguła decyzyjna:** skilla robisz, gdy ciągle wklejasz te same instrukcje do czatu, albo gdy sekcja `CLAUDE.md` urosła z **faktu** do **procedury**.

- Fakt → `CLAUDE.md`: „testy uruchamia się przez `python3 -m unittest discover`"
- Procedura → skill: „uruchom testy, policz wyniki, sprawdź czy któryś nie przeszedł, opisz powód, sprawdź czy pliki testowe nie były modyfikowane"

### Progressive disclosure (stopniowe odsłanianie)

Mechanizm, dzięki któremu skille są tanie:

```
Poziom 1 — zawsze w kontekście    → nazwa + description
Poziom 2 — po wywołaniu skilla    → całe ciało SKILL.md
Poziom 3 — tylko gdy potrzebne    → pliki pomocnicze (reference.md, examples/)
```

Analogia QA: nie czytasz wszystkich 400 test casów przed sesją testową. Czytasz spis treści, otwierasz interesujący cię suite, do załączników zaglądasz tylko gdy trzeba.

---

## 3. Anatomia `SKILL.md`

```markdown
---
name: testy
description: Uruchamia testy jednostkowe w tym projekcie i podsumowuje wynik. Użyj gdy użytkownik prosi o uruchomienie testów, sprawdzenie czy testy przechodzą, weryfikację czy kod działa poprawnie, albo pyta o stan testów.
---

Uruchom `python3 -m unittest discover -v` w katalogu głównym projektu.

Następnie podsumuj:
- ile testów przeszło, ile nie przeszło
- jeśli któryś nie przeszedł: nazwa testu i powód
```

Dwie części:

1. **Front Matter** — między znacznikami `---`. Metadane w formacie YAML. To samo, co w module 5.
2. **Ciało** — wszystko pod drugim `---`. Zwykły Markdown, zwykłe zdania.

### KRYTYCZNE: `---` musi być w pierwszej linii pliku

Claude Code czyta Front Matter **tylko wtedy**, gdy otwierające `---` jest pierwszą linią. W przeciwnym razie traktuje cały plik, razem ze znacznikami, jako treść skilla.

Pusta linia lub komentarz przed `---` → metadane przestają istnieć. Skill nadal da się wywołać przez `/nazwa`, ale Claude nie ma `description`, więc nigdy nie uruchomi go sam.

To jest **cicha awaria**: nic nie wybucha, nic nie krzyczy, po prostu połowa funkcjonalności znika.

### Nazwa katalogu = nazwa komendy

```
.claude/skills/testy/SKILL.md   →   /testy
```

Pole `name` we Front Matterze to tylko etykieta wyświetlana na listach. **Komenda bierze się z nazwy katalogu**, nie z pola `name`. (Wyjątek: skille w pluginach, gdzie `name` ma znaczenie — moduł 7.)

---

## 4. Front Matter — pola

Wszystkie pola są opcjonalne. Zalecane jest tylko `description`.

### Podstawowe

| Pole | Znaczenie |
|---|---|
| `name` | Nazwa wyświetlana na listach. Domyślnie nazwa katalogu |
| `description` | **Najważniejsze pole.** Co skill robi i kiedy go użyć. Na tej podstawie Claude decyduje o automatycznym uruchomieniu |
| `when_to_use` | Dodatkowe frazy wyzwalające. Doklejane do `description` |
| `argument-hint` | Podpowiedź przy autouzupełnianiu, np. `[numer-zgloszenia]` |

### Sterujące zachowaniem

| Pole | Znaczenie |
|---|---|
| `disable-model-invocation: true` | Tylko **ty** możesz wywołać. Claude nie może |
| `user-invocable: false` | Tylko **Claude** może wywołać. Ty nie możesz |
| `allowed-tools` | Narzędzia dostępne bez pytania o zgodę, na czas jednej tury |
| `disallowed-tools` | Narzędzia zablokowane na czas działania skilla |
| `paths` | Wzorce glob — skill aktywuje się tylko przy pracy z pasującymi plikami |
| `context: fork` | Uruchamia skilla w osobnym subagencie, bez dostępu do historii rozmowy |
| `model`, `effort` | Wymuszają model / poziom wysiłku |
| `license`, `metadata`, `compatibility` | Metadane, Claude Code ich nie interpretuje |

### Tabela trzech trybów wywołania

| Front Matter | Ty możesz | Claude może | Kiedy w kontekście |
|---|---|---|---|
| (domyślnie) | Tak | Tak | Opis zawsze, całość przy wywołaniu |
| `disable-model-invocation: true` | Tak | Nie | Opis **nie** trafia do kontekstu |
| `user-invocable: false` | Nie | Tak | Opis zawsze, całość przy wywołaniu |

**Kiedy używać którego (kontekst QA):**

- **Domyślnie** — skill formatujący bug report. Chcesz, żeby zadziałał sam, gdy opisujesz defekt.
- **`disable-model-invocation: true`** — skill wypychający na środowisko testowe albo tworzący PR. Efekty uboczne, timing kontrolujesz ty. Nie chcesz, żeby Claude sam zdecydował o deployu tylko dlatego, że kod „wygląda na gotowy".
- **`user-invocable: false`** — wiedza tłem, np. „jak działa nasz legacy moduł płatności". Claude ma to wiedzieć, ale `/legacy-platnosci` nie jest sensowną komendą dla człowieka.

---

## 5. Gdzie mieszkają skille

| Poziom | Ścieżka | Zasięg |
|---|---|---|
| Wbudowany (bundled) | wewnątrz pakietu npm | Zawsze dostępny, nie edytujesz |
| Osobisty | `~/.claude/skills/<nazwa>/SKILL.md` | Wszystkie twoje projekty |
| Projektowy | `.claude/skills/<nazwa>/SKILL.md` | Tylko ten projekt |
| Pluginowy | `<plugin>/skills/<nazwa>/SKILL.md` | Tam, gdzie plugin włączony |

**Priorytet przy konflikcie nazw:** enterprise > osobisty > projektowy.

Uwaga, to jest odwrotnie niż podpowiada intuicja. Skill osobisty **nadpisuje** projektowy.

**Reguła decyzyjna:**

- Przydatny w każdym twoim projekcie → osobisty (`~/.claude/skills/`)
- Zależny od tego konkretnego repo → projektowy (`.claude/skills/`), commitowany do Gita, żeby zespół też go miał

**Dlaczego `ls ~/.claude/skills/` nie pokazuje skilli wbudowanych:** bo one nie leżą w tej lokalizacji. Są częścią pakietu `@anthropic-ai/claude-code` w `node_modules/`. `ls` przeszukuje tylko dwie ścieżki i bundled skille są dla niego niewidzialne.

**Wykrywanie zmian na żywo:** Claude Code obserwuje katalogi skilli. Gdy edytujesz `SKILL.md`, zmiana jest widoczna w bieżącej sesji bez restartu. Wyjątek: jeśli tworzysz katalog skilli, którego **nie było** przy starcie sesji, trzeba zrestartować Claude Code.

---

## 6. Skill kontra reszta

| Mechanizm | Kiedy ładowany | Kto uruchamia | Do czego |
|---|---|---|---|
| `CLAUDE.md` | Zawsze, przy starcie | — (jest tłem) | Stałe fakty o projekcie |
| Slash command (`.claude/commands/x.md`) | Przy wywołaniu `/x` | Tylko ty | Jedno polecenie, jeden płaski plik |
| Skill (`.claude/skills/x/SKILL.md`) | Opis zawsze, ciało przy wywołaniu | Ty **lub** Claude | Procedura + zaplecze |
| Subagent (`.claude/agents/x.md`) | Przy delegacji | Claude (lub ty) | Osobny kontekst, izolowana praca |
| Plugin | Po instalacji | — (dostarcza rzeczy) | Paczka: skille + komendy + hooki + MCP |

### Ważne: komendy zostały scalone ze skillami

Plik `.claude/commands/deploy.md` i skill `.claude/skills/deploy/SKILL.md` tworzą **to samo `/deploy`** i działają tak samo. Stare pliki w `commands/` nadal działają.

Z perspektywy modelu nie ma między nimi różnicy — jedne i drugie trafiają do tego samego listingu. Różnica jest tylko na dysku:

- **komenda** = jeden płaski plik `.md`
- **skill** = katalog z możliwością dołożenia skryptów, referencji, przykładów; plus Front Matter sterujący tym, kto może wywołać

Dlatego pytając agenta „jakie masz skille?", zobaczysz na liście też swoje stare slash commandy.

---

## 7. Dwie drogi wywołania — najważniejsza lekcja modułu

**Droga 1 — jawna, ukośnikiem:**
```
/testy
```
**Deterministyczna.** Zadziała zawsze.

**Droga 2 — naturalnym językiem:**
```
sprawdź czy testy przechodzą
```
**Probabilistyczna.** Claude porównuje twoje zdanie z listą opisów wszystkich skilli i **sam decyduje**, czy sięgnąć po któryś.

### Eksperyment, który to potwierdził

| `description` | Zapytanie | Wynik |
|---|---|---|
| „Użyj gdy użytkownik prosi o uruchomienie testów, sprawdzenie czy testy przechodzą…" | „sprawdź czy testy przechodzą" | `Skill(testy)` — 8 s |
| „Skill do testów." | „zweryfikuj czy kod działa poprawnie" | brak skilla — 25 s |
| „…weryfikację czy kod działa poprawnie…" (opis rozszerzony!) | „zweryfikuj czy kod działa poprawnie" | **nadal brak skilla** |

Trzeci wiersz jest najważniejszy. Opis zawierał **dokładnie** te słowa i skill i tak się nie uruchomił. Claude uznał zadanie za szersze niż uruchomienie testów i poszedł własną drogą (przeczytał logikę `rabaty.py` i `walidator.py`).

**Wniosek:** dopasowanie opisu **zwiększa szansę**, ale jej **nie gwarantuje**.

### Reguła praktyczna dla QA

> **Jeśli coś musi się wykonać — wywołuj jawnie przez `/nazwa`.**
> Automatyczne wyzwalanie traktuj jako wygodę, nie jako fundament procesu.

Nie budujesz procesu regresyjnego na założeniu, że model „pewnie sięgnie po właściwy skill".

### Diagnostyka

| Objaw | Gdzie szukać |
|---|---|
| `/nazwa` działa, naturalny język nie | Problem w `description` |
| `/nazwa` też nie działa | Problem w składni pliku (najczęściej `---` nie w pierwszej linii) |

---

## 8. Jak pisać `description`

`description` nie jest dokumentacją dla człowieka. To **warunek wyzwalania**.

Musi zawierać:
1. **Co skill robi**
2. **Kiedy go użyć** — konkretnie: słowa, które faktycznie wypowiesz

Źle:
```yaml
description: Skill do testów.
```

Dobrze:
```yaml
description: Uruchamia testy jednostkowe w tym projekcie i podsumowuje wynik.
  Użyj gdy użytkownik prosi o uruchomienie testów, sprawdzenie czy testy
  przechodzą, weryfikację czy kod działa poprawnie, albo pyta o stan testów.
```

**Najważniejszy przypadek użycia wstaw na początek.** Powód: Claude Code ładuje do kontekstu listing wszystkich skilli, a listing ma budżet znakowy (domyślnie ~1% okna kontekstowego). Przy dużej liczbie skilli opisy są **skracane**, a skrócenie może obciąć właśnie te słowa kluczowe, których model potrzebował.

### Ciało też ma koszt

Gdy skill się załaduje, jego treść zostaje w kontekście przez kolejne tury rozmowy. Każda linia to powtarzalny koszt tokenów.

- Pisz **co zrobić**, nie **jak i dlaczego**
- Trzymaj `SKILL.md` poniżej 500 linii
- Długi materiał referencyjny przenoś do osobnych plików

Claude Code **nie odczytuje pliku ponownie** w kolejnych turach. Instrukcje, które mają obowiązywać przez całe zadanie, pisz jako reguły stałe, nie jako kroki jednorazowe.

---

## 9. Pliki pomocnicze

```
moj-skill/
├── SKILL.md
├── reference.md      ← CZYTANY (treść wchodzi do kontekstu na żądanie)
├── examples.md       ← CZYTANY
└── scripts/
    └── walidator.py  ← WYKONYWANY (do kontekstu wchodzi tylko wynik)
```

Różnica ma ogromne znaczenie dla kosztu: skrypt na 500 linii, który wypisuje trzy liczby, kosztuje cię **te trzy liczby**, a nie 500 linii kodu.

Żeby Claude wiedział, że te pliki istnieją i kiedy po nie sięgnąć, **musisz je opisać w `SKILL.md`**:

```markdown
## Dodatkowe zasoby

- Pełna specyfikacja: [reference.md](reference.md)
- Przykłady użycia: [examples.md](examples.md)
```

Bez tego opisu pliki leżą na dysku i nic nie robią.

---

## 10. Komendy z tego modułu

### Bash

| Komenda | Po co jej użyliśmy |
|---|---|
| `mkdir -p .claude/skills/testy` | Utworzenie katalogu skilla. `-p` tworzy też brakujące katalogi nadrzędne i nie zgłasza błędu, gdy katalog już istnieje |
| `nano plik` | Edycja pliku. `Ctrl+O`, `Enter` zapisuje, `Ctrl+X` wychodzi |
| `cat plik` | Wypisanie zawartości. **Nawyk weryfikacyjny** — nie ufaj, że edytor zapisał |
| `head -20 plik` | Pierwsze 20 linii. Do podejrzenia Front Mattera bez ładowania całości |
| `wc -l plik` | Liczba linii. Sprawdzenie, czy skill mieści się w limicie 500 |
| `ls -la` | Zawartość katalogu. `-a` pokazuje pliki ukryte — bez tego nie zobaczysz `.claude/` |
| `git clone <url> <katalog>` | Pobranie cudzego repozytorium ze skillami |
| `cp -r zrodlo cel` | Kopiowanie katalogu. `-r` jest konieczne przy katalogach |

### Operatory łączenia komend

| Operator | Znaczenie | Wykona prawą stronę |
|---|---|---|
| `;` lub nowa linia | „potem" | **Zawsze** |
| `&&` | „i wtedy" | Tylko gdy lewa się powiodła |
| `\|\|` | „albo" | Tylko gdy lewa zawiodła |

**Reguła:** gdy komenda zmienia stan (`cd`, `git checkout`, `mkdir`), a kolejna od tego stanu zależy — łącz przez `&&`.

```bash
# ŹLE — jeśli cd zawiedzie, ls i tak się wykona w złym katalogu
cd /tmp/skille/webapp-testing
ls -la

# DOBRZE — ls uruchomi się tylko po udanym cd
cd /tmp/skille/webapp-testing && ls -la
```

### Git

| Komenda | Po co |
|---|---|
| `git rm plik` | Usuwa plik **i** zapisuje usunięcie do poczekalni. Zwykłe `rm` usuwa tylko z dysku |
| `git checkout plik` | Przywraca plik do stanu z ostatniego commita. **Zmiany przepadają bezpowrotnie** |
| `git checkout -b nazwa` | Tworzy nowy branch i przechodzi na niego. Zmiany w poczekalni przenoszą się razem |
| `git add .claude/skills/` | Dodaje katalog do poczekalni |
| `git status` | Weryfikacja przed commitem |
| `git push -u origin nazwa` | Wysyła branch i zapamiętuje powiązanie. Przy kolejnych pushach wystarczy `git push` |
| `gh pr create --title "..." --body "..."` | Tworzy Pull Request z terminala |

### W sesji Claude Code

| Komenda | Po co |
|---|---|
| `/skills` | Menu wszystkich dostępnych skilli. `Esc` wychodzi |
| `/context` | Czym wypełniony jest kontekst. Pokazuje realny koszt listingu skilli |
| `/skill-doctor` | Ile kosztuje każdy skill i jak często jest używany (wymaga Claude Code 2.1.252+) |
| `/doctor` | Szacunek kosztu listingu i jego największe składniki |
| `/exit` | Wyjście z sesji |
| `claude plugin validate .claude/skills` | Znajduje pliki `SKILL.md` z niepoprawnym Front Matterem |

---

## 11. Typowe błędy

### Błędy w samym skillu

**1. `---` nie w pierwszej linii pliku**
Front Matter przestaje istnieć. `/nazwa` nadal działa, ale Claude nie ma opisu, więc nigdy nie sięgnie sam. Cicha awaria.

**2. `description` bez słów wyzwalających**
„Skill do testów" nie da modelowi się czego złapać. Potwierdzone eksperymentem.

**3. Zbyt długie ciało**
Zostaje w kontekście przez całą rozmowę. Każda zbędna linia to powtarzalny koszt.

**4. Pliki pomocnicze nieopisane w `SKILL.md`**
Leżą na dysku i nic nie robią, bo Claude nie ma powodu tam zajrzeć.

**5. Oczekiwanie gwarancji od automatycznego wyzwalania**
To decyzja modelu, nie mechanizm deterministyczny.

### Błędy przy pracy w terminalu

**6. Wklejanie kilku komend naraz bez `&&`**

```bash
cd /zla/sciezka
ls -la
```

`cd` zawodzi, ale `ls` **i tak się wykonuje** — w poprzednim katalogu. Dostajesz wiarygodnie wyglądający output, który opisuje coś innego, niż myślisz. Awaria nie jest cicha (bash wypisuje błąd), ale zostaje **zagłuszona** przez wynik kolejnych komend. Efekt praktyczny jest identyczny.

**7. `nano` na katalogu**
`nano` edytuje pliki, nie katalogi. Do oglądania zawartości katalogu służy `ls`.

**8. Testowanie skilla w brudnej sesji**
Jeśli w tej samej sesji już uruchomiłeś testy, Claude po prostu powtórzy zapamiętany wynik zamiast uruchomić skilla. Rozpoznasz to po czasie: 1 s zamiast 8 s.

> **Do testowania automatycznego wyzwalania zawsze startuj nową sesję (`/exit`, potem `claude`) i zadaj pytanie jako pierwszą wiadomość.**

---

## 12. Zastosowania praktyczne w QA

**Uruchamianie testów** (zrobione w tym module)
Skill uruchamia suite i podsumowuje w ustalonym formacie. Zamiast pamiętać komendę i ręcznie liczyć wyniki.

**Formatowanie bug reportu**
`description` z frazami typu „zgłoś bug", „opisz defekt", „przygotuj bug report". Ciało: wymagane sekcje (kroki reprodukcji, oczekiwany rezultat, faktyczny rezultat, środowisko, priorytet). Efekt: każde zgłoszenie ma ten sam kształt.

**Checklista przed releasem**
`disable-model-invocation: true`, bo chcesz kontrolować timing. Ciało: lista punktów do przejścia.

**Analiza pokrycia testami**
Skill ze skryptem w `scripts/`, który liczy pokrycie i wypisuje podsumowanie. Skrypt się wykonuje, do kontekstu wchodzi tylko wynik.

**Wiedza o legacy module**
`user-invocable: false`. Claude ma znać kontekst, ale to nie jest komenda dla człowieka.

---

## 13. Pytania kontrolne

Odpowiedz sobie z zamkniętą notatką.

1. Czym różni się skill od pliku w `.claude/commands/`? Podaj różnicę na dysku i różnicę z perspektywy modelu.
2. Dlaczego `ls ~/.claude/skills/` nie pokazuje skilla `/code-review`?
3. Skill działa po wpisaniu `/nazwa`, ale Claude nigdy nie uruchamia go sam. Gdzie szukasz przyczyny?
4. Skill nie działa ani przez `/nazwa`, ani automatycznie. Gdzie szukasz teraz?
5. Masz skill `deploy` w `~/.claude/skills/` i w `.claude/skills/`. Który zadziała po wpisaniu `/deploy`?
6. Co robi `disable-model-invocation: true` i dla jakiego typu skilla ma to sens?
7. Co robi `user-invocable: false` i dla jakiego typu skilla ma to sens?
8. Dlaczego `SKILL.md` ma limit ~500 linii, skoro treść ładuje się dopiero przy wywołaniu?
9. Czym różni się plik `reference.md` od skryptu w `scripts/` z punktu widzenia kosztu tokenów?
10. Wyjaśnij progressive disclosure na trzech poziomach.
11. Napisałeś skilla z `description` idealnie pasującym do twojego zapytania, a mimo to się nie uruchomił. Czy to bug?
12. Testujesz automatyczne wyzwalanie skilla. Dlaczego musisz zrobić to w nowej sesji?
13. Wykonujesz `cd /jakis/katalog` i `ls -la` w dwóch osobnych liniach. `cd` zawodzi. Co zobaczysz i dlaczego to niebezpieczne?
14. Czym różni się `git rm plik` od `rm plik`?
15. Kiedy informacja o projekcie powinna trafić do `CLAUDE.md`, a kiedy do skilla?

---

## 14. Co zostało zrobione praktycznie

- Rekonesans dostępnych skilli (`/skills`, `/context`, `ls -la`)
- Sklonowanie i obejrzenie oficjalnego repozytorium `anthropics/skills`
- Analiza cudzego skilla (`webapp-testing`) — struktura katalogu i Front Matter
- **Napisanie własnego skilla** `.claude/skills/testy/SKILL.md`
- Test obu dróg wywołania (`/testy` i naturalny język)
- Celowe zepsucie `description` i obserwacja skutku
- Usunięcie duplikatu (`git rm .claude/commands/testy-goly.md`)
- Branch → commit → push → Pull Request #3 → merge
