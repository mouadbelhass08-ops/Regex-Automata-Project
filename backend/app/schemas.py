"""API contract: the shapes exchanged between backend and frontend.

Decisions captured here:
  * One shared Automaton shape for NFA, DFA and minimized DFA.
  * Epsilon transitions are represented by symbol=None.
  * The response is an object (not a bare automaton) so that an optional
    `steps` field can be added later without breaking existing clients.
"""

from typing import Literal

from pydantic import BaseModel, Field


class State(BaseModel):
    id: int
    label: str  # display name, e.g. "q0" or "{q0,q1}" for DFA subset states


class Transition(BaseModel):
    source: int
    target: int
    symbol: str | None  # None means epsilon (NFA only)


class Automaton(BaseModel):
    type: Literal["NFA", "DFA", "MIN_DFA"]
    states: list[State]
    alphabet: list[str]
    transitions: list[Transition]
    start: int
    accepting: list[int]


class AnalyzeRequest(BaseModel):
    regex: str = Field(min_length=1, max_length=200)
    test_strings: list[str] = Field(default_factory=list)


class MatchResult(BaseModel):
    input: str
    nfa_accepts: bool
    dfa_accepts: bool
    min_dfa_accepts: bool


class AnalyzeResponse(BaseModel):
    regex: str
    nfa: Automaton
    dfa: Automaton
    min_dfa: Automaton
    results: list[MatchResult]
    # steps: list[Step] | None = None   # reserved for step-by-step mode (later)
