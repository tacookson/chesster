"""Spike: sweep maiachess.com's own Maia-3 ONNX (onnxruntime only, no torch) across 600–2600 for every flag.

Usage: python site_sweep.py FLAGS_JSON ONNX OUT_JSON [--ort-default]

--ort-default keeps onnxruntime's default graph optimisation (segfaulted on Linux, ORT 1.31).
"""
import json, sys, time
t_import = time.monotonic()
import onnxruntime as ort, numpy as np, chess
PIECE = {chess.PAWN: 1, chess.KNIGHT: 2, chess.BISHOP: 3, chess.ROOK: 4, chess.QUEEN: 5, chess.KING: 6}
def mirror(u): return u[0] + str(9 - int(u[1])) + u[2] + str(9 - int(u[3])) + u[4:]
MOVES = [chess.square_name(a) + chess.square_name(b) for a in range(64) for b in range(64)] + [f"{f}7{t}8{p}" for f in "abcdefgh" for t in "abcdefgh" for p in "qrbn"]
IDX = {m: i for i, m in enumerate(MOVES)}
RATINGS = list(range(600, 2601, 100))

so = ort.SessionOptions()
if "--ort-default" not in sys.argv:
    so.graph_optimization_level = ort.GraphOptimizationLevel.ORT_DISABLE_ALL  # default level segfaulted (ORT 1.31, Linux)
t0 = time.monotonic(); sess = ort.InferenceSession(sys.argv[2], so); load_s = time.monotonic() - t0

def tokens(b):
    bb = b.mirror() if b.turn == chess.BLACK else b
    tok = np.zeros((64, 12), np.float32)
    for sq in chess.SQUARES:
        p = bb.piece_at(sq)
        if p: tok[sq][PIECE[p.piece_type] + (6 if p.color == chess.BLACK else 0) - 1] = 1
    return tok

def sweep(fen, self_elos, oppo_elos):
    b = chess.Board(fen); n = len(self_elos)
    lg, _ = sess.run(None, {"tokens": np.repeat(tokens(b)[None], n, 0),
                            "elo_self": np.array(self_elos, np.float32), "elo_oppo": np.array(oppo_elos, np.float32)})
    legal = [m.uci() for m in b.legal_moves]
    keys = [IDX[u if b.turn == chess.WHITE else mirror(u)] for u in legal]
    l = lg[:, keys].astype(np.float64); p = np.exp(l - l.max(1, keepdims=True)); p /= p.sum(1, keepdims=True)
    return [dict(zip(legal, row.tolist())) for row in p]

flags = json.load(open(sys.argv[1])); fen0 = flags[0]["fen"]
sweep(fen0, RATINGS, RATINGS)
t = time.monotonic(); sweep(fen0, RATINGS, RATINGS); one_batched = time.monotonic() - t
t = time.monotonic(); [sweep(fen0, [r], [r]) for r in RATINGS]; one_seq = time.monotonic() - t
t = time.monotonic()
for f in flags:
    f["site"] = sweep(f["fen"], RATINGS, RATINGS)
    f["fixed_opp"] = sweep(f["fen"], RATINGS, [f["opp_elo"]] * len(RATINGS))
all_s = time.monotonic() - t
res = dict(model="site-onnx", ratings=RATINGS, load_s=load_s, one_batched_s=one_batched, one_sequential_s=one_seq,
           all_flags_two_sweeps_s=all_s, n_flags=len(flags), flags=flags)
json.dump(res, open(sys.argv[3], "w"))
print({k: v for k, v in res.items() if k != "flags"})
