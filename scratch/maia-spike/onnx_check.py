"""Compare a Maia-3 PyTorch sweep (maia3_sweep.py output) with maiachess.com's ONNX on every flagged position.

Usage: python onnx_check.py OUT_JSON ONNX
"""
import json, sys
import onnxruntime as ort
import numpy as np, chess

PIECE = {chess.PAWN: 1, chess.KNIGHT: 2, chess.BISHOP: 3, chess.ROOK: 4, chess.QUEEN: 5, chess.KING: 6}
def mirror(u): return u[0] + str(9 - int(u[1])) + u[2] + str(9 - int(u[3])) + u[4:]
moves = [chess.square_name(a) + chess.square_name(b) for a in range(64) for b in range(64)]
moves += [f"{f}7{t}8{p}" for f in "abcdefgh" for t in "abcdefgh" for p in "qrbn"]
idx = {m: i for i, m in enumerate(moves)}

res = json.load(open(sys.argv[1])); R = res["ratings"]
so = ort.SessionOptions(); so.graph_optimization_level = ort.GraphOptimizationLevel.ORT_DISABLE_ALL; so.intra_op_num_threads = 1
sess = ort.InferenceSession(sys.argv[2], so, providers=["CPUExecutionProvider"])
diffs, top_agree, n = [], 0, 0
for f in res["flags"]:
    b = chess.Board(f["fen"]); bb = b.mirror() if b.turn == chess.BLACK else b
    tok = np.zeros((64, 12), np.float32)
    for sq in chess.SQUARES:
        p = bb.piece_at(sq)
        if p: tok[sq][PIECE[p.piece_type] + (6 if p.color == chess.BLACK else 0) - 1] = 1
    e = np.array(R, np.float32)
    logits, _ = sess.run(None, {"tokens": np.repeat(tok[None], len(R), 0), "elo_self": e, "elo_oppo": e})
    legal = [m.uci() for m in b.legal_moves]
    keys = [idx[u if b.turn == chess.WHITE else mirror(u)] for u in legal]
    lg = logits[:, keys].astype(np.float64); p = np.exp(lg - lg.max(1, keepdims=True)); p /= p.sum(1, keepdims=True)
    for k in range(len(R)):
        torch_p = np.array([f["site"][k][u] for u in legal])
        diffs.extend(np.abs(p[k] - torch_p)); n += 1
        top_agree += int(np.argmax(p[k]) == np.argmax(torch_p))
print(f"positions×ratings={n} max|Δp|={max(diffs):.4f} mean|Δp|={np.mean(diffs):.5f} top-move agreement={top_agree}/{n}")
