# Classifying Mistakes with Maia: the Crossover Method

Maia can sort each of my mistakes into one of four classes, and each class calls for a different fix. This is the main reason to use Maia alongside Stockfish.

## The idea

Maia predicts what a human at a given rating would play. Its **Moves by Rating** graph shows how likely each candidate move is at every rating from 600 to 2600.

Maia's researchers found that players at each rating make some mistakes predictably. In their published example, Maia set to 1100–1400 predicted a tempting but wrong move (the one actually played), while Maia set to 1500+ predicted the correct move. The rating where the right move overtakes the wrong one is the **crossover**. Below it, most players make my mistake; above it, most find the right move.

## The method (2–3 minutes per moment)

1. Paste the game's PGN into maiachess.com analysis. Set the rating to my Lichess-equivalent, about 1000–1200 (Maia uses the Lichess scale).
2. Go to the position *before* one of my notebook moments.
3. In Moves by Rating, find two lines: **my move** and **Stockfish's best move**.
4. Note the rating where the best move's line rises above mine, then classify:

| Class | What the graph shows | What to do |
| --- | --- | --- |
| **N – Next level** | The lines cross within ~300 points above my level | Priority lesson. Replay the position and drill that puzzle theme |
| **L – Later** | The lines cross 300–800 points above my level | Note it, don't drill it yet |
| **X – Hard** | The best move stays rare even near 2000+ | "Engine idea – skip." No guilt |
| **R – Random lapse** | Even players at *my* rating rarely play my move | A habit problem, not a knowledge gap |

## Why N and R matter most

- **R moves:** players at my level usually find the right move and I didn't. I skipped a check, rushed, or tilted. The fix is process: the blunder check, slowing down on captures, clock management. These usually line up with the H, M and C error tags.
- **N moves:** mistakes most people at my level make and the next tier has learned not to. These are the real study list: puzzles on that theme, and replaying that exact position against Maia.

The Maia team frames the same idea as telling predictable blunders apart from random ones. Their original research found Maia predicts the exact blunder a human made about 25% of the time.

## Other signals worth a glance

- **"Tempting blunder" hint:** the panel flags positions with a trap that catches many people at my level. Learn to recognize that kind of position.
- **Blunder meter:** how likely someone at my rating is to go wrong here. High means the position itself was hard, so a mistake there hurts less than one in a quiet position.

## Weekly interpretation

Add an N/L/X/R letter next to each moment's error tag. On the weekly page, count N and R:

- **Mostly R:** process is the bottleneck. Tighten the blunder check and use more clock time.
- **Mostly N:** careful play, missing patterns. Weight next week toward puzzles and replays of those positions.

## Caveats

- **One position is noisy.** Maia's percentages are population averages, and its top guess is wrong roughly 4 times in 10. Trust patterns across weeks.
- **Skip the first ~5 moves.** Opening moves are mostly memorized, so the graph says less about them.
- **Rating scale.** Maia uses Lichess ratings (and was trained on Lichess blitz games). The thresholds above are relative to my Lichess-equivalent, not my Chess.com number.
- **The screen may change.** maiachess.com is in beta; some features (like the Move Map) have been hard to locate. Each page has a "?" walkthrough.
- The 300 / 800 point boundaries are my own working thresholds, not values from Maia's research.

## Prior art

An analyst at Chess Engine Lab proposed the same idea with the original Maia models: label an error by the highest-rated Maia model that would still make it.

## Sources

- [Introducing Maia: a Human-Like Chess Engine (Maia blog)](https://www.maiachess.com/blog/maia-v1)
- [Introducing Maia (Lichess blog)](https://lichess.org/blog/X9PUixUAANCqFRSh/introducing-maia-a-human-like-neural-network-chess-engine)
- [Maia-2 paper (arXiv)](https://arxiv.org/abs/2409.20553)
- [Introducing Maia Platform v1 (Maia blog)](https://www.maiachess.com/blog/platform-v1)
- [Maia Chess (maiachess.com) – Testbericht (Freibauer Mörlenbach)](https://www.freibauer80.de/maia-chess-maiachess-com-testbericht/comment-page-1/)
- [Testing Maia's puzzle performance (Chess Engine Lab)](https://chessenginelab.substack.com/p/testing-maias-puzzle-performance)
