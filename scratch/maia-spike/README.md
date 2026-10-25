# Maia spike scripts (M1)

Throwaway scripts behind `docs/08-maia-spike.md`. Not part of chesster, and not tested. Model files and outputs go in a scratch folder outside the repo (`~/maia-spike` below); none of them belong in git.

| Script | What it does |
| --- | --- |
| `extract_flags.py` | Runs Stockfish on chesster game files; writes every pre-merge flag (FEN, my move, best move, ratings) as JSON |
| `site_sweep.py` | maiachess.com's Maia-3 ONNX across 600–2600, onnxruntime only |
| `maia3_sweep.py` | Maia-3 PyTorch release (5m / 23m / 79m) across 600–2600 |
| `maia2_sweep.py` | Maia-2 rapid across its 11 bands |
| `onnx_check.py` | How close a `maia3_sweep.py` result is to the site ONNX |
| `summary.py` | Crossover shapes with a minimum gap (the table in docs/08) |
| `crossovers.py` | Per-position P(my move) / P(best) tables and monotonic counts |
| `agree.py` | Per-flag shape agreement between two sweeps |

Each sweep writes two sets of probabilities per flag: `site` (opponent = player, as maiachess.com does) and `fixed_opp` (opponent at their Chess.com rating).

## Running on the Mac

From the repo root. Licences: Maia-2 MIT, Maia-3 code AGPLv3 (installed, not copied in), site ONNX licence unstated (downloaded, not committed).

```sh
W=~/maia-spike; mkdir -p $W
brew info stockfish | head -1                      # note the version (cloud run used 16)
uv python list | grep 3.12                         # Maia-2 needs Python 3.10–3.12

# 1. Games and flags (42 flags with Stockfish 16)
sed "s#games_dir = \"games\"#games_dir = \"$W/games\"#" chesster.toml > $W/chesster.toml
uv run chesster --config $W/chesster.toml
uv run python scratch/maia-spike/extract_flags.py $W/games $W/flags.json

# 2. Maia-3 environment and the site model
uv venv -p 3.12 $W/.venv-maia3
VIRTUAL_ENV=$W/.venv-maia3 uv pip install "maia3 @ git+https://github.com/CSSLab/maia3" onnxruntime numpy torch
curl -o $W/maia3_simplified.onnx https://www.maiachess.com/maia3/maia3_simplified.onnx

# 3. Site ONNX: default optimisation first (segfaulted on Linux), then with it off
$W/.venv-maia3/bin/python -I scratch/maia-spike/site_sweep.py $W/flags.json $W/maia3_simplified.onnx $W/out_site.json --ort-default
$W/.venv-maia3/bin/python -I scratch/maia-spike/site_sweep.py $W/flags.json $W/maia3_simplified.onnx $W/out_site.json

# 4. Maia3-23M on CPU and Apple GPU, then compare with the site model
$W/.venv-maia3/bin/python -I scratch/maia-spike/maia3_sweep.py $W/flags.json $W/out_23m.json 23m cpu
$W/.venv-maia3/bin/python -I scratch/maia-spike/maia3_sweep.py $W/flags.json $W/out_23m_mps.json 23m mps
$W/.venv-maia3/bin/python -I scratch/maia-spike/onnx_check.py $W/out_23m.json $W/maia3_simplified.onnx

# 5. Summaries
$W/.venv-maia3/bin/python -I scratch/maia-spike/summary.py $W/out_site.json site 0.05
$W/.venv-maia3/bin/python -I scratch/maia-spike/crossovers.py $W/out_site.json site "Rb8 (best Ba6),Rab8,Bxf3 (best Nxd5)"
```

Each sweep prints `load_s`, `one_batched_s`, `one_sequential_s` and `all_flags_two_sweeps_s`; compare them with the cloud table in docs/08. `maia3_sweep.py` caches Hugging Face weights next to its output (`<OUT_JSON>.hf/`).

Maia-2 (optional, it's the no-go model):

```sh
uv venv -p 3.12 $W/.venv-maia2 && VIRTUAL_ENV=$W/.venv-maia2 uv pip install maia2
$W/.venv-maia2/bin/python -I scratch/maia-spike/maia2_sweep.py $W/flags.json $W/maia2_models $W/out_maia2.json
```
