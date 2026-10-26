import io

import chess
import chess.pgn
import pytest

from chesster import analyse
from chesster.analyse import Flag


def test_win_percent_matches_lichess_curve():
    assert analyse.win_percent(0) == 50
    assert analyse.win_percent(100) == pytest.approx(59.1, abs=0.1)
    assert analyse.win_percent(-200) == pytest.approx(32.4, abs=0.1)


def test_win_percent_clamps_at_1000_cp():
    assert analyse.win_percent(5000) == analyse.win_percent(1000)
    assert analyse.win_percent(-100_000) == analyse.win_percent(-1000)


def test_material_is_from_colour_point_of_view():
    board = chess.Board("4k3/8/8/8/8/8/8/R3K3 w - - 0 1")
    assert analyse.material(board, chess.WHITE) == 5
    assert analyse.material(board, chess.BLACK) == -5


def test_move_label_uses_dots_for_black():
    board = chess.Board()
    assert analyse.move_label(board, chess.Move.from_uci("e2e4")) == "1. e4"
    board.push_san("e4")
    assert analyse.move_label(board, chess.Move.from_uci("e7e5")) == "1... e5"


def _flag(ply, best="e2e4", punish="d7d5", severity="mistake", drop=21.0):
    return Flag(ply=ply, move_label=f"ply{ply}", severity=severity, kind=analyse.DEEPER, drop=drop,
                before="+0.0", after="−2.5", best="e4", punished_by="d5", best_uci=best,
                punished_uci=punish)


def test_merge_joins_consecutive_flags_with_same_idea():
    moments = analyse.merge([_flag(30), _flag(32, severity="blunder", drop=35), _flag(34)])
    assert len(moments) == 1
    assert moments[0].merged == ["ply32", "ply34"]
    assert moments[0].severity == "blunder"
    assert moments[0].drop == 35


def test_merge_keeps_flags_with_a_gap_or_a_different_idea():
    assert len(analyse.merge([_flag(30), _flag(34)])) == 2
    assert len(analyse.merge([_flag(30), _flag(32, best="g1f3", punish="b8c6")])) == 2


def test_merge_joins_on_shared_punishing_reply():
    assert len(analyse.merge([_flag(30), _flag(32, best="g1f3")])) == 1


def test_first_material_loss_marks_only_the_first():
    moments = [_flag(10), _flag(20), _flag(40)]
    moments[1].kind = moments[2].kind = analyse.LOST_MATERIAL
    analyse.mark_first_material_loss(moments)
    assert [m.first_material_loss for m in moments] == [False, True, False]


def _eval(cp, pv=()):
    return analyse.Eval(chess.engine.PovScore(chess.engine.Cp(cp), chess.WHITE),
                        [chess.Move.from_uci(m) for m in pv])


def test_find_flags_uses_my_point_of_view_and_thresholds():
    game = chess.pgn.read_game(io.StringIO("1. e4 e5 2. Qh5 Nc6 3. Qxf7+ Kxf7 *"))
    # Evals (White's view) before each ply and after the last one.
    evals = [_eval(30), _eval(30), _eval(30), _eval(0), _eval(0, ["h5e5"]),
             _eval(-800, ["e8f7"]), _eval(-800)]
    white = analyse.find_flags(game, chess.WHITE, evals, mistake=20, blunder=30)
    assert [(f.move_label, f.severity) for f in white] == [("3. Qxf7+", "blunder")]
    assert white[0].before == "0.0" and white[0].after == "−8.0"
    assert white[0].punished_by == "3... Kxf7"
    assert analyse.find_flags(game, chess.BLACK, evals, mistake=20, blunder=30) == []


def test_small_drops_are_not_flagged():
    game = chess.pgn.read_game(io.StringIO("1. e4 e5 *"))
    evals = [_eval(30), _eval(-50), _eval(-50)]
    assert analyse.find_flags(game, chess.WHITE, evals, mistake=20, blunder=30) == []


def test_line_formats_black_moves_with_a_space_after_dots():
    board = chess.Board()
    board.push_san("e4")
    pv = [chess.Move.from_uci(m) for m in ("e7e5", "g1f3", "b8c6")]
    assert analyse.line(board, pv, 3) == "1... e5 2. Nf3 Nc6"


