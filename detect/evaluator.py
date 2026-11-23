"""Evaluate a parsed Sigma rule directly against an event dict.

pySigma parses the rule and resolves its condition into a tree of AND/OR/NOT
nodes whose leaves compare one field to one value. This module walks that tree.
It covers the subset of Sigma the starter rules use; anything else raises
NotImplementedError so an unsupported rule fails loudly in CI instead of
silently never matching.
"""

from __future__ import annotations

import ipaddress
import re
from pathlib import Path
from typing import Any

from sigma.conditions import (
    ConditionAND,
    ConditionFieldEqualsValueExpression,
    ConditionNOT,
    ConditionOR,
    ConditionValueExpression,
)
from sigma.rule import SigmaRule
from sigma.types import (
    SigmaCIDRExpression,
    SigmaNull,
    SigmaNumber,
    SigmaRegularExpression,
    SigmaRegularExpressionFlag,
    SigmaString,
    SpecialChars,
)

Event = dict[str, Any]

REGEX_FLAGS = {
    SigmaRegularExpressionFlag.IGNORECASE: re.IGNORECASE,
    SigmaRegularExpressionFlag.MULTILINE: re.MULTILINE,
    SigmaRegularExpressionFlag.DOTALL: re.DOTALL,
}


def load_rule(path: str | Path) -> SigmaRule:
    return SigmaRule.from_yaml(Path(path).read_text(encoding="utf-8"))


def matches(rule: SigmaRule, event: Event) -> bool:
    """True if any of the rule's conditions matches the event."""
    return any(_eval(cond.parse(), event) for cond in rule.detection.parsed_condition)


def _eval(node: Any, event: Event) -> bool:
    if isinstance(node, ConditionAND):
        return all(_eval(arg, event) for arg in node.args)
    if isinstance(node, ConditionOR):
        return any(_eval(arg, event) for arg in node.args)
    if isinstance(node, ConditionNOT):
        return not _eval(node.args[0], event)
    if isinstance(node, ConditionFieldEqualsValueExpression):
        return _match_value(node.value, event.get(node.field))
    if isinstance(node, ConditionValueExpression):
        # Keyword search: match against every field value of the event.
        return any(_match_value(node.value, v) for v in event.values())
    raise NotImplementedError(f"unsupported condition node: {type(node).__name__}")


def _match_value(expected: Any, actual: Any) -> bool:
    if isinstance(expected, SigmaNull):
        return actual is None or actual == ""
    if actual is None:
        return False
    if isinstance(expected, SigmaNumber):
        try:
            return float(actual) == float(expected.number)
        except (TypeError, ValueError):
            return False
    if isinstance(expected, SigmaString):
        # Sigma string matching is case-insensitive and anchored.
        return _wildcard_regex(expected).fullmatch(str(actual)) is not None
    if isinstance(expected, SigmaRegularExpression):
        flags = 0
        for flag in expected.flags:
            flags |= REGEX_FLAGS[flag]
        return re.search(str(expected.regexp), str(actual), flags) is not None
    if isinstance(expected, SigmaCIDRExpression):
        try:
            return ipaddress.ip_address(str(actual)) in expected.network
        except ValueError:
            return False
    raise NotImplementedError(f"unsupported value type: {type(expected).__name__}")


def _wildcard_regex(value: SigmaString) -> re.Pattern[str]:
    parts = []
    for part in value.s:
        if part is SpecialChars.WILDCARD_MULTI:
            parts.append(".*")
        elif part is SpecialChars.WILDCARD_SINGLE:
            parts.append(".")
        elif isinstance(part, str):
            parts.append(re.escape(part))
        else:
            raise NotImplementedError(f"unsupported string part: {part!r}")
    return re.compile("".join(parts), re.IGNORECASE | re.DOTALL)


def applies(
    rule: SigmaRule, product: str | None, service: str | None, category: str | None
) -> bool:
    """True if the event's logsource is one the rule is written for (unset rule keys match all)."""
    ls = rule.logsource
    return all(
        want is None or want == have
        for want, have in ((ls.product, product), (ls.service, service), (ls.category, category))
    )


def condition_fields(rule: SigmaRule) -> set[str]:
    """Field names the rule's conditions compare, for the alert summary."""
    found: set[str] = set()

    def walk(node: Any) -> None:
        if isinstance(node, ConditionFieldEqualsValueExpression):
            found.add(node.field)
        for arg in getattr(node, "args", ()):
            walk(arg)

    for cond in rule.detection.parsed_condition:
        walk(cond.parse())
    return found
