# Build Plan

How chesster gets built, in small slices. Each slice is usable on its own and ends with a check against my real games. Design decisions behind this plan are in `docs/00-goals-and-context.md` (Repo role); gaps and evidence are in `docs/05-design-survey.md`.

Written October 25, 2026.

## What chesster does

1. Fetches my Chess.com games and finds rapid games with no archive file yet.
2. Runs Stockfish on each new game and flags my moves that cost 20+ points of winning chances.
3. Writes one markdown file per game: header, flagged moves with labels, engine answers folded away, and the PGN to paste into maiachess.com.

I read the file in VS Code's Markdown preview, study the flagged positions on maiachess.com, and write insights in my notebook.

## Out of scope

- A board or any UI beyond markdown files (maiachess.com is the board)
- Storing notebook data: tags, ✓/✗, lessons, weekly tallies
- Weekly or monthly summaries
- Running on a schedule or in GitHub Actions
- Accuracy %, Game Rating, inaccuracies (the Chess.com API returns `accuracies`; never render them)

## Stack

| Part | Choice | Why |
| --- | --- | --- |
| Language | Python, managed with `uv` | Already in my harness; one command to run |
| Chess logic | `python-chess` | PGN parsing, board state, UCI engine control |
| Engine | Stockfish via Homebrew (`brew install stockfish`) | Free, local; path configurable |
| HTTP | Python standard library | Two endpoints, no auth; no dependency needed |
| Config | `chesster.toml` at repo root | Username, thresholds, depth, Stockfish path |

Run with `uv run chesster`.

## Repo layout

```text
chesster.toml            # username, thresholds, engine settings
pyproject.toml
src/chesster/
    cli.py               # entry point and options
    fetch.py             # Chess.com archive API
    analyse.py           # Stockfish evaluation, flags, labels, merging
    render.py            # markdown output
games/
    2026-10/
        2026-10-24-vs-suresh_0705-185827995884.md
tests/
```

The game ID ends each filename, so dedupe is a filename check. Dates use America/Toronto time.

## Game file format

````markdown
---
url: https://www.chess.com/game/live/185827995884
date: 2026-10-24
colour: white
result: loss (checkmated)
opponent: suresh_0705 (932)
my_rating: 797
opening: Queen's Pawn Opening, Accelerated London System
---

# 2026-10-24 · White · Loss · vs suresh_0705 (932)

Opening: Queen's Pawn Opening, Accelerated London System
Clock left (me / opp): 3:12 / 8:40

## Flagged moves

1. **15. Bd3** · blunder · material · 4s on the clock

    <details>
    <summary>Engine answer</summary>

    Best: 15. Bxc6 · Punished by: 15... Nxe5 · +0.3 → −4.5

    </details>

## PGN

```pgn
[Event "Live Chess"]
...
```
````

The header matches the notebook entry's header (date, colour, result, opponent, opening, clocks), so I can copy it straight into the notebook.

## Slices

### Slice 0: Scaffold

- `pyproject.toml`, `uv` setup, `chesster.toml`, CLI stub, README usage section.
- **Done when:** `uv run chesster --help` works on my Mac.

### Slice 1: Fetch and archive

- List monthly archives; fetch each month; keep `time_class == "rapid"`.
- Skip games that already have a file; write header + PGN for the rest (no engine yet).
- Requests run one at a time with a descriptive User-Agent.
- Option `--game <url>` re-processes one game (overwrites its file).
- **Done when:** the first run writes all October 2026 rapid games (16 as of Oct 25), and a second run writes nothing.

### Slice 2: Stockfish flags

