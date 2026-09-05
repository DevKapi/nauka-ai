---
modul: 5
tytul: "Markdown i Front Matter"
autor: Kacper
data: 2026-09-05
tagi:
  - markdown
  - yaml
  - front-matter
  - claude-code
status: ukonczony
---

# Moduł 5 — Markdown i Front Matter

> Ta notatka sama zaczyna się od Front Mattera — blok powyżej to praktyczny przykład tego,
> o czym jest cały moduł. GitHub wyrenderuje go jako tabelkę metadanych nad treścią.

---

## 1. Po co był ten moduł

Markdown i Front Matter wyglądają jak temat kosmetyczny. Nie są. To **format wejściowy
całego ekosystemu narzędzi AI**: pliki `CLAUDE.md`, skille, slash commands i definicje
subagentów to fizycznie pliki `.md` z blokiem YAML na górze.

Bez zrozumienia tego modułu w Module 6 (Skills) kopiowałbym składnię, nie wiedząc,
dlaczego coś działa albo dlaczego nie działa.

---

## 2. Słownik pojęć

| Pojęcie | Wyjaśnienie własnymi słowami |
|---|---|
| **Markup language** | Język znaczników — sposób zapisania formatowania *wewnątrz* zwykłego tekstu. Znaki takie jak `#` czy `**` nie są ozdobą, tylko poleceniem dla programu. |
| **Markdown** | Konkretny markup language. Plik `.md` to zwykły tekst — nie ma w nim ukrytego formatowania jak w `.docx`. |
| **Renderer** | Program, który zamienia znaki Markdown na wygląd (GitHub, VS Code, podgląd w edytorze). `cat` **nie** renderuje — pokazuje surowe znaki. |
| **YAML** | Format zapisu **danych** (nie tekstu do czytania). Odpowiada na pytanie „jakie są właściwości tego obiektu". |
| **Parser** | Program czytający plik i zamieniający go na strukturę danych. To on decyduje o typach i on zgłasza błędy składni. |
| **Front Matter** | Blok YAML na samym początku pliku Markdown, odgrodzony liniami `---`. Metadane *o* dokumencie. |
| **Body** | Wszystko po zamykającym `---`. Właściwa treść dokumentu. |
| **Metadane** | Dane o danych. Nie treść, tylko informacje o niej: autor, data, priorytet, tagi. |
| **Progressive disclosure** | Stopniowe odsłanianie. Agent czyta najpierw same metadane wszystkich skilli, a pełną treść wczytuje tylko dla tego, którego faktycznie potrzebuje. |
| **Slash command** | Plik `.md` w `.claude/commands/`, uruchamiany w sesji Claude Code przez `/nazwa`. Nazwa komendy = nazwa pliku. |
| **Heredoc** | Sposób wpisania wielolinijkowego tekstu prosto do pliku z poziomu terminala: `cat > plik << 'EOF' ... EOF`. |
| **Command substitution** | Mechanizm „uruchom komendę i wstaw jej wynik w to miejsce". W bashu — backticki. W slash commandzie — `` !`komenda` ``. |
| **Flow style** | Skrócony zapis listy w YAML w nawiasach kwadratowych: `[a, b, c]`. Równoważny liście z myślnikami. |
| **Block scalar** | Tekst wielolinijkowy w YAML. `\|` zachowuje łamania linii, `>` skleja je w jeden akapit. |
| **BOM** | *Byte Order Mark* — niewidzialny znak wstawiany przez niektóre edytory Windows na początek pliku. Psuje Front Matter, bo `---` przestaje być w kolumnie 1. |
| **Traceback** | Ślad wywołań w błędzie Pythona. Czyta się **od dołu** — tam jest typ błędu, opis i lokalizacja. |
| **Cicha awaria** | Awaria bez komunikatu o błędzie. Program działa, ale inaczej, niż zakładasz. |

---

## 3. Markdown vs YAML vs Front Matter — czym się różnią

To pytanie prawie na pewno padnie na teście. Rozróżnienie:

| | Markdown | YAML | Front Matter |
|---|---|---|---|
| **Co opisuje** | jak ma wyglądać treść | jakie są właściwości obiektu | właściwości *dokumentu* |
| **Dla kogo** | dla człowieka do czytania | dla programu do przetworzenia | dla programu |
| **Odpowiada na pytanie** | „jak to wyświetlić?" | „jakie to ma dane?" | „czym jest ten plik?" |
| **Przykład** | `## Nagłówek` | `priority: critical` | blok `---` na górze pliku |
| **Czy to osobny język?** | tak | tak | **nie** |

