---
title: "Moduł 7 — Pluginy Claude Code"
module: 7
author: DevKapi
tags: [pluginy, claude-code, mcp, hooki, marketplace, qa]
status: reference
updated: 2026-09-06
zrodlo: https://code.claude.com/docs/en/plugins-reference
---

# Moduł 7 — Pluginy

## Czym jest plugin

Plugin to **samodzielny katalog z komponentami rozszerzającymi Claude Code**. To jest opakowanie dystrybucyjne: bierzesz kilka rzeczy, które razem tworzą sensowną całość, pakujesz w jeden katalog, dajesz mu nazwę i wersję, i ktoś inny może to zainstalować jedną komendą.

Analogia z QA: skill to pojedyncza procedura testowa. Plugin to **pełny pakiet narzędziowy zespołu** — procedury, szablony, skrypty automatyzujące, integracje z Jirą i zasady, które uruchamiają się same przy pewnych zdarzeniach. Jeden `git clone` i nowy tester ma to samo, co reszta zespołu.

## Skill kontra plugin — czym się różnią

To pytanie prawie na pewno padnie na teście, więc rozbiję je porządnie.

| | Skill | Plugin |
|---|---|---|
| Czym jest | katalog z `SKILL.md` | katalog z komponentami i manifestem |
| Zawartość | instrukcja tekstowa dla modelu | skille, agenci, hooki, serwery MCP, serwery LSP, monitory, motywy, style wyjścia, pliki wykonywalne |
| Może uruchamiać kod | pośrednio, przez skrypty i wstrzykiwanie komend | tak, w tym automatycznie przy zdarzeniach |
| Reaguje na zdarzenia | nie | tak, przez hooki |
| Łączy się z systemami zewnętrznymi | nie | tak, przez MCP |
| Dystrybucja | skopiowanie katalogu, commit do repo | marketplace, `claude plugin install`, wersjonowanie |
| Wersjonowanie i zależności | brak | `version`, `dependencies`, aktualizacje |
| Relacja | — | **plugin może zawierać wiele skilli** |

Kluczowe zdanie do zapamiętania: **skill dodaje wiedzę i procedurę, plugin dodaje możliwości i infrastrukturę.** Skill mówi modelowi *jak coś zrobić*. Plugin daje modelowi *nowe rzeczy, które może zrobić*, i może wykonywać działania nawet wtedy, gdy model o nic nie prosi (hooki).

I odwrotna strona tej relacji: jeżeli masz jeden skill i chcesz go dać zespołowi — nie potrzebujesz pluginu, wystarczy `.claude/skills/` w repo. Plugin bierzesz wtedy, gdy potrzebujesz wielu komponentów, automatyzacji przy zdarzeniach albo prawdziwej dystrybucji z wersjami.

## Jak pluginy rozszerzają możliwości agenta — komponenty po kolei

### Skille

Plugin może zawierać skille, które trafiają do `skills/` w korzeniu pluginu. Zasady z modułu 6 obowiązują bez zmian, z jednym dodatkiem: skille z pluginu dostają **przestrzeń nazw** — `my-plugin/skills/review/SKILL.md` staje się `/my-plugin:review`. Dzięki temu nie kolidują z twoimi własnymi skillami.

W skillu z pluginu pole `name` z Front Mattera **ustawia ostatni człon komendy** — inaczej niż w skillu osobistym, gdzie decyduje nazwa katalogu.

Istnieje też starszy katalog `commands/` z płaskimi plikami `.md`. Działa dalej, ale w nowych pluginach używa się `skills/`.

### Agenci (subagenci)

Katalog `agents/`, pliki `.md` z Front Matterem. Subagent to wyspecjalizowany "pracownik" z własnym promptem systemowym, własnym kontekstem i ograniczonym zestawem narzędzi. Główny model może mu delegować zadanie, dostać wynik i nie zaśmiecić sobie kontekstu całą pracą pośrednią.

