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


def _mate(n):
    return analyse.Eval(chess.engine.PovScore(chess.engine.Mate(n), chess.WHITE), [])


@pytest.mark.parametrize("before_cp, severity", [(-300, "blunder"), (-750, "mistake"), (-1200, None)])
def test_walking_into_mate_follows_lichess_grading(before_cp, severity):
    # Win% barely moves from a lost position, so the mate rule decides the label.
    game = chess.pgn.read_game(io.StringIO("1. e4 e5 *"))
    evals = [_eval(before_cp), _mate(-1), _mate(-1)]
    flags = analyse.find_flags(game, chess.WHITE, evals, mistake=20, blunder=30)
    assert [f.severity for f in flags] == ([severity] if severity else [])


def test_mate_rule_ignores_a_mate_already_on_the_board():
    assert analyse.mate_severity(_mate(-3), _mate(-1), chess.WHITE) is None


def test_count_safe_excludes_avoidable_mates():
    Cp, Mate = chess.engine.Cp, chess.engine.Mate
    # Lost position: every move is within 20 Win% points, but one walks into mate.
    assert analyse.count_safe([Cp(-750), Cp(-800), Mate(-1)], mistake=20) == 2
    assert analyse.count_safe([Mate(-3), Mate(-1)], mistake=20) == 2
    assert analyse.count_safe([Cp(0), Cp(-50), Cp(-400)], mistake=20) == 2


def test_line_formats_black_moves_with_a_space_after_dots():
    board = chess.Board()
    board.push_san("e4")
    pv = [chess.Move.from_uci(m) for m in ("e7e5", "g1f3", "b8c6")]
    assert analyse.line(board, pv, 3) == "1... e5 2. Nf3 Nc6"


def test_captured_names_the_piece():
    board = chess.Board("4k3/8/8/3n4/4P3/8/8/4K3 w - - 0 1")
    assert analyse.captured(board, chess.Move.from_uci("e4d5")) == "knight"
    assert analyse.captured(board, chess.Move.from_uci("e1e2")) == ""
