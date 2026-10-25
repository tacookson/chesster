"""Stockfish evaluation of my moves: flags, type labels, merging and safe-move counts."""

import math
from dataclasses import dataclass, field

import chess
import chess.engine

# Lichess's curve (scalachess eval.scala), with cp clamped to ±1000 and mate counted as ±1000.
MULTIPLIER = -0.00368208
CP_CLAMP = 1000
VALUES = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3, chess.ROOK: 5, chess.QUEEN: 9}

LOST_MATERIAL = "lost material"
MISSED_MATERIAL = "missed material"
MISSED_MATE = "missed mate"
ALLOWED_MATE = "allowed mate"
DEEPER = "deeper"
# Flags where I lost ground, as opposed to failing to cash in an opponent's error.
LOST_GROUND = {LOST_MATERIAL, ALLOWED_MATE, DEEPER}


def win_percent(cp: int) -> float:
    cp = max(-CP_CLAMP, min(CP_CLAMP, cp))
    return 50 + 50 * (2 / (1 + math.exp(MULTIPLIER * cp)) - 1)


def material(board: chess.Board, colour: chess.Color) -> int:
    """Material balance from `colour`'s point of view."""
    return sum(
        VALUES.get(piece.piece_type, 0) * (1 if piece.color == colour else -1)
        for piece in board.piece_map().values()
    )


@dataclass
class Eval:
    score: chess.engine.PovScore
    pv: list[chess.Move]

    def cp(self, colour: chess.Color) -> int:
        return self.score.pov(colour).score(mate_score=100_000)

    def mate(self, colour: chess.Color) -> int | None:
        return self.score.pov(colour).mate()


@dataclass
class Flag:
    ply: int                    # index of my move in the mainline
    move_label: str             # e.g. "15. Bd3" or "15... Nxe5"
    severity: str               # "mistake" or "blunder"
    kind: str                   # one of the type labels above
    drop: float                 # Win% points lost
    before: str                 # eval before my move, my point of view
    after: str                  # eval after my move, my point of view
    best: str                   # Stockfish's best move (SAN)
    punished_by: str            # opponent's best reply to my move (SAN)
    best_uci: str
    punished_uci: str
    before_cp: int = 0          # my point of view; mate as ±100000
    after_cp: int = 0
    best_line: str = ""         # first moves of the best line, e.g. "15. Bxc6 Qxc6 16. Qxc6 bxc6"
    punish_line: str = ""       # first moves after my move, e.g. "15... Nxe5 16. Qxd7 Nxd7"
    material: int = 0           # points lost (lost material) or missed (missed material)
    best_takes: str = ""        # piece the best move captures, e.g. "knight"
    punish_takes: str = ""      # piece of mine the punishing reply captures
    safe: tuple[int, int] | None = None  # (safe moves, legal moves), lost-ground flags only
    mate_in: int | None = None  # moves to mate, for missed or allowed mate
    merged: list[str] = field(default_factory=list)  # later moves merged into this moment
    first_material_loss: bool = False


def format_eval(e: Eval, colour: chess.Color) -> str:
    mate = e.mate(colour)
    if mate is not None:
        return f"M{mate}" if mate > 0 else f"−M{-mate}"
    cp = e.score.pov(colour).score()
    if round(cp / 100, 1) == 0:
        return "0.0"
    return f"{cp / 100:+.1f}".replace("-", "−")


def move_label(board: chess.Board, move: chess.Move) -> str:
    dots = "." if board.turn == chess.WHITE else "..."
    return f"{board.fullmove_number}{dots} {board.san(move)}"


def captured(board: chess.Board, move: chess.Move | None) -> str:
    """Name of the piece `move` captures, or "" if it isn't a capture."""
    if move is None or move not in board.legal_moves or not board.is_capture(move):
        return ""
    if board.is_en_passant(move):
        return "pawn"
    return chess.piece_name(board.piece_at(move.to_square).piece_type)


def line(board: chess.Board, pv: list[chess.Move], plies: int) -> str:
    """The first `plies` moves of a line in SAN, e.g. "15... Nxe5 16. Qxd7 Nxd7"."""
    b = board.copy()
    moves = []
    for move in pv[:plies]:
        if move not in b.legal_moves:
            break
        moves.append(move)
        b.push(move)
    return board.variation_san(moves).replace("...", "... ") if moves else ""


def _material_after(board: chess.Board, pv: list[chess.Move], plies: int, colour: chess.Color) -> int:
    b = board.copy()
    for move in pv[:plies]:
        if move not in b.legal_moves:
            break
        b.push(move)
    return material(b, colour)


def classify(before_board: chess.Board, after_board: chess.Board, before: Eval, after: Eval,
             me: chess.Color) -> tuple[str, int | None, int]:
    """Type label, mate distance and material (points lost or missed) for a flagged move.

    Precedence: mate, then lost material, then missed material. Any missed mate is a missed
    chance, whatever its length; the mate distance shows whether it was simple.
    """
    best_mate = before.mate(me)
    after_mate = after.mate(me)
    if after_mate is not None and after_mate < 0 and (best_mate is None or best_mate > 0):
        return ALLOWED_MATE, -after_mate, 0
    if best_mate is not None and best_mate > 0 and (after_mate is None or after_mate <= 0):
        return MISSED_MATE, best_mate, 0
    start = material(before_board, me)
    # Opponent, me, opponent, me: did I end up 2+ points down within 2 moves?
    lost = start - _material_after(after_board, after.pv, 4, me)
    if lost >= 2:
        return LOST_MATERIAL, None, lost
    # Me, opponent, me, opponent, me: did the best line win 2+ points within 3 moves?
    missed = _material_after(before_board, before.pv, 5, me) - start
    if missed >= 2:
        return MISSED_MATERIAL, None, missed
    return DEEPER, None, 0