- For each of my moves: evaluate before and after at the configured depth, from my point of view. Convert to winning chances (Lichess curve, cp clamped to ±1000, a forced mate counted as ±1000 cp). Flag drops at or above the mistake threshold; mark blunders at the higher threshold.
- Missed chances need no special case: if the opponent hung a piece, my winning chances before my move are already high, so not taking it shows as a drop.
- Label each flag by type, in this order: **allowed mate in N**, **missed mate in N**, **lost material** (I'm 2+ points down within 2 moves), **missed material** (the best line wins 2+ within 3 moves), **deeper** (anything else). The mate distance shows whether a mate was simple.
- Mates go through the same Win% rule as everything else (mate = ±1000 cp), not Lichess's separate mate rules: its −700 / −999 cp cut-offs are tuned to its lower bars, and the clamp gives the same behaviour at ours (losing a mate while still +8 isn't flagged; losing it to 0.0 is).
- Merge consecutive flags for the same missed idea into one moment.
- **Safe-move count** on flags where I lost ground (types **material**-lost and **deeper**): score every legal move with MultiPV and count those within the mistake threshold of the best move, e.g. "35 of 48 moves held". Not shown on missed chances, where only the punishing move is "safe" and the count reads as hard when it usually isn't. Shown inside the fold, since it hints at the answer. Evidence: `docs/05-design-survey.md`.
- Render labels on top and engine answers (best move, punishing reply, eval change, safe-move count) in `<details>`.
- **Done when:** the October games reproduce the evidence in `docs/05-design-survey.md` (31 flags before merging, at depth 16), and the folds collapse in VS Code's preview.

### Slice 3: Clock and polish

- Show time spent on each flagged move (previous clock − current clock + 10 s increment). Supports question bank Q8 and the C tag, and reveals nothing about the answer.
- Option `--all-time-controls` to include blitz, daily and unrated games.
- Progress output while Stockfish runs (Nothing silent).
- **Done when:** I've used chesster for a week of real reviews and logged any friction.

## Maia track (in parallel)

### M1: Spike

Test **Maia-2 first**: it is trained on Lichess rapid (closer to 15+10 than Maia-3's blitz), has a (0, 1000] rating band, and maiachess.com's Platform v1 was built on it. Fall back to Maia-3 only if Maia-2 fails. See `docs/07-mistake-classification-research.md`.

Answer, on my Mac:

1. Which model does maiachess.com run today? chesster's classes should come from the same model as the Moves by Rating graph I look at.
2. Does Maia-2 install and run locally? Packaging, licence, Python version.
3. What inputs does it take? Fix the opponent's rating explicitly: it changes the predicted move in up to 6% of positions.
4. Does it return a probability for every legal move, including a move it wouldn't pick?
5. How long does a sweep across its rating bands take for one position, and for the 31 October flags?
6. Only if Maia-2 fails: repeat 2–5 for Maia-3 (CSSLab/maia3, AGPLv3; fine for local personal use, check before vendoring code).

**Output:** a go / no-go note in `docs/`, with timings.

### M2: Classification (only if M1 is a go)

- For each flag, sweep Maia for my move and Stockfish's best move; find the crossover; label N / L / X / R. Report in coarse bands with a minimum probability gap, and give explicit outcomes for "no crossover" and "multiple crossovers" (Maia-2's predictions move consistently with rating in only ~27% of positions).
- Before building, tighten the rules in survey gaps 5 and 6: numeric definitions of "rare", the 2000–2600 gap, multiple crossings, and which Maia rating counts as "me" (my Chess.com rating is now 773–816, not ~700).
- Optional: estimate how likely an opponent at my level was to find the punishing reply.

## Rules to confirm

Defaults chesster ships with. All live in `chesster.toml` so they can change without code changes.

| Rule | Default | Why / open point |
| --- | --- | --- |
| Mistake threshold | 20-point drop in winning chances | ≈ Studer's 2-point rule from a level position (0 → −2.3) |
| Blunder threshold | 30-point drop | About 2× Lichess (whose bars are 5 / 10 / 15 Win% points); close to Chess.com's Expected Points bands. See `docs/07` |
| Inaccuracies | Hidden | Non-negotiable |
| Engine depth | 16 | 16 games took about 2 minutes in the experiment; raise if the Mac is fast |
| Skip opening moves | None for Stockfish flags | The experiment skipped moves 1–5; a hung piece on move 4 still matters. The 5-move skip stays for Maia only |
| Order of flags | Game order | Matches stepping through the game on maiachess.com |
| Cap | Show all flags | The 3-moment cap applies to the notebook; about 2 flags per game in October |
| First material loss in a loss | Marked | The method says always include it |
| Merging | Consecutive flags of my moves with the same best move or punishing reply | Covers the 15...Rab8 / 16...a5 / 17...Rb5 case |
| Material values | P1 N3 B3 R5 Q9 | Standard |

## Validation for every slice

- Unit tests for winning-chance conversion, the point-of-view flip, merging and clock maths, using a fixture PGN.
- Run against my real October games and compare with the previous slice or the recorded evidence.
- No slice is done until it has run on my Mac, not just in a cloud session.
