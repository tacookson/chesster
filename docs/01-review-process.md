# Chess Game Review System (v2)

Review every rapid game with one fixed 15-minute routine, then tally mistakes weekly. Built for a ~700–800 Chess.com rapid (15+10) player, 5–7 games a week, notes in a paper notebook. v2 (October 26, 2026) keeps v1's order, caps and tags, but chesster now finds the swings, so the engine step checks its list instead of scrubbing the eval bar.

| Step | When | Min | Look at | Write in the notebook |
| --- | --- | --- | --- | --- |
| 1. Hot notes | Right after the game, before the next one | 2 | Nothing but your memory | Header line 1, HOT lines |
| 2. Own review | Review session; chesster file still closed | 6 | Chess.com game, engine hidden | Up to 3 moment rows, left half |
| 3. chesster check | After Step 2 is written | 5 | chesster's game file + the board | Right half of each row, ✗ rows, CHK line |
| 4. Lesson | Last | 2 | Your rows | NEXT TIME line |

At 700–800, almost every game is decided by safety: hung pieces, missed opponent threats and missed free material. The routine is built to catch those and skip opening theory and strategy.

## What changed from v1

| Area | v1 | v2 | Why |
| --- | --- | --- | --- |
| Finding swings | Tap through the Chess.com Analysis board watching the number | Read chesster's game file: every move that cut my winning chances by 20+ points, already labelled | Saves about 2 minutes and never misses one |
| When the engine appears | Self-discipline | Don't open the game file until my own moments are written | The file's headings name the move and what happened before any fold, so opening it early spoils Step 2 |
| ✓ / ✗ | Did I find this moment myself? | Same, judged against chesster's list | A fixed list makes ✓ objective |
| My moments that weren't swings | Kept | Struck through, counted | Enforces the 2-point rule; the count shows calibration improving |
| Picking 3 when there are more | Not defined | Fixed order (Rules) | Different reviews used to pick differently |
| Tag when a blunder was also fast | H or C, by mood | Tag what I missed on the board; tick a separate <10 s column | Keeps H / M / T honest and still tracks speed |
| Maia classes | Overlapping definitions | One decision order, every case covered | R and N could both apply; crossovers at 2000–2600 had no class |
| Weekly page | Tally + rule + drill | Adds reviewed / played, struck rows, fast moves | Consistency is the main goal |

## What to focus on at ~700

Focus on safety. Below about 1200, coaches agree the biggest problems are hanging pieces and missing basic tactics, not openings or strategy.

- **GM Noël Studer** argues that players under 1200 should stop losing pieces before memorizing opening theory. The lower the rating, the more games are decided by tactics.
- **Dan Heisman** calls the core habit "Real Chess": before every move, check the opponent's possible checks, captures and threats in reply. Moving without checking is what he calls "Hope Chess".
- **Chess.com forum consensus** from players stuck at 600–700 says the same: the climb to ~1200 is mostly about not blundering pieces.

**Ignore for now:**

- Opening theory beyond the first few moves
- Engine "best moves" in quiet positions
- Evaluation changes under about 1–2 points
- Accuracy % and Game Rating
- Any engine idea you can't explain in one sentence

## The process

Step 1 happens right after each game. Steps 2–4 happen when I sit down to review, which can be several games later. At the start of that session, run `uv run chesster` once: it prints only file names, so it gives nothing away. Don't open the files yet.

### Step 1: Hot notes (2 min, right after the game)

No next game until these two lines exist. Once I've seen engine output I can't recover what I was thinking.

1. Write header line 1: game number, date, colour, result. Leave the rest of the header for Step 2.
2. **HOT line 1:** the move where I think the game turned and what happened there.
3. **HOT line 2:** how I felt and used the clock ("rushed after move 14", "tilted", "fine").

### Step 2: Own review, chesster file closed (6 min)

1. Open the game on Chess.com, then the Analysis board with the evaluation bar, engine lines, suggestion arrows and move feedback hidden (see "The Chess.com Analysis board" below).
2. Fill the rest of the header from the game page: opponent and ratings, opening, clock left for both sides.
3. Step through. Stop every time material changes hands, a check appears, or a mate threat appears.
4. Pick up to 3 moments using the selection order in Rules. In a loss, the first material I lost is always one of them.
5. For each, fill the **left half** of a moment row: move number, "I played … because", "Bad because", "Better … because". Write "?" in any column I can't answer.
6. Not sure a moment mattered? Write it anyway. Step 3 will tell me.

Don't tag yet and don't write ✓. Both depend on Step 3. The left-half columns are GM Noël Studer's three "why" questions (why did I choose it, why was it not good, what was better and why), trimmed to fit 700: *up to* three moments and one lesson per game.

### Step 3: chesster check (5 min)

