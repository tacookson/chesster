# Goals and Context

## Player profile

| Item | Value |
| --- | --- |
| Platform | Chess.com |
| Time control | Rapid, 15+10 |
| Rating | About 700 Chess.com rapid (roughly 1000–1200 on the Lichess scale) |
| Volume | 5–7 games a week |
| Review time budget | 10–20 minutes per game |
| Note-taking | Physical paper notebook |
| Timezone | America/Toronto |

## Goals

1. A clear, repeatable process for analyzing each game.
2. A notebook template: sections, what goes in each, questions to ask.
3. Light enough that I actually do it consistently.
4. Specific, practical guidance on using an engine at my level.
5. Use Maia to tell apart mistakes that slightly better players avoid from mistakes even strong players make.

## Decisions made

**Repo role** (decided October 25, 2026)

- The notebook is the only place insights and tracking live: tags, ✓/✗, Maia classes, lessons and weekly tallies stay on paper.
- The repo does two things: (1) identifies mistakes and blunders by engine, used alongside the open notebook during review; (2) archives the games I've played for later reference.
- The repo does not store notebook data.
- **Shape: a companion to maiachess.com.** chesster fetches Chess.com games, archives them, runs Stockfish to list each game's flagged moves, and hands over the PGN to paste into maiachess.com. Positions are studied on maiachess.com with the notebook open. A standalone tool with its own board and local Maia-3 is deferred until pasting into Maia proves to be real friction.
- **Runs on:** my laptop (macOS), triggered manually. Not GitHub Actions.
- **Input:** triggered manually when I sit down to review, which may be after several games.
- **Output:** a markdown file per game, which is also its archive entry.
- **Archive scope:** new games from October 2026 onward; no backfill.

**Review method**

- Four steps per game, about 15 minutes: hot notes (2 min) → my own review, engine off (5–7 min) → engine check (4–6 min) → one lesson plus tally (2 min).
- Self-review uses a trimmed version of GM Noël Studer's 3×3 method: *up to* three moments, three "why" questions each, *one* lesson per game.
- In a loss, always include the *first* moment I lost material, not just the final blunder.
- Short versions exist: 10 minutes, and a 3-minute "bad day" version. Clean wins get a 5-minute lite review.
- An optional move-by-move deep review (30–45 min) for an interesting game, at most once a week. Thinking happens on the analysis board; only the top 2–3 findings go in the notebook.

**Engine use**

- Main engine step uses the **Chess.com Analysis board** (magnifying glass), *not* Game Review.
- Setup: 2–3 engine lines, depth 18–20, suggestion arrows off, move classification off, "show threats" off while searching.
- Only look at swings of **2+ points** that changed the likely result. Guess before revealing. Stop at a one-sentence lesson; skip ideas I can't explain within about 60 seconds.
- Ignore Accuracy %, Game Rating, inaccuracies, and small differences between engine lines (within about 0.5).
- Mark each moment ✓ (I found it myself) or ✗ (engine-only). The ✓ count is a progress signal.
- No paid membership needed. Lichess "Learn from your mistakes" is a free backup.

**Tracking**

- Tag every mistake with one of seven error tags: H, M, T, K, C, O, E (see `templates/tag-key.md`).
- Weekly Sunday page: tally tags, pick one rule and one drill for next week.
- Monthly: take the last 10 losses, find the deciding mistake in each, sort by tag, and weight study time toward the leading category.

**Maia**

- Stockfish stays the main engine for "was this a blunder and what was better". The version doesn't matter at 700.
- Maia (maiachess.com) is a weekly add-on, about 30 minutes: analyze one game, replay its key positions, one round of opening drills.
- Each notebook moment gets a Maia class: N (next level), L (later), X (hard), R (random lapse), using the crossover method in `docs/02-maia-mistake-classification.md`.
- Mostly R tags in a week → the fix is process (blunder check, clock use). Mostly N tags → the fix is pattern study.
- Play Maia on maiachess.com at a chosen level, *not* the old Lichess bots (maia1/5/9), which play far above their labels. Pick the level by win rate (about 40–50%), not the number.
- Rated 15+10 games against people remain the main practice. Bot games are reviewed the same way but kept out of the weekly tally.

## Things I explicitly set aside

- A per-move tactical pattern checklist based on a GM Igor Smirnov video. The video transcript couldn't be retrieved, so this was dropped.
- Opening theory beyond the first few moves.
- Paid Chess.com tiers.
