---
title: "Moduł 5 — Markdown, YAML i Front Matter"
module: 5
author: DevKapi
tags: [markdown, yaml, front-matter, dokumentacja, qa]
status: reference
updated: 2026-09-06
---

# Moduł 5 — Markdown, YAML i Front Matter

To jest fundament pod moduły 6 i 7. Skill to plik Markdown z blokiem YAML na górze. Plugin to katalog opisany plikiem JSON, którego składnia jest podzbiorem YAML-a. Jeżeli nie rozumiesz tych trzech rzeczy dokładnie, to skille i pluginy będą dla ciebie magią, która czasem działa, a czasem nie — i nie będziesz wiedział dlaczego. Dlatego zaczynamy tutaj.

---

## CZĘŚĆ A — MARKDOWN

### Czym jest Markdown i dlaczego w ogóle istnieje

Markdown to lekki język znaczników. "Lekki" znaczy tyle, że zapisujesz formatowanie zwykłymi znakami z klawiatury, a plik dalej da się przeczytać gołym okiem, bez żadnego programu. Plik `.md` to zwykły plik tekstowy — możesz go otworzyć w Notatniku i wszystko zrozumiesz. To jest cała idea: HTML wygląda jak `<strong>ważne</strong>`, a Markdown wygląda jak `**ważne**`. Jedno i drugie da ten sam wynik po wyrenderowaniu, ale drugie czyta się jak tekst.

Powstał w 2004 roku (John Gruber), a spopularyzował go GitHub, bo README każdego repozytorium jest właśnie w Markdownie. Dzisiaj piszesz w nim dokumentację, notatki (Obsidian, Notion), issue i pull requesty na GitHubie, wpisy blogowe, a przede wszystkim — z twojej perspektywy — pliki instrukcji dla agentów AI: `SKILL.md`, `CLAUDE.md`, `README.md` pluginu, definicje agentów.

**Dlaczego to ma znaczenie dla pracy z AI.** Model językowy czyta twój plik jako tekst. Markdown nie jest "ładniejszy dla oka" — Markdown jest **strukturą semantyczną**. Kiedy piszesz `## Kroki`, model widzi wyraźną granicę sekcji i wie, że to, co pod spodem, to jedna spójna całość. Kiedy wrzucasz ten sam tekst jako jeden wielki akapit, model musi się domyślać, gdzie kończy się jedna myśl, a zaczyna druga. Dobrze ustrukturyzowany Markdown to dosłownie lepsze wyniki agenta. To jest ten sam mechanizm, co z ludźmi: instrukcja podzielona na ponumerowane kroki jest wykonywana lepiej niż ściana tekstu.

### Nagłówki

Nagłówek to linia zaczynająca się od jednego do sześciu znaków `#`, po których jest spacja.

```markdown
# Poziom 1 — tytuł dokumentu
## Poziom 2 — główna sekcja
### Poziom 3 — podsekcja
#### Poziom 4
##### Poziom 5
###### Poziom 6
```

Zasady, których warto się trzymać. Po pierwsze, **spacja po `#` jest obowiązkowa** — `#Tytuł` w wielu parserach nie zadziała i zostanie zwykłym tekstem. Po drugie, w jednym pliku powinien być **jeden nagłówek H1** — to tytuł dokumentu. Po trzecie, **nie przeskakuj poziomów** (z `#` na `###`), bo psujesz hierarchię, którą narzędzia (spis treści, nawigacja, model AI) odczytują dosłownie. Po czwarte, nagłówek to znacznik struktury, a nie sposób na powiększenie tekstu — jeżeli chcesz coś wyróżnić w środku akapitu, użyj pogrubienia.

Istnieje też stara składnia z podkreśleniem, którą spotkasz w starszych plikach i którą trzeba umieć rozpoznać:

```markdown
Tytuł poziomu 1
===============

Tytuł poziomu 2
---------------
```

Ta druga forma jest ważna z jednego powodu, który zaraz wróci przy Front Matterze: **linia złożona z myślników pod tekstem robi z tego tekstu nagłówek**. To źródło jednego z najczęstszych błędów w plikach z metadanymi.

### Akapity i łamanie linii

Akapit to blok tekstu oddzielony od innych **pustą linią**. To jest kluczowe i często zaskakuje początkujących: jeżeli napiszesz dwie linie jedna pod drugą bez pustej linii między nimi, Markdown skleji je w jeden akapit.

```markdown
To jest pierwsza linia.
To jest druga linia.
```

Wyrenderuje się jako: `To jest pierwsza linia. To jest druga linia.` — jedno zdanie ciągiem.

Jeżeli chcesz twarde złamanie linii wewnątrz jednego akapitu, masz dwie opcje: zakończyć linię **dwiema spacjami** (niewidoczne, więc źródło koszmarów przy code review) albo wstawić **pustą linię** i zrobić nowy akapit. W praktyce w dokumentacji technicznej używa się pustej linii, bo jest jawna i widoczna w diffie.

Jest jeszcze jedna praktyczna konwencja: **jedno zdanie w jednej linii źródła** (tzw. semantic line breaks). Renderuje się to i tak jako jeden akapit, ale w `git diff` widać wtedy dokładnie, które zdanie się zmieniło, zamiast całego przepakowanego bloku. Przy dokumentacji trzymanej w Gicie to bardzo ułatwia review.

### Wyróżnienia tekstu

```markdown
*kursywa* albo _kursywa_
**pogrubienie** albo __pogrubienie__
***pogrubiona kursywa***
~~przekreślenie~~
`kod w linii`
```

