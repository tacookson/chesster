# Build Plan

How chesster gets built, in small slices. Each slice is usable on its own and ends with a check against my real games. Design decisions behind this plan are in `docs/00-goals-and-context.md` (Repo role); gaps and evidence are in `docs/05-design-survey.md`.

Written October 25, 2026.

## What chesster does

1. Fetches my Chess.com games and finds rapid games with no archive file yet.
2. Runs Stockfish on each new game and flags my moves that cost 15+ points of winning chances.
3. Writes one markdown file per game, in review order: the header for hot notes, the PGN to paste into maiachess.com for my own review, then every flagged move with its label, folded until I open it after my own review.

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
        2026-10-23-vs-suresh_0705-185827995884.md
tests/
```

The game ID ends each filename, so dedupe is a filename check; other files in `games/` are ignored. A file written with `--no-engine` has `analysed: false` and is analysed by the next run with the engine on. Dates use America/Toronto time.

## Game file format

````markdown
---
match: 261023-2
url: https://www.chess.com/game/live/185827995884
date: 2026-10-23
colour: white
result: loss (checkmated)
opponent: suresh_0705 (932)
my_rating: 797
opening: Queen's Pawn Opening Accelerated London System
time_control: 900+10
rated: true
analysed: true
---

# 261023-2 · 23 Oct 2026 · Loss as White vs suresh_0705 (932)

## 1. Hot notes

You: 797 · 15+10 rated · Queen's Pawn Opening Accelerated London System  
Ended: you were checkmated · Clock left: you 9:28, opponent 11:04

## 2. Own review, engine off

Paste into maiachess.com and pick your own moments before opening the engine check.

```pgn
[Event "Live Chess"]
...
```

## 3. Engine check

<details>
<summary>Open after your own review</summary>

Stockfish flagged 2 moves. Go deep on the ones you choose.

### Move 15 as White: you played Bd3

**Blunder: you lost a piece.** This was the first material you lost in the game.

Time: 2m 03s on this move, 10:23 left.

<details>
<summary>Show the engine's answer</summary>

- **Better:** 15. Bxc6, taking the knight.  
  Line: 15. Bxc6 Qxc6 16. Qxc6 bxc6
- **What your move allowed:** 15... Nxe5, taking your bishop.  
  Line: 15... Nxe5 16. Qxd7 Nxd7
- **Effect:** about equal (+0.2) → losing (−4.6), from your side.
- **Difficulty:** 1 of your 37 legal moves kept your position.

</details>

### Move 26 as White: you played f4

**Blunder: you allowed a mate in 1.** You were already losing, so this didn't change the likely result.

Time: 4s on this move, 9:28 left.

<details>
<summary>Show the engine's answer</summary>

- **Better:** 26. Kf1.  
  Line: 26. Kf1 Qc4+ 27. Kg1 a5
- **What your move allowed:** 26... Qxe1#, taking your rook.  
  Line: 26... Qxe1#
- **Effect:** losing (−6.9) → forced mate against you (−M1), from your side.
- **Difficulty:** 7 of your 18 legal moves kept your position.

</details>

</details>
````

The sections follow the review order. The hot-notes lines match the notebook entry's header (date, colour, result, opponent, opening, clocks), so I can copy them straight into the notebook without seeing any engine output. A swing that didn't change the likely result adds, for example, "You were already losing, so this didn't change the likely result." to its label.

**Match ID** (`261023-2`): the game's local date as YYMMDD, then its number among that day's rapid games, by end time. Rapid games only; other time controls get none. It's worked out from Chess.com's game list each run, so re-processing a game with `--game` gives it the same ID. It goes in the notebook entry's `#` slot to link the page to the file.

## Slices

### Slice 0: Scaffold

- `pyproject.toml`, `uv` setup, `chesster.toml`, CLI stub, README usage section.
- **Done when:** `uv run chesster --help` works on my Mac.

### Slice 1: Fetch and archive

- List monthly archives; fetch each month; keep `time_class == "rapid"`.
- Skip games that already have a file; write header + PGN for the rest (no engine yet). Files written without the engine are picked up again once the engine runs.
- Requests run one at a time with a descriptive User-Agent.
- Option `--game <url>` re-processes one game (overwrites its file).
- **Done when:** the first run writes all October 2026 rapid games (16 as of Oct 25), and a second run writes nothing.

### Slice 2: Stockfish flags

