# Design Survey

A survey of the repo's existing design, its inputs, and the gaps to close before building tooling. Written October 25, 2026, after the knowledge base was added.

## What the "design" is

| Layer | Where | State |
| --- | --- | --- |
| Review method (human process) | `docs/01`, `docs/02`, `templates/` | Detailed and sourced: steps, timings, caps, tags, drills |
| Tooling principles | `PROJECT_BRIEF.md` (7 principles), `CLAUDE.md` (non-negotiables) | Clear limits on what the tool must and mustn't do |
| Tooling design | `PROJECT_BRIEF.md` (candidate features, open questions) | None yet: 8 feature ideas, 5 open shape questions, no workflow, data model or architecture |

The process is well specified and the tooling is constrained, but there is no tooling design yet.

## Inputs

| Input | Source | Status |
| --- | --- | --- |
| Game PGNs with per-move clocks | Chess.com public API (monthly archives) | Unverified: endpoint, rate limits, whether archive PGNs carry `%clk` |
| Objective evaluation | Stockfish (local or web) | Low risk; any modern build works at this level |
| Human move probabilities | Maia-3 (Hugging Face weights) or maiachess.com | Unverified locally: licence, CPU speed, input format, full legal-move probabilities per rating |
| Notebook data (tags, ✓/✗, lessons, Maia classes) | Paper | No path into the repo (gap 1) |
| Thresholds and rules | `docs/04` | Partly second-hand; some conflict (gap 2) |
| Player constants | `docs/00` | 700 Chess.com ≈ 1000–1200 Lichess; approximate (gap 6) |

## Gaps

### A. Conflicts between principles (need a decision)

1. **Resolved (Oct 25):** the notebook holds all insights and tracking; the repo finds engine mistakes/blunders and archives games, and stores no notebook data. Weekly/monthly summary features drop out. Original framing: **Paper-first vs pattern tracking.** Principle 6 keeps paper primary; principle 4 says the value is in weekly tallies and trends. Any summary feature (weekly tally, ✓/✗ ratio, N vs R counts, monthly loss audit) needs notebook data in the repo, and nothing says how it gets there: re-type, quick capture (e.g. one line per moment, `14 H ✓ R`), photograph, or don't track in the repo. This is open question #2 and the decision most others depend on.

2. **"Swing" has three definitions that disagree.** "2+ points", "changed the likely result" and "Lichess winning-chance drops" are treated as one rule. Using the Lichess win-percentage formula (constant 0.00368208):

   | Change | Drop in winning chances | Lichess label |
   | --- | --- | --- |
   | 0 → −2 | 17.6 points | mistake, not blunder |
   | +1 → −2 | 26.7 points | mistake, not blunder |
   | +9 → +6 | 6.4 points | nothing |

   A Lichess-style blunder (30-point drop) from a level position needs about −3.3. A swing finder needs one rule, e.g. "a drop of at least N winning-chance points from my point of view". The rule must also cover **missed chances** (opponent errors not punished), which Step 3 counts but the swing-finder idea doesn't mention.

3. **Maia class scope.** Principle 5 says classify *each* moment N/L/X/R; the templates and weekly plan say only the weekly Maia game, because the manual crossover costs 2–3 minutes per moment. Automation removes that cost, so the scope needs deciding again.

4. **Enforcing "engine last".** On paper the reveal order is self-discipline. With tooling, something must stop engine output appearing before the own review. Nothing specifies how (two-phase command, recording moments first, trust). Recording moments first means typing, which conflicts with paper-first (gap 1).

### B. Rules too loose to automate

5. **Crossover classification** (`docs/02`).
   - R is defined by absolute probability ("players at my rating rarely play my move"); N, L and X by crossover position. A move can qualify for both R and N.
   - "Rare" has no number, and it defines both R and X.
   - L covers crossovers up to +800 (≈1900); X is "rare near 2000+". A crossover at 2000–2600 is neither.
   - No rule for multiple crossings or a crossover below my level.
   - On maiachess.com my move may not appear in the graph's candidate moves.

6. **"My level" in Maia.** The cited converter maps 700 Chess.com rapid to ~950 Lichess *classical*; Maia models Lichess *blitz*. The 1000–1200 range (default 1100) isn't backed by its cited source, and a 100-point shift moves N/L boundaries. Recalibration is open question #5.

7. **Three notions of "the critical moment."** First material loss (in losses), "the deciding mistake" (monthly audit), and biggest drop (swing finder) can be three different moves. Tooling also needs a ranking rule when there are more than 3 swings, and material tracking (not just evals) to find the first material loss.

8. **Tag precedence.** One tag per moment, but no precedence: a piece hung in 4 seconds is H or C. Without a rule, tallies drift with mood. If the clock check auto-flags C, decide who wins when tool and human disagree.

9. **Small undefined rules.**
   - Normalize evaluations to *my* point of view, not White's (I play both colours).
   - Time spent per move = previous clock − current clock + 10 s increment.
   - Week boundaries in America/Toronto.
   - Game selection: "most interesting" game for the Maia session; the full vs lite line ("clearly winning but didn't win").

### C. Missing entirely

10. **Which manual steps the tool replaces.** The method finds swings on the Chess.com Analysis board. If the tool finds them, does that part of Step 3 go away, or happen twice? Features aren't mapped to the minutes they remove from the 15-minute routine, so the tool risks adding steps.

11. **Success criteria.** Goal #3 is consistency, with no measure: reviews done vs games played, minutes per review, ✓ ratio over time. The choice affects what data is stored.

12. **Source of truth.** The docs were exported from two living artifacts that may have been edited since. Decide whether this repo is now canonical.

13. **Integration checks still to do** (local Maia-3 deferred by the companion decision, Oct 25).
    - **Verified Oct 25:** `https://api.chess.com/pub/player/{username}/games/archives` lists monthly archives; `.../games/{YYYY}/{MM}` returns games as JSON without auth. Each game has `url`, `pgn`, `time_class`, `rated`, `white`/`black`, `eco`, `end_time` and `accuracies` (to hide). The PGN carries `[%clk h:mm:ss.s]` after every move. There is no documented single-game endpoint, so a game is found within its month's archive.
    - Original list: (validate before building): Chess.com archive endpoint, rate limits and `%clk` presence; local Maia-3 inference with a rating sweep; where the tooling runs (machine, OS, Python).

## Evidence: Stockfish flags on my October 2026 games

Stockfish 16, depth 16, flag = my winning chances dropped 20+ points (Lichess formula), first 5 moves skipped. 16 rated 15+10 games, 31 flags (about 2 per game):

| Kind | Count |
| --- | --- |
| Missed free material (best move wins 2+ within 3 moves) | 10 |
| Lost material within 2 moves | 9 |
| Missed mate in 1–2 | 5 |
| Missed long mate (mate in 8) | 1 |
| Other: no quick material change | 7 |

- About three-quarters of flags are simple safety errors; the rest are where "is this human-findable?" matters.
- A depth-4 search also saw all 31 drops, so shallow search depth is not a usable proxy for human difficulty.
- One missed idea was flagged on three consecutive moves; such runs should merge into one moment.
- Categories are crude material counts over one month of games.

## Dependencies

Gap 1 decides what can be tracked, which bounds gaps 3, 4 and 11. Gaps 2, 5, 7 and 8 are rule-tightening that needs no code. Gap 13 is validation work that can run in parallel.
