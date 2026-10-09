# Regex Automata

A web app that turns a regular expression into finite automata and visualizes them.

```
regex -> lexer -> parser (AST) -> NFA -> DFA -> minimized DFA
                                    \-> simulator (runs strings on NFA / DFA / min DFA)
```

## Scope (v1)

- **Syntax:** literal characters, implicit concatenation, `|`, `*`, `?`, `+`, and `( )` grouping.
- **Output:** NFA, DFA and minimized DFA (final results only, no step-by-step mode yet).
- **Simulation:** test strings are run on the NFA (state-set tracking) and on both DFAs.
- **Not in v1:** Character classes ([a-z]), escape sequences (\d, \w), wildcard dot (.), counted repeats ({n,m}), lookarounds, non-capturing groups ((?:...)), and step-by-step construction.

## Stack

| Part     | Tech                         | Port |
|----------|------------------------------|------|
| backend  | Python 3.12, FastAPI, Uvicorn | 8000 |
| frontend | React 18, Vite               | 3000 |

## Run

```bash
docker compose up --build
```

- Frontend: http://localhost:3000 (shows the backend status)
- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

Run the backend tests:

```bash
docker compose exec backend pytest
```

## Backend layout

| Path | Responsibility |
|---|---|
| `app/main.py` | App creation, CORS, router registration |
| `app/api/routes.py` | HTTP endpoints (`POST /api/analyze`) |
| `app/schemas.py` | API contract (Pydantic models) |
| `app/core/lexer.py` | Regex string -> tokens |
| `app/core/ast.py` | Definitions of regex AST node types |
| `app/core/parser.py` | Tokens -> AST (postfix `*`, `+`, `?` > concatenation > alternation `\|`) |
| `app/core/nfa.py` | AST -> NFA (Thompson's construction) |
| `app/core/dfa.py` | NFA -> DFA (subset construction) and DFA minimization |
| `app/core/simulator.py` | Run a string on an NFA or DFA |
| `app/serializers/json_serializer.py` | Internal automata -> `Automaton` schema |

## API contract

`POST /api/analyze`

```json
{ "regex": "a(b|c)*", "test_strings": ["abc", "b"] }
```

The request requires a non-empty `regex` of at most 200 characters. `test_strings`
is optional and defaults to an empty list.

The intended response contains the input `regex`, `nfa`, `dfa`, and `min_dfa`
(each an `Automaton`), plus `results`. Each result contains the tested `input`
and its `nfa_accepts`, `dfa_accepts`, and `min_dfa_accepts` booleans. An
`Automaton` has a `type` (`NFA`, `DFA`, or `MIN_DFA`), `states` (`id`, `label`),
`alphabet`, `transitions` (`source`, `target`, `symbol`; `null` represents an
epsilon transition), `start`, and `accepting`.

The response is an object, leaving room to add an optional `steps` field later.
The schema describes the intended successful response; the endpoint currently
returns `501 Not Implemented` until the core pipeline is implemented.

## Status

Scaffold only: containers, health check, API schema and tests are in place. The `core/` modules are stubs.
