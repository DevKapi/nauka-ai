---
title: "Moduł 6 — AI Skills"
module: 6
author: DevKapi
tags: [skills, claude-code, agent-skills, qa]
status: reference
updated: 2026-09-06
zrodlo: https://code.claude.com/docs/en/skills
---

# Moduł 6 — AI Skills

## Czym jest skill — najprościej jak się da

Skill to **katalog z plikiem `SKILL.md`**, w którym zapisujesz instrukcję dla modelu. Nic więcej. Nie ma tu żadnego kodu, żadnej instalacji, żadnego API. To jest plik tekstowy z nagłówkiem YAML i treścią w Markdownie.

Analogia, która działa najlepiej w kontekście QA: skill to **procedura testowa w formie dokumentu**. W dziale QA masz procedury opisujące, jak przeprowadzić regresję, jak zgłosić błąd, jak przygotować środowisko. Nowy tester dostaje ten dokument i wykonuje procedurę. Skill jest dokładnie tym samym, tylko odbiorcą jest agent AI, a "wykonanie" polega na tym, że model czyta procedurę i się nią kieruje.

Formalnie: skille w Claude Code realizują otwarty standard **Agent Skills** (agentskills.io), który działa też w innych narzędziach AI. Claude Code dokłada do niego własne rozszerzenia, o których poniżej.

## Po co skill istnieje — problem, który rozwiązuje

Wyobraź sobie, że przy każdej sesji z agentem wklejasz mu tę samą instrukcję: "kiedy piszesz raport z błędu, zawsze podawaj kroki reprodukcji, środowisko, wersję, oczekiwany i faktyczny rezultat, i formatuj to według szablonu Jiry". Za piątym razem to męczy. Za dwudziestym — zaczynasz zapominać fragmenty i raporty przestają być spójne.

Skill to ta instrukcja zapisana raz, na dysku, w miejscu, w którym agent sam ją znajdzie.

Trzy sytuacje, w których warto zrobić skill: kiedy **wklejasz w kółko ten sam prompt**; kiedy **procedura ma więcej niż kilka kroków** i pamiętanie ich to ryzyko; kiedy **fragment `CLAUDE.md` urósł z faktu do procedury** — bo `CLAUDE.md` ładuje się w całości do każdej sesji i płacisz za niego tokenami zawsze, a skill kosztuje prawie nic, dopóki go nie użyjesz.

## Progressive disclosure — mechanizm, który musisz rozumieć

To jest najważniejsza koncepcja w tym module i najczęstsze pytanie na teście.

Kontekst modelu jest ograniczony i kosztowny. Gdyby Claude Code ładował pełną treść wszystkich twoich skilli do każdej sesji, przy trzydziestu skillach nie zostałoby miejsca na pracę. Dlatego ładowanie jest **stopniowe**, w warstwach.

**Warstwa pierwsza — listing.** Do kontekstu każdej sesji trafia lista nazw skilli i ich opisów (`description`, ewentualnie plus `when_to_use`). To kilkadziesiąt tokenów na skill. Model wie, że coś istnieje i do czego służy, ale nie zna treści.

**Warstwa druga — treść.** Gdy model uzna, że skill pasuje do zadania, albo gdy ty wpiszesz `/nazwa-skilla`, cała treść `SKILL.md` wchodzi do rozmowy jako jedna wiadomość i **zostaje tam do końca sesji**. To ważne: treść nie jest wczytywana ponownie przy każdej turze i nie znika po jednej odpowiedzi. Każda linia treści to więc powtarzalny koszt tokenów przez resztę sesji — stąd zalecenie, żeby `SKILL.md` był zwięzły.

**Warstwa trzecia — pliki pomocnicze.** Wszystko, co leży obok `SKILL.md` (`reference.md`, `examples.md`, skrypty), model czyta dopiero wtedy, gdy uzna, że tego potrzebuje. Możesz w ten sposób trzymać przy skillu stustronicową specyfikację API i nie płacić za nią nic, dopóki nie będzie potrzebna.