Kluczowe zdanie do zapamiętania:

> **Front Matter to nie jest osobny język. To blok YAML wklejony na początek pliku Markdown.**

Czyli hierarchia jest taka:

```
plik .md
├── Front Matter  ← napisany w YAML
└── body          ← napisany w Markdown
```

Wniosek praktyczny: **żeby napisać Front Matter, trzeba umieć YAML.** Wszystkie pułapki
YAML-a (dwukropki, tabulatory, zgadywanie typów) obowiązują wewnątrz Front Mattera
w stu procentach.

### Ta sama składnia, dwa znaczenia

| Zapis | Gdzie | Znaczenie |
|---|---|---|
| `---` | pierwsza linia pliku | otwiera Front Matter |
| `---` | w środku pliku | linia pozioma (Markdown) |

Decyduje **pozycja**, nie sam znak.

---

## 4. Markdown — składnia

### Podstawy

```markdown
# Nagłówek 1        (jeden na dokument)
## Nagłówek 2
### Nagłówek 3

*kursywa*  **pogrubienie**  `kod inline`

- lista punktowana
  - zagnieżdżona (2 spacje)

1. lista numerowana
2. drugi punkt

[tekst linku](https://adres.pl)
[link względny](notatki/modul-04.md)

> cytat blokowy

---                 (linia pozioma)
```

Blok kodu — trzy backticki plus nazwa języka:

    ```bash
    git status
    ```

Nazwa języka (`bash`, `python`, `yaml`) włącza kolorowanie, ale ważniejsze jest, że
**dla agenta AI to informacja o tym, czym jest zawartość bloku**.

Tabela — linia z myślnikami jest obowiązkowa:

```markdown
| Komenda | Opis |
|---------|------|
| `pwd`   | pokazuje katalog |
```

### Trzy pułapki Markdown

**1. Brak pustej linii przed listą.** Lista przyklejona do akapitu może się nie
wyrenderować. Zasada ogólna: **bloki oddzielaj pustą linią**.

**2. Pojedynczy Enter nie robi nowej linii.** Dwie linie pod sobą zlepią się w jeden
akapit. Nowy akapit = pusta linia.

**3. Brak spacji po znaku.** `#Nagłówek` i `-punkt` nie zadziałają. Musi być `# Nagłówek`
i `- punkt`.

---

## 5. YAML — składnia

```yaml
nazwa: raport-regresji        # tekst (string)
liczba_testow: 42             # int
czas_minuty: 12.5             # float
zakonczony: true              # bool
autor: null                   # brak wartości

tagi:                         # lista
  - regresja
  - smoke

tagi: [regresja, smoke]       # ta sama lista, flow style

srodowisko:                   # zagnieżdżenie
  system: Ubuntu
  narzedzia:
    - git
    - claude-code

opis: |                       # zachowuje łamania linii
  Pierwsza linia.
  Druga linia.

opis: >                       # skleja w jeden akapit
  Te linie
  połączą się.
```

Reguły twarde:

- **spacja po dwukropku jest obowiązkowa** (`name:wartosc` to błąd)
- **wcięcia tylko spacjami** — tabulator jest w YAML zakazany przez specyfikację
- standard to 2 spacje na poziom
- `#` rozpoczyna komentarz

### Cztery pułapki YAML

| Problem | Zły zapis | Poprawnie |
|---|---|---|
| Dwukropek w wartości | `tytul: Raport: wyniki` | `tytul: "Raport: wyniki"` |
| „Problem Norwegii" | `kraj: NO` → *false* | `kraj: "NO"` |
| Wersja jako liczba | `wersja: 1.10` → *1.1* | `wersja: "1.10"` |
| Tabulator | `\timie: Kacper` | dwie spacje |
| Nawiasy = lista | `argument-hint: [nazwa]` → lista | `argument-hint: "[nazwa]"` |

**Zasada ogólna: jeśli wartość zawiera `:`, `#`, `[`, `]`, `{`, `}` albo zaczyna się od
`-` — bierz ją w cudzysłów.**

