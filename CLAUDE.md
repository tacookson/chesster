# CLAUDE.md

Context for a coding agent working in this repo.

## What this repo is for

Tools to help me analyze my own chess games as a 773–816 Chess.com rapid (15+10) player who reviews 5–7 games a week in 10–20 minutes each and keeps notes in a paper notebook.

## Read first

1. `PROJECT_BRIEF.md` — goals, principles, candidate features, open questions.
2. `docs/00-goals-and-context.md` — profile and every decision made so far.
3. `docs/01-review-process.md` — the review method the tooling must support.
4. `docs/02-maia-mistake-classification.md` — the N / L / X / R crossover method.
5. `docs/03-maia-guide.md` and `docs/04-research-notes.md` — background, thresholds and sources.

## Non-negotiables

- Don't show engine answers before I've done my own review. Support the order: hot notes → own review → engine check → one lesson. Output follows that order too: header for hot notes first, PGN for my own review next, engine flags last and folded.
- Surface only big swings (15+ Win% points; see `docs/06-build-plan.md` "Rules to confirm"). A swing in a game I was already losing, or was still winning after, is still listed but says it didn't change the likely result. Hide inaccuracies and Accuracy %.
- Max 3 moments and 1 lesson per game *in the notebook*. chesster lists every flagged swing; I pick which ones to go deep on.
- Engine output gives facts (best move, eval change, safe-move count), never a judgement about why I went wrong. Cause is mine to tag.
- Error tags are fixed: H, M, T, K, C, O, E. Maia classes are fixed: N, L, X, R. Engine marks: ✓ / ✗.
- No paid services assumed.

## Conventions to watch

- Evaluation sign differs by source (Chess.com: White's view; maiachess.com: side to move). Normalize.
- Maia ratings are on the Lichess scale; my Chess.com rapid is 773–816. The Lichess equivalent of ≈ 1000–1200 is based on ~700; needs re-deriving (Q5).
- Facts in `docs/` were researched in October 2026 and may have changed (Chess.com menus, Maia site features, model versions). Verify before depending on them.
- Open questions about the repo's shape are listed at the end of `PROJECT_BRIEF.md`. Ask me before deciding them.
- Commits carry no Claude attribution: no `Co-Authored-By: Claude` or `Claude-Session:` lines.