Open the game's file in VS Code's Markdown preview (Cmd+Shift+V): `games/YYYY-MM/<date>-vs-<opponent>-<id>.md`. Each flagged move is a heading with one line saying what happened; the engine's answer is folded underneath. Work through the flags in order:

1. **Match.** Is this move (or one in a merged run, "Moves 15–17") one of my rows? Yes → ✓. No → it's a ✗ moment; add it as a row if it makes the top 3.
2. **Guess before unfolding.** For a ✗ flag, or any row with "?" under Better, go to the position before the move and spend about a minute looking for the better move. Checks, captures and threats for both sides.
3. **Unfold "Show the engine's answer".** Read Better and What your move allowed. If the punishment isn't obvious, play it out on the board. If the idea takes more than about 60 seconds to explain, write "engine idea – skip" under Better.
4. **Use the Difficulty line** (shown on flags where I lost ground). "Careless slip" means most moves were fine: a process error. "Hard spot" means only 1–3 moves held. It doesn't go in the notebook.
5. **Fill the right half** of the row: <10 s tick, Tag (see Rules), ✓ / ✗. Leave Maia blank unless this is the week's Maia game.
6. **Strike out** any of my rows with no flag: draw a line through it and write "–" under ✓/✗. It wasn't a 2-point swing.
7. **Write the CHK line:** total flags (all of them, even past 3), how many ✓ and ✗, how many rows struck. No flags → "CHK 0 flags".

### Step 4: Lesson (2 min)

1. Write one **NEXT TIME I WILL** rule from the top kept row. It must be an action at the board, such as "before moving a piece, ask whether a pawn can take it there", not "be more careful".
2. No kept rows (a clean game)? Write **KEEP:** and one habit that worked instead.
3. Add a tally mark per kept row to the weekly page.

### Shorter and longer versions

A short review beats a skipped one. Pick the version when I sit down and write it next to the game number (e.g. `#32 lite`).

| Version | Use for | Min | What to do |
| --- | --- | --- | --- |
| Full | Losses, draws, wins where I was ever losing | 15 | All four steps |
| 10-minute | A busy day | 10 | Hot notes 1, own review 4 (1–2 rows), check 3, lesson 2 |
| Lite | Clean wins (never felt worse than even) | 5 | Hot notes, then open the chesster file straight away. 0 flags → "CHK 0 flags", KEEP line, done. Otherwise a row per flag, tagged, no ✓/✗ |
| Bad day | When I'd otherwise skip | 3 | Hot notes, open the file, tag the ★ flag (or the first), one tally mark |
| Deep | One interesting game, at most weekly | 30–45 | See "Optional: move-by-move deep review" |

More than 7 games in a week: review losses first, then games I was winning and didn't win.

## Rules

Three rules v1 left to mood. Apply them the same way every game so the weekly tally means something.

### Which 3 moments to keep

Take moments in this order until there are 3. Struck rows never count.

1. **★ First material lost**, in a loss. chesster's line ends "This was the first material you lost in the game." Mark the row with ★.
2. **The result-changer:** the flag that took me from roughly even or better to losing, or from winning to not winning.
3. **Engine-only (✗) flags.** A blind spot teaches more than a mistake I already saw.
4. **Anything else**, in game order.

### Which tag

One tag per row: what I missed on the board. Speed goes in the <10 s column, not the tag.

| chesster says | Usual tag | Pick the other when |
| --- | --- | --- |
| you lost material | H | **M** if their previous move created the attack and I didn't look |
| you missed winning material | T | – |
| you missed a mate in N | T | – |
| you allowed a mate in N | K | – |
| got much worse, no material changes | O in moves 1–10 | **E** in an endgame; otherwise the closest fit |

- **H vs M:** my move put the piece en prise → H. Their move attacked it and I ignored it → M.
- **C** only when I can't name a board cause, or I was under about 2 minutes on the clock.

### Which Maia class

Weekly Maia game only, kept rows after move 5, rating 1100. The decision order is in `02-maia-mistake-classification.md`.

## The Chess.com Analysis board

chesster now finds the swings, so the Analysis board (magnifying glass on a finished game, not Game Review) is for three jobs: Step 2 with the engine hidden, playing out an engine idea in Step 3, and the deep review. The thresholds and pitfalls below are also the reasoning behind chesster's flags.

### One-time setup

- **Showing and hiding the engine:** on the website, the three dots next to the Analysis toggle turn the evaluation bar, engine lines, suggestion arrows and move feedback on or off. The app's menus may be laid out differently.
- **Settings → Engine:** show **2–3 lines**. Depth 18–20 is plenty; you don't need the deeper paid settings.
- **Settings → Interface:** turn **suggestion arrows off**, since they give the answer away. Keep move classification off.
- **Show threats (Interface):** leave it off while you search. Turn it on afterwards only to check whether you missed an opponent threat.