Konsekwencja praktyczna, którą trzeba zapamiętać: **`description` jest jedyną rzeczą, którą model widzi, zanim zdecyduje, czy sięgnąć po skill**. Jeżeli opis jest zły, treść może być genialna i nikt jej nigdy nie zobaczy.

Uzupełnienie o limitach, bo to bywa zaskoczeniem: listing skilli ma budżet znakowy (domyślnie około 1% okna kontekstu). Gdy masz bardzo dużo skilli, Claude Code zaczyna **skracać opisy**, zaczynając od tych najrzadziej używanych. Pojedynczy wpis (`description` + `when_to_use`) jest przycinany na 1536 znakach. Dlatego najważniejszy przypadek użycia pisz **na początku opisu** — koniec może zostać obcięty.

## Anatomia skilla — struktura katalogu

Minimum:

```text
moj-skill/
└── SKILL.md
```

Pełniejsza, typowa struktura:

```text
bug-report/
├── SKILL.md            # wymagany: nagłówek + instrukcja
├── reference.md        # szczegóły ładowane na żądanie
├── examples.md         # przykłady dobrych i złych raportów
├── templates/
│   └── jira.md         # szablon do wypełnienia
└── scripts/
    └── zbierz_logi.sh  # skrypt uruchamiany, nie wczytywany do kontekstu
```

Zasada podziału: `SKILL.md` to **mapa** — mówi, co robić i gdzie szukać szczegółów. Pozostałe pliki to **teren**. Dokumentacja zaleca trzymać `SKILL.md` **poniżej 500 linii**; wszystko dłuższe przenieś do plików obok i odwołaj się do nich z treści, na przykład tak:

```markdown
## Dodatkowe materiały

- Pełna lista pól Jiry: [reference.md](reference.md)
- Przykłady dobrych raportów: [examples.md](examples.md)
```

Model przeczyta te pliki tylko wtedy, gdy uzna, że są potrzebne.

## SKILL.md — Front Matter, pole po polu

Nagłówek to YAML między `---`. Wszystkie pola są **opcjonalne**; rekomendowane jest `description`, żeby model wiedział, kiedy sięgnąć po skill.

```yaml
---
name: bug-report
description: "Tworzy ustandaryzowany raport błędu. Użyj, gdy użytkownik zgłasza defekt, wkleja stacktrace albo prosi o sformatowanie zgłoszenia do Jiry."
allowed-tools: Read Grep
---
```

Pola, które realnie będziesz używał:

| Pole | Do czego służy |
|------|----------------|
| `name` | Nazwa wyświetlana na liście skilli. **Nie decyduje o komendzie** w skillach osobistych i projektowych — tam komenda bierze się z nazwy katalogu. W skillach z pluginu `name` ustawia ostatni człon komendy. |
| `description` | Co skill robi i **kiedy go użyć**. Na tej podstawie model decyduje o aktywacji. Jeżeli pominiesz, użyty zostanie pierwszy akapit treści. |
| `when_to_use` | Dodatkowy kontekst aktywacji: frazy wyzwalające, przykładowe prośby. Doklejane do `description` i liczy się do limitu 1536 znaków. |
| `argument-hint` | Podpowiedź argumentów w autouzupełnianiu, np. `[numer-issue]`. |
| `arguments` | Nazwane argumenty pozycyjne do podstawienia jako `$nazwa`. |
| `disable-model-invocation` | `true` = tylko ty możesz uruchomić skill przez `/nazwa`; model nie uruchomi go sam. Dla operacji ze skutkami ubocznymi: deploy, commit, wysyłka. Skill znika wtedy z kontekstu, więc oszczędza tokeny. |
| `user-invocable` | `false` = tylko model może uruchomić skill; nie pojawia się w menu `/`. Dla wiedzy tła, której nie uruchamia się jak komendy. |
| `allowed-tools` | Narzędzia, których model może użyć **bez pytania o zgodę** w turze, w której skill został wywołany. Uprawnienie wygasa przy twojej następnej wiadomości. |
| `disallowed-tools` | Narzędzia usunięte z puli na czas działania skilla. |
| `model` | Model używany, gdy skill jest aktywny. |
| `effort` | Poziom wysiłku: `low`, `medium`, `high`, `xhigh`, `max`. |
| `context` | `fork` = skill uruchamia się w osobnym subagencie, bez dostępu do historii rozmowy. |
| `agent` | Typ subagenta przy `context: fork` (np. `Explore`, `Plan`, `general-purpose`). |
| `paths` | Wzorce glob ograniczające automatyczną aktywację do pracy nad pasującymi plikami. |
| `hooks` | Hooki rejestrowane przy wywołaniu skilla. |
| `metadata` | Dowolna mapa na twoje własne dane; Claude Code jej nie interpretuje. |
| `license`, `compatibility` | Pola ze standardu Agent Skills; Claude Code je przyjmuje, ale nic z nimi nie robi. |

