"""Chess.com published-data API: monthly game archives, no auth."""

import json
import re
import urllib.error
import urllib.request

API = "https://api.chess.com/pub/player/{user}/games/archives"
USER_AGENT = "chesster (personal game review tool; github.com/tacookson/chesster)"


class FetchError(RuntimeError):
    """Chess.com couldn't be reached or didn't have what we asked for."""


def _get(url: str) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)
    except urllib.error.HTTPError as e:
        raise FetchError(f"Chess.com returned HTTP {e.code} for {url}") from e
    except urllib.error.URLError as e:
        raise FetchError(f"Couldn't reach Chess.com ({e.reason}). Check your connection.") from e


def archive_urls(username: str) -> list[str]:
    try:
        return _get(API.format(user=username.lower()))["archives"]
    except FetchError as e:
        if "HTTP 404" in str(e):
            raise FetchError(f"Chess.com has no player '{username}'. Check username in chesster.toml.") from e
        raise


def is_coach(game: dict) -> bool:
    """A game against one of Chess.com's coach bots (e.g. Coach-Magnus)."""
    return any(game.get(side, {}).get("username", "").lower().startswith("coach-") for side in ("white", "black"))


def games(username: str, time_classes: tuple[str, ...]):
    """Yield every game in the player's archives with a matching time class, oldest first.

    Coach-bot games are left out.
    """
    for url in archive_urls(username):
        for game in _get(url).get("games", []):
            if game.get("time_class") in time_classes and game.get("rules") == "chess" and not is_coach(game):
                yield game


def game_id(game: dict) -> str:
    return game["url"].rstrip("/").rsplit("/", 1)[1]


def id_from_url(url: str) -> str:
    """The game id in a Chess.com game URL, including copied analysis links and ?move= suffixes."""
    match = re.search(r"/game/(?:live/|daily/)?(\d+)", url) or re.fullmatch(r"\s*(\d+)\s*", url)
    if not match:
        raise LookupError(f"'{url}' doesn't look like a Chess.com game URL, e.g. "
                          "https://www.chess.com/game/live/123456789")
    return match.group(1)


def find_game(username: str, url: str) -> tuple[dict, list[dict]]:
    """Find one game by its URL, with every game in its month and the months either side.

    There is no single-game endpoint, so search the archives. The neighbouring months are
    included because a local day can span two monthly archives (they're split by UTC).
    """
    wanted = id_from_url(url)
    archives = archive_urls(username)
    for i in reversed(range(len(archives))):
        month = _get(archives[i]).get("games", [])
        for game in month:
            if game_id(game) == wanted:
                nearby = [g for j in (i - 1, i + 1) if 0 <= j < len(archives)
                          for g in _get(archives[j]).get("games", [])]
                return game, month + nearby
    raise LookupError(f"Game {wanted} not found in {username}'s archives")
