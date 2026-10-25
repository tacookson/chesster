"""chesster: fetch new rapid games, flag big swings with Stockfish, write one markdown file per game."""

import argparse
import io
import shutil
import sys
import time
from pathlib import Path

import chess
import chess.engine
import chess.pgn

from chesster import analyse, config, fetch, render


def _existing_ids(games_dir: Path) -> set[str]:
    return {p.stem.rsplit("-", 1)[1] for p in games_dir.glob("*/*.md")}


def _open_engine(path: str) -> chess.engine.SimpleEngine:
    resolved = shutil.which(path) or (path if Path(path).exists() else None)
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
                                  cfg.mistake, cfg.blunder, lost=info.result == "loss")
    path = render.path_for(info, cfg.games_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render.render(info, game["pgn"], moments))
    return path


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="chesster", description=__doc__)
    parser.add_argument("--game", metavar="URL", help="re-process one game (overwrites its file)")
    parser.add_argument("--no-engine", action="store_true", help="archive only; skip Stockfish")
    parser.add_argument("--config", type=Path, default=Path("chesster.toml"), help="path to chesster.toml")
    args = parser.parse_args(argv)

    if not args.config.exists():
        sys.exit(f"Config not found: {args.config}. Run from the repo root or pass --config.")
    cfg = config.load(args.config)

    if args.game:
        todo = [fetch.find_game(cfg.username, args.game)]
    else:
        print(f"Fetching {cfg.username}'s archives from Chess.com…")
        done = _existing_ids(cfg.games_dir)
        todo = [g for g in fetch.games(cfg.username, cfg.time_classes) if fetch.game_id(g) not in done]
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
