# Maia Spike (M1)

Result of the M1 spike in `docs/06-build-plan.md`: can chesster run Maia locally and read the probability of my move and Stockfish's best move across ratings?

Run October 25, 2026, in a Linux cloud container (4 vCPU Intel Xeon 2.1 GHz, CPU only, Python 3.12, Stockfish 16 from apt). **Not yet re-run on my Mac**, so every timing below is a cloud timing and needs re-checking there (see "What to run on the Mac").

## Verdict

**Go for M2, on Maia-3, not Maia-2.**

- **Maia-2 fails the goal.** It installs and runs, but its lowest rating band is "under 1100". So 600, 800 and 1000 all give the same answer, and my band of interest (about 1000–1200 on Lichess) straddles a band edge. It is also not the model maiachess.com uses, and it found a clear crossover in only 3 of 42 flags.
- **Maia-3 works.** It takes any rating, returns a probability for every legal move, and sweeps all 42 October flags across 21 ratings in about 8 seconds in the cloud. The ONNX file maiachess.com serves to my browser runs with `onnxruntime` and `numpy`, without torch. That gives exactly the numbers behind the Moves by Rating graph.
- **The caveat for M2:** a clean crossover is the minority case. Of 42 flags, 9 have one clear crossover, 22 have the best move ahead of mine at every rating, 7 have no clear crossover and 1 crosses more than once. N/L/X/R can be automated only if M2 gives explicit outcomes for the non-crossover shapes, as `docs/07` already predicted.

## Inputs used

- 16 October rapid games for Me4tbegZ0r, fetched with `uv run chesster` (config copy with `[engine] path = "/usr/games/stockfish"`, output to a scratch directory, not `games/`).
- Stockfish 16 at depth 16, current `chesster.toml` thresholds (mistake 15, blunder 30). **42 flags before merging, 38 moments after.** The "31 October flags" in `docs/06` M1 were counted at the old 20-point bar.
- For each flag: the position before my move, my move, Stockfish's best move, my rating and the opponent's Chess.com rating.

## 1. Which model does maiachess.com run today?

**Maia-3**, as a single ONNX file run in the browser. Evidence, gathered October 25, 2026:

- The site's JavaScript (the `_app` bundle served with `/analysis`) creates its Maia engine with `model: "/maia3/maia3_simplified.onnx"` and `modelVersion: "3"`. Server requests carry `maia_version: "maia3"`. The download prompt reads "Maia-3 runs entirely on your device and requires a one-time 44mb download."
- **Moves by Rating** calls `batchEvaluateMaia3` with 21 ratings, 600 to 2600 in steps of 100. It passes the same list as both the player's and the opponent's rating, so each point on the graph is "a 1400 playing a 1400".
- `maia3_simplified.onnx` is 45.7 MB, last modified October 19, 2026. It holds 22.7 M fp16 parameters and takes one position (a 64×12 board) plus two ratings.
- It is **not byte-for-byte any Hugging Face release.** On the 42 flags at 21 ratings, Maia3-23M (PyTorch) picked the same top move in 793 of 882 cases (90%), with a mean probability difference of 0.006 and a worst case of 0.39. I checked the tokenisation and padding against the site's code, and they don't explain the gap. My best guess is a separate single-position export or fine-tune, which fits the name "simplified".
- The Maia-2 README now says "Maia-3 is recommended for new projects" and links maiachess.com.
- This settles the open question in `docs/03` and `docs/04` (July 2026 review saw Maia-2). The site has moved to Maia-3. `docs/07`'s line that the Blunder Meter and Moves by Rating "are built on Maia-2" is out of date.

