# chesster

A repo that helps me analyze my own chess games. It captures my goals, the review method I've settled on, how I use engines (Stockfish via Chess.com, and Maia), and the research behind those choices.

The knowledge base below was compiled October 25, 2026, from a research and planning conversation. No tooling exists yet; see `PROJECT_BRIEF.md` for candidate features and open questions.

## Who this is for

- **Me:** a reference for the review routine and notebook format.
- **Anyone (or any coding agent) building the repo:** the requirements and domain knowledge the tooling should follow. Start with `CLAUDE.md` and `PROJECT_BRIEF.md`.

## Contents

| File | What it holds |
| --- | --- |
| `CLAUDE.md` | Short orientation for a coding agent working in the repo |
| `PROJECT_BRIEF.md` | Goals for the repo, requirements derived from the method, candidate features, open questions |
| `docs/00-goals-and-context.md` | My player profile, constraints and every decision made so far |
| `docs/01-review-process.md` | The full 15-minute game review system (process, engine routine, question bank, notebook template) |
| `docs/02-maia-mistake-classification.md` | The crossover method: sorting each mistake into N / L / X / R using Maia |
| `docs/03-maia-guide.md` | Deep dive on Maia: models, features, how people use it, limitations, my weekly Maia plan |
| `docs/04-research-notes.md` | Key research findings, thresholds and caveats, with sources |
| `docs/assets/chesscom-analysis-board-example.png` | Screenshot of the Chess.com Analysis board used as the worked example |
| `templates/game-entry.md` | Per-game notebook entry |
| `templates/weekly-page.md` | Weekly tally page |
| `templates/tag-key.md` | Error tags and Maia classes |

## Source documents

These files were exported from two living docs, which may have been edited since:

- Chess Game Review System: https://claude.ai/artifact/66XYr4VUEGUvFqBynq6Yyr
- Maia Chess Deep Dive: https://claude.ai/artifact/XKM7tGAEMPbQGVRfzAnmBf