Dwie rzeczy warte podkreślenia, bo są nieoczywiste i bywają pytaniem.

**Pierwsza: `allowed-tools` w skillu nie ogranicza, tylko przyznaje.** To nie jest lista "wolno tylko tego". To jest lista "tego nie musisz pytać o zgodę". Wszystkie inne narzędzia dalej są dostępne i podlegają normalnym uprawnieniom. Jeżeli chcesz coś **odebrać**, służy do tego `disallowed-tools` albo reguły `deny` w ustawieniach uprawnień.

**Druga: `---` musi być pierwszą linią.** Jeżeli nie jest, Claude Code potraktuje cały plik razem z myślnikami jako treść skilla. Nie dostaniesz błędu.

**Uwaga przy dystrybucji poza Claude Code.** Jeżeli chcesz wgrać skill na claude.ai, przez Skills API albo spakować `package_skill.py`, wolno użyć tylko sześciu pól ze standardu: `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`. Każde inne pole powoduje **twardy błąd** przy pakowaniu, a nie ciche zignorowanie.

## Skąd bierze się nazwa komendy

To bywa mylące, więc tabelka:

| Gdzie leży skill | Skąd komenda | Przykład |
|---|---|---|
| `~/.claude/skills/<katalog>/SKILL.md` | nazwa katalogu | `deploy-staging/` → `/deploy-staging` |
| `.claude/skills/<katalog>/SKILL.md` | nazwa katalogu | jw. |
| `.claude/commands/<plik>.md` | nazwa pliku | `deploy.md` → `/deploy` |
| `<plugin>/skills/<katalog>/SKILL.md` | `name` z Front Mattera lub nazwa katalogu, z prefiksem pluginu | `/my-plugin:review` |

Czyli: w swoim własnym skillu możesz mieć `name: cokolwiek`, a komenda i tak będzie się nazywać jak katalog. To pierwsze źródło zdziwienia. Dla porządku trzymaj nazwę katalogu i `name` identyczne.

## Gdzie mieszkają skille

| Poziom | Ścieżka | Zasięg |
|---|---|---|
| Osobisty | `~/.claude/skills/<nazwa>/SKILL.md` | wszystkie twoje projekty |
| Projektowy | `.claude/skills/<nazwa>/SKILL.md` | tylko ten projekt, wersjonowany w Gicie |
| Plugin | `<plugin>/skills/<nazwa>/SKILL.md` | tam, gdzie plugin jest włączony |
| Firmowy | przez managed settings | cała organizacja |

Rozstrzyganie konfliktów nazw: firmowy przebija osobisty, osobisty przebija projektowy. Skill z któregokolwiek z tych poziomów przebija skill wbudowany o tej samej nazwie. Skille z pluginów mają własną przestrzeń nazw `plugin:skill`, więc nie kolidują z niczym.

