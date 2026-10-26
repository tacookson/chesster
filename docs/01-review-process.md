# Chess Game Review System

Review every rapid game with one fixed 15-minute routine, then tally mistakes weekly. Built for a ~700 Chess.com rapid (15+10) player, 5–7 games a week, notes in a paper notebook.

1. **Hot notes (2 min):** write what you think happened before touching any engine.
2. **Your own review (5–7 min):** engine off. Pick up to 3 moments where material changed hands and ask three "why" questions.
3. **Engine check (4–6 min):** Chess.com Analysis board. Guess first, then look only at swings of 2+ points.
4. **Lesson and tally (2 min):** one "Next time I will…" rule and a tally mark per error type.

At 700, almost every game is decided by safety: hung pieces, missed opponent threats and missed free material. The routine is built to catch those and skip opening theory and strategy.

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

Four steps, about 15 minutes, in the same order every time. The engine always comes last, so you train your own eyes first.

### Step 1: Hot notes (2 min)

Right after the game, before any analysis, fill in the header and two lines: where you think the game turned, and how you felt and used your clock. Once you've seen engine lines, you can't recover what you were actually thinking.

### Step 2: Your own review, engine off (5–7 min)

1. Open the game in the Analysis board with the engine lines, evaluation bar and arrows turned off (see the engine section for how).
2. Step through quickly. Stop every time material changed hands, or a check or mate threat appeared.
3. Pick **up to 3** of these moments. In a loss, always include the **first** moment you lost material, not just the final blunder.
4. For each moment, write one short line for each of the three "why" questions, then add an error tag:
   - Why did I choose that move?
   - Why was it not good?
   - What would have been better, and why?
5. If you can't find a moment, write "?" and let the engine find it. That still counts as a finding.

This is GM Noël Studer's "3×3" method (three moments, three whys each), trimmed to fit 700: *up to* three moments and only one lesson per game.

### Step 3: Engine check (4–6 min)

Turn the engine on and check only the big swings. The full routine is in the next section. If you use chesster, its game file already lists them under "3. Engine check", folded until you open it; open it only after Step 2.

### Step 4: Lesson and tally (2 min)

Write **one** "Next time I will…" rule. Make it an action you can do at the board, such as "Before I move a piece, check whether a pawn can take it there." Avoid vague rules like "be more careful." Then add tally marks to the weekly page.

### Shorter and longer versions

- **10 minutes:** 1 min hot notes, 4 min own review (1–2 moments), 3 min engine, 2 min lesson.
- **20 minutes:** add 5 minutes to play out the engine's idea at each moment, plus a quick check of your first 8–10 moves in the Explorer.
- **Bad day (3 minutes):** hot notes, one engine look at the biggest swing, one tally mark.

## Using the engine (Chess.com Analysis board)

Use the engine to check your own review, not replace it: guess first, then reveal, and only look where the number jumped 2+ points. This uses the Analysis board (magnifying glass on a finished game), not Game Review.

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

### The routine (4–6 min)

1. **Find the swings.** Engine on, lines hidden. Tap Forward through the game watching only the top number. Write down every one of your moves after which it moved 2+ points against you, or where you missed a 2+ point chance. Ignore smaller changes.
2. **Guess first.** At each swing, go back to the position *before* your move. Cover the engine lines with your thumb and spend about a minute looking for a better move. Check captures, checks and threats for both sides.
3. **Reveal the first move or two only.** Read the start of the top line. Is it a capture, a check or a threat? That tells you your tag (H, M, T or K).
4. **Find what punished you.** Play the move you actually made, then look at the engine's top reply for your opponent. That reply usually shows exactly what you missed, such as a free piece or a fork.
5. **Test your in-game idea.** If you considered a different move during the game, play it on the board and watch the number. Two or three tries at most.
6. **Stop at one sentence.** If you can explain the lesson in one sentence, write it down. If the line is long quiet maneuvering you can't explain within about 60 seconds, write "engine idea – skip."
7. **Mark ✓ or ✗.** ✓ if you had already found this moment in Step 2, ✗ if only the engine found it. Add any ✗ moment to your notes (still 3 moments maximum).

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

Copy the tag key inside the front cover, use half a page per game, and keep one weekly page. Templates are in `../templates/`.

**Choosing the drill from your tally:**

- Lots of **H or M:** hanging-piece puzzles, plus a "can anything take it?" check before every move.
- Lots of **T:** tactics puzzles (forks, pins).
- Lots of **C:** spend at least 30 seconds on any move involving a capture or check.
- Lots of **E:** practice basic winning endgames.

