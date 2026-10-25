"""One markdown file per game: header, flagged moves (answers folded), PGN."""

import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import chess
import chess.pgn

from chesster.analyse import Flag

DRAWS = {"agreed", "repetition", "stalemate", "insufficient", "50move", "timevsinsufficient"}
WIN_REASONS = {"checkmated": "by checkmate", "resigned": "by resignation", "timeout": "on time",
               "abandoned": "by abandonment"}


@dataclass
class GameInfo:
    id: str
    url: str
    date: str
    colour: str
    result: str           # "win", "loss" or "draw"
    reason: str           # Chess.com result code for the loser/drawer, e.g. "checkmated"
    me: str
    my_rating: int
    opponent: str
    opponent_rating: int
    opening: str
    time_control: str
    rated: bool
    clock_me: str
    clock_opp: str


def _opening(pgn_game) -> str:
    url = pgn_game.headers.get("ECOUrl", "")
    slug = url.rsplit("/openings/", 1)[-1].split("...")[0]
    return slug.replace("-", " ").strip() or pgn_game.headers.get("ECO", "?")


def _clock(seconds: float | None) -> str:
    if seconds is None:
        return "?"
    seconds = int(seconds)
    return f"{seconds // 60}:{seconds % 60:02d}"


def _last_clocks(pgn_game) -> dict[chess.Color, float | None]:
    clocks: dict[chess.Color, float | None] = {chess.WHITE: None, chess.BLACK: None}
    board = pgn_game.board()
    for node in pgn_game.mainline():
        mover = board.turn
        if node.clock() is not None:
            clocks[mover] = node.clock()
        board.push(node.move)
    return clocks


def game_info(game: dict, pgn_game, username: str, timezone: str) -> GameInfo:
    white = game["white"]["username"].lower() == username.lower()
    mine, theirs = (game["white"], game["black"]) if white else (game["black"], game["white"])
    if mine["result"] == "win":
        result, reason = "win", WIN_REASONS.get(theirs["result"], theirs["result"])
    elif mine["result"] in DRAWS:
        result, reason = "draw", mine["result"]
    else:
        result, reason = "loss", mine["result"]
    clocks = _last_clocks(pgn_game)
    me = chess.WHITE if white else chess.BLACK
    end = datetime.fromtimestamp(game["end_time"], ZoneInfo(timezone))
    return GameInfo(
        id=game["url"].rstrip("/").rsplit("/", 1)[1],
        url=game["url"],
        date=end.strftime("%Y-%m-%d"),
        colour="white" if white else "black",
        result=result,
        reason=reason,
        me=mine["username"],
        my_rating=mine["rating"],
        opponent=theirs["username"],
        opponent_rating=theirs["rating"],
        opening=_opening(pgn_game),
        time_control=game["time_control"],
        rated=game.get("rated", False),
        clock_me=_clock(clocks[me]),
        clock_opp=_clock(clocks[not me]),
    )


def path_for(info: GameInfo, games_dir: Path) -> Path:
    opponent = re.sub(r"[^A-Za-z0-9_-]", "", info.opponent)
    return games_dir / info.date[:7] / f"{info.date}-vs-{opponent}-{info.id}.md"


def _moment(n: int, flag: Flag) -> str:
    moves = " → ".join([flag.move_label, *flag.merged]) if flag.merged else flag.move_label
    kind = f"{flag.kind} in {flag.mate_in}" if flag.mate_in else flag.kind
    tags = [flag.severity, kind]
    if flag.merged:
        tags.append(f"{len(flag.merged) + 1} moves, same idea")
    if flag.first_material_loss:
        tags.append("first material loss")
    lines = [
        f"### {n}. {moves}",
        "",
        " · ".join(tags),
        "",
        "<details>",
        "<summary>Engine answer</summary>",
        "",
        f"Best: {flag.best} · Punished by: {flag.punished_by or '—'} · {flag.before} → {flag.after}",
    ]
    if flag.safe:
        lines += ["", f"{flag.safe[0]} of {flag.safe[1]} moves held"]
    lines += ["", "</details>", ""]
    return "\n".join(lines)


def render(info: GameInfo, pgn: str, moments: list[Flag] | None) -> str:
    colour = info.colour.capitalize()
    result = info.result.capitalize()
    reason = f" ({info.reason})" if info.reason else ""
    out = [
        "---",
        f"url: {info.url}",
        f"date: {info.date}",
        f"colour: {info.colour}",
        f"result: {info.result}{reason}",
        f"opponent: {info.opponent} ({info.opponent_rating})",
        f"my_rating: {info.my_rating}",
        f"opening: {info.opening}",
        f"time_control: {info.time_control}",
        f"rated: {str(info.rated).lower()}",
        "---",
        "",
        f"# {info.date} · {colour} · {result} · vs {info.opponent} ({info.opponent_rating})",
        "",
        f"Opening: {info.opening}  ",
        f"Clock left (me / opp): {info.clock_me} / {info.clock_opp}",
        "",
        "## Flagged moves",
        "",
    ]
    if moments is None:
        out += ["Not analysed yet.", ""]
    elif not moments:
        out += ["No flagged moves.", ""]
    else:
        out += [_moment(n, m) for n, m in enumerate(moments, 1)]
    out += ["## PGN", "", "```pgn", pgn.strip(), "```", ""]
    return "\n".join(out)