Sources: [maiachess.com/analysis](https://www.maiachess.com/analysis) (bundle inspected directly), [CSSLab/maia2 README](https://github.com/CSSLab/maia2), [CSSLab/maia3](https://github.com/CSSLab/maia3), [Maia3-23M model card](https://huggingface.co/UofTCSSLab/Maia3-23M), [Maia Chess on X, Maia-3 launch](https://x.com/maiachess/status/2058643976136069365), [maia-platform-frontend](https://github.com/CSSLab/maia-platform-frontend). A third-party repo, [bqrio/maia3-onnx](https://huggingface.co/bqrio/maia3-onnx), describes the same "simplified" interface with the timing head dropped. It is unofficial, so I'm citing it only as corroboration.

## 2. Does it install and run locally?

| | Maia-2 | Maia-3 (PyTorch release) | Maia-3 (site ONNX) |
| --- | --- | --- | --- |
| Package | `pip install maia2` (0.11.0 on PyPI) | Not on PyPI; install from git (`CSSLab/maia3`, version 0.1.0) | No package; one `.onnx` file plus `onnxruntime` and `numpy` |
| Python | **3.10–3.12 only** (`<3.13`) | ≥ 3.10 | Any supported by onnxruntime (tested 3.12) |
| Heavy dependencies | torch 2.8, pandas, gdown | torch, huggingface-hub | onnxruntime (no torch) |
| Weights | 280 MB rapid model, from Google Drive (via gdown) | Hugging Face: 5M 21 MB, 23M 88 MB, 79M 302 MB | 45.7 MB from maiachess.com |
| Licence | MIT | **AGPLv3** (code). Weights' licence not stated on the model card | Frontend is GPLv3; the model file's own licence isn't stated |
| Ran here? | Yes | Yes (5M, 23M, 79M) | Yes, **but onnxruntime 1.31 segfaulted with default graph optimisation**. It runs with optimisation turned off |

**Licence and vendoring.** Nothing was vendored. For M2:

- **Maia-2 (MIT)** could be vendored with its notice, but it's the no-go model.
- **Maia-3 code (AGPLv3):** depend on it rather than copying it in. If chesster vendored it and was ever distributed, chesster would have to be AGPL too. A git dependency in `pyproject.toml` avoids that.
- **Site ONNX:** download it at first run (as the browser does) and keep it out of git, since its licence is unstated.
- My spike's tokeniser is a 15-line reimplementation of a 64×12 one-hot board, which is a standard encoding. I'd still keep it outside the repo until you decide how M2 loads the model.

## 3. What inputs does it take?

- **Maia-2:** a FEN plus the player's and opponent's ratings. Each rating is snapped into one of 11 bands: <1100, 1100–1199 … 1900–1999, ≥2000. No move history, no clock. It returns move probabilities (rounded, so very rare moves show as 0.0) and White's expected score.
- **Maia-3 (PyTorch):** the current position plus up to 7 previous positions (by default the current one is repeated), the player's and opponent's ratings as plain integers (0–5000, interpolated smoothly, no bands), and a clock-thinking-time input that the UCI wrapper sets to 0.
- **Site ONNX:** current position only, plus the two ratings as floats. No history, no clock.
- **Opponent rating has to be fixed explicitly.** The site sets opponent = player. Fixing the opponent at their actual Chess.com rating changed the crossover shape in 4 of 42 flags (38 of 42 unchanged). M2 needs a rule; matching the site (opponent = player) keeps chesster's answer equal to what I see on the graph.
- **Board orientation:** both models mirror the board when Black is to move, and moves come back in normal notation. chesster can pass a FEN and a UCI move directly.

## 4. A probability for every legal move?

**Yes, for both.** In all 42 flagged positions, every legal move had a probability (softmax over the legal moves only). The smallest Maia-3 probability was about 3 × 10⁻⁹, so even a move it would never pick has a value. Maia-2's output is rounded and shows 0.0 for very rare moves; that is fine for "rare" thresholds, but not for ratios.

## 5. Timings (cloud, CPU only; re-check on Mac)

One position = one sweep across all rating bands (21 for Maia-3, 11 for Maia-2). "All flags" = 42 positions, with two sweeps each (opponent = player, and opponent fixed). Halve it for one sweep.

| Model | Load | One position, batched | One position, one rating at a time | All 42 flags × 2 sweeps |
| --- | --- | --- | --- | --- |
| Maia-3 site ONNX (onnxruntime, optimisation off) | 0.7 s | 0.21 s | 0.59 s | 15.6 s |
| Maia-3 5M (PyTorch) | 2.7 s | 0.05 s | 0.21 s | 4.1 s |
| Maia-3 23M (PyTorch) | 0.7 s | 0.21 s | 0.41 s | 12.7 s |
| Maia-3 79M (PyTorch) | 8.1 s | 0.42 s | 1.0 s | 37.0 s |
| Maia-2 rapid (PyTorch) | 1.3 s | n/a | 0.08 s | 8.1 s |

For scale, the Stockfish pass for the same 16 games took 3 min 28 s here, with Stockfish 16 at depth 16. My Mac runs Homebrew's Stockfish, a newer version, so flags may differ slightly. Any of the Maia options adds seconds, not minutes, to a run. Load times exclude the one-time download.

## 6. Maia-3 (because Maia-2 failed)

Items 2–5 above cover it. Maia-2 "failed" for this purpose, not technically. It ran fine, but its bands can't separate 600 from 1099. It isn't the model behind the graph I read, and it rarely shows a crossover: 3 clear crossovers in 42 flags, against 9 for the site model and 10 for Maia3-23M.

## Crossovers in the October flags

**How I counted.** A "clear" crossover means the best move's lead over my move goes from ≤ −5 points to ≥ +5 points, once, with ratings rising. The site model sweeps 600–2600, with opponent = player.

| Shape | Site ONNX | Maia3-23M | Maia-2 |
| --- | --- | --- | --- |
| One clear crossover | 9 | 10 | 3 |
| Best move ≥ my move at every rating | 22 | 21 | 22 |
| Best ahead, but within 5 points somewhere | 3 | 3 | 4 |
| My move ahead, or too close, everywhere (no crossover) | 7 | 8 | 12 |
| Multiple crossings | 1 | 0 | 1 |
| P(my move) < 5% at 1100 | 16 | 15 | 20 (at 1150) |

- **Clear-crossover ratings (site):** 1400, 1700, 1700, 1800, 1800, 1900, 2000, 2300, 2600.
- **Monotonicity:** P(best) rises steadily in 17 of 42, P(my move) falls steadily in 21, and both happen in 11 (26%). That matches the ~27% Maia-2's paper reports (`docs/07`).
- **Model agreement:** the site ONNX and Maia3-23M give the same shape on 35 of 42 flags, and the same shape with the crossover within 300 points on 33. 79M: 34 and 33. 5M: 33 and 31.
- **What it means:** most of my October flags are moves almost nobody at any level plays. P(my move) is under 5% at 1100 in 16 of 42. That is the R ("random lapse") pattern, and it fits flags that are mostly hung pieces. Only about a quarter of flags have the textbook crossover the N/L/X labels depend on.

### Three positions (P in %, site model unless noted)

**PRO_311, 23 Oct, 11... Rb8 (best 11... Ba6).** Lost material, +0.1 → −2.6. A clean crossover at 1800.

| Rating | 600 | 800 | 1000 | 1100 | 1200 | 1400 | 1600 | 1800 | 2000 | 2200 | 2600 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P(Rb8, mine) | 51 | 59 | 64 | 64 | 63 | 56 | 43 | 26 | 14 | 6 | 2 |
| P(Ba6, best) | 10 | 8 | 7 | 8 | 8 | 12 | 21 | 36 | 52 | 67 | 77 |

Maia3-23M crosses at the same rating (best 35 vs mine 31 at 1800). Maia-2 never crosses: at its top band (≥2000), mine is 33 and best is 26. Under `docs/02` this is L if "me" is 1100–1500 (crossover 300–800 above).

**CHOCHOWINS, 18 Oct, 15... Rab8 (best 15... Bxf3).** Deeper, −0.1 → −2.6. Multiple crossings.

| Rating | 600 | 800 | 1000 | 1100 | 1200 | 1400 | 1600 | 1800 | 2000 | 2200 | 2600 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P(Rab8, mine) | 21 | 24 | 27 | 29 | 32 | 35 | 36 | 34 | 26 | 13 | 2 |
| P(Bxf3, best) | 37 | 37 | 31 | 27 | 23 | 17 | 16 | 18 | 27 | 45 | 74 |

Best is ahead up to 1000, mine is ahead from 1100 to 1900, and best leads again from 2000. The answer depends on the model: 23M shows mine ahead from 600 to 2100, then one crossover at about 2200. Fixing the opponent at 607 flattens it, with best ahead only up to about 1100. This is the case M2 must report as "unclear" rather than force into N or L.

**bigbird775, 10 Oct, 11... Bxf3 (best 11... Nxd5).** Lost material, +5.8 → −0.3. No crossover needed.

| Rating | 600 | 800 | 1000 | 1100 | 1200 | 1400 | 1600 | 1800 | 2000 | 2200 | 2600 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P(Bxf3, mine) | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| P(Nxd5, best) | 5 | 5 | 5 | 6 | 7 | 10 | 14 | 20 | 30 | 45 | 67 |

My move is essentially never played, so this is R (a lapse). But the best move is also rare at my level (5–7%), because players at 1100 spread across many safe moves. "Best ≥ mine everywhere" alone doesn't mean "easy". M2's R rule should use P(my move) at my rating (or the safe-move sum from `docs/06` "Deferred"), not the two-line comparison.

## What M2 needs from me

1. **Which Maia rating counts as "me" (Q5).** It matters: P(my move) < 5% holds for 12 flags at 800, 16 at 1100 and 20 at 1400. So the number of R labels moves with this choice. Maia-3 accepts any value, so this is a judgement call, not a band limit. Options: a fixed number (e.g. 1100), or one derived from my current Chess.com rapid rating (773–816) through a conversion I'd need to source. The 1000–1200 band in the docs came from ~700 and hasn't been re-derived.
2. **Which model:** the site ONNX (identical to the graph, light dependencies, unstated licence, downloaded from maiachess.com, and could change when they redeploy) or Maia3-23M from Hugging Face (versioned, AGPLv3 code dependency, needs torch, same crossover shape as the graph on 35 of 42 flags). I lean towards the site ONNX, because "same model as the graph I look at" was M1's first requirement.
3. **Opponent rating rule:** opponent = player (as the site does) or the actual opponent's rating. I lean towards opponent = player, so the graph and chesster agree.
4. **Numeric rules from survey gaps 5 and 6**, now with data. The two are below.
   - **Gap 5 needs:** a "rare" threshold (5% used here), the minimum probability gap for a crossover (5 points used here), and what to call "best ahead everywhere", "no crossover" and "multiple crossings".
   - **Gap 6 needs:** where a crossover at 2000–2600 goes (3 of the 9 here).
5. **Whether to keep the spike scripts** (see below).

## What to run on the Mac

The cloud run needs confirming on macOS before M2 starts:

1. **Python 3.12 is available to uv** (`uv python list`). Maia-2 needs it; Maia-3 and onnxruntime don't.
2. **The site ONNX sweep with onnxruntime**, first with default graph optimisation, to see whether the Linux segfault happens on macOS, then with optimisation off. Note the timings.
3. **Maia3-23M on CPU and on Apple MPS**: load time, one-position sweep, and all-flags sweep.
4. **`brew info stockfish`** for the version, then `uv run chesster` on a scratch copy of the config to check the flag count (42 here with Stockfish 16).

These need the spike scripts, which currently live only in the cloud session's scratch directory and disappear when it ends.