- For each of my moves: evaluate before and after at the configured depth, from my point of view. Each game starts with an empty engine hash (`ucinewgame`), so a game's flags don't depend on which games ran before it. A game that ends in threefold repetition or the fifty-move rule scores its final position 0.0, so throwing a win away into a draw is flagged. A forced move (one legal move) is never flagged. Convert to winning chances (Lichess curve, cp clamped to ±1000, a forced mate counted as ±1000 cp). Flag drops at or above the mistake threshold; mark blunders at the higher threshold.
- Missed chances need no special case: if the opponent hung a piece, my winning chances before my move are already high, so not taking it shows as a drop.
- Label each flag by type, in this order: **allowed mate in N**, **missed mate in N**, **lost material** (I'm 2+ points down within 3 moves), **missed material** (the best line wins 2+ within 3 moves; both counts play on until the captures stop, so a trade isn't cut off half-way), **deeper** (anything else). The mate distance shows whether a mate was simple.
- Mates go through the same Win% rule as everything else (mate = ±1000 cp), so losing a mate while still +8 isn't flagged and losing it to 0.0 is. **Exception (Oct 25):** walking into a forced mate also follows Lichess's rule (blunder; mistake below −7; hidden below −10). A Maia game showed a mate-in-1 allowed at −7.5 costing only 3.4 Win% points, so the Win% rule alone never flagged it. Lichess's lost-mate rule is not copied: missing a mate while still +5 doesn't change the result.
- Merge consecutive flags for the same missed idea into one moment. The moment runs from the first move's eval to the last move's, and takes the worst severity and the most specific label among its moves.
- **Safe-move count** on flags where I lost ground (types **lost material**, **allowed mate** and **deeper**): score every legal move with MultiPV and count those within the mistake threshold of the best move, e.g. "35 of 48 moves held". Neither the move I played (even if the shallower count search rates it higher) nor a walk into an avoidable mate counts. The count is stated as a fact with no verdict ("hard spot", "careless slip"): cause is mine to judge. Not shown on missed chances, where only the punishing move is "safe" and the count reads as hard when it usually isn't. Shown inside the fold, since it hints at the answer. Evidence: `docs/05-design-survey.md`.
- Render the engine check last, after the header and PGN, inside a `<details>` fold to open after my own review. Inside it, each flag shows its label; its engine answer (best move, punishing reply, eval change, safe-move count) sits in a second `<details>`.
- **Already decided:** if I was already 2+ points down before the move, or still 2+ points up after it (`decided` in `chesster.toml`), the flag stays but its label adds that it didn't change the likely result.
- **Done when:** the 16 October games give about 43 flags before merging and 40 moments after (Stockfish 16, depth 16, 15-point bar, Oct 25; a newer Stockfish may differ by a few), and the folds collapse in VS Code's preview. The original 31 in `docs/05-design-survey.md` was at the old 20-point bar. **Done on my Mac, Oct 25.** Since then each game starts with an empty engine hash; before that, counts could shift with the order games were analysed in.

### Slice 3: Clock and polish

- Show time spent on each flagged move (previous clock − current clock + 10 s increment). Supports question bank Q8 and the C tag, and reveals nothing about the answer.
- Option `--all-time-controls` to include blitz, daily and unrated games.
- Progress output while Stockfish runs (Nothing silent).
- **Built Oct 25:** time spent and clock left show under each flag's headline, inside the engine-check fold but outside the engine answer's (for merged moments, one time per move; none for daily games). Progress shows the game, the stage and the position count.
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

### Deferred: a rating-scale difficulty score

Considered October 25, 2026 and set aside. The manual crossover on maiachess.com already answers "how hard was this?", and any score would be accurate only to a few hundred points, worst near my band (`docs/07`). Revisit if reading the crossover often goes over its 2–3 minutes or keeps giving no clear answer, or if M1 is a go.

Score the two questions separately:

- **Position difficulty (50% rating).** Sum Maia's probabilities over the safe moves (the slice 2 definition) at each rating. Report the rating where that sum crosses 50%, in bands, with "unclear" allowed. This is more robust than the two-line crossover and could replace it for N / L / X / R.
- **Temptation.** P(my move) at my rating, and the rating where it falls below about 10%.

Ideas that need no local Maia:

- **Lichess explorer by rating bucket.** Who actually plays my move in early positions (roughly moves 1–15). It covers the moves Maia skips. Check the current API and auth rules first.
- **Puzzle-theme median rating.** Median rating of Lichess puzzles with the missed idea's theme. Coarse.

Never show a single precise number. Difficulty is engine output, so it stays inside the fold.

## Rules to confirm

Defaults chesster ships with. All live in `chesster.toml` so they can change without code changes.

| Rule | Default | Why / open point |
| --- | --- | --- |
| Mistake threshold | 15-point drop in winning chances | Lowered from 20 on Oct 25: 20 matched Studer's 2-point rule only from equality and missed 2-pawn swings from slightly worse (−1.3 → −3.5 = 16.7 points). Lichess's blunder line. On the 16 October games: 32 → 39 flags. Also the safe-move cut-off |
| Blunder threshold | 30-point drop | About 2× Lichess (whose bars are 5 / 10 / 15 Win% points); close to Chess.com's Expected Points bands. See `docs/07` |
| Walking into mate | Blunder; mistake if I was already below −7; hidden below −10 | Lichess's rule (lila `Advice.scala`). Win% barely moves in a lost position, so without it a mate-in-1 allowed at −7.5 went unflagged. Moves that walk into an avoidable mate don't count as safe |
| Inaccuracies | Hidden | Non-negotiable |
| Engine depth | 16 | 16 games took about 2 minutes in the experiment; raise if the Mac is fast |
| Skip opening moves | None for Stockfish flags | The experiment skipped moves 1–5; a hung piece on move 4 still matters. The 5-move skip stays for Maia only |
| Order of flags | Game order | Matches stepping through the game on maiachess.com |
| Cap | Show all flags | Decided: the 3-moment cap applies to the notebook, and I pick which flags to go deep on; about 2 flags per game in October |
| Already decided | Flagged, labelled "didn't change the likely result" | Before ≤ −2.0 and after ≤ −2.0, or before ≥ +2.0 and after ≥ +2.0 (`decided = 200` cp) |
| Output order | Hot notes → own review → engine check | Decided: header first, PGN second, engine check last and folded |
| Cause judgements | None | Decided: the safe-move count is shown as a number only |
| First material loss in a loss | Marked | The method says always include it |
| Merging | Consecutive flags of my moves with the same best move or punishing reply | Covers the 15...Rab8 / 16...a5 / 17...Rb5 case |
| Material values | P1 N3 B3 R5 Q9 | Standard |

## Validation for every slice

- Unit tests for winning-chance conversion, the point-of-view flip, merging and clock maths, using a fixture PGN.
- Run against my real October games and compare with the previous slice or the recorded evidence.
- No slice is done until it has run on my Mac, not just in a cloud session.
