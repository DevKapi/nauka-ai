# Moduł 4 — Agent AI na istniejącym projekcie

Notatka referencyjna. Projekt ćwiczeniowy: `projekt-zamowienia` (walidacja zamówień + naliczanie rabatów, Python + unittest).

---

## 1. O czym jest ten moduł

W Module 3 uczyłem się uruchamiać Claude Code i z nim rozmawiać. Moduł 4 jest o czymś trudniejszym: **jak wpuścić agenta do projektu, którego sam jeszcze nie rozumiem, i go nie zepsuć.**

To jest realna sytuacja w pracy QA. Prawie nigdy nie dostaje się pustego katalogu. Dostaje się kod, który ktoś napisał, w którym coś nie działa, i trzeba się w tym połapać.

Jedno zdanie, które streszcza cały moduł:

> **Agent jest szybki, ale to ja odpowiadam za to, co trafi do repozytorium.**

---

## 2. Dlaczego istniejący projekt to inna praca niż projekt od zera

Przy projekcie od zera agent zna cały kontekst — sam wszystko napisał w tej sesji. Przy istniejącym projekcie są trzy problemy naraz:

| Problem | Dlaczego to boli |
|---|---|
| Ja nie wiem, co tam jest | Nie umiem ocenić, czy agent mówi prawdę |
| Agent też nie wie | Musi to odkryć, czytając pliki — i może przeczytać nie te |
| Jest co zepsuć | W pustym katalogu zła zmiana nic nie kosztuje, w działającym kosztuje |

Dlatego kolejność pracy jest zawsze taka sama:

```
Rekonesans → Plan → Zmiana → Weryfikacja → Commit
```

**Najczęstszy błąd początkującego:** wejście od razu w „Zmianę". Prosisz „napraw ten błąd", agent coś zmienia, klikasz „yes", i po dwóch minutach nie wiesz, w jakim stanie jest projekt.

---

## 3. Jak agent „widzi" projekt

To jest kluczowe i często źle rozumiane.

**Claude Code NIE wczytuje całego repozytorium do pamięci.** Gdyby to robił, przy dużym projekcie skończyłoby się miejsce w oknie kontekstu (context window — ograniczona ilość tekstu, którą model widzi naraz).

Agent działa jak nowy człowiek w zespole — czyta wybiórczo, używając narzędzi:

