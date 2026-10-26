"""Spike: Maia-2 rapid across its 11 rating bands for every flag. Usage: python maia2_sweep.py FLAGS_JSON MODEL_DIR OUT_JSON"""
import json, sys, time
from maia2 import model, inference
# One Elo per band: <1100, 1100-1199 … 1900-1999, >=2000
BANDS = [1000] + list(range(1150, 2000, 100)) + [2100]
t0 = time.monotonic(); m = model.from_pretrained(type="rapid", device="cpu", save_root=sys.argv[2]); prep = inference.prepare(); load_s = time.monotonic() - t0
def sweep(fen, selfs, oppos):
    return [inference.inference_each(m, prep, fen, s, o)[0] for s, o in zip(selfs, oppos)]
flags = json.load(open(sys.argv[1])); fen0 = flags[0]["fen"]
sweep(fen0, BANDS, BANDS)
t = time.monotonic(); sweep(fen0, BANDS, BANDS); one = time.monotonic() - t
t = time.monotonic()
for f in flags:
    f["site"] = sweep(f["fen"], BANDS, BANDS)
    f["fixed_opp"] = sweep(f["fen"], BANDS, [f["opp_elo"]] * len(BANDS))
all_s = time.monotonic() - t
res = dict(model="maia2-rapid", ratings=BANDS, load_s=load_s, one_sequential_s=one, all_flags_two_sweeps_s=all_s, n_flags=len(flags), flags=flags)
json.dump(res, open(sys.argv[3], "w")); print({k: v for k, v in res.items() if k != "flags"})