Do tego dwie rzeczy praktyczne. Skille projektowe ładują się z `.claude/skills/` w katalogu startowym **i we wszystkich katalogach nadrzędnych** aż do korzenia repozytorium. Skille w katalogach *poniżej* startowego ładują się dopiero wtedy, gdy Claude pierwszy raz dotknie pliku w tym podkatalogu — do tego czasu nie ma ich nawet w autouzupełnianiu.

**Wykrywanie zmian na żywo.** Claude Code obserwuje katalogi skilli. Gdy dodasz, zmienisz albo usuniesz `SKILL.md`, zmiana łapie się w bieżącej sesji, bez restartu. Ale jeżeli tworzysz katalog skilli, którego nie było przy starcie sesji, trzeba zrestartować.

## Jak używać gotowych skilli

Trzy drogi.

**Wpisujesz `/nazwa`** — jawne wywołanie. Możesz dodać argumenty: `/fix-issue 123`.

**Model uruchamia sam** — gdy twoja prośba pasuje do `description`. Nie musisz nic robić.

**Sprawdzasz, co masz** — komenda `/skills` pokazuje menu ze wszystkimi dostępnymi skillami i pozwala przełączać ich widoczność. Zapytanie "jakie masz dostępne skille?" też działa i jest dobrym testem, czy twój nowy skill w ogóle się załadował.

Skille wbudowane, które warto znać, bo są od razu dostępne: `/doctor` (diagnostyka konfiguracji), `/code-review`, `/debug`, `/verify`, `/run`, `/batch`, `/loop`. Do znalezienia nieużywanych skilli i ich kosztu tokenowego służy `/skill-doctor`.

## Argumenty i podstawienia

W treści skilla możesz używać placeholderów, które Claude Code podmienia przed wysłaniem treści do modelu.

`$ARGUMENTS` — całość tego, co wpisałeś po nazwie skilla. `$ARGUMENTS[0]` albo krócej `$0` — pierwszy argument, `$1` drugi i tak dalej. Wartości wielowyrazowe trzeba wziąć w cudzysłów przy wywołaniu.

```markdown
---
name: migrate-component
description: Migruje komponent z jednego języka na drugi
---

Zmigruj komponent $0 z $1 na $2. Zachowaj istniejące zachowanie i testy.
```

Wywołanie `/migrate-component SearchBar JavaScript TypeScript` podstawi kolejno trzy wartości.

Zmienne środowiskowe dostępne w treści: `${CLAUDE_SKILL_DIR}` (katalog samego skilla — używaj go do odwołań do własnych skryptów, żeby działały niezależnie od katalogu roboczego), `${CLAUDE_PROJECT_DIR}` (korzeń projektu), `${CLAUDE_SESSION_ID}`, `${CLAUDE_EFFORT}`, a w skillach z pluginu dodatkowo `${CLAUDE_PLUGIN_ROOT}` i `${CLAUDE_PLUGIN_DATA}`.

## Wstrzykiwanie kontekstu dynamicznego

To jest funkcja, która zamienia skill ze statycznej instrukcji w narzędzie operujące na żywych danych. Zapis `` !`komenda` `` powoduje, że Claude Code **uruchamia tę komendę zanim treść trafi do modelu** i wstawia w to miejsce jej wynik.

```markdown
---
description: "Podsumowuje niezacommitowane zmiany i wskazuje ryzyka. Użyj, gdy pytam co zmieniłem albo proszę o wiadomość commita."
---

## Bieżące zmiany

!`git diff HEAD`

## Instrukcja

Podsumuj powyższe zmiany w dwóch, trzech punktach, a potem wypisz ryzyka: brak obsługi błędów, wartości zaszyte na sztywno, testy wymagające aktualizacji.
```

