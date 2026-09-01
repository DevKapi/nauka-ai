# Moduł 3 — Claude Code

Data: 2026-09-01
Moduł: 3
Cel: praca z agentem AI z poziomu terminala — uruchamianie, uprawnienia, kontekst, komendy, konfiguracja projektu

---

## 1. Czym jest agent CLI

Claude Code to agent działający w terminalu: dostaje zadanie po polsku,
sam czyta pliki, uruchamia komendy, edytuje kod i sprawdza wynik w pętli,
aż dojdzie do celu. Nie jest to podpowiadacz kodu w edytorze ani czat.

| Cecha | Znaczenie w praktyce |
|---|---|
| Agent, nie autouzupełnianie | sam decyduje, które pliki otworzyć i jakie komendy odpalić |
| Pętla działania | czyta → planuje → działa → weryfikuje → poprawia |
| Ma narzędzia | odczyt/zapis plików, bash, grep, wyszukiwanie, web, MCP |
| Działa w repo | widzi cały katalog projektu i historię gita |
| Wymaga zatwierdzeń | akcje ryzykowne (zapis, `git push`, instalacje) pyta przed wykonaniem |
| Wymaga płatnego konta | Pro / Max / Team / Enterprise / Console. Darmowy Claude.ai nie działa |

Kiedy używać: refaktor, nowa funkcja rozłożona na wiele plików, debugowanie,
pisanie testów, przeszukiwanie nieznanego kodu, operacje gita, notatki.

Kiedy nie: gdy sam nie umiesz opisać celu ani ocenić, czy wynik jest poprawny.

---

## 2. Sposoby uruchamiania

Program: `claude`. Uruchamiać z katalogu projektu (`cd ~/projekt` najpierw).

| Komenda | Co robi |
|---|---|
| `claude` | tryb interaktywny — rozmowa w terminalu |
| `claude "napraw test w auth.py"` | interaktywnie, ale z zadaniem od razu w pierwszym prompcie |
| `claude -p "wypisz funkcje w tym pliku"` | tryb `--print` — jedna odpowiedź na stdout i wyjście, bez rozmowy |
| `claude -c` | wznów ostatnią sesję w tym katalogu (`--continue`) |
| `claude -r` | wybierz sesję z listy do wznowienia (`--resume`) |
| `cat log.txt \| claude -p "znajdź błąd"` | dane z pipe'a jako wejście |
| `claude --model claude-opus-5` | wymuś konkretny model na tę sesję |
| `claude --version` | wersja |
| `claude update` | aktualizacja |
| `claude mcp` | zarządzanie serwerami MCP |

Tryb `-p` jest do skryptów i CI: brak interakcji, wynik nadaje się do potoku.

Wyjście z sesji interaktywnej: `Ctrl+C` dwa razy albo `/exit`.

---

## 3. Tryby uprawnień

Kontrolują, kiedy agent pyta o zgodę przed użyciem narzędzia.
Przełączanie w sesji: `Shift+Tab`. Ustawienie na start: flaga `--permission-mode`.

| Tryb | Zachowanie | Kiedy |
|---|---|---|
| `default` | pyta przy pierwszym użyciu każdego narzędzia/komendy | codzienna praca |
| `acceptEdits` | edycje plików bez pytania, reszta (bash, push) nadal pyta | dużo drobnych zmian w plikach, którym ufasz |
| `plan` | tylko czyta i analizuje, nic nie zmienia — kończy planem do zatwierdzenia | rozeznanie w kodzie, projekt zmiany przed startem |
| `bypassPermissions` | nie pyta o nic | tylko w izolowanym środowisku (kontener, VM), nigdy na produkcyjnej maszynie |

```bash
claude --permission-mode plan "zaproponuj jak dodać cache do API"
claude --permission-mode acceptEdits
```

Reguły stałe trzyma się w `settings.json` (`allow` / `ask` / `deny`),
nie zatwierdza się w kółko tego samego:

```json
{
  "permissions": {
    "allow": ["Bash(npm run test:*)", "Bash(git status)"],
    "deny": ["Bash(rm -rf *)", "Read(./.env)"]
  }
}
```

Poziomy plików: `~/.claude/settings.json` (globalny) →
`.claude/settings.json` (projekt, w repo) →
`.claude/settings.local.json` (projekt, prywatny, poza repo).

---

## 4. Sesje i kontekst

**Sesja** — jedna ciągła rozmowa z historią. Zapisywana per katalog,
można wrócić (`claude -c`, `claude -r`).

**Kontekst** — ile agent „pamięta" naraz (okno tokenów). Zapełnia się od:
treści plików, outputów komend, rozmowy.

| Sytuacja | Komenda / mechanizm |
|---|---|
| Kontekst się zapełnia | automatyczne streszczenie starszej części (kompakcja) |
| Ręczne streszczenie teraz | `/compact` |
| Nowe zadanie, czysty stan | `/clear` — czyści kontekst, zostaje w tej samej sesji |
| Podejrzenie „zapomniał" | `/context` — pokazuje zużycie kontekstu |
| Wznowienie po przerwie | `claude -c` (ostatnia) / `claude -r` (wybór) |

Zasada: jedno zadanie = jedna sesja. Przed nowym, niezwiązanym tematem `/clear`.
Nie wrzucaj do jednej sesji refaktoru, debugowania i pisania notatek naraz —
kontekst się zaśmieca i jakość spada.

---