```markdown
---
name: security-reviewer
description: Sprawdza zmiany pod kątem podatności bezpieczeństwa i wskazuje ryzykowne wzorce
model: sonnet
effort: medium
maxTurns: 20
disallowedTools: Write, Edit
---

Jesteś recenzentem bezpieczeństwa. Dla każdego zmienionego pliku sprawdź:
1. Dane wejściowe użytkownika trafiające do zapytań SQL bez parametryzacji
2. Sekrety zapisane na sztywno w kodzie
3. Brakującą walidację uprawnień w endpointach
Zwróć listę znalezisk z plikiem i numerem linii. Nie modyfikuj plików.
```

Agenci z pluginu obsługują pola `name`, `description`, `model`, `effort`, `maxTurns`, `tools`, `disallowedTools`, `skills`, `memory`, `background`, `isolation`. Ze względów bezpieczeństwa **nie wolno** im deklarować `hooks`, `mcpServers` ani `permissionMode`.

W interfejsie widać ich pod nazwą z prefiksem: `my-plugin:security-reviewer`.

### Hooki — automatyzacja reagująca na zdarzenia

To jest komponent, który najbardziej odróżnia plugin od skilla. Hook to **komenda uruchamiana automatycznie, gdy zajdzie określone zdarzenie**. Model o tym nie decyduje i nie może tego pominąć — to działa deterministycznie, na poziomie narzędzia.

Analogia z QA jest niemal dosłowna: hook to **git hook albo trigger w pipeline CI**. "Po każdym zapisie pliku uruchom formatter." "Przed uruchomieniem komendy w bashu sprawdź, czy nie zawiera `rm -rf`." "Na starcie sesji zainstaluj zależności."

