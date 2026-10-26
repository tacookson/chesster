"""One markdown file per game, in review order: header for hot notes, PGN for my own review, then
the engine check, folded."""

import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import chess
import chess.pgn

from chesster import analyse, fetch
from chesster.analyse import Flag

DRAWS = {"agreed", "repetition", "stalemate", "insufficient", "50move", "timevsinsufficient"}
ENDINGS = {
    "win": {"checkmated": "you won by checkmate", "resigned": "your opponent resigned",
            "timeout": "you won on time", "abandoned": "your opponent abandoned the game"},
    "loss": {"checkmated": "you were checkmated", "resigned": "you resigned",
             "timeout": "you lost on time", "abandoned": "you abandoned the game"},
    "draw": {"agreed": "draw by agreement", "repetition": "draw by repetition",
             "stalemate": "draw by stalemate", "insufficient": "draw, insufficient material",
             "50move": "draw by the 50-move rule",
             "timevsinsufficient": "draw, time ran out with no mating material"},
}
NOT_ANALYSED = "Not analysed yet."
MATERIAL = {1: "a pawn", 2: "two pawns' worth of material", 3: "a piece", 4: "a piece and a pawn",
            5: "a rook", 6: "a rook and a pawn", 8: "a rook and a piece", 9: "a queen"}


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
    match: str | None = None  # e.g. "261023-1"; rapid games only


def _opening(pgn_game) -> str:
    url = pgn_game.headers.get("ECOUrl", "")
    slug = url.rsplit("/openings/", 1)[-1].split("...")[0]
    # Slugs can end in a move number cut off from the "..." moves, e.g. "Exchange-Variation-3".
    name = re.sub(r"-\d+$", "", slug).replace("-", " ").strip()
    if not name:
        eco = pgn_game.headers.get("ECO", "")
        name = eco if eco not in ("", "?") else "Unknown opening"
    return re.sub(r"\b(Queen|King|Bishop|Alekhine|Petrov|Bird|Philidor)s\b", r"\1's", name)


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


def _local_end(game: dict, timezone: str) -> datetime:
    return datetime.fromtimestamp(game["end_time"], ZoneInfo(timezone))


def match_ids(games: list[dict], timezone: str) -> dict[str, str]:
    """Match ID per rapid game: local date as YYMMDD, then its number that day by end time."""
    rapid = sorted((g for g in games if g.get("time_class") == "rapid" and g.get("rules") == "chess"
                    and not fetch.is_coach(g)),
                   key=lambda g: g["end_time"])
    ids, per_day = {}, {}
    for game in rapid:
        day = _local_end(game, timezone).strftime("%y%m%d")
        per_day[day] = per_day.get(day, 0) + 1
        ids[game["url"].rstrip("/").rsplit("/", 1)[1]] = f"{day}-{per_day[day]}"
    return ids


def game_info(game: dict, pgn_game, username: str, timezone: str, match: str | None = None) -> GameInfo:
    white = game["white"]["username"].lower() == username.lower()
    mine, theirs = (game["white"], game["black"]) if white else (game["black"], game["white"])
    if mine["result"] == "win":
        result, reason = "win", theirs["result"]
    elif mine["result"] in DRAWS:
        result, reason = "draw", mine["result"]
    else:
        result, reason = "loss", mine["result"]
    clocks = _last_clocks(pgn_game)
    me = chess.WHITE if white else chess.BLACK
    end = _local_end(game, timezone)
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
        match=match,
    )


def path_for(info: GameInfo, games_dir: Path) -> Path:
    opponent = re.sub(r"[^A-Za-z0-9_-]", "", info.opponent)
    return games_dir / info.date[:7] / f"{info.date}-vs-{opponent}-{info.id}.md"


def eval_words(cp: int) -> str:
    """An evaluation in words, from my point of view (cp in centipawns, mate as ±100000)."""
    if abs(cp) >= 10_000:
        return "forced mate for you" if cp > 0 else "forced mate against you"
    size = abs(cp)
    if size <= 50:
        return "about equal"
    side = "better" if cp > 0 else "worse"
    if size <= 150:
        return f"slightly {side}"
    if size <= 400:
        return f"clearly {side}"
    return "winning" if cp > 0 else "losing"


def material_words(points: int) -> str:
    return MATERIAL.get(points, f"{points} points of material")


def _headline(flag: Flag) -> str:
    severity = flag.severity.capitalize()
    if flag.kind == analyse.LOST_MATERIAL:
        what = f"you lost {material_words(flag.material)}"
    elif flag.kind == analyse.MISSED_MATERIAL:
        what = f"you missed winning {material_words(flag.material)}"
    elif flag.kind == analyse.MISSED_MATE:
        what = f"you missed a mate in {flag.mate_in}"
    elif flag.kind == analyse.ALLOWED_MATE:
        what = f"you allowed a mate in {flag.mate_in}"
    else:
        what = "your position got much worse, though no material changes hands right away"
    headline = f"**{severity}: {what}.**"
    if flag.decided == "losing":
        headline += " You were already losing, so this didn't change the likely result."
    elif flag.decided == "winning":
        headline += " You were still winning after it, so this didn't change the likely result."
    return headline


