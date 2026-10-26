# Tag Key

Copy inside the notebook's front cover.

```text
TAGS   H hung a piece        M missed their threat   T missed my tactic
       K king safety/mate    C clock                 O opening   E endgame
CHECK  ✓ I found it first   ✗ engine only   – struck: not a swing
MAIA   R lapse (my level finds it)   N next level (+300)
       L later (+300–800)            X hard (never by +800)
KEEP   ★ first material lost (loss)  → result-changer → ✗ flags → rest
```

## Error tags (one per moment)

Tag what I missed on the board. Speed goes in the <10 s column, not the tag.

| Tag | Meaning |
| --- | --- |
| H | Hung a piece: my move put a piece where it could be taken for free |
| M | Missed opponent's threat: their move attacked something and I didn't check their checks, captures and threats |
| T | Missed my own tactic, mate or free material |
| K | King safety or mate: back rank, exposed king, allowed a mate |
| C | Clock: no board cause I can name, or under about 2 minutes left |
| O | Opening principle broken: lost material or development in moves 1–10 |
| E | Endgame: failed to convert a winning position |

## Engine marks

| Mark | Meaning |
| --- | --- |
| ✓ | I found this moment myself before opening chesster's file |
| ✗ | Only chesster found it |
| – | My moment, but chesster didn't flag it: struck, not tallied |

## Maia classes (weekly Maia game only, rating 1100)

Stop at the first that fits. Details in `../docs/02-maia-mistake-classification.md`.

| Class | Moves by Rating shows | Fix |
| --- | --- | --- |
| R | Best move already above mine at 1100, or my move isn't in the graph | Process: blunder check, clock |
| N | Best move overtakes mine by 1400 | Study the pattern; replay the position |
| L | Best move overtakes mine between 1400 and 1900 | Note it, don't drill |
| X | Best move never overtakes mine by 1900 | Skip |