Ostatni wiersz tabeli to błąd, który sam wykryłem w tym module: `[nazwa-modulu]` bez
cudzysłowu parser odczytał jako jednoelementową listę, a nie tekst.

### Jak odróżnić listę od tekstu w wyniku parsera

```
argument-hint = ['nazwa-modulu']   ← nawiasy na zewnątrz = lista
argument-hint = '[nazwa-modulu]'   ← apostrofy na zewnątrz = tekst
```

---

## 6. Front Matter — cztery reguły

1. Otwierające `---` musi być w **linii 1, kolumnie 1**. Nie po pustej linii, nie po komentarzu.
2. `---` musi stać **samo w linii**, bez spacji i bez niczego po nim.
3. Między znacznikami obowiązuje **YAML** ze wszystkimi jego regułami.
4. Musi istnieć **domykające `---`**.

### Przykład

```markdown
---
id: TC-001
title: "Logowanie: poprawne dane"
priority: critical
automated: true
tags: [logowanie, smoke]
---

# TC-001 Logowanie poprawnymi danymi

Kroki testowe...
```

### Nie ma jednego standardu pól

Każde narzędzie definiuje własny zestaw:

| Narzędzie | Typowe pola |
|---|---|
| Jekyll / Hugo | `layout`, `permalink`, `draft` |
| Obsidian | `tags`, `aliases` |
| Claude Code — skill | `name`, `description` |
| Claude Code — slash command | `description`, `argument-hint`, `allowed-tools`, `model` |

**Front Matter to format, nie schemat.** Jeśli piszesz dla konkretnego narzędzia —
sprawdź w jego dokumentacji, czego oczekuje.

### Kiedy dodawać Front Matter

Wtedy i tylko wtedy, gdy **jakiś program ma z niego coś odczytać**. `README.md` na
GitHubie go nie potrzebuje — nikt go nie odpytuje o metadane.

---

## 7. Front Matter w narzędziach AI

### Progressive disclosure — mechanizm, nie ozdoba

Agent na starcie widzi **wyłącznie Front Matter** wszystkich dostępnych skilli. Pełną
treść pliku wczytuje dopiero wtedy, gdy uzna, że `description` pasuje do zadania.

Dlaczego to jest konieczne:

- **okno kontekstowe jest skończone** — przy 300 skillach agent fizycznie by się nie zmieścił
- koszt tokenów rośnie liniowo z każdym niepotrzebnie wczytanym plikiem
- im więcej nieistotnej treści w kontekście, tym niższa dokładność odpowiedzi

Stosunek objętości: Front Matter to kilka linii, treść skilla to często kilkaset. Agent
przegląda „katalog" narzędzi kosztem ułamka kontekstu.

**Konsekwencja praktyczna: świetny skill ze słabym `description` nigdy nie zostanie użyty.**
Zawartość nie ma znaczenia, jeśli metryczka nie przekona modelu, żeby ją otworzyć.

### Slash command — budowa

Plik `.claude/commands/nazwa.md` (poziom projektu) lub `~/.claude/commands/nazwa.md`
(poziom osobisty). **Nazwa pliku staje się nazwą komendy** — `commit.md` daje `/commit`.

```markdown
---
description: "Uruchamia testy i tworzy raport QA: status, pokrycie, ryzyka"
argument-hint: "[nazwa-modulu]"
allowed-tools: Bash(python3:*), Bash(pytest:*), Bash(git status:*), Read
model: haiku
---

## Kontekst

Stan repozytorium: !`git status --short`

## Zadanie

Uruchom testy dla modulu: $ARGUMENTS
```

| Pole | Do czego służy |
|---|---|
| `description` | opis w podpowiedziach po wpisaniu `/` |
| `argument-hint` | podpowiedź, jakich argumentów komenda oczekuje |
| `allowed-tools` | **zawęża** uprawnienia — wymienione narzędzia działają bez pytania, inne nie |
| `model` | którym modelem uruchomić (np. `haiku` dla prostych zadań = szybciej) |

Frontmatter jest **opcjonalny** — plik bez niego zadziała, tylko straci te możliwości.

### Dwa mechanizmy w body

**`` !`komenda` ``** — Claude Code uruchamia komendę **zanim wyśle prompt do modelu** i
wstawia w to miejsce jej wynik. Model nigdy nie widzi samej komendy, widzi rezultat.
Wymaga dopuszczenia w `allowed-tools`.