Rekomendacja: używaj konsekwentnie gwiazdek, nie podkreślników. Podkreślnik ma problem ze słowami typu `nazwa_zmiennej_w_kodzie` — parser może uznać środkowy fragment za kursywę i rozwalić ci nazwę. Gwiazdki są bezpieczniejsze.

Przekreślenie (`~~`) to rozszerzenie GitHub Flavored Markdown, nie ma go w oryginalnej specyfikacji — na GitHubie działa, w jakimś minimalnym parserze może nie zadziałać.

### Listy

**Lista nieuporządkowana** — myślnik, gwiazdka albo plus, potem spacja. Wybierz jeden znak i trzymaj się go w całym pliku; mieszanie znaków w niektórych parserach rozbija jedną listę na kilka osobnych.

```markdown
- pierwszy element
- drugi element
- trzeci element
```

**Lista uporządkowana** — liczba, kropka, spacja.

```markdown
1. pierwszy krok
2. drugi krok
3. trzeci krok
```

Ciekawostka, która bywa pytaniem: numeracja w źródle nie musi być poprawna. Jeżeli napiszesz `1.`, `1.`, `1.`, renderer i tak wypisze 1, 2, 3. To bywa wygodne przy długich listach, gdzie wstawiasz coś w środku — ale utrudnia czytanie surowego pliku, a model AI czyta właśnie surowy plik. Przy instrukcjach dla agenta numeruj normalnie.

**Zagnieżdżanie** — wcięcie o dwie do czterech spacji (dla list numerowanych bezpieczniej trzy albo cztery, bo wcięcie musi wypaść za znacznikiem rodzica).

```markdown
- Testy jednostkowe
  - pytest
  - unittest
- Testy API
  1. Przygotuj żądanie
  2. Wyślij
  3. Sprawdź kod odpowiedzi
```

**Lista zadań** (GitHub Flavored Markdown) — bardzo przydatna w QA, bo renderuje się jako klikalne checkboxy w issue i pull requestach:

```markdown
- [ ] Przygotować środowisko testowe
- [x] Napisać przypadki testowe
- [ ] Wykonać regresję
```

**Najczęstszy błąd z listami:** brak pustej linii przed listą, gdy poprzedza ją akapit. Część parserów wtedy wklei listę do akapitu jako zwykły tekst z myślnikami. Zasada: pusta linia przed listą i po liście.

### Bloki kodu

