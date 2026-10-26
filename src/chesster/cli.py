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


def process(game: dict, cfg: config.Config, engine: chess.engine.SimpleEngine | None) -> Path:
    pgn_game = chess.pgn.read_game(io.StringIO(game["pgn"]))
    info = render.game_info(game, pgn_game, cfg.username, cfg.timezone)
    moments = None
    if engine is not None:
        me = chess.WHITE if info.colour == "white" else chess.BLACK
        moments = analyse.analyse(pgn_game, me, engine, cfg.depth, cfg.safe_depth,
                                  cfg.mistake, cfg.blunder, cfg.decided, lost=info.result == "loss")
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
    parser.add_argument("--config", type=Path, default=Path("chesster.toml"), help="path to chesster.toml")
    args = parser.parse_args(argv)

    if not args.config.exists():
        sys.exit(f"Config not found: {args.config}. Run from the repo root or pass --config.")
    try:
        cfg = config.load(args.config)
    except config.ConfigError as e:
        sys.exit(f"Problem in {args.config}: {e}")

    try:
        if args.game:
            todo = [fetch.find_game(cfg.username, args.game)]
        else:
            print(f"Fetching {cfg.username}'s archives from Chess.com…")
            existing = _existing(cfg.games_dir)
            # With the engine on, games archived earlier with --no-engine are still to do.
            done = set(existing) if args.no_engine else {i for i, analysed in existing.items() if analysed}
            todo = [g for g in fetch.games(cfg.username, cfg.time_classes) if fetch.game_id(g) not in done]
    except (fetch.FetchError, LookupError) as e:
        sys.exit(str(e))
    if not todo:
        print("No new games.")
        return

    engine = None if args.no_engine else _open_engine(cfg.engine_path)
    try:
        for n, game in enumerate(todo, 1):
            start = time.monotonic()
            path = process(game, cfg, engine)
            print(f"[{n}/{len(todo)}] {path} ({time.monotonic() - start:.0f}s)")
    finally:
        if engine is not None:
            engine.quit()
    print(f"Wrote {len(todo)} game file(s).")


if __name__ == "__main__":
    main()