def evaluate_game(game, me: chess.Color, engine: chess.engine.SimpleEngine, depth: int) -> list[Eval]:
    """Evaluate every position in the mainline once (N moves → N+1 evals)."""
    board = game.board()
    evals = []
    for node in [None, *game.mainline()]:
        if node is not None:
            board.push(node.move)
        info = engine.analyse(board, chess.engine.Limit(depth=depth))
        evals.append(Eval(info["score"], info.get("pv", [])))
    return evals


def mate_severity(before: Eval, after: Eval, me: chess.Color) -> str | None:
    """Lichess's rule for walking into a forced mate (lila Advice.scala, MateCreated).

    Blunder, or mistake if I was already below −7; below −9.99 Lichess calls it an
    inaccuracy, which chesster hides.
    """
    after_mate = after.mate(me)
    if before.mate(me) is not None or after_mate is None or after_mate >= 0:
        return None
    cp = before.cp(me)
    if cp < -999:
        return None
    return "mistake" if cp < -700 else "blunder"


SEVERITIES = [None, "mistake", "blunder"]


def find_flags(game, me: chess.Color, evals: list[Eval], mistake: float, blunder: float) -> list[Flag]:
    board = game.board()
    flags = []
    for ply, node in enumerate(game.mainline()):
        move = node.move
        if board.turn == me:
            before, after = evals[ply], evals[ply + 1]
            drop = win_percent(before.cp(me)) - win_percent(after.cp(me))
            by_drop = "blunder" if drop >= blunder else "mistake" if drop >= mistake else None
            severity = max(by_drop, mate_severity(before, after, me), key=SEVERITIES.index)
            if severity:
                after_board = board.copy()
                after_board.push(move)
                best = before.pv[0] if before.pv else move
                punish = after.pv[0] if after.pv else None
                kind, mate_in, points = classify(board, after_board, before, after, me)
                flags.append(Flag(
                    ply=ply,
                    move_label=move_label(board, move),
                    severity=severity,
                    kind=kind,
                    mate_in=mate_in,
                    material=points,
                    drop=drop,
                    before=format_eval(before, me),
                    after=format_eval(after, me),
                    best=board.san(best),
                    punished_by=move_label(after_board, punish) if punish else "",
                    best_uci=best.uci(),
                    punished_uci=punish.uci() if punish else "",
                    before_cp=before.cp(me),
                    after_cp=after.cp(me),
                    best_line=line(board, before.pv or [best], 4),
                    best_takes=captured(board, best),
                    punish_takes=captured(after_board, punish),
                    punish_line=line(after_board, after.pv, 3),
                ))
        board.push(move)
    return flags


def merge(flags: list[Flag]) -> list[Flag]:
    """Merge flags on my consecutive moves that share a best move or a punishing reply."""
    moments: list[Flag] = []
    for flag in flags:
        if moments:
            last = moments[-1]
            last_ply = last.ply + 2 * len(last.merged)
            same_idea = flag.best_uci == last.best_uci or (
                flag.punished_uci and flag.punished_uci == last.punished_uci)
            if flag.ply == last_ply + 2 and same_idea:
                last.merged.append(flag.move_label)
                if flag.severity == "blunder":
                    last.severity = "blunder"
                last.drop = max(last.drop, flag.drop)
                continue
        moments.append(flag)
    return moments


def add_safe_counts(game, me: chess.Color, moments: list[Flag], engine: chess.engine.SimpleEngine,
                    depth: int, mistake: float) -> None:
    """Count legal moves within the mistake threshold of the best move, for lost-ground flags."""
    wanted = {m.ply: m for m in moments if m.kind in LOST_GROUND}
    board = game.board()
    for ply, node in enumerate(game.mainline()):
        if ply in wanted:
            legal = board.legal_moves.count()
            infos = engine.analyse(board, chess.engine.Limit(depth=depth), multipv=legal)
            wanted[ply].safe = (count_safe([i["score"].pov(me) for i in infos], mistake), legal)
        board.push(node.move)


def count_safe(scores: list[chess.engine.Score], mistake: float) -> int:
    """Moves within the mistake threshold of the best one, not counting walks into an avoidable mate."""
    percents = [win_percent(s.score(mate_score=100_000)) for s in scores]
    best = max(percents)
    mated = [s.mate() is not None and s.mate() < 0 for s in scores]
    avoidable = not all(mated)
    return sum(1 for p, m in zip(percents, mated) if best - p < mistake and not (m and avoidable))


def mark_first_material_loss(moments: list[Flag]) -> None:
    for moment in moments:
        if moment.kind == LOST_MATERIAL:
            moment.first_material_loss = True
            return


def analyse(game, me: chess.Color, engine: chess.engine.SimpleEngine, depth: int, safe_depth: int,
            mistake: float, blunder: float, lost: bool) -> list[Flag]:
    evals = evaluate_game(game, me, engine, depth)
    moments = merge(find_flags(game, me, evals, mistake, blunder))
    add_safe_counts(game, me, moments, engine, safe_depth, mistake)
    if lost:
        mark_first_material_loss(moments)
    return moments