Kod w linii otaczasz pojedynczym grawisem: `` `git status` ``. Jeżeli sam kod zawiera grawis, otocz go podwójnym: `` `` kod z ` w środku `` ``.

Blok kodu otaczasz trzema grawisami, a **zaraz po otwierających grawisach podajesz nazwę języka**:

````markdown
```bash
git status
git add .
```
````

Podanie języka nie jest ozdobnikiem. Po pierwsze daje kolorowanie składni. Po drugie — i to ważniejsze przy AI — mówi modelowi jednoznacznie, czym jest zawartość bloku. Blok oznaczony `bash` to komendy do wykonania; blok oznaczony `text` to przykładowy output, którego nie należy uruchamiać. Ta różnica realnie zmienia zachowanie agenta.

Typowe oznaczenia, których będziesz używał: `bash`, `python`, `json`, `yaml`, `markdown`, `text`, `diff`.

Jeżeli musisz pokazać blok kodu **wewnątrz** bloku kodu (a będziesz musiał, bo dokumentujesz pliki Markdown), użyj czterech grawisów na zewnątrz i trzech w środku. Dokładnie tak, jak w przykładzie powyżej.

Istnieje też stara składnia bloku kodu przez wcięcie czterema spacjami. Rozpoznawaj ją, ale nie używaj — jest mniej czytelna i nie pozwala oznaczyć języka.

### Cytaty

```markdown
> To jest cytat.
> Druga linia cytatu.
>
> > A to cytat zagnieżdżony.
```

W dokumentacji technicznej cytat wykorzystuje się głównie jako "callout" — wyróżniony blok z ostrzeżeniem albo uwagą:

```markdown
> **Uwaga:** ta komenda nadpisuje historię zdalnego repozytorium.
```

### Linki i obrazki

```markdown
[tekst linku](https://example.com)
[tekst z tooltipem](https://example.com "Podpowiedź po najechaniu")
[link do pliku w repo](./docs/instalacja.md)
[link do sekcji w tym pliku](#czesc-a--markdown)
```

Obrazek to to samo z wykrzyknikiem z przodu; tekst w nawiasach kwadratowych staje się tekstem alternatywnym:

```markdown
![Zrzut ekranu z panelu logowania](./img/logowanie.png)
```

Linki referencyjne przydają się, gdy ten sam adres powtarza się wielokrotnie albo gdy długie URL-e rozwalają czytelność akapitu:

```markdown
Zobacz [dokumentację Claude Code][cc-docs] oraz [specyfikację skilli][skills].

[cc-docs]: https://code.claude.com/docs/en/overview
[skills]: https://agentskills.io
```

Definicje odnośników mogą stać na końcu pliku, nie renderują się.

Autolink to po prostu adres w ostrych nawiasach: `<https://example.com>`.

**Linkowanie do sekcji** działa tak, że nagłówek zamieniany jest na "anchor": małe litery, spacje na myślniki, znaki specjalne usunięte. Nagłówek `## Typowe błędy` daje `#typowe-błędy`. To bywa niestabilne przy polskich znakach — jeżeli linkujesz do sekcji, sprawdź to na GitHubie po wypchnięciu.

### Tabele

Tabele to rozszerzenie GFM. Składnia jest prosta: pierwsza linia to nagłówki, druga to separator z myślnikami, dalej wiersze.

```markdown
| Komenda | Co robi | Kiedy używam |
|---------|---------|--------------|
| `git status` | Pokazuje stan drzewa roboczego | Zawsze przed commitem |
| `git diff` | Pokazuje niezacommitowane zmiany | Przed `git add` |
| `git log --oneline` | Skrócona historia | Przy szukaniu commita |
```

Wyrównanie kolumny ustawia się dwukropkami w linii separatora: `:---` do lewej, `:---:` do środka, `---:` do prawej.

Pionowe kreski na początku i końcu wiersza są opcjonalne, ale zostawiaj je — plik jest wtedy czytelniejszy w źródle. Kolumny **nie muszą** być wyrównane spacjami w źródle, żeby tabela zadziałała, ale surowy plik czyta się wtedy fatalnie.

Ograniczenie, o którym trzeba wiedzieć: w komórce tabeli nie zrobisz bloku kodu ani wielolinijkowego tekstu. Jeżeli tego potrzebujesz, tabela jest złym narzędziem — użyj nagłówków i akapitów.

Jeżeli musisz wstawić do komórki znak `|`, escape'uj go: `\|`.

### Linia pozioma

```markdown
---
***
___
```

Trzy albo więcej myślników, gwiazdek albo podkreślników w osobnej linii. **I tutaj zaczyna się najważniejsza pułapka całego tego modułu.** Trzy myślniki na początku pliku to nie linia pozioma — to otwarcie Front Mattera. Trzy myślniki bezpośrednio pod linią tekstu to nie linia pozioma — to zamiana tej linii w nagłówek H2. Zapamiętaj: `---` znaczy trzy zupełnie różne rzeczy w zależności od tego, gdzie stoi.

### Znaki specjalne i escapowanie

Jeżeli chcesz pokazać znak, który Markdown traktuje jako składnię, poprzedź go backslashem:

```markdown
\*to nie jest kursywa\*
\# to nie jest nagłówek
100\% ukończenia
```

Znaki, które można escape'ować: `` \ ` * _ { } [ ] ( ) # + - . ! | ``

### HTML wewnątrz Markdowna

Większość parserów pozwala wstawić surowy HTML. Najużyteczniejszy przypadek w dokumentacji to zwijana sekcja:

```markdown
<details>
<summary>Pełny log błędu (kliknij, żeby rozwinąć)</summary>

```text
Traceback (most recent call last):
  ...
```

</details>
```

To ratuje czytelność raportów z testów, gdzie masz stustronicowy log. Uwaga: po otwierającym tagu HTML dawaj pustą linię, inaczej Markdown w środku może się nie wyrenderować.

### GitHub Flavored Markdown — co dokładnie jest rozszerzeniem

Warto wiedzieć, co jest w oryginalnej specyfikacji, a co dołożył GitHub, bo nie każde narzędzie obsługuje rozszerzenia. Rozszerzenia GFM to: tabele, przekreślenie `~~`, listy zadań `- [ ]`, automatyczne linkowanie gołych URL-i, przypisy `[^1]`, oraz podświetlanie składni po nazwie języka. Reszta — nagłówki, listy, cytaty, kod, linki, wyróżnienia — jest w każdym parserze.

### Typowe błędy w Markdownie

Brak pustej linii przed listą albo przed tabelą — element renderuje się jako zwykły tekst. Brak spacji po `#` — nagłówek się nie tworzy. Mieszanie tabulatorów i spacji przy wcięciach — zagnieżdżenie się rozjeżdża, bo różne parsery liczą tab jako różną liczbę spacji. Blok kodu bez języka — tracisz kolorowanie i jednoznaczność dla modelu. Niezamknięty blok kodu — reszta pliku wsiąka w blok i przestaje się formatować, co jest jednym z tych błędów, które widać dopiero po wyrenderowaniu. Podkreślniki w nazwach zmiennych bez otoczenia grawisami — parser robi kursywę w środku nazwy. Nagłówki użyte jako stylizacja zamiast struktury — psuje spis treści i nawigację.

### Praktyczny przykład — notatka QA w Markdownie

```markdown
# Raport z regresji — release 2.4.0

**Data:** 2026-09-06
**Środowisko:** staging
**Wykonał:** Kacper

## Zakres

Regresja modułu zamówień po zmianie logiki rabatów.

## Wyniki

| Zestaw | Przypadków | Zaliczone | Niezaliczone |
|--------|-----------:|----------:|-------------:|
| Zamówienia | 42 | 40 | 2 |
| Rabaty | 18 | 18 | 0 |

## Niezaliczone przypadki

### TC-118 — rabat 100% na zamówieniu zerowym

- [x] Odtworzone na staging
- [ ] Zgłoszone do dev

Kroki:

1. Utwórz zamówienie o wartości 0.00
2. Zastosuj kupon `FULL100`
3. Zatwierdź

Oczekiwane: błąd walidacji.
Otrzymane: wyjątek `ZeroDivisionError`.

<details>
<summary>Stacktrace</summary>

```text
File "discount.py", line 41, in apply
    return total / base
ZeroDivisionError: division by zero
```

</details>
```

---

## CZĘŚĆ B — YAML

### Czym jest YAML

YAML to format zapisu **danych** — konfiguracji, ustawień, metadanych. Nazwa to żartobliwy skrót "YAML Ain't Markup Language", czyli "YAML to nie jest język znaczników" — dokładnie po to, żeby odróżnić go od HTML-a i XML-a. To nie jest język do pisania tekstu, tylko do opisywania struktury: co jest czym, co zawiera co.

Porównaj to samo w trzech formatach:

```json
{"name": "bug-report", "tools": ["Read", "Write"], "active": true}
```

```yaml
name: bug-report
tools:
  - Read
  - Write
active: true
```

XML pominę, ale idea jest ta sama. YAML wygrywa czytelnością, dlatego wszędzie, gdzie konfigurację czyta i pisze człowiek, dominuje YAML: GitHub Actions, Docker Compose, Kubernetes, Ansible, OpenAPI, i — co najważniejsze dla ciebie — Front Matter w plikach Markdown, czyli nagłówki skilli i agentów.

Kluczowa cecha: **YAML jest wrażliwy na wcięcia**. Struktura wynika z tego, jak głęboko coś jest wcięte. To jest jednocześnie jego zaleta (czytelność) i największe źródło błędów.

### Podstawowa jednostka — para klucz i wartość

```yaml
name: bug-report
version: 1.2.0
```

Dwukropek, **spacja**, wartość. Spacja po dwukropku jest obowiązkowa. `name:bug-report` bez spacji zostanie odczytane jako jeden string `name:bug-report` będący kluczem bez wartości albo wywali błąd, zależnie od parsera.

### Wcięcia

Wcinamy **wyłącznie spacjami**. Tabulator jest w YAML-u zakazany i powoduje twardy błąd parsowania. To jest najczęstsza przyczyna komunikatu "found character that cannot start any token". Konwencja to **dwie spacje** na poziom. Ważne jest, żeby w jednym pliku poziomy były konsekwentne — YAML nie wymaga akurat dwóch spacji, ale wymaga, żeby elementy tego samego poziomu miały identyczne wcięcie.

Praktyczna rada dla twojego środowiska: ustaw w edytorze "insert spaces instead of tabs" i włącz pokazywanie białych znaków, kiedy debugujesz YAML. Połowa problemów znika.

### Zagnieżdżanie — mapy

Mapa (słownik, obiekt) to zbiór par klucz-wartość. Zagnieżdżenie robisz przez wcięcie:

```yaml
author:
  name: Kacper
  email: kacper@example.com
  social:
    github: DevKapi
```

Czytasz to tak: klucz `author` ma jako wartość mapę z kluczami `name`, `email` i `social`; a `social` ma jako wartość kolejną mapę. Zauważ, że po `author:` nie ma nic w tej samej linii — wartość jest "pod spodem", wcięta.

### Listy (sekwencje)

Element listy to myślnik, spacja, wartość:

```yaml
tags:
  - markdown
  - yaml
  - qa
```

Wcięcie myślników względem klucza jest opcjonalne — poniższe jest równie poprawne i spotkasz oba warianty:

```yaml
tags:
- markdown
- yaml
```

Wybierz jeden styl i się go trzymaj.

### Lista map — najczęstsza struktura w prawdziwych konfiguracjach

To jest wzorzec, który zobaczysz w GitHub Actions, w konfiguracji hooków, wszędzie. Myślnik zaczyna element listy, a to, co po nim, jest mapą:

```yaml
testy:
  - nazwa: logowanie
    priorytet: wysoki
    automatyczny: true
  - nazwa: wylogowanie
    priorytet: niski
    automatyczny: false
```

Kluczowa rzecz do zrozumienia: `nazwa` i `priorytet` należą do **tego samego** elementu listy, bo są wyrównane do tej samej kolumny co `nazwa` po myślniku. Gdyby `priorytet` był wcięty inaczej, dostałbyś albo błąd, albo zupełnie inną strukturę. To jest miejsce, gdzie ludzie najczęściej się gubią.

### Typy danych

YAML sam zgaduje typ wartości na podstawie tego, jak wygląda.

```yaml
tekst: Kacper                # string
tekst_w_cudzyslowie: "Kacper"  # też string
liczba: 42                   # integer
zmiennoprzecinkowa: 3.14     # float
prawda: true                 # boolean
falsz: false                 # boolean
nic: null                    # null
tez_nic:                     # pusta wartość = null
tylda: ~                     # też null
data: 2026-09-06             # data (w YAML 1.1/1.2 rozpoznawana jako timestamp)
```

To automatyczne zgadywanie typu jest wygodne i jednocześnie jest źródłem najbrzydszych pułapek, do których zaraz dojdziemy.

### Cudzysłowy

String nie wymaga cudzysłowów, ale czasem ich potrzebuje. Reguły:

**Bez cudzysłowów** — domyślnie, gdy wartość nie zawiera znaków specjalnych.

**Pojedyncze cudzysłowy** — wartość jest brana dosłownie, nic w środku nie jest interpretowane. Żeby wstawić apostrof, podwajasz go: `'It''s fine'`.

**Podwójne cudzysłowy** — działają sekwencje escape jak `\n` (nowa linia), `\t` (tabulator), `\"`. Jeżeli potrzebujesz znaku nowej linii w wartości, musisz użyć podwójnych.

Kiedy cudzysłowy są **konieczne**: gdy wartość zawiera dwukropek ze spacją (`Uwaga: to jest ważne` bez cudzysłowów zostanie odczytane jako zagnieżdżona mapa i wywali błąd), gdy zaczyna się od znaku specjalnego (`@`, `` ` ``, `%`, `&`, `*`, `!`, `#`, `-` na początku), gdy chcesz, żeby coś wyglądającego na liczbę albo boolean pozostało stringiem (`wersja: "1.0"` zamiast `1.0`, `kod: "0123"` zamiast `0123`).

Ten pierwszy przypadek — dwukropek w tekście — jest **najczęstszym błędem w Front Matterze skilli**, bo opisy naturalnie zawierają dwukropki.

```yaml
# ŹLE — parser zobaczy tu zagnieżdżoną mapę i się wywali
description: Skill do raportów: generuje bug reporty z logów

# DOBRZE
description: "Skill do raportów: generuje bug reporty z logów"
```

### Bloki wielolinijkowe

Kiedy wartość ma być dłuższym tekstem, masz dwa operatory.

**Pionowa kreska `|` — literal block.** Zachowuje znaki nowej linii dokładnie tak, jak je napisałeś.

```yaml
opis: |
  Pierwsza linia.
  Druga linia.
  Trzecia linia.
```

Wartość to dosłownie `Pierwsza linia.\nDruga linia.\nTrzecia linia.\n`.

**Znak większości `>` — folded block.** Skleja linie w jeden akapit, zamieniając pojedyncze złamania linii na spacje. Pusta linia w środku daje prawdziwe złamanie akapitu.

```yaml
opis: >
  Ten tekst
  zostanie sklejony
  w jedną linię.
```

Wartość to `Ten tekst zostanie sklejony w jedną linię.\n`.

**Kontrola końcowej nowej linii (chomping).** Domyślnie na końcu zostaje jedna nowa linia. Dodanie minusa (`|-` albo `>-`) usuwa ją całkowicie. Dodanie plusa (`|+`) zachowuje wszystkie końcowe puste linie. W praktyce najczęściej używa się `|-`, gdy chcesz czysty tekst bez śmieci na końcu.

Ważne: cały blok musi być wcięty względem klucza, i to wcięcie jest odcinane od wartości. Nadmiarowe wcięcie w środku bloku **zostaje** w wartości — dzięki temu możesz w bloku `|` trzymać kod z zachowanymi wcięciami.

### Komentarze

Znak `#` i wszystko za nim do końca linii jest ignorowane.

```yaml
# To jest komentarz na całą linię
name: bug-report  # to jest komentarz na końcu linii
```

Uwaga: `#` robi komentarz tylko wtedy, gdy stoi na początku linii albo jest poprzedzony spacją. `kolor: #FF0000` — tutaj `#FF0000` zostanie potraktowane jako komentarz i wartość będzie pusta. Trzeba napisać `kolor: "#FF0000"`.

### Dokumenty w jednym pliku

Trzy myślniki `---` rozdzielają dokumenty w jednym pliku YAML, a trzy kropki `...` opcjonalnie kończą dokument.

```yaml
---
srodowisko: dev
---
srodowisko: prod
...
```

**I to jest dokładnie ten mechanizm, na którym zbudowany jest Front Matter.** Blok między `---` a `---` na początku pliku Markdown to po prostu osobny dokument YAML doklejony przed treścią.

### Kotwice i aliasy

Zaawansowane, ale spotkasz to w konfiguracjach CI i warto rozpoznawać. Kotwica `&nazwa` zapamiętuje fragment, alias `*nazwa` go wkleja, a `<<:` scala mapę.

```yaml
domyslne: &domyslne
  timeout: 30
  retry: 3

test_api:
  <<: *domyslne
  endpoint: /api/v1

test_web:
  <<: *domyslne
  timeout: 60      # nadpisuje wartość z domyślnych
```

### JSON jest poprawnym YAML-em

To nie ciekawostka, tylko praktyczna informacja: YAML 1.2 jest nadzbiorem JSON-a. Każdy poprawny JSON jest poprawnym YAML-em. Dlatego możesz pisać w YAML-u tzw. flow style:

```yaml
tags: [markdown, yaml, qa]
author: {name: Kacper, github: DevKapi}
```

To jest dokładnie to samo, co wersja blokowa z myślnikami i wcięciami. Flow style przydaje się do krótkich list — i właśnie tak najczęściej zapisuje się `tags` albo `aliases` we Front Matterze.

I dlatego `plugin.json` z modułu 7, mimo że jest JSON-em, rządzi się bardzo podobną logiką struktury: mapy, listy, wartości.

### Pułapki YAML-a, o które można zapytać na teście

**Problem norweski.** W YAML 1.1 wartości `yes`, `no`, `on`, `off`, `true`, `false`, `y`, `n` są booleanami. Więc:

```yaml
kraj: NO      # to jest false, a nie kod Norwegii!
```

Rozwiązanie: cudzysłowy. `kraj: "NO"`. To jest legendarny błąd i klasyczne pytanie rekrutacyjne.

**Wersje YAML.** YAML 1.2 zawęził to do samych `true`/`false`, ale mnóstwo bibliotek dalej pracuje w trybie 1.1. Nie zakładaj — testuj.

**Wiodące zera.** `kod: 0123` w YAML 1.1 zostanie zinterpretowane jako liczba ósemkowa i wyjdzie 83. Numery telefonów, kody pocztowe, wersje — zawsze w cudzysłowie.

**Coś, co wygląda jak liczba.** `wersja: 1.0` to float, więc `1.0` — a `wersja: 1.0.0` to string, bo dwie kropki nie tworzą liczby. Niespójność, która potrafi zaskoczyć. Wersje zawsze w cudzysłowie.

**Duplikaty kluczy.** Ten sam klucz dwa razy w jednej mapie — część parserów po cichu bierze ostatnią wartość, część rzuca błędem. Nigdy się na tym nie opieraj.

**Puste wartości.** `klucz:` bez niczego to `null`, a nie pusty string. Jeżeli chcesz pusty string, napisz `klucz: ""`.

**Białe znaki na końcu linii.** Zwykle nieszkodliwe, ale w blokach `|` trafiają do wartości.

### Walidacja YAML-a — jak sprawdzić, że plik jest poprawny

To jest odruch QA, który masz wyrobić: nie zakładaj, że plik jest poprawny — sprawdź.

Najprostszy sposób w Pythonie, jeżeli masz PyYAML:

```bash
python3 -c "import yaml, sys; print(yaml.safe_load(open('plik.yaml')))"
```

Jeżeli plik jest poprawny, dostaniesz wypisaną strukturę Pythona (słowniki i listy). Jeżeli nie — dostaniesz wyjątek z numerem linii. To drugie jest cenniejsze, bo mówi ci dokładnie gdzie.

Ważne: **zawsze `safe_load`, nigdy `load`**. `yaml.load` bez wskazania loadera potrafi wykonać dowolny kod z pliku — to znana klasa podatności. `safe_load` czyta tylko dane.

Dedykowany linter:

```bash
pip install yamllint
yamllint plik.yaml
```

`yamllint` sprawdza nie tylko poprawność składni, ale też styl: długość linii, spójność wcięć, białe znaki na końcu, duplikaty kluczy.

Sprawdzenie samego Front Mattera z pliku Markdown (przyda się w module 6):

```bash
sed -n '/^---$/,/^---$/p' SKILL.md | sed '1d;$d' | python3 -c "import yaml,sys; print(yaml.safe_load(sys.stdin))"
```

To wycina blok między pierwszymi dwoma `---`, usuwa same delimitery i przepuszcza resztę przez parser.

---

## CZĘŚĆ C — FRONT MATTER

### Czym jest Front Matter

Front Matter to blok **metadanych** umieszczony na samym początku pliku, oddzielony od reszty pliku separatorami. Metadane to dane o danych — nie treść dokumentu, tylko informacje o dokumencie: kto go napisał, kiedy, jak się nazywa, jakich tagów dotyczy, czy jest opublikowany.

```markdown
---
title: Jak konfigurować środowisko testowe
author: Kacper
date: 2026-09-06
tags: [qa, setup]
draft: false
---

# Jak konfigurować środowisko testowe

Właściwa treść dokumentu zaczyna się tutaj.
```

Wszystko między pierwszym `---` a drugim `---` to Front Matter, zapisany w YAML-u. Wszystko poniżej to treść w Markdownie.

### Po co to w ogóle jest

Trzy powody, wszystkie praktyczne.

**Po pierwsze, oddzielenie metadanych od treści.** Data publikacji nie jest częścią artykułu, ale jest potrzebna. Gdyby ją wpisać w treść, trzeba by ją stamtąd wyłuskiwać parsowaniem tekstu. Front Matter daje jej jasne, ustrukturyzowane miejsce.

**Po drugie, maszyny mogą przeczytać metadane bez czytania treści.** Generator strony może przeczytać sam nagłówek z tysiąca plików i zbudować z tego listę artykułów, indeks tagów, sortowanie po dacie — nie zaglądając w treść. To jest szybkie i tanie.

**Po trzecie — i to jest kluczowe dla modułu 6 — w narzędziach AI Front Matter jest mechanizmem oszczędzania kontekstu.** Claude Code ładuje do kontekstu sesji tylko `name` i `description` każdego skilla. Pełna treść `SKILL.md` wchodzi do kontekstu dopiero wtedy, gdy skill zostanie faktycznie użyty. Dzięki temu możesz mieć pięćdziesiąt skilli i płacić za nie kilkaset tokenów zamiast kilkudziesięciu tysięcy. Front Matter to jest "wizytówka" pliku, po której model decyduje, czy w ogóle warto go otwierać. Ten mechanizm nazywa się progressive disclosure i wrócimy do niego w module 6.

### Skąd się wziął

Z Jekylla — generatora statycznych stron, na którym stoi GitHub Pages. Stamtąd konwencja rozlała się na Hugo, Astro, Next.js, Gatsby, Eleventy, Obsidian, Zettlr, Pandoc, a ostatnio na formaty instrukcji dla agentów AI. Dzięki temu jest to dziś de facto standard: jeśli widzisz `.md` z blokiem `---` na górze, wiesz czego się spodziewać.

### Składnia — dokładnie

Cztery reguły, każda ważna.

**Reguła pierwsza: otwierające `---` musi być pierwszą linią pliku.** Nie druga, nie po pustej linii, nie po komentarzu. Pierwszy znak pliku to pierwszy myślnik. Claude Code parsuje Front Matter tylko wtedy, gdy otwierające `---` jest pierwszą linią; w przeciwnym razie traktuje **cały plik razem z myślnikami** jako treść skilla.

**Reguła druga: `---` stoi samotnie w linii.** Nic przed, nic po, żadnych spacji.

**Reguła trzecia: zawartość między delimiterami to poprawny YAML.** Wszystkie zasady z części B obowiązują: spacje zamiast tabów, spacja po dwukropku, cudzysłowy tam, gdzie trzeba.

**Reguła czwarta: musi być zamykające `---`.** Bez niego parser nie wie, gdzie kończą się metadane.

Po zamykającym `---` zwyczajowo daje się pustą linię i zaczyna treść.

### Warianty składni

YAML jest domyślny i jedyny, który interesuje cię w kontekście Claude Code. Dla porządku warto jednak wiedzieć, że istnieją dwa inne, bo spotkasz je w cudzych projektach.

TOML Front Matter, używany głównie w Hugo, oddzielany trzema plusami:

```toml
+++
title = "Tytuł"
date = 2026-09-06
+++
```

JSON Front Matter, rzadki, oddzielany klamrami:

```json
{
  "title": "Tytuł"
}
```

### Jak czytać istniejący Front Matter

Kiedy otwierasz cudzy plik, zadaj sobie trzy pytania po kolei.

**Pytanie pierwsze: jakie narzędzie to czyta?** To samo pole `description` w Jekyllu robi meta-opis strony, a w `SKILL.md` decyduje o tym, kiedy Claude uruchomi skill. Klucze nie mają uniwersalnego znaczenia — znaczenie nadaje im narzędzie. Nie ma "standardowego Front Mattera"; jest Front Matter Jekylla, Hugo, Obsidiana, Claude Code.

**Pytanie drugie: które pola są wymagane, a które opcjonalne?** Znajdziesz to w dokumentacji narzędzia. Ważne: pole, którego narzędzie nie zna, jest zwykle po prostu ignorowane — nie wywala błędu. To ma jedną paskudną konsekwencję: **literówka w nazwie pola nie daje błędu, tylko ciche pominięcie**. `descripton` zamiast `description` to skill bez opisu, który nigdy się nie uruchomi automatycznie, a Claude Code nie powie ci ani słowa.

**Pytanie trzecie: jakie są typy wartości?** Czy `tags` to string, czy lista? Czy `draft` to boolean, czy string `"false"`? To decyduje, czy filtrowanie zadziała.

Praktycznie, żeby zobaczyć sam Front Matter pliku:

```bash
head -20 SKILL.md
```

albo precyzyjniej, sam blok metadanych:

```bash
awk '/^---$/{n++} n==1' SKILL.md
```

### Jak pisać własny Front Matter

Trzymaj się czterech zasad.

**Tylko pola, które ktoś czyta.** Metadane, których żadne narzędzie nie używa i żaden człowiek nie czyta, to śmieci, które trzeba utrzymywać.

**Nazwy pól spójne w całym projekcie.** Jeżeli w jednym pliku masz `author`, a w drugim `autor`, żaden filtr nie zadziała na obu.

**Cudzysłowy wszędzie tam, gdzie wartość może być błędnie zinterpretowana.** Dwukropki w tekście, wartości zaczynające się od znaku specjalnego, wersje, kody, `NO`/`ON`/`OFF`.

**Wartości krótkie, ale konkretne.** Zwłaszcza `description` w skillach — to jedno pole decyduje o tym, czy narzędzie w ogóle zostanie użyte.

### Przykłady, przypadek po przypadku

**Wpis blogowy (Jekyll/Hugo):**

```markdown
---
title: "Jak testować API bez środowiska stagingowego"
date: 2026-09-06
author: Kacper
tags: [qa, api, testing]
categories: [praktyka]
draft: false
description: "Krótki poradnik o mockowaniu zależności w testach integracyjnych."
permalink: /testowanie-api-bez-staging/
---
```

Znaczenie: `draft: true` powoduje, że generator pominie plik przy budowaniu strony. `permalink` nadpisuje adres URL. `date` służy do sortowania.

**Notatka w Obsidianie:**

```markdown
---
aliases: [regresja 2.4.0, testy release 2.4]
tags: [qa/regresja, release/2-4-0]
created: 2026-09-06
related: "[[Moduł 5 — Markdown, YAML i Front Matter]]"
---
```

Znaczenie: `aliases` sprawia, że notatkę znajdziesz też pod inną nazwą. `tags` z ukośnikami tworzą hierarchię tagów.

**Dokumentacja przypadku testowego — przykład dla twojego działu QA:**

```markdown
---
id: TC-118
tytul: "Rabat 100% na zamówieniu o wartości zerowej"
modul: zamowienia
priorytet: wysoki
typ: negatywny
automatyzacja: false
wymaganie: REQ-042
autor: Kacper
zaktualizowano: 2026-09-06
srodowiska: [staging, prod]
---

## Warunki wstępne

Konto testowe z uprawnieniami do składania zamówień.

## Kroki

1. Utwórz zamówienie o wartości 0.00
2. Zastosuj kupon `FULL100`
3. Zatwierdź zamówienie

## Oczekiwany rezultat

Walidacja odrzuca zamówienie z komunikatem o zerowej wartości koszyka.
```

Sens tego przykładu: gdy masz trzysta takich plików w repozytorium, jednym skryptem wyciągniesz wszystkie przypadki o priorytecie wysokim, które nie są zautomatyzowane i dotyczą modułu zamówień. Bez Front Mattera musiałbyś parsować treść.

**Skill dla Claude Code (przedsmak modułu 6):**

```markdown
---
name: bug-report
description: "Tworzy ustandaryzowany raport błędu z logu lub opisu problemu. Użyj, gdy użytkownik zgłasza błąd, wkleja stacktrace albo prosi o sformatowanie zgłoszenia do Jiry."
allowed-tools: Read, Grep
---

Treść instrukcji dla modelu...
```

**Definicja subagenta:**

```markdown
---
name: test-reviewer
description: Sprawdza kompletność testów jednostkowych w zmienionych plikach
model: sonnet
tools: Read, Grep, Glob
---

Jesteś recenzentem testów. Dla każdego zmienionego pliku sprawdź...
```

### Typowe błędy — i dlaczego są groźne

To jest najważniejszy fragment tego modułu, bo błędy Front Mattera należą do kategorii **cichych awarii**. Nic nie wybucha. Nie ma czerwonego komunikatu. Po prostu funkcja nie działa, a ty tego nie widzisz.

**Pusta linia albo cokolwiek przed otwierającym `---`.** Front Matter nie zostaje rozpoznany. W Claude Code efekt jest taki, że myślniki i wszystkie pola wjeżdżają do promptu jako zwykły tekst, a skill nie ma opisu.

**Brak zamykającego `---`.** Parser nie znajduje końca metadanych. W najlepszym razie błąd, w najgorszym — cały plik traktowany jako YAML albo cały jako treść.

**Trzy myślniki użyte w treści jako linia pozioma.** Jeżeli w treści pliku wstawisz `---` w miejscu, gdzie parser jeszcze szuka końca Front Mattera, obetniesz metadane w złym miejscu. W treści używaj `***` zamiast `---`.

**Tabulator zamiast spacji.** Twardy błąd YAML, ale komunikat bywa mylący.

**Niecytowany dwukropek w wartości.** `description: Robi X: i Y` wywala parsowanie. Efekt w Claude Code: skill ładuje się z pustymi metadanymi, `/nazwa` dalej działa, ale model nigdy nie uruchomi go sam, bo nie ma opisu do dopasowania.

**Literówka w nazwie pola.** Ciche pominięcie, jak wyżej.

**Znaki BOM na początku pliku albo końcówki linii CRLF.** Plik skopiowany z Windowsa może mieć niewidoczny znacznik BOM przed pierwszym `---`, przez co pierwsza linia technicznie nie jest już `---`. To dokładnie ta klasa problemów, na którą trafiłeś przy uprawnieniach plików w WSL. Sprawdzenie:

```bash
file SKILL.md
head -c 20 SKILL.md | xxd | head -2
```

Jeżeli zobaczysz `efbbbf` na początku, masz BOM. Usuniesz go tak:

```bash
sed -i '1s/^\xEF\xBB\xBF//' SKILL.md
```

**Jak wykrywać ciche awarie — sposób myślenia QA.** Skoro błąd nie krzyczy, musisz mieć sposób na sprawdzenie, że rzecz *działa*, a nie tylko że *nie wywaliła się*. Dla Front Mattera oznacza to trzy sprawdzenia: czy plik parsuje się jako YAML, czy pola mają oczekiwane nazwy i typy, czy narzędzie faktycznie widzi metadane (dla skilla: czy pojawia się w `/skills`, czy `--debug` nie zgłasza błędu parsowania). To jest dokładnie ta sama logika, co test z asercją — samo "kod się wykonał" nic nie znaczy, jeżeli nie sprawdziłeś wyniku.

### Prosty walidator Front Mattera w Pythonie

Warto mieć takie narzędzie własnoręcznie, bo używa się go w każdym module dalej:

```python
#!/usr/bin/env python3
"""Sprawdza, czy plik Markdown ma poprawny YAML Front Matter."""
import sys
import yaml

def sprawdz(sciezka):
    with open(sciezka, encoding="utf-8") as f:
        tresc = f.read()

    if not tresc.startswith("---\n"):
        return False, "Plik nie zaczyna się od '---' w pierwszej linii"

    koniec = tresc.find("\n---", 3)
    if koniec == -1:
        return False, "Brak zamykającego '---'"

    blok = tresc[4:koniec]
    try:
        dane = yaml.safe_load(blok)
    except yaml.YAMLError as e:
        return False, f"Błąd YAML: {e}"

    if not isinstance(dane, dict):
        return False, "Front Matter nie jest mapą klucz-wartość"

    return True, dane

if __name__ == "__main__":
    ok, wynik = sprawdz(sys.argv[1])
    print("OK:" if ok else "BŁĄD:", wynik)
    sys.exit(0 if ok else 1)
```

Zwróć uwagę na `sys.exit` — dzięki temu skrypt nadaje się do użycia w CI, gdzie liczy się kod wyjścia.

---

## ZADANIE PRAKTYCZNE — MODUŁ 5

**Zadanie 5.1 [WYŚLIJ]** — W repozytorium `nauka-ai` utwórz plik `modul-05/przyklady/tc-001.md` opisujący dowolny przypadek testowy, z Front Matterem zawierającym co najmniej: `id`, `tytul`, `priorytet`, `automatyzacja` (boolean), `tagi` (lista), `data` oraz jedno pole, którego wartość zawiera dwukropek. Treść pod Front Matterem ma zawierać nagłówek, listę numerowaną kroków, tabelę i blok kodu z oznaczonym językiem. Wyślij zawartość pliku.

**Zadanie 5.2 [WYŚLIJ]** — Uruchom na tym pliku walidator z sekcji wyżej (zapisz go jako `narzedzia/waliduj_fm.py`) i wyślij surowy output razem z kodem wyjścia:

```bash
python3 narzedzia/waliduj_fm.py modul-05/przyklady/tc-001.md
echo "kod wyjścia: $?"
```

**Zadanie 5.3 [WYŚLIJ]** — Zepsuj plik na trzy sposoby, po kolei, za każdym razem uruchamiając walidator i notując komunikat: (a) wstaw pustą linię przed pierwszym `---`, (b) usuń zamykające `---`, (c) usuń cudzysłowy z wartości zawierającej dwukropek. Wyślij trzy komunikaty błędu i napisz jednym zdaniem, dlaczego każdy z nich powstał.

**Zadanie 5.4 [bez wysyłki]** — Otwórz swój `tc-001.md` na GitHubie i sprawdź, jak Front Matter renderuje się w podglądzie. Zwróć uwagę, co GitHub z nim robi.