Model dostaje gotowy diff w treści, a nie polecenie "zrób git diff". Różnica jest zasadnicza: nie ma dodatkowej tury, nie ma pytania o uprawnienia, dane są na pewno aktualne.

Rzeczy, które trzeba wiedzieć, żeby nie wpaść w pułapkę. **Nieudana komenda przerywa całe wywołanie skilla** — model nie zobaczy nic. Przy domyślnym bashu każdy niezerowy kod wyjścia to porażka (z wyjątkiem kodu 1 z komend wyszukujących, jak `grep`). Jeżeli twoja komenda ma prawo zwracać niezerowy kod, dopisz `|| true`. Komendy nigdy nie pytają o uprawnienia — jeżeli reguła uprawnień nie mówi "allow", wywołanie jest przerywane; dlatego takie komendy warto wpisać do `allowed-tools`. Znak `!` musi stać na początku linii albo po spacji. Do komend wielolinijkowych używa się bloku otwartego ` ```! `.

## Uruchamianie skilla w subagencie

`context: fork` powoduje, że skill działa w osobnym, izolowanym kontekście: treść `SKILL.md` staje się promptem subagenta, a subagent nie widzi twojej rozmowy. Wynik wraca do głównej konwersacji po zakończeniu. Domyślnie działa w tle, więc możesz pracować dalej; `background: false` każe poczekać na wynik w tej samej turze.

Kiedy to ma sens: przy zadaniach zwiadowczych i długich, które zaśmieciłyby główny kontekst (przeszukanie repozytorium, analiza dużego PR-a). Kiedy nie ma sensu: przy skillach zawierających same wytyczne bez zadania — subagent dostanie wtedy wytyczne i nie będzie miał czego wykonać.

## Jak pisać dobry `description` — najważniejsza umiejętność w tym module

Opis odpowiada na dwa pytania: **co skill robi** i **kiedy go użyć**. To drugie jest ważniejsze, a początkujący prawie zawsze je pomijają.

Źle:

```yaml
description: Skill do raportowania błędów
```

Model wie, że coś takiego istnieje, ale nie ma pojęcia, w jakiej sytuacji sięgnąć. Efekt: skill nigdy nie uruchamia się sam.

Dobrze:

```yaml
description: "Tworzy ustandaryzowany raport błędu w formacie Jiry, z krokami reprodukcji, środowiskiem i klasyfikacją ważności. Użyj, gdy użytkownik zgłasza defekt, wkleja stacktrace, opisuje nieprawidłowe zachowanie aplikacji albo prosi o sformatowanie zgłoszenia."
```

Zasady, które to odróżniają. **Zaczynaj od czasownika opisującego rezultat** — "Tworzy", "Waliduje", "Generuje", nie "Ten skill służy do". **Dopisz jawne 'Użyj, gdy...'** z konkretnymi sytuacjami. **Wpleć słowa, których naprawdę użyje użytkownik** — jeżeli twój zespół mówi "stacktrace", "wywalił się", "regresja", to te słowa mają być w opisie, bo dopasowanie idzie po znaczeniu, ale konkretne słownictwo bardzo pomaga. **Najważniejszy przypadek na początku**, bo opis może zostać przycięty. **Pisz w trzeciej osobie** — to opis narzędzia, nie polecenie.

Jeżeli chcesz rozdzielić "co robi" od "kiedy używać" na dwa pola, użyj `when_to_use`. Efekt w listingu jest ten sam (pola są sklejane), ale plik jest czytelniejszy.

## Jak pisać treść skilla

**Rozkazująco i konkretnie.** "Sprawdź, czy raport zawiera wersję aplikacji" jest lepsze niż "warto sprawdzać wersje". Model traktuje treść jak instrukcję, więc pisz instrukcję.

**Krok po kroku, numerowanie.** Procedura o pięciu krokach ma być pięcioma ponumerowanymi krokami.

**Zwięźle.** Treść zostaje w kontekście do końca sesji. Każde zdanie wyjaśniające "dlaczego" płacisz tokenami przy każdej turze. Pisz **co zrobić**, nie **dlaczego to dobry pomysł**.

**Podaj przykład wejścia i oczekiwanego wyjścia.** Jeden konkretny przykład działa lepiej niż akapit opisu formatu.

**Opisz, co robić w sytuacjach brzegowych.** "Jeżeli w logu nie ma stacktrace'a, poproś użytkownika o numer wersji i kroki." Bez tego model improwizuje.

**Nie duplikuj informacji.** Jeżeli coś jest w `reference.md`, w `SKILL.md` napisz tylko, gdzie tego szukać.

**Nie wkładaj sekretów.** Skille bywają commitowane do repo i udostępniane. Żadnych tokenów, haseł, wewnętrznych adresów, jeżeli repo ma szansę wyjść poza zespół.

## Testowanie i poprawianie skilla

To jest część, która najbardziej łączy się z twoim zawodem, i część, którą prawie wszyscy pomijają.

**Podstawowa zasada: to, że skill się uruchomił, nie znaczy, że zadziałał.** To dwa oddzielne pytania i mierzy się je osobno.

**Pytanie pierwsze: czy skill aktywuje się wtedy, kiedy powinien?** Testujesz to tak, że przygotowujesz zestaw realistycznych promptów: kilka takich, przy których skill **powinien** się odpalić, i kilka takich, przy których **nie powinien**. Ten drugi zestaw jest równie ważny — skill, który odpala się na wszystko, zaśmieca kontekst i psuje inne odpowiedzi. To dokładnie odpowiednik testów pozytywnych i negatywnych.

**Pytanie drugie: czy wynik jest taki, jakiego chcesz?** Tutaj metodą jest **porównanie z bazą odniesienia**: uruchamiasz ten sam prompt raz ze skillem, raz bez, i porównujesz wyniki. Jeżeli nie ma różnicy, skill nic nie wnosi.

**Każdy test w świeżej sesji.** To jest krytyczne i łatwo zapomnieć. Kiedy pisałeś skill, w kontekście sesji siedzi cała rozmowa o tym, co skill ma robić — model "wie", czego chcesz, niezależnie od tego, co jest w pliku. Testowanie w tej samej sesji zamaskuje ci wszystkie luki w instrukcji. Nowa sesja, `/clear`, albo najlepiej osobny terminal.

**Iteracja.** Skill nie odpala się → popraw `description`, dodaj słowa wyzwalające, sprawdź `--debug`. Skill odpala się za często → zawęź opis albo dodaj `disable-model-invocation: true`. Skill odpala się, ale wynik jest zły → problem jest w treści, nie w opisie; dodaj przykłady i konkretne kroki.

**Narzędzia diagnostyczne.** `claude --debug` pokazuje błędy parsowania Front Mattera i rejestrację skilli. Zapytanie "jakie skille są dostępne" weryfikuje, że skill w ogóle się widzi. `claude plugin validate ~/.claude/skills` (albo `.claude/skills`) sprawdza, które pliki `SKILL.md` mają nieparsujący się Front Matter. `/doctor` szacuje koszt kontekstowy listingu skilli, `/skill-doctor` pokazuje, które skille nigdy nie były użyte.

**Automatyzacja porównań.** Do systematycznej ewaluacji istnieje oficjalny plugin `skill-creator`:

```text
/plugin marketplace add anthropics/claude-plugins-official
/plugin install skill-creator@claude-plugins-official
```

Robi to, co opisałem wyżej, tylko automatycznie: trzyma przypadki testowe w `evals/evals.json`, uruchamia każdy w osobnym subagencie z czystym kontekstem, ocenia asercje i zapisuje wynik do `grading.json`, agreguje porównanie "ze skillem" kontra "bez skilla" do `benchmark.json`, robi ślepe A/B między dwiema wersjami skilla i osobno mierzy trafność samego `description` na promptach, które powinny i nie powinny go wyzwolić.

## Typowe błędy

**Opis zbyt ogólny.** Najczęstsza przyczyna, dla której skill nigdy się nie uruchamia.

**Za długi `SKILL.md`.** Powyżej 500 linii koszt tokenowy zaczyna boleć. Przenieś do plików pomocniczych.

**Zależność od kontekstu, którego w świeżej sesji nie ma.** "Popraw to tak jak wcześniej" nie ma sensu w skillu.

**Błąd YAML w Front Matterze.** Skill ładuje się z pustymi metadanymi. `/nazwa` dalej działa, więc wygląda, że wszystko gra — ale model nigdy nie uruchomi go sam. To jest klasyczna cicha awaria z modułu 5.

**Niedopasowana nazwa katalogu i pola `name`.** Nie powoduje błędu, ale myli.

**`allowed-tools` traktowane jako ograniczenie.** Nie ogranicza. Przyznaje.

**Brak testów negatywnych.** Skill odpalający się na wszystko jest gorszy niż jego brak.

## Kompletny przykład — skill QA do raportowania błędów

Struktura:

```text
~/.claude/skills/bug-report/
├── SKILL.md
├── reference.md
└── examples.md
```

`SKILL.md`:

````markdown
---
name: bug-report
description: "Tworzy ustandaryzowany raport błędu z krokami reprodukcji, środowiskiem, wersją oraz oczekiwanym i faktycznym rezultatem. Użyj, gdy użytkownik zgłasza defekt, wkleja stacktrace, opisuje nieprawidłowe zachowanie aplikacji albo prosi o przygotowanie zgłoszenia do Jiry."
when_to_use: "Frazy wyzwalające: 'wywalił się', 'nie działa', 'zgłoś błąd', 'zrób z tego ticket', wklejony traceback lub log błędu."
allowed-tools: Read Grep Bash(git log *)
---

# Raport błędu

## Kontekst repozytorium

- Ostatni commit: !`git log -1 --oneline`
- Bieżąca gałąź: !`git rev-parse --abbrev-ref HEAD`

## Zadanie

Przygotuj raport błędu w poniższym formacie. Jeżeli którejś informacji brakuje, **zapytaj o nią zamiast zgadywać**.

## Format

```text
Tytuł: [moduł] zwięzły opis objawu

