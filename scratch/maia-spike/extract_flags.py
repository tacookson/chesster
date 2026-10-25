"""Extract pre-merge Stockfish flags from chesster game files as JSON (FEN before, my move, best move, ratings).

Usage: uv run python extract_flags.py GAMES_DIR OUT_JSON [STOCKFISH]
"""
import io, json, re, sys
from pathlib import Path
import chess, chess.engine, chess.pgn
from chesster import analyse

games_dir, out = Path(sys.argv[1]), Path(sys.argv[2])
engine = chess.engine.SimpleEngine.popen_uci(sys.argv[3] if len(sys.argv) > 3 else "stockfish")
rows = []
for md in sorted(games_dir.glob("*/*.md")):
    text = md.read_text()
    pgn = re.search(r"```pgn\n(.*?)```", text, re.S).group(1)
    g = chess.pgn.read_game(io.StringIO(pgn))
    me = chess.WHITE if "colour: white" in text else chess.BLACK
    my_elo = int(g.headers["WhiteElo" if me else "BlackElo"]); opp_elo = int(g.headers["BlackElo" if me else "WhiteElo"])
    evals = analyse.evaluate_game(g, me, engine, 16)
    flags = analyse.find_flags(g, me, evals, 15, 30)
    moments = {m.ply for m in analyse.merge(flags)}
    nodes = list(g.mainline())
    for f in flags:
        board = nodes[f.ply].parent.board()
        rows.append(dict(game=md.stem, ply=f.ply, label=f.move_label, severity=f.severity, kind=f.kind,
                         drop=round(f.drop, 1), fen=board.fen(), played=nodes[f.ply].move.uci(),
                         best=f.best_uci, best_san=f.best, my_elo=my_elo, opp_elo=opp_elo,
                         moment=f.ply in moments, before=f.before, after=f.after))
engine.quit()
out.write_text(json.dumps(rows, indent=1))
print(len(rows), "flags;", sum(r["moment"] for r in rows), "after merging")
