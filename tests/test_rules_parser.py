"""Spec for the rule parser. Week 2.

Every test here is ``xfail(strict=True)``. When you implement the parser these
start XPASSing, which fails the build until you delete the marker. That is
deliberate: it forces the spec and the code to stay in step.

Cases are drawn from real OoT Randomizer ``data/World/*.json`` rule strings.
"""

import pytest

from pylon.rules.ast import And, HasItem, Literal, Macro, Not, Or, Setting
from pylon.rules.parser import ParseError, Vocabulary, parse

xfail_week2 = pytest.mark.xfail(
    raises=NotImplementedError, strict=True, reason="week 2: parser not implemented"
)


@xfail_week2
def test_bare_identifier_is_an_item():
    assert parse("Kokiri_Sword") == HasItem("Kokiri_Sword")


@xfail_week2
def test_and_of_two_items():
    assert parse("Bow and Bomb_Bag") == And((HasItem("Bow"), HasItem("Bomb_Bag")))


@xfail_week2
def test_or_of_two_items():
    assert parse("Bow or Slingshot") == Or((HasItem("Bow"), HasItem("Slingshot")))


@xfail_week2
def test_and_binds_tighter_than_or():
    """``a or b and c`` parses as ``a or (b and c)``."""
    assert parse("A or B and C") == Or((HasItem("A"), And((HasItem("B"), HasItem("C")))))


@xfail_week2
def test_parentheses_override_precedence():
    assert parse("(A or B) and C") == And((Or((HasItem("A"), HasItem("B"))), HasItem("C")))


@xfail_week2
def test_not_binds_tighter_than_and():
    assert parse("not A and B") == And((Not(HasItem("A")), HasItem("B")))


@xfail_week2
def test_macro_call_with_one_arg():
    """Real OoT rule string."""
    assert parse("can_play(Prelude_of_Light)", Vocabulary(macros=frozenset({"can_play"}))) == Macro(
        "can_play", ("Prelude_of_Light",)
    )


@xfail_week2
def test_macro_call_with_no_args():
    vocab = Vocabulary(macros=frozenset({"can_leave_forest"}))
    assert parse("can_leave_forest", vocab) == Macro("can_leave_forest", ())


@xfail_week2
def test_setting_comparison():
    """From OoT ``Overworld.json``: ``open_kakariko == 'open'``."""
    vocab = Vocabulary(settings=frozenset({"open_kakariko"}))
    assert parse("open_kakariko == 'open'", vocab) == Setting("open_kakariko", "open")


@xfail_week2
def test_real_oot_rule_from_root_region():
    """Verbatim from OoT ``Overworld.json``, region ``Root``."""
    vocab = Vocabulary(
        macros=frozenset({"can_play", "can_leave_forest"}),
        settings=frozenset({"open_kakariko"}),
        items=frozenset({"Zeldas_Letter"}),
    )
    parsed = parse("open_kakariko == 'open' or (open_kakariko == 'zelda' and Zeldas_Letter)", vocab)
    assert parsed == Or(
        (
            Setting("open_kakariko", "open"),
            And((Setting("open_kakariko", "zelda"), HasItem("Zeldas_Letter"))),
        )
    )


@xfail_week2
def test_boolean_literals():
    assert parse("True") == Literal(True)
    assert parse("False") == Literal(False)


@xfail_week2
def test_unbalanced_parenthesis_raises_parse_error():
    with pytest.raises(ParseError):
        parse("(A and B")


@xfail_week2
def test_trailing_operator_raises_parse_error():
    with pytest.raises(ParseError):
        parse("A and")


@xfail_week2
def test_empty_string_raises_parse_error():
    with pytest.raises(ParseError):
        parse("")


@xfail_week2
def test_parse_error_reports_position():
    """Ingest needs to say which upstream rule failed, not just that one did."""
    with pytest.raises(ParseError) as exc:
        parse("A and and B")
    assert exc.value.position > 0