**`$ARGUMENTS` / `$1`, `$2`** — miejsca, w które trafiają argumenty podane po nazwie komendy.

### Skill vs slash command — różnice

| | Slash command | Skill |
|---|---|---|
| Lokalizacja | `.claude/commands/nazwa.md` | `.claude/skills/nazwa/SKILL.md` |
| Pole `name` we Front Matterze | **nie ma** — nazwa z nazwy pliku | **jest** |
| Jak uruchamiany | ręcznie przez `/nazwa` | model sam decyduje na podstawie `description` |
| Struktura | pojedynczy plik | katalog z plikiem głównym |

### Cztery częste błędy w slash commandach

| Błąd | Poprawnie |
|---|---|
| `allowed-tools: [Read, Write]` (lista) | `allowed-tools: Read, Write` (tekst) |
| `tools:` / `arguments:` | `allowed-tools:` / `argument-hint:` |
| Brak `---` przed i po | oba znaczniki obowiązkowe |
| `bash`, `grep` małą literą | `Bash`, `Grep` |

---

## 8. Komendy — co znać, a czego nie

Odpowiedź na pytanie „czy muszę pamiętać te wszystkie długie komendy": **nie**.
Dzielą się na trzy grupy.

### Grupa A — do zapamiętania, używam codziennie

| Komenda | Co robi |
|---|---|
| `cd katalog` | wejście do katalogu |
| `ls -la` | lista plików z ukrytymi |
| `cat plik` | wyświetlenie zawartości |
| `mkdir -p sciezka` | utworzenie katalogu (`-p` = bez błędu, gdy istnieje) |
| `cp zrodlo cel` | kopiowanie |
| `head -n 5 plik` | pierwsze 5 linii |
| `> plik` | zapis do pliku (nadpisuje) |
| `>> plik` | dopisanie na koniec pliku |

### Grupa B — mam wiedzieć, że istnieją i jaki problem rozwiązują

Składnię wolno sprawdzić. Ważne jest rozpoznanie sytuacji.

| Komenda | Problem, który rozwiązuje |
|---|---|
| `cat > plik << 'EOF'` | zapisanie wielolinijkowego tekstu bez otwierania edytora |
| `wc -l plik` | ile plik ma linii — kontrola, czy zapisało się wszystko |
| `grep -c '^$' plik` | ile jest pustych linii |
| `cat -A plik` | pokazuje znaki niewidoczne (`^I` = tabulator, `$` = koniec linii) |
| `xxd` | podgląd bajtów — wykrywanie BOM i niewidocznych znaków |

### Grupa C — rekwizyty dydaktyczne, w normalnej pracy nieużywane

| Komenda z modułu | Prostszy sposób |
|---|---|
| `sed -i '1d' plik` (usuń linię 1) | otwórz w `nano`, skasuj linię, `Ctrl+O`, `Ctrl+X` |
| `sed -i 's/stare/nowe/' plik` | `nano` + `Ctrl+\` (zamiana) albo VS Code |
| `printf -- '---\n\n# Tytul\n' >> plik` | `nano plik`, dopisz na końcu |
| wielolinijkowy `python3 -c "..."` | zapisz do pliku `.py` i uruchom `python3 plik.py` |
| `cat > plik << 'EOF'` | `nano plik` i wpisz normalnie |

**Dlaczego więc były używane w kursie:** komenda w terminalu jest odtwarzalna i widoczna
w historii. Mogę ją wkleić, mogę ją powtórzyć, widać dokładnie, co zostało zrobione.
Edytor tego nie daje. To zaleta **dydaktyczna i automatyzacyjna**, nie codzienna.

### Prostsze alternatywy do zapamiętania

| Zamiast | Użyj |
|---|---|
| heredoc do pisania plików | `nano plik` — prosty edytor w terminalu |
| ręcznej edycji w terminalu | `code .` — otwiera cały katalog w VS Code (działa z WSL) |
| `python3 -c` do walidacji YAML | własny skrypt `czytaj.py`, raz napisany i wielokrotnie używany |

**`nano` — minimum:** `Ctrl+O` zapisz, `Enter` potwierdź nazwę, `Ctrl+X` wyjdź,
`Ctrl+K` usuń linię.

---

## 9. Typowe błędy — z własnego doświadczenia w tym module

| Błąd | Objaw | Przyczyna |
|---|---|---|
| `<< EOF` bez apostrofów | zamiast `` `pwd` `` w pliku jest ścieżka | bash wykonał command substitution przed zapisem |
| Brak domykającego `---` | `BLAD - brak domykajacego ---` | `split('---', 2)` zwrócił 2 części zamiast 3 |
| Pusta linia przed `---` | `BRAK Front Mattera` | złamana Reguła 1 |
| `[nazwa]` bez cudzysłowu | parser zwrócił listę zamiast tekstu | nawiasy kwadratowe = flow style |
| `/claude` wpisane w bashu | `No such file or directory` | slash commands działają **wewnątrz sesji**, nie w bashu |

### Trzy warstwy — gdzie szukać winowajcy

Gdy coś nie działa, pierwsze pytanie: **która warstwa zawiodła?**

| Warstwa | Co robi | Kiedy |
|---|---|---|
| bash | interpretuje `$`, backticki, `\` | przy tworzeniu pliku |
| plik na dysku | martwe znaki, nic nie interpretuje | zawsze |
| parser YAML | zgaduje typy, waliduje składnię | przy odczycie |

Odpowiedź daje `cat`. Jeśli w pliku jest to, co chciałeś — winny parser. Jeśli nie —
zawinił bash przy zapisie.

### Jak czytać błędy

**Traceback Pythona czyta się od dołu.** Ostatnie linie to typ błędu, opis i lokalizacja:

```
yaml.scanner.ScannerError: while scanning for the next token
found character '\t' that cannot start any token
  in "zly-tab.yaml", line 2, column 1
