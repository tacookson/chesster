"""Crossover shapes with a minimum probability gap. Usage: summary.py OUT_JSON KEY GAP"""
import json, sys
from collections import Counter
res = json.load(open(sys.argv[1])); R = res["ratings"]; key = sys.argv[2]; G = float(sys.argv[3])
c = Counter(); xs = []
near = lambda r: min(range(len(R)), key=lambda i: abs(R[i] - r))
for f in res["flags"]:
    pm = [d.get(f["played"], 0) for d in f[key]]; pb = [d.get(f["best"], 0) for d in f[key]]
    gap = [b - m for b, m in zip(pb, pm)]
    state = [1 if g >= G else -1 if g <= -G else 0 for g in gap]
    seq = [s for s in state if s]; flips = sum(1 for a, b in zip(seq, seq[1:]) if a != b)
    if all(g >= 0 for g in gap): k = "best ≥ mine at every rating"
    elif not seq or all(s == -1 for s in seq): k = "mine ahead or too close everywhere (no clear crossover)"
    elif seq[0] == -1 and flips == 1:
        k = "one clear crossover"; xs.append(R[next(i for i, s in enumerate(state) if s == 1)])
    elif seq[0] == 1 and flips == 0: k = "best ahead, gap < threshold somewhere"
    else: k = f"multiple crossings"
    c[k] += 1
    for r in (800, 1100, 1400):
        c[f"P(mine) < 5% at {R[near(r)]}"] += pm[near(r)] < 0.05
print(f"{res['model']} [{key}] gap ≥ {G}: n = {len(res['flags'])}")
for k, v in sorted(c.items()): print(f"  {k}: {v}")
print("  clear-crossover ratings:", sorted(xs))
