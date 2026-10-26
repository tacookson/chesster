# Maia Chess Guide

Maia is a free University of Toronto research engine that predicts the move a human at a given rating would play, not the best move. For a ~700 Chess.com rapid player, its most valuable feature is analysis of my own games; drills and practice games come next.

- **What it is:** a neural network trained on millions of Lichess games, able to model any rating from 600 to 2600.
- **Where to use it:** maiachess.com (sign in with Lichess). The three Lichess bots run the original 2020 models and play well above their labels.
- **Best use for me:** checking whether each mistake is one players slightly above me avoid (learn it now) or one even strong players make (skip it). See `02-maia-mistake-classification.md`.
- **Main caveats:** Lichess rating scale, still in beta, and a dense analysis screen that can eat time.

Researched October 24, 2026.

## Models and history

Maia has gone through three generations since 2020; the current one, Maia-3, predicts the human move about 57% of the time across ratings 600–2600.

| When | Release | What changed |
| --- | --- | --- |
| May 2026 | [Maia-3 (Chessformer, ICLR 2026)](https://arxiv.org/abs/2605.19091) | New transformer design; 57.1% move-matching accuracy with under a quarter of the parameters of the previous best. Announced as powering maiachess.com ([Lichess blog](https://lichess.org/@/ashtonanderson/blog/introducing-maia-3-free-and-open-source/vCPPRtX3)). Open models on Hugging Face (UofTCSSLab Maia3 collection) and GitHub (CSSLab/maia3) |
| Jul 2025 | [Maia4All](https://arxiv.org/abs/2507.21488) (research) | Models an individual player's style from about 20 games, down from 5,000; accuracy for that player rose from 51.4% to 53.2% |
| Jul 2025 | [Platform v1](https://www.maiachess.com/blog/platform-v1) | Site rebuilt on Maia-2: new analysis page, opening drills, training puzzles |
| Oct 2024 | [Maia-2 (NeurIPS 2024)](https://arxiv.org/abs/2409.20553) and [platform v0 beta](https://www.maiachess.com/blog/platform-v0) | One model for every rating instead of nine; predictions change smoothly as rating rises |
| Aug 2020 | [Maia-1 (KDD 2020)](https://www.maiachess.com/blog/maia-v1) | Nine separate models, 1100–1900; three became the Lichess bots maia1, maia5 and maia9 |

**Why the generations matter:**

- **Maia-1** cannot model a 700-level player; its lowest model is 1100.
- **Maia-2 and Maia-3** take rating as an input, so the site can show how a move's popularity changes from 600 to 2600.
- **Smoothness:** Maia-2's paper reports its predictions move consistently with skill for 27% of sampled positions, versus 1% for Maia-1. That consistency is what makes the Moves by Rating graph readable.
- **Model on the site:** the project lead says Maia-3 powers maiachess.com, but a [July 2026 review](https://www.freibauer80.de/maia-chess-maiachess-com-testbericht/comment-page-1/) still described Maia-2. The features work the same either way.

## Stockfish on maiachess.com

- The site runs Stockfish in the browser as WebAssembly (the Lichess web build, `lila-stockfish-web`, per the site's open-source frontend). The exact Stockfish version wasn't stated anywhere I could find.
- For reference, the newest Stockfish release is version 19 (September 5, 2026).
- At 700 the Stockfish version doesn't matter; any modern build at depth 18–20 finds every blunder that matters.
- **Evaluation sign:** maiachess.com shows scores from the side to move (+2 = good for whoever is moving). Chess.com shows scores from White's side.

## Play

You can play Maia on maiachess.com at a chosen rating, or start it from any position you paste in. Players consistently report it plays stronger than its label, so pick a level by results.

**What you can do**

- **Pick a rating:** 600–2600 on the Lichess scale.
- **Start from any position:** paste a FEN and Maia plays on from there ([v0 announcement](https://www.maiachess.com/blog/platform-v0)).
- **Lichess bots:** @maia1, @maia5 and @maia9 still run the 2020 models (1100, 1500, 1900 labels).

**What players report**

- **Stronger than labeled:** after the Maia-3 release, one player found Maia 1500 several hundred points stronger than its label in a 3+0 game ([Lichess forum](https://lichess.org/forum/community-blog-discussions/ublog-vCPPRtX3)). Another said the downloadable model is beatable at 2600 but the website version beat them, and asked whether the site plays Maia's top move instead of sampling. No answer appears in that thread.
- **The old bots too:** in August 2025, maia1 (labeled 1100) was rated about 1495 in Lichess rapid ([ChessUp forum](https://community.playchessup.com/t/humanlike-bots-maia-lc0-hiarcs-etc/3807)).
- **Why:** Maia plays the average move of many players at a level, so individuals' one-off blunders cancel out ([Lichess blog](https://lichess.org/blog/X9PUixUAANCqFRSh/introducing-maia-a-human-like-neural-network-chess-engine)).
- **Old complaints (2020 bots):** knew too much opening theory for their level ([Chess.com forum](https://www.chess.com/forum/view/general/maia-chess)); rarely lost on time the way weak humans do ([TalkChess](https://talkchess.com/viewtopic.php?t=76002&start=30)).
- **A bug:** on Firefox, clicks sometimes land on the neighboring square; zooming in and back out fixes it.

**Choosing a level:** start near 900–1000 on the site, then adjust until winning roughly 40–50% of games.

**Why Maia beats a weakened Stockfish for practice:** a weakened Stockfish plays mostly perfect moves plus random blunders no human would make. Maia leaves pieces hanging and misses threats the way real opponents do, so punishing those mistakes carries over to rated games.

## Analysis

The analysis page shows every position through two lenses: what Stockfish says is best, and what humans at a chosen rating actually play.

**Getting a game in**

- **Lichess games:** load directly after signing in with Lichess.
- **Chess.com games:** paste the PGN (or a FEN for one position). Saved in the browser's local storage, so it stays on that device.
- **Variations:** try your own moves from any position, with live evaluation.
- **Export:** games and positions export as PGN or FEN.

**What's on the screen**

| Component | What it shows | How to use it |
| --- | --- | --- |
| Two evaluation bars | Win probability (%) and Stockfish's score in pawns | Win % is easier to read at a glance |
| Human moves vs engine moves | Maia's likely moves at the chosen rating, with percentages, beside Stockfish's top moves | Compare what people play with what's best |
| Text hint | A short plain-language note, such as flagging a "tempting blunder" | Read it before the numbers |
| Moves by Rating graph | How likely each candidate move is from 600 to 2600 | Find the crossover (see `02-maia-mistake-classification.md`) |
| Blunder meter | How often a player at the chosen rating makes good, okay and bad moves here | High = a genuinely hard position |
| Move Map | A scatter of moves by popularity and quality | Spot popular moves that are actually bad |
| Accuracy bar | How closely the game matched Maia at a rating, plus a blunder/mistake/best breakdown | A rough summary, not a score to chase |
| Options and Export tabs | Engine choice, analyze entire game, "Learn from mistakes" | Run whole-game analysis before stepping through |

The July 2026 reviewer couldn't find the Move Map described in the 2025 announcement. Each page has a walkthrough behind the "?" button.

## Puzzles

Rated tactics problems that, after you solve or miss them, show how players at each rating handled the position.

- The site says Maia curates puzzles based on how millions of players improve, with per-rating data for each one.
- After each puzzle, the full analysis toolset is available and the position can be played out.
- Puzzle history tracks rating changes and past puzzles.
- **Unconfirmed:** whether Maia puzzles can be filtered by theme. For theme-targeted drilling, Chess.com's Custom Puzzles let you pick themes ([Chess.com help](https://support.chess.com/en/articles/8708983-how-are-the-next-puzzles-chosen-for-me-when-i-am-training)).
- **Best use:** after a missed puzzle, check Moves by Rating. If most players near my level also miss it, it's a next-level lesson; if they mostly find it, learn it now.

## Drills

Drills drop you into positions from openings (and now endgames) you choose and have you play them out against Maia at a set level, then grade your decisions.

**Opening drills** ([v1 announcement](https://www.maiachess.com/blog/platform-v1))

1. Pick a set of openings; set line length, difficulty and number of drills.
2. Each drill starts after the opening; you play into the middlegame against the chosen Maia level.
3. Analysis tools are available during the drill.
4. Afterwards: feedback on critical decisions, an estimate of what rating you played like, Stockfish's evaluation over time, and move-by-move quality.
5. A summary across all openings when the set is done.

**Endgame drills:** listed in the Maia-3 announcement alongside openings (pick endgames, pick a skill level, go). I couldn't find details on grading.

**How people use them**

- A player on the Maia-3 thread said they were enjoying the opening drills.
- An Android Maia app developer declined to build opening practice, citing maiachess.com's drills ([GitHub](https://github.com/Dash1971/maia-chess-android-preview/issues/28)).
- For winning endgames, one coach recommends practicing against a tablebase, which defends perfectly ([64 Squares](https://64squares.substack.com/p/engine-sparring)). A hobby project combines both: Maia plays human-like moves but uses a tablebase to punish any slip ([maia-local](https://github.com/gr-g/maia-local)).

**Best use:** drill only my main opening as White and main defence as Black, in short sessions. Treat the "played like" rating as a rough trend.

## Other features

| Feature | What it does | Worth it at 700? |
| --- | --- | --- |
| Hand & Brain | Team variant: the Brain names a piece type, the Hand picks the move; you can team with Maia | Fun, not training |
| Bot-or-Not | A chess Turing test: guess which player is the bot | Fun only |
| Broadcasts | Follow tournaments and any Lichess game live, with Maia beside Stockfish | Occasionally |
| Leaderboards and profiles | Rankings for puzzles and Bot-or-Not; profiles link to Lichess | No |
| Famous games | Classic games ready to analyze | Rarely |

**Research not available as site features:** Maia4All (a Maia that plays like a specific person from ~20 games) and skill-compatible partner bots.

## How people use Maia

1. **Sparring partner.** Felt more human than Chess.com's bots to one beginner ([Chess.com forum](https://chess.com/forum/view/general/maia-chess)). Available on Chessnut Evo smart boards; ChessUp lets players challenge the Lichess Maia bots, though the company says Maia gets the style right but the strength wrong.
2. **A human view beside Stockfish.** Project lead Ashton Anderson has said Maia can show which mistakes are typical at each level, and so which to work on now versus later. Apps building on this: an offline Android app with Maia-3 at 600–2600 and two Maia ratings side by side in review ([GitHub](https://github.com/Dash1971/maia-chess-android)); the iOS app Gambito pairing Stockfish 18 with Maia; Lucas Chess shipping the original Maia engines.
3. **Rating difficulty.** Labelling an error by the highest-rated Maia model that would still make it ([Chess Engine Lab](https://chessenginelab.substack.com/p/testing-maias-puzzle-performance)); research estimating puzzle difficulty with a fine-tuned Maia-2; estimating practical chances where Stockfish says "equal" ([Chess Engine Lab](https://chessenginelab.substack.com/p/expected-scores-for-chess-positions)).
4. **Developer projects.** A service serving Maia-3 over an API; a write-up of running Maia-2 in the browser ([DEV](https://dev.to/mrdimosthenis/why-stockfish-isnt-enough-running-maia-2-in-the-browser-for-human-chess-analysis-53no)), which notes puzzle and playing ratings sit on different scales.

## Limitations

| Limitation | What it means |
| --- | --- |
| Plays above its label | Pick a level by win rate, not the number |
| Lichess rating scale | Lichess runs roughly 200–400 above Chess.com at club level, more for beginners ([Chessiro](https://chessiro.com/chess-rating-converter)). Treat 700 Chess.com rapid as ~1000–1200 on Maia |
| Trained on Lichess blitz | Maia-3 models Lichess blitz ratings from games Jan 2023 – Jul 2025. My 15+10 games give more thinking time, so treat it as a close guide |
| Predictions are averages | At 57% move-matching, the top guess is wrong about 4 times in 10. Trust patterns across weeks |
| Opening moves | Mostly memorized; skip the first ~5 moves when reading graphs |
| Beta software | Features move or get renamed |
| Lichess sign-in | Needed for the analysis page; games can come from anywhere |
| Browser-only storage | Pasted games stay on that device's browser |
| Evaluation sign | Side to move, unlike Chess.com |
| Dense screen | Cap at 2–3 minutes per moment |

## My weekly Maia plan

One 30-minute session a week on top of daily Chess.com reviews. Rated 15+10 games against people stay the main practice.

**One-time setup (10 min)**

- Sign in to maiachess.com with a Lichess account (free).
- Set the analysis rating to 1100 (decided October 26, 2026).
- Run each page's "?" walkthrough once.

**Weekly session (30 min)**

1. **Analyze one game (10 min).** Paste the PGN of the most interesting reviewed game. Classify each notebook moment N / L / X / R.
2. **Replay key positions (10 min).** The position before each N or R moment, plus any clearly winning position. Play each out against Maia 2–3 times at a level I beat about half the time.
3. **One round of opening drills (10 min).** Alternate weeks: main opening as White, main defence as Black.

**Optional:** a warm-up game against Maia before a rated session (kept out of the tally); after a missed puzzle, check Moves by Rating.

**Skip for now:** Hand & Brain, Bot-or-Not, leaderboards, the old Lichess Maia bots.

## Sources

**Maia project**

- [Maia Chess (maiachess.com)](https://www.maiachess.com/)
- [Introducing Maia: a Human-Like Chess Engine (2020)](https://www.maiachess.com/blog/maia-v1)
- [Beta Testing Maia Chess v0 (2024)](https://www.maiachess.com/blog/platform-v0)
- [Introducing Maia Platform v1 (2025)](https://www.maiachess.com/blog/platform-v1)
- [Introducing Maia-3: free and open source (Lichess blog, 2026)](https://lichess.org/@/ashtonanderson/blog/introducing-maia-3-free-and-open-source/vCPPRtX3)
- [Introducing Maia (Lichess blog, 2020)](https://lichess.org/blog/X9PUixUAANCqFRSh/introducing-maia-a-human-like-neural-network-chess-engine)
- [maia-platform-frontend (GitHub)](https://github.com/CSSLab/maia-platform-frontend)
- [Maia3-79M (Hugging Face)](https://huggingface.co/UofTCSSLab/Maia3-79M)

**Papers**

- [Maia-2 (NeurIPS 2024)](https://arxiv.org/abs/2409.20553)
- [Chessformer / Maia-3 (ICLR 2026)](https://arxiv.org/abs/2605.19091)
- [Learning to Imitate with Less / Maia4All](https://arxiv.org/abs/2507.21488)

**Reviews, forums and user reports**

- [Maia Chess Testbericht (Freibauer Mörlenbach, July 2026)](https://www.freibauer80.de/maia-chess-maiachess-com-testbericht/comment-page-1/)
- [Maia-3 discussion (Lichess forum)](https://lichess.org/forum/community-blog-discussions/ublog-vCPPRtX3)
- [Humanlike Bots thread (ChessUp community)](https://community.playchessup.com/t/humanlike-bots-maia-lc0-hiarcs-etc/3807)
- [Maia Chess thread (Chess.com forum)](https://www.chess.com/forum/view/general/maia-chess)
- [Maia chess thread (TalkChess)](https://talkchess.com/viewtopic.php?t=76002&start=30)
- [Engine sparring (64 Squares)](https://64squares.substack.com/p/engine-sparring)
- [Testing Maia's puzzle performance (Chess Engine Lab)](https://chessenginelab.substack.com/p/testing-maias-puzzle-performance)
- [Expected scores for chess positions (Chess Engine Lab)](https://chessenginelab.substack.com/p/expected-scores-for-chess-positions)

**Third-party apps and other references**

- [maia-chess-android (GitHub)](https://github.com/Dash1971/maia-chess-android)
- [maia-local (GitHub)](https://github.com/gr-g/maia-local)
- [Running Maia 2 in the browser (DEV)](https://dev.to/mrdimosthenis/why-stockfish-isnt-enough-running-maia-2-in-the-browser-for-human-chess-analysis-53no)
- [Stockfish 19 (Stockfish blog)](https://stockfishchess.org/blog/2026/stockfish-19/)
- [Chess Rating Converter (Chessiro)](https://chessiro.com/chess-rating-converter)
