# Research Notes

Findings, thresholds and caveats behind the review system, in paraphrase. Useful when the tooling needs a number or a rule with a source behind it.

## What decides games at ~700

- **Safety dominates.** GM Noël Studer's beginner material says players below about 1200 mostly lose by hanging pieces and missing basic tactics, and don't need opening theory yet ([Next Level Chess](https://nextlevelchess.com/beginner-chess-mastery/)).
- **"Chess is 99% tactics"** is usually attributed to Richard Teichmann. Chess historian Edward Winter traces it to a 1930 book by E. Voellmy, where Teichmann is described as exaggerating slightly.
- **Hope Chess vs Real Chess.** Dan Heisman's terms: Hope Chess is moving without checking whether the opponent's checks, captures and threats can be met; Real Chess is checking every candidate for safety ([Heisman](https://www.danheisman.com/definitions.html)).
- **Clock.** Heisman's principles include never playing a bad move fast and using nearly all your time ([Heisman](https://www.danheisman.com/thought-process-principles.html)).

## Review method

- **3×3 method.** Studer's November 2025 video describes picking three moments and asking three "why" questions about each. The exact question wording comes secondhand from a player who used it for a month ([MattPlaysChess](https://mattplayschess.com/the-game-review-habit-that-finally-stuck/)), who added a "Next time I will…" step, reported about 10 minutes per review, and found speed was his biggest source of blunders.
- **"3 good / 3 bad / 3 lessons"** has no authoritative source that could be found.
- **Engine last.** WGM Dina Belenkaya advises analyzing without an engine first, then using the engine like a sparring partner, prioritizing blunders, then major mistakes, then recurring patterns, missed chances and finally openings ([Chess.com](https://www.chess.com/article/view/how-to-analyze-your-chess-games)). She also recommends finding the *first* mistake in a loss, not the last.
- **Monthly loss audit.** Studer suggests taking recent losses, finding the mistake that actually decided each, categorizing them, and weighting study time by category ([Next Level Chess](https://nextlevelchess.com/most-effective-chess-training/)).

## Engine thresholds

- **±2 filter.** Studer's One-Third Rule article treats swings under about 2 pawns as negligible for beginners ([Next Level Chess](https://nextlevelchess.com/the-one-third-rule/)). Written with blitz in mind.
- **Winning chances, not raw points.** Lichess converts evaluations to winning chances with a curve fitted on its own games. Its code labels a drop of 0.1 / 0.2 / 0.3 in winning chances on a −1 to +1 scale as inaccuracy / mistake / blunder, which is **5 / 10 / 15 Win% points**. Forum threads quoting "10 / 20 / 30 percentage points" misread the scale. Roughly: +1 ≈ 60% winning chances, +4 ≈ 83%. This is why +9 → +6 barely matters while +1 → −2 does. Corrected Oct 25, 2026 against lila `Advice.scala`: see `docs/07-mistake-classification-research.md`.
- **Practical rule used here:** look at Blunder/Miss labels or swings of 2+ points that happened while the game was roughly balanced, or that threw away a win.

## Chess.com facts (as of October 2026)

- Free members get one full Game Review per day; reopening an existing review doesn't count against the limit ([Chess.com help](https://support.chess.com/en/articles/8584089-how-does-game-review-work)).
- Analysis board settings: Engine tab (depth, engine, number of lines), Interface tab (suggestion arrows, move classification, threats). Deep/Maximum strength and Cloud Analysis are Diamond-only ([Chess.com help](https://support.chess.com/en/articles/8583757-how-do-i-use-game-analysis)).
- Chess.com says Accuracy isn't a measure of overall playing strength, and the per-game Game Rating can be far from your real rating.
- Chess.com evaluations are shown from White's perspective.
- Membership prices could not be confirmed from an official page.

## Lichess facts

- "Learn from your mistakes" is free and unlimited, and works on imported games; it asks you to find a better move before showing one ([Lichess blog](https://lichess.org/@/lichess/blog/learn-from-your-mistakes/WFvLpiQA)).
- Lichess founder Thibault has said server analysis is capped at about 40 games a day and 200 a week; browser analysis is unlimited.
- Import a Chess.com game: Share → copy PGN → lichess.org/paste → request computer analysis.

## Rating conversion

- Lichess ratings run roughly 200–400 above Chess.com at club level, with a wider gap at beginner level ([Chessiro](https://chessiro.com/chess-rating-converter)). A ChessDojo-based converter suggests ~700 Chess.com rapid sits around 950 Lichess classical. Working assumption: ~1000–1200 on Maia's Lichess blitz scale. Treat as approximate.

## Open questions

- Which Maia model maiachess.com actually runs today (Maia-3 per the announcement; a July 2026 review saw Maia-2).
- Whether the maiachess.com play mode samples moves or always plays Maia's top move.
- Whether Maia puzzles can be filtered by theme.
- How maiachess.com's endgame drills are graded.
