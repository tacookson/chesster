from chesster import analyse, render
from chesster.analyse import Flag


def test_eval_words_are_from_my_side():
    assert render.eval_words(30) == "about equal"
    assert render.eval_words(-120) == "slightly worse"
    assert render.eval_words(300) == "clearly better"
    assert render.eval_words(-460) == "losing"
    assert render.eval_words(100_000) == "forced mate for you"


def test_material_words():
    assert render.material_words(3) == "a piece"
    assert render.material_words(7) == "7 points of material"


def _flag(**kw):
    base = dict(ply=28, move_label="15. Bd3", severity="blunder", kind=analyse.LOST_MATERIAL, drop=38,
                before="+0.3", after="−4.6", best="Bxc6", punished_by="15... Nxe5", best_uci="b5c6",
                punished_uci="c6e5", before_cp=25, after_cp=-460,
                best_line="15. Bxc6 Qxc6 16. Qxc6 bxc6", punish_line="15... Nxe5 16. Qxd7 Nxd7",
                material=3, best_takes="knight", punish_takes="bishop", safe=(1, 37))
    base.update(kw)
    return Flag(**base)


def test_moment_reads_as_sentences():
    text = render._moment(_flag(first_material_loss=True), "White")
    assert "### Move 15 as White: you played Bd3" in text
    assert "**Blunder: you lost a piece.** This was the first material you lost in the game." in text
    assert "- **Better:** 15. Bxc6, taking the knight." in text
    assert "- **What your move allowed:** 15... Nxe5, taking your bishop." in text
    assert "about equal (+0.3) → losing (−4.6), from your side." in text
    assert "Only 1 of your 37 legal moves kept your position. This was a hard spot." in text


def test_merged_moment_lists_every_move():
    flag = _flag(move_label="15... Rab8", merged=["16... a5", "17... Rb5"], kind=analyse.DEEPER,
                 material=0, safe=None)
    text = render._moment(flag, "Black")
    assert "### Moves 15–17 as Black: you played Rab8, a5, Rb5" in text
    assert "The same idea was missed on 3 moves in a row." in text


def test_moment_shows_time_outside_the_fold():
    text = render._moment(_flag(clocks=[(4.0, 192.0)]), "White")
    assert text.index("Time: 4s on this move, 3:12 left.") < text.index("<details>")


def test_merged_moment_lists_time_per_move():
    flag = _flag(merged=["16. Be2"], clocks=[(4.0, 192.0), (75.0, 127.0)])
    assert "Time: 4s and 1m 15s on these moves, 2:07 left after the last." in render._moment(flag, "White")


def _game(game_id, end_time, time_class="rapid"):
    return dict(url=f"https://www.chess.com/game/live/{game_id}", end_time=end_time,
                time_class=time_class, rules="chess")


def test_match_ids_number_rapid_games_per_local_day():
    games = [
        _game("3", 1792807200),            # 2026-10-23 22:00 Toronto (24 Oct 02:00 UTC)
        _game("1", 1792760400),            # 2026-10-23 09:00 Toronto
        _game("2", 1792764000, "blitz"),   # blitz on the same day: no ID, not counted
        _game("4", 1792818000),            # 2026-10-24 01:00 Toronto
    ]
    assert render.match_ids(games, "America/Toronto") == {"1": "261023-1", "3": "261023-2", "4": "261024-1"}


def _info(**kw):
    base = dict(id="1", url="https://www.chess.com/game/live/1", date="2026-10-23", colour="white",
                result="loss", reason="checkmated", me="Me4tbegZ0r", my_rating=797, opponent="opp",
                opponent_rating=932, opening="Italian Game", time_control="900+10", rated=True,
                clock_me="3:12", clock_opp="8:40")
    base.update(kw)
    return render.GameInfo(**base)


def test_match_id_leads_front_matter_and_title():
    text = render.render(_info(match="261023-1"), "1. e4 *", None)
    assert text.startswith("---\nmatch: 261023-1\nurl: ")
    assert "# 261023-1 · 23 Oct 2026 · Loss as White vs opp (932)" in text


def test_no_match_id_for_non_rapid():
    text = render.render(_info(), "1. e4 *", None)
    assert "match:" not in text
    assert "# 23 Oct 2026 · Loss as White" in text


def test_coach_games_get_no_match_id():
    coach = _game("5", 1792760400) | dict(white={"username": "Me4tbegZ0r"}, black={"username": "Coach-Magnus"})
    human = _game("6", 1792764000) | dict(white={"username": "Me4tbegZ0r"}, black={"username": "opp"})
    assert render.match_ids([coach, human], "America/Toronto") == {"6": "261023-1"}
