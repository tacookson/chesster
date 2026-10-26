import io
import urllib.error

import pytest

from chesster import fetch


@pytest.mark.parametrize("url", [
    "https://www.chess.com/game/live/185828873624",
    "https://www.chess.com/game/live/185828873624/",
    "https://www.chess.com/game/live/185828873624?move=10",
    "https://www.chess.com/analysis/game/live/185828873624/analysis",
    "https://www.chess.com/game/185828873624",
    "185828873624",
])
def test_id_from_url(url):
    assert fetch.id_from_url(url) == "185828873624"


def test_id_from_url_rejects_other_links():
    with pytest.raises(LookupError, match="doesn't look like a Chess.com game URL"):
        fetch.id_from_url("https://www.chess.com/member/me4tbegz0r")


def test_unknown_username_says_so(monkeypatch):
    def not_found(request, timeout):
        raise urllib.error.HTTPError(request.full_url, 404, "Not Found", {}, io.BytesIO())
    monkeypatch.setattr(fetch.urllib.request, "urlopen", not_found)
    with pytest.raises(fetch.FetchError, match="no player 'Nobody'"):
        fetch.archive_urls("Nobody")


def test_network_down_says_so(monkeypatch):
    def offline(request, timeout):
        raise urllib.error.URLError("Name or service not known")
    monkeypatch.setattr(fetch.urllib.request, "urlopen", offline)
    with pytest.raises(fetch.FetchError, match="Couldn't reach Chess.com"):
        fetch.archive_urls("me")


def test_games_filters_time_class_and_variants(monkeypatch):
    archive = {"games": [
        {"url": "u/1", "time_class": "rapid", "rules": "chess"},
        {"url": "u/2", "time_class": "rapid", "rules": "chess960"},
        {"url": "u/3", "time_class": "daily", "rules": "chess"},
    ]}
    monkeypatch.setattr(fetch, "archive_urls", lambda username: ["a"])
    monkeypatch.setattr(fetch, "_get", lambda url: archive)
    assert [fetch.game_id(g) for g in fetch.games("me", ("rapid",))] == ["1"]
