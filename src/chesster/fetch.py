"""Chess.com published-data API: monthly game archives, no auth."""

import json
import urllib.request

API = "https://api.chess.com/pub/player/{user}/games/archives"
USER_AGENT = "chesster (personal game review tool; github.com/tacookson/chesster)"


def _get(url: str) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def archive_urls(username: str) -> list[str]:
    return _get(API.format(user=username.lower()))["archives"]


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


def find_game(username: str, url: str) -> tuple[dict, list[dict]]:
    """Find one game by its URL, with every game in its month and the months either side.

    There is no single-game endpoint, so search the archives. The neighbouring months are
    included because a local day can span two monthly archives (they're split by UTC).
    """
    wanted = url.rstrip("/").rsplit("/", 1)[1]
    archives = archive_urls(username)
    for i in reversed(range(len(archives))):
        month = _get(archives[i]).get("games", [])
        for game in month:
            if game_id(game) == wanted:
                nearby = [g for j in (i - 1, i + 1) if 0 <= j < len(archives)
                          for g in _get(archives[j]).get("games", [])]
                return game, month + nearby
    raise LookupError(f"Game {url} not found in {username}'s archives")