Konfiguracja leży w `hooks/hooks.json` w korzeniu pluginu:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"${CLAUDE_PLUGIN_ROOT}\"/scripts/format-code.sh"
          }
        ]
      }
    ]
  }
}
```

Czytanie tego: klucz `PostToolUse` to zdarzenie. `matcher` to wzorzec (wyrażenie regularne) dopasowujący nazwę narzędzia — tutaj `Write` albo `Edit`. `hooks` to lista akcji do wykonania. `type: command` znaczy "uruchom komendę powłoki". Zmienna `${CLAUDE_PLUGIN_ROOT}` rozwija się do katalogu instalacji pluginu.

Zdarzenia, które warto znać na pamięć, bo są najczęściej używane:

| Zdarzenie | Kiedy się odpala |
|---|---|
| `SessionStart` | start albo wznowienie sesji |
| `UserPromptSubmit` | po wysłaniu przez ciebie promptu, przed przetworzeniem |
| `PreToolUse` | przed wywołaniem narzędzia — **może je zablokować** |
| `PostToolUse` | po udanym wywołaniu narzędzia |
| `PostToolUseFailure` | po nieudanym wywołaniu narzędzia |
| `PermissionRequest` | gdy wywołanie narzędzia wymaga decyzji o uprawnieniach |
| `Stop` | gdy Claude kończy odpowiedź |
| `SubagentStart` / `SubagentStop` | uruchomienie i zakończenie subagenta |
| `PreCompact` / `PostCompact` | przed i po kompaktowaniu kontekstu |
| `FileChanged` | gdy obserwowany plik zmieni się na dysku |
| `SessionEnd` | zakończenie sesji |

Pełna lista jest dłuższa (są zdarzenia dla worktree, zmiany modelu, zmiany katalogu roboczego, elicitacji MCP i inne), ale te powyżej pokrywają 90% zastosowań.

Typy hooków: `command` (komenda powłoki), `http` (POST z JSON-em zdarzenia pod URL), `mcp_tool` (wywołanie narzędzia serwera MCP), `prompt` (ocena promptem przez model), `agent` (uruchomienie agentowego weryfikatora).

Nazwy zdarzeń są **wrażliwe na wielkość liter**: `PostToolUse`, nie `postToolUse`. To pierwsza rzecz do sprawdzenia, gdy hook nie działa. Druga: czy skrypt ma prawo wykonywania (`chmod +x`).

### Serwery MCP — połączenie ze światem zewnętrznym

MCP to Model Context Protocol — otwarty standard, który pozwala podłączyć do agenta zewnętrzne narzędzia i źródła danych. Serwer MCP wystawia narzędzia, a Claude Code widzi je tak samo jak swoje wbudowane.

To jest sposób, w jaki agent zaczyna umieć rzeczy, których w ogóle nie potrafił: czytać zgłoszenia z Jiry, odpytywać bazę danych, sprawdzać status deploya, pobierać wyniki z narzędzia testowego.

Konfiguracja w `.mcp.json` w korzeniu pluginu:

```json
{
  "mcpServers": {
    "plugin-database": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_PATH": "${CLAUDE_PLUGIN_DATA}/data"
      }
    },
    "plugin-api-client": {
      "command": "npx",
      "args": ["@company/mcp-server", "--plugin-mode"]
    }
  }
}
```

Serwery MCP z pluginu startują automatycznie, gdy plugin jest włączony, i ich narzędzia pojawiają się w zestawie modelu.

### Serwery LSP — inteligencja kodu

LSP to Language Server Protocol, ten sam, którego używa twój edytor do "przejdź do definicji" i "znajdź użycia". Plugin może dostarczyć konfigurację serwera LSP w `.lsp.json`, dzięki czemu Claude dostaje realną nawigację po kodzie i diagnostykę zamiast zgadywania z treści plików.

```json
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": { ".go": "go" }
  }
}
```

Ważne zastrzeżenie: **plugin LSP nie zawiera samego serwera językowego**. Konfiguruje tylko połączenie. Binarkę (`pyright`, `typescript-language-server`, `rust-analyzer`) instalujesz osobno. Komunikat `Executable not found in $PATH` w zakładce Errors interfejsu `/plugin` oznacza właśnie to.

Oficjalne pluginy LSP dostępne w marketplace: `pyright-lsp`, `typescript-lsp`, `rust-analyzer-lsp`.

### Monitory, motywy, style wyjścia, pliki wykonywalne

Dla kompletności, bo mogą paść w pytaniu o to, co plugin potrafi. **Monitory** (`monitors/monitors.json`) to procesy działające w tle przez całą sesję, których każda linia wyjścia trafia do Claude jako powiadomienie — na przykład `tail -F logs/error.log`. **Motywy** (`themes/`) to schematy kolorów widoczne w `/theme`. **Style wyjścia** (`output-styles/`) zmieniają sposób, w jaki Claude formatuje odpowiedzi. **`bin/`** to katalog, którego zawartość trafia do `PATH` narzędzia Bash, więc twoje skrypty stają się wywoływalne jak zwykłe komendy.

## Struktura katalogów pluginu

```text
enterprise-plugin/
├── .claude-plugin/
│   └── plugin.json           # manifest — JEDYNY plik w tym katalogu
├── skills/                   # skille
│   ├── code-reviewer/
│   │   └── SKILL.md
│   └── pdf-processor/
│       ├── SKILL.md
│       └── scripts/
├── commands/                 # starsza forma skilli: płaskie pliki .md
├── agents/                   # definicje subagentów
│   └── security-reviewer.md
├── workflows/                # skrypty workflow
├── output-styles/            # style wyjścia
├── themes/                   # motywy kolorów
├── monitors/
│   └── monitors.json         # monitory działające w tle
├── hooks/
│   └── hooks.json            # konfiguracja hooków
├── bin/                      # pliki wykonywalne trafiające do PATH
├── settings.json             # domyślne ustawienia pluginu
├── .mcp.json                 # serwery MCP
├── .lsp.json                 # serwery LSP
├── scripts/                  # skrypty pomocnicze wywoływane z hooków
├── README.md
├── LICENSE
└── CHANGELOG.md
```

**Najważniejsza reguła strukturalna całego modułu:** w katalogu `.claude-plugin/` leży **wyłącznie** `plugin.json`. Wszystkie pozostałe katalogi — `skills/`, `agents/`, `hooks/`, `commands/` — muszą być w **korzeniu pluginu**, nie w środku `.claude-plugin/`.

To jest najczęstszy błąd początkujących i ma bardzo charakterystyczny objaw: **plugin ładuje się bez błędu, ale komponenty nie istnieją**. Nie ma komunikatu, nie ma ostrzeżenia. Po prostu skille się nie pojawiają. Kolejna cicha awaria — ten sam wzorzec, co brak delimitera Front Mattera z modułu 5.

Druga rzecz, o której warto wiedzieć: `CLAUDE.md` w korzeniu pluginu **nie jest ładowany** jako kontekst projektu. Jeżeli chcesz, żeby plugin wnosił instrukcje do kontekstu, zapakuj je w skill.

## Manifest `plugin.json`

Manifest jest **opcjonalny**. Jeżeli go nie ma, Claude Code sam wykrywa komponenty w domyślnych lokalizacjach, a nazwę pluginu bierze z nazwy katalogu. Manifest robisz wtedy, gdy chcesz dodać metadane albo wskazać niestandardowe ścieżki.

Jeżeli manifest jest, **jedynym wymaganym polem jest `name`**.

Pełny przykład z komentarzem, co do czego:

```json
{
  "name": "qa-toolkit",
  "displayName": "QA Toolkit",
  "version": "1.2.0",
  "description": "Narzędzia QA: raporty błędów, analiza logów, generowanie przypadków testowych",
  "author": {
    "name": "Kacper",
    "email": "kacper@example.com",
    "url": "https://github.com/DevKapi"
  },
  "homepage": "https://github.com/DevKapi/qa-toolkit",
  "repository": "https://github.com/DevKapi/qa-toolkit",
  "license": "MIT",
  "keywords": ["qa", "testing", "bug-report"],
  "skills": "./custom/skills/",
  "commands": ["./custom/commands/special.md"],
  "agents": ["./custom/agents/reviewer.md"],
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json",
  "defaultEnabled": true
}
```

Pola metadanych i ich znaczenie:

| Pole | Znaczenie |
|---|---|
| `name` | **Wymagane.** Identyfikator w kebab-case, bez spacji. Służy do przestrzeni nazw komponentów. |
| `displayName` | Nazwa czytelna dla człowieka, pokazywana w interfejsie. Może mieć spacje. |
| `version` | Wersja semantyczna. Ustawienie jej **przypina** plugin do tej wersji: użytkownicy dostaną aktualizację dopiero, gdy ją podbijesz. |
| `description` | Krótki opis przeznaczenia. |
| `author` | Obiekt z `name`, `email`, `url`. |
| `homepage`, `repository`, `license`, `keywords` | Metadane katalogowe. |
| `metadata` | Dowolny obiekt na twoje dane; Claude Code go nie czyta. |
| `defaultEnabled` | Czy plugin startuje włączony, gdy użytkownik nic nie ustawił. Domyślnie `true`. |
| `dependencies` | Inne pluginy wymagane przez ten, opcjonalnie z zakresem wersji. |
| `userConfig` | Wartości, o które Claude Code zapyta użytkownika przy włączaniu pluginu (np. token API). |

Pola ze ścieżkami komponentów mają **jedną niuansową regułę**, którą warto znać, bo bywa pytaniem. Dla `commands`, `agents`, `workflows`, `outputStyles`, `experimental.themes` i `experimental.monitors` podanie własnej ścieżki **zastępuje** domyślny katalog — czyli jeśli wpiszesz `"commands": "./extras/"`, to domyślny `commands/` przestaje być skanowany. Dla `skills` jest odwrotnie: podana ścieżka **dokłada się** do domyślnego `skills/`, który jest skanowany zawsze.

Wszystkie ścieżki muszą być względne wobec korzenia pluginu i zaczynać się od `./`.

**Nieznane pola** są ignorowane przy ładowaniu, a `claude plugin validate` zgłasza je jako ostrzeżenia, nie błędy. Dzięki temu jeden manifest może służyć też jako `package.json` czy manifest rozszerzenia edytora. Ale to znaczy też, że literówka w nazwie pola nie zatrzyma ładowania — tylko po cichu wyłączy funkcję. Stąd `--strict` w CI, o którym za chwilę.

Zła **wartość** rozpoznanego pola to inna sprawa: dla większości pól plugin się wtedy **nie załaduje** (np. `keywords` podane jako string zamiast tablicy to błąd ładowania).

## Zmienne środowiskowe — trzy, które trzeba znać

| Zmienna | Wskazuje na | Do czego |
|---|---|---|
| `${CLAUDE_PLUGIN_ROOT}` | katalog instalacji pluginu | skrypty, binarki i pliki konfiguracyjne dostarczone z pluginem |
| `${CLAUDE_PLUGIN_DATA}` | katalog trwały, przeżywający aktualizacje | zainstalowane zależności, cache, generowane pliki |
| `${CLAUDE_PROJECT_DIR}` | korzeń projektu | skrypty i konfiguracja lokalne dla projektu |

Dlaczego to jest ważne, a nie kosmetyczne: plugin instaluje się w **różnych miejscach** w zależności od systemu, sposobu instalacji i wersji. Ścieżka zaszyta na sztywno (`/home/kapi/plugins/...`) zadziała tylko u ciebie. Ścieżka względna (`./scripts/...`) rozwinie się względem katalogu roboczego sesji, czyli w praktyce cudzego projektu. Tylko `${CLAUDE_PLUGIN_ROOT}` daje poprawny wynik zawsze.

Dodatkowo: `${CLAUDE_PLUGIN_ROOT}` **zmienia się przy każdej aktualizacji pluginu**, bo każda wersja to osobny katalog w cache. Dlatego nigdy nie zapisuj tam stanu — od tego jest `${CLAUDE_PLUGIN_DATA}`.

W hookach w formie powłokowej opakuj zmienną w cudzysłowy: `"\"${CLAUDE_PLUGIN_ROOT}\"/scripts/process.sh"` — inaczej spacja w ścieżce rozbije komendę.

## Marketplace — skąd biorą się pluginy

Marketplace to **katalog pluginów**: repozytorium (najczęściej na GitHubie) z plikiem `.claude-plugin/marketplace.json`, który wylicza dostępne pluginy i mówi, gdzie leży każdy z nich.

Uproszczony schemat:

```json
{
  "name": "moj-marketplace",
  "owner": {
    "name": "Kacper",
    "url": "https://github.com/DevKapi"
  },
  "plugins": [
    {
      "name": "qa-toolkit",
      "source": "./plugins/qa-toolkit",
      "description": "Narzędzia QA"
    }
  ]
}
```

Źródłem pluginu (`source`) może być ścieżka względna w tym samym repo, repozytorium GitHub, dowolne repo Git, archiwum ZIP, paczka npm albo komenda produkująca katalog.

Przepływ jest dwuetapowy i to jest częste pytanie: **najpierw dodajesz marketplace, dopiero potem instalujesz z niego plugin.** Nie da się zainstalować pluginu, którego marketplace nie jest znany.

```bash
claude plugin marketplace add anthropics/claude-plugins-official
claude plugin install skill-creator@claude-plugins-official
```

Zapis `nazwa-pluginu@nazwa-marketplace` jednoznacznie wskazuje, skąd bierzesz plugin — przydaje się, gdy dwa marketplace mają plugin o tej samej nazwie.

## Instalacja i cykl życia — komendy CLI

Wszystkie te komendy mają też odpowiedniki wewnątrz sesji, wpisywane jako `/plugin ...`. Wersje z terminala (`claude plugin ...`) nadają się do skryptów i CI, bo zwracają kody wyjścia.

**Zarządzanie marketplace'ami:**

```bash
claude plugin marketplace add <źródło>      # dodaj katalog pluginów
claude plugin marketplace list              # pokaż znane marketplace
claude plugin marketplace update <nazwa>    # odśwież listę pluginów
claude plugin marketplace remove <nazwa>    # usuń
```

**Instalacja i usuwanie:**

```bash
claude plugin install <plugin>@<marketplace>
claude plugin install qa-toolkit@moj-marketplace --scope project
claude plugin uninstall qa-toolkit          # aliasy: remove, rm
claude plugin uninstall qa-toolkit --keep-data   # zachowaj katalog danych
claude plugin uninstall qa-toolkit --prune       # usuń też osierocone zależności
```

**Włączanie i wyłączanie bez odinstalowywania:**

```bash
claude plugin enable qa-toolkit
claude plugin disable qa-toolkit
claude plugin disable --all
```

Różnica, którą trzeba rozumieć: `disable` zostawia pliki na dysku i wyłącza plugin z sesji; `uninstall` usuwa go z cache i domyślnie kasuje jego katalog danych. Przy diagnozowaniu "czy to plugin robi problem" używasz `disable`.

**Przegląd i diagnostyka:**

```bash
claude plugin list                  # zainstalowane, z wersją, źródłem i statusem
claude plugin list --json
claude plugin details qa-toolkit    # spis komponentów i szacowany koszt tokenowy
claude --debug                      # szczegóły ładowania pluginów przy starcie
```

`claude plugin details` jest bardzo pouczające, bo rozbija koszt na dwie liczby: **always-on** (tokeny dokładane do każdej sesji przez sam listing komponentów) i **on-invoke** (koszt jednorazowego uruchomienia komponentu). To jest realny budżet, który wydajesz na trzymanie pluginu włączonym.

**Tworzenie nowego pluginu:**

```bash
claude plugin init moj-plugin
claude plugin init moj-plugin --with skills hooks
claude plugin init moj-plugin --with skills agents hooks mcp --force
```

Komenda tworzy szkielet w `~/.claude/skills/<nazwa>/`, który przy następnej sesji ładuje się automatycznie jako plugin `<nazwa>@skills-dir` — bez marketplace i bez instalacji. Dostępne wartości `--with`: `skills`, `agents`, `hooks`, `mcp`, `lsp`, `output-style`, `channel`.

**Walidacja:**

```bash
claude plugin validate ./moj-plugin
claude plugin validate ./moj-plugin --strict
claude plugin validate ./moj-plugin --json
echo "kod wyjścia: $?"
```

Kody wyjścia, do zapamiętania: **0** — walidacja przeszła, **1** — walidacja nie przeszła, **2** — sama walidacja się nie powiodła (np. ścieżka nieczytelna). To rozróżnienie ma znaczenie w CI: kod 2 to nie "plugin jest zły", tylko "coś jest nie tak z uruchomieniem".

`--strict` zamienia ostrzeżenia w błędy. To jest **to, czego używa się w CI**, bo domyślnie literówka w nazwie pola przechodzi jako ostrzeżenie i plugin się ładuje z po cichu wyłączoną funkcją. W pipeline chcesz to złapać przed publikacją, a nie po zgłoszeniach użytkowników. To jest dokładnie ta sama filozofia, co traktowanie ostrzeżeń kompilatora jako błędów.

## Zakresy instalacji

| Zakres | Plik ustawień | Do czego |
|---|---|---|
| `user` | `~/.claude/settings.json` | twoje osobiste pluginy, we wszystkich projektach — **domyślny** |
| `project` | `.claude/settings.json` | pluginy zespołowe, wersjonowane w Gicie |
| `local` | `.claude/settings.local.json` | pluginy dla tego projektu, ale nieudostępniane |
| `managed` | ustawienia zarządzane | pluginy narzucone przez organizację, tylko do odczytu |

`--scope project` jest tym, o co chodzi przy pracy zespołowej: zapisuje wpis do `enabledPlugins` w `.claude/settings.json`, który commitujesz. Każdy, kto sklonuje repozytorium, ma ten sam zestaw pluginów bez żadnej ręcznej konfiguracji. To odpowiednik `requirements.txt` albo `package.json` dla środowiska agenta.

Żeby to zadziałało u kolegi z zespołu, marketplace musi być znany także jemu — do tego służy klucz `extraKnownMarketplaces` w tym samym pliku ustawień.

## Pluginy z katalogu skilli

Jest jedna droga na skróty, którą warto znać, bo poznasz ją przy `plugin init`. Jeżeli w katalogu skilla (`~/.claude/skills/foo/` albo `.claude/skills/foo/`) umieścisz plik `.claude-plugin/plugin.json`, to ten katalog ładuje się jako **plugin** o nazwie `foo@skills-dir` — bez marketplace, bez instalacji, przy następnej sesji. Dzięki temu może dodatkowo mieć własnych agentów, hooki i serwery MCP.

Trzy warianty, które trzeba umieć rozróżnić:

| Co masz | Czym to jest |
|---|---|
| `<skills-dir>/foo/SKILL.md` bez manifestu | zwykły skill `foo` |
| `<skills-dir>/foo/.claude-plugin/plugin.json` | plugin `foo@skills-dir` |
| `<plugin>/skills/bar/SKILL.md` | skill `bar` zapakowany w pluginie |

Uwaga na zaufanie: plugin w zakresie projektowym pochodzi z repozytorium, a nie od ciebie, więc ładuje się dopiero po zaakceptowaniu okna zaufania do katalogu roboczego, serwery MCP wymagają osobnej zgody, a monitory w ogóle się nie ładują.

## Wersjonowanie

Trzy podejścia i konsekwencje każdego.

**Wersja jawna** — ustawiasz `"version": "2.1.0"` w `plugin.json`. Użytkownicy dostaną aktualizację **tylko wtedy, gdy podbijesz to pole**. Wypchnięcie nowych commitów bez podbicia wersji nie zrobi nic, a `plugin update` powie "już masz najnowszą". Dobre dla publikowanych pluginów ze stabilnym cyklem wydań.

**Wersja z commita** — pomijasz `version` i w manifeście, i we wpisie marketplace. Wtedy wersją jest SHA commita źródła i użytkownicy dostają zmianę przy każdym nowym commicie. Dobre dla pluginów wewnętrznych w aktywnym rozwoju.

**Wersja z sumy kontrolnej** — dla źródeł typu archiwum ZIP.

Jeżeli używasz wersji jawnych, trzymaj się semantic versioning (`MAJOR.MINOR.PATCH`) i prowadź `CHANGELOG.md`.

## Typowe błędy i ich diagnostyka

| Objaw | Przyczyna | Naprawa |
|---|---|---|
| Plugin się nie ładuje | niepoprawny `plugin.json` | `claude plugin validate ./plugin`, sprawdź składnię JSON |
| Plugin się ładuje, ale nie ma skilli | `skills/` w środku `.claude-plugin/` | przenieś do korzenia pluginu |
| Hook się nie odpala | skrypt bez prawa wykonywania | `chmod +x scripts/hook.sh` |
| Hook się nie odpala | zła wielkość liter w nazwie zdarzenia | `PostToolUse`, nie `postToolUse` |
| Hook się nie odpala | matcher nie pasuje do narzędzia | sprawdź wzorzec, np. `"Write\|Edit"` |
| Serwer MCP nie startuje | ścieżka bez `${CLAUDE_PLUGIN_ROOT}` | użyj zmiennej we wszystkich ścieżkach |
| Błąd ścieżki | ścieżka bezwzględna w manifeście | ścieżki względne zaczynające się od `./` |
| LSP: `Executable not found in $PATH` | brak binarki serwera językowego | zainstaluj serwer osobno |
| Funkcja po cichu nie działa | literówka w nazwie pola manifestu | `claude plugin validate --strict` |

Kolejność diagnostyczna, którą warto mieć w głowie: **najpierw `validate`, potem `--debug`, potem `plugin list`.** `validate` mówi, czy pliki są poprawne. `--debug` pokazuje, co faktycznie zostało załadowane i zarejestrowane. `plugin list` pokazuje, czy plugin jest w ogóle włączony i w którym zakresie. Trzy poziomy — plik, ładowanie, konfiguracja — dokładnie analogicznie do trójwarstwowej diagnostyki Gita, którą już znasz.

## Popularne pluginy i marketplace'y — do sprawdzenia w praktyce

Oficjalny marketplace Anthropic to `anthropics/claude-plugins-official`. Znajdziesz tam między innymi `skill-creator` (ewaluacja i iterowanie skilli, opisany w module 6) oraz pluginy LSP: `pyright-lsp`, `typescript-lsp`, `rust-analyzer-lsp`. Repozytorium `anthropics/claude-code` zawiera własny katalog `plugins/` z przykładami.

Świadomie nie wypisuję tu listy "najpopularniejszych pluginów z GitHuba" z pamięci, bo ekosystem zmienia się z tygodnia na tydzień i podana z głowy lista byłaby nieaktualna albo zmyślona. To jest zadanie do wykonania praktycznie — poniżej.

## Zastosowania w dziale QA

Plugin zespołowy z kompletem skilli QA (raport błędu, checklista przypadku testowego, analiza logu) instalowany przez `--scope project`, żeby cały zespół miał to samo. Hook `PostToolUse` na `Write|Edit`, który po każdej zmianie pliku testowego uruchamia linter testów. Hook `PreToolUse`, który blokuje uruchomienie komend na produkcyjnej bazie. Serwer MCP łączący się z Jirą, żeby agent mógł czytać zgłoszenia i tworzyć tickety bez przełączania kontekstu. Subagent recenzujący pokrycie testami w zmienionych plikach przy każdym PR. Monitor obserwujący log aplikacji na środowisku testowym i zgłaszający Claude każdy nowy błąd.

## Pytania, które mogą paść na teście

Czym plugin różni się od skilla — trzy konkretne różnice. Który plik jest manifestem i gdzie dokładnie leży. Czy manifest jest wymagany i które pole jest w nim jedynym obowiązkowym. Co jest jedynym plikiem, który wolno umieścić w `.claude-plugin/`. Jaki jest objaw umieszczenia `skills/` w złym miejscu. Do czego służy `${CLAUDE_PLUGIN_ROOT}` i dlaczego nie wolno używać ścieżek bezwzględnych. Czym różni się `${CLAUDE_PLUGIN_ROOT}` od `${CLAUDE_PLUGIN_DATA}`. Wymień pięć zdarzeń hooków i powiedz, które z nich może zablokować akcję. Co to jest MCP i co daje pluginowi. Jaka jest kolejność: marketplace czy instalacja pluginu. Co robi `--scope project` i jaki plik zmienia. Do czego służy `--strict` w `plugin validate` i dlaczego akurat w CI. Jakie są kody wyjścia `plugin validate` i co znaczy 2. Czym różni się `disable` od `uninstall`. Jak zachowuje się plugin, gdy ustawisz `version`, a jak gdy go nie ustawisz. Co pokazuje `claude plugin details` i co znaczą "always-on" i "on-invoke".

---

## ZADANIE PRAKTYCZNE — MODUŁ 7

**Zadanie 7.1 [WYŚLIJ]** — Wygeneruj szkielet pluginu i obejrzyj strukturę:

```bash
claude plugin init qa-toolkit --with skills hooks
find ~/.claude/skills/qa-toolkit -type f | sort
cat ~/.claude/skills/qa-toolkit/.claude-plugin/plugin.json
```

Wyślij surowy output obu komend i napisz, który plik leży w `.claude-plugin/`, a które katalogi są w korzeniu.

**Zadanie 7.2 [WYŚLIJ]** — Zwaliduj plugin i pokaż kod wyjścia w dwóch trybach:

```bash
claude plugin validate ~/.claude/skills/qa-toolkit
echo "zwykły: $?"
claude plugin validate ~/.claude/skills/qa-toolkit --strict
echo "strict: $?"
```

**Zadanie 7.3 [WYŚLIJ]** — Celowo złam regułę struktury: przenieś katalog `skills/` do środka `.claude-plugin/`, zrestartuj sesję i sprawdź, czy skille są widoczne. Wyślij, co zaobserwowałeś, i napisz jednym zdaniem, dlaczego to jest cicha awaria. Potem przywróć strukturę.

**Zadanie 7.4 [WYŚLIJ]** — Dopisz do manifestu pole z literówką (np. `"decription"` zamiast `"description"`), uruchom walidację normalną i ze `--strict`, i wyślij oba komunikaty razem z kodami wyjścia. Napisz, dlaczego to uzasadnia użycie `--strict` w CI.

**Zadanie 7.5 [WYŚLIJ]** — Zbadaj ekosystem. Dodaj oficjalny marketplace i wypisz dostępne pluginy:

```bash
claude plugin marketplace add anthropics/claude-plugins-official
claude plugin marketplace list
claude plugin list --json --available | head -60
```

Następnie na GitHubie znajdź trzy repozytoria z pluginami albo marketplace'ami dla Claude Code, posortowane po liczbie gwiazdek. Dla każdego napisz krótką notatkę: nazwa, link, co robi, jakie komponenty zawiera (skille, hooki, agenci, MCP) i jedno konkretne zastosowanie w pracy QA. Wyślij trzy notatki.

**Zadanie 7.6 [WYŚLIJ]** — Zainstaluj `skill-creator` z oficjalnego marketplace, uruchom `claude plugin details skill-creator` i wyślij output. Napisz, co znaczą liczby "always-on" i "on-invoke" w kontekście tego pluginu.