## Example entry

A filled-in entry takes about half a page. This one is an invented example.

```text
#261014-1  B  Result L  Opp 712  Opening: Italian
Clock left (me/opp): 6:40 / 9:15
HOT: Turned at move 14 – lost my knight, then got mated
     Felt fine, played 14...Nd4 fast. Tilted after.
MOMENTS
 14 | ...Nd4, to hit queen | c3 pawn takes d4 | ...Be7 (develop) | H | ✓
 19 | ...a6, "waiting"     | Qxf7+ coming     | ...Qe7 guards f7 | M | ✓
 22 | ...Rd8               | ...Qxb2 won rook | ...Qxb2          | T | ✗
ENGINE: 22...Qxb2 found only by engine (+0.3 → −2.8).
        Ignored 5 small changes under 1 point.
NEXT TIME I WILL: before moving a piece, ask "can a PAWN take it there?"
```

**Reading it:** two of the three moments were "Hope Chess" (H and M). The engine-only moment (T) points to tactics puzzles as a secondary drill. Tally added: H I, M I, T I.

## Which games, and the bigger reviews

Review every rapid game, up to about 7 a week, at two depths. Losses get the full routine; clean wins get a quick pass.

- **Full routine (15 min):** losses, draws, and games where you were clearly winning but didn't win.
- **Lite routine (5 min):** clean wins. Hot notes, a quick engine scan for big swings, tally only. Wins often hide a mistake your opponent failed to punish.
- **More than 7 games a week:** review losses first, then near-misses.

### Weekly review (Sunday, 10 min)

Fill in the weekly page, find your most common tag, and pick one rule and one drill for next week. The tally only helps if you look at it.

### Monthly check

Take your last 10 losses and find the mistake that actually decided each one. Sort them by tag. Spend most of next month's study time on the leading category, and keep opening study a small share. This follows Studer's approach of weighting study time by what actually loses you games.

### Optional: move-by-move deep review

For an especially interesting game, about once a week at most, you can review every move instead of just 3 moments. Expect 30–45 minutes.

- Skip the first 5–6 opening moves and forced recaptures.
- At each move, engine off, ask: what did their last move change? Was there a free capture or tactic for me? After my move, was anything left hanging?
- Do the thinking on the Analysis board and type comments on moves there (Save adds it to your Chess.com Library).
- Copy only the 2–3 most important findings and your "Next time I will…" rule into the notebook.
- Good games work well for this: noticing what you did right shows you which habits to keep.

## Tools and cost

You don't need to pay for anything. The Analysis board is available to free members, and Lichess is a free backup.

| Tool | Cost | Use it for |
| --- | --- | --- |
| Chess.com Analysis board | Free (Self Analysis) | Your main engine step: eval number, 2–3 lines, testing moves |
| Chess.com Game Review | 1 free per day; unlimited with Premium | Optional guided review with a Retry button at key moves |
| Lichess "Learn from your mistakes" | Free, unlimited | Backup: Share → copy PGN, paste at lichess.org/paste, request computer analysis |
| maiachess.com | Free (Lichess sign-in) | Weekly human-aware analysis, replays, opening drills (see `03-maia-guide.md`) |

Deeper engine settings (Deep, Maximum) and Cloud Analysis are Diamond-only on Chess.com. At 700 you don't need them; depth 18–20 finds every mistake that matters.

## Staying consistent

The caps are what make this sustainable: up to 3 moments, 1 lesson, 15 minutes.

- **No next game until the hot notes are written.** Two minutes protects the most valuable part of the review.
- **On bad days, do the 3-minute version** rather than skipping. A short review keeps the habit alive.
- **Keep the notebook by the screen** with the tag key inside the front cover.
- **Make the weekly page a fixed Sunday slot.**
- **Track your ✓ count.** More moments found on your own is visible progress, even in weeks your rating is flat.
- **Turn each week's top tag into a board habit,** such as a final "can anything take it?" check before every move. The review only pays off if it changes your next game.

## Caveats

- The exact wording of Studer's three "why" questions comes from secondhand accounts of his video; his own articles confirm the three-moments idea.
- The 2-point threshold comes from Studer's advice for beginners. Treat it as a filter, not an exact rule.
- Chess.com menus differ between website and app, and features change often. Menu names here follow Chess.com's help pages as of October 2026.
- The example entry is invented for illustration.

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
