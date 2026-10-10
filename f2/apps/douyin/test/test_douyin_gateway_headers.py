# path: f2/apps/douyin/test/test_douyin_gateway_headers.py

from f2.apps.douyin.crawler import DouyinCrawler
from f2.apps.douyin.utils import GatewayHeaderManager


def test_gen_gateway_headers_always_sends_argus_placeholder():
    headers = GatewayHeaderManager.gen_gateway_headers(None)
    assert headers == {"x-tt-argus": GatewayHeaderManager.ARGUS_PLACEHOLDER}


def test_gen_gateway_headers_extracts_uifid():
    headers = GatewayHeaderManager.gen_gateway_headers("ttwid=abc; UIFID=from-cookie")
    assert headers["x-tt-argus"] == "1"
    assert headers["uifid"] == "from-cookie"


def test_gen_gateway_headers_falls_back_to_uifid_temp():
    headers = GatewayHeaderManager.gen_gateway_headers("UIFID_TEMP=temp-id")
    assert headers["uifid"] == "temp-id"


def test_gen_gateway_headers_prefers_uifid_over_temp():
    headers = GatewayHeaderManager.gen_gateway_headers(
        "UIFID_TEMP=temp-id; UIFID=real-id"
    )
    assert headers["uifid"] == "real-id"


def test_merge_headers_keeps_explicit_overrides_case_insensitive():
    merged = GatewayHeaderManager.merge_headers(
        {"X-Tt-Argus": "browser-value", "User-Agent": "ua"},
        "UIFID=from-cookie",
    )
    assert merged["X-Tt-Argus"] == "browser-value"
    assert "x-tt-argus" not in merged
    assert merged["uifid"] == "from-cookie"
    assert merged["User-Agent"] == "ua"


def test_douyin_crawler_attaches_gateway_headers():
    crawler = DouyinCrawler(
        {
            "cookie": "UIFID=from-cookie; ttwid=abc",
            "headers": {"User-Agent": "ua", "Referer": "https://www.douyin.com/"},
        }
    )
    assert crawler.headers["x-tt-argus"] == "1"
    assert crawler.headers["uifid"] == "from-cookie"
    assert crawler.headers["Cookie"] == "UIFID=from-cookie; ttwid=abc"
    assert crawler.headers["User-Agent"] == "ua"