Środowisko: <dev | staging | prod>
Wersja/commit: <hash lub numer wersji>
Ważność: <krytyczny | wysoki | średni | niski>

Kroki reprodukcji:
1.
2.
3.

Oczekiwany rezultat:
Faktyczny rezultat:

Dowody: <log, zrzut ekranu, stacktrace>
```

## Zasady

1. Tytuł ma opisywać **objaw**, nie domniemaną przyczynę.
2. Kroki muszą być odtwarzalne przez kogoś, kto nie zna kontekstu — bez "zaloguj się jak zwykle".
3. Ważność ustalaj według tabeli w [reference.md](reference.md).
4. Jeżeli w treści jest stacktrace, wyciągnij z niego plik i numer linii i wpisz do sekcji Dowody.
5. Jeżeli brakuje wersji, sprawdź ostatni commit powyżej i zaproponuj go, oznaczając jako wymagający potwierdzenia.

## Materiały

- Tabela ważności i pola Jiry: [reference.md](reference.md)
- Przykłady dobrych i złych raportów: [examples.md](examples.md)
````

Zwróć uwagę na kilka decyzji projektowych w tym pliku. `description` mówi wprost, kiedy użyć, i wymienia sytuacje. `when_to_use` dokłada dosłowne frazy, których używa zespół. `allowed-tools` ogranicza się do odczytu i jednej wąskiej komendy gita — nie ma tam `Write` ani `Bash(*)`, bo skill niczego nie zapisuje. Wstrzyknięcie `git log` daje wersję bez dodatkowej tury. Punkt 5 opisuje sytuację brzegową. Szczegóły siedzą w plikach obok.

## Zastosowania w dziale QA — co realnie warto zrobić

Skill generujący raport błędu w firmowym formacie (powyżej). Skill sprawdzający kompletność przypadku testowego według checklisty zespołu. Skill zamieniający opis wymagania w szkielet przypadków testowych, z uwzględnieniem ścieżek negatywnych. Skill analizujący log z nieudanego builda i wskazujący pierwszy realny błąd, a nie ostatni. Skill do przygotowania podsumowania regresji z wyników testów. Skill z konwencjami nazewnictwa testów w projekcie, ustawiony na `user-invocable: false`, bo to wiedza tła, a nie komenda.

## Pytania, które mogą paść na teście

Czym różni się skill od promptu wklejanego ręcznie. Co to jest progressive disclosure i ile ma warstw. Które pole Front Mattera decyduje o automatycznej aktywacji i dlaczego. Co się stanie, gdy `---` nie będzie pierwszą linią pliku. Czy `allowed-tools` ogranicza, czy przyznaje uprawnienia i na jak długo. Jaka jest różnica między `disable-model-invocation: true` a `user-invocable: false`. Skąd bierze się nazwa komendy skilla w skillu projektowym, a skąd w skillu z pluginu. Dlaczego skill trzeba testować w świeżej sesji. Czym jest test negatywny w kontekście skilla. Co zrobić, gdy skill nigdy się nie uruchamia, a co, gdy uruchamia się za często. Jak sprawdzić, czy Front Matter skilla się parsuje. Gdzie leżą skille osobiste, a gdzie projektowe, i który wygrywa przy konflikcie nazw. Dlaczego treść `SKILL.md` ma być krótka.

---

## ZADANIE PRAKTYCZNE — MODUŁ 6

**Zadanie 6.1 [WYŚLIJ]** — Utwórz własny skill osobisty w `~/.claude/skills/`. Temat: cokolwiek związanego z twoją pracą QA (raport błędu, checklista przypadku testowego, analiza logu). Wymagania: poprawny Front Matter z `name`, `description` zawierającym jawne "Użyj, gdy...", oraz `allowed-tools` ograniczonym do minimum. Treść ma zawierać numerowaną procedurę, format wyjścia i co najmniej jedną regułę dla sytuacji brzegowej. Wyślij zawartość `SKILL.md`.

**Zadanie 6.2 [WYŚLIJ]** — Zweryfikuj, że skill się załadował, i wyślij surowy output:

```bash
ls -la ~/.claude/skills/<twoja-nazwa>/
claude plugin validate ~/.claude/skills
echo "kod wyjścia: $?"
```

**Zadanie 6.3 [WYŚLIJ]** — Test aktywacji. W **nowej** sesji Claude Code napisz trzy prompty: dwa, które powinny wyzwolić skill, i jeden, który nie powinien. Zanotuj, czy skill się uruchomił za każdym razem. Wyślij trzy prompty i trzy wyniki.

**Zadanie 6.4 [WYŚLIJ]** — Porównanie z bazą odniesienia. Uruchom jeden ze swoich promptów pozytywnych w sesji ze skillem i w sesji bez niego (możesz tymczasowo zmienić nazwę katalogu skilla). Napisz w trzech zdaniach, co konkretnie skill zmienił w odpowiedzi.

**Zadanie 6.5 [WYŚLIJ]** — Celowo zepsuj Front Matter skilla, wstawiając niecytowany dwukropek w `description`. Uruchom `claude --debug`, znajdź komunikat o błędzie parsowania i wyślij go. Potem sprawdź, czy `/nazwa-skilla` dalej działa, i napisz jednym zdaniem, dlaczego to jest przykład cichej awarii.
