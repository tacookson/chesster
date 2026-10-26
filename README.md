# chesster

A repo that helps me analyze my own chess games. It captures my goals, the review method I've settled on, how I use engines (Stockfish via Chess.com, and Maia), and the research behind those choices.

The knowledge base below was compiled October 25, 2026, from a research and planning conversation. No tooling exists yet; see `PROJECT_BRIEF.md` for candidate features and open questions.

## Using chesster

One-time setup on macOS:

```sh
brew install stockfish
uv sync
```

From the repo root:

```sh
uv run chesster                 # fetch new rapid games, flag big swings, write games/YYYY-MM/*.md
uv run chesster --game <url>    # re-process one game (overwrites its file)
uv run chesster --no-engine     # archive only, skip Stockfish
uv run --group dev pytest       # run tests
```

Settings (username, thresholds, engine depth, Stockfish path) live in `chesster.toml`. Each game file has the header, flagged moves with their type, the engine answer folded under each move, and the PGN to paste into maiachess.com. Open it in VS Code's Markdown preview (Cmd+Shift+V) so the answers stay folded.

## Who this is for

- **Me:** a reference for the review routine and notebook format.
- **Anyone (or any coding agent) building the repo:** the requirements and domain knowledge the tooling should follow. Start with `CLAUDE.md` and `PROJECT_BRIEF.md`.

## Contents

| File | What it holds |
| --- | --- |
| `CLAUDE.md` | Short orientation for a coding agent working in the repo |
| `PROJECT_BRIEF.md` | Goals for the repo, requirements derived from the method, candidate features, open questions |
| `docs/00-goals-and-context.md` | My player profile, constraints and every decision made so far |
| `docs/01-review-process.md` | The 15-minute game review system, v2 (process with chesster, selection and tag rules, question bank, notebook template) |
| `docs/02-maia-mistake-classification.md` | The crossover method: sorting each mistake into N / L / X / R using Maia |
| `docs/03-maia-guide.md` | Deep dive on Maia: models, features, how people use it, limitations, my weekly Maia plan |
| `docs/04-research-notes.md` | Key research findings, thresholds and caveats, with sources |
| `docs/05-design-survey.md` | Survey of the current design, its inputs, and gaps to close before building tooling |
| `docs/06-build-plan.md` | Build plan: slices, Maia spike, file format, and rule defaults |
| `docs/07-mistake-classification-research.md` | Research: severity, difficulty and cause frameworks for classifying mistakes, and what they mean for chesster |
| `docs/assets/chesscom-analysis-board-example.png` | Screenshot of the Chess.com Analysis board used as the worked example |
| `templates/game-entry.md` | Per-game notebook entry |
| `templates/weekly-page.md` | Weekly tally page |
| `templates/tag-key.md` | Error tags and Maia classes |

## Source documents

These files were exported from two living docs, which may have been edited since:

- Chess Game Review System (v1): https://claude.ai/artifact/66XYr4VUEGUvFqBynq6Yyr
- Chess Game Review Framework v2: https://claude.ai/artifact/NLpPsJqsApS2tg4ULEr56r (`docs/01` and `templates/` were updated to match on October 26, 2026)
- Maia Chess Deep Dive: https://claude.ai/artifact/XKM7tGAEMPbQGVRfzAnmBf
