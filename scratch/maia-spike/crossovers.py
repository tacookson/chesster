"""Summarise P(my move) and P(Stockfish best) across ratings; count crossovers and monotonic positions.

Usage: python crossovers.py OUT_JSON [site|fixed_opp] [all | comma-separated substrings of "<opponent> <move> (best <move>)"]
"""
import json, sys
from collections import Counter
res = json.load(open(sys.argv[1])); R = res["ratings"]; key = sys.argv[2] if len(sys.argv) > 2 else "site"
show = sys.argv[3].split(",") if len(sys.argv) > 3 else []
stats = Counter(); first_x = []
def mono(xs, up):  # non-strict, tolerance 0.005
    return all((b - a) >= -0.005 if up else (a - b) >= -0.005 for a, b in zip(xs, xs[1:]))
for f in res["flags"]:
    pm = [d.get(f["played"], 0) for d in f[key]]; pb = [d.get(f["best"], 0) for d in f[key]]
    gap = [b - m for b, m in zip(pb, pm)]
    signs = [1 if g > 0 else -1 for g in gap]
    crossings = [R[i + 1] for i in range(len(R) - 1) if signs[i] < 0 < signs[i + 1]]
    recross = sum(1 for i in range(len(R) - 1) if signs[i] > 0 > signs[i + 1])
    opening = f["ply"] < 10
    stats["opening (first 5 moves)"] += opening
    if signs[0] > 0: kind = "best already ahead at lowest rating"
    elif not crossings: kind = "no crossover (my move stays ahead)"
    elif len(crossings) + recross > 1: kind = "multiple crossings"
    else: kind = "one clean crossover"
    stats[kind] += 1
    stats["P(best) monotonic up"] += mono(pb, True); stats["P(my move) monotonic down"] += mono(pm, False)
    stats["both monotonic"] += mono(pb, True) and mono(pm, False)
    if crossings: first_x.append(crossings[0])
    tag = f"{f['game'].split('-vs-')[1][:-13]} {f['label']} (best {f['best_san']})"
    if any(s in tag for s in show) or "all" in show:
        print(f"\n{tag} [{f['kind']}, {f['before']}→{f['after']}, opp {f['opp_elo']}] {kind}; crossings at {crossings}")
        print("  rating   " + " ".join(f"{r:>5}" for r in R))
        print("  P(mine)  " + " ".join(f"{p:5.2f}" for p in pm))
        print("  P(best)  " + " ".join(f"{p:5.2f}" for p in pb))
print(res["model"], key, "n =", len(res["flags"]))
for k, v in stats.items(): print(f"  {k}: {v}")
print("  first-crossover ratings:", sorted(Counter(first_x).items()))
