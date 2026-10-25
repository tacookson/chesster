"""Spike: Maia-3 move probabilities across ratings for chesster's flagged positions.

Usage: python maia3_sweep.py FLAGS_JSON OUT_JSON MODEL(5m|23m|79m) [DEVICE(cpu|mps)]

Compare with the site model afterwards with onnx_check.py.
"""
import json, sys, time
from collections import deque
import chess, torch
from maia3.uci import parse_args, Maia3UCIEngine
from maia3.dataset import get_historical_tokens, get_legal_moves_mask, tokenize_board
from maia3.utils import mirror_move

RATINGS = list(range(600, 2601, 100))  # what maiachess.com's Moves by Rating sweeps
flags_path, out_path, size = sys.argv[1:4]
device = sys.argv[4] if len(sys.argv) > 4 else "cpu"

t0 = time.monotonic()
cfg = parse_args(["--model", size, "--device", device, "--cache-dir", sys.argv[2] + ".hf"])
eng = Maia3UCIEngine(cfg); eng.ensure_model_loaded(); model = eng.model
load_s = time.monotonic() - t0
moves = eng.all_moves_dict; idx_to_move = eng.idx_to_move


def tokens_for(board):
    return get_historical_tokens(deque([tokenize_board(board)], maxlen=cfg.history), cfg,
                                 base=0.0, inc=0.0, clk_left_before=0.0, clk_ponder=0.0)


@torch.no_grad()
def sweep(fen, self_elos, oppo_elos):
    """Probability of every legal move at each (self, oppo) pair. Returns list of {uci: p}."""
    board = chess.Board(fen)
    toks = tokens_for(board).unsqueeze(0).expand(len(self_elos), -1, -1).to(device)
    logits, _, _ = model(toks, torch.tensor(self_elos, device=device), torch.tensor(oppo_elos, device=device))
    mask = get_legal_moves_mask(board, moves)
    probs = torch.softmax(logits.float().cpu().masked_fill(~mask, float("-inf")), dim=-1)
    legal = mask.nonzero().flatten().tolist()
    out = []
    for row in probs:
        d = {}
        for i in legal:
            u = idx_to_move[i]
            d[u if board.turn == chess.WHITE else mirror_move(u)] = row[i].item()
        out.append(d)
    return out


flags = json.load(open(flags_path))
# Timings
fen0 = flags[0]["fen"]
sweep(fen0, RATINGS, RATINGS)  # warm-up
t = time.monotonic(); sweep(fen0, RATINGS, RATINGS); one_batched = time.monotonic() - t
t = time.monotonic()
for r in RATINGS:
    sweep(fen0, [r], [r])
one_seq = time.monotonic() - t

t = time.monotonic()
for f in flags:
    f["site"] = sweep(f["fen"], RATINGS, RATINGS)                       # self = oppo, like the site
    f["fixed_opp"] = sweep(f["fen"], RATINGS, [f["opp_elo"] + 0] * len(RATINGS))  # opponent fixed at their Chess.com rating
all_s = time.monotonic() - t

result = dict(model=size, ratings=RATINGS, load_s=load_s, one_batched_s=one_batched, one_sequential_s=one_seq,
              all_flags_two_sweeps_s=all_s, n_flags=len(flags), flags=flags)

json.dump(result, open(out_path, "w"))
print({k: v for k, v in result.items() if k != "flags"})