## 5. Komendy slash

Wpisywane w sesji interaktywnej, zaczynają się od `/`.

| Komenda | Do czego |
|---|---|
| `/help` | lista komend |
| `/clear` | wyczyść kontekst |
| `/compact` | streść rozmowę teraz |
| `/context` | zużycie okna kontekstu |
| `/init` | wygeneruj `CLAUDE.md` dla tego repo |
| `/model` | zmień model |
| `/config` | ustawienia (motyw, model domyślny) |
| `/permissions` | podejrzyj i edytuj reguły uprawnień |
| `/review` | przegląd zmian / PR-a |
| `/agents` | zarządzanie subagentami |
| `/mcp` | status serwerów MCP |
| `/memory` | edytuj pliki `CLAUDE.md` |
| `/cost` | koszt bieżącej sesji |
| `/vim` | tryb edycji vim w prompcie |
| `/exit` | wyjście |

Dodatkowo:
- `!komenda` — uruchom komendę shella, output ląduje w rozmowie (np. `!git log --oneline -5`)
- `@ścieżka/plik` — wstaw plik do promptu
- `#tekst` — dopisz tekst do `CLAUDE.md` bez otwierania pliku
- `Esc` — przerwij agenta w trakcie
- Własne komendy: pliki `.md` w `.claude/commands/`

---

## 6. CLAUDE.md

Plik z instrukcjami dla agenta, wczytywany automatycznie na starcie każdej sesji.
Miejsce na to, czego nie widać z samego kodu.

| Lokalizacja | Zasięg |
|---|---|
| `~/.claude/CLAUDE.md` | wszystkie projekty (osobiste preferencje) |
| `./CLAUDE.md` | ten projekt, wspólny — commitowany do repo |
| `./CLAUDE.local.md` | ten projekt, prywatny — w `.gitignore` |
| `podkatalog/CLAUDE.md` | wczytywany, gdy agent pracuje w tym podkatalogu |

Co wpisać:
- komendy projektu (build, test, lint, uruchomienie)
- konwencje (styl, nazewnictwo, struktura commitów)
- czego NIE ruszać (wygenerowane pliki, katalogi legacy)
- kontekst architektury nieoczywisty z kodu

Czego nie wpisywać: rzeczy widocznych z kodu, długich opisów, całej dokumentacji.
Im krótszy i konkretniejszy, tym lepiej — zajmuje kontekst w każdej sesji.

Przykład:

```markdown
# Projekt: nauka-ai

## Komendy
- Testy: `pytest -q`
- Lint: `ruff check .`

## Konwencje
- Notatki po polsku, w katalogu notatki/
- Commity po polsku, tryb rozkazujący
- Tabele i przykłady komend zamiast streszczeń

## Nie ruszać
- notatki/modul-1-cli-referencja.md — wersja zamknięta
```

Start: `/init` generuje szkielet na podstawie repo. Potem dopisuje się `#` albo `/memory`.

---

## 7. Ściąga

```bash
# Uruchamianie
claude                              # sesja interaktywna
claude "zadanie"                    # sesja z promptem na start
claude -p "zadanie"                 # jednorazowa odpowiedź, bez rozmowy
claude -c                           # wznów ostatnią sesję
claude -r                           # wybierz sesję do wznowienia
claude --permission-mode plan "..." # tryb tylko-analiza
claude --model claude-opus-5        # wybór modelu

# W sesji
/clear            # wyczyść kontekst przed nowym zadaniem
/compact          # streść rozmowę
/context          # ile kontekstu zużyte
/init             # wygeneruj CLAUDE.md
/permissions      # reguły uprawnień
/review           # przegląd zmian
Shift+Tab         # przełącz tryb uprawnień
Esc               # przerwij agenta
!git status       # shell w rozmowie
@src/api.py       # wstaw plik do promptu
#zawsze po polsku # dopisz do CLAUDE.md
```

---

## 8. Pytania na test

1. Czym agent CLI różni się od autouzupełniania kodu w edytorze?
2. Na czym polega pętla działania agenta?
3. Kiedy użyć `claude -p` zamiast trybu interaktywnego?
4. Do czego służy `claude -c`, a do czego `claude -r`?
5. Wymień cztery tryby uprawnień i po jednym scenariuszu dla każdego.
6. Czym `acceptEdits` różni się od `bypassPermissions`?
7. W jakim trybie agent niczego nie zmienia? Co zwraca na końcu?
8. Gdzie trzymać stałe reguły uprawnień zamiast zatwierdzać je co sesję?
9. Jaka jest kolejność nadpisywania plików `settings.json` (globalny → lokalny)?
10. Czym różni się sesja od kontekstu?
11. Co robi `/clear`, a czego nie robi (czy kończy sesję)?
12. Kiedy następuje automatyczna kompakcja i co się wtedy dzieje?
13. Po co `/context`?
14. Do czego służą `!`, `@` i `#` w prompcie?
15. Gdzie umieścić `CLAUDE.md` prywatny, żeby nie trafił do repo?
16. Co wpisać do `CLAUDE.md`, a czego tam nie umieszczać i dlaczego?
17. Który `CLAUDE.md` wczytuje się przy pracy w podkatalogu?
18. Co robi `/init`?
19. Dlaczego zbyt długi `CLAUDE.md` jest problemem?
20. Opisz workflow: nowe zadanie w repo → wybór trybu → praca → weryfikacja → commit.
