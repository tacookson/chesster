"""chesster: fetch new rapid games, flag big swings with Stockfish, write one markdown file per game."""

import argparse
import io
import re
import shutil
import sys
import time
from pathlib import Path

import chess
import chess.engine
import chess.pgn

from chesster import analyse, config, fetch, render


def _existing(games_dir: Path) -> dict[str, bool]:
    """Game id → whether its file has been analysed. Files that aren't game files are ignored."""
    found = {}
    for p in games_dir.glob("*/*.md"):
        match = re.search(r"-(\d+)$", p.stem)
        if match:
            found[match.group(1)] = render.NOT_ANALYSED not in p.read_text()
    return found


def _open_engine(path: str) -> chess.engine.SimpleEngine:
    resolved = shutil.which(path)
    if not resolved:
        sys.exit(f"Stockfish not found at '{path}'. Install it (brew install stockfish) "
                 "or set [engine] path in chesster.toml.")
    return chess.engine.SimpleEngine.popen_uci(resolved)


ALL_TIME_CLASSES = ("rapid", "blitz", "bullet", "daily")


def _progress(prefix: str) -> analyse.Progress:
    def show(stage: str, done: int, total: int) -> None:
        print(f"\r\x1b[2K{prefix} Stockfish: {stage} {done}/{total}", end="", flush=True)
    return show


def process(game: dict, cfg: config.Config, engine: chess.engine.SimpleEngine | None,
            progress: analyse.Progress = analyse._quiet, match: str | None = None) -> Path:
    pgn_game = chess.pgn.read_game(io.StringIO(game["pgn"]))
    info = render.game_info(game, pgn_game, cfg.username, cfg.timezone, match)
    moments = None
    if engine is not None:
        me = chess.WHITE if info.colour == "white" else chess.BLACK
        moments = analyse.analyse(pgn_game, me, engine, cfg.depth, cfg.safe_depth,
                                  cfg.mistake, cfg.blunder, cfg.decided, lost=info.result == "loss",
                                  progress=progress)
    path = render.path_for(info, cfg.games_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".md.tmp")
    tmp.write_text(render.render(info, game["pgn"], moments))
    tmp.replace(path)
    return path


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="chesster", description=__doc__)
    parser.add_argument("--game", metavar="URL", help="re-process one game (overwrites its file)")
    parser.add_argument("--no-engine", action="store_true",
                        help="archive only; skip Stockfish (a later run without it analyses these games)")
    parser.add_argument("--all-time-controls", action="store_true",
                        help="include blitz, bullet and daily games, not just rapid")
    parser.add_argument("--config", type=Path, default=Path("chesster.toml"), help="path to chesster.toml")
    args = parser.parse_args(argv)

    if not args.config.exists():
        sys.exit(f"Config not found: {args.config}. Run from the repo root or pass --config.")
    try:
        cfg = config.load(args.config)
    except config.ConfigError as e:
        sys.exit(f"Problem in {args.config}: {e}")
    time_classes = ALL_TIME_CLASSES if args.all_time_controls else cfg.time_classes

    try:
        if args.game:
            game, nearby = fetch.find_game(cfg.username, args.game)
            if fetch.is_coach(game):
                sys.exit(f"{args.game} is a game against a Chess.com coach bot; chesster doesn't import those.")
            todo, matches = [game], render.match_ids(nearby, cfg.timezone)
        else:
            print(f"Fetching {cfg.username}'s archives from Chess.com…")
            existing = _existing(cfg.games_dir)
            # With the engine on, games archived earlier with --no-engine are still to do.
            done = set(existing) if args.no_engine else {i for i, analysed in existing.items() if analysed}
            fetched = list(fetch.games(cfg.username, time_classes))
            matches = render.match_ids(fetched, cfg.timezone)
            todo = [g for g in fetched if fetch.game_id(g) not in done]
    except (fetch.FetchError, LookupError) as e:
        sys.exit(str(e))
    if not todo:
        print("No new games.")
        return

    engine = None if args.no_engine else _open_engine(cfg.engine_path)
    try:
        for n, game in enumerate(todo, 1):
            start = time.monotonic()
            prefix = f"[{n}/{len(todo)}]"
            path = process(game, cfg, engine, _progress(prefix), matches.get(fetch.game_id(game)))
            print(f"\r\x1b[2K{prefix} {path} ({time.monotonic() - start:.0f}s)")
    finally:
        if engine is not None:
            engine.quit()
    print(f"Wrote {len(todo)} game file(s).")


if __name__ == "__main__":
    main()