```

Wszystko powyżej — kilkanaście linii `File "/usr/lib/python3/..."` — to historia wywołań
wewnątrz biblioteki. Do problemu wnosi zero.

Dwa komunikaty warte zapamiętania:

- `found character '\t' that cannot start any token` → tabulator w YAML
- `mapping values are not allowed here` → niezacytowany dwukropek w wartości

---

## 10. Cicha awaria — najważniejsza lekcja modułu

Eksperyment: usunięcie otwierającego `---` ze slash commanda.

**Czego się spodziewałem:** komunikatu o błędzie.
**Co się stało:** komenda dalej działała i dawała sensowny raport.

Co po cichu przestało działać:

- `model: haiku` przestał obowiązywać — komenda poszła na modelu domyślnym
- `allowed-tools` przestało obowiązywać (przed zepsuciem konsola pokazywała
  `Successfully loaded skill · 4 tools allowed`, po zepsuciu tej linii nie było)
- cały Front Matter wyciekł do promptu jako zwykły tekst — model dostał do przeczytania
  konfigurację, która miała nim sterować
- opis w podpowiedziach zastąpiła pierwsza linia body

**Żadna z tych rzeczy nie wygenerowała komunikatu o błędzie.**

### Dlaczego to jest groźniejsze niż jawny błąd

Jawny błąd składni jest **samodiagnozujący**: parser podaje plik, linię, kolumnę
i przyczynę. Naprawa to minuta. Koszt jest wysoki natychmiast i spada do zera.

Cicha awaria działa odwrotnie: koszt jest zerowy w momencie wystąpienia i rośnie
z każdym dniem, bo przez ten czas podejmuje się decyzje na podstawie fałszywego obrazu.

**Analogia z QA: test, który świeci na zielono, ale niczego nie sprawdza.** Test rzucający
wyjątek jest widoczny i ktoś go naprawi. Test z zapomnianą asercją przechodzi zawsze,
buduje fałszywe poczucie bezpieczeństwa i przepuszcza bugi na produkcję. Zauważa się go
dopiero wtedy, gdy klient zgłosi błąd w obszarze „pokrytym testami".

**Odruch zawodowy: nie pytam „czy się wywaliło", tylko „czy zweryfikowałem, że działa tak,
jak zakładam".** Stąd walidacja Front Mattera osobnym skryptem — sprawdza to, czego brak
komunikatu błędu nie sprawdzi.

---

## 11. Zastosowania praktyczne w QA

**Przypadki testowe z metadanymi.** Każdy plik `.md` z Front Matterem zawierającym `id`,
`priority`, `status`, `automated`, `tags`. Przy 300 plikach wyciągnięcie wszystkich
krytycznych to odczyt 6 pierwszych linii każdego zamiast parsowania całych dokumentów.

**Slash command do raportowania testów.** Jedna komenda `/raport-testow` zamiast
powtarzania tego samego promptu. `allowed-tools` gwarantuje, że agent nie zmodyfikuje
kodu, `model: haiku` obniża koszt rutynowego zadania.

**Walidacja metadanych w CI.** Skrypt sprawdzający, czy każdy plik przypadku testowego ma
poprawny Front Matter, może działać jako krok w pipeline. Wyłapuje cichą awarię, zanim
trafi na `main`.

**Dokumentacja testowa dla agenta AI.** Nagłówki `##` dają modelowi strukturę, bloki kodu
z nazwą języka dają kontekst, Front Matter daje odpowiedź na pytanie „czym jest ten plik".