- listuje katalogi (odpowiednik `ls`)
- szuka po nazwach plików (glob, np. `**/*.py`)
- szuka po treści (grep, np. „gdzie jest słowo `rabat`")
- czyta konkretny plik, często tylko fragment
- uruchamia polecenia w terminalu

**Co z tego wynika praktycznie:** jakość odpowiedzi agenta zależy od tego, czy trafił na właściwe pliki.

| Prompt | Co się dzieje |
|---|---|
| „popraw walidację" | Agent zgaduje, gdzie ona jest. Przy 3000 plików może nie trafić. |
| „popraw walidację w `@walidator.py`" | Trafia od razu, zero zgadywania. |

**Znak `@`** w prompcie oznacza „weź ten konkretny plik do kontekstu". Podczas pisania `@` pojawia się podpowiadanie ścieżek.

W małym projekcie (6 plików) agent przeczyta wszystko i `@` nie robi różnicy. W dużym repozytorium **mój prompt jest jedynym kompasem agenta.**

---

## 4. Tryby uprawnień — hamulec bezpieczeństwa

Tryb decyduje, **co agent może zrobić bez pytania mnie o zgodę**. Przełącza się je `Shift+Tab` (cyklicznie), aktualny tryb widać na pasku na dole terminala.

| Tryb | Co robi | Kiedy używam |
|---|---|---|
| **manual** (ręczny) | Pyta przed każdą edycją pliku i przed komendą w terminalu | Gdy chcę widzieć każdy krok |
| **accept edits** | Sam edytuje pliki, bez pytania | Gdy ufam zadaniu i przejrzę diff później |
| **plan** | **Tylko czyta i bada.** Nie edytuje. Na końcu przedstawia plan | **Rekonesans w nieznanym projekcie** |
| **auto** | Działa sam, ale każdą akcję sprawdza osobny model-klasyfikator | Praca hands-off, gdy nie patrzę w terminal |

Sposoby wejścia w tryb plan:

```bash
claude --permission-mode plan        # cała sesja startuje w trybie plan
```

```
/plan                                 # przełączenie w środku rozmowy
Shift+Tab                             # cykliczne przełączanie trybów
```

**Zasada, którą stosuję na stałe:** rekonesans w nieznanym projekcie robię w trybie **plan**. Wtedy agent fizycznie nie może nic popsuć, więc mogę zadawać dowolnie „głupie" pytania bez ryzyka.

Po zatwierdzeniu planu sesja **wychodzi** z trybu plan i przechodzi do trybu, który wybrałem przy zatwierdzaniu. Żeby planować dalej — `Shift+Tab` z powrotem albo `/plan` na początku kolejnego promptu.

---

## 5. CLAUDE.md — pamięć projektu

### Problem, który to rozwiązuje

Każda sesja Claude Code startuje z **pustym oknem kontekstu**. Zamykam terminal, otwieram jutro — agent nie pamięta nic. Nie wie, jak uruchomić testy, nie wie o decyzjach biznesowych, nie wie, czego nie wolno ruszać.

CLAUDE.md to plik markdown, który agent **czyta na starcie każdej sesji**.

### Gdzie może leżeć

| Zakres | Lokalizacja | Do czego |
|---|---|---|
| Użytkownik | `~/.claude/CLAUDE.md` | Moje preferencje we wszystkich projektach |
| Projekt | `./CLAUDE.md` lub `./.claude/CLAUDE.md` | Zasady zespołu, **wchodzi do gita** |
| Lokalny | `./CLAUDE.local.md` | Moje prywatne notatki, **do `.gitignore`** |
| Firmowy | `/etc/claude-code/CLAUDE.md` (Linux/WSL) | Narzucany przez IT, nie da się wyłączyć |

### Jak się wczytują

Claude Code wczytuje `CLAUDE.md` z katalogu roboczego **i z każdego katalogu powyżej**. Uruchomienie w `foo/bar/` wczytuje `foo/bar/CLAUDE.md` oraz `foo/CLAUDE.md`.

Dwa niuanse:

1. **Pliki się nie nadpisują — sklejają.** Wszystkie znalezione trafiają do kontekstu, uporządkowane od korzenia w dół. Ten najbliżej miejsca uruchomienia jest czytany jako ostatni.
2. **Pliki w podkatalogach poniżej** nie ładują się na starcie — dołączają dopiero, gdy agent sięgnie po pliki z tych podkatalogów.

### Najważniejsze: to nie jest twardy zakaz

CLAUDE.md trafia do agenta jako **kontekst, nie jako wymuszona konfiguracja**. Agent go czyta i stara się stosować, ale nie ma gwarancji — zwłaszcza przy instrukcjach mglistych albo sprzecznych.

> **CLAUDE.md to instruktaż, nie bramka.**

Poziomy egzekwowania zasad, od najsłabszego:

| Poziom | Narzędzie | Co daje |
|---|---|---|
| Sugestia | `CLAUDE.md` | Agent *stara się* stosować |
| Blokada lokalna | hook `PreToolUse` | Polecenie shell przed akcją narzędzia; **blokuje niezależnie od decyzji modelu** |
| Blokada uprawnień | `permissions.deny` w ustawieniach | Konkretne narzędzia/ścieżki wycięte po stronie klienta |
| Blokada zespołowa | branch protection + CI na GitHubie | Nawet człowiek nie wepchnie zmiany, jeśli testy padają |

> **CLAUDE.md kształtuje zachowanie, hooki i uprawnienia je egzekwują.**

### Jak pisać, żeby działało

- **Konkretnie i sprawdzalnie.** „Uruchom `python3 -m unittest discover -v` przed commitem" — nie „testuj swoje zmiany".
- **Krótko.** Cel: poniżej 200 linii. Dłuższe pliki zjadają kontekst i **obniżają** stopień stosowania się do nich.
- **Strukturalnie.** Nagłówki i punkty. Agent skanuje strukturę tak jak człowiek.
- **Bez sprzeczności.** Jeśli dwie reguły się kłócą, agent może wybrać dowolną — nie ma reguły „nowsza wygrywa".
- **Bez rzeczy oczywistych z kodu.** Trzymaj to, czego z kodu **nie da się wyczytać**: decyzje, pułapki, powody.

**Kiedy dopisać linijkę:** gdy po raz drugi wpisuję agentowi tę samą poprawkę.

### Pułapka jednoznaczności — mój własny błąd

Napisałem w CLAUDE.md:

```
nie wolno modyfikowac plikow test_*.py, jest to wymagane zeby testy przeszly
```

Zdanie da się przeczytać odwrotnie: *modyfikuj testy, bo to jest wymagane, żeby przeszły*. Dokładna odwrotność intencji.

Poprawna wersja — trzy zdania, każde robi jedną rzecz:

```markdown
## Zakazy
- NIE modyfikuj plików `test_*.py`.
- Testy są źródłem prawdy. Jeśli test i kod dają sprzeczny wynik, poprawiamy kod.
- Nie osłabiaj asercji ani nie usuwaj testów, żeby uzyskać zielony wynik.
```

**Odruch:** po napisaniu CLAUDE.md przeczytać go na głos i szukać zdań, które da się zrozumieć na dwa sposoby.

### Druga pułapka — dezaktualizacja

Wygenerowany przez `/init` plik to **szkic sprzed moich decyzji**. Gdy podejmę decyzję, muszę wrócić i usunąć zdanie, które ją zawiesza. W moim projekcie sekcja `Known state` twierdziła, że testy padają, jeszcze dwie godziny po ich naprawieniu — i agent sam to wychwycił.

**CLAUDE.md dezaktualizuje się szybciej niż kod.** Aktualizacja to część zadania, nie osobne zadanie.

### Komendy

| Komenda | Do czego |
|---|---|
| `/init` | Wygeneruj startowy CLAUDE.md — agent analizuje projekt i wypisuje komendy, testy, konwencje |
| `/memory` | Lista plików pamięci, otwiera je do edycji, przełącznik auto memory |
| `/context` | **Weryfikacja** — pokazuje, co realnie wczytało się do sesji, sekcja *Memory files* |

`/context` to narzędzie sprawdzania. **Jeśli pliku tam nie ma, agent go nie widzi** — koniec dyskusji.

### Auto memory — drugi mechanizm pamięci

Poza CLAUDE.md agent prowadzi własne notatki (auto memory), zapisywane per repozytorium.

| | CLAUDE.md | auto memory |
|---|---|---|
| Kto pisze | ja | agent |
| Co zawiera | instrukcje, zasady | wnioski, moje poprawki, preferencje |
| Wczytywane | każda sesja | każda sesja |

Auto memory da się obejrzeć i edytować przez `/memory`. To zwykłe pliki markdown.

---

## 6. Bezpieczna pętla zmiany

### Dlaczego branch, zanim agent cokolwiek dotknie

Branch (gałąź) to **ruchoma etykieta wskazująca na commit** — nie kopia plików, nie osobny folder.

Praca na osobnej gałęzi daje trzy rzeczy:

1. **`main` zostaje nietknięty.** Jeśli agent narobi bałaganu, mam punkt powrotu.
2. **Diff jest czysty.** Porównuję gałąź z `main` i widzę sumę zmian z tego zadania.
3. **Powstaje jednostka do przeglądu.** Bez gałęzi nie ma PR-a, a bez PR-a nie ma code review.

> **Gałąź powstaje ZANIM agent zacznie edytować.** Zrobiona po zmianach nie pomoże — zmiany i tak siedzą w katalogu roboczym.

### Zakres zadania dla agenta

Zły prompt: *„napraw ten projekt"*. Agent sam zdecyduje, co naprawić — może przy okazji poprawić walidację e-maila, zamienić `float` na `Decimal`, dodać obsługę wyjątków. Wszystko sensowne, wszystko nie na temat, i wszystko trzeba przejrzeć.

Dobry prompt zawiera trzy rzeczy: **co zmienić, w którym pliku, czego nie ruszać.**

Przykład, który zadziałał:

```
Napraw błąd graniczny w @rabaty.py: progi rabatowe mają być włączne,
czyli kwota równa progowi ma łapać rabat tego progu.

Ograniczenia:
- Zmieniasz WYŁĄCZNIE plik rabaty.py.
- Nie dotykasz plików test_*.py.
- Zmiana ma być minimalna - nie refaktoryzuj, nie poprawiaj niczego innego,
  nawet jeśli widzisz inne problemy.

Najpierw pokaż mi plan.
```

Zdanie „nawet jeśli widzisz inne problemy" jest ważne — bez niego agent traktuje zauważone usterki jako zaproszenie.

---

## 7. Czytanie diffa — główne narzędzie kontroli

Diff to **jedyne miejsce, w którym widzę, co agent faktycznie zrobił**, a nie co napisał, że zrobił.

| Komenda | Co pokazuje | Kiedy |
|---|---|---|
| `git diff` | Zmiany niedodane do poczekalni | Zaraz po pracy agenta |
| `git diff --staged` | Zmiany już po `git add`, czekające na commit | Tuż przed commitem |
| `git diff main` | Różnica całej gałęzi względem `main` | Przed założeniem PR-a |
| `git diff --stat` | Tylko podsumowanie: które pliki, ile linii | Szybki rzut oka na rozmiar zmiany |

### Anatomia

```diff
diff --git a/rabaty.py b/rabaty.py
index 1a2b3c4..5d6e7f8 100644
--- a/rabaty.py
+++ b/rabaty.py
@@ -3,7 +3,7 @@ PROGI = [(1000, 0.10), (500, 0.05), (100, 0.02)]

 def oblicz_rabat(kwota):
     for prog, rabat in PROGI:
-        if kwota > prog:
+        if kwota >= prog:
             return rabat
     return 0.0
```

| Element | Znaczenie |
|---|---|
| `--- a/plik` | Wersja **przed** |
| `+++ b/plik` | Wersja **po** |
| `@@ -3,7 +3,7 @@` | Nagłówek fragmentu: od linii 3, 7 linii przed / od linii 3, 7 linii po |
| Linia z `-` | **Usunięta** |
| Linia z `+` | **Dodana** |
| Linia ze spacją | Kontekst, bez zmian |

Zmiana jednej linii to **jedna para `-` / `+`**. Więcej par = agent zrobił coś ponad zadanie.

### Pułapka zielonego wyniku

Zadanie „spraw, żeby testy przechodziły" ma dwie drogi do celu:

```
naprawić kod  →  11/11 zielone
osłabić test  →  11/11 zielone
```

Terminal wygląda identycznie. Różnica jest **tylko w diffie**.

> **Kolejność: najpierw diff, potem testy.** Zielony wynik wyłącza czujność — po nim diff przegląda się pobieżnie i to właśnie wtedy przechodzi osłabiona asercja.

> **Zielony wynik nie jest dowodem, jest hipotezą.**

---

## 8. FAIL kontra ERROR — dwa różne światy

| | **FAIL** | **ERROR** |
|---|---|---|
| Co się stało | Asercja nie wyszła | Kod wyrzucił wyjątek |
| Test | Dobiegł do końca | Przerwał się albo w ogóle nie wystartował |
| Znaczenie | Kod działa, ale daje **zły wynik** | Kod **w ogóle nie zadziałał** |
| Przykład | `AssertionError: 0.0 != 0.02` | `SyntaxError`, `ImportError`, `NameError` |
| Zwykła przyczyna | Błąd logiki albo złe oczekiwanie w teście | Literówka, zła ścieżka, brak zależności, zepsute środowisko |

To są **dwie różne ścieżki debugowania i dwa różne typy zgłoszeń.**

### Czytanie tracebacku — od dołu do góry

```
Traceback (most recent call last):
  File ".../test_walidator.py", line 2, in <module>
    from walidator import waliduj_email, ...
  File ".../walidator.py", line 15
    if not waliduj_email(zamowienie.get(email", "")):
SyntaxError: unterminated string literal
```

| Gdzie patrzę | Co tam jest |
|---|---|
| **Ostatnia linia** | Typ błędu i komunikat — odpowiedź na „co się stało" |
| **Przedostatnia ramka** | Miejsce, gdzie realnie wybuchło |
| Ramki wyżej | Łańcuch wywołań — jak tam dotarliśmy |

> **`Most recent call last` znaczy, że winowajca jest na DOLE.**

**Mój błąd w tym module:** przeczytałem od góry i napisałem, że błąd jest w `test_walidator.py`. Błąd był w `walidator.py`. Plik testowy tylko poprosił o zepsuty moduł. W pracy kończy się to zgłoszeniem bugu przypisanym do złego komponentu.

### Znikające testy — najważniejsza pułapka

Ten sam przebieg, przed i po wprowadzeniu `SyntaxError` do `walidator.py`:

| | przed | po |
|---|---|---|
| `Ran X tests` | **10** | **7** |
| test_rabaty.py | 6 | 6 |
| test_walidator.py | 4 | **0** |
| `_FailedTest` (atrapa) | 0 | 1 |

`unittest.loader._FailedTest` **to nie jest mój test.** To sztuczny obiekt, który unittest podstawia w miejsce **całego modułu**, którego nie dało się zaimportować.

Cztery testy walidatora **nie padły — one się nie odbyły.**

Dlaczego to groźne: patrząc tylko na „ile FAIL" widzę jeden błąd i myślę „drobiazg". Realnie straciłem 40% pokrycia i nie wiem, czy walidator działa. W CI, gdzie nikt nie czyta logów tylko patrzy na czerwone/zielone, tak przechodzą regresje.

> **Przy każdym przebiegu porównuję nie tylko liczbę FAIL, ale liczbę URUCHOMIONYCH testów z poprzednim przebiegiem. Spadek liczby testów to osobny alarm.**

Dlaczego `SyntaxError` w jednym pliku nie zabił całego przebiegu: import jest **per-moduł**. `test_rabaty.py` importuje tylko `rabaty.py`, który był zdrowy, więc jego 6 testów poszło normalnie.

### Jak dawać agentowi błąd do analizy

Trzy sposoby, od najgorszego:

1. **Opis własnymi słowami** — „coś się wywala przy walidacji". Agent zgaduje.
2. **Wklejenie surowego tracebacku** — działa dobrze, agent ma numery linii i typ wyjątku.
3. **Pozwolenie agentowi uruchomić komendę** — najlepsze. Widzi pełny aktualny wynik i może iterować.

Przy trzecim wariancie: agent, który sam uruchamia testy i sam je poprawia, potrafi zapętlić się w „byle zielone". Dlatego zakaz ruszania testów w CLAUDE.md **i tak oglądam diff**.

---

## 9. Luki w pokryciu — błąd, którego testy nie widzą

Zmiana jednego znaku:

```python
round(kwota * (1 - rabat), 2)   # 2 miejsca po przecinku → grosze
round(kwota * (1 - rabat), 1)   # 1 miejsce → dziesiątki groszy
```

Zamówienie za 101 zł:

```
101 × 0.98 = 98.98
round(98.98, 2) = 98.98   ← poprawnie
round(98.98, 1) = 99.0    ← klient płaci 99,00 zamiast 98,98
```

Każde zamówienie z groszami liczone źle. **Wszystkie 10 testów przechodziło.**

Dlaczego nikt tego nie złapał — jedyny test dotykający tej funkcji:

```python
self.assertEqual(cena_po_rabacie(200), 196.0)
```

200 × 0.98 = **196.0**. Zero groszy. `round(196.0, 1)` i `round(196.0, 2)` dają ten sam wynik. Test przechodzi w obu wersjach kodu, bo **dane testowe w ogóle nie uruchamiają mechanizmu zaokrąglania**.

> **Dane testowe muszą uruchamiać mechanizm, który testuję.** Testując zaokrąglanie na okrągłych liczbach, nie testuję niczego — tylko ładnie wyglądam w raporcie pokrycia.

To jest groźniejsze niż brak testu, bo daje **fałszywe poczucie bezpieczeństwa**.

### Testowanie wartości granicznych

Oryginalny błąd projektu: `kwota > prog` zamiast `kwota >= prog`. Efekt zależy od tego, gdzie leży kwota:

| Kwota | Co się dzieje | Wynik |
|---|---|---|
| 50 | Poniżej wszystkich progów | `0.0` — poprawnie, granica nietestowana |
| 100 | Najniższy próg pominięty, nie ma niżej gdzie spaść | `0.0` — **brak rabatu w ogóle** |
| 500 | Próg 500 pominięty, pętla łapie próg 100 | `0.02` — **rabat niższego progu** |
| 1000 | Próg 1000 pominięty, pętla łapie próg 500 | `0.05` zamiast `0.10` |
| 1500 | Wyraźnie powyżej progu | `0.10` — poprawnie, granica nietestowana |

**Padają dokładnie te przypadki, które trafiają w granicę.** Wszystko wyraźnie powyżej lub poniżej progu przechodzi, bo tam wybór `>` vs `>=` niczego nie zmienia.

Gdyby autor testów napisał tylko `oblicz_rabat(50)` i `oblicz_rabat(1500)`, błąd siedziałby w produkcji do pierwszej reklamacji.

> Formułka na rozmowę: **błąd off-by-one na granicy przedziału, wykryty przez testy wartości granicznych (boundary value analysis).**

### Nowy test najpierw na czerwono

```
1. Napisz test           →  ma FAIL
2. Napraw kod            →  ma OK
```

Test napisany od razu przy poprawnym kodzie świeci na zielono — ale nie wiem, czy dlatego, że kod jest dobry, czy dlatego, że **test niczego nie sprawdza** (literówka w nazwie, zła asercja, złe dane).

> **Zielony test, który nigdy nie był czerwony, jest niezweryfikowany.**

---

## 10. Siatka bezpieczeństwa — cofanie zmian

| Komenda | Co robi | Uwaga |
|---|---|---|
| `git restore plik` | Wyrzuca **niezacommitowane** zmiany, wraca do stanu z ostatniego commita | **Nieodwracalne** |
| `git restore .` | To samo dla wszystkich plików | |
| `git restore --staged plik` | Cofa `git add`, zmiany zostają w pliku | Bezpieczne |
| `git switch -` | Wróć na poprzednią gałąź | |
| `git branch -d nazwa` | Skasuj gałąź **tylko jeśli** jej commity są już gdzie indziej | **Domyślnie używam tego** |
| `git branch -D nazwa` | Skasuj na siłę, z utratą commitów | Tylko świadomie |

### Czego `git restore` NIE zrobi

**Nie usuwa plików nieśledzonych.** Restore cofa zmiany w plikach, które git zna. Nowego pliku nie zna, więc go nie dotyka.

Mój przypadek: przez pomyłkę powstał plik `testy_rabaty.py` z samą metodą bez klasy. `git restore test_rabaty.py` niczego nie naprawił, bo dotyczył innego pliku. Trzeba było `rm testy_rabaty.py`.

Do sprzątania nieśledzonych: `rm plik` albo `git clean -n` (podgląd) → `git clean -f` (usunięcie).

**Dlaczego commituję małymi krokami:** commit to punkt, do którego zawsze mogę wrócić. Bez commita `git restore` nie ma dokąd cofnąć.

---

## 11. Sprawdzanie składni bez uruchamiania

```bash
python3 -c "import ast; ast.parse(open('test_rabaty.py').read()); print('skladnia OK')"
```

Parsuje plik i sprawdza wcięcia oraz składnię, **nie wykonując go**. Wypisze `skladnia OK` albo pokaże, w której linii coś się nie zgadza.

Po co osobno: gdy plik ma `SyntaxError`, wynik testów zamienia się w `ImportError` i ciężko dojść, co jest grane. **Najpierw sprawdzam składnię, potem szukam błędów logicznych.**

Pokrewne:

```bash
grep -n "test_cena_z_groszami" test_rabaty.py    # -n = pokaż numery linii
python3 -c "print(1+1)"                          # szybki eksperyment bez tworzenia pliku
```

`python3 -c` jest świetne do sprawdzenia hipotezy o zachowaniu kodu — wklejam fragment logiki i patrzę, co zwraca, zamiast zgadywać z pamięci.

---

## 12. Git i GitHub z CLI — pełny cykl

### Pojęcia

| Pojęcie | Co to |
|---|---|
| **remote** | Repozytorium zdalne. `origin` = standardowa nazwa dla „moje repo na GitHubie" |
| **push** | Wyślij commity na remote. Wysyła tylko te, których tam jeszcze nie ma |
| **Pull Request (PR)** | Prośba: „weźcie zmiany z mojej gałęzi i wcielcie do `main`" |
| **code review** | Przegląd diffa w PR-ze przed wcieleniem |
| **merge** | Wcielenie gałęzi do `main` |

**Dlaczego PR dotyczy mnie jako QA:** PR jest tym, co dostaję do sprawdzenia. Patrzę na **diff w PR-ze**, nie na cały projekt. Umiejętność powiedzenia „tu brakuje testu granicznego" to konkretna wartość.

### Komendy

```bash
# utworzenie repo na GitHubie z bieżącego katalogu
gh repo create projekt-zamowienia --public --source=. --remote=origin --push
```

| Flaga | Znaczenie |
|---|---|
| `--public` | Repozytorium publiczne |
| `--source=.` | Użyj bieżącego katalogu jako źródła |
| `--remote=origin` | Nazwij remote `origin` |
| `--push` | Wypchnij od razu |

```bash
git push -u origin fix/progi-rabatowe   # pierwszy push gałęzi
git push                                 # kolejne pushe — wystarczy tyle
git remote -v                            # sprawdź, dokąd wskazuje origin
```

`-u` ustawia powiązanie lokalnej gałęzi ze zdalną. Robi się to **raz na gałąź**.

```bash
gh pr create --base main --head fix/progi-rabatowe \
  --title "Napraw granice progow rabatowych" \
  --body "Opis zmiany i wynik testów."
```

| Flaga | Znaczenie |
|---|---|
| `--base` | Gałąź docelowa (dokąd wcielamy) |
| `--head` | Gałąź źródłowa (skąd bierzemy) |
| `\` na końcu linii | Polecenie ciągnie się dalej |

Po utworzeniu wypisuje się **URL PR-a**.

**Znany problem w moim środowisku:** `gh pr view` wywala błąd GraphQL, bo GitHub wycofał stare API Projects. Obejście — używam URL-a wypisanego przez `gh pr create`.

### Gałąź to etykieta, nie folder

`git log --oneline` po całym module:

```
f31f260 (HEAD -> fix/progi-rabatowe) Dodaj test ceny z groszami
31ee848 (test/analiza-bledow) Napraw granice progow rabatowych...
d3a9f4d (main) Usun sprzecznosc i doprecyzuj zakazy w CLAUDE.md
2879351 Dodaj brakujace pliki projektu odziedziczonego
5903a7a Dodaj CLAUDE.md z zasadami projektu
baa723c Wersja odziedziczona po poprzednim zespole
```

Trzy nazwy gałęzi wskazują na trzy różne commity **w jednej linii historii**. `test/analiza-bledow` została stworzona na `31ee848` i tam została, bo nie zrobiłem na niej żadnego commita. `main` stoi na `d3a9f4d`, a moja praca poszła dalej.

---

## 13. Typowe błędy — z własnego doświadczenia w tym module

| Błąd | Co się stało | Odruch na przyszłość |
|---|---|---|
| Czytanie tracebacku od góry | Wskazałem `test_walidator.py` zamiast `walidator.py` | Ostatnia linia = typ błędu, przedostatnia ramka = miejsce |
| Nieporównanie liczby testów | 10 → 7 testów, nie zauważyłem | Porównuję `Ran X tests` z poprzednim przebiegiem |
| Uznanie `_FailedTest` za mój test | „wykonał 1 test na walidatorze" — wykonał zero | To atrapa po nieudanym imporcie całego modułu |
| Sprzeczność w CLAUDE.md | `/init` mówił „zdecyduj", ja mówiłem „zdecydowane" | Po decyzji usuwam zdanie, które ją zawiesza |
| Dwuznaczne zdanie w CLAUDE.md | Zakaz dał się przeczytać odwrotnie | Jedno zdanie = jedna reguła, czytam na głos |
| Dopisanie testu do nowego pliku | Powstał `testy_rabaty.py` z metodą bez klasy | `grep -n` + `ast.parse` przed uruchomieniem testów |
| `git restore` na nieśledzonym pliku | Nie zadziałał, bo git tego pliku nie znał | Nieśledzone usuwam `rm` albo `git clean` |
| Odpuszczenie analizy („nie znam kodu") | Miałem diff jednej linii i podpowiedź | Diff jednej linii zawsze da się prześledzić |
| Niecommitowanie wygenerowanego `/init` | Straciłem możliwość zobaczenia własnego wkładu | Commituję wygenerowane, potem edytuję |
| Niekonsekwencja w komendzie testów | Raz `unittest -v`, raz `unittest discover -v` | Jedna wersja, ta z CLAUDE.md — ona pójdzie do CI |

---

## 14. Ściąga komend

### Claude Code

```bash
claude                                # start sesji
claude --permission-mode plan         # start w trybie plan (tylko odczyt)
```

```
/help          lista komend
/plan          wejście w tryb plan w trakcie rozmowy
/init          wygeneruj startowy CLAUDE.md
/memory        pliki pamięci — podgląd i edycja
/context       co realnie wczytało się do sesji
/clear         wyrzuć historię rozmowy (nowy temat)
/compact       streść historię (długie zadanie, kończy się kontekst)
@sciezka/plik  wskaż agentowi konkretny plik
Esc            przerwij agenta
Ctrl+C x2      wyjdź z Claude Code
Shift+Tab      przełącz tryb uprawnień
```

Różnica `/clear` vs `/compact`: `/clear` **wyrzuca** historię, `/compact` ją **streszcza i zostawia**.

### Git

```bash
git status                      # stan katalogu roboczego — przed i po każdym add
git log --oneline               # historia, jedna linia na commit
git ls-files                    # które pliki git ŚLEDZI
git show --stat HEAD            # co dokładnie weszło do ostatniego commita

git branch                      # lista gałęzi, gwiazdka przy aktualnej
git switch -c fix/nazwa         # utwórz gałąź i przełącz się (-c = create)
git switch main                 # przełącz się na istniejącą
git switch -                    # wróć na poprzednią
git branch -d nazwa             # skasuj gałąź (bezpiecznie)

git diff                        # zmiany niedodane
git diff --staged               # zmiany po git add
git diff main                   # cała gałąź vs main
git diff --stat                 # podsumowanie

git add plik                    # dodaj do poczekalni
git commit -m "opis"            # zatwierdź
git restore plik                # cofnij niezacommitowane zmiany
git restore --staged plik       # cofnij git add
```

### GitHub CLI

```bash
gh repo create nazwa --public --source=. --remote=origin --push
git push -u origin nazwa-galezi
gh pr create --base main --head nazwa-galezi --title "..." --body "..."
```

### Testy (Python unittest)

```bash
python3 -m unittest discover -v                            # wszystkie testy
python3 -m unittest test_rabaty -v                         # jeden moduł
python3 -m unittest test_rabaty.TestRabaty.test_prog_100   # jeden test
```

| Element | Znaczenie |
|---|---|
| `-m unittest` | Uruchom moduł `unittest` (wbudowany, nic nie trzeba instalować) |
| `discover` | Sam znajdź pliki testowe, wzorzec `test*.py` |
| `-v` | Verbose — pokaż każdy test osobno |

**Uwaga:** wzorzec `test*.py` łapie też przypadkowe pliki jak `testy_cos.py`.

---

## 15. Odruchy weryfikacyjne

Zebrane z modułów 1–4, wszystkie w jednym miejscu:

| Po czym | Sprawdzam |
|---|---|
| Po zapisaniu pliku | `cat plik` — czy treść jest ta, której oczekuję |
| Po `git add` | `git status` — czy pliki przeszły do „Changes to be committed" |
| Po `git commit` | Czy widzę `[gałąź hash]` i `N insertions` |
| Po pracy agenta | **`git diff` PRZED uruchomieniem testów** |
| Po uruchomieniu testów | Liczba FAIL **i liczba uruchomionych testów** |
| Po edycji pliku Pythona | `ast.parse` — czy składnia się zgadza |
| Po edycji CLAUDE.md | `/context` w nowej sesji — czy plik się wczytał |
| Po twierdzeniu agenta | Komenda, która to twierdzenie potwierdza lub obala |

Ostatni wiersz jest najważniejszy. Agent bywa dokładny i bywa w błędzie, a jedno i drugie brzmi tak samo pewnie. **Weryfikuję tak samo agenta, jak i człowieka, który mnie uczy.** Źródłem prawdy jest wynik narzędzia.

---

## 16. Zastosowania w pracy QA

**Wejście w nieznany projekt.** Odpalam `claude --permission-mode plan` w katalogu projektu i proszę o opis struktury, sposobu uruchamiania testów i podejrzanych miejsc. W godzinę mam obraz, na który normalnie poszedłby dzień. Potem weryfikuję każde twierdzenie komendą.

**Przegląd cudzego PR-a.** Patrzę na diff, nie na cały projekt. Pytania: czy zmiana dotyka tylko tego, co obiecuje opis? czy testy zostały dopisane, czy tylko zmienione? czy liczba testów wzrosła? Jeśli test został osłabiony, żeby przeszedł — to jest mój główny cel.

**Analiza czerwonego buildu.** Najpierw rozstrzygam FAIL czy ERROR, bo to dwie różne ścieżki. ERROR zwykle znaczy zepsute środowisko albo literówka, FAIL znaczy błąd logiki albo złe oczekiwanie w teście. Dopiero potem czytam traceback od dołu.

**Uzupełnianie pokrycia.** Szukam przypadków, których dane testowe nie uruchamiają: granice przedziałów, wartości z groszami, puste listy, zera, wartości ujemne. Każdy nowy test najpierw musi zaświecić na czerwono.

**Utrwalanie zasad zespołu.** Reguły, które powtarzam ludziom i agentom, trafiają do CLAUDE.md. To, co musi być egzekwowane twardo (nie ruszamy testów, nie pushujemy na main), idzie do hooków, uprawnień albo branch protection.

**Praca agenta na zadaniu, nie na projekcie.** Zadanie dostaje własną gałąź, dokładny zakres i listę zakazów. Diff przed testami. Commit dopiero po obu.

---

## 17. Możliwe pytania testowe

**Podstawy**

1. Dlaczego Claude Code nie wczytuje całego repozytorium do kontekstu i co z tego wynika dla sposobu pisania promptów?
2. Do czego służy `@` w prompcie?
3. Wymień cztery tryby uprawnień i powiedz, kiedy używasz którego.
4. Dlaczego rekonesans w nieznanym projekcie robi się w trybie plan?

**CLAUDE.md**

5. Wymień lokalizacje CLAUDE.md i powiedz, która wchodzi do repozytorium.
6. Co się dzieje, gdy CLAUDE.md jest w kilku katalogach w drzewie — nadpisują się czy sklejają?
7. Dlaczego CLAUDE.md nie jest gwarancją? Co zrobić, gdy zasada musi być egzekwowana twardo?
8. Co robi `/init` i jaka jest główna pułapka z wygenerowanym plikiem?
9. Czym `/context` różni się od `/memory`?
10. Podaj przykład instrukcji źle i dobrze napisanej.

**Git i workflow**

11. Dlaczego gałąź tworzy się przed pracą agenta, a nie po?
12. Czym różni się `git diff` od `git diff --staged` i od `git diff main`?
13. Co oznacza `@@ -3,7 +3,7 @@` w diffie?
14. Dlaczego diff oglądamy przed uruchomieniem testów?
15. Czym różni się `git branch -d` od `-D`?
16. Czego `git restore` nie potrafi cofnąć?
17. Opisz pełny cykl: zmiana → commit → push → PR → review → merge.
18. Co to jest gałąź w gicie — kopia plików czy coś innego?

**Testy i analiza błędów**

19. Czym różni się FAIL od ERROR? Podaj po jednym przykładzie.
20. Jak czyta się traceback i gdzie leży faktyczna przyczyna błędu?
21. Co to jest `unittest.loader._FailedTest` i ile testów wtedy realnie się wykonało?
22. Przebieg pokazuje 0 FAIL, ale mniej uruchomionych testów niż wczoraj. Co to znaczy i co robisz?
23. Dlaczego zmiana `round(x, 2)` na `round(x, 1)` nie została wykryta przez żaden test?
24. Co to jest testowanie wartości granicznych? Podaj przykład z tego projektu.
25. Dlaczego nowy test powinien najpierw zaświecić na czerwono?

**Scenariusze**

26. Agent zgłasza „naprawiłem, wszystkie testy przechodzą". Jakie trzy rzeczy sprawdzasz, zanim uwierzysz?
27. Dostajesz PR od agenta. Co sprawdzasz w pierwszej kolejności i dlaczego?
28. Agent w trybie accept edits zmienił pięć plików zamiast jednego. Jak wracasz do stanu wyjściowego?
29. Jak sformułować zadanie, żeby agent nie „poprawiał przy okazji" innych rzeczy?
30. Kod ma warunek `kwota > prog` z progami `[(1000, 0.10), (500, 0.05), (100, 0.02)]`. Co zwróci `oblicz_rabat(1000)` i dlaczego?

---

## 18. Moimi słowami

*(sekcja do uzupełnienia — co z tego modułu było dla mnie nowe, co mnie zaskoczyło, czego bym się bał w prawdziwym projekcie)*