def test_captured_names_the_piece():
    board = chess.Board("4k3/8/8/3n4/4P3/8/8/4K3 w - - 0 1")
    assert analyse.captured(board, chess.Move.from_uci("e4d5")) == "knight"
    assert analyse.captured(board, chess.Move.from_uci("e1e2")) == ""


# Positions: White Ka1 Qd1, Black Kh8 Rd8, White to move. The rook attacks the queen down the d-file.
HANGING = "3r3k/8/8/8/8/8/8/K2Q4 w - - 0 1"


def _mate(n, pv=()):
    return analyse.Eval(chess.engine.PovScore(chess.engine.Mate(n), chess.WHITE),
                        [chess.Move.from_uci(m) for m in pv])


def _classify(fen, played, before, after):
    board = chess.Board(fen)
    after_board = board.copy()
    after_board.push_uci(played)
    return analyse.classify(board, after_board, before, after, chess.WHITE)


def test_classify_allowed_mate_takes_precedence():
    assert _classify(HANGING, "a1b1", _mate(2, ["d1d8"]), _mate(-1, ["d8d1"])) == (analyse.ALLOWED_MATE, 1, 0)


def test_classify_missed_mate():
    assert _classify(HANGING, "a1b1", _mate(2, ["d1d8"]), _eval(100, ["h8g7"])) == (analyse.MISSED_MATE, 2, 0)


def test_classify_lost_material_before_missed_material():
    # Ka2 leaves the queen en prise; the best move Qxd8+ would have won the rook.
    kind = _classify(HANGING, "a1a2", _eval(500, ["d1d8"]), _eval(-500, ["d8d1"]))
    assert kind == (analyse.LOST_MATERIAL, None, 9)


def test_classify_missed_material():
    kind = _classify(HANGING, "d1e2", _eval(500, ["d1d8"]), _eval(0, ["h8g7"]))
    assert kind == (analyse.MISSED_MATERIAL, None, 5)


def test_classify_deeper_when_no_material_moves():
    kind = _classify(HANGING, "d1e2", _eval(300, ["a1b1"]), _eval(0, ["h8g7"]))
    assert kind == (analyse.DEEPER, None, 0)


def test_format_eval_mates_and_zero():
    assert analyse.format_eval(_mate(2), chess.WHITE) == "M2"
    assert analyse.format_eval(_mate(2), chess.BLACK) == "−M2"
    assert analyse.format_eval(_eval(-4), chess.WHITE) == "0.0"
    assert analyse.format_eval(_eval(250), chess.BLACK) == "−2.5"


def test_format_eval_checkmate_on_the_board_has_the_winners_sign():
    # After 1. f3 e5 2. g4 Qh4#: White to move and mated.
    mated = analyse.Eval(chess.engine.PovScore(chess.engine.Mate(-0), chess.WHITE), [])
    assert analyse.format_eval(mated, chess.WHITE) == "−M0"
    assert analyse.format_eval(mated, chess.BLACK) == "M0"


def _stm(cp, turn, pv=()):
    """An eval as Stockfish reports it: from the side to move."""
    return analyse.Eval(chess.engine.PovScore(chess.engine.Cp(cp), turn),
                        [chess.Move.from_uci(m) for m in pv])


def test_find_flags_with_side_to_move_evals_from_a_fen_start():
    game = chess.pgn.read_game(io.StringIO(
        '[SetUp "1"]\n[FEN "3qk3/8/8/8/8/8/8/3QK3 b - - 0 20"]\n\n20... Qd7 21. Qxd7+ *'))
    # Black to move, equal; after 20...Qd7?? White to move, a queen up.
    evals = [_stm(0, chess.BLACK, ["d8d1"]), _stm(900, chess.WHITE, ["d1d7"]), _stm(900, chess.BLACK)]
    flags = analyse.find_flags(game, chess.BLACK, evals, mistake=20, blunder=30)
    assert [(f.move_label, f.severity, f.after) for f in flags] == [("20... Qd7", "blunder", "−9.0")]
    assert flags[0].best == "Qxd1+" and flags[0].punished_by == "21. Qxd7+"


def test_find_flags_skips_forced_moves():
    game = chess.pgn.read_game(io.StringIO(
        '[SetUp "1"]\n[FEN "7k/8/6K1/8/8/8/8/5R2 b - - 0 40"]\n\n40... Kg8 41. Rf8# *'))
    evals = [_stm(0, chess.BLACK), _stm(5000, chess.WHITE), _stm(-5000, chess.BLACK)]
    assert analyse.find_flags(game, chess.BLACK, evals, mistake=20, blunder=30) == []


