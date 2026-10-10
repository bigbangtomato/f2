# path: tests/test_cookie.py

import pytest

from f2.utils.http.cookie import parse_cookie_str


def test_parse_cookie_str_basic():
    assert parse_cookie_str("a=1; b=2") == {"a": "1", "b": "2"}


def test_parse_cookie_str_keeps_equals_in_value():
    assert parse_cookie_str("token=a=b=c") == {"token": "a=b=c"}


def test_parse_cookie_str_ignores_empty_and_nameless_parts():
    assert parse_cookie_str("a=1;; =orphan; ; b=2") == {"a": "1", "b": "2"}


def test_parse_cookie_str_last_duplicate_wins():
    assert parse_cookie_str("UIFID=old; UIFID=new") == {"UIFID": "new"}


def test_parse_cookie_str_rejects_non_string():
    with pytest.raises(TypeError, match="cookie_str 参数应为字符串"):
        parse_cookie_str(None)  # type: ignore[arg-type]