### Reading the numbers

| Number | Meaning |
| --- | --- |
| + / − | + means White is better, − means Black is better (Chess.com shows scores from White's side) |
| about 1 | Roughly a pawn's worth of advantage |
| ±2 | A real advantage; a swing this size is worth reviewing |
| ±5 or more | Usually winning |
| M3 | Forced mate in 3 |

### Worked example: when *not* to dig in

See `assets/chesscom-analysis-board-example.png`. After 15...exf5 in a recent game, White was +5. The engine's top line was 16.Qh5+ (+5.11), and the move played was 16.O-O (+4.86). A gap of 0.25 when you're five points up is not a lesson: both moves win. The same goes whenever the top 2–3 lines are within about half a point. The moments worth reviewing are where the number actually dropped, and how you got to +5 in the first place.

### Which swings count

- Count a swing only if it changed the likely result: from roughly even to clearly losing, or from winning to even. A drop from +9 to +6 changes almost nothing.
- The 2-point threshold comes from Studer's advice to beginners to look only at large swings that decided the game.
- Lichess uses the same idea: it labels moves by how much they cut your winning chances, not by raw points.

### Pitfalls

- **Chasing small numbers:** a −0.4 move on move 9 doesn't matter if you hung a rook on move 21.
- **Copying lines you don't understand:** if you can't explain it, skip it.
- **Looking at the answer first:** always guess before revealing.
- **Lessons from decided positions:** a big drop from +9 isn't a lesson. A drop from +1 to −2 is.

If you want a guided version on a particular game, Chess.com's Game Review (one free per day) has a Retry button at each key move, and Lichess's free "Learn from your mistakes" does the same on imported games.

## Question bank

Pick the questions that fit the moment; you don't need all of them every game. The safety questions matter most.

**Safety (every critical moment)**

1. On what move did material first change hands unfairly? Who lost what?
2. Before my bad move, what were my opponent's checks, captures and threats? Did I actually look?
3. What did my opponent's last move change? Did it attack something, or remove a defender?
4. Was the square I moved to safe? Could a piece or pawn take it? Did moving leave something else undefended?
5. After my move, was any piece of mine attacked and undefended?

**Opportunities**

6. Did my opponent's move leave something I could take for free?
7. Did I have a check, capture or fork I didn't look at?

**Clock (15+10)**

8. How much time did I have at the critical moment? Did I play it in under 10 seconds? Heisman's advice: never play a bad move fast, and use almost all your time.

**Opening (keep it short)**

9. By move 10, had I developed, castled and kept my material? Only write something if you lost material or got mated early.

**Converting and tilt**

10. If I was ahead, did I trade pieces and stop counterplay, or let it slip?
11. After my first mistake, did I tilt and speed up?

## Notebook template

Three kinds of page: the tag key inside the front cover (`../templates/tag-key.md`), half a page per game (`../templates/game-entry.md`, with field-by-field instructions and a filled-in example), and one weekly page every Sunday (`../templates/weekly-page.md`, with the drill table).

```text
#___  Date ____  W/B  W/L/D how ______   vs __________ (____)  me ____
Opening _____________________________   Clock me/opp ____ / ____
HOT  Turned at move ___: _____________________________________________
     Felt / clock: ___________________________________________________
  Mv | I played … because | Bad because     | Better … because ||<10s|Tag|✓✗|Maia
 ___ | __________________ | _______________ | ________________ || __ | _ | _ | _
 ___ | __________________ | _______________ | ________________ || __ | _ | _ | _
 ___ | __________________ | _______________ | ________________ || __ | _ | _ | _
CHK  flags ___   ✓ ___   ✗ ___   struck ___
NEXT TIME I WILL _____________________________________________________
```

The double bar splits what I write in Step 2 (left) from what I write in Step 3 (right).

## Weekly and monthly

### Weekly review (Sunday, 10 min)

Fill in the weekly page after reading last week's, find the most common tag, and pick one rule and one drill for next week. Reviewed / Played is the consistency score. The tally only helps if I look at it.

### Weekly Maia session (about 30 min)

1. Pick one game: the week's loss with the most kept rows, or the most interesting one.
2. Copy the PGN from the bottom of its chesster file and paste it into maiachess.com analysis.
3. Classify each kept row after move 5 (`02-maia-mistake-classification.md`). Write the letter in that entry's Maia column.
4. Replay the positions before any N moment against Maia at my level.
5. One round of opening drills.

### Monthly check

1. In the notebook, find the last 10 losses (chesster's `games/` folder has the full archive if a page is missing).
2. For each, take the row that decided it: the ★ row if there is one, else the result-changer.
3. Count those 10 tags. Spend most of next month's study time on the leading one, and keep opening study a small share. This follows Studer's approach of weighting study time by what actually loses games.

### Optional: move-by-move deep review

For an especially interesting game, about once a week at most, review every move instead of just 3 moments. Expect 30–45 minutes.

- Skip the first 5–6 opening moves and forced recaptures.
- At each move, engine off, ask: what did their last move change? Was there a free capture or tactic for me? After my move, was anything left hanging?
- Do the thinking on the Analysis board and type comments on moves there (Save adds it to my Chess.com Library).
- Copy only the 2–3 most important findings and the "Next time I will…" rule into the notebook.
- Good games work well for this: noticing what I did right shows which habits to keep.

## Tools and cost

You don't need to pay for anything. The Analysis board is available to free members, and Lichess is a free backup.

| Tool | Cost | Use it for |
| --- | --- | --- |
| chesster (this repo) | Free (Stockfish, local) | Flags every 2+ point swing per game, engine answer folded; archives games |
| Chess.com Analysis board | Free (Self Analysis) | Step 2 with the engine hidden; playing out engine ideas; deep reviews |
| Chess.com Game Review | 1 free per day; unlimited with Premium | Optional guided review with a Retry button at key moves |
| Lichess "Learn from your mistakes" | Free, unlimited | Backup: Share → copy PGN, paste at lichess.org/paste, request computer analysis |
| maiachess.com | Free (Lichess sign-in) | Weekly human-aware analysis, replays, opening drills (see `03-maia-guide.md`) |

Deeper engine settings (Deep, Maximum) and Cloud Analysis are Diamond-only on Chess.com. At 700 you don't need them; depth 18–20 finds every mistake that matters.

## Staying consistent

The caps are what make this sustainable: up to 3 moments, 1 lesson, 15 minutes.

- **No next game until the hot notes are written.** Two minutes protects the most valuable part of the review.
- **Run `uv run chesster` the moment I sit down to review,** so the files are ready when Step 2 ends.
- **On bad days, do the 3-minute version** rather than skipping. A short review keeps the habit alive.
- **Keep the notebook by the screen** with the tag key inside the front cover.
- **Make the weekly page a fixed Sunday slot.** Watch Reviewed / Played and the ✓ count: both can climb in a week my rating doesn't.
- **Turn each week's top tag into a board habit,** such as a final "can anything take it?" check before every move. The review only pays off if it changes my next game.

## Caveats

- The exact wording of Studer's three "why" questions comes from secondhand accounts of his video; his own articles confirm the three-moments idea.
- The 2-point threshold comes from Studer's advice for beginners. Treat it as a filter, not an exact rule.
- Chess.com menus differ between website and app, and features change often. Menu names here follow Chess.com's help pages as of October 2026.
- The example entry in `../templates/game-entry.md` is invented for illustration.
- The selection order, tag precedence and <10 s column are working rules added in v2 (October 26, 2026), not from a published source.
- chesster does not show time per move yet (planned in slice 3 of `06-build-plan.md`). Until it does, tick the <10 s column from memory and the HOT line.

## Sources

- [How do I use Game Analysis? (Chess.com Help Center)](https://support.chess.com/en/articles/8583757-how-do-i-use-game-analysis)
- [How does Game Review work? (Chess.com Help Center)](https://support.chess.com/en/articles/8584089-how-does-game-review-work)
- [What does each level of premium membership get me? (Chess.com Help Center)](https://support.chess.com/en/articles/8562418-what-does-each-level-of-premium-membership-get-me)
- [How to Analyze Your Chess Games (Chess.com, WGM Dina Belenkaya)](https://www.chess.com/article/view/how-to-analyze-your-chess-games)
- [Beginner Chess Mastery (Noël Studer, Next Level Chess)](https://nextlevelchess.com/beginner-chess-mastery/)
- [The One-Third Rule (Next Level Chess)](https://nextlevelchess.com/the-one-third-rule/)
- [Game analysis mistake (Next Level Chess)](https://nextlevelchess.com/game-analysis-mistake/)
- [Most effective chess training (Next Level Chess)](https://nextlevelchess.com/most-effective-chess-training/)
- [Better Chess Analysis: The 3x3 Method (ChemCool Chess)](https://chemcoolchess.co.za/blog/Better-Chess-Analysis-The-3x3-Method)
- [The game review habit that finally stuck (MattPlaysChess)](https://mattplayschess.com/the-game-review-habit-that-finally-stuck/)
- [Definitions: Hope Chess and Real Chess (Dan Heisman)](https://www.danheisman.com/definitions.html)
- [Thought process principles (Dan Heisman)](https://www.danheisman.com/thought-process-principles.html)
- [Learn from your mistakes (Lichess blog)](https://lichess.org/@/lichess/blog/learn-from-your-mistakes/WFvLpiQA)
- [Stuck at around 600-700 (Chess.com forum)](https://www.chess.com/forum/view/general/stuck-at-around-600-700)