def test_evaluate_game_sends_the_game_so_the_engine_starts_fresh(fake_engine):
    game = chess.pgn.read_game(io.StringIO("1. e4 e5 *"))
    engine = fake_engine()
    evals = analyse.evaluate_game(game, chess.WHITE, engine, depth=1)
    assert len(evals) == 3
    assert all(call["game"] is game for call in engine.calls)


def test_evaluate_game_scores_a_final_repetition_as_a_draw(fake_engine):
    game = chess.pgn.read_game(io.StringIO("1. Nf3 Nf6 2. Ng1 Ng8 3. Nf3 Nf6 4. Ng1 Ng8 *"))
    engine = fake_engine(score=lambda board: 900)
    evals = analyse.evaluate_game(game, chess.WHITE, engine, depth=1)
    assert evals[-1].cp(chess.WHITE) == 0 and evals[-1].pv == []
    assert evals[-2].cp(chess.WHITE) == 900
    assert len(engine.calls) == len(evals) - 1


def test_merge_spans_first_eval_to_last_and_takes_the_worst():
    first = _flag(30)
    first.before, first.before_cp, first.after, first.after_cp = "+0.3", 30, "−1.5", -150
    second = _flag(32, severity="blunder", drop=35)
    second.kind, second.material, second.after, second.after_cp = analyse.LOST_MATERIAL, 3, "−6.0", -600
    [moment] = analyse.merge([first, second])
    assert (moment.before, moment.after, moment.after_cp) == ("+0.3", "−6.0", -600)
    assert (moment.severity, moment.kind, moment.material) == ("blunder", analyse.LOST_MATERIAL, 3)


def test_merge_follows_a_chain_of_shared_ideas():
    flags = [_flag(30, best="e2e4", punish="d7d5"), _flag(32, best="e2e4", punish="g8f6"),
             _flag(34, best="h2h3", punish="g8f6")]
    assert [m.merged for m in analyse.merge(flags)] == [["ply32", "ply34"]]


def test_merged_material_loss_is_marked_as_the_first():
    deeper, lost = _flag(30), _flag(32)
    lost.kind = analyse.LOST_MATERIAL
    moments = analyse.merge([deeper, lost])
    analyse.mark_first_material_loss(moments)
    assert moments[0].first_material_loss


def test_add_safe_counts_skips_missed_chances_and_never_counts_my_move(fake_engine):
    game = chess.pgn.read_game(io.StringIO("1. e4 e5 2. Nf3 *"))
    lost, missed = _flag(0), _flag(2)
    missed.kind = analyse.MISSED_MATERIAL
    engine = fake_engine(score=lambda board: 0)  # every move holds
    analyse.add_safe_counts(game, chess.WHITE, [lost, missed], engine, depth=1, mistake=20)
    assert lost.safe == (19, 20)  # 20 legal moves, all equal, minus 1. e4 itself
    assert missed.safe is None
    assert [c["multipv"] for c in engine.calls] == [20]
    assert engine.calls[0]["game"] is game


def test_mark_decided():
    def flag(before, after):
        f = _flag(0)
        f.before_cp, f.after_cp = before, after
        return f
    moments = [flag(-300, -1000), flag(1000, 300), flag(50, -400), flag(400, 100), flag(-250, -100_000)]
    analyse.mark_decided(moments, 200)
    assert [m.decided for m in moments] == ["losing", "winning", "", "", "losing"]


def test_analyse_end_to_end_with_fake_engine(fake_engine):
    # 1. e4 e5 2. Qh5 Nc6 3. Qxf7+?? Kxf7: White gives the queen for a pawn.
    game = chess.pgn.read_game(io.StringIO("1. e4 e5 2. Qh5 Nc6 3. Qxf7+ Kxf7 *"))
    engine = fake_engine(score=lambda board: -800 if board.ply() >= 5 else 30)  # lost after 3. Qxf7+
    moments = analyse.analyse(game, chess.WHITE, engine, depth=1, safe_depth=1, mistake=20, blunder=30,
                              decided_cp=200, lost=True)
    assert [(m.move_label, m.severity, m.decided) for m in moments] == [("3. Qxf7+", "blunder", "")]
