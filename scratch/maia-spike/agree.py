"""Per-flag shape agreement between two sweeps (same gap rule as summary.py).

Usage: python agree.py OUT_A KEY_A OUT_B KEY_B
"""
import json, sys
def shapes(path, key, G=0.05):
    res = json.load(open(path)); R = res["ratings"]; out = []
    for f in res["flags"]:
        pm = [d.get(f["played"], 0) for d in f[key]]; pb = [d.get(f["best"], 0) for d in f[key]]
        gap = [b - m for b, m in zip(pb, pm)]; st = [1 if g >= G else -1 if g <= -G else 0 for g in gap]
        seq = [s for s in st if s]; flips = sum(1 for a, b in zip(seq, seq[1:]) if a != b)
        if all(g >= 0 for g in gap) or (seq and seq[0] == 1 and flips == 0): k = ("ahead", None)
        elif not seq or all(s == -1 for s in seq): k = ("none", None)
        elif seq[0] == -1 and flips == 1: k = ("cross", R[st.index(1)])
        else: k = ("multi", None)
        out.append(k)
    return out
a, b = shapes(sys.argv[1], sys.argv[2]), shapes(sys.argv[3], sys.argv[4])
same = sum(x[0] == y[0] for x, y in zip(a, b))
close = sum(x[0] == y[0] and (x[1] is None or abs(x[1] - y[1]) <= 300) for x, y in zip(a, b))
print(f"{sys.argv[1]}:{sys.argv[2]} vs {sys.argv[3]}:{sys.argv[4]}: same shape {same}/42, same shape and crossover within 300 {close}/42")