def _difficulty(safe: tuple[int, int]) -> str:
    """The safe-move count, with no verdict: why the move happened is mine to judge."""
    held, legal = safe
    return f"{held} of your {legal} legal {'move' if legal == 1 else 'moves'} kept your position."


def _duration(seconds: float) -> str:
    seconds = round(seconds)
    return f"{seconds}s" if seconds < 60 else f"{seconds // 60}m {seconds % 60:02d}s"


def _time(clocks: list[tuple[float, float]]) -> str:
    """Time spent and clock left, e.g. "Time: 4s on this move, 3:12 left." (no engine information)."""
    spent = [_duration(s) for s, _ in clocks]
    left = _clock(clocks[-1][1])
    if len(spent) == 1:
        return f"Time: {spent[0]} on this move, {left} left."
    return f"Time: {', '.join(spent[:-1])} and {spent[-1]} on these moves, {left} left after the last."


def _moment(flag: Flag, colour: str) -> str:
    labels = [flag.move_label, *flag.merged]
    numbers = [label.split(".")[0] for label in labels]
    sans = [label.split(" ", 1)[1] for label in labels]
    if len(labels) == 1:
        heading = f"### Move {numbers[0]} as {colour}: you played {sans[0]}"
    else:
        heading = f"### Moves {numbers[0]}–{numbers[-1]} as {colour}: you played {', '.join(sans)}"
    lines = [heading, "", _headline(flag)]
    if flag.merged:
        lines[-1] += f" The same idea was missed on {len(labels)} moves in a row."
    if flag.first_material_loss:
        lines[-1] += " This was the first material you lost in the game."
    if flag.clocks:
        lines += ["", _time(flag.clocks)]
    lines += [
        "",
        "<details>",
        "<summary>Show the engine's answer</summary>",
        "",
        f"- **Better:** {flag.best_line.split(' ', 1)[0]} {flag.best}"
        f"{', taking the ' + flag.best_takes if flag.best_takes else ''}.  ",
        f"  Line: {flag.best_line}",
    ]
    if flag.punish_line:
        lines += [
            f"- **What your move allowed:** {flag.punished_by}"
            f"{', taking your ' + flag.punish_takes if flag.punish_takes else ''}.  ",
            f"  Line: {flag.punish_line}",
        ]
    lines.append(f"- **Effect:** {eval_words(flag.before_cp)} ({flag.before}) → "
                 f"{eval_words(flag.after_cp)} ({flag.after}), from your side.")
    if flag.safe:
        lines.append(f"- **Difficulty:** {_difficulty(flag.safe)}")
    lines += ["", "</details>", ""]
    return "\n".join(lines)


def _ending(info: GameInfo) -> str:
    return ENDINGS[info.result].get(info.reason, f"{info.result} ({info.reason})")


def _time_control(tc: str) -> str:
    base, _, increment = tc.partition("+")
    return f"{int(base) // 60}+{increment or 0}" if base.isdigit() else tc


def render(info: GameInfo, pgn: str, moments: list[Flag] | None) -> str:
    date = datetime.strptime(info.date, "%Y-%m-%d").strftime("%-d %b %Y")
    rated = "rated" if info.rated else "unrated"
    analysed = moments is not None
    match = [f"match: {info.match}"] if info.match else []
    title = f"{info.match} · {date}" if info.match else date
    out = [
        "---",
        *match,
        f"url: {info.url}",
        f"date: {info.date}",
        f"colour: {info.colour}",
        f"result: {info.result} ({info.reason})",
        f"opponent: {info.opponent} ({info.opponent_rating})",
        f"my_rating: {info.my_rating}",
        f"opening: {info.opening}",
        f"time_control: {info.time_control}",
        f"rated: {str(info.rated).lower()}",
        f"analysed: {str(analysed).lower()}",
        "---",
        "",
        f"# {title} · {info.result.capitalize()} as {info.colour.capitalize()} vs "
        f"{info.opponent} ({info.opponent_rating})",
        "",
        "## 1. Hot notes",
        "",
        f"You: {info.my_rating} · {_time_control(info.time_control)} {rated} · {info.opening}  ",
        f"Ended: {_ending(info)} · Clock left: you {info.clock_me}, opponent {info.clock_opp}",
        "",
        "## 2. Own review, engine off",
        "",
        "Paste into maiachess.com and pick your own moments before opening the engine check.",
        "",
        "```pgn", pgn.strip(), "```",
        "",
        "## 3. Engine check",
        "",
    ]
    if not analysed:
        out += [f"{NOT_ANALYSED} Run `uv run chesster` after your own review.", ""]
        return "\n".join(out)
    out += ["<details>", "<summary>Open after your own review</summary>", ""]
    if not moments:
        out += ["No big swings in this game.", ""]
    else:
        count = "1 move" if len(moments) == 1 else f"{len(moments)} moves"
        out += [f"Stockfish flagged {count}. Go deep on the ones you choose.", ""]
        out += [_moment(m, info.colour.capitalize()) for m in moments]
    out += ["</details>", ""]
    return "\n".join(out)
