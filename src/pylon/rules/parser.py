"""Tokenizer and recursive-descent parser for source rule strings.

Grammar, lowest precedence first::

    expr    := or_expr
    or_expr := and_expr ( "or" and_expr )*
    and_expr:= unary ( "and" unary )*
    unary   := "not" unary | primary
    primary := "(" expr ")"
             | IDENT "(" arglist? ")"        -> Macro
             | IDENT "==" value              -> Setting
             | IDENT                         -> HasItem | Macro | Literal
             | "True" | "False"              -> Literal

Whether a bare identifier is an item, a macro, or a setting is not decidable from
syntax alone. The parser takes an optional vocabulary so the adapter, which does
know, can disambiguate. Without one, bare identifiers become ``HasItem``.

⚠️ Never use ``eval``. This is a real parser. See ADR-003.
"""

from dataclasses import dataclass

from pylon.rules.ast import Rule

__all__ = ["ParseError", "Vocabulary", "parse", "tokenize"]


class ParseError(ValueError):
    """Raised when a rule string cannot be parsed.

    Carries the offending position so ingest can report which upstream file and
    line failed, rather than dying with a bare message.
    """

    def __init__(self, message: str, source: str, position: int) -> None:
        super().__init__(f"{message} at position {position}: {source[:80]!r}")
        self.source = source
        self.position = position


@dataclass(frozen=True, slots=True)
class Vocabulary:
    """What the adapter knows about the identifiers in a source.

    Anything not listed is treated as an item.
    """

    items: frozenset[str] = frozenset()
    macros: frozenset[str] = frozenset()
    settings: frozenset[str] = frozenset()
    regions: frozenset[str] = frozenset()


@dataclass(frozen=True, slots=True)
class Token:
    """A lexeme plus where it started, for error reporting."""

    kind: str
    value: str
    position: int


def tokenize(source: str) -> list[Token]:
    """Split a rule string into tokens.

    TODO(week 2). Token kinds: IDENT, LPAREN, RPAREN, COMMA, AND, OR, NOT, EQ,
    STRING, NUMBER, EOF.

    See tests/test_rules_parser.py for the cases that define correct behaviour.
    """
    raise NotImplementedError("week 2")


def parse(source: str, vocabulary: Vocabulary | None = None) -> Rule:
    """Parse a rule string into an AST.

    TODO(week 2). Implement against the xfail tests in tests/test_rules_parser.py,
    removing each marker as it passes.

    Args:
        source: the rule expression, e.g. ``"can_play(Bolero_of_Fire) and is_adult"``.
        vocabulary: optional adapter-supplied hints for classifying bare identifiers.

    Raises:
        ParseError: if the source is not a well-formed expression.
    """
    raise NotImplementedError("week 2")