---

## 12. Potencjalne pytania testowe

**Teoria i rozróżnienia**

1. Czym różni się Markdown od YAML? Na jakie pytanie odpowiada każdy z nich?
2. Czy Front Matter to osobny język? Uzasadnij.
3. Co oznacza `---` w pierwszej linii pliku, a co w środku?
4. Wymień cztery reguły poprawnego Front Mattera.
5. Czy Front Matter jest obowiązkowy w slash commandzie? Co się stanie bez niego?

**YAML**

6. Dlaczego `wersja: 1.10` to problem? Jak to naprawić?
7. Na czym polega „problem Norwegii"?
8. Dlaczego tabulator w YAML jest błędem, a nie kwestią stylu?
9. Czym różni się `[a, b]` od `"[a, b]"` z punktu widzenia parsera?
10. Kiedy wartość trzeba wziąć w cudzysłów?

**Claude Code**

11. Skąd Claude Code wie, jak nazywa się slash command, skoro nie ma pola `name`?
12. Czy `allowed-tools` rozszerza czy zawęża uprawnienia? Co się dzieje bez tego pola?
13. Kto i kiedy uruchamia to, co jest w `` !`komenda` ``? Czy model widzi samą komendę?
14. Wymień trzy różnice między skillem a slash commandem.
15. Wyjaśnij progressive disclosure. Co by się stało, gdyby agent wczytywał od razu całą
    treść wszystkich skilli?
16. Dlaczego świetny skill ze słabym `description` jest bezużyteczny?

**Praktyka i diagnostyka**

17. Dlaczego apostrofy w `<< 'EOF'` mają znaczenie? Co się stanie bez nich?
18. Plik wygląda poprawnie, a parser zgłasza błąd. Jak ustalić, która warstwa zawiodła?
19. Co oznacza `found character '\t' that cannot start any token`? Gdzie w komunikacie
    jest lokalizacja problemu?
20. Czym jest cicha awaria i dlaczego jest groźniejsza od jawnego błędu? Podaj analogię z QA.
21. Jak sprawdzić, czy plik ma na początku niewidoczny BOM?
22. Czym różni się `>` od `>>` przy zapisie do pliku?

---

## 13. Ściąga — komendy z modułu

```bash
# Nawigacja i pliki
mkdir -p ~/md-lab                    # utwórz katalog (bez błędu, gdy istnieje)
cat plik.md                          # wyświetl zawartość
head -n 6 plik.md                    # pierwsze 6 linii
cp zrodlo.md cel.md                  # kopia

# Zapis do pliku
echo "tekst" > plik.md               # jedna linia, nadpisuje
echo "tekst" >> plik.md              # jedna linia, dopisuje
cat > plik.md << 'EOF'               # wiele linii (apostrofy obowiązkowe!)
tresc
EOF
nano plik.md                         # prościej: zwykły edytor

# Weryfikacja
wc -l plik.md                        # liczba linii
grep -c '^$' plik.md                 # liczba pustych linii
cat -A plik.md                       # znaki niewidoczne (^I = tab)
head -c 20 plik.md | xxd             # bajty początku pliku (wykrywanie BOM)

# Walidacja YAML / Front Matter
python3 czytaj.py plik.md            # własny skrypt walidujący
python3 -c "import yaml; yaml.safe_load(open('plik.yaml'))"

# Claude Code
claude                               # start sesji (w bashu)
/raport-testow                       # uruchomienie komendy (w sesji!)
/exit                                # wyjście z sesji
```

---

## 14. Moimi słowami

<!-- Sekcja do uzupełnienia własnoręcznie na GitHubie -->
