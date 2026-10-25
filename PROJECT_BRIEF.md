# Project Brief: Chess Game Analysis Repo

## Purpose

Help me (a ~700 Chess.com rapid player) analyze my own games using the review method in `docs/01-review-process.md`, faster and more consistently, without replacing the parts that make me better: thinking before the engine, writing one lesson, and tracking patterns.

## Principles the tooling must respect

1. **My thinking comes first.** Never show engine output before I've recorded my own moments. Anything automated should support the "hot notes → own review → engine check" order, not skip it.
2. **Only big swings matter.** Surface moves that cost about 2+ points *and* changed the likely result (judge by winning chances, not raw centipawns). Hide inaccuracies, Accuracy %, and small differences between engine lines.
3. **Cap the output.** At most 3 moments and 1 lesson per game. More detail is noise at this level.
4. **Track patterns over time.** The value is in the weekly tally (H/M/T/K/C/O/E) and the ✓/✗ ratio, not in any single game.
5. **Human context from Maia.** For each moment, classify it N / L / X / R using the crossover method (`docs/02-maia-mistake-classification.md`).
6. **Paper stays primary.** I take notes in a physical notebook. Tooling should prepare and summarize, not force me to type everything.
7. **Free tools only.** No paid Chess.com membership assumed.

## Inputs available

- My Chess.com rapid games (PGN), including clock times per move.
- Stockfish for objective evaluation (Stockfish 19 is current as of September 2026).
- Maia-3 models for human move prediction at a given rating (open source; see `docs/03-maia-guide.md`).
- My notebook entries and weekly tallies (manual input, if the tool tracks them).

## Candidate features (ideas, not decisions)

| Idea | Supports which step | Notes |
| --- | --- | --- |
| Fetch my recent rapid games from Chess.com | Setup | Chess.com has a public published-data API with monthly game archives per player; verify the current endpoint and rate limits |
| Swing finder: list moves where my winning chances dropped sharply | Step 3 engine check | Convert evals to win % (Lichess-style curve), flag drops that matter, hide the rest |
| "Before" positions only | Steps 2–3 | Show the position before each swing without revealing the best move, so I can guess first |
| Clock check | Question bank Q8, C tag | Flag critical moves played in under ~10 seconds |
| Maia crossover per moment | Weekly Maia session | Run Maia across ratings 600–2600 for my move vs the best move; report the crossover and suggested N/L/X/R class |
| Printable game sheet | Notebook | Pre-fill the header (date, colour, result, opponent, opening, clocks) and leave the moments blank |
| Weekly / monthly summary | Weekly page, monthly check | Tally tags, ✓/✗ ratio, N vs R counts, top tag, suggested drill |
| Replay list | Weekly Maia session | Export FENs of positions to replay against Maia (before N/R moments, winning positions) |

## Key domain facts for implementers

- Chess.com shows evaluations from White's side; maiachess.com shows them from the side to move. Normalize to one convention.
- Lichess labels mistakes by drops in winning chances (10 / 20 / 30 points = inaccuracy / mistake / blunder, per forum quotes of its code). See `docs/04-research-notes.md`.
- Maia uses the Lichess rating scale. My ~700 Chess.com rapid maps to roughly 1000–1200 there (approximate).
- Maia-3 was trained on Lichess blitz games (Jan 2023 – Jul 2025); it's a close guide for 15+10 rapid, not exact.
- Maia's top-move prediction is right about 57% of the time; trust patterns across games, not single positions.
- Skip the first ~5 moves for Maia classification (memorized openings).

## Open questions for me

1. What form should the repo take: a command-line script, a notebook, a small web page, something else?
2. Should it store my notebook data (tags, lessons), or only prepare and summarize games?
3. Run engines locally (Stockfish binary, Maia-3 model files) or rely on websites (Chess.com, Lichess, maiachess.com)?
4. Printed sheets vs a screen view for the per-game prep?
5. Which Maia rating to treat as "my level" (default 1100) and whether to recalibrate as my rating changes.
